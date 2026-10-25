"""Build the two-page evaluation from its editable Markdown source."""

from __future__ import annotations

import argparse
import re
from html import escape
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate

ROOT = Path(__file__).resolve().parents[1]


def academic_font(font_dir: Path) -> str:
    """Embed Times New Roman when installed; otherwise use standard PDF Times."""
    names = {
        "Academic": "times.ttf",
        "Academic-Bold": "timesbd.ttf",
        "Academic-Italic": "timesi.ttf",
        "Academic-BoldItalic": "timesbi.ttf",
    }
    if not all((font_dir / filename).is_file() for filename in names.values()):
        return "Times-Roman"
    for name, filename in names.items():
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily(
        "Academic",
        normal="Academic",
        bold="Academic-Bold",
        italic="Academic-Italic",
        boldItalic="Academic-BoldItalic",
    )
    return "Academic"


def paragraph_markup(text: str) -> str:
    """Support italic reference titles and clickable URLs without raw HTML."""
    marked = escape(text)
    marked = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", marked)
    return re.sub(
        r"https://[^\s<]+", lambda match: f'<link href="{match[0]}">{match[0]}</link>', marked
    )


def build_evaluation(source: Path, output: Path, font_dir: Path) -> int:
    """Render APA-style body/references and enforce exactly two readable pages."""
    font = academic_font(font_dir)
    bold = "Academic-Bold" if font == "Academic" else "Times-Bold"
    body = ParagraphStyle(
        "Body",
        fontName=font,
        fontSize=12,
        leading=24,
        firstLineIndent=36,
        allowWidows=0,
        allowOrphans=0,
    )
    title = ParagraphStyle(
        "Title",
        parent=body,
        fontName=bold,
        alignment=TA_CENTER,
        firstLineIndent=0,
        keepWithNext=True,
    )
    heading = ParagraphStyle(
        "Heading", parent=body, fontName=bold, firstLineIndent=0, keepWithNext=True
    )
    references = ParagraphStyle("Reference", parent=body, leftIndent=36, firstLineIndent=-36)
    story = []
    in_references = False
    for block in re.split(r"\n\s*\n", source.read_text(encoding="utf-8").strip()):
        text = " ".join(block.splitlines())
        if text == "<!-- pagebreak -->":
            story.append(PageBreak())
        elif text.startswith("# "):
            story.append(Paragraph(paragraph_markup(text[2:]), title))
        elif text.startswith("## "):
            label = text[3:]
            in_references = label == "References"
            story.append(Paragraph(paragraph_markup(label), title if in_references else heading))
        else:
            story.append(Paragraph(paragraph_markup(text), references if in_references else body))

    def page_number(canvas, document) -> None:
        canvas.setFont(font, 12)
        canvas.drawRightString(letter[0] - 72, letter[1] - 36, str(document.page))

    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72,
        title="Evaluating Tree-Based Data Structures",
        author="",
        invariant=1,
    )
    document.build(story, onFirstPage=page_number, onLaterPages=page_number)
    reader = PdfReader(output)
    if len(reader.pages) != 2:
        raise ValueError(
            f"Evaluation must be two pages; generated {len(reader.pages)}. Revise prose."
        )
    if any(len(page.extract_text().strip()) < 700 for page in reader.pages):
        raise ValueError("Both pages must contain substantial readable evaluation text.")
    return len(reader.pages)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "docs/evaluation.md")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/evaluation.pdf")
    parser.add_argument("--font-dir", type=Path, default=Path("C:/Windows/Fonts"))
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    pages = build_evaluation(args.source, args.output, args.font_dir)
    print(f"Wrote {args.output} ({pages} pages, 12-point Times, double-spaced).")
    if args.preview_dir is not None:
        import pymupdf

        args.preview_dir.mkdir(parents=True, exist_ok=True)
        with pymupdf.open(args.output) as document:
            for index, page in enumerate(document):
                page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(
                    args.preview_dir / f"page-{index + 1}.png"
                )


if __name__ == "__main__":
    main()
