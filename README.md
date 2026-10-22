# bstkit

**A modular Python toolkit for Binary Search Trees and tree-based Maps.**

> **Status:** Day 1 complete — BST core implemented and tested
>
> **Language:** Python 3.11+
>
> **Development:** Four-day milestone project

## Overview

`bstkit` is an educational software engineering project that implements a Binary Search Tree (BST) and a Map backed by that tree. It demonstrates ordered key-value storage, tree manipulation, traversal, balance detection, visualization, and search-performance analysis. The repository directory is `treemap`; Python imports use `bst_map`.

The implementation emphasizes modularity, clear interfaces, automated tests, and reproducible benchmarks. **The initial BST is not self-balancing**: balance detection reports problems but does not perform rotations.

## Features

Implemented for Day 1:

- **BST:** Insert, search, delete, find minimum/maximum, and preserve the BST ordering invariant.
- **Generic nodes:** Comparable keys, unrestricted values, and typed child references.
- **Core validation:** 69 tests, including strict ancestor bounds, 50+ entries, and seeded mutations compared with a dictionary.
- **Development setup:** Installable package, virtual environment, pytest, Ruff, and a runnable example.

Planned for later milestones:

- **Traversal:** In-order, pre-order, and post-order traversal with reproducible examples.
- **TreeMap:** Store, retrieve, update, and remove key-value pairs using the BST.
- **Balance analysis:** Calculate tree height and detect unbalanced subtrees.
- **Visualization:** Render ASCII diagrams before and after tree modifications.
- **Testing:** Exercise at least 50 items, multiple comparable key types, heterogeneous values, and edge cases.
- **Benchmarking:** Compare search operations in a BST-backed Map and a list-backed Map.

## Technology

Python 3.11+, Python standard library, `pytest`, `ruff`, and Git. Project configuration will use `pyproject.toml` and a `src/` package layout.

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

Day 1 implements the BST API below. The TreeMap example describes a later milestone.

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
mapping.remove("beta")
```

**Key policy:** Keys within a tree must have a stable total ordering with consistent equality and `<`; inserting an existing key updates its value without changing size. Do not use NaN keys or mutate stored keys. Values may have different types, including `None`.

**BST results:** `insert` returns `None`. `search` returns a `TreeNode`, or `None`
for a missing key, so stored `None` values remain distinguishable from absence.
`delete` returns the removed value and raises `KeyError` for a missing key.
`minimum` and `maximum` return nodes and raise `ValueError` on an empty tree.
`len(tree)` counts distinct keys. See [architecture](docs/architecture.md) for
the key contract, node-reference behavior, and operation complexity.

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

## Tests and code quality

After installation, run:

```bash
python -m pytest -v
python -m ruff check .
python -m ruff format --check .

# Run the Day 1 example
python examples/demo.py
```

Day 1 tests cover empty and single-node trees; duplicate and missing keys; leaf,
one-child, two-child, and root deletion; minimum/maximum; and BST ordering after
mutations. Datasets include **at least 50 items**, six key types tested in separate
trees, heterogeneous values including `None`, trees beyond the recursion limit,
and five seeded workloads of 400 mixed operations starting with 100 keys each.

Validation passed with Python 3.14.4: **69 tests**, Ruff lint and format checks,
dependency consistency, and the demo. Python 3.11 is the minimum supported syntax
target; it has not been separately exercised in this environment. Traversal,
TreeMap, and balance tests will arrive with those implementations.

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

- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) — Day 1 tasks, quality gate, Git commit schedule, and remaining scope.
- [`docs/architecture.md`](docs/architecture.md) — module design and core interfaces.
- `docs/performance_analysis.md` — benchmark methodology and findings *(planned)*.
- `docs/evaluation.pdf` — two-page evaluation of when tree data structures are beneficial *(planned)*.
- `docs/diagrams/` — before-and-after tree diagrams *(planned)*.

## Completion criteria

The project is complete when BST operations preserve ordering; all traversals produce expected output; the Map stores and retrieves entries correctly; minimum/maximum and deletion handle edge cases; balance detection works; the 50+ item tests pass; diagrams and reproducible benchmarks are available; and the two-page evaluation is finished.

## Future improvements

Potential extensions include AVL or red-black balancing, breadth-first traversal, iterative algorithms, property-based tests, and additional benchmark comparisons.

---

**bstkit** — Build, test, visualize, and analyze tree-based data structures in Python.
