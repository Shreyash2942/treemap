# Final submission guide

Release: **bstkit 1.0.0**, lightweight tag **v1.0.0**, **23 milestone commits**.

## Review order

1. [README](../README.md): objectives, requirements, installation, API, and reproduction.
2. [Architecture](architecture.md): responsibilities, dependencies, contracts, and decisions.
3. [Performance analysis](performance_analysis.md): executed results, theory, uncertainty, and limits.
4. [Evaluation PDF](evaluation.pdf), [editable source](evaluation.md), and [citation notes](evaluation_sources.md).
5. [Requirements matrix](requirements.md), [final validation](../results/final_validation.json), and [213-test JUnit evidence](../results/pytest_results.xml).

The evaluation is exactly two pages including references. It uses third-person
academic prose, author/date citations, hanging references, 12-point Times,
double spacing, one-inch margins, and page numbers. No separate title page or
unsupplied student details were invented.

## Reproduce validation

After creating and activating a virtual environment:

```bash
python -m pip install -e ".[dev]"
python -m pytest -v
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m pip check
python examples/demo.py
python scripts/validate_release.py
git log --oneline
git status
```

On PowerShell without activation, substitute `.venv\Scripts\python.exe` for
`python`. Preserve the published measurements when reproducing timings:

```bash
python benchmarks/benchmark_search.py --output results/reproduced
```

Seeds reproduce workloads, not elapsed times. The default benchmark command
replaces published CSV/PNG/metadata; preserve that snapshot or update the written
findings when publishing replacement measurements.

Rebuild the PDF with `python -m pip install -e ".[docs]"` followed by
`python scripts/build_evaluation.py`. From the clean release tag, prepare artifacts:

```bash
python -m build
python scripts/build_submission.py --tag v1.0.0
```

## Generated files in dist/

- `bstkit-v1.0.0.zip`: all committed source, tests, documentation, PDF, and evidence.
- `bstkit-v1.0.0.bundle`: Git history and refs, including the release tag.
- `bstkit-1.0.0-py3-none-any.whl`: installable typed runtime library.
- `bstkit-1.0.0.tar.gz`: source distribution with documentation and evidence.
- `release_manifest.json` and `SHA256SUMS`: revision and artifact-integrity information.
- `clean_install_validation.json`: isolated wheel-install verification, when generated.

The ZIP excludes `.git`, environments, and caches. Recover history separately
with `git clone bstkit-v1.0.0.bundle treemap`. Use the ZIP or source distribution
for coursework materials; the wheel contains the runtime package.

Verification uses CPython 3.14.4, with a Python 3.11 syntax/type-check target.
The library has no runtime dependencies and does not rebalance automatically.
