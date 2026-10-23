# bstkit

**A modular Python toolkit for Binary Search Trees and tree-based Maps.**

> **Status:** Days 1 and 2 complete — BST, traversals, balance analysis, and TreeMap
>
> **Language:** Python 3.11+
>
> **Development:** Four-day milestone project

## Overview

`bstkit` is an educational software engineering project that implements a Binary Search Tree (BST) and a Map backed by that tree. It demonstrates ordered key-value storage, tree manipulation, traversal, balance detection, visualization, and search-performance analysis. The repository directory is `treemap`; Python imports use `bst_map`.

The implementation emphasizes modularity, clear interfaces, automated tests, and reproducible benchmarks. **The initial BST is not self-balancing**: balance detection reports problems but does not perform rotations.

## Features

Implemented through Day 2:

- **BST:** Insert, search, delete, find minimum/maximum, and preserve the BST ordering invariant.
- **Generic nodes:** Comparable keys, unrestricted values, and typed child references.
- **Traversal:** Iterative in-order, pre-order, and post-order node iterators.
- **TreeMap:** Complete key-value API with sorted collections and stored `None` support.
- **Balance analysis:** Height, root balance factor, overall balance, and unbalanced node keys.
- **Validation:** 140 tests, including strict ancestor bounds, 50+ entries, deep trees, and seeded mutations compared with a dictionary.
- **Development setup:** Installable package, virtual environment, pytest, Ruff, and a runnable example.

Planned for later milestones:

- **Visualization:** Render ASCII diagrams before and after tree modifications.
- **Benchmarking:** Compare search operations in a BST-backed Map and a list-backed Map.

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

# Run the BST, traversal, balance, and TreeMap examples
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

Validation passed with Python 3.14.4: **140 tests**, Ruff lint and format checks,
dependency consistency, and the demo. Python 3.11 is the minimum supported syntax
target; it has not been separately exercised in this environment.

## Performance evaluation

The benchmark will compare equivalent search workloads in `TreeMap` and a simple list-backed `ListMap`, using dataset sizes of **50, 100, 500, and 1,000** items. Results will be recorded in `results/` after execution.

| Search structure | Typical behavior | Worst case |
|---|---|---|
| Reasonably balanced BST | O(log n) | O(n) across arbitrary BST shapes |
| Degenerate BST | O(n) | O(n) |
| Unsorted list-backed Map | O(n) | O(n) |

Benchmarks will use repeatable datasets, multiple runs, and both successful and unsuccessful lookups. **No speed advantage is claimed until measured.**

## Documentation

Detailed planning and project evidence are maintained separately from this README:

- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) — Days 1 and 2 tasks, quality gates, Git commit schedules, and remaining scope.
- [`docs/architecture.md`](docs/architecture.md) — module design and core interfaces.
- `docs/performance_analysis.md` — benchmark methodology and findings *(planned)*.
- `docs/evaluation.pdf` — two-page evaluation of when tree data structures are beneficial *(planned)*.
- `docs/diagrams/` — before-and-after tree diagrams *(planned)*.

## Project knowledge graph

Graphify outputs are available in [`graphify-out/`](graphify-out/):

- [`graph.html`](graphify-out/graph.html) — interactive architecture graph; open in a browser.
- [`graph.json`](graphify-out/graph.json) — graph data with sources and confidence labels.
- [`GRAPH_REPORT.md`](graphify-out/GRAPH_REPORT.md) — communities, cohesion, connections, and audit limitations.

The graph is a snapshot of code and documentation, not a correctness proof.
Graphify's token counters are unavailable here; no measured token cost is claimed.

## Completion criteria

The project is complete when BST operations preserve ordering; all traversals produce expected output; the Map stores and retrieves entries correctly; minimum/maximum and deletion handle edge cases; balance detection works; the 50+ item tests pass; diagrams and reproducible benchmarks are available; and the two-page evaluation is finished.

## Future improvements

Potential extensions include AVL or red-black balancing, breadth-first traversal, iterative algorithms, property-based tests, and additional benchmark comparisons.

---

**bstkit** — Build, test, visualize, and analyze tree-based data structures in Python.
