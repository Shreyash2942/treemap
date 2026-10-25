# TreeMap: Detailed User Guide

This guide explains how to install TreeMap, run its examples, use the library in
Python programs, inspect trees, run tests, and reproduce the performance analysis.
The project name is **TreeMap**; the distribution and Python import are `treemap`.
These instructions describe the API delivered in release `v1.0.2`.

## Contents

1. [What the project does](#1-what-the-project-does)
2. [Requirements and download](#2-requirements-and-download)
3. [Installation](#3-installation)
4. [Run the demonstration](#4-run-the-demonstration)
5. [Use TreeMap in your own program](#5-use-treemap-in-your-own-program)
6. [Work directly with a BST](#6-work-directly-with-a-bst)
7. [Traverse a tree and check its balance](#7-traverse-a-tree-and-check-its-balance)
8. [Display a tree before and after deletion](#8-display-a-tree-before-and-after-deletion)
9. [Use the comparison ListMap](#9-use-the-comparison-listmap)
10. [Run tests and quality checks](#10-run-tests-and-quality-checks)
11. [Run and interpret benchmarks](#11-run-and-interpret-benchmarks)
12. [Read or rebuild the documentation](#12-read-or-rebuild-the-documentation)
13. [Build an installable package](#13-build-an-installable-package)
14. [Troubleshooting](#14-troubleshooting)
15. [Suggested first-use checklist](#15-suggested-first-use-checklist)

## 1. What the project does

TreeMap is an educational Python library and a set of terminal demonstrations.
It stores key-value pairs in memory and demonstrates how a Binary Search Tree
(BST) maintains keys in order. Data lasts for the lifetime of the Python objects;
the library does not save entries to a database or file automatically.

Choose the class that matches the task:

| Class | Use it for | Import |
| --- | --- | --- |
| `TreeMap` | Store values by unique keys and retrieve collections in key order | `from treemap import TreeMap` |
| `BinarySearchTree` | Study nodes, insertion, searching, deletion, and extrema directly | `from treemap import BinarySearchTree` |
| `ListMap` | Compare the same Map operations with sequential list searches | `from treemap import ListMap` |

The BST does not rebalance automatically. Balance analysis reports the shape;
it does not rotate nodes or improve that shape.

## 2. Requirements and download

You need Python **3.11 or newer**. Git is needed for cloning the repository and
reviewing its history. Installation also needs access to the configured Python
package index to download build tools and optional development dependencies.
Runtime verification for the published release used CPython 3.14.4; Python 3.11
is the syntax and type-check target, rather than a separately verified runtime.

Check the tools in PowerShell, Terminal, or your editor's integrated terminal:

```bash
python --version
git --version
```

On macOS/Linux, the Python command may be `python3`. On Windows, `py -3` may be
available if `python` is not found. Select an interpreter whose reported version
is at least 3.11.

Clone the project and enter its directory:

```bash
git clone https://github.com/Shreyash2942/treemap.git
cd treemap
```

Alternatively, extract the provided submission ZIP and open a terminal in the
extracted directory that contains `pyproject.toml`, `README.md`, `src/`, and
`tests/`. A submission ZIP does not contain `.git`; Git history commands require
a clone or the supplied Git bundle. The guide is also available on the current
GitHub branch; older release archives may predate this file.

Run the commands below from this project directory unless instructed otherwise.
If the directory path contains spaces, put the path in quotes when using `cd`.

## 3. Installation

### Windows PowerShell: no activation required

Create a virtual environment and use its interpreter directly. This works when
PowerShell blocks activation scripts, without changing execution policy.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -c "import treemap; print(treemap.__file__)"
.\.venv\Scripts\python.exe examples/demo.py
```

If `python` is unavailable but the Windows launcher works, use
`py -3 -m venv .venv` for the first command. The printed import path should point
to this checkout's `src/treemap/__init__.py` after an editable installation.

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -c "import treemap; print(treemap.__file__)"
python examples/demo.py
```

After activation, `python` and `python -m pip` use the virtual environment.
Run `deactivate` when finished. In a new terminal, activate the environment again.

### Choose the installation options

| Command | What it installs |
| --- | --- |
| `python -m pip install -e .` | The editable library, with no third-party runtime dependencies |
| `python -m pip install -e ".[dev]"` | Library, pytest, Ruff, mypy, build tools, Matplotlib, and PDF validation support |
| `python -m pip install -e ".[benchmark]"` | Library and Matplotlib for benchmark charts |
| `python -m pip install -e ".[docs]"` | Library and tools for generating and inspecting the evaluation PDF |
| `python -m pip install -e ".[dev,docs]"` | Tools for all documented development and documentation workflows |

`-e` means editable: changes to source files are used by the installed library.
The development option is the recommended starting point for reviewing the project.

**Interpreter convention for the rest of this guide:** commands beginning with
`python` assume the virtual environment is active. On Windows without activation,
replace `python` with `.\.venv\Scripts\python.exe`. For example:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

To confirm the installed distribution version:

```bash
python -c "from importlib.metadata import version; print(version('treemap'))"
```

The package's current release version is `1.0.2`.

## 4. Run the demonstration

```bash
python examples/demo.py
```

The demonstration creates a seven-node tree, searches for key 40, reports the
minimum and maximum, prints three traversals, and checks height and balance.
It then displays the tree before and after deleting key 30, and demonstrates
TreeMap updates, sorted entries, missing-key defaults, and stored `None` values.

Selected output includes:

```text
Search 40: value-40
Minimum key: 20
Maximum key: 80
inorder: [20, 30, 40, 50, 60, 70, 80]
preorder: [50, 30, 20, 40, 70, 60, 80]
postorder: [20, 40, 30, 60, 80, 70, 50]
Height: 2; balanced: True
```

The remaining output includes the ASCII diagrams and Map examples. The demo
prints results to the terminal; it does not start a graphical application.

## 5. Use TreeMap in your own program

Save the following as `try_treemap.py` in the project directory, then run
`python try_treemap.py`. Each Python example in this guide is self-contained.

```python
from treemap import TreeMap

scores = TreeMap[str, object]()
scores.put("Ben", 82)
scores.put("Ada", 95)
scores.put("Ben", 88)  # Update the existing entry.

assert len(scores) == 2
print(scores.keys())  # ['Ada', 'Ben']
print(scores.values())  # [95, 88]
print(scores.items())  # [('Ada', 95), ('Ben', 88)]

assert scores.get("Ada") == 95
assert scores.get("Missing", "not found") == "not found"

scores.put("Pending", None)
assert scores.contains_key("Pending")
assert scores.get("Pending", "not found") is None
assert not scores.contains_key("Missing")

removed = scores.remove("Ben")
assert removed == 88
assert len(scores) == 2  # Ada and Pending remain.

try:
    scores.remove("Missing")
except KeyError:
    print("The key does not exist.")
```

### Map method reference

| Method | Result |
| --- | --- |
| `put(key, value)` | Inserts or updates an entry; returns `None` |
| `get(key, default=None)` | Returns the stored value, or the default if the key is absent |
| `remove(key)` | Removes the entry and returns its value; raises `KeyError` if absent |
| `contains_key(key)` | Returns whether the key exists, even when its value is `None` |
| `keys()` | Returns a new list of keys in ascending order |
| `values()` | Returns a new list of values ordered by their keys |
| `items()` | Returns a new list of `(key, value)` tuples ordered by key |
| `len(mapping)` | Returns the number of unique keys |

Use these methods for Map access; bracket access such as `mapping[key]` is not
implemented. Updating a key replaces its value without increasing the size.
Check `contains_key` when a stored `None` must be distinguished from a missing key.

### Key and value rules

Keys within one Map must support a stable total order: equality and `<` must agree
about their ordering. Use, for example, all integer keys or all string keys in
one Map. Mixing integer and string keys can raise `TypeError` during comparison.
Do not use NaN keys or change a stored key's ordering behavior.

Values may have different types, including lists, dictionaries, and `None`.
Returned collections are new lists, but the values inside them are references
to the stored objects. Mutable values are not copied automatically.

## 6. Work directly with a BST

`BinarySearchTree` exposes node-oriented operations for studying the algorithms:

```python
from treemap import BinarySearchTree

tree = BinarySearchTree[int, str]()
for key in [50, 30, 70, 20, 40, 60, 80]:
    tree.insert(key, f"value-{key}")

node = tree.search(40)
assert node is not None
print(node.key, node.value)  # 40 value-40
assert tree.search(999) is None

assert tree.minimum().key == 20
assert tree.maximum().key == 80

tree.insert(40, "updated")
assert len(tree) == 7
assert tree.delete(30) == "value-30"
assert len(tree) == 6

try:
    tree.delete(999)
except KeyError:
    print("Cannot delete an absent key.")
```

`search` returns a `TreeNode`, or `None` for an absent key. It does not return
the value directly. `minimum` and `maximum` also return nodes; both raise
`ValueError` on an empty tree. `delete` returns the removed value and raises
`KeyError` if the key is missing. `insert` returns `None`.

When deleting a node with two children, the implementation uses its in-order
successor: the smallest key in the node's right subtree. In the example above,
key 40 takes the place of key 30.

`tree.root` and `mapping.root` allow inspection, traversal, and rendering.
Leave node keys and child links unchanged; direct structural edits bypass the
BST's ordering and size bookkeeping. Perform updates through the public methods.

## 7. Traverse a tree and check its balance

```python
from treemap import BinarySearchTree
from treemap.core import analyze_balance, inorder, postorder, preorder

tree = BinarySearchTree[int, str]()
for key in [50, 30, 70, 20, 40, 60, 80]:
    tree.insert(key, str(key))

assert [node.key for node in inorder(tree.root)] == [20, 30, 40, 50, 60, 70, 80]
assert [node.key for node in preorder(tree.root)] == [50, 30, 20, 40, 70, 60, 80]
assert [node.key for node in postorder(tree.root)] == [20, 40, 30, 60, 80, 70, 50]

report = analyze_balance(tree.root)
assert report.height == 2
assert report.balance_factor == 0
assert report.is_balanced
assert report.unbalanced_keys == ()

skewed = BinarySearchTree[int, str]()
for key in [1, 2, 3]:
    skewed.insert(key, str(key))
assert not analyze_balance(skewed.root).is_balanced
```

Each traversal accepts a root node, yields nodes, and visits nothing for `None`.
Start a new traversal call to repeat it; a consumed iterator is exhausted.
The same functions work with `mapping.root` from a `TreeMap`.

| Traversal | Visit sequence | Typical use |
| --- | --- | --- |
| In-order | Left, root, right | Read entries in ascending key order |
| Pre-order | Root, left, right | Inspect parents before descendants |
| Post-order | Left, right, root | Inspect descendants before parents |

Height counts edges: an empty tree has height **-1**, a leaf has height **0**.
The balance factor is `height(left) - height(right)`. A tree is height-balanced
only if every node has a balance factor between -1 and 1, inclusive.
`analyze_balance` examines all subtrees and reports unbalanced keys in post-order.
The convenience functions `height`, `balance_factor`, and `is_balanced` are
also available from `treemap.core`.

## 8. Display a tree before and after deletion

```python
from treemap import BinarySearchTree
from treemap.visualization import render_tree

tree = BinarySearchTree[int, str]()
for key in [50, 30, 70, 20, 40, 60, 80]:
    tree.insert(key, f"value-{key}")

before = render_tree(tree.root)
print("Before deletion:")
print(before)

tree.delete(30)
after = render_tree(tree.root)
print("After deleting 30:")
print(after)

assert "L: 30" in before
assert "L: 30" not in after
assert "L: 40" in after
```

The diagram after deletion is:

```text
50
|-- L: 40
|   `-- L: 20
`-- R: 70
    |-- L: 60
    `-- R: 80
```

`L` and `R` identify left and right children. Pass `show_values=True` to
`render_tree` to include values. An empty tree renders as `(empty)`.
The renderer returns a string; use `print` to display it or `Path.write_text`
from Python's standard library to save it. Saved project diagrams are in
[docs/diagrams/](docs/diagrams/).

## 9. Use the comparison ListMap

```python
from treemap import ListMap, TreeMap

for map_type in (TreeMap, ListMap):
    mapping = map_type()
    mapping.put(3, "three")
    mapping.put(1, "one")
    mapping.put(2, None)
    assert mapping.items() == [(1, "one"), (2, None), (3, "three")]
    assert mapping.get(2, "missing") is None
    assert mapping.get(99, "missing") == "missing"
    assert mapping.remove(3) == "three"
```

ListMap offers the same Map methods for valid comparable keys, but stores entries
in a list and searches sequentially. Its sorted collection methods sort the
entries for each call. It has no tree root, traversal, or balance report.

## 10. Run tests and quality checks

Install the `dev` extra, then run:

```bash
python -m pytest -v
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m pip check
```

The current suite contains **213 tests**. A successful run reports all tests
passing. Ruff checks lint and formatting, mypy checks static types, and
`pip check` checks installed dependency compatibility.

For a quieter run or one group of tests:

```bash
python -m pytest -q
python -m pytest tests/test_tree_map.py -v
python -m pytest -k deletion -v
```

Generate a fresh JUnit report separately from the committed evidence:

```bash
python -m pytest -v --junitxml=results/reproduced-tests.xml
```

Validate required file paths and casing, the two-page PDF, recorded benchmark
hashes and statistics, documentation links, and the committed regression report:

```bash
python scripts/validate_release.py --output results/reproduced-validation.json
```

This validator reads the committed JUnit report; it does not run pytest itself.
Run pytest as well when checking current code. The commands above preserve the
published evidence. To intentionally replace the committed JUnit evidence, use
`--junitxml=results/pytest_results.xml`, then run `python scripts/validate_release.py`.

## 11. Run and interpret benchmarks

### Reproduce the complete workload

The `dev` extra already includes Matplotlib. Run:

```bash
python benchmarks/benchmark_search.py --output results/reproduced
```

This uses sizes **50, 100, 500, and 1,000**, seed **506**, **4,000** queries per
sample, **nine** measured repetitions, and **two** warmups. It compares successful
and unsuccessful searches under median-first and sorted insertion orders.
Both implementations receive equivalent data and query workloads.

The command writes these files to `results/reproduced/`:

| File | Contents |
| --- | --- |
| `performance_results.csv` | 32 summary cases with median, minimum, maximum, and IQR in nanoseconds per search |
| `benchmark_samples.csv` | 288 measured batches used to calculate those summaries |
| `benchmark_metadata.json` | Configuration, environment, source hashes, CSV hashes, and Git revision when available |
| `benchmark_chart.png` | Comparison chart with medians and observed batch ranges |

The benchmark does not generate `benchmark_environment.txt`; that file in the
published evidence is a separately captured installed-package snapshot.

### A shorter practice run

```bash
python benchmarks/benchmark_search.py --sizes 50 100 --queries 400 --repeats 3 --warmups 1 --seed 506 --output results/quick-run
```

For a CSV/metadata run without Matplotlib, add `--no-chart` and use a fresh
output directory. Full benchmark sizes are required for the published release
validation; a smaller practice run does not replace that evidence.

### Read the results correctly

Lower time means a faster lookup for that workload. Divide nanoseconds by
1,000 to obtain microseconds. Each sample is a batch average; reported medians
are medians of batch averages, rather than individual lookup latencies.
Seeds reproduce the workload, but scheduling and machine state affect timings.

A reasonably balanced BST has logarithmic height and O(log n) lookup; sorted
insertion can create a chain with O(n) lookup. ListMap searches in O(n).
An unbalanced BST can be slower than a list for some workloads. Review the
actual ranges and limitations in [performance_analysis.md](docs/performance_analysis.md).

Using `--output results/reproduced` preserves the submitted CSV, chart, and
metadata. Running the benchmark without `--output` replaces published files in
`results/`; update the written analysis and evaluation if replacing that snapshot.

## 12. Read or rebuild the documentation

| Document | Purpose |
| --- | --- |
| [README.md](README.md) | Project overview and compact API reference |
| [Architecture](docs/architecture.md) | Class responsibilities, dependencies, and design decisions |
| [Requirements](docs/REQUIREMENTS.md) | Full completion checklist and evidence matrix |
| [Changelog](CHANGELOG.md) | Milestone history and cleanup decisions |
| [Performance analysis](docs/performance_analysis.md) | Measured results, theory, and limitations |
| [Evaluation PDF](docs/evaluation.pdf) | Two-page academic evaluation |
| [Evaluation source](docs/evaluation.md) | Editable Markdown for the evaluation |
| [Expanded report PDF](docs/project_report.pdf) | 18-page APA-style project report |
| [Expanded report Word file](docs/project_report.docx) | Editable report; export a revised PDF after changes |

Open the existing PDF directly; no PDF generation dependency is needed to read it.
To rebuild it from the Markdown source:

```bash
python -m pip install -e ".[docs]"
python scripts/build_evaluation.py
```

The builder writes `docs/evaluation.pdf` and requires exactly two substantive
pages. After changing its source, review the result as well as the page-count
check. To save page images for inspection:

```bash
python scripts/build_evaluation.py --preview-dir dist/evaluation-preview
```

The expanded report is maintained as an editable Word document and a PDF.
Open the Word file to make changes, then export it to PDF. Shared citation and
formatting notes are in [evaluation_sources.md](docs/evaluation_sources.md).

## 13. Build an installable package

From the project root, with the `dev` extra installed:

```bash
python -m build
```

For version 1.0.2, this creates an installable wheel named
`dist/treemap-1.0.2-py3-none-any.whl` and a source distribution named
`dist/treemap-1.0.2.tar.gz`. The wheel contains the runtime package; the source
distribution includes project documentation and testing materials.

To try the wheel in a separate environment on Windows:

```powershell
python -m venv build/wheel-env
.\build\wheel-env\Scripts\python.exe -m pip install dist/treemap-1.0.2-py3-none-any.whl
.\build\wheel-env\Scripts\python.exe -c "from treemap import TreeMap; m = TreeMap(); m.put(1, 'hello'); print(m.get(1))"
```

The final command prints `hello`. On macOS/Linux, use
`build/wheel-env/bin/python` instead of `.\build\wheel-env\Scripts\python.exe`.
The wheel environment is under `build/`, which the project's `.gitignore` excludes.

After committing the intended project files, create a clean source ZIP and
an optional history bundle using standard Git commands:

```bash
git archive --format=zip --prefix=treemap/ --output=dist/treemap-submission.zip HEAD
git bundle create dist/treemap-history.bundle --all
```

The ZIP excludes untracked environments, caches, and local build output. The
bundle preserves history and tags; restore it with
`git clone dist/treemap-history.bundle restored-treemap`. These commands require
a Git checkout, while library use and package installation also work from an
extracted source archive. Earlier release tags describe historical snapshots;
the current branch includes the cleanup and the latest documentation.

## 14. Troubleshooting

| Problem | What to check or do |
| --- | --- |
| `python` is not found | Try `python3` on macOS/Linux or `py -3` on Windows; check the selected interpreter's version. |
| PowerShell blocks `Activate.ps1` | Use `.\.venv\Scripts\python.exe` directly, as in the Windows setup instructions. |
| `No module named treemap` | Run `python -m pip install -e ".[dev]"` from the directory containing `pyproject.toml`, using the same interpreter that runs the program. |
| `treemap` imports your own script | Name the practice file `try_treemap.py`, rather than `treemap.py`; inspect `treemap.__file__` to confirm the imported location. |
| pytest, Ruff, mypy, or build is missing | Install the `dev` extra and invoke tools through the environment's `python -m ...`. |
| Matplotlib is missing | Install `.[benchmark]` or `.[dev]`, or use `--no-chart` with a fresh output directory. |
| PDF tools are missing | Install `.[docs]` before rebuilding the PDF. |
| `TypeError` during key comparison | Use mutually comparable keys in each Map, such as all integers or all strings. |
| `KeyError` during removal | The key is absent; check `contains_key` or handle the exception. |
| `ValueError` for minimum/maximum | The BST is empty; insert an entry or check `len(tree)` first. |
| `get` returns `None` | Use `contains_key` or a distinct default to distinguish an absent key from a stored `None`. |
| A sorted-input tree is unbalanced | This is expected for an ordinary BST; analysis detects imbalance but does not rebalance it. |
| Benchmark times differ from the report | Compare the workload and environment; fixed seeds do not fix elapsed time. |
| Release validation reports a source/hash mismatch | Check whether measured source or evidence changed; restore the matching snapshot or rerun benchmarks and update their analysis. Do not change hashes merely to hide a mismatch. |

## 15. Suggested first-use checklist

- [ ] Download or clone the project and open its root directory.
- [ ] Create `.venv` and install `.[dev]`.
- [ ] Confirm `import treemap` uses the expected installation.
- [ ] Run `python examples/demo.py`.
- [ ] Save and run the TreeMap example as `try_treemap.py`.
- [ ] Try traversals, balance analysis, and before/after rendering.
- [ ] Run `python -m pytest -v` and the quality checks.
- [ ] Run benchmarks with `--output results/reproduced`.
- [ ] Read the measured performance analysis and evaluation PDF.

Use `git status` to review local practice files and generated artifacts before
making a commit.
