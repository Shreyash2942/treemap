"""Release evidence must remain readable, reproducible, and internally consistent."""

import csv
import hashlib
import json
import re
import shutil
import tomllib
from pathlib import Path

import pytest
from packaging.requirements import Requirement
from pypdf import PdfWriter
from scripts.validate_release import validate_benchmarks, validate_evaluation, validate_local_links

ROOT = Path(__file__).resolve().parents[1]


def test_evaluation_has_two_substantial_pages_and_required_sections():
    assert validate_evaluation(ROOT / "docs/evaluation.pdf")["pages"] == 2


def test_one_page_pdf_is_rejected(tmp_path):
    path = tmp_path / "one.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.write(path)
    with pytest.raises(ValueError, match="exactly two pages"):
        validate_evaluation(path)


def test_committed_benchmark_statistics_and_hashes_are_consistent():
    report = validate_benchmarks(ROOT)
    assert report["summary_cases"] == 32
    assert report["raw_samples"] == 288


def test_changed_median_is_detected_even_if_its_csv_hash_is_updated(tmp_path):
    metadata = json.loads((ROOT / "results/benchmark_metadata.json").read_text(encoding="utf-8"))
    for filename in [
        *metadata["source_sha256"],
        *(f"results/{name}" for name in metadata["artifact_sha256"]),
        "results/benchmark_chart.png",
    ]:
        target = tmp_path / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / filename, target)
    summary = tmp_path / "results/performance_results.csv"
    with summary.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    rows[0]["median_ns_per_search"] = str(float(rows[0]["median_ns_per_search"]) + 100)
    with summary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    metadata["artifact_sha256"][summary.name] = hashlib.sha256(summary.read_bytes()).hexdigest()
    (tmp_path / "results/benchmark_metadata.json").write_text(
        json.dumps(metadata), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="Summary statistic mismatch"):
        validate_benchmarks(tmp_path)


def test_documentation_local_links_resolve():
    assert validate_local_links(ROOT) > 20


def test_broken_documentation_link_is_detected(tmp_path):
    (tmp_path / "README.md").write_text("[missing](docs/missing.md)", encoding="utf-8")
    with pytest.raises(ValueError, match="Broken local link"):
        validate_local_links(tmp_path)


def test_readme_python_examples_execute(capsys):
    namespace = {"__name__": "readme_example"}
    source = (ROOT / "README.md").read_text(encoding="utf-8")
    snippets = re.findall(r"```python\n(.*?)```", source, re.S)
    assert len(snippets) >= 4
    for snippet in snippets:
        exec(compile(snippet, "README.md", "exec"), namespace)


def test_dev_extra_supports_the_complete_documented_validation_workflow():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    packages = {
        Requirement(value).name for value in config["project"]["optional-dependencies"]["dev"]
    }
    assert {"pytest", "ruff", "mypy", "build", "matplotlib", "pypdf"} <= packages
