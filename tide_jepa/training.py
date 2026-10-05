"""One-batch trainer and initial matched-input objective controls."""

from dataclasses import dataclass
import math

import torch
from torch.nn import functional as F

from tide_jepa.schema import (
    Edge,
    EdgePair,
    EdgePath,
    Inventory,
    PathPair,
    validate_pair,
    validate_path,
    validate_path_pair,
)


@dataclass
class Batch:
    source: torch.Tensor
    target: torch.Tensor
    decoder_input: torch.Tensor
    labels: torch.Tensor
    action_ids: torch.Tensor
    language_ids: torch.Tensor
    edges: tuple[Edge, ...]
    copy_mask: torch.Tensor | None = None
    pairs: tuple[EdgePair, ...] = ()
    paths: tuple[EdgePath, ...] = ()
    path_pairs: tuple[PathPair, ...] = ()
    edge_weights: torch.Tensor | None = None

    def validate(self, cfg, inventory):
        size = len(self.edges)
        if not size or len(inventory.actions) != cfg.action_count:
            raise ValueError("nonempty edges and matching inventory size are required")
        tensors = (self.source, self.target, self.decoder_input, self.labels, self.action_ids, self.language_ids)
        if any(t.dtype != torch.long or t.device != self.source.device for t in tensors):
            raise ValueError("all batch tensors must be int64 on one device")
        for tokens in tensors[:4]:
            if tokens.ndim != 2 or tokens.shape[0] != size or not 0 < tokens.shape[1] <= cfg.max_length:
                raise ValueError("token tensors must have [edges, length] shape")
            if (tokens < 0).any() or (tokens >= cfg.vocab_size).any():
                raise ValueError("token ID outside configured vocabulary")
            if not (tokens != cfg.pad_id).any(dim=1).all():
                raise ValueError("each token row must contain at least one nonpadding token")
            # The interface uses right padding so positions and teacher forcing agree.
            padding = tokens == cfg.pad_id
            if (padding[:, :-1] & ~padding[:, 1:]).any():
                raise ValueError("only right-padded token rows are supported")
        if self.decoder_input.shape != self.labels.shape:
            raise ValueError("decoder inputs and labels must have identical shapes")
        if self.copy_mask is not None:
            if (self.copy_mask.dtype != torch.bool or self.copy_mask.device != self.source.device
                    or self.copy_mask.shape != self.labels.shape):
                raise ValueError("copy mask must be a boolean tensor matching labels on the batch device")
            if (self.copy_mask & (self.labels == cfg.pad_id)).any():
                raise ValueError("copy mask cannot select padding labels")
        if self.edge_weights is not None:
            if (self.edge_weights.shape != (size,) or self.edge_weights.device != self.source.device
                    or not self.edge_weights.is_floating_point()):
                raise ValueError("edge weights must be a floating-point [edges] tensor on the batch device")
            if not torch.isfinite(self.edge_weights).all() or (self.edge_weights <= 0).any():
                raise ValueError("edge weights must be finite and positive")
        if not torch.equal(self.target, self.labels):
            raise ValueError("EMA target tokens and next-token labels must describe the same sequence")
        if not (self.decoder_input[:, 0] == cfg.bos_id).all():
            raise ValueError("every decoder input must start with the configured BOS token")
        if not torch.equal(self.decoder_input[:, 1:], self.labels[:, :-1]):
            raise ValueError("teacher-forcing inputs must be the labels shifted right after BOS")
        if self.action_ids.shape != (size,) or self.language_ids.shape != (size,):
            raise ValueError("action/language IDs must have [edges] shape")
        for index, edge in enumerate(self.edges):
            action_id = inventory.require(edge.language, edge.action)
            if edge.language not in cfg.languages:
                raise ValueError("edge language is not configured")
            if self.action_ids[index].item() != action_id or self.language_ids[index].item() != cfg.languages.index(edge.language):
                raise ValueError("tensor IDs disagree with the annotation metadata")
        for pair in self.pairs:
            validate_pair(pair, self.edges, inventory)
        for path in self.paths:
            validate_path(path, self.edges, inventory)
            for edge_index in path.edge_indices:
                edge = self.edges[edge_index]
                expected_action_id = inventory.require(edge.language, edge.action)
                expected_language_id = cfg.languages.index(edge.language)
                if self.action_ids[edge_index].item() != expected_action_id:
                    raise ValueError("path action metadata disagrees with its tensor ID")
                if self.language_ids[edge_index].item() != expected_language_id:
                    raise ValueError("path language metadata disagrees with its tensor ID")
        for pair in self.path_pairs:
            validate_path_pair(pair, self.paths, self.edges, inventory)


@dataclass(frozen=True)
class Objective:
    mode: str = "tide"
    latent_objective_weight: float = 1.0
    jepa_weight: float = 1.0
    alignment_weight: float = 1.0
    variance_weight: float = 0.1
    path_weight: float = 1.0
    path_token_weight: float = 1.0
    path_alignment_weight: float = 1.0
    source_copy_weight: float = 0.0
    compute_source_copy_term: bool = False
    ema_momentum: float = 0.99
    grad_clip: float = 1.0

    def __post_init__(self):
        if self.mode not in {"token_only", "generic_jepa", "static_alignment", "tide"}:
            raise ValueError("unknown objective mode")
        weights = (
            self.latent_objective_weight,
            self.jepa_weight,
            self.alignment_weight,
            self.variance_weight,
            self.path_weight,
            self.path_token_weight,
            self.path_alignment_weight,
            self.source_copy_weight,
        )
        if any(not math.isfinite(v) or v < 0 for v in weights):
            raise ValueError("loss weights must be finite and nonnegative")
        if type(self.compute_source_copy_term) is not bool:
            raise ValueError("compute_source_copy_term must be boolean")
        if not 0 <= self.ema_momentum <= 1 or not math.isfinite(self.grad_clip) or self.grad_clip <= 0:
            raise ValueError("invalid EMA momentum or gradient clip")


def compute_loss(model, batch: Batch, inventory: Inventory, objective: Objective):
    batch.validate(model.cfg, inventory)
    logits, state, predicted = model(batch.source, batch.decoder_input, batch.action_ids, batch.language_ids)
    edge_weights = (batch.edge_weights if batch.edge_weights is not None
                    else torch.ones(len(batch.edges), dtype=logits.dtype, device=logits.device))
    per_token = F.cross_entropy(logits.transpose(1, 2), batch.labels,
                                ignore_index=model.cfg.pad_id, reduction="none")
    token_mask = batch.labels != model.cfg.pad_id
    token_weights = token_mask.to(logits.dtype) * edge_weights[:, None]
    token_count = token_weights.sum()
    token = (per_token * token_weights).sum() / token_count.clamp_min(1.0)
    copy_token = token.new_zeros(())
    copy_token_count = token.new_zeros(())
    if objective.source_copy_weight or objective.compute_source_copy_term:
        if batch.copy_mask is None:
            if objective.source_copy_weight:
                raise ValueError("source-copy objective requires a token-alignment mask")
        else:
            copy_mask = batch.copy_mask & (batch.labels != model.cfg.pad_id)
            copy_weights = copy_mask.to(logits.dtype) * edge_weights[:, None]
            copy_token_count = copy_weights.sum()
            if copy_token_count.item() == 0 and objective.source_copy_weight:
                raise ValueError("source-copy objective has no aligned target tokens")
            if copy_token_count.item() > 0:
                copy_token = (per_token * copy_weights).sum() / copy_token_count
    zero = token.new_zeros(())
    jepa, alignment, variance = zero, zero, zero
    path_jepa, path_token, path_alignment = zero, zero, zero
    edge_weight_sum = edge_weights.sum()
    weighted_state_mean = (state * edge_weights[:, None]).sum(dim=0) / edge_weight_sum
    spread = (((state - weighted_state_mean).square() * edge_weights[:, None]).sum(dim=0)
              / edge_weight_sum).add(1e-4).sqrt()
    target = None
    if objective.mode != "token_only":
        with torch.no_grad():
            target = model.target(batch.target)
        edge_jepa = F.mse_loss(predicted, target, reduction="none").mean(dim=-1)
        jepa = (edge_jepa * edge_weights).sum() / edge_weight_sum
        variance = F.relu(1.0 - spread).mean()
        if objective.mode in {"static_alignment", "tide"} and batch.pairs:
            canonical_source = model.canonical(state)
            canonical_predicted = model.canonical(predicted)
            aligned = canonical_predicted if objective.mode == "static_alignment" else canonical_predicted - canonical_source
            pair_losses = torch.stack([F.mse_loss(aligned[p.left], aligned[p.right]) for p in batch.pairs])
            pair_weights = torch.stack([(edge_weights[p.left] + edge_weights[p.right]) / 2
                                        for p in batch.pairs])
            alignment = (pair_losses * pair_weights).sum() / pair_weights.sum()
    if batch.paths:
        path_predictions = []
        path_starts = []
        path_targets = []
        path_token_losses = []
        for path in batch.paths:
            first_index, final_index = path.edge_indices[0], path.edge_indices[-1]
            action_sequence = batch.action_ids[list(path.edge_indices)]
            language_id = batch.language_ids[first_index : first_index + 1]
            composed = model.predict_path(state[first_index : first_index + 1], action_sequence, language_id)
            path_predictions.append(composed.squeeze(0))
            path_starts.append(state[first_index])
            if target is not None:
                path_targets.append(target[final_index])
            _, source_memory, source_valid = model.online.encode(
                batch.source[first_index : first_index + 1])
            composed_logits = model.decode(
                batch.decoder_input[final_index : final_index + 1],
                composed,
                batch.language_ids[final_index : final_index + 1],
                source_memory,
                source_valid,
                batch.source[first_index : first_index + 1],
            )
            path_token_losses.append(
                F.cross_entropy(
                    composed_logits.flatten(0, 1),
                    batch.labels[final_index : final_index + 1].flatten(),
                    ignore_index=model.cfg.pad_id,
                )
            )
        path_predictions = torch.stack(path_predictions)
        path_starts = torch.stack(path_starts)
        path_token = torch.stack(path_token_losses).mean()
        if target is not None:
            path_targets = torch.stack(path_targets)
            path_jepa = F.mse_loss(path_predictions, path_targets)
        if objective.mode in {"static_alignment", "tide"} and batch.path_pairs:
            composed = model.canonical(path_predictions)
            if objective.mode == "tide":
                composed = composed - model.canonical(path_starts)
            path_alignment = torch.stack(
                [F.mse_loss(composed[p.left], composed[p.right]) for p in batch.path_pairs]
            ).mean()
    total = (
        token
        + objective.latent_objective_weight * objective.jepa_weight * jepa
        + objective.latent_objective_weight * objective.alignment_weight * alignment
        + objective.latent_objective_weight * objective.variance_weight * variance
        + objective.latent_objective_weight * objective.path_weight * path_jepa
        + objective.path_token_weight * path_token
        + objective.latent_objective_weight * objective.path_alignment_weight * path_alignment
        + objective.source_copy_weight * copy_token
    )
    denominators = {
        "token_count": float(token_count.detach()),
        "copy_token": copy_token,
        "copy_token_count": float(copy_token_count.detach()),
        "edge_count": float(edge_weight_sum.detach()),
        "alignment_count": float(pair_weights.sum().detach()) if objective.mode in {"static_alignment", "tide"} and batch.pairs else 0.0,
        "path_count": len(batch.paths),
        "path_alignment_count": len(batch.path_pairs),
    }
    return total, {
        "loss": total,
        "token": token,
        "jepa": jepa,
        "alignment": alignment,
        "variance": variance,
        "path_jepa": path_jepa,
        "path_token": path_token,
        "path_alignment": path_alignment,
        "latent_std": spread.mean(),
        **denominators,
    }


class Trainer:
    def __init__(self, model, inventory: Inventory, objective: Objective, learning_rate=1e-3):
        self.model, self.inventory, self.objective = model, inventory, objective
        self.optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=learning_rate)
        self.steps = 0

    def step(self, batch: Batch):
        self.model.train()
        self.optimizer.zero_grad(set_to_none=True)
        loss, values = compute_loss(self.model, batch, self.inventory, self.objective)
        if not torch.isfinite(loss):
            raise FloatingPointError("nonfinite loss; no optimizer or EMA update performed")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.objective.grad_clip, error_if_nonfinite=True)
        self.optimizer.step()
        self.model.update_target(self.objective.ema_momentum)
        self.steps += 1
        return {key: (float(value.detach()) if isinstance(value, torch.Tensor) else value)
                for key, value in values.items()}
