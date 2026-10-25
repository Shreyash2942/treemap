# Evaluation sources and formatting decisions

The evaluation uses third-person analytical prose and attributes external
claims with APA-style author/date citations. References are alphabetized and
use hanging indents. References count within the requested two pages; no
separate title page, fictional author, or invented student details are added.

Primary sources verified on October 25, 2026:

- Sedgewick and Wayne's [BST chapter](https://algs4.cs.princeton.edu/32bst/)
  supports ordered-search structure, successor deletion, and height-dependent
  complexity. The [publisher's catalog](https://www.pearson.com/en-gb/subject-catalog/p/algorithms/P200000000597/9780132762564)
  and [Princeton course description](https://algs4.cs.princeton.edu/home/CS2013-final-report.pdf)
  verify the 2011 fourth edition and Addison-Wesley Professional attribution.
- The Python Software Foundation's [versioned documentation](https://docs.python.org/3.14/library/sys.html#sys.getrecursionlimit)
  supports the finite interpreter recursion limit. The source has no explicit
  publication date for that page, so its reference uses `n.d.`.
- The PostgreSQL Global Development Group's [version 18 documentation](https://www.postgresql.org/docs/18/btree.html)
  identifies its index as a balanced, multiway B-tree. It is used as a related
  application, with an explicit distinction from this project's ordinary BST.
  Its undated documentation reference also uses `n.d.`.

Project performance findings are original measurements from
`results/performance_results.csv`, with full method and limits in
`performance_analysis.md`; they are not attributed to the external sources.

Regeneration:

```bash
python -m pip install -e ".[docs]"
python scripts/build_evaluation.py
python scripts/build_evaluation.py --preview-dir dist/evaluation_preview
```

The builder checks that the PDF contains exactly two substantive, text-readable
pages. It uses US Letter paper, one-inch margins, 12-point Times, double-spaced
paragraphs, page numbers, and hanging references. Installed Times New Roman
fonts are embedded on Windows; standard PDF Times is the fallback elsewhere.
The editable Markdown and generated PDF retain the same wording.
