"""Iterative operations on BST subtrees, independent of tree size tracking."""

from __future__ import annotations

from bst_map.core.node import K, TreeNode, V


def minimum_node(root: TreeNode[K, V] | None) -> TreeNode[K, V]:
    """Return the leftmost node; raise `ValueError` for an empty subtree."""
    if root is None:
        raise ValueError("minimum is undefined for an empty tree")
    current = root
    while current.left is not None:
        current = current.left
    return current


def maximum_node(root: TreeNode[K, V] | None) -> TreeNode[K, V]:
    """Return the rightmost node; raise `ValueError` for an empty subtree."""
    if root is None:
        raise ValueError("maximum is undefined for an empty tree")
    current = root
    while current.right is not None:
        current = current.right
    return current


def delete_node(root: TreeNode[K, V] | None, key: K) -> tuple[TreeNode[K, V] | None, V]:
    """Remove key and return the new subtree root and original value.

    Raise `KeyError(key)` without changing the subtree if the key is absent.
    For two children, copy the in-order successor entry and unlink that successor.
    Time is O(h) and auxiliary space is O(1).
    """
    parent: TreeNode[K, V] | None = None
    current = root
    while current is not None:
        if key == current.key:
            break
        parent = current
        current = current.left if key < current.key else current.right

    if current is None:
        raise KeyError(key)

    removed_value = current.value
    if current.left is not None and current.right is not None:
        successor_parent = current
        successor = current.right
        while successor.left is not None:
            successor_parent = successor
            successor = successor.left

        current.key = successor.key
        current.value = successor.value
        if successor_parent is current:
            successor_parent.right = successor.right
        else:
            successor_parent.left = successor.right
        return root, removed_value

    replacement = current.left if current.left is not None else current.right
    if parent is None:
        return replacement, removed_value
    if parent.left is current:
        parent.left = replacement
    else:
        parent.right = replacement
    return root, removed_value
