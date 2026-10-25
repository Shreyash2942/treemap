"""Repeatable iterative traversals yielding nodes from a subtree root.

Traversals assume a valid tree that is not mutated during iteration. Each call
creates a fresh iterator. Empty subtrees yield no nodes.
"""

from __future__ import annotations

from collections.abc import Iterator

from treemap.core.node import K, TreeNode, V


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


def preorder(root: TreeNode[K, V] | None) -> Iterator[TreeNode[K, V]]:
    """Yield root, left, right in O(n) time and O(h) auxiliary space."""
    if root is None:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        yield node
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)


def postorder(root: TreeNode[K, V] | None) -> Iterator[TreeNode[K, V]]:
    """Yield left, right, root in O(n) time and O(h) auxiliary space."""
    if root is None:
        return
    stack = [(root, False)]
    while stack:
        node, visited = stack.pop()
        if visited:
            yield node
            continue
        stack.append((node, True))
        if node.right is not None:
            stack.append((node.right, False))
        if node.left is not None:
            stack.append((node.left, False))
