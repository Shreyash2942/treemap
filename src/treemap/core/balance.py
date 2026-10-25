"""Iterative height and balance analysis; reports imbalance without rotations.

Height counts edges: an empty tree has height -1 and a leaf has height 0.
Every node is inspected, even when an earlier subtree is already unbalanced.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic

from treemap.core.node import K, TreeNode, V


@dataclass(frozen=True, slots=True)
class BalanceReport(Generic[K]):
    """Tree height, root balance factor, and unbalanced keys in post-order."""

    height: int
    balance_factor: int
    unbalanced_keys: tuple[K, ...]

    @property
    def is_balanced(self) -> bool:
        """Return whether every node's absolute balance factor is at most 1."""
        return not self.unbalanced_keys


def analyze_balance(root: TreeNode[K, V] | None) -> BalanceReport[K]:
    """Inspect all subtrees in one O(n) pass without mutation or recursion.

    Pending work and child heights use O(h) auxiliary space, plus O(u) output
    space for u unbalanced keys. Balance factor is height(left) - height(right).
    The empty tree is balanced with height -1 and root balance factor 0.
    """
    stack: list[tuple[TreeNode[K, V] | None, bool]] = [(root, False)]
    heights: list[int] = []
    unbalanced: list[K] = []
    factor = 0
    while stack:
        node, visited = stack.pop()
        if node is None:
            heights.append(-1)
        elif not visited:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))
        else:
            right_height = heights.pop()
            left_height = heights.pop()
            factor = left_height - right_height
            if abs(factor) > 1:
                unbalanced.append(node.key)
            heights.append(1 + max(left_height, right_height))
    return BalanceReport(
        height=heights[0], balance_factor=factor, unbalanced_keys=tuple(unbalanced)
    )


def height(root: TreeNode[K, V] | None) -> int:
    """Return subtree height in edges; return -1 for an empty subtree."""
    return analyze_balance(root).height


def balance_factor(root: TreeNode[K, V] | None) -> int:
    """Return height(left) - height(right); return 0 for an empty subtree."""
    return analyze_balance(root).balance_factor


def is_balanced(root: TreeNode[K, V] | None) -> bool:
    """Return whether all subtrees satisfy the height-balance condition."""
    return analyze_balance(root).is_balanced
