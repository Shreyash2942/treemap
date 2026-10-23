"""An ordered key-value map backed by the project's unbalanced BST."""

from __future__ import annotations

from typing import Generic, TypeVar, overload

from bst_map.core.bst import BinarySearchTree
from bst_map.core.node import K, V

D = TypeVar("D")


class TreeMap(Generic[K, V]):
    """Store unique comparable keys with unrestricted values, including `None`.

    Keys follow the BST's stable total-order contract. Lookup and mutation take
    O(h) time for tree height h; this map does not rebalance its underlying tree.
    """

    def __init__(self) -> None:
        self._tree: BinarySearchTree[K, V] = BinarySearchTree()

    def __len__(self) -> int:
        """Return the number of unique keys in O(1) time."""
        return len(self._tree)

    def put(self, key: K, value: V) -> None:
        """Insert or update an entry; updates preserve the number of keys."""
        self._tree.insert(key, value)

    @overload
    def get(self, key: K) -> V | None: ...

    @overload
    def get(self, key: K, default: D) -> V | D: ...

    def get(self, key: K, default: D | None = None) -> V | D | None:
        """Return the stored value, or default only when key is absent."""
        node = self._tree.search(key)
        return default if node is None else node.value
