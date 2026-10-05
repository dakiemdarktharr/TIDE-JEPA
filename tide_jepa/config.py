"""Explicit registry; identifiers are project-local, not language-code claims."""

from dataclasses import dataclass


LANGUAGES = ("vi", "en", "cham_phan_rang")


@dataclass(frozen=True)
class ModelConfig:
    vocab_size: int
    action_count: int
    width: int = 64
    heads: int = 4
    layers: int = 2
    max_length: int = 128
    pad_id: int = 0
    bos_id: int = 1
    languages: tuple[str, ...] = LANGUAGES
    source_pointer_decoder: bool = False

    def __post_init__(self):
        for key in ("vocab_size", "action_count", "width", "heads", "layers", "max_length"):
            value = getattr(self, key)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{key} must be a positive integer")
        if self.width % self.heads:
            raise ValueError("width must be divisible by heads")
        for key in ("pad_id", "bos_id"):
            value = getattr(self, key)
            if type(value) is not int or not 0 <= value < self.vocab_size:
                raise ValueError(f"{key} must be an integer in the vocabulary")
        if self.bos_id == self.pad_id:
            raise ValueError("bos_id must differ from pad_id")
        if not self.languages or len(set(self.languages)) != len(self.languages):
            raise ValueError("languages must be nonempty and unique")
        if type(self.source_pointer_decoder) is not bool:
            raise ValueError("source_pointer_decoder must be boolean")
