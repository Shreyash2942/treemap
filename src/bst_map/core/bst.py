"""Iterative, unbalanced binary search tree with unique comparable keys."""

from __future__ import annotations

from typing import Generic

from bst_map.core.node import K, TreeNode, V
from bst_map.core.operations import delete_node


class BinarySearchTree(Generic[K, V]):
    """Store key-value pairs in strict BST order without automatic balancing.

    Keys must satisfy the total-order contract in `core.node.Comparable`.
    Operations take O(h) time for tree height h and O(1) auxiliary space.
    """

    def __init__(self) -> None:
        self._root: TreeNode[K, V] | None = None
        self._size = 0

    @property
    def root(self) -> TreeNode[K, V] | None:
        """Return the root for inspection, or `None` for an empty tree."""
        return self._root

    def __len__(self) -> int:
        """Return the number of distinct keys in O(1) time."""
        return self._size

    def insert(self, key: K, value: V) -> None:
        """Insert a key or replace its value; an update does not change size."""
        if self._root is None:
            self._root = TreeNode(key, value)
            self._size = 1
            return

        current = self._root
        while True:
            if key == current.key:
                current.value = value
                return
            if key < current.key:
                if current.left is None:
                    current.left = TreeNode(key, value)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(key, value)
                    break
                current = current.right
        self._size += 1

    def search(self, key: K) -> TreeNode[K, V] | None:
        """Return the matching node, or `None` if key is absent.

        Returning a node keeps a stored `None` value distinct from absence.
        """
        current = self._root
        while current is not None:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    def delete(self, key: K) -> V:
        """Remove key and return its old value; raise `KeyError` if absent.

        Two-child deletion uses the in-order successor. A failed deletion
        leaves the root and size unchanged.
        """
        self._root, removed_value = delete_node(self._root, key)
        self._size -= 1
        return removed_value
