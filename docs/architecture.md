# Architecture

The distribution is named `bstkit`, the repository directory is `treemap`, and
the import package is `bst_map`. The project uses a `src/` layout; install it
with `python -m pip install -e ".[dev]"` before running tests.

## Day 1 core

- `core/node.py`: generic `TreeNode` dataclass and comparable-key type contract.
- `core/bst.py`: tree ownership, root, size, and public operations.
- `core/operations.py`: subtree deletion and minimum/maximum helpers.
- `tests/conftest.py`: independent strict-bound invariant checker and fixtures.

Keys in each tree must share a stable total ordering: equality and `<` must agree.
Do not mix incompatible key types, mutate stored keys, or use unordered keys such
as floating-point NaN. Values have no ordering requirement and may include `None`.
Incompatible comparisons propagate `TypeError` from the key type. The tree does
not attempt to validate every pair of keys or detect unsupported ordering laws.

| Operation | Result | Absent/empty behavior |
| --- | --- | --- |
| `insert(key, value)` | `None`; inserts or updates an existing value | Creates the root |
| `search(key)` | Matching `TreeNode` | Returns `None` |
| `delete(key)` | Removed value, which can be `None` | Raises `KeyError(key)` |
| `minimum()` / `maximum()` | Matching `TreeNode` | Raises `ValueError` |
| `len(tree)` | Number of distinct keys | Returns `0` |
| `tree.root` | Root node, for inspection | Returns `None` |

Returning nodes from search distinguishes an absent key from a stored `None`
value. Node references expose the structure for educational inspection; callers
must not mutate keys or child links behind the tree's size tracking. Deletion
with two children copies the in-order successor's key and value into the target
and unlinks the successor, so retained node references may reflect this change.

All core operations are iterative. With height `h`, each operation takes O(h)
time and O(1) auxiliary space. A reasonably balanced tree has O(log n) height;
sorted insertion can produce O(n) height. There are no automatic rotations.

## Later modules

Traversal and balance modules will operate on the core tree structure. TreeMap
will delegate storage to the BST; ListMap will provide a benchmark baseline.
Rendering, examples, benchmarks, and evaluation artifacts will be added with
their respective milestones. Reserved source modules contain docstrings only.
