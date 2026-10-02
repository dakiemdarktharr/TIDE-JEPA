"""Small attention network written for this project from PyTorch primitives."""

import copy
import math

import torch
from torch import nn

from .config import ModelConfig
from .data import BYTE_OFFSET


class AttentionBlock(nn.Module):
    def __init__(self, width: int, heads: int):
        super().__init__()
        self.heads, self.head_width = heads, width // heads
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.qkv = nn.Linear(width, 3 * width)
        self.out = nn.Linear(width, width)
        self.ff = nn.Sequential(nn.Linear(width, 4 * width), nn.GELU(), nn.Linear(4 * width, width))

    def forward(self, x, valid, causal=False):
        batch, length, width = x.shape
        q, k, v = self.qkv(self.norm1(x)).chunk(3, dim=-1)
        q, k, v = [t.reshape(batch, length, self.heads, self.head_width).transpose(1, 2) for t in (q, k, v)]
        scores = q @ k.transpose(-1, -2) / math.sqrt(self.head_width)
        allowed = valid[:, None, None, :].expand(batch, 1, length, length)
        if causal:
            allowed = allowed & torch.ones(length, length, device=x.device, dtype=torch.bool).tril()
        scores = scores.masked_fill(~allowed, torch.finfo(scores.dtype).min)
        weights = scores.softmax(dim=-1) * allowed
        # For all-masked padding queries, zero attention rather than NaNs.
        weights = weights / weights.sum(dim=-1, keepdim=True).clamp_min(1e-9)
        attended = (weights @ v).transpose(1, 2).reshape(batch, length, width)
        x = x + self.out(attended)
        x = x + self.ff(self.norm2(x))
        return x * valid.unsqueeze(-1)


class CrossAttention(nn.Module):
    """Decoder-to-source attention that keeps source roles available to generation."""

    def __init__(self, width: int, heads: int):
        super().__init__()
        self.heads, self.head_width = heads, width // heads
        self.norm = nn.LayerNorm(width)
        self.query = nn.Linear(width, width)
        self.key_value = nn.Linear(width, 2 * width)
        self.output = nn.Linear(width, width)

    def forward(self, x, memory, memory_valid):
        batch, target_length, _ = x.shape
        source_length = memory.shape[1]
        q = self.query(self.norm(x)).reshape(
            batch, target_length, self.heads, self.head_width).transpose(1, 2)
        k, v = self.key_value(memory).chunk(2, dim=-1)
        k, v = [value.reshape(batch, source_length, self.heads, self.head_width).transpose(1, 2)
                for value in (k, v)]
        scores = q @ k.transpose(-1, -2) / math.sqrt(self.head_width)
        allowed = memory_valid[:, None, None, :]
        weights = scores.masked_fill(~allowed, torch.finfo(scores.dtype).min).softmax(dim=-1)
        attended = (weights @ v).transpose(1, 2).reshape(batch, target_length, x.shape[-1])
        return x + self.output(attended)


class SequenceEncoder(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg
        self.tokens = nn.Embedding(cfg.vocab_size, cfg.width, padding_idx=cfg.pad_id)
        self.positions = nn.Embedding(cfg.max_length, cfg.width)
        self.blocks = nn.ModuleList([AttentionBlock(cfg.width, cfg.heads) for _ in range(cfg.layers)])
        self.norm = nn.LayerNorm(cfg.width)

    def encode(self, tokens):
        if tokens.dtype != torch.long or tokens.ndim != 2 or tokens.shape[1] > self.cfg.max_length:
            raise ValueError("encoder expects int64 token IDs with [batch, length] shape within max_length")
        if (tokens < 0).any() or (tokens >= self.cfg.vocab_size).any():
            raise ValueError("encoder token ID outside configured vocabulary")
        valid = tokens != self.cfg.pad_id
        if not valid.any(dim=1).all():
            raise ValueError("encoder expects nonempty padded sequences within max_length")
        padding = ~valid
        if (padding[:, :-1] & valid[:, 1:]).any():
            raise ValueError("encoder supports right padding only")
        positions = torch.arange(tokens.shape[1], device=tokens.device)
        x = self.tokens(tokens) + self.positions(positions)
        for block in self.blocks:
            x = block(x, valid)
        x = self.norm(x) * valid.unsqueeze(-1)
        pooled = x.sum(dim=1) / valid.sum(dim=1, keepdim=True)
        return pooled, x, valid

    def forward(self, tokens):
        return self.encode(tokens)[0]


class TIDEJEPA(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg
        self.online = SequenceEncoder(cfg)
        self.target = copy.deepcopy(self.online).requires_grad_(False)
        self.actions = nn.Embedding(cfg.action_count, cfg.width)
        self.languages = nn.Embedding(len(cfg.languages), cfg.width)
        self.transition = nn.Sequential(nn.Linear(3 * cfg.width, 2 * cfg.width), nn.GELU(), nn.Linear(2 * cfg.width, cfg.width))
        # First milestone compares the shared latent basis directly. A freely
        # learned comparison head could minimize alignment merely by shrinking.
        self.canonical = nn.Identity()
        self.decoder_tokens = nn.Embedding(cfg.vocab_size, cfg.width, padding_idx=cfg.pad_id)
        self.decoder_positions = nn.Embedding(cfg.max_length, cfg.width)
        self.decoder = nn.ModuleList([AttentionBlock(cfg.width, cfg.heads) for _ in range(cfg.layers)])
        self.decoder_cross_attention = nn.ModuleList(
            [CrossAttention(cfg.width, cfg.heads) for _ in range(cfg.layers)])
        self.decoder_norm = nn.LayerNorm(cfg.width)
        self.output = nn.Linear(cfg.width, cfg.vocab_size)
        self.target.eval()

    def train(self, mode=True):
        super().train(mode)
        self.target.eval()
        return self

    def predict(self, state, action_ids, language_ids):
        context = torch.cat((state, self.actions(action_ids), self.languages(language_ids)), dim=-1)
        return state + self.transition(context)

    def predict_path(
        self,
        state: torch.Tensor,
        action_ids: torch.Tensor,
        language_ids: torch.Tensor,
    ) -> torch.Tensor:
        """Apply one ordered semantic-action path to each state in the batch."""
        if state.ndim != 2 or state.shape[0] == 0:
            raise ValueError("path prediction expects a nonempty [batch, width] state")
        if action_ids.dtype != torch.long or action_ids.ndim != 1 or action_ids.numel() == 0:
            raise ValueError("a prediction path must be a nonempty int64 action sequence")
        if language_ids.dtype != torch.long or language_ids.shape != (state.shape[0],):
            raise ValueError("path language IDs must have [batch] shape and int64 dtype")
        if action_ids.device != state.device or language_ids.device != state.device:
            raise ValueError("states and action/language IDs must share a device")
        if (action_ids < 0).any() or (action_ids >= self.cfg.action_count).any():
            raise ValueError("path action ID outside configured inventory")
        if (language_ids < 0).any() or (language_ids >= len(self.cfg.languages)).any():
            raise ValueError("path language ID outside configured registry")
        predicted = state
        for action_id in action_ids:
            predicted = self.predict(predicted, action_id.expand(state.shape[0]), language_ids)
        return predicted

    def decode(self, decoder_input, predicted, language_ids, encoder_memory=None, source_valid=None):
        if decoder_input.ndim != 2 or not 0 < decoder_input.shape[1] <= self.cfg.max_length:
            raise ValueError("decoder input length is invalid")
        valid = decoder_input != self.cfg.pad_id
        positions = torch.arange(decoder_input.shape[1], device=decoder_input.device)
        x = self.decoder_tokens(decoder_input) + self.decoder_positions(positions)
        x = x + (predicted + self.languages(language_ids)).unsqueeze(1)
        if encoder_memory is not None:
            if (encoder_memory.ndim != 3 or encoder_memory.shape[0] != decoder_input.shape[0]
                    or encoder_memory.shape[2] != self.cfg.width or source_valid is None
                    or source_valid.shape != encoder_memory.shape[:2] or source_valid.dtype != torch.bool
                    or not source_valid.any(dim=1).all() or encoder_memory.device != x.device
                    or source_valid.device != x.device):
                raise ValueError("encoder memory and valid-token mask must match decoder batch and width")
        elif source_valid is not None:
            raise ValueError("source_valid requires encoder_memory")
        for index, block in enumerate(self.decoder):
            x = block(x, valid, causal=True)
            if encoder_memory is not None:
                x = self.decoder_cross_attention[index](x, encoder_memory, source_valid)
        return self.output(self.decoder_norm(x))

    def forward(self, source, decoder_input, action_ids, language_ids):
        state, encoder_memory, source_valid = self.online.encode(source)
        predicted = self.predict(state, action_ids, language_ids)
        logits = self.decode(decoder_input, predicted, language_ids, encoder_memory, source_valid)
        return logits, state, predicted

    @torch.no_grad()
    def update_target(self, momentum: float):
        if not 0 <= momentum <= 1:
            raise ValueError("EMA momentum must lie in [0, 1]")
        for target, online in zip(self.target.parameters(), self.online.parameters()):
            target.mul_(momentum).add_(online, alpha=1 - momentum)

    @torch.no_grad()
    def generate(self, source, action_ids, language_ids, bos_id: int, eos_id: int, max_new_tokens: int):
        self._validate_generation_args(bos_id, eos_id, max_new_tokens)
        self._validate_generation_inputs(source, action_ids, language_ids, path=False)
        state, encoder_memory, source_valid = self.online.encode(source)
        predicted = self.predict(state, action_ids, language_ids)
        return self._generate_from_prediction(predicted, language_ids, bos_id, eos_id,
                                              max_new_tokens, encoder_memory, source_valid)

    @torch.no_grad()
    def generate_path(
        self,
        source: torch.Tensor,
        action_ids: torch.Tensor,
        language_ids: torch.Tensor,
        bos_id: int,
        eos_id: int,
        max_new_tokens: int,
    ) -> torch.Tensor:
        """Generate from a shared ordered action path for the supplied batch."""
        self._validate_generation_args(bos_id, eos_id, max_new_tokens)
        self._validate_generation_inputs(source, action_ids, language_ids, path=True)
        state, encoder_memory, source_valid = self.online.encode(source)
        predicted = self.predict_path(state, action_ids, language_ids)
        return self._generate_from_prediction(predicted, language_ids, bos_id, eos_id,
                                              max_new_tokens, encoder_memory, source_valid)

    def _validate_generation_args(self, bos_id: int, eos_id: int, max_new_tokens: int) -> None:
        if type(bos_id) is not int or bos_id != self.cfg.bos_id:
            raise ValueError("generation BOS must equal the configured BOS token")
        if type(eos_id) is not int:
            raise ValueError("generation EOS must be an integer token ID")
        if type(max_new_tokens) is not int or not 0 < max_new_tokens < self.cfg.max_length:
            raise ValueError("max_new_tokens must leave room for BOS within max_length")
        if not (0 <= bos_id < self.cfg.vocab_size and 0 <= eos_id < self.cfg.vocab_size):
            raise ValueError("BOS and EOS must belong to the supplied vocabulary")
        if len({bos_id, eos_id, self.cfg.pad_id}) != 3:
            raise ValueError("BOS, EOS, and PAD must be distinct")

    def _validate_generation_inputs(self, source, action_ids, language_ids, *, path: bool) -> None:
        if source.dtype != torch.long or source.ndim != 2 or source.shape[0] < 1:
            raise ValueError("source must be an int64 [batch, length] tensor")
        if language_ids.dtype != torch.long or language_ids.shape != (source.shape[0],):
            raise ValueError("language IDs must be an int64 vector matching the source batch")
        if (language_ids < 0).any() or (language_ids >= len(self.cfg.languages)).any():
            raise ValueError("language ID outside configured registry")
        expected_shape = (source.shape[0],) if not path else None
        if action_ids.dtype != torch.long or (not path and action_ids.shape != expected_shape):
            raise ValueError("single-action IDs must be an int64 vector matching the source batch")
        if path and (action_ids.ndim != 1 or not 1 <= len(action_ids) <= 8):
            raise ValueError("action path must contain from 1 through 8 action IDs")
        if (action_ids < 0).any() or (action_ids >= self.cfg.action_count).any():
            raise ValueError("action ID outside configured inventory")

    def _generate_from_prediction(
        self,
        predicted: torch.Tensor,
        language_ids: torch.Tensor,
        bos_id: int,
        eos_id: int,
        max_new_tokens: int,
        encoder_memory: torch.Tensor,
        source_valid: torch.Tensor,
    ) -> torch.Tensor:
        tokens = torch.full((predicted.shape[0], 1), bos_id, dtype=torch.long, device=predicted.device)
        done = torch.zeros(predicted.shape[0], dtype=torch.bool, device=predicted.device)
        # UTF-8 DFA state per example: continuation count and bounds for the
        # next byte. EOS is available only at a codepoint boundary. Multi-byte
        # leads are masked unless there is room to finish them and emit EOS.
        constrain_utf8 = self.cfg.vocab_size == BYTE_OFFSET + 256
        utf8_states = [[0, 0x80, 0xBF] for _ in range(predicted.shape[0])]
        for step in range(max_new_tokens):
            remaining = max_new_tokens - step
            logits = self.decode(tokens, predicted, language_ids, encoder_memory, source_valid)[:, -1].clone()
            for row, (needed, lower, upper) in enumerate(utf8_states):
                if not constrain_utf8:
                    allowed_ids = [token for token in range(self.cfg.vocab_size)
                                   if token not in {self.cfg.pad_id, bos_id}]
                elif done[row]:
                    allowed_ids = [self.cfg.pad_id]
                elif needed:
                    if remaining < needed + 1:
                        raise RuntimeError("UTF-8 decoder state cannot finish within its token budget")
                    allowed_ids = [BYTE_OFFSET + value for value in range(lower, upper + 1)]
                elif remaining == 1:
                    allowed_ids = [eos_id]
                else:
                    allowed_ids = [BYTE_OFFSET + value for value in range(0x00, 0x80)]
                    if remaining >= 3:  # lead + one continuation + EOS
                        allowed_ids.extend(BYTE_OFFSET + value for value in range(0xC2, 0xE0))
                    if remaining >= 4:  # lead + two continuations + EOS
                        allowed_ids.extend(BYTE_OFFSET + value for value in range(0xE0, 0xF0))
                    if remaining >= 5:  # lead + three continuations + EOS
                        allowed_ids.extend(BYTE_OFFSET + value for value in range(0xF0, 0xF5))
                    allowed_ids.append(eos_id)
                masked = torch.full_like(logits[row], -torch.inf)
                masked[allowed_ids] = logits[row, allowed_ids]
                logits[row] = masked
            next_token = logits.argmax(dim=-1).masked_fill(done, self.cfg.pad_id)
            for row, token_id in enumerate(next_token.tolist()):
                if done[row] or token_id == eos_id or not constrain_utf8:
                    continue
                byte = token_id - BYTE_OFFSET
                needed, lower, upper = utf8_states[row]
                if needed:
                    if not lower <= byte <= upper:
                        raise RuntimeError("UTF-8 decoder emitted an invalid continuation byte")
                    utf8_states[row] = [needed - 1, 0x80, 0xBF]
                elif byte <= 0x7F:
                    utf8_states[row] = [0, 0x80, 0xBF]
                elif 0xC2 <= byte <= 0xDF:
                    utf8_states[row] = [1, 0x80, 0xBF]
                elif byte == 0xE0:
                    utf8_states[row] = [2, 0xA0, 0xBF]
                elif 0xE1 <= byte <= 0xEC or 0xEE <= byte <= 0xEF:
                    utf8_states[row] = [2, 0x80, 0xBF]
                elif byte == 0xED:
                    utf8_states[row] = [2, 0x80, 0x9F]
                elif byte == 0xF0:
                    utf8_states[row] = [3, 0x90, 0xBF]
                elif 0xF1 <= byte <= 0xF3:
                    utf8_states[row] = [3, 0x80, 0xBF]
                elif byte == 0xF4:
                    utf8_states[row] = [3, 0x80, 0x8F]
                else:
                    raise RuntimeError("UTF-8 decoder emitted an invalid lead byte")
            tokens = torch.cat((tokens, next_token[:, None]), dim=1)
            done |= next_token == eos_id
            if done.all():
                break
        return tokens
