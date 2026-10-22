"""Generic nodes and the key-ordering contract shared by the BST modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Protocol, Self, TypeVar


class Comparable(Protocol):
    """Keys must support `<` and equality with a consistent total ordering.

    All keys within one tree must be mutually comparable. Stored keys must not
    change their ordering. Unordered keys (for example, NaN) are unsupported.
    """

    def __lt__(self, other: Self, /) -> bool:
        """Return whether this key precedes another key."""
        ...


K = TypeVar("K", bound=Comparable)
V = TypeVar("V")


@dataclass(slots=True, eq=False)
class TreeNode(Generic[K, V]):
    """A key-value entry with optional children; nodes compare by identity.

    Values need not be comparable and may be `None`. Child links default to
    `None` independently for each node. Direct mutation of a tree's node keys
    or links is unsupported; use the tree's public operations instead.
    """

    key: K
    value: V
    left: TreeNode[K, V] | None = None
    right: TreeNode[K, V] | None = None
