"""Original TIDE-JEPA research infrastructure; importing this package needs no torch."""

from .config import ModelConfig
from .data import (
    BYTE_VOCAB_SIZE,
    DATA_SCHEMA_VERSION,
    CorpusRecord,
    SplitManifest,
    UTF8ByteTokenizer,
    build_batch,
    dataset_fingerprint,
    grouped_split,
    read_jsonl,
    validate_records,
    write_split_manifest,
)
from .schema import (
    Action,
    Edge,
    EdgePair,
    EdgePath,
    Inventory,
    PathPair,
    validate_pair,
    validate_path,
    validate_path_pair,
)

__all__ = [
    "Action",
    "BYTE_VOCAB_SIZE",
    "CorpusRecord",
    "DATA_SCHEMA_VERSION",
    "Edge",
    "EdgePair",
    "EdgePath",
    "Inventory",
    "ModelConfig",
    "PathPair",
    "SplitManifest",
    "UTF8ByteTokenizer",
    "build_batch",
    "dataset_fingerprint",
    "grouped_split",
    "read_jsonl",
    "validate_pair",
    "validate_path",
    "validate_path_pair",
    "validate_records",
    "write_split_manifest",
]
