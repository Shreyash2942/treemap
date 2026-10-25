# bstkit

**A modular Python toolkit for Binary Search Trees and tree-based Maps.**

> **Status:** Days 1–3 complete — tested maps, tree diagrams, and measured benchmarks
>
> **Language:** Python 3.11+
>
> **Development:** Four-day milestone project

## Overview

`bstkit` is an educational software engineering project that implements a Binary Search Tree (BST) and a Map backed by that tree. It demonstrates ordered key-value storage, tree manipulation, traversal, balance detection, visualization, and search-performance analysis. The repository directory is `treemap`; Python imports use `bst_map`.

The implementation emphasizes modularity, clear interfaces, automated tests, and reproducible benchmarks. **The initial BST is not self-balancing**: balance detection reports problems but does not perform rotations.

## Features

Implemented through Day 3:

- **BST:** Insert, search, delete, find minimum/maximum, and preserve the BST ordering invariant.
- **Generic nodes:** Comparable keys, unrestricted values, and typed child references.
- **Traversal:** Iterative in-order, pre-order, and post-order node iterators.
- **TreeMap:** Complete key-value API with sorted collections and stored `None` support.
- **Balance analysis:** Height, root balance factor, overall balance, and unbalanced node keys.
- **ListMap:** Sequential lookup with the same valid-key API as TreeMap.
- **Visualization:** Deterministic ASCII diagrams before and after deletion.
- **Benchmarking:** Reproducible hit/miss searches, raw samples, environment metadata, and a PNG chart.
- **Validation:** 204 tests, including six explicit 50-item scenarios, strict ancestor bounds, deep trees, and dictionary comparisons.
- **Development setup:** Installable package, virtual environment, pytest, Ruff, and a runnable example.

Remaining: the two-page evaluation and final project review.

## Technology

Python 3.11+, Python standard library, `pytest`, `ruff`, and Git. Project configuration uses `pyproject.toml` and a `src/` package layout. Graphify is an optional analysis tool, separate from runtime and development dependencies.

## Planned repository structure

```text
treemap/
├── src/
│   └── bst_map/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── node.py
│       │   ├── bst.py
│       │   ├── operations.py
│       │   ├── traversals.py
│       │   └── balance.py
│       ├── maps/
│       │   ├── __init__.py
│       │   ├── tree_map.py
│       │   └── list_map.py
│       └── visualization/
│           ├── __init__.py
│           └── tree_renderer.py
├── tests/
│   ├── conftest.py
│   ├── test_bst.py
│   ├── test_traversals.py
│   ├── test_tree_map.py
│   ├── test_balance.py
│   ├── test_datasets.py
│   ├── test_list_map.py
│   ├── test_tree_renderer.py
│   ├── test_benchmark_search.py
│   └── test_edge_cases.py
├── benchmarks/
│   └── benchmark_search.py
├── examples/
│   └── demo.py
├── docs/
│   ├── IMPLEMENTATION_PLAN.md
│   ├── architecture.md
│   ├── performance_analysis.md
│   ├── evaluation.md
│   ├── evaluation.pdf
│   └── diagrams/
├── results/
│   ├── performance_results.csv
│   └── benchmark_chart.png
├── pyproject.toml
├── .gitattributes
├── .gitignore
└── README.md
```

> The structure above is the **target layout**; files will be added as milestones are implemented.

## Getting started

From the repository directory:

```bash
# Create a virtual environment
python -m venv .venv

# Activate it on macOS/Linux
source .venv/bin/activate
# Or on Windows PowerShell:
# .venv\Scripts\Activate.ps1

# Install project and development dependencies
python -m pip install -e ".[dev]"

# Also install plotting support to generate the benchmark PNG
python -m pip install -e ".[dev,benchmark]"
```

On Windows, activation is optional: use `.venv\Scripts\python.exe` in place of
`python` if PowerShell script execution is disabled.

## API

The BST and TreeMap APIs below are implemented.

### Binary Search Tree

```python
from bst_map.core.bst import BinarySearchTree

tree = BinarySearchTree()
for key in [50, 30, 70, 20, 40, 60, 80]:
    tree.insert(key, f"value-{key}")

assert tree.search(40).value == "value-40"
assert tree.minimum().key == 20
assert tree.maximum().key == 80
assert tree.delete(30) == "value-30"
assert len(tree) == 6
```

### TreeMap

```python
from bst_map.maps.tree_map import TreeMap

mapping = TreeMap()
mapping.put("alpha", 10)
mapping.put("beta", 20)
mapping.put("alpha", 15)  # Update an existing key

assert mapping.get("alpha") == 15
assert mapping.contains_key("beta")
assert mapping.keys() == ["alpha", "beta"]
assert mapping.values() == [15, 20]
assert mapping.items() == [("alpha", 15), ("beta", 20)]
assert mapping.remove("beta") == 20
assert len(mapping) == 1

mapping.put("optional", None)
assert mapping.contains_key("optional")
assert mapping.get("optional", "fallback") is None
assert mapping.get("missing", "fallback") == "fallback"
```

**Key policy:** Keys within a tree must have a stable total ordering with consistent equality and `<`; inserting an existing key updates its value without changing size. Do not use NaN keys or mutate stored keys. Values may have different types, including `None`.

**BST results:** `insert` returns `None`. `search` returns a `TreeNode`, or `None`
for a missing key, so stored `None` values remain distinguishable from absence.
`delete` returns the removed value and raises `KeyError` for a missing key.
`minimum` and `maximum` return nodes and raise `ValueError` on an empty tree.
`len(tree)` counts distinct keys. See [architecture](docs/architecture.md) for
the key contract, node-reference behavior, and operation complexity.

**TreeMap results:** `put` returns `None`; `remove` returns the removed value
and raises `KeyError` if absent. `keys`, `values`, and `items` return new lists,
ordered by key, containing references to the stored keys and values.

`ListMap` is available from `bst_map` or `bst_map.maps.list_map`. It offers the
same methods for valid, mutually comparable keys, storing entries in a list
and scanning sequentially. Lookup/update/removal are O(n); sorted collections
are O(n log n). TreeMap operations depend on tree height. Both retain stored
`None` values and return the supplied default only for an absent key.

## Traversal example

For insertion order `50, 30, 70, 20, 40, 60, 80`:

```text
         50
       /    \
     30      70
    /  \    /  \
   20  40  60  80
```

| Traversal | Expected key order |
|---|---|
| In-order | 20, 30, 40, 50, 60, 70, 80 |
| Pre-order | 50, 30, 20, 40, 70, 60, 80 |
| Post-order | 20, 40, 30, 60, 80, 70, 50 |

```python
from bst_map.core import analyze_balance, inorder, postorder, preorder

for traversal in [inorder, preorder, postorder]:
    print([node.key for node in traversal(tree.root)])

report = analyze_balance(tree.root)
print(report.height, report.is_balanced, report.unbalanced_keys)
```

Each traversal accepts a subtree root, yields the actual nodes, and returns an
empty iterator for `None`. The table describes the seven-node tree before
deletion; after the BST example's `delete(30)`, output reflects that mutation.

Height counts edges: empty tree **−1**, leaf **0**. Balance factor is
`height(left) - height(right)`. `analyze_balance` returns the tree's height,
root balance factor, overall `is_balanced`, and a tuple of unbalanced keys in
post-order. It checks every subtree and performs no rotations. The convenience
functions `height(root)`, `balance_factor(root)`, and `is_balanced(root)` are
also available from `bst_map.core`.

## Tests and code quality

After installation, run:

```bash
python -m pytest -v
python -m ruff check .
python -m ruff format --check .

# Run the maps, algorithms, and before/after ASCII diagrams
python examples/demo.py
```

Day 1 tests cover empty and single-node trees; duplicate and missing keys; leaf,
one-child, two-child, and root deletion; minimum/maximum; and BST ordering after
mutations. Datasets include **at least 50 items**, six key types tested in separate
trees, heterogeneous values including `None`, trees beyond the recursion limit,
and five seeded workloads of 400 mixed operations starting with 100 keys each.

Day 2 adds traversal repeatability and node identity checks, every-subtree
balance validation against breadth-first reference heights, sorted map
collections, stored `None` and defaults, and three seeded TreeMap workloads.
Traversal, balance, and map integration tests also exceed the recursion limit.

Day 3 adds explicit 50-item random/sorted/reverse/string/mixed-value datasets,
50 duplicate-key updates after preloading 50 keys, repeated deletions to empty,
ListMap equivalence, golden tree diagrams, and benchmark-methodology tests.
The committed [JUnit report](results/pytest_results.xml) records the full run.

Validation passed with Python 3.14.4: **204 tests**, Ruff lint and format checks,
dependency consistency, and the demo. Python 3.11 is the minimum supported syntax
target; it has not been separately exercised in this environment.

## Performance evaluation

The executed benchmark uses **50, 100, 500, and 1,000** entries, median-first
and sorted insertion, and identical successful/unsuccessful queries for both
maps. Each result is the median of nine batch means, with 4,000 queries per
batch, two warmups, and fixed seed 506. Construction is outside timing.

```bash
python benchmarks/benchmark_search.py
# Without the optional plotting dependency:
python benchmarks/benchmark_search.py --no-chart
```

Measured on this machine with CPython 3.14.4:

| 1,000 entries | TreeMap hit (µs) | ListMap hit (µs) | TreeMap miss (µs) | ListMap miss (µs) |
| --- | ---: | ---: | ---: | ---: |
| Median-first, height 9 | 0.283 | 7.099 | 0.340 | 15.879 |
| Sorted, height 999 | 10.855 | 6.603 | 10.896 | 13.268 |

These are per-lookup batch averages, not individual-operation latency
percentiles. Balanced shape helped TreeMap here; ListMap won successful
lookups against the sorted chain. See the [performance analysis](docs/performance_analysis.md)
for all sizes, exact methodology, uncertainty, and limits.

![Measured lookup times](results/benchmark_chart.png)

Evidence: [summary CSV](results/performance_results.csv),
[288 raw samples](results/benchmark_samples.csv),
[environment and source hashes](results/benchmark_metadata.json), and
[installed versions](results/benchmark_environment.txt). Re-running replaces
the benchmark evidence in `results/`; exact timings vary with the environment.

| Search structure | Typical behavior | Worst case |
|---|---|---|
| Reasonably balanced BST | O(log n) | O(n) across arbitrary BST shapes |
| Degenerate BST | O(n) | O(n) |
| Unsorted list-backed Map | O(n) | O(n) |

Median-first insertion deliberately constructs a favorable shape; the BST
does not rebalance itself. Measurements cover this implementation and workload,
not a universal speed advantage or proof of asymptotic complexity.

## Reproducible tree diagrams

```python
from bst_map.visualization import render_tree

print(render_tree(tree.root))
print(render_tree(tree.root, show_values=True))
```

The renderer labels left/right links, escapes labels to ASCII, and handles
empty and deep trees without recursion. Checked-in diagrams show the seven-node
example [before deletion](docs/diagrams/tree_before.txt) and
[after deleting 30](docs/diagrams/tree_after.txt), using successor 40.

## Documentation

Detailed planning and project evidence are maintained separately from this README:

- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) — Days 1–3 tasks, quality gates, Git commit schedules, and remaining scope.
- [`docs/architecture.md`](docs/architecture.md) — module design and core interfaces.
- [`docs/performance_analysis.md`](docs/performance_analysis.md) — executed benchmark methodology, results, and limits.
- `docs/evaluation.pdf` — two-page evaluation of when tree data structures are beneficial *(planned)*.
- [`docs/diagrams/`](docs/diagrams/) — reproducible before-and-after tree diagrams.

## Project knowledge graph

Graphify outputs are available in [`graphify-out/`](graphify-out/):

- [`graph.html`](graphify-out/graph.html) — interactive architecture graph; open in a browser.
- [`graph.json`](graphify-out/graph.json) — graph data with sources and confidence labels.
- [`GRAPH_REPORT.md`](graphify-out/GRAPH_REPORT.md) — communities, cohesion, connections, and audit limitations.

The checked-in graph is the **Day 2 snapshot**, before ListMap, the renderer,
and the benchmark were implemented. It is not a current Day 3 architecture graph
or a correctness proof; re-run graphify to refresh it.
Graphify's token counters are unavailable here; no measured token cost is claimed.

## Completion criteria

The project is complete when BST operations preserve ordering; all traversals produce expected output; the Map stores and retrieves entries correctly; minimum/maximum and deletion handle edge cases; balance detection works; the 50+ item tests pass; diagrams and reproducible benchmarks are available; and the two-page evaluation is finished.

## Future improvements

Potential extensions include AVL or red-black balancing, breadth-first traversal, property-based tests, and additional benchmark comparisons.

---

**bstkit** — Build, test, visualize, and analyze tree-based data structures in Python.
