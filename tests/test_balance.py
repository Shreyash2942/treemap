"""Height conventions, balance of every subtree, and independent height checks."""

import random
import sys
from collections import deque
from dataclasses import FrozenInstanceError

import pytest
from conftest import assert_bst_valid

from treemap import BinarySearchTree
from treemap.core.balance import analyze_balance, balance_factor, height, is_balanced
from treemap.core.traversals import postorder


def breadth_first_height(root):
    """Independent reference height using breadth-first levels, not post-order."""
    if root is None:
        return -1
    queue = deque([(root, 0)])
    deepest = 0
    while queue:
        node, depth = queue.popleft()
        deepest = max(deepest, depth)
        if node.left is not None:
            queue.append((node.left, depth + 1))
        if node.right is not None:
            queue.append((node.right, depth + 1))
    return deepest


@pytest.mark.parametrize(
    ("keys", "expected_height", "expected_factor", "unbalanced"),
    [
        ([], -1, 0, ()),
        ([1], 0, 0, ()),
        ([2, 1], 1, 1, ()),
        ([2, 3], 1, -1, ()),
        ([4, 2, 6, 1, 3, 5, 7], 2, 0, ()),
        ([5, 3, 8, 2, 4, 7, 9, 1], 3, 1, ()),
        ([1, 2, 3], 2, -2, (1,)),
        ([3, 2, 1], 2, 2, (3,)),
        ([1, 2, 3, 4, 5], 4, -4, (3, 2, 1)),
        ([50, 30, 70, 20, 80, 10, 90], 3, 0, (30, 70)),
        ([50, 30, 70, 20, 10, 80], 3, 1, (30,)),
    ],
)
def test_height_root_factor_and_all_unbalanced_nodes(
    keys, expected_height, expected_factor, unbalanced
):
    tree = BinarySearchTree()
    for key in keys:
        tree.insert(key, None)
    report = analyze_balance(tree.root)
    assert report.height == expected_height
    assert report.balance_factor == expected_factor
    assert report.unbalanced_keys == unbalanced
    assert report.is_balanced is (not unbalanced)
    assert height(tree.root) == expected_height
    assert balance_factor(tree.root) == expected_factor
    assert is_balanced(tree.root) is (not unbalanced)
    assert analyze_balance(tree.root) == report
    assert_bst_valid(tree)


def test_analysis_does_not_change_nodes_or_rotate_tree(sample_tree):
    original_root = sample_tree.root
    nodes = list(postorder(sample_tree.root))
    before = [(node, node.key, node.value, node.left, node.right) for node in nodes]
    analyze_balance(sample_tree.root)
    assert sample_tree.root is original_root
    assert [(node, node.key, node.value, node.left, node.right) for node in nodes] == before
    assert_bst_valid(sample_tree)


def test_report_is_immutable(sample_tree):
    report = analyze_balance(sample_tree.root)
    with pytest.raises(FrozenInstanceError):
        report.height = 100


def test_analysis_reflects_insertions_and_deletions():
    tree = BinarySearchTree()
    for key in [3, 2, 1]:
        tree.insert(key, str(key))
    assert analyze_balance(tree.root).unbalanced_keys == (3,)
    tree.delete(1)
    assert analyze_balance(tree.root).is_balanced
    assert height(tree.root) == 1
    tree.insert(4, None)
    assert balance_factor(tree.root) == 0
    for key in [3, 2, 4]:
        tree.delete(key)
    assert height(tree.root) == -1
    assert is_balanced(tree.root)


@pytest.mark.parametrize("seed", [0, 6, 506])
def test_every_subtree_matches_breadth_first_reference(seed):
    keys = list(range(75))
    random.Random(seed).shuffle(keys)
    tree = BinarySearchTree()
    for key in keys:
        tree.insert(key, str(key))
    expected_unbalanced = []
    for node in postorder(tree.root):
        factor = breadth_first_height(node.left) - breadth_first_height(node.right)
        assert balance_factor(node) == factor
        if abs(factor) > 1:
            expected_unbalanced.append(node.key)
    report = analyze_balance(tree.root)
    assert report.height == breadth_first_height(tree.root)
    assert report.unbalanced_keys == tuple(expected_unbalanced)
    assert report.is_balanced is (not expected_unbalanced)


@pytest.mark.parametrize("descending", [False, True])
def test_balance_analysis_beyond_recursion_limit(descending):
    count = sys.getrecursionlimit() + 100
    keys = list(range(count))
    if descending:
        keys.reverse()
    tree = BinarySearchTree()
    for key in keys:
        tree.insert(key, None)
    report = analyze_balance(tree.root)
    assert report.height == count - 1
    assert report.balance_factor == (count - 1 if descending else 1 - count)
    assert not report.is_balanced
    assert report.unbalanced_keys == tuple(reversed(keys[:-2]))
    assert tree.root.key == keys[0]
    assert_bst_valid(tree)


def test_balance_reporting_supports_string_keys():
    tree = BinarySearchTree()
    for key in ["alpha", "beta", "delta"]:
        tree.insert(key, {})
    report = analyze_balance(tree.root)
    assert report.unbalanced_keys == ("alpha",)
    assert report.height == 2
