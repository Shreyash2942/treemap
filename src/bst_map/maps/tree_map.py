"""An ordered key-value map backed by the project's unbalanced BST."""

from __future__ import annotations

from typing import Generic, TypeVar, overload

from bst_map.core.bst import BinarySearchTree
from bst_map.core.node import K, TreeNode, V
from bst_map.core.traversals import inorder

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

    @property
    def root(self) -> TreeNode[K, V] | None:
        """Return the BST root for traversal/analysis; do not mutate its links or keys."""
        return self._tree.root

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

    def remove(self, key: K) -> V:
        """Remove an entry and return its value; raise `KeyError` if absent."""
        return self._tree.delete(key)

    def contains_key(self, key: K) -> bool:
        """Return whether key exists, including entries whose value is `None`."""
        return self._tree.search(key) is not None

    def keys(self) -> list[K]:
        """Return a new list of keys in sorted order in O(n) time."""
        return [node.key for node in inorder(self._tree.root)]

    def values(self) -> list[V]:
        """Return a new list of values ordered by key, retaining value references."""
        return [node.value for node in inorder(self._tree.root)]

    def items(self) -> list[tuple[K, V]]:
        """Return a new list of key-value tuples sorted by key in O(n) time."""
        return [(node.key, node.value) for node in inorder(self._tree.root)]
