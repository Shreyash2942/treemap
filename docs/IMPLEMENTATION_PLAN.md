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

## Remaining project scope

The README defines the remaining features: traversals, TreeMap and ListMap,
height and balance analysis, ASCII rendering, reproducible search benchmarks,
performance analysis, and a two-page evaluation. These are later milestones;
their detailed daily schedules have not yet been supplied.
