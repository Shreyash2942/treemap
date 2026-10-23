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

All Day 1 core operations are iterative. With height `h`, each operation takes O(h)
time and O(1) auxiliary space. A reasonably balanced tree has O(log n) height;
sorted insertion can produce O(n) height. There are no automatic rotations.

## Day 2 traversals

`core/traversals.py` exposes `inorder(root)`, `preorder(root)`, and
`postorder(root)`. Each accepts a subtree root or `None` and returns a fresh lazy
iterator of the actual `TreeNode` objects. Empty roots yield no nodes. In-order
visits keys in sorted order; pre-order visits parents first; post-order visits
children first. Iterators have independent progress and do not modify nodes.
Mutating the tree while consuming a traversal is unsupported.

All three traversals use explicit stacks: O(n) time and O(h) auxiliary space.
They work on skewed trees deeper than Python's recursion limit.

## Day 2 height and balance

`core/balance.py` uses edge-count height: an empty subtree has height -1 and a
leaf has height 0. A node's balance factor is `height(left) - height(right)`.
Positive factors indicate a taller left subtree; negative factors indicate a
taller right subtree. Every node must have an absolute factor at most 1 for the
tree to be height-balanced.

`analyze_balance(root)` returns an immutable `BalanceReport` with `height`, the
root's `balance_factor`, `unbalanced_keys` in post-order, and an `is_balanced`
property. An empty tree reports `(-1, 0, (), True)` for those fields. A zero
root factor alone does not guarantee balance; all descendants are inspected.
The `height(root)`, `balance_factor(root)`, and `is_balanced(root)` convenience
functions delegate to the same analyzer and each take O(n) time.

Analysis uses iterative post-order evaluation and child-height stacks. It takes
O(n) time, O(h) working space, and O(u) report space for u unbalanced nodes.
It neither rotates nor mutates the tree, and reports are recomputed on each call.

## Day 2 TreeMap

`maps/tree_map.py` owns a `BinarySearchTree` and delegates storage, lookup,
size, and deletion to it. It uses the shared in-order traversal for collections.
The public class is available from `bst_map`, `bst_map.maps`, or its module.

| Method | Result | Missing key behavior | Time |
| --- | --- | --- | --- |
| `put(key, value)` | `None`; inserts or updates | Inserts | O(h) |
| `get(key, default=None)` | Stored value | Returns default unchanged | O(h) |
| `remove(key)` | Removed value | Raises `KeyError(key)` | O(h) |
| `contains_key(key)` | Boolean | Returns `False` | O(h) |
| `keys()` | New list of sorted keys | Empty list on empty map | O(n) |
| `values()` | New list of values ordered by key | Empty list on empty map | O(n) |
| `items()` | New list of key-value tuples sorted by key | Empty list on empty map | O(n) |
| `len(mapping)` | Number of unique keys | Returns `0` on empty map | O(1) |

`get` tests whether a node exists, so stored `None` values never cause the
default to be returned. Duplicate puts do not increase size. Collections are
independent lists built at call time and take O(n) result space plus O(h)
traversal space; their keys and values remain references to the stored objects.
They are not live views or deep copies. TreeMap inherits the BST's key contract,
comparison errors, and unbalanced worst-case O(n) lookup/mutation behavior.

## Later modules

ListMap will provide the benchmark baseline. ASCII rendering, reproducible
benchmarks, performance analysis, and evaluation artifacts remain future work.
The reserved ListMap and renderer modules contain docstrings only.

## Knowledge graph

The graphify skill generates `graphify-out/graph.html`, `graph.json`, and
`GRAPH_REPORT.md` from the implemented code and project documents. The graph is
an architecture aid, with extracted/inferred confidence labels and numeric
community cohesion scores. Token usage is unavailable in this environment;
the audit records that limitation rather than claiming a measured zero cost.
