# Changelog

## Unreleased - Project cleanup

- Removed the standalone implementation plan and submission guide at the user's request.
- Retired the historical knowledge graph, generated extraction caches, and empty results placeholder.
- Retained the expanded report as PDF and editable Word; removed its duplicate Markdown, standalone image copies, and custom generator.
- Removed the custom submission builder and its obsolete documentation; standard Python/Git commands handle packaging.
- Kept the two-page evaluation builder and evidence validator, which support required deliverables and tests.
- Removed the report-only `python-docx` dependency and consolidated citation notes.
- Moved ignored old archives, previews, caches, and build output to an external recovery backup.
- Reviewed the runtime and test modules; their public algorithms and edge-case checks implement the required scope.

The original development history remains available:

| Milestone | Planned commits | Completion evidence |
| --- | ---: | --- |
| Day 1: BST foundation | 6 | Nodes, mutation, extrema, and strict invariants |
| Day 2: Traversals and TreeMap | 6 | Traversals, all-subtree balance, and Map integration |
| Day 3: Testing and performance | 6 | Diverse datasets, diagrams, ListMap, and measured benchmarks |
| Day 4: Documentation and release | 5 | Evaluation, quality checks, and packaged deliverables |

The 23 milestone commits and original release tags are preserved. Subsequent
commits record naming corrections, the user guide, academic report, and cleanup.

## 1.0.2 - October 25, 2026

- Aligned the installed import package and source directory with `treemap`.
- Added the full completion requirements, checked deliverables, and evidence matrix in `docs/REQUIREMENTS.md`.
- Updated imports, examples, type-check configuration, graph paths, and release validation.
- Repeated the benchmarks after the package rename and refreshed the analysis and evaluation.
- Verified the submission from an isolated wheel installation and synchronized GitHub commits and release tags.

## 1.0.1 — October 25, 2026

- Standardized the project title as Treemap and the distribution name as `treemap`.
- Corrected documentation, knowledge-graph labels, and generated release filenames.
- Derived archive names and the default release tag from package metadata.
- Retained the prescribed Python imports and the original benchmark measurements.
- Preserved the 23 milestone commits and original release tag; added a naming correction release.

## 1.0.0 — October 25, 2026

- Completed generic iterative BST operations, traversals, and whole-tree balance analysis.
- Completed TreeMap, sequential ListMap, ASCII diagrams, and recorded search benchmarks.
- Added an exactly two-page evaluation, editable source, and verified academic references.
- Passed 213 automated tests, strict mypy, Ruff lint/format, and dependency checks.
- Added typed-package metadata, PDF generation, and release-evidence validation.
- Prepared source/package archives, Git history, and SHA-256 submission checksums.

The BST remains unbalanced by design. Historical analysis artifacts remain
recoverable through Git history and are omitted from the current submission.
