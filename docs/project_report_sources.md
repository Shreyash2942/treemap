# Expanded report: sources, evidence, and reproduction

The expanded report supplements the required two-page evaluation. It provides
an APA 7-style PDF, editable Word document, and Markdown source. The title page
and document metadata omit the author name, as requested. No student name,
instructor name, affiliation, or due date was invented. Add the institution's
required title-page details in Word before submission if needed.

## Files

- [PDF report](project_report.pdf)
- [Editable Word report](project_report.docx)
- [Markdown source](project_report.md)
- [Diagram source image](diagrams/report_tree_changes.png)
- [Report search comparison](diagrams/report_search_comparison.png)
- [Build script](../scripts/build_project_report.py)

The PDF builder enforces more than six main-body pages, excluding the title
page, abstract, references, and appendices. It also checks that all 75 numbered
requirements, deliverables, and success criteria appear in the PDF. The report
uses 12-point Times New Roman when installed, double-spaced body text, one-inch
margins, a half-inch first-line indent, top-right page numbers, and hanging
references. Table bodies use compact 10-point text, with repeated header rows
and horizontal rules. The Word document uses corresponding editable styles;
pagination may vary with Word's font and layout environment.

## Verified external sources

Primary sources were checked on October 25, 2026:

- APA's [Student Paper Setup Guide](https://apastyle.apa.org/instructional-aids/student-paper-setup-guide.pdf)
  supplies the formatting conventions. The requested omission of the author
  and other unsupplied identifying details is a deliberate title-page adaptation.
- Sedgewick and Wayne's [BST chapter](https://algs4.cs.princeton.edu/32bst/)
  supports the brief theoretical background and height-dependent search analysis.
  Direct retrieval was blocked by the host, but the search index supplied the
  chapter text. The [publisher's record](https://www.pearson.com/en-gb/subject-catalog/p/algorithms/P200000000597)
  verifies the 2011 fourth edition and Addison-Wesley Professional attribution.
- The Python Software Foundation's [versioned sys documentation](https://docs.python.org/3.14/library/sys.html#sys.getrecursionlimit)
  supports the interpreter recursion-limit discussion. Its reference uses `n.d.`.
- The PostgreSQL Global Development Group's [version 18 B-tree documentation](https://www.postgresql.org/docs/18/btree.html)
  supports the production-index comparison. The report distinguishes its
  balanced, multiway B-tree from the project's ordinary BST; the reference uses `n.d.`.
- The versioned [TreeMap repository](https://github.com/Shreyash2942/treemap/tree/v1.0.2)
  is cited as software with no named author in the reference entry.

Theoretical background is paraphrased. There are no direct quotations. Project
algorithms, API behavior, tests, and performance findings are assessed from the
local source and retained artifacts, rather than attributed to external authors.

## Project evidence

The report uses [the full requirements](REQUIREMENTS.md),
[architecture](architecture.md), [performance analysis](performance_analysis.md),
[recorded regression results](../results/pytest_results.xml),
[release validation](../results/final_validation.json), and
[benchmark metadata](../results/benchmark_metadata.json).

The numerical table is a three-decimal microsecond conversion of
`results/performance_results.csv`. The associated raw file retains 288 measured
batches for 32 summary cases. Ratio calculations use unrounded values. Recorded
tests number 213, with no failures, errors, or skips. These counts are not a
claim of exhaustive proof or a measured statement-coverage percentage.

Appendix A maps all 63 FR/TR/PR/SE/D identifiers. Appendix B maps all 12 SC
identifiers. The original evaluation remains exactly two pages and is separate
from the expanded report. No benchmark measurements were replaced for this task.

## Rebuild and inspect

From the repository root, after creating the documented virtual environment:

```bash
python -m pip install -e ".[docs]"
python scripts/build_project_report.py --preview-dir dist/report-preview
```

On Windows without activation, use `.venv\Scripts\python.exe` in place of
`python`. The command writes `docs/project_report.pdf` and
`docs/project_report.docx`. Markdown remains the editable source; edits made
only in Word will be replaced by the next build. Preview images and a JSON
validation summary are generated under the ignored `dist/report-preview/`.

The tree image was generated from the checked-in renderer diagrams. The
report's benchmark figure plots the retained 1,000-entry summary measurements
and batch ranges; the complete four-size chart remains in `results/benchmark_chart.png`.
If replacing measured results,
update the report's numerical table and narrative as well as the associated
figures before rebuilding. The script checks pagination and requirement
coverage, but visual review and numerical consistency checks remain necessary.
