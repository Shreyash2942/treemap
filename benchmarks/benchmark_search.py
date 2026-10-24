"""Measure equivalent TreeMap/ListMap lookups; construction is outside timing."""

from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import importlib.util
import json
import os
import platform
import random
import statistics
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from bst_map import ListMap, TreeMap
from bst_map.core import height

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORDERS = ("balanced_like", "sorted")
IMPLEMENTATIONS = ("TreeMap", "ListMap")


@dataclass(frozen=True)
class BenchmarkConfig:
    sizes: tuple[int, ...] = (50, 100, 500, 1000)
    queries: int = 4000
    repeats: int = 9
    warmups: int = 2
    seed: int = 506

    def __post_init__(self) -> None:
        if not self.sizes or any(size < 1 for size in self.sizes):
            raise ValueError("sizes must contain positive integers")
        if len(set(self.sizes)) != len(self.sizes):
            raise ValueError("sizes must be unique")
        if self.queries < 3:
            raise ValueError("queries must be at least 3")
        if self.repeats < 3:
            raise ValueError("repeats must be at least 3")
        if self.warmups < 1:
            raise ValueError("warmups must be at least 1")


@dataclass(frozen=True)
class SearchResult:
    size: int
    insertion_order: str
    tree_height: int
    search_kind: str
    implementation: str
    queries_per_sample: int
    repeats: int
    warmups: int
    median_ns_per_search: float
    min_ns_per_search: float
    max_ns_per_search: float
    iqr_ns_per_search: float


@dataclass(frozen=True)
class SearchSample:
    size: int
    insertion_order: str
    search_kind: str
    implementation: str
    repeat: int
    query_count: int
    elapsed_ns: int


def insertion_keys(size: int, order: str) -> list[int]:
    """Return even keys, sorted or median-first for a reproducibly balanced BST."""
    if size < 1:
        raise ValueError("size must be positive")
    keys = list(range(0, 2 * size, 2))
    if order == "sorted":
        return keys
    if order != "balanced_like":
        raise ValueError(f"unknown insertion order: {order}")
    result = []
    stack = [(0, size)]
    while stack:
        start, stop = stack.pop()
        if start >= stop:
            continue
        middle = (start + stop) // 2
        result.append(keys[middle])
        stack.append((middle + 1, stop))
        stack.append((start, middle))
    return result


def make_queries(size: int, count: int, seed: int) -> dict[str, tuple[int, ...]]:
    """Sample uniform hits and shuffled misses below/between/above even keys.

    Miss categories are as equal as possible. For size 1 there is no interior
    gap, so its middle category is also above the sole stored key.
    """
    if size < 1 or count < 3:
        raise ValueError("size must be positive and count must be at least 3")
    rng = random.Random(seed + size)
    hits = tuple(2 * rng.randrange(size) for _ in range(count))
    misses = []
    for index in range(count):
        if index % 3 == 0:
            key = -2 * rng.randrange(1, size + 1) + 1
        elif index % 3 == 1:
            key = 2 * rng.randrange(max(1, size - 1)) + 1
        else:
            key = 2 * size + 2 * rng.randrange(size) + 1
        misses.append(key)
    rng.shuffle(misses)
    return {"hit": hits, "miss": tuple(misses)}


def _validate_queries(lookup, queries, expected, missing) -> None:
    """Check values and missing-default identity before any timed calls."""
    for key in queries:
        actual = lookup(key, missing)
        wanted = expected.get(key, missing)
        if wanted is missing:
            if actual is not missing:
                raise AssertionError("lookup did not return the missing sentinel")
        elif actual != wanted:
            raise AssertionError(f"incorrect lookup value for key {key}")


def _time_queries(lookup, queries, missing) -> int:
    start = time.perf_counter_ns()
    for key in queries:
        lookup(key, missing)
    return time.perf_counter_ns() - start


def run_benchmarks(
    config: BenchmarkConfig, progress: Callable[[str], None] | None = None
) -> tuple[list[SearchResult], list[SearchSample]]:
    """Return median batch means and raw timings; do not time map construction."""
    results: list[SearchResult] = []
    samples: list[SearchSample] = []
    rng = random.Random(config.seed)
    missing = object()
    for size in config.sizes:
        workloads = make_queries(size, config.queries, config.seed)
        for order in ORDERS:
            keys = insertion_keys(size, order)
            expected = {key: None if key % 10 == 0 else key for key in keys}
            tree = TreeMap[int, int | None]()
            listing = ListMap[int, int | None]()
            for key, value in expected.items():
                tree.put(key, value)
                listing.put(key, value)
            tree_height = height(tree._tree.root)
            lookups = {"TreeMap": tree.get, "ListMap": listing.get}
            for kind, queries in workloads.items():
                for lookup in lookups.values():
                    _validate_queries(lookup, queries, expected, missing)
                timings: dict[str, list[float]] = {name: [] for name in IMPLEMENTATIONS}
                gc_was_enabled = gc.isenabled()
                gc.disable()
                try:
                    for _ in range(config.warmups):
                        for lookup in lookups.values():
                            _time_queries(lookup, queries, missing)
                    for repeat in range(1, config.repeats + 1):
                        names = list(IMPLEMENTATIONS)
                        rng.shuffle(names)
                        for name in names:
                            elapsed = _time_queries(lookups[name], queries, missing)
                            timings[name].append(elapsed / len(queries))
                            samples.append(
                                SearchSample(size, order, kind, name, repeat, len(queries), elapsed)
                            )
                finally:
                    if gc_was_enabled:
                        gc.enable()
                for name in IMPLEMENTATIONS:
                    measured = timings[name]
                    quartiles = statistics.quantiles(measured, n=4, method="inclusive")
                    results.append(
                        SearchResult(
                            size,
                            order,
                            tree_height,
                            kind,
                            name,
                            config.queries,
                            config.repeats,
                            config.warmups,
                            statistics.median(measured),
                            min(measured),
                            max(measured),
                            quartiles[2] - quartiles[0],
                        )
                    )
            if progress is not None:
                progress(f"Completed n={size}, order={order}, tree height={tree_height}")
    return results, samples


def _write_csv(path: Path, rows: Sequence[SearchResult] | Sequence[SearchSample]) -> None:
    dictionaries = [asdict(row) for row in rows]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(dictionaries[0]))
        writer.writeheader()
        writer.writerows(dictionaries)


def plot_results(results: Sequence[SearchResult], path: Path, config: BenchmarkConfig) -> None:
    """Create a headless Matplotlib PNG from measured medians and sample ranges."""
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    figure = Figure(figsize=(12, 8), layout="constrained")
    FigureCanvasAgg(figure)
    axes = figure.subplots(2, 2, sharex=True, sharey=True)
    for row, kind in enumerate(("hit", "miss")):
        for column, order in enumerate(ORDERS):
            axis = axes[row, column]
            for name, color in zip(IMPLEMENTATIONS, ("tab:blue", "tab:orange"), strict=True):
                selected = sorted(
                    (
                        r
                        for r in results
                        if r.search_kind == kind
                        and r.insertion_order == order
                        and r.implementation == name
                    ),
                    key=lambda result: result.size,
                )
                sizes = [r.size for r in selected]
                axis.plot(
                    sizes,
                    [r.median_ns_per_search / 1000 for r in selected],
                    marker="o",
                    label=name,
                    color=color,
                )
                axis.fill_between(
                    sizes,
                    [r.min_ns_per_search / 1000 for r in selected],
                    [r.max_ns_per_search / 1000 for r in selected],
                    color=color,
                    alpha=0.14,
                )
            axis.set_title(f"{'Median-first' if order == 'balanced_like' else 'Sorted'} insertion")
            axis.set_yscale("log")
            axis.grid(True, which="both", alpha=0.2)
            axis.set_xticks(sorted(config.sizes))
            if column == 0:
                axis.set_ylabel(
                    f"{'Successful' if kind == 'hit' else 'Unsuccessful'} search\n"
                    "Microseconds per lookup (log scale)"
                )
            axis.legend()
    figure.suptitle("TreeMap and sequential ListMap: measured search time")
    figure.supxlabel(
        f"Items | {config.queries:,} queries/sample, {config.repeats} repeats, "
        f"{config.warmups} warmups, seed {config.seed}\n"
        "Points: median batch means; shading: minimum to maximum batch means"
    )
    figure.savefig(path, dpi=180)


def write_outputs(
    output: Path,
    config: BenchmarkConfig,
    results: list[SearchResult],
    samples: list[SearchSample],
    *,
    chart: bool = True,
) -> None:
    """Write summary/raw CSV, environment metadata, and optionally a PNG chart."""
    output.mkdir(parents=True, exist_ok=True)
    summary_path = output / "performance_results.csv"
    samples_path = output / "benchmark_samples.csv"
    _write_csv(summary_path, results)
    _write_csv(samples_path, samples)
    if chart:
        plot_results(results, output / "benchmark_chart.png", config)
    timer = time.get_clock_info("perf_counter")
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    sources = [
        "benchmarks/benchmark_search.py",
        "src/bst_map/core/node.py",
        "src/bst_map/core/bst.py",
        "src/bst_map/maps/tree_map.py",
        "src/bst_map/maps/list_map.py",
    ]
    metadata = {
        "measured_at_utc": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "logical_cpus": os.cpu_count(),
        "config": asdict(config),
        "git_revision": revision.stdout.strip() if revision.returncode == 0 else None,
        "source_sha256": {
            p: hashlib.sha256((PROJECT_ROOT / p).read_bytes()).hexdigest() for p in sources
        },
        "artifact_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (summary_path, samples_path)
        },
        "timer": {
            "implementation": timer.implementation,
            "resolution_seconds": timer.resolution,
            "monotonic": timer.monotonic,
        },
        "method": "Median of repeated batch elapsed times divided by query count; ns/search.",
        "gc": "Disabled during warmups/measurement, restored to its prior state afterward.",
        "measurement_order": "Map order shuffled independently each repeat with a fixed seed.",
        "misses": "Approximately equal below-minimum, interior-gap, and above-maximum keys.",
        "chart_generated": chart,
    }
    (output / "benchmark_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[50, 100, 500, 1000])
    parser.add_argument("--queries", type=int, default=4000)
    parser.add_argument("--repeats", type=int, default=9)
    parser.add_argument("--warmups", type=int, default=2)
    parser.add_argument("--seed", type=int, default=506)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "results")
    parser.add_argument("--no-chart", action="store_true")
    args = parser.parse_args(argv)
    try:
        config = BenchmarkConfig(
            tuple(args.sizes), args.queries, args.repeats, args.warmups, args.seed
        )
    except ValueError as error:
        parser.error(str(error))
    if not args.no_chart and importlib.util.find_spec("matplotlib") is None:
        parser.error('Install ".[benchmark]" or use --no-chart.')
    results, samples = run_benchmarks(config, progress=print)
    write_outputs(args.output, config, results, samples, chart=not args.no_chart)
    print(f"Wrote {len(results)} summary rows and {len(samples)} raw samples to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
