"""Empty trees, key/value contracts, deep trees, and seeded mutation workloads."""

import random
import sys
from dataclasses import dataclass
from datetime import date

import pytest
from conftest import assert_bst_valid

from treemap import BinarySearchTree
from treemap.core.operations import delete_node, maximum_node, minimum_node


@pytest.mark.parametrize("selection", ["root", "minimum", "maximum"])
def test_repeated_deletions_to_empty_preserve_size_bounds_and_missing_behavior(selection):
    keys = list(range(50))
    random.Random(506).shuffle(keys)
    tree = BinarySearchTree()
    expected = {}
    for key in keys:
        tree.insert(key, None if key % 2 else str(key))
        expected[key] = None if key % 2 else str(key)
        assert_bst_valid(tree)
    while expected:
        if selection == "root":
            key = tree.root.key
        else:
            key = getattr(tree, selection)().key
        assert tree.delete(key) == expected.pop(key)
        assert len(tree) == len(expected)
        assert tree.search(key) is None
        for _ in range(2):
            with pytest.raises(KeyError) as error:
                tree.delete(key)
            assert error.value.args == (key,)
            assert len(tree) == len(expected)
            assert_bst_valid(tree)
        if expected:
            assert tree.minimum().key == min(expected)
            assert tree.maximum().key == max(expected)
    assert tree.root is None
    tree.insert(100, "reused")
    assert len(tree) == 1
    assert tree.search(100).value == "reused"
    assert_bst_valid(tree)


def test_equal_numeric_keys_replace_without_creating_duplicate_nodes():
    tree = BinarySearchTree()
    tree.insert(1, "integer")
    node = tree.search(1)
    tree.insert(1.0, "float")
    tree.insert(True, None)
    assert len(tree) == 1
    assert tree.search(1.0) is node
    assert tree.search(True).value is None
    assert_bst_valid(tree)
    assert tree.delete(True) is None
    assert len(tree) == 0


def test_empty_tree_behavior():
    tree = BinarySearchTree()
    assert tree.root is None
    assert len(tree) == 0
    assert tree.search(1) is None
    with pytest.raises(KeyError) as error:
        tree.delete(1)
    assert error.value.args == (1,)
    assert_bst_valid(tree)


@pytest.mark.parametrize("operation", ["minimum", "maximum"])
def test_empty_tree_extrema_raise_value_error(operation):
    tree = BinarySearchTree()
    with pytest.raises(ValueError, match="empty tree"):
        getattr(tree, operation)()


@pytest.mark.parametrize("operation", [minimum_node, maximum_node])
def test_empty_subtree_extrema_raise_value_error(operation):
    with pytest.raises(ValueError, match="empty tree"):
        operation(None)


def test_empty_subtree_delete_raises_key_error():
    with pytest.raises(KeyError) as error:
        delete_node(None, "absent")
    assert error.value.args == ("absent",)


def test_single_node_can_be_updated_deleted_and_reinserted():
    tree = BinarySearchTree()
    tree.insert(0, "initial")
    assert tree.minimum() is tree.maximum() is tree.root
    tree.insert(0, None)
    assert len(tree) == 1
    assert tree.search(0) is not None
    assert tree.search(0).value is None
    assert tree.delete(0) is None
    assert tree.root is None
    assert len(tree) == 0
    assert tree.search(0) is None
    tree.insert(1, "new root")
    assert tree.root.key == 1
    assert tree.search(1).value == "new root"
    assert_bst_valid(tree)


@dataclass(frozen=True, order=True)
class RankedKey:
    rank: int


@pytest.mark.parametrize(
    "keys",
    [
        [0, -100, 100, -1, 1],
        [0.5, -2.5, 10.5, 0.0, 1.25],
        ["delta", "alpha", "omega", "beta", ""],
        [(2, "a"), (1, "z"), (3, "a"), (2, "b"), (1, "a")],
        [date(2026, 6, 1), date(2025, 1, 1), date(2027, 1, 1)],
        [RankedKey(2), RankedKey(1), RankedKey(3)],
    ],
)
def test_comparable_key_types(keys):
    tree = BinarySearchTree()
    for index, key in enumerate(keys):
        tree.insert(key, index)
        assert_bst_valid(tree)
    assert tree.minimum().key == min(keys)
    assert tree.maximum().key == max(keys)
    for index, key in enumerate(keys):
        assert tree.search(key).value == index
    for index, key in enumerate(keys):
        assert tree.delete(key) == index
        assert_bst_valid(tree)
    assert tree.root is None


def test_fifty_entries_with_heterogeneous_values_including_none():
    values = [None, 42, 3.5, "text", False, [1, 2], {"key": "value"}, (1, 2), {3, 4}]
    keys = list(range(50))
    random.Random(506).shuffle(keys)
    expected = {key: values[key % len(values)] for key in keys}
    tree = BinarySearchTree[int, object]()
    for key, value in expected.items():
        tree.insert(key, value)
        assert_bst_valid(tree)
    assert len(tree) == 50
    for key, value in expected.items():
        assert tree.search(key).value is value
    for key in reversed(keys):
        assert tree.delete(key) is expected[key]
        assert_bst_valid(tree)


@pytest.mark.parametrize("operation", ["insert", "search", "delete"])
def test_incompatible_key_comparison_raises_without_mutation(operation):
    tree = BinarySearchTree()
    tree.insert(5, "five")
    root = tree.root
    with pytest.raises(TypeError):
        if operation == "insert":
            tree.insert("incompatible", "value")
        else:
            getattr(tree, operation)("incompatible")
    assert tree.root is root
    assert tree.search(5).value == "five"
    assert len(tree) == 1
    assert_bst_valid(tree)


@pytest.mark.parametrize("descending", [False, True])
def test_skewed_tree_beyond_recursion_limit(descending):
    count = sys.getrecursionlimit() + 100
    keys = list(range(count))
    if descending:
        keys.reverse()
    tree = BinarySearchTree()
    for key in keys:
        tree.insert(key, str(key))
    assert len(tree) == count
    assert_bst_valid(tree)
    assert tree.search(keys[-1]).value == str(keys[-1])
    assert tree.search(count) is None
    assert tree.minimum().key == 0
    assert tree.maximum().key == count - 1
    for key in [keys[-1], keys[0], keys[count // 2]]:
        assert tree.delete(key) == str(key)
        assert tree.search(key) is None
        assert_bst_valid(tree)
    assert len(tree) == count - 3


@pytest.mark.parametrize("seed", [0, 1, 6, 50, 506])
def test_seeded_mutations_match_dictionary(seed):
    rng = random.Random(seed)
    tree = BinarySearchTree[int, object]()
    expected = {}
    keys = list(range(100))
    rng.shuffle(keys)
    for key in keys:
        tree.insert(key, key)
        expected[key] = key
        assert_bst_valid(tree)

    for _ in range(400):
        key = rng.randrange(125)
        operation = rng.choice(["insert", "insert", "search", "delete"])
        if operation == "insert":
            value = rng.choice([None, "updated", -1, False, (seed, key), {"key": key}])
            tree.insert(key, value)
            expected[key] = value
        elif operation == "delete":
            if key in expected:
                assert tree.delete(key) == expected.pop(key)
            else:
                with pytest.raises(KeyError):
                    tree.delete(key)
        else:
            node = tree.search(key)
            if key in expected:
                assert node is not None
                assert node.value == expected[key]
            else:
                assert node is None

        assert len(tree) == len(expected)
        assert_bst_valid(tree)
        for existing, value in expected.items():
            assert tree.search(existing).value == value
        if expected:
            assert tree.minimum().key == min(expected)
            assert tree.maximum().key == max(expected)

    remaining = list(expected)
    rng.shuffle(remaining)
    for key in remaining:
        assert tree.delete(key) == expected.pop(key)
        assert_bst_valid(tree)
    assert tree.root is None
    assert len(tree) == 0
