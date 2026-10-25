"""Deterministic, iterative ASCII diagrams with explicit left/right branches."""

from __future__ import annotations

from treemap.core.node import K, TreeNode, V


def render_tree(root: TreeNode[K, V] | None, *, show_values: bool = False) -> str:
    """Return a top-down diagram, or `(empty)` for an empty tree.

    Children are labeled L/R, with left visited before right. `ascii()` keeps
    labels on one line and escapes non-ASCII characters. Values are optional;
    reproducibility requires stable key/value representations. No nodes change.

    Work is proportional to emitted text, which can be O(n*h) for indentation
    in deep trees. The explicit traversal stack uses O(h) entries.
    """
    if root is None:
        return "(empty)"
    lines: list[str] = []
    stack = [(root, "", "", True)]
    while stack:
        node, prefix, side, last = stack.pop()
        label = ascii(node.key)
        if show_values:
            label += f": {ascii(node.value)}"
        if side:
            connector = "`-- " if last else "|-- "
            lines.append(f"{prefix}{connector}{side}: {label}")
            child_prefix = prefix + ("    " if last else "|   ")
        else:
            lines.append(label)
            child_prefix = ""
        if node.right is not None:
            stack.append((node.right, child_prefix, "R", True))
        if node.left is not None:
            stack.append((node.left, child_prefix, "L", node.right is None))
    return "\n".join(lines)
