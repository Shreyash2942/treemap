# Academic sources and editing notes

The two-page evaluation and expanded report use third-person analytical prose,
APA-style author/date citations, alphabetized references, and hanging indents.
The expanded report retains the title and title-page details exactly as supplied
in the edited Word document. Its PDF was exported from that saved document.

## Retained documents

- [Two-page evaluation PDF](evaluation.pdf), rebuilt from [evaluation.md](evaluation.md).
- [Expanded report PDF](project_report.pdf): 18 pages, including 11 main-body pages
  (pages 3–13).
- [Editable expanded report](project_report.docx): open in a compatible Word processor,
  make changes, and export to PDF. Both figures are embedded in the document.

The expanded report assesses the original validated version 1.0.2 snapshot.
Its 63 requirement/deliverable identifiers and 12 success criteria describe
that evidence. The later cleanup removed the separate implementation-plan
and submission-guide documents at the user's request; the current D-16
milestone record is in CHANGELOG and Git history. Historical document paths
in the report remain recoverable from the original release history.

## Sources

Primary sources were verified on October 25, 2026:

- Sedgewick and Wayne's [BST chapter](https://algs4.cs.princeton.edu/32bst/)
  supports the theoretical background. The [publisher's record](https://www.pearson.com/en-gb/subject-catalog/p/algorithms/P200000000597)
  verifies *Algorithms*, fourth edition, 2011, Addison-Wesley Professional.
- The Python Software Foundation's [versioned sys documentation](https://docs.python.org/3.14/library/sys.html#sys.getrecursionlimit)
  supports the interpreter recursion-limit discussion; its reference uses `n.d.`.
- The PostgreSQL Global Development Group's [version 18 documentation](https://www.postgresql.org/docs/18/btree.html)
  describes a balanced, multiway B-tree, explicitly distinguished from this
  project's ordinary BST. Its undated reference uses `n.d.`.
- APA's [Student Paper Setup Guide](https://apastyle.apa.org/instructional-aids/student-paper-setup-guide.pdf)
  supplies the formatting conventions. The expanded report's current title page
  retains the details supplied through the Word edits.
- The [versioned project repository](https://github.com/Shreyash2942/treemap/tree/v1.0.2)
  is cited as software in the expanded report, without a named author.

The reports paraphrase their external sources. Implementation behavior,
213-test evidence, and benchmark findings come from the project itself.
Published measurements are retained in `results/performance_results.csv`,
with 288 samples and methodology in [performance_analysis.md](performance_analysis.md).
The cleanup does not replace those measurements or claim exhaustive proof.

## Rebuild the two-page evaluation

```bash
python -m pip install -e ".[docs]"
python scripts/build_evaluation.py
```

Optional page previews: add `--preview-dir dist/evaluation-preview`.
The builder enforces two substantive pages, uses 12-point Times, double
spacing, one-inch margins, page numbers, and hanging references. Times New
Roman is embedded when available; standard PDF Times is the fallback.

The expanded report is maintained in Word and exported as PDF. Its duplicate
Markdown, standalone figure copies, and custom generator were removed during
cleanup. Review content, measured values, references, and pagination after edits.
