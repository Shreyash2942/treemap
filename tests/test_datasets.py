"""Explicit evidence for each of the six required 50-item Day 3 datasets."""

import random

from conftest import assert_bst_valid

from bst_map import BinarySearchTree, TreeMap
from bst_map.core import analyze_balance, inorder, postorder, preorder


def test_bst_dataset_preserves_entries_and_invariants_after_every_mutation(fifty_item_dataset):
    data = fifty_item_dataset
    assert len(data.entries) == 50
    tree = BinarySearchTree()
    expected = {}
    for key, value in data.initial + data.entries:
        tree.insert(key, value)
        expected[key] = value
        assert len(tree) == len(expected)
        assert_bst_valid(tree)
        assert [(node.key, node.value) for node in inorder(tree.root)] == sorted(expected.items())
    assert len(tree) == 50
    if data.name in {"sorted_int", "reverse_int"}:
        report = analyze_balance(tree.root)
        assert report.height == 49
        assert abs(report.balance_factor) == 49
        assert not report.is_balanced
    for traversal in [inorder, preorder, postorder]:
        assert {node.key for node in traversal(tree.root)} == set(expected)
        assert len(list(traversal(tree.root))) == 50

    removal_keys = list(expected)
    random.Random(650).shuffle(removal_keys)
    for key in removal_keys:
        assert tree.delete(key) == expected.pop(key)
        assert tree.search(key) is None
        assert len(tree) == len(expected)
        assert_bst_valid(tree)
    assert tree.root is None


def test_tree_map_dataset_has_sorted_collections_and_replacement_semantics(fifty_item_dataset):
    data = fifty_item_dataset
    mapping = TreeMap()
    expected = {}
    for key, value in data.initial + data.entries:
        previous_size = len(mapping)
        was_present = key in expected
        mapping.put(key, value)
        expected[key] = value
        assert len(mapping) == previous_size + (not was_present)
        assert mapping.get(key, object()) is value
        assert mapping.contains_key(key)
        assert mapping.items() == sorted(expected.items())
        assert mapping.values() == [expected[k] for k in sorted(expected)]
        assert_bst_valid(mapping._tree)
    assert len(mapping) == 50
    if data.name == "updates":
        assert len(data.initial) == 50  # all 50 subsequent operations replace existing entries
        assert all(value != "original" for value in mapping.values())
    for key in reversed(list(expected)):
        assert mapping.remove(key) == expected.pop(key)
        assert len(mapping) == len(expected)
        assert_bst_valid(mapping._tree)
    assert mapping.items() == []
