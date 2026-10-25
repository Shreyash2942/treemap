# Implementation milestones

## Day 1: BST core (M1 complete)

Establish the Python package and development environment, then implement generic
nodes, insertion, search, deletion using the in-order successor, and extrema.
Validate ordering with strict lower and upper bounds after mutations.

Planned commits:

1. `chore: initialize modular Python project`
2. `feat: define generic tree node structure`
3. `feat: implement BST insertion and search`
4. `feat: implement BST deletion cases`
5. `feat: add BST min and max operations`
6. `test: validate core BST behavior`

M1 acceptance checklist:

- [x] Package installs with development dependencies in `.venv`.
- [x] Generic nodes store key, value, and child references independently.
- [x] Insert and search preserve ordering; duplicate keys update values.
- [x] Delete handles leaves, one child, two children, and root replacement.
- [x] Missing-key and empty-tree behavior is documented and tested.
- [x] Minimum and maximum follow the appropriate outer branches.
- [x] Tests verify strict ancestor bounds and node count after mutations.
- [x] Tests include at least 50 keys, multiple key types, and heterogeneous values.
- [x] Pytest, Ruff lint, and Ruff formatting checks pass.
- [x] Six Day 1 commits exist in the local Git history.

Validation used the available Python 3.14.4 interpreter in `.venv`:

| Check | Result |
| --- | --- |
| `python -m pytest -v` | 69 passed |
| `python -m ruff check .` | Passed |
| `python -m ruff format --check .` | Passed |
| `python -m pip check` | No broken requirements |
| `python examples/demo.py` | Search 40, extrema 20/80, deletion 30, six entries remain |

The randomized tests start with 100 distinct keys and run 400 mixed operations
for each of five fixed seeds. An independent dictionary checks observable
results while the bounds helper checks structure and size after every mutation.
Deep-tree cases exercise both ascending and descending insertion orders beyond
the interpreter's recursion limit. The declared Python 3.11 minimum has not
been separately exercised in this environment.

## Day 2: Traversals, balance, and TreeMap (M2 complete)

Implement three iterative traversals yielding nodes, analyze every subtree's
height and balance, and expose a reusable BST-backed TreeMap with sorted lists
of keys, values, and entries. Height counts edges: empty is -1 and a leaf is 0.

Commit schedule:

7. `feat: implement inorder traversal`
8. `feat: add preorder and postorder traversals`
9. `feat: implement tree balance detection`
10. `feat: create BST-backed TreeMap`
11. `feat: complete TreeMap key-value API`
12. `test: verify traversals and TreeMap integration`

M2 acceptance checklist:

- [x] In-order, pre-order, and post-order match the README's example.
- [x] Traversals handle empty and single-node trees with repeatable output.
- [x] Height and balance factor use a documented, consistent convention.
- [x] Balance analysis inspects all subtrees and reports unbalanced keys.
- [x] TreeMap supports put/get/remove/contains, sorted collections, and length.
- [x] Stored `None` values are distinct from absent keys and get defaults.
- [x] Integration tests cover updates, all root deletion shapes, and 50+ entries.
- [x] Iterative algorithms and TreeMap handle trees beyond the recursion limit.
- [x] All tests, Ruff checks, dependency checks, and the expanded demo pass.
- [x] Graphify HTML, JSON, and an honest audit report reflect Day 2.
- [x] Six additional commits exist (twelve total).

Validation on Python 3.14.4:

| Check | Result |
| --- | --- |
| `python -m pytest -q` | 140 passed (69 Day 1 and 71 new Day 2 cases) |
| `python -m ruff check .` | Passed |
| `python -m ruff format --check .` | Passed |
| `python -m pip check` | No broken requirements |
| `python examples/demo.py` | Traversal orders, balanced/skewed reports, and TreeMap examples passed |

Balance tests compare subtree heights with an independent breadth-first
reference. Three seeded map workloads each start with 100 keys, then perform
400 mixed operations checked against a dictionary and strict BST invariants.
The graph report separates extracted/inferred links and discloses unavailable
token counters. Graphify is installed separately from the project's `.venv`.

## Day 3: Testing, visualization, and performance (M3 complete)

Validate six explicit datasets, produce diagrams, implement sequential ListMap,
and run equivalent search workloads on both maps with reproducible evidence.

Commit schedule:

13. `test: add diverse 50-item datasets`
14. `test: expand edge-case and invariant coverage`
15. `feat: add ASCII tree visualization`
16. `feat: implement list-based comparison Map`
17. `perf: add reproducible search benchmarks`
18. `docs: record performance findings and diagrams`

M3 acceptance checklist:

- [x] Six named scenarios cover random, sorted, reverse, string, mixed values,
  and 50 replacement operations after a 50-key preload.
- [x] Strict bounds and size are checked after mutations in selected sequences.
- [x] Empty/missing keys, repeated deletions, and reuse after emptying are covered.
- [x] Iterative ASCII rendering generates the actual before/after diagrams.
- [x] Sequential ListMap has equivalent value/default/update semantics for valid keys.
- [x] Benchmarks use 50/100/500/1,000 entries, two tree shapes, and hit/miss queries.
- [x] Seeds, warmups, repetitions, measurement order, and timed scope are explicit.
- [x] Median results, 288 raw samples, environment/source hashes, and a PNG are saved.
- [x] Performance analysis explains favorable shapes, degeneration, and limits.
- [x] The complete 204-test regression suite and Ruff/dependency checks pass.
- [x] Six additional commits exist (eighteen total).

Validation on Python 3.14.4:

| Check | Result |
| --- | --- |
| `python -m pytest -q --junitxml=results/pytest_results.xml` | 204 passed, no failures/errors/skips |
| `pytest -q` | 204 passed; benchmark imports also work with the standalone entry point |
| `python -m ruff check .` | Passed |
| `python -m ruff format --check .` | Passed |
| `python -m pip check` | No broken requirements |
| `python examples/demo.py` | Actual before/after diagrams and existing examples passed |
| `python benchmarks/benchmark_search.py` | 32 summary cells, 288 measured batches, PNG and metadata |

The benchmark uses seed 506, 4,000 queries per sample, nine measured repetitions,
and two warmups. Median-first tree heights are 5/6/8/9; sorted heights are
49/99/499/999. Search results and limitations are recorded in
`docs/performance_analysis.md`. The graphify artifacts intentionally remain
the labeled Day 2 snapshot; graph refresh is not part of M3 acceptance.

## Remaining project scope

The two-page evaluation and final review remain. Their detailed daily schedule
has not yet been supplied.
