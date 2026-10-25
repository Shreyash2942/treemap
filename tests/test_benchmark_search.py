"""Verify workload equivalence and statistics without asserting machine speed."""

import csv
import gc
import json
import statistics
from dataclasses import replace

import pytest
from benchmarks import benchmark_search as benchmark

from treemap import BinarySearchTree
from treemap.core import height


@pytest.mark.parametrize("size", [1, 50, 100, 500, 1000])
def test_insertion_orders_use_identical_keys_and_documented_heights(size):
    for order in benchmark.ORDERS:
        keys = benchmark.insertion_keys(size, order)
        assert sorted(keys) == list(range(0, 2 * size, 2))
        tree = BinarySearchTree()
        for key in keys:
            tree.insert(key, None)
        assert height(tree.root) == (size - 1 if order == "sorted" else size.bit_length() - 1)


def test_queries_are_seeded_and_misses_cover_both_boundaries_and_interior():
    workloads = benchmark.make_queries(50, 99, 506)
    assert workloads == benchmark.make_queries(50, 99, 506)
    assert workloads != benchmark.make_queries(50, 99, 507)
    assert len(workloads["hit"]) == len(workloads["miss"]) == 99
    assert all(0 <= key <= 98 and key % 2 == 0 for key in workloads["hit"])
    misses = workloads["miss"]
    assert sum(key < 0 for key in misses) == 33
    assert sum(0 < key < 98 for key in misses) == 33
    assert sum(key > 98 for key in misses) == 33
    assert all(key % 2 for key in misses)


@pytest.mark.parametrize(
    "changes",
    [
        {"sizes": ()},
        {"sizes": (0,)},
        {"sizes": (50, 50)},
        {"queries": 0},
        {"repeats": 2},
        {"warmups": 0},
    ],
)
def test_invalid_config_is_rejected(changes):
    with pytest.raises(ValueError):
        replace(benchmark.BenchmarkConfig(), **changes)


def test_validation_does_not_accept_none_for_an_absent_key():
    with pytest.raises(AssertionError, match="missing sentinel"):
        benchmark._validate_queries(lambda key, default: None, [99], {}, object())


@pytest.fixture(scope="module")
def tiny_run():
    config = benchmark.BenchmarkConfig(sizes=(3, 7), queries=12, repeats=3, warmups=1)
    results, samples = benchmark.run_benchmarks(config)
    return config, results, samples


def test_summary_medians_can_be_reconstructed_from_all_raw_samples(tiny_run):
    config, results, samples = tiny_run
    assert len(results) == len(config.sizes) * 2 * 2 * 2
    assert len(samples) == len(results) * config.repeats
    for result in results:
        measured = [
            sample.elapsed_ns / sample.query_count
            for sample in samples
            if (sample.size, sample.insertion_order, sample.search_kind, sample.implementation)
            == (result.size, result.insertion_order, result.search_kind, result.implementation)
        ]
        assert len(measured) == config.repeats
        assert result.median_ns_per_search == statistics.median(measured)
        assert result.min_ns_per_search <= result.median_ns_per_search <= result.max_ns_per_search
        assert result.iqr_ns_per_search >= 0


def test_csv_and_metadata_preserve_the_measured_run(tmp_path, tiny_run):
    config, results, samples = tiny_run
    benchmark.write_outputs(tmp_path, config, results, samples, chart=False)
    with (tmp_path / "performance_results.csv").open(newline="", encoding="utf-8") as stream:
        assert len(list(csv.DictReader(stream))) == len(results)
    with (tmp_path / "benchmark_samples.csv").open(newline="", encoding="utf-8") as stream:
        assert len(list(csv.DictReader(stream))) == len(samples)
    metadata = json.loads((tmp_path / "benchmark_metadata.json").read_text(encoding="utf-8"))
    assert metadata["config"]["seed"] == config.seed
    assert metadata["timer"]["monotonic"]
    assert metadata["chart_generated"] is False
    assert len(metadata["source_sha256"]) == 5


@pytest.mark.parametrize("initially_enabled", [False, True])
def test_gc_state_is_restored_if_measurement_fails(monkeypatch, initially_enabled):
    original = gc.isenabled()

    def fail(*args):
        raise RuntimeError("timer failed")

    monkeypatch.setattr(benchmark, "_time_queries", fail)
    try:
        (gc.enable if initially_enabled else gc.disable)()
        with pytest.raises(RuntimeError, match="timer failed"):
            benchmark.run_benchmarks(benchmark.BenchmarkConfig((3,), 3, 3, 1))
        assert gc.isenabled() is initially_enabled
    finally:
        (gc.enable if original else gc.disable)()


def test_chart_is_a_real_png(tmp_path, tiny_run):
    pytest.importorskip("matplotlib")
    config, results, _ = tiny_run
    path = tmp_path / "chart.png"
    benchmark.plot_results(results, path, config)
    assert path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
