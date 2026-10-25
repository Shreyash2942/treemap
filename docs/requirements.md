# Requirements and submission evidence

The project implements an ordinary, unbalanced BST. Balance detection reports
shape; it does not apply rotations. All keys within a tree must have consistent
equality and a stable total ordering. Values may include `None`.

| Requirement | Implementation or document | Verification evidence |
| --- | --- | --- |
| Modular Python package and installable dev extra | `pyproject.toml`, `src/bst_map/` | Editable install, wheel install, dependency checks |
| Generic node with key/value/left/right | `core/node.py` | Node-field tests, mypy, `py.typed` in wheel |
| Ordered insertion and duplicate replacement | `core/bst.py` | Dataset, dictionary-reference, and strict-bound tests |
| Search with distinct stored-None behavior | BST node results, TreeMap/ListMap defaults | Empty/missing/None/default tests |
| Leaf, one-child, two-child, and root deletion | `core/operations.py` | All deletion shapes, repeated removal/reuse, successor checks |
| Minimum and maximum | `minimum_node`, `maximum_node` | Empty, subtree, and repeated-extrema tests |
| Three deterministic traversals | `core/traversals.py` | Exact orders, subtree roots, repeatability, identity, deep trees |
| Height and all-subtree balance factors | `core/balance.py` | Independent breadth-first reference, hidden imbalance tests |
| Complete TreeMap key-value API | `maps/tree_map.py` | Sorted collections, size, 50-item data, seeded integration |
| At least 50 items and diverse data | Six fixtures in `tests/conftest.py` | `test_datasets.py`, shared-map tests, 50 preloads plus 50 updates |
| Invariant checks after selected mutations | Strict lower/upper bounds and size helper | Dataset, seeded, and repeated-deletion sequences |
| Iterative handling of skewed trees | All core/traversal/balance/render operations | Trees beyond the active recursion limit |
| Reproducible diagrams before/after deletion | `docs/diagrams/tree_before.txt`, `tree_after.txt` | Golden-file renderer tests and demo output |
| Sequential list-backed comparison map | `maps/list_map.py` | Shared contracts, dictionary workloads, comparison-count probe |
| Equivalent hit/miss benchmark workloads | `benchmarks/benchmark_search.py` | Fixed seeds, two shapes, warmups, shuffled order, raw medians |
| Defensible measured performance | `docs/performance_analysis.md`, `results/` | 32 cases, 288 samples, environment and source/result hashes |
| Objectives/setup/API/reproduction guidance | `README.md` | Executed commands and runnable code examples |
| Class responsibilities and dependencies | `docs/architecture.md` | Dependency overview, contracts, complexity, design decisions |
| Two-page analytical academic evaluation | `docs/evaluation.md`, `evaluation.pdf` | Third-person prose, source citations, references, PDF page-count check |
| Complete regression and code quality | Tests, Ruff, mypy | JUnit XML and final validation report |
| Clean, reproducible submission and history | Packaging scripts, Git tag `v1.0.0` | Source ZIP, history bundle, wheel/sdist, SHA-256 manifest |

The evaluation's two-page limit includes its references. It uses APA-style
author/date citations and hanging references without a separate title page,
because student identity/title-page details were not supplied. The graphify
artifacts are an explicitly labeled historical Day 2 snapshot, not final
correctness or performance evidence.
