"""Language-neutral annotation contracts; no linguistic judgments are inferred."""

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Action:
    kind: str
    value: str

    def __post_init__(self):
        if (
            not isinstance(self.kind, str)
            or not self.kind.strip()
            or not isinstance(self.value, str)
            or not self.value.strip()
        ):
            raise ValueError("an action needs a kind and value")


@dataclass(frozen=True)
class Inventory:
    actions: tuple[Action, ...]
    approved_by_language: Mapping[str, frozenset[Action]]

    def __post_init__(self):
        if not self.actions or len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be nonempty and unique")
        if any(not set(items) <= set(self.actions) for items in self.approved_by_language.values()):
            raise ValueError("approved actions must occur in the inventory")

    def require(self, language: str, action: Action) -> int:
        if action not in self.approved_by_language.get(language, frozenset()):
            raise ValueError(f"action is not approved for {language}")
        return self.actions.index(action)


@dataclass(frozen=True)
class Edge:
    language: str
    source_frame: str
    target_frame: str
    action: Action

    def __post_init__(self):
        if not self.language or not self.source_frame or not self.target_frame:
            raise ValueError("edges require language and nonempty semantic frame IDs")


@dataclass(frozen=True)
class EdgePair:
    left: int
    right: int
    relation: str


@dataclass(frozen=True)
class EdgePath:
    """An ordered, within-language chain of licensed single-action edges."""

    edge_indices: tuple[int, ...]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.edge_indices, tuple)
            or len(self.edge_indices) < 2
            or any(type(index) is not int or index < 0 for index in self.edge_indices)
            or len(set(self.edge_indices)) != len(self.edge_indices)
        ):
            raise ValueError("a path needs at least two distinct, nonnegative edge indices")


@dataclass(frozen=True)
class PathPair:
    """An explicit cross-language correspondence between two action paths."""

    left: int
    right: int
    relation: str


def validate_pair(pair: EdgePair, edges: tuple[Edge, ...], inventory: Inventory) -> None:
    if type(pair.left) is not int or type(pair.right) is not int:
        raise ValueError("alignment indices must be integers")
    if pair.relation != "same_event":
        raise ValueError("only explicitly licensed same_event pairs may be aligned")
    if pair.left == pair.right or not (0 <= pair.left < len(edges) and 0 <= pair.right < len(edges)):
        raise ValueError("alignment needs two distinct valid edge indices")
    left, right = edges[pair.left], edges[pair.right]
    for edge in (left, right):
        inventory.require(edge.language, edge.action)
    if left.language == right.language:
        raise ValueError("cross-language alignment requires different languages")
    if (left.source_frame, left.target_frame, left.action) != (right.source_frame, right.target_frame, right.action):
        raise ValueError("aligned edges must share source, target, and action semantics")


def validate_path(path: EdgePath, edges: tuple[Edge, ...], inventory: Inventory) -> None:
    """Validate licensing, language consistency, and frame continuity of a path."""
    if any(index >= len(edges) for index in path.edge_indices):
        raise ValueError("path refers to an edge outside the batch")
    selected = tuple(edges[index] for index in path.edge_indices)
    language = selected[0].language
    for edge in selected:
        inventory.require(edge.language, edge.action)
        if edge.language != language:
            raise ValueError("a path must stay within one language")
    for current, following in zip(selected, selected[1:]):
        if current.target_frame != following.source_frame:
            raise ValueError("path edges must form a continuous semantic-frame chain")


def validate_path_pair(
    pair: PathPair,
    paths: tuple[EdgePath, ...],
    edges: tuple[Edge, ...],
    inventory: Inventory,
) -> None:
    """Validate an explicitly aligned pair of semantically matching paths."""
    if pair.relation != "same_event":
        raise ValueError("only explicitly licensed same_event paths may be aligned")
    if (
        type(pair.left) is not int
        or type(pair.right) is not int
        or pair.left == pair.right
        or not (0 <= pair.left < len(paths) and 0 <= pair.right < len(paths))
    ):
        raise ValueError("path alignment needs two distinct valid path indices")
    left_path, right_path = paths[pair.left], paths[pair.right]
    validate_path(left_path, edges, inventory)
    validate_path(right_path, edges, inventory)
    left = tuple(edges[index] for index in left_path.edge_indices)
    right = tuple(edges[index] for index in right_path.edge_indices)
    if left[0].language == right[0].language:
        raise ValueError("cross-language path alignment requires different languages")
    left_frames = (left[0].source_frame,) + tuple(edge.target_frame for edge in left)
    right_frames = (right[0].source_frame,) + tuple(edge.target_frame for edge in right)
    if left_frames != right_frames or tuple(edge.action for edge in left) != tuple(edge.action for edge in right):
        raise ValueError("aligned paths must share frame and action semantics at every step")
