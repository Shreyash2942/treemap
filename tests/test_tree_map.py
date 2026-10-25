"""TreeMap contract and integration with BST traversal, deletion, and balance."""

import random
import sys

import pytest
from conftest import assert_bst_valid

from bst_map import TreeMap
from bst_map.core.balance import analyze_balance
from bst_map.maps import TreeMap as ExportedTreeMap
from bst_map.maps.tree_map import TreeMap as ModuleTreeMap


def test_public_root_supports_read_only_inspection_and_tracks_deletion():
    mapping = TreeMap()
    assert mapping.root is None
    for key in [20, 10, 30]:
        mapping.put(key, str(key))
    assert mapping.root.key == 20
    assert analyze_balance(mapping.root).is_balanced
    with pytest.raises(AttributeError):
        mapping.root = None
    assert mapping.remove(20) == "20"
    assert mapping.root.key == 30
    assert mapping.items() == [(10, "10"), (30, "30")]
    assert_bst_valid(mapping._tree)


def test_fifty_missing_removals_do_not_change_existing_none_entries():
    mapping = TreeMap()
    for key in range(50):
        mapping.put(key, None)
    for key in range(50, 100):
        with pytest.raises(KeyError) as error:
            mapping.remove(key)
        assert error.value.args == (key,)
        assert len(mapping) == 50
        assert mapping.items() == [(existing, None) for existing in range(50)]
        assert_bst_valid(mapping._tree)


def test_map_can_be_repeatedly_emptied_and_reused():
    mapping = TreeMap()
    for round_number in range(3):
        for key in range(50):
            mapping.put(key, (round_number, key))
            assert_bst_valid(mapping._tree)
        for key in reversed(range(50)):
            assert mapping.remove(key) == (round_number, key)
            assert len(mapping) == key
            assert_bst_valid(mapping._tree)
        assert mapping.keys() == mapping.values() == mapping.items() == []
        assert mapping.get(0, "missing") == "missing"


def test_map_exports_are_consistent():
    assert TreeMap is ExportedTreeMap is ModuleTreeMap


def test_empty_map_contract():
    mapping = TreeMap()
    assert len(mapping) == 0
    assert mapping.keys() == mapping.values() == mapping.items() == []
    assert not mapping.contains_key("absent")
    assert mapping.get("absent") is None
    sentinel = object()
    assert mapping.get("absent", default=sentinel) is sentinel
    with pytest.raises(KeyError) as error:
        mapping.remove("absent")
    assert error.value.args == ("absent",)
    assert len(mapping) == 0


def test_put_updates_existing_keys_and_get_distinguishes_none():
    mapping = TreeMap[str, object]()
    assert mapping.put("alpha", 10) is None
    mapping.put("beta", None)
    mapping.put("alpha", 15)
    assert len(mapping) == 2
    assert mapping.get("alpha") == 15
    sentinel = object()
    assert mapping.get("beta", sentinel) is None
    assert mapping.contains_key("beta")
    assert mapping.get("absent", sentinel) is sentinel
    mapping.put("alpha", None)
    assert mapping.get("alpha", sentinel) is None
    assert mapping.remove("beta") is None
    assert not mapping.contains_key("beta")
    assert len(mapping) == 1
    assert_bst_valid(mapping._tree)


def test_collections_are_sorted_by_keys_and_return_independent_lists():
    mapping = TreeMap()
    entries = {"delta": [4], "alpha": None, "gamma": {"value": 3}, "beta": False}
    for key, value in entries.items():
        mapping.put(key, value)
    assert mapping.keys() == ["alpha", "beta", "delta", "gamma"]
    assert mapping.values() == [None, False, [4], {"value": 3}]
    assert mapping.items() == sorted(entries.items())
    old_keys, old_values, old_items = mapping.keys(), mapping.values(), mapping.items()
    old_keys.clear()
    old_values.clear()
    old_items.clear()
    assert len(mapping) == 4
    assert mapping.items() == sorted(entries.items())
    snapshot = mapping.items()
    mapping.put("epsilon", "new")
    assert snapshot == sorted(entries.items())
    assert mapping.get("delta") is entries["delta"]


@pytest.mark.parametrize("default", [None, False, 0, "fallback", [1], {"missing": True}])
def test_default_is_returned_unchanged_only_for_missing_keys(default):
    mapping = TreeMap()
    mapping.put(1, None)
    assert mapping.get(2, default) is default
    assert mapping.get(1, default) is None


@pytest.mark.parametrize("keys", [[50], [50, 30], [50, 70], [50, 30, 80, 60, 65, 90]])
def test_root_removal_delegates_all_deletion_cases(keys):
    mapping = TreeMap()
    for key in keys:
        mapping.put(key, f"value-{key}")
    assert mapping.remove(50) == "value-50"
    assert mapping.keys() == sorted(set(keys) - {50})
    assert not mapping.contains_key(50)
    assert len(mapping) == len(keys) - 1
    assert_bst_valid(mapping._tree)


def test_missing_remove_preserves_entries():
    mapping = TreeMap()
    mapping.put(1, None)
    mapping.put(2, "two")
    with pytest.raises(KeyError) as error:
        mapping.remove(3)
    assert error.value.args == (3,)
    assert mapping.items() == [(1, None), (2, "two")]
    assert len(mapping) == 2
    assert_bst_valid(mapping._tree)


@pytest.mark.parametrize("key_kind", ["int", "str", "tuple"])
def test_fifty_entries_support_key_types_and_heterogeneous_values(key_kind):
    keys = list(range(50))
    if key_kind == "str":
        keys = [f"key-{key:02}" for key in keys]
    elif key_kind == "tuple":
        keys = [(key // 10, key % 10) for key in keys]
    random.Random(506).shuffle(keys)
    values = [None, False, 3.5, "text", [1, 2], {"nested": 3}]
    expected = {key: values[index % len(values)] for index, key in enumerate(keys)}
    mapping = TreeMap()
    for key, value in expected.items():
        mapping.put(key, value)
    assert mapping.keys() == sorted(expected)
    assert mapping.items() == sorted(expected.items())
    assert mapping.values() == [expected[key] for key in sorted(expected)]
    assert len(mapping) == 50
    for key, value in expected.items():
        assert mapping.contains_key(key)
        assert mapping.get(key) is value
    for key in keys:
        assert mapping.remove(key) is expected[key]
        assert_bst_valid(mapping._tree)
    assert mapping.items() == []


@pytest.mark.parametrize("operation", ["put", "get", "remove", "contains_key"])
def test_incompatible_key_comparisons_propagate_without_mutation(operation):
    mapping = TreeMap()
    mapping.put(1, "one")
    with pytest.raises(TypeError):
        if operation == "put":
            mapping.put("bad", 2)
        else:
            getattr(mapping, operation)("bad")
    assert mapping.items() == [(1, "one")]
    assert len(mapping) == 1


@pytest.mark.parametrize("seed", [0, 6, 506])
def test_mixed_map_operations_match_dictionary(seed):
    rng = random.Random(seed)
    mapping = TreeMap[int, object]()
    expected = {}
    initial = list(range(100))
    rng.shuffle(initial)
    for key in initial:
        mapping.put(key, key)
        expected[key] = key
    sentinel = object()
    for _ in range(400):
        key = rng.randrange(125)
        operation = rng.choice(["put", "put", "get", "remove"])
        if operation == "put":
            value = rng.choice([None, False, "updated", (seed, key), {"key": key}])
            mapping.put(key, value)
            expected[key] = value
        elif operation == "remove":
            if key in expected:
                assert mapping.remove(key) == expected.pop(key)
            else:
                with pytest.raises(KeyError):
                    mapping.remove(key)
        else:
            assert mapping.get(key, sentinel) == expected.get(key, sentinel)
        assert mapping.contains_key(key) is (key in expected)
        assert len(mapping) == len(expected)
        assert mapping.items() == sorted(expected.items())
        assert mapping.keys() == sorted(expected)
        assert mapping.values() == [expected[k] for k in sorted(expected)]
        assert_bst_valid(mapping._tree)

    for key in list(expected):
        assert mapping.remove(key) == expected.pop(key)
        assert_bst_valid(mapping._tree)
    assert len(mapping) == 0
    assert mapping.items() == []


def test_deep_map_integrates_sorted_traversal_balance_and_deletion():
    count = sys.getrecursionlimit() + 100
    mapping = TreeMap()
    for key in range(count):
        mapping.put(key, None)
    assert mapping.keys() == list(range(count))
    assert mapping.values() == [None] * count
    assert mapping.items() == [(key, None) for key in range(count)]
    assert mapping.contains_key(count - 1)
    report = analyze_balance(mapping._tree.root)
    assert report.height == count - 1
    assert not report.is_balanced
    assert mapping.remove(count // 2) is None
    assert len(mapping) == count - 1
    assert not mapping.contains_key(count // 2)
    assert_bst_valid(mapping._tree)
