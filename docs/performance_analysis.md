# Performance analysis and release evidence

Measured on 2026-10-25. These are executed results, not projected timings.

## Method and reproducibility

Run from the installed repository:

```powershell
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe benchmarks/benchmark_search.py
```

For CSV and metadata only, add `--no-chart`. Install the package from this repository; the optional plotting extra supplies Matplotlib. `results/benchmark_environment.txt` records the installed versions used for this run.

The experiment uses sizes 50, 100, 500, and 1,000, seed 506, 4,000 queries per batch, two warm-up batches, and nine measured batches per case. There are 32 cases (four sizes × two insertion orders × hit/miss × two maps), producing 288 raw samples and 1,152,000 timed lookups.

For each size, both maps receive identical even-integer keys and values in the same insertion order. Twenty percent of entries store `None`. Median-first insertion deliberately creates a balanced BST; sorted insertion creates a right chain. ListMap retains either insertion order internally. Hit queries sample keys uniformly with replacement. Miss queries are shuffled and split approximately equally among below-minimum, interior odd-number gaps, and above-maximum keys. The same query tuples are reused for both maps and both insertion orders at a given size.

Before timing, every query result is checked against a dictionary. Misses must return the exact supplied default sentinel, while stored `None` remains a legitimate value. Construction, query generation, correctness checks, tree-height calculation, file output, and plotting are outside timing.

Timing uses prebound public `get(key, default)` calls in a Python loop with `perf_counter_ns`. The loop and API call costs are included; no baseline is subtracted. Garbage collection is disabled during warm-up and measurement and then restored to its prior state. The order of the two map measurements is shuffled for each repetition with a seeded RNG. The full benchmark ran without concurrent test or plotting jobs; chart generation followed timing.

For each batch, elapsed nanoseconds are divided by 4,000. The reported statistic is the median of those nine batch means, not the median or a percentile of individual lookup latencies. The CSV also records minimum, maximum, and interquartile range (inclusive quartiles).

Environment:

| Property | Recorded value |
| --- | --- |
| Interpreter | CPython 3.14.4 |
| Platform | Windows-11-10.0.26300-SP0 |
| Processor identifier | AMD64 Family 26 Model 36 Stepping 0, AuthenticAMD |
| Logical processors | 24 |
| Clock | QueryPerformanceCounter(); resolution 1e-07 s |
| Benchmark/source revision | `b0a20d4926824ff5b18b2ed720dff4f5c0ca5b07` (package-alignment commit) |

The metadata contains the configuration, timestamp, raw-byte SHA-256 hashes of the benchmark/map source files, and hashes of both CSV artifacts. Those hashes identify the measured files; source hashes can change if line endings are rewritten. `.gitattributes` preserves CSV bytes across Git checkout. Subsequent documentation and packaging commits add evidence without changing the measured lookup implementation.

## Measured results

All times below are microseconds per lookup, converted from the unrounded nanosecond CSV. Height counts edges.

| Items | Insertion order | BST height | TreeMap hit | ListMap hit | TreeMap miss | ListMap miss |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 50 | Median-first | 5 | 0.173 | 0.379 | 0.193 | 0.673 |
| 100 | Median-first | 6 | 0.195 | 0.672 | 0.237 | 1.279 |
| 500 | Median-first | 8 | 0.263 | 3.639 | 0.287 | 7.431 |
| 1,000 | Median-first | 9 | 0.313 | 7.321 | 0.332 | 20.466 |
| 50 | Sorted | 49 | 0.584 | 0.353 | 0.611 | 0.650 |
| 100 | Sorted | 99 | 1.143 | 0.655 | 1.156 | 1.258 |
| 500 | Sorted | 499 | 5.465 | 3.418 | 5.489 | 6.488 |
| 1,000 | Sorted | 999 | 17.305 | 8.531 | 15.145 | 17.839 |

![Search-time medians and observed batch ranges](../results/benchmark_chart.png)

The chart uses a logarithmic time axis. Points show median batch means; shaded bands span minimum to maximum observed batch means, not confidence intervals.

## Findings and interpretation

At 1,000 entries with median-first insertion, TreeMap took 0.313 microseconds for hits versus ListMap's 7.321, a ratio of 23.42 between ListMap and TreeMap times. For misses the ratio was 61.70. The controlled tree height was only 9.

With sorted insertion, height reached 999. Successful TreeMap searches took 17.305 microseconds versus 8.531 for ListMap, so ListMap was about 2.03 times faster for hits. Successful TreeMap lookups were 55.35 times slower than with median-first insertion. Sorted TreeMap still beat ListMap on the mixed miss workload by about 1.18 times; a key below the root fails immediately in that chain, so not every miss traverses its full height.

Across all tested sizes, median-first TreeMap won hits and misses. ListMap won hits against the sorted chain, including at 50 entries. This run did not identify a size where ListMap beats the deliberately balanced tree. Small-dataset constant factors can make a list competitive, but no universal crossover point is supported by these four sizes.

The code explains the shape effect: BST search visits at most one node per tree level, so its cost is O(h). Reasonably balanced shapes have logarithmic height and O(log n) search. With uniformly random insertion of distinct keys, expected lookup path length is logarithmic; random insertion was tested for correctness but was not timed in this experiment. Sorted insertion gives h = n - 1 and worst-case O(n) search. ListMap scans sequentially: a failed lookup checks all n entries, and a uniformly sampled successful lookup averages approximately (n + 1)/2 equality checks. Its search is O(n). These finite measurements are consistent with the analysis; they do not prove asymptotic bounds.

## Variability and limits

Observed range at 1,000 entries (µs per search in each batch):

| Order | Search | Map | Minimum | Median | Maximum | IQR |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Median-first | hit | TreeMap | 0.294 | 0.313 | 0.321 | 0.007 |
| Median-first | hit | ListMap | 7.234 | 7.321 | 7.458 | 0.155 |
| Median-first | miss | TreeMap | 0.304 | 0.332 | 0.792 | 0.417 |
| Median-first | miss | ListMap | 14.839 | 20.466 | 31.450 | 9.053 |
| Sorted | hit | TreeMap | 10.785 | 17.305 | 22.320 | 5.065 |
| Sorted | hit | ListMap | 6.876 | 8.531 | 14.245 | 2.460 |
| Sorted | miss | TreeMap | 10.988 | 15.145 | 26.253 | 6.612 |
| Sorted | miss | ListMap | 13.769 | 17.839 | 21.032 | 3.652 |

The 1,000-item cases show substantial batch-to-batch variation in this run, particularly for misses and sorted trees; the reported ratios should be interpreted alongside those ranges.

These are repeated batches in one process on one Windows machine and Python version. They do not represent independent machines or process-level replications. OS scheduling, CPU frequency/power state, cache behavior, Python specialization, and background activity can change timings; CPU affinity and power settings were not controlled. Warmups, medians, shuffled measurement order, and recorded ranges reduce or reveal some variation but do not eliminate it.

Only integer keys and these hit/miss distributions were timed. String comparisons, expensive user-defined keys, other insertion orders, updates, deletion, construction time, memory usage, and other runtimes could yield different trade-offs. Uniform hits do not model every real application. The median-first case is intentionally favorable, not a claim that an ordinary BST will maintain that shape under future changes. The tree performs no automatic balancing. Nanosecond units describe the clock and arithmetic; they do not imply nanosecond measurement accuracy.

Seeds reproduce data and execution order, not identical elapsed time. The raw samples, ranges, and environment should accompany any comparison. Broader claims would require repeated processes, more machines, more key types/workloads, and a balancing implementation as another comparator.

## Reproducible deletion diagrams

Starting insertion order: `50, 30, 70, 20, 40, 60, 80`. The actual ASCII renderer generated this before deletion:

```text
50
|-- L: 30
|   |-- L: 20
|   `-- R: 40
`-- R: 70
    |-- L: 60
    `-- R: 80
```

After deleting 30, its in-order successor 40 replaces it and retains left child 20. Root 50 and its right subtree are unchanged; the tree contains six keys:

```text
50
|-- L: 40
|   `-- L: 20
`-- R: 70
    |-- L: 60
    `-- R: 80
```

Golden-file tests compare these saved diagrams against fresh renderer output and verify BST bounds after deletion. Both outputs come from the implementation, not hand-drawn illustrations.

## Validation and retained evidence

- The complete regression suite passes on CPython 3.14.4; the final count and outcomes are recorded in [JUnit XML](../results/pytest_results.xml) and the release validation report.
- Six fresh named fixtures cover 50 random integers, sorted integers, reverse-sorted integers, strings, heterogeneous values, and 50 replacement operations after preloading 50 keys.
- Unit, map integration, repeated deletion/reuse, strict bounds/size, deep-tree, and dictionary-reference checks cover the system. Benchmark tests check shapes, workload equivalence, result validation, raw-sample medians, GC restoration, output files, and PNG generation without asserting a speed threshold.
- Ruff lint, formatting, dependency checks, and the extended demo passed. Python 3.11 remains the syntax target; runtime tests were executed on the locally available Python 3.14.4.

Artifacts:

- [32 summary cases](../results/performance_results.csv)
- [288 raw measured batches](../results/benchmark_samples.csv)
- [Environment, configuration, Git revision, and SHA-256 hashes](../results/benchmark_metadata.json)
- [Installed environment versions](../results/benchmark_environment.txt)
- [PNG chart](../results/benchmark_chart.png)
- [Before](diagrams/tree_before.txt) and [after](diagrams/tree_after.txt) diagram files

The completed [two-page evaluation](evaluation.pdf) uses these final measurements; its [editable source](evaluation.md) and [source notes](evaluation_sources.md) are included.
