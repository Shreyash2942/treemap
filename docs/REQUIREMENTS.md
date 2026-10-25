# TreeMap

## Project Completion Requirements and Success Criteria

Release evidence: **v1.0.2**. The current branch contains the subsequent cleanup.

**Cleanup scope adjustment:** The standalone implementation-plan and submission-guide documents were removed at the user's request. Requirement D-16 now uses `CHANGELOG.md` and Git milestone history as its evidence. The expanded academic report describes the original validated 1.0.2 snapshot; its historical deliverable paths remain available through Git history.

**Project Name:** TreeMap
**Project Type:** Data Structures and Algorithms
**Programming Language:** Python 3.11+
**Architecture:** Modular, Object-Oriented Python
**Development Duration:** 4 Days
**Development Framework:** PSEPF Level 1 — Lightweight Hybrid Agile
**Version Control:** Git and GitHub
**Project Status:** Implementation complete; final release verification recorded below

---

# 1. Project Overview

TreeMap is a modular Python project designed to demonstrate the implementation, functionality, and performance characteristics of Binary Search Trees (BSTs) and tree-based Map data structures.

The project focuses on developing a reusable BST implementation that supports insertion, deletion, searching, traversal algorithms, minimum and maximum operations, and tree balance detection.

The BST will serve as the underlying storage structure for a custom Map implementation that manages key-value pairs.

The project will also include comprehensive automated testing, tree visualization, and performance benchmarking to compare BST-based searching against list-based searching.

The implementation will follow professional software engineering practices, including modular architecture, object-oriented programming, version control, automated testing, and technical documentation.

## 1.1 Primary Objective

Develop a fully functional, modular, tested, and documented Python system that demonstrates how Binary Search Trees can support ordered data storage and key-value retrieval.

## 1.2 Project Scope

The project includes:

* Binary Search Tree implementation.
* Three tree traversal algorithms.
* Tree-based Map implementation.
* Tree manipulation algorithms.
* Tree height and balance detection.
* List-based Map implementation for comparison.
* Automated testing with at least 50 data items.
* Tree visualization before and after modifications.
* Performance benchmarking and analysis.
* Two-page written evaluation.
* Technical documentation and reproducible demonstrations.

Automatic tree rebalancing, database integration, graphical user interfaces, and cloud deployment are outside the initial project scope.

---

# 2. Functional Requirements

All functional requirements must be implemented and verified before project completion.

| ID    | Requirement              | Completion Criteria                                                                  |
| ----- | ------------------------ | ------------------------------------------------------------------------------------ |
| FR-01 | Tree Node Implementation | A reusable node structure stores keys, values, and left/right child references.      |
| FR-02 | BST Construction         | The BST correctly creates and maintains its root and child nodes.                    |
| FR-03 | BST Insertion            | New nodes are inserted while preserving BST ordering.                                |
| FR-04 | BST Searching            | Existing keys are located correctly, and missing keys are handled predictably.       |
| FR-05 | BST Deletion             | Leaf, single-child, two-child, and root deletion are supported.                      |
| FR-06 | Minimum Value            | The smallest key is identified correctly.                                            |
| FR-07 | Maximum Value            | The largest key is identified correctly.                                             |
| FR-08 | In-Order Traversal       | Nodes are visited in left-root-right order.                                          |
| FR-09 | Pre-Order Traversal      | Nodes are visited in root-left-right order.                                          |
| FR-10 | Post-Order Traversal     | Nodes are visited in left-right-root order.                                          |
| FR-11 | Tree Height              | The height of a tree or subtree is calculated correctly.                             |
| FR-12 | Balance Detection        | Balanced and unbalanced trees are identified correctly.                              |
| FR-13 | TreeMap Implementation   | A custom Map stores key-value pairs using the BST.                                   |
| FR-14 | Map Operations           | The Map supports insertion, retrieval, updating, deletion, and key existence checks. |
| FR-15 | Duplicate-Key Handling   | Inserting an existing key updates its value without creating a duplicate node.       |
| FR-16 | ListMap Implementation   | A list-based Map supports equivalent search operations for benchmarking.             |
| FR-17 | Tree Visualization       | Tree structures can be displayed before and after insertion and deletion.            |

### Functional Acceptance Criteria

The functional implementation is complete when:

* All 17 functional requirements are implemented.
* BST ordering is preserved after every supported modification.
* TreeMap uses the BST as its actual storage structure.
* Traversal algorithms return correct sequences.
* Tree manipulation algorithms handle required edge cases.
* Balance detection correctly identifies unbalanced structures.
* Visualization accurately represents the underlying tree.

---

# 3. Modular Architecture Requirements

TreeMap must follow a modular Python package structure.

## 3.1 Required Architecture

```text
treemap/
│
├── src/
│   └── treemap/
│       ├── __init__.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── node.py
│       │   ├── bst.py
│       │   ├── traversals.py
│       │   ├── operations.py
│       │   └── balance.py
│       │
│       ├── maps/
│       │   ├── __init__.py
│       │   ├── tree_map.py
│       │   └── list_map.py
│       │
│       └── visualization/
│           ├── __init__.py
│           └── tree_renderer.py
│
├── tests/
│   ├── conftest.py
│   ├── test_bst.py
│   ├── test_traversals.py
│   ├── test_tree_map.py
│   ├── test_balance.py
│   └── test_edge_cases.py
│
├── benchmarks/
│   └── benchmark_search.py
│
├── examples/
│   └── demo.py
│
├── docs/
│   ├── REQUIREMENTS.md
│   ├── architecture.md
│   ├── performance_analysis.md
│   ├── evaluation.md
│   ├── evaluation.pdf
│   └── diagrams/
│       ├── tree_before.txt
│       └── tree_after.txt
│
├── results/
│   ├── performance_results.csv
│   └── benchmark_chart.png
│
├── pyproject.toml
├── README.md
└── .gitignore
```

## 3.2 Architecture Success Criteria

* Each module has a clearly defined responsibility.
* The BST serves as the single source of truth for tree storage.
* TreeMap delegates key-value storage to the BST.
* Traversal, balance detection, and visualization logic remain modular.
* Python classes use appropriate encapsulation.
* Type hints and generics are applied where appropriate.
* Internal implementation details are separated from public interfaces.
* Modules can be tested independently.
* The project can be installed as a Python package.

---

# 4. Testing Requirements

Automated testing will be implemented using pytest.

| ID    | Requirement         | Completion Criteria                                                                     |
| ----- | ------------------- | --------------------------------------------------------------------------------------- |
| TR-01 | BST Unit Testing    | Insertion, searching, and deletion tests pass.                                          |
| TR-02 | Traversal Testing   | All three traversals match expected outputs.                                            |
| TR-03 | TreeMap Testing     | Key-value operations work correctly.                                                    |
| TR-04 | Balance Testing     | Balanced and unbalanced trees are classified correctly.                                 |
| TR-05 | Dataset Testing     | At least 50 data items are tested.                                                      |
| TR-06 | Data Type Testing   | Integer and string keys work in separate trees, and heterogeneous values are supported. |
| TR-07 | Edge-Case Testing   | Empty trees, missing keys, duplicate keys, and deletion cases are covered.              |
| TR-08 | Invariant Testing   | BST ordering remains valid after modifications.                                         |
| TR-09 | Integration Testing | BST and TreeMap components function correctly together.                                 |
| TR-10 | Regression Testing  | Previously working functionality remains correct after changes.                         |

## 4.1 Required Test Datasets

| Dataset                     | Minimum Items | Purpose                      |
| --------------------------- | ------------: | ---------------------------- |
| Random integer keys         |            50 | General correctness          |
| Sorted integer keys         |            50 | Worst-case tree behavior     |
| Reverse-sorted integer keys |            50 | Degenerate tree construction |
| String keys                 |            50 | Key-type compatibility       |
| Mixed value types           |            50 | Flexible Map storage         |

Different key types must be tested in separate trees unless they support a consistent comparison rule.

## 4.2 Testing Acceptance Criteria

Testing is complete when:

* All required automated tests pass.
* BST invariants remain valid after insertions and deletions.
* TreeMap operations return expected results.
* Traversal results match known reference sequences.
* Balance detection passes balanced and skewed tree tests.
* At least 50 data items are processed successfully.
* No known critical functional defects remain unresolved.

**Required command:**

```bash
python -m pytest -v
```

**Acceptance target:** 100% of required tests passing.

---

# 5. Performance Requirements

The project must evaluate BST-based searching against list-based searching.

| ID    | Requirement           | Completion Criteria                                              |
| ----- | --------------------- | ---------------------------------------------------------------- |
| PR-01 | Search Benchmark      | TreeMap and ListMap search operations are compared.              |
| PR-02 | Dataset Sizes         | Benchmarks include 50, 100, 500, and 1,000 items.                |
| PR-03 | Execution Measurement | Search execution times are recorded.                             |
| PR-04 | Reproducibility       | Fixed datasets and repeated measurements are used.               |
| PR-05 | Complexity Analysis   | Average and worst-case complexity are explained.                 |
| PR-06 | Balance Impact        | Balanced-like and skewed BST structures are evaluated.           |
| PR-07 | Results Visualization | A performance comparison chart is generated.                     |
| PR-08 | Written Analysis      | Results, limitations, and practical implications are documented. |

## 5.1 Expected Algorithm Complexity

| Operation | Balanced BST | Worst-Case BST | ListMap |
| --------- | ------------ | -------------- | ------- |
| Search    | O(log n)     | O(n)           | O(n)    |
| Insert    | O(log n)     | O(n)           | O(n)*   |
| Delete    | O(log n)     | O(n)           | O(n)    |
| Minimum   | O(log n)     | O(n)           | O(n)    |
| Maximum   | O(log n)     | O(n)           | O(n)    |

*ListMap insertion assumes unique-key semantics and therefore may require searching for an existing key before appending.*

## 5.2 Performance Success Criteria

Performance evaluation is complete when:

* Both implementations use equivalent datasets and search workloads.
* Successful and unsuccessful searches are tested.
* Multiple benchmark measurements are recorded.
* Results are saved in CSV format.
* A comparison chart is generated.
* The analysis explains the effects of tree height and insertion order.
* Measured results are distinguished from theoretical complexity.

The evaluation must accurately demonstrate where tree-based searching provides advantages and where unbalanced trees or implementation overhead reduce those benefits.

---

# 6. Software Engineering and Code Quality Requirements

| ID    | Requirement            | Completion Criteria                                                  |
| ----- | ---------------------- | -------------------------------------------------------------------- |
| SE-01 | Modular Design         | Code follows the defined package structure.                          |
| SE-02 | Object-Oriented Design | Classes have appropriate responsibilities.                           |
| SE-03 | Type Hints             | Public interfaces use meaningful type annotations.                   |
| SE-04 | Documentation          | Public classes and methods include useful docstrings.                |
| SE-05 | Error Handling         | Invalid operations are handled consistently.                         |
| SE-06 | Code Formatting        | Ruff formatting checks pass.                                         |
| SE-07 | Code Linting           | Ruff linting checks pass.                                            |
| SE-08 | Dependency Management  | Dependencies are defined in `pyproject.toml`.                        |
| SE-09 | Version Control        | Git history contains meaningful development commits.                 |
| SE-10 | Reproducibility        | Installation, tests, and examples run using documented instructions. |

## 6.1 Required Code Quality Checks

```bash
python -m pytest -v

ruff check .

ruff format --check .
```

All three checks must pass before final submission.

---

# 7. Git and Development Milestone Requirements

The project follows a four-day milestone-based implementation schedule.

| Day       | Milestone                 | Planned Commits | Completion Requirement                                            |
| --------- | ------------------------- | --------------: | ----------------------------------------------------------------- |
| Day 1     | BST Foundation            |               6 | Core BST operations work correctly.                               |
| Day 2     | Traversals and TreeMap    |               6 | Traversals, balance detection, and Map integration work.          |
| Day 3     | Testing and Performance   |               6 | Comprehensive tests, visualizations, and benchmarks are complete. |
| Day 4     | Documentation and Release |               5 | Documentation and final verification are complete.                |
| **Total** | **4 Milestones**          |          **23** | **All acceptance criteria satisfied**                             |

## 7.1 Git Success Criteria

* Commits represent meaningful implementation progress.
* Commit messages follow Conventional Commits conventions.
* Core functionality is tested before milestone completion.
* No unnecessary generated files or virtual environments are committed.
* The final repository contains the complete source code and documentation.
* The final working tree is clean.

The target is 23 planned commits. Additional meaningful commits are acceptable when necessary.

---

# 8. Required Project Deliverables

| ID   | Deliverable                  | Required Location                            |
| ---- | ---------------------------- | -------------------------------------------- |
| D-01 | BST implementation           | `src/treemap/core/bst.py`                    |
| D-02 | Tree node implementation     | `src/treemap/core/node.py`                   |
| D-03 | Tree manipulation algorithms | `src/treemap/core/operations.py`             |
| D-04 | Three traversal algorithms   | `src/treemap/core/traversals.py`             |
| D-05 | Balance detection            | `src/treemap/core/balance.py`                |
| D-06 | TreeMap implementation       | `src/treemap/maps/tree_map.py`               |
| D-07 | ListMap implementation       | `src/treemap/maps/list_map.py`               |
| D-08 | Tree visualization           | `src/treemap/visualization/tree_renderer.py` |
| D-09 | Automated tests              | `tests/`                                     |
| D-10 | Demonstration program        | `examples/demo.py`                           |
| D-11 | Benchmark program            | `benchmarks/benchmark_search.py`             |
| D-12 | Benchmark results and chart  | `results/`                                   |
| D-13 | Performance analysis         | `docs/performance_analysis.md`               |
| D-14 | Two-page evaluation          | `docs/evaluation.pdf`                        |
| D-15 | Architecture documentation   | `docs/architecture.md`                       |
| D-16 | Development milestone record | `CHANGELOG.md` and Git history |
| D-17 | Completion requirements      | `docs/REQUIREMENTS.md`                       |
| D-18 | Main README                  | `README.md`                                  |

**Deliverable acceptance:** All 18 required deliverables must exist and accurately reflect the final implementation.

---

# 9. Project Success Criteria

The following success criteria determine whether TreeMap has achieved its intended objectives.

## SC-01 — BST Correctness

The BST must maintain its ordering property after insertion, searching, and deletion operations.

**Verification:** Automated invariant tests and known reference trees.

## SC-02 — Traversal Accuracy

In-order, pre-order, and post-order traversal algorithms must produce correct sequences.

**Verification:** Automated tests comparing actual and expected traversal outputs.

## SC-03 — TreeMap Functionality

The Map must successfully store, retrieve, update, and remove key-value pairs using the BST.

**Verification:** Unit and integration tests.

## SC-04 — Tree Manipulation Accuracy

Minimum, maximum, and deletion algorithms must operate correctly across normal and edge cases.

**Verification:** Tests covering empty, single-node, and multi-node trees.

## SC-05 — Balance Detection

The system must correctly identify balanced and unbalanced trees.

**Verification:** Tests using balanced, sorted, and reverse-sorted insertion sequences.

## SC-06 — Data Compatibility

The implementation must process at least 50 data items and support the specified key and value types.

**Verification:** Parameterized tests using multiple datasets.

## SC-07 — Performance Evaluation

The project must provide a valid comparison between BST-based and list-based searching.

**Verification:** Reproducible benchmark results, charts, and written analysis.

## SC-08 — Modular Architecture

The implementation must follow the defined Python package architecture with clear module responsibilities.

**Verification:** Architecture review and integration testing.

## SC-09 — Code Quality

The project must pass automated tests, linting, and formatting checks.

**Verification:** Successful execution of pytest and Ruff.

## SC-10 — Documentation

The project must include accurate technical documentation, visualizations, and a two-page written evaluation.

**Verification:** Review of all required documentation deliverables.

## SC-11 — Git Development History

The repository must demonstrate incremental development across the four milestones.

**Verification:** Review Git commits and milestone completion evidence.

## SC-12 — Final Project Readiness

The complete project must be installable, executable, testable, and reproducible using documented commands.

**Verification:** Final acceptance testing in a clean development environment.

---

# 10. Final Project Completion Checklist

## Functional Implementation

* [x] BST node structure implemented.
* [x] BST insertion implemented.
* [x] BST searching implemented.
* [x] BST deletion implemented.
* [x] Minimum and maximum operations implemented.
* [x] In-order traversal implemented.
* [x] Pre-order traversal implemented.
* [x] Post-order traversal implemented.
* [x] Tree height calculation implemented.
* [x] Balance detection implemented.
* [x] TreeMap implemented.
* [x] ListMap implemented.
* [x] Tree visualization implemented.

## Testing and Validation

* [x] At least 50 data items tested.
* [x] Multiple supported data types tested.
* [x] BST ordering validated.
* [x] All deletion cases tested.
* [x] All traversal outputs verified.
* [x] Map integration tests passed.
* [x] Balance detection tests passed.
* [x] All required pytest tests passed.

## Performance

* [x] TreeMap and ListMap benchmarks completed.
* [x] All planned dataset sizes tested.
* [x] Execution times recorded.
* [x] Performance CSV generated.
* [x] Benchmark chart generated.
* [x] Performance analysis completed.

## Documentation

* [x] Main README completed.
* [x] Architecture documentation completed.
* [x] Development milestone record retained in CHANGELOG and Git history.
* [x] Requirements document completed.
* [x] Tree diagrams generated.
* [x] Traversal examples documented.
* [x] Two-page written evaluation completed.
* [x] Performance report completed.

## Code Quality and Release

* [x] Modular architecture verified.
* [x] Type hints and docstrings reviewed.
* [x] Ruff linting passed.
* [x] Ruff formatting passed.
* [x] Installation instructions verified.
* [x] Demonstration program executed successfully.
* [x] Git history reviewed.
* [x] Final project files committed and pushed.
* [x] Repository working tree clean.

---

# 11. Final Definition of Done

The TreeMap project is considered successfully completed when:

1. All mandatory functional requirements are implemented and verified.
2. BST operations consistently preserve the binary search tree property.
3. All three traversal algorithms return correct results.
4. TreeMap successfully manages key-value pairs using BST storage.
5. Tree manipulation and balance detection algorithms operate correctly.
6. Automated tests validate at least 50 data items and required edge cases.
7. Performance benchmarks provide reproducible comparisons against ListMap.
8. Tree visualizations demonstrate insertion and deletion behavior.
9. The modular Python architecture meets the defined engineering standards.
10. All required documentation and the two-page evaluation are complete.
11. Automated testing, linting, and formatting checks pass.
12. The repository contains all required deliverables and accurately documents development progress.

**Final Acceptance Standard**

TreeMap will be considered complete only when all mandatory requirements and success criteria have been satisfied through implementation, automated testing, documented evidence, and final project review.

The completed system must demonstrate correct tree-based data management, reliable algorithms, modular software architecture, and an accurate assessment of the benefits and limitations of Binary Search Trees.

---

# 12. Requirement-to-Evidence Matrix

The project implements an ordinary, unbalanced BST. Balance detection reports
shape; it does not apply rotations. All keys within a tree must have consistent
equality and a stable total ordering. Values may include `None`.

| Requirement | Implementation or document | Verification evidence |
| --- | --- | --- |
| Modular Python package and installable dev extra | `pyproject.toml`, `src/treemap/` | Editable install, wheel install, dependency checks |
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
| Clean, reproducible submission and history | Standard Python/Git commands in README, historical release tags | Source ZIP, history bundle, wheel/sdist, clean-install verification |

The evaluation's two-page limit includes its references. It uses APA-style
author/date citations and hanging references without a separate title page,
because student identity/title-page details were not supplied. The expanded
report is retained as PDF and editable Word; its figures are embedded in those files.
