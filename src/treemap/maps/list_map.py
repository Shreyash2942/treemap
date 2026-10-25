"""A simple sequential-search map for comparison with TreeMap."""

from __future__ import annotations

from typing import Generic, TypeVar, overload

from treemap.core.node import K, V

D = TypeVar("D")


class ListMap(Generic[K, V]):
    """Store entries in insertion order with linear equality-based lookup.

    Valid keys follow TreeMap's stable total-order contract. Search uses only
    equality; sorted collections require `<`. Mixed incompatible key types are
    outside the shared contract. Values are unrestricted, including `None`.
    """

    def __init__(self) -> None:
        self._entries: list[tuple[K, V]] = []

    def __len__(self) -> int:
        """Return the number of unique keys in O(1) time."""
        return len(self._entries)

    def put(self, key: K, value: V) -> None:
        """Insert or replace in O(n) time, retaining the original equal key."""
        for index, (existing_key, _) in enumerate(self._entries):
            if key == existing_key:
                self._entries[index] = (existing_key, value)
                return
        self._entries.append((key, value))

    @overload
    def get(self, key: K) -> V | None: ...

    @overload
    def get(self, key: K, default: D) -> V | D: ...

    def get(self, key: K, default: D | None = None) -> V | D | None:
        """Scan sequentially; return default only when no matching key exists."""
        for existing_key, value in self._entries:
            if key == existing_key:
                return value
        return default

    def remove(self, key: K) -> V:
        """Remove and return the value in O(n) time; raise `KeyError` if absent."""
        for index, (existing_key, value) in enumerate(self._entries):
            if key == existing_key:
                self._entries.pop(index)
                return value
        raise KeyError(key)

    def contains_key(self, key: K) -> bool:
        """Return whether a matching key exists, independently of its value."""
        return any(key == existing_key for existing_key, _ in self._entries)

    def keys(self) -> list[K]:
        """Return sorted keys in a new list in O(n log n) time."""
        return sorted(key for key, _ in self._entries)

    def values(self) -> list[V]:
        """Return values in key order in a new list in O(n log n) time."""
        return [value for _, value in self.items()]

    def items(self) -> list[tuple[K, V]]:
        """Return a new list of pairs sorted by key in O(n log n) time."""
        return sorted(self._entries, key=lambda entry: entry[0])
