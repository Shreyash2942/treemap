"""Traversal order, node identity, repeatability, and recursion-free behavior."""

import sys

import pytest
from conftest import assert_bst_valid

from treemap import BinarySearchTree, TreeNode
from treemap.core.traversals import inorder, postorder, preorder

TRAVERSALS = [inorder, preorder, postorder]


@pytest.mark.parametrize("traversal", TRAVERSALS)
def test_empty_traversal(traversal):
    assert list(traversal(None)) == []


@pytest.mark.parametrize("traversal", TRAVERSALS)
def test_single_node_traversal_preserves_node_and_value(traversal):
    node = TreeNode("only", None)
    assert list(traversal(node)) == [node]
    assert node.value is None


@pytest.mark.parametrize(
    ("traversal", "expected"),
    [
        (inorder, [20, 30, 40, 50, 60, 70, 80]),
        (preorder, [50, 30, 20, 40, 70, 60, 80]),
        (postorder, [20, 40, 30, 60, 80, 70, 50]),
    ],
)
def test_readme_orders_are_repeatable_and_do_not_mutate_tree(sample_tree, traversal, expected):
    nodes = {key: sample_tree.search(key) for key in expected}
    links = {key: (node.left, node.right, node.value) for key, node in nodes.items()}
    for _ in range(2):
        result = list(traversal(sample_tree.root))
        assert [node.key for node in result] == expected
        assert all(node is nodes[node.key] for node in result)
    for key, node in nodes.items():
        assert (node.left, node.right, node.value) == links[key]
    assert_bst_valid(sample_tree)


@pytest.mark.parametrize("traversal", TRAVERSALS)
def test_iterators_have_independent_progress(sample_tree, traversal):
    first = traversal(sample_tree.root)
    second = traversal(sample_tree.root)
    first_node = next(first)
    assert next(second) is first_node
    assert list(first) == list(second)


@pytest.mark.parametrize(
    ("traversal", "expected"),
    [(inorder, [20, 30, 40]), (preorder, [30, 20, 40]), (postorder, [20, 40, 30])],
)
def test_traversals_accept_subtree_roots(sample_tree, traversal, expected):
    assert [node.key for node in traversal(sample_tree.root.left)] == expected


@pytest.mark.parametrize(
    ("traversal", "expected"),
    [
        (inorder, [20, 30, 40, 60, 70, 80]),
        (preorder, [60, 30, 20, 40, 70, 80]),
        (postorder, [20, 40, 30, 80, 70, 60]),
    ],
)
def test_traversals_reflect_two_child_deletion(sample_tree, traversal, expected):
    sample_tree.delete(50)
    sample_tree.insert(40, "updated")
    result = list(traversal(sample_tree.root))
    assert [node.key for node in result] == expected
    assert next(node.value for node in result if node.key == 40) == "updated"
    assert_bst_valid(sample_tree)


@pytest.mark.parametrize("descending", [False, True])
@pytest.mark.parametrize("traversal", TRAVERSALS)
def test_deep_chain_traversal_beyond_recursion_limit(traversal, descending):
    count = sys.getrecursionlimit() + 100
    keys = list(range(count))
    if descending:
        keys.reverse()
    tree = BinarySearchTree()
    for key in keys:
        tree.insert(key, None)
    if traversal is inorder:
        expected = list(range(count))
    elif traversal is preorder:
        expected = keys
    else:
        expected = list(reversed(keys))
    assert [node.key for node in traversal(tree.root)] == expected
    assert_bst_valid(tree)


def test_string_keys_and_unorderable_values_are_traversed_by_key():
    tree = BinarySearchTree()
    entries = {"delta": {"nested": 1}, "alpha": None, "omega": [1, 2], "beta": False}
    for key, value in entries.items():
        tree.insert(key, value)
    assert [(node.key, node.value) for node in inorder(tree.root)] == sorted(entries.items())
