"""Repeatable iterative traversals yielding nodes from a subtree root.

Traversals assume a valid tree that is not mutated during iteration. Each call
creates a fresh iterator. Empty subtrees yield no nodes.
"""

from __future__ import annotations

from collections.abc import Iterator

from bst_map.core.node import K, TreeNode, V


def inorder(root: TreeNode[K, V] | None) -> Iterator[TreeNode[K, V]]:
    """Yield left, root, right: sorted keys for a BST, in O(n) time/O(h) space."""
    stack: list[TreeNode[K, V]] = []
    current = root
    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        yield current
        current = current.right
