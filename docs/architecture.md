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

## Day 3 ListMap and visualization

`maps/list_map.py` stores `(key, value)` tuples in a list in insertion order.
`get` checks equality sequentially and returns on the first match; `put`
replaces the value of an equal key while retaining the original key, or appends
a new entry. `remove` scans and removes an entry, raising `KeyError` if absent.
All three operations are O(n), `len` is O(1), and sorted collection snapshots
are O(n log n). Values and default semantics match TreeMap. Keys must satisfy
the shared total-order contract; invalid mixed types can fail at different
points because ListMap equality lookup does not need the BST's `<` comparisons.

`visualization/tree_renderer.py` exposes `render_tree(root, show_values=False)`.
It returns `(empty)` for no root, otherwise emits the root followed by L/R
branches with ASCII connectors, left before right. `ascii()` escapes keys and
optional values to one line. Stable representations are required for repeatable
labels. The renderer never mutates nodes and uses an explicit stack, including
for deep trees. Time and storage depend on emitted text: long chains can require
O(n*h) characters of indentation. The traversal stack has O(h) entries, whose
prefix strings also contribute storage; this is not a compact layout algorithm.

## Day 3 benchmark and evidence

`benchmarks/benchmark_search.py` is a standalone command against the installed
package. It creates even integer keys, builds both maps with the same entries
in the same insertion order, and uses seeded hit/miss workloads. Median-first
insertion produces a controlled balanced shape; sorted insertion produces a
right chain. Misses cover below-minimum, interior-gap, and above-maximum keys.
Stored `None` values are included, and default-sentinel identity is validated
before timing so a missing lookup cannot masquerade as a stored `None`.

Only prebound public `get(key, default)` calls and their Python loop are timed
with `perf_counter_ns`. Building maps, generating queries, correctness checks,
height calculation, and output generation are outside timing. Garbage collection
is disabled during measurement and restored afterward. Each cell warms up,
then measures both maps in a seeded shuffled order for every repetition.

The summary CSV reports the median of batch means, minimum, maximum, and IQR.
Raw CSV retains query counts and total elapsed nanoseconds so every statistic
can be reconstructed. Metadata records interpreter/platform, timer, configuration,
Git revision, and SHA-256 source/result hashes. `.gitattributes` preserves exact
CSV bytes across Git checkout. Plotting is optional via the `benchmark` extra;
Matplotlib is imported only when creating the PNG. Neither map needs it at runtime.

The full run and constraints are documented in `performance_analysis.md`.
`results/pytest_results.xml` records the full 204-case regression run. The two-page
evaluation remains the final milestone.

Pytest adds the repository root to its test import path so the standalone
`pytest` command can import the benchmark module just like `python -m pytest`.
The runtime `bst_map` package still comes from the installed `src/` package.

## Knowledge graph

The graphify skill generated `graphify-out/graph.html`, `graph.json`, and
`GRAPH_REPORT.md` as a Day 2 snapshot of the code and documents, before the Day 3
modules above existed. Refresh graphify to include the current implementation.
The graph is an architecture aid, with extracted/inferred confidence labels and numeric
community cohesion scores. Token usage is unavailable in this environment;
the audit records that limitation rather than claiming a measured zero cost.
