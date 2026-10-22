"""Core node, insertion, search, deletion, and extrema behavior."""

import pytest
from conftest import assert_bst_valid

from bst_map import BinarySearchTree, TreeNode
from bst_map.core.operations import delete_node, maximum_node, minimum_node


def test_node_fields_and_independent_child_defaults():
    first = TreeNode(1, None)
    second = TreeNode(2, {"nested": [1, 2]})
    assert first.key == 1
    assert first.value is None
    assert first.left is first.right is None
    first.left = TreeNode(0, "child")
    assert second.left is second.right is None
    parent = TreeNode(3, "parent", first, second)
    assert parent.left is first
    assert parent.right is second


@pytest.mark.parametrize(
    "keys",
    [
        [50, 30, 70, 20, 40, 60, 80],
        [20, 30, 40, 50, 60, 70, 80],
        [80, 70, 60, 50, 40, 30, 20],
    ],
)
def test_insertion_preserves_order_and_size(keys):
    tree = BinarySearchTree()
    for count, key in enumerate(keys, start=1):
        assert tree.insert(key, f"value-{key}") is None
        assert len(tree) == count
        assert_bst_valid(tree)
    assert tree.root.key == keys[0]
    for key in keys:
        assert tree.search(key).value == f"value-{key}"


@pytest.mark.parametrize("key", [50, 30, 70, 20, 40, 60, 80])
def test_search_finds_root_and_both_subtrees(sample_tree, key):
    node = sample_tree.search(key)
    assert node.key == key
    assert node.value == f"value-{key}"
    assert len(sample_tree) == 7


@pytest.mark.parametrize("key", [0, 35, 100])
def test_search_missing_key_returns_none(sample_tree, key):
    assert sample_tree.search(key) is None
    assert len(sample_tree) == 7
    assert_bst_valid(sample_tree)


@pytest.mark.parametrize("key", [50, 30, 80])
def test_duplicate_key_updates_existing_node_without_growing(sample_tree, key):
    original_node = sample_tree.search(key)
    sample_tree.insert(key, "updated")
    assert sample_tree.search(key) is original_node
    assert original_node.value == "updated"
    assert len(sample_tree) == 7
    assert_bst_valid(sample_tree)


@pytest.mark.parametrize(
    ("keys", "removed"),
    [
        ([50], 50),  # only node
        ([50, 30], 50),  # root with left child
        ([50, 70], 50),  # root with right child
        ([50, 30, 70], 30),  # left leaf
        ([50, 30, 70], 70),  # right leaf
        ([50, 30, 20], 30),  # left branch, left child
        ([50, 30, 40], 30),  # left branch, right child
        ([50, 70, 60], 70),  # right branch, left child
        ([50, 70, 80], 70),  # right branch, right child
        ([50, 30, 70], 50),  # immediate successor
        ([50, 30, 70, 80], 50),  # immediate successor with right child
        ([50, 30, 80, 60, 90], 50),  # deeper successor
        ([50, 30, 80, 60, 65, 90], 50),  # deeper successor with right child
        ([50, 20, 80, 60, 90, 55, 57], 50),  # successor multiple levels down
        ([100, 50, 150, 30, 80, 60, 65, 90], 50),  # two children on left branch
        ([100, 50, 150, 130, 180, 160, 170], 150),  # two children on right branch
    ],
)
def test_deletion_cases_preserve_all_remaining_entries(keys, removed):
    tree = BinarySearchTree()
    for key in keys:
        tree.insert(key, f"value-{key}")
    assert tree.delete(removed) == f"value-{removed}"
    assert tree.search(removed) is None
    assert len(tree) == len(keys) - 1
    for key in set(keys) - {removed}:
        assert tree.search(key).value == f"value-{key}"
    assert_bst_valid(tree)


def test_two_child_deletion_consistently_uses_in_order_successor(sample_tree):
    assert sample_tree.delete(50) == "value-50"
    assert sample_tree.root.key == 60
    assert sample_tree.root.value == "value-60"
    assert_bst_valid(sample_tree)


@pytest.mark.parametrize("key", [0, 35, 100])
def test_missing_deletion_raises_and_preserves_tree(sample_tree, key):
    root = sample_tree.root
    original_nodes = {k: sample_tree.search(k) for k in [50, 30, 70, 20, 40, 60, 80]}
    with pytest.raises(KeyError) as error:
        sample_tree.delete(key)
    assert error.value.args == (key,)
    assert sample_tree.root is root
    for existing, node in original_nodes.items():
        assert sample_tree.search(existing) is node
        assert node.value == f"value-{existing}"
    assert len(sample_tree) == 7
    assert_bst_valid(sample_tree)


def test_extrema_return_actual_nodes_and_support_subtrees(sample_tree):
    assert sample_tree.minimum() is sample_tree.search(20)
    assert sample_tree.maximum() is sample_tree.search(80)
    assert minimum_node(sample_tree.root.right) is sample_tree.search(60)
    assert maximum_node(sample_tree.root.left) is sample_tree.search(40)


@pytest.mark.parametrize("direction", ["minimum", "maximum"])
def test_extrema_remain_correct_during_deletion(sample_tree, direction):
    expected = list(range(20, 81, 10))
    if direction == "maximum":
        expected.reverse()
    for remaining, key in zip(range(7, 0, -1), expected, strict=True):
        assert len(sample_tree) == remaining
        assert getattr(sample_tree, direction)().key == key
        sample_tree.delete(key)
        assert_bst_valid(sample_tree)
    assert sample_tree.root is None


def test_subtree_delete_helper_returns_replacement_and_original_value():
    child = TreeNode(5, "five")
    root = TreeNode(10, "ten", left=child)
    replacement, value = delete_node(root, 10)
    assert replacement is child
    assert value == "ten"
    replacement, value = delete_node(replacement, 5)
    assert replacement is None
    assert value == "five"


@pytest.mark.parametrize(
    ("branch", "invalid_key", "message"),
    [("left", 55, "upper ancestor bound"), ("right", 45, "lower ancestor bound")],
)
def test_validator_rejects_distant_ancestor_violations(sample_tree, branch, invalid_key, message):
    # Each corrupted descendant still satisfies its immediate parent's ordering.
    if branch == "left":
        sample_tree.root.left.right.key = invalid_key
    else:
        sample_tree.root.right.left.key = invalid_key
    with pytest.raises(AssertionError, match=message):
        assert_bst_valid(sample_tree)


def test_validator_rejects_cycles(sample_tree):
    sample_tree.root.left = sample_tree.root
    with pytest.raises(AssertionError, match="Cycle or shared child"):
        assert_bst_valid(sample_tree)


def test_validator_rejects_incorrect_size(sample_tree):
    sample_tree.root.left = None
    with pytest.raises(AssertionError, match="Recorded size"):
        assert_bst_valid(sample_tree)
