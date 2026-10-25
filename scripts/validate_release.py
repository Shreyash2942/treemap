"""Verify submitted documentation, PDF, benchmark evidence, and regression results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import re
import statistics
import tomllib
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_evaluation(path: Path) -> dict:
    reader = PdfReader(path)
    require(len(reader.pages) == 2, "Evaluation must contain exactly two pages")
    texts = [page.extract_text() for page in reader.pages]
    require(all(len(text.strip()) >= 700 for text in texts), "Evaluation pages must be substantive")
    text = " ".join(" ".join(texts).split())
    for heading in (
        "Introduction",
        "BST Operations",
        "Practical Benefits",
        "Limitations",
        "Performance Comparison",
        "Real-World Applications",
        "Conclusion",
        "References",
    ):
        require(heading in text, f"Missing evaluation section: {heading}")
    for author in (
        "Sedgewick",
        "Wayne",
        "Python Software Foundation",
        "PostgreSQL Global Development Group",
    ):
        require(author in text, f"Missing evaluation citation/reference: {author}")
    for page in reader.pages:
        require(
            tuple(float(x) for x in page.mediabox[2:]) == (612.0, 792.0), "Expected US Letter pages"
        )
    return {"pages": 2, "words_per_page": [len(text.split()) for text in texts]}


def validate_benchmarks(root: Path) -> dict:
    output = root / "results"
    metadata = json.loads((output / "benchmark_metadata.json").read_text(encoding="utf-8"))
    for filename, expected in metadata["source_sha256"].items():
        require(
            hashlib.sha256((root / filename).read_bytes()).hexdigest() == expected,
            f"Measured source hash mismatch: {filename}",
        )
    for filename, expected in metadata["artifact_sha256"].items():
        require(
            hashlib.sha256((output / filename).read_bytes()).hexdigest() == expected,
            f"Benchmark artifact hash mismatch: {filename}",
        )
    with (output / "performance_results.csv").open(newline="", encoding="utf-8") as stream:
        results = list(csv.DictReader(stream))
    with (output / "benchmark_samples.csv").open(newline="", encoding="utf-8") as stream:
        raw = list(csv.DictReader(stream))
    config = metadata["config"]
    require(set(config["sizes"]) == {50, 100, 500, 1000}, "Expected all four benchmark sizes")
    expected_keys = {
        (str(size), order, kind, name)
        for size in config["sizes"]
        for order in ("balanced_like", "sorted")
        for kind in ("hit", "miss")
        for name in ("TreeMap", "ListMap")
    }
    fields = ("size", "insertion_order", "search_kind", "implementation")
    grouped = defaultdict(list)
    for row in raw:
        require(int(row["query_count"]) == config["queries"], "Raw query count mismatch")
        grouped[tuple(row[field] for field in fields)].append(
            int(row["elapsed_ns"]) / int(row["query_count"])
        )
    require(len(results) == len(expected_keys), "Unexpected number of benchmark summary cells")
    require(
        {tuple(row[f] for f in fields) for row in results} == expected_keys,
        "Missing or duplicated benchmark cases",
    )
    require(set(grouped) == expected_keys, "Raw benchmark cases do not match summary")
    for row in results:
        measured = grouped[tuple(row[field] for field in fields)]
        require(len(measured) == config["repeats"], "Raw repetition count mismatch")
        quartiles = statistics.quantiles(measured, n=4, method="inclusive")
        expected = {
            "median_ns_per_search": statistics.median(measured),
            "min_ns_per_search": min(measured),
            "max_ns_per_search": max(measured),
            "iqr_ns_per_search": quartiles[2] - quartiles[0],
        }
        for field, number in expected.items():
            require(
                math.isclose(float(row[field]), number, rel_tol=1e-12, abs_tol=1e-9),
                f"Summary statistic mismatch: {field}",
            )
    require(
        (output / "benchmark_chart.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"),
        "Benchmark chart is not a PNG",
    )
    return {
        "summary_cases": len(results),
        "raw_samples": len(raw),
        "source_revision": metadata["git_revision"],
        "hashes_verified": True,
        "all_statistics_reconstructed": True,
    }


def validate_local_links(root: Path) -> int:
    checked = 0
    for document in [root / "README.md", *sorted((root / "docs").rglob("*.md"))]:
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            target = target.strip("<>")
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            resolved = (document.parent / unquote(target.split("#", 1)[0])).resolve()
            require(resolved.is_relative_to(root.resolve()), f"Link escapes project: {target}")
            require(resolved.exists(), f"Broken local link in {document.name}: {target}")
            checked += 1
    return checked


def validate_release(root: Path) -> dict:
    root = root.resolve()
    required = [
        "README.md",
        "pyproject.toml",
        "src/bst_map/py.typed",
        "docs/architecture.md",
        "docs/performance_analysis.md",
        "docs/requirements.md",
        "docs/evaluation.md",
        "docs/evaluation.pdf",
        "docs/evaluation_sources.md",
        "docs/diagrams/tree_before.txt",
        "docs/diagrams/tree_after.txt",
        "benchmarks/benchmark_search.py",
        "examples/demo.py",
        "results/pytest_results.xml",
    ]
    for filename in required:
        require((root / filename).is_file(), f"Missing required deliverable: {filename}")
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    require(project["name"] == "treemap", "Expected project distribution name treemap")
    require(
        re.fullmatch(r"\d+\.\d+\.\d+", project["version"]) is not None, "Expected release version"
    )
    require(project["dependencies"] == [], "Runtime library should remain dependency-free")
    suites = list(
        ElementTree.parse(root / "results/pytest_results.xml").getroot().iter("testsuite")
    )
    count = sum(int(suite.attrib["tests"]) for suite in suites)
    require(count >= 204, "Full regression evidence is missing")
    require(
        all(
            int(suite.attrib[field]) == 0
            for suite in suites
            for field in ("failures", "errors", "skipped")
        ),
        "Regression report is not fully passing",
    )
    return {
        "validated_at_utc": datetime.now(UTC).isoformat(),
        "passed": True,
        "name": project["name"],
        "version": project["version"],
        "validation_python": platform.python_version(),
        "evaluation": validate_evaluation(root / "docs/evaluation.pdf"),
        "benchmarks": validate_benchmarks(root),
        "local_links_checked": validate_local_links(root),
        "required_files_checked": len(required),
        "regression_tests": count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "results/final_validation.json")
    args = parser.parse_args()
    report = validate_release(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"Release checks passed: {report['regression_tests']} tests, two-page PDF, "
        f"32 benchmark cases, 288 samples, {report['local_links_checked']} local links."
    )


if __name__ == "__main__":
    main()
