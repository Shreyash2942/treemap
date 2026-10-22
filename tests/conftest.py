"""Shared fixtures and an independent, iterative BST invariant validator."""

from __future__ import annotations

import pytest

from bst_map import BinarySearchTree, TreeNode
from bst_map.core.node import K, V


def assert_bst_valid(tree: BinarySearchTree[K, V]) -> None:
    """Verify strict ancestor bounds, unique node ownership, and recorded size.

    Carry both bounds through every branch: checking only a node's immediate
    children would miss descendants that violate a more distant ancestor.
    Bound nodes avoid reserving any key value as a sentinel.
    """
    stack: list[tuple[TreeNode[K, V] | None, TreeNode[K, V] | None, TreeNode[K, V] | None]]
    stack = [(tree.root, None, None)]
    seen: set[int] = set()
    while stack:
        node, lower, upper = stack.pop()
        if node is None:
            continue
        assert id(node) not in seen, "Cycle or shared child detected"
        seen.add(id(node))
        if lower is not None:
            assert lower.key < node.key, "Key violates strict lower ancestor bound"
        if upper is not None:
            assert node.key < upper.key, "Key violates strict upper ancestor bound"
        stack.append((node.left, lower, node))
        stack.append((node.right, node, upper))
    assert len(seen) == len(tree), "Recorded size differs from reachable node count"


@pytest.fixture
def sample_tree() -> BinarySearchTree[int, str]:
    """Return the seven-node example from the README."""
    tree = BinarySearchTree[int, str]()
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key, f"value-{key}")
    return tree
