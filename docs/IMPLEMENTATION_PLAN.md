# Implementation milestones

## Day 1: BST core (M1)

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

- [ ] Package installs with development dependencies in `.venv`.
- [ ] Generic nodes store key, value, and child references independently.
- [ ] Insert and search preserve ordering; duplicate keys update values.
- [ ] Delete handles leaves, one child, two children, and root replacement.
- [ ] Missing-key and empty-tree behavior is documented and tested.
- [ ] Minimum and maximum follow the appropriate outer branches.
- [ ] Tests verify strict ancestor bounds and node count after mutations.
- [ ] Tests include at least 50 keys, multiple key types, and heterogeneous values.
- [ ] Pytest, Ruff lint, and Ruff formatting checks pass.
- [ ] Six Day 1 commits exist in the local Git history.

## Remaining project scope

The README defines the remaining features: traversals, TreeMap and ListMap,
height and balance analysis, ASCII rendering, reproducible search benchmarks,
performance analysis, and a two-page evaluation. These are later milestones;
their detailed daily schedules have not yet been supplied.
