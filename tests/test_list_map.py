"""ListMap search semantics, sequential cost, and equivalence on valid datasets."""

import random

import pytest

from treemap import ListMap, TreeMap
from treemap.maps import ListMap as ExportedListMap
from treemap.maps.list_map import ListMap as ModuleListMap


def test_list_map_exports():
    assert ListMap is ExportedListMap is ModuleListMap


@pytest.mark.parametrize("map_type", [ListMap, TreeMap])
def test_equivalent_empty_defaults_updates_and_removal(map_type):
    mapping = map_type()
    sentinel = object()
    assert len(mapping) == 0
    assert mapping.keys() == mapping.values() == mapping.items() == []
    assert mapping.get(1, sentinel) is sentinel
    assert mapping.get(1) is None
    assert not mapping.contains_key(1)
    with pytest.raises(KeyError) as error:
        mapping.remove(1)
    assert error.value.args == (1,)
    assert mapping.put(1, "initial") is None
    mapping.put(1.0, None)
    assert len(mapping) == 1
    assert type(mapping.keys()[0]) is int
    assert mapping.get(1, sentinel) is None
    assert mapping.contains_key(1)
    assert mapping.remove(1) is None
    assert len(mapping) == 0
    assert mapping.get(1, sentinel) is sentinel


@pytest.mark.parametrize("map_type", [ListMap, TreeMap])
def test_all_six_datasets_have_identical_contracts(fifty_item_dataset, map_type):
    data = fifty_item_dataset
    mapping = map_type()
    expected = {}
    for key, value in data.initial + data.entries:
        mapping.put(key, value)
        expected[key] = value
        assert len(mapping) == len(expected)
        assert mapping.get(key, object()) is value
        assert mapping.items() == sorted(expected.items())
        assert mapping.keys() == sorted(expected)
        assert mapping.values() == [expected[k] for k in sorted(expected)]
    snapshots = [mapping.keys(), mapping.values(), mapping.items()]
    for snapshot in snapshots:
        snapshot.clear()
    assert len(mapping) == 50
    for key in list(expected):
        assert mapping.remove(key) == expected.pop(key)
        assert len(mapping) == len(expected)
        assert mapping.items() == sorted(expected.items())


@pytest.mark.parametrize("seed", [0, 6, 506])
def test_both_maps_match_dictionary_during_mixed_workload(seed):
    rng = random.Random(seed)
    maps = [ListMap(), TreeMap()]
    expected = {}
    sentinel = object()
    for _ in range(400):
        key = rng.randrange(75)
        operation = rng.choice(["put", "put", "get", "remove"])
        if operation == "put":
            value = rng.choice([None, False, "updated", [seed, key], {"key": key}])
            expected[key] = value
            for mapping in maps:
                mapping.put(key, value)
        elif operation == "remove":
            if key in expected:
                value = expected.pop(key)
                for mapping in maps:
                    assert mapping.remove(key) == value
            else:
                for mapping in maps:
                    with pytest.raises(KeyError):
                        mapping.remove(key)
        else:
            for mapping in maps:
                assert mapping.get(key, sentinel) == expected.get(key, sentinel)
        for mapping in maps:
            assert mapping.contains_key(key) is (key in expected)
            assert len(mapping) == len(expected)
            assert mapping.items() == sorted(expected.items())


class ProbeKey:
    """Record equality comparisons to distinguish sequential lookup from indexing."""

    def __init__(self, value, comparisons):
        self.value = value
        self.comparisons = comparisons

    def __eq__(self, other):
        if not isinstance(other, ProbeKey):
            return NotImplemented
        self.comparisons.append(other.value)
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


@pytest.mark.parametrize(
    ("target", "visited"), [(0, [0]), (4, [0, 1, 2, 3, 4]), (5, list(range(5)))]
)
def test_list_search_checks_entries_sequentially_until_found_or_exhausted(target, visited):
    mapping = ListMap()
    for key in range(5):
        mapping.put(ProbeKey(key, []), key)
    comparisons = []
    sentinel = object()
    result = mapping.get(ProbeKey(target, comparisons), sentinel)
    assert comparisons == visited
    if target == 5:
        assert result is sentinel
    else:
        assert result == target
