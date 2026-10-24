"""Golden diagrams and renderer behavior for empty, one-sided, and deep trees."""

import sys
from pathlib import Path

import pytest
from conftest import assert_bst_valid

from bst_map import BinarySearchTree, TreeNode
from bst_map.visualization import render_tree


def test_empty_tree():
    assert render_tree(None) == "(empty)"


def test_single_node_and_optional_values():
    root = TreeNode("key", None)
    assert render_tree(root) == "'key'"
    assert render_tree(root, show_values=True) == "'key': None"


@pytest.mark.parametrize(("child_key", "side"), [(5, "L"), (15, "R")])
def test_one_child_retains_its_side(child_key, side):
    tree = BinarySearchTree()
    tree.insert(10, None)
    tree.insert(child_key, None)
    assert render_tree(tree.root) == f"10\n`-- {side}: {child_key}"
    assert_bst_valid(tree)


def test_checked_in_before_and_after_diagrams_match_actual_successor_deletion(sample_tree):
    diagrams = Path(__file__).resolve().parents[1] / "docs" / "diagrams"
    before = render_tree(sample_tree.root)
    assert before == (diagrams / "tree_before.txt").read_text(encoding="utf-8").rstrip("\n")
    assert render_tree(sample_tree.root) == before
    assert sample_tree.delete(30) == "value-30"
    assert sample_tree.root.left.key == 40
    after = render_tree(sample_tree.root)
    assert after == (diagrams / "tree_after.txt").read_text(encoding="utf-8").rstrip("\n")
    assert_bst_valid(sample_tree)


def test_labels_escape_newlines_and_non_ascii_characters():
    rendered = render_tree(TreeNode("line\n\u00e9", {"tab": "\t"}), show_values=True)
    assert rendered.isascii()
    assert len(rendered.splitlines()) == 1
    assert "\\n" in rendered
    assert "\\xe9" in rendered
    assert "\\t" in rendered


def test_rendering_beyond_recursion_limit():
    count = sys.getrecursionlimit() + 100
    root = TreeNode(0, None)
    current = root
    for key in range(1, count):
        current.right = TreeNode(key, None)
        current = current.right
    lines = render_tree(root).splitlines()
    assert len(lines) == count
    assert lines[0] == "0"
    assert lines[-1].endswith(f"`-- R: {count - 1}")
