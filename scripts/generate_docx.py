"""
Generate a professional PRD DOCX from markdown content.

Usage:
    python generate_docx.py --input <markdown_file> --output <output_docx>

Or use as a library:
    from generate_docx import DocxBuilder
    builder = DocxBuilder("My Document Title")
    builder.add_heading("Section 1", level=1)
    builder.add_paragraph("Content here")
    builder.add_table(headers, rows)
    builder.add_image("diagram.png", caption="Architecture Diagram")
    builder.save("output.docx")

Requirements:
    pip install python-docx Pillow
"""

import argparse
import re
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

try:
    from PIL import Image as PILImage
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# Brand colors
BRAND_BLUE = RGBColor(0x00, 0x78, 0xD4)
BRAND_BLUE_LIGHT = RGBColor(0xE3, 0xF2, 0xFD)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MID_GRAY = RGBColor(0x6C, 0x75, 0x7D)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
GREEN = RGBColor(0x28, 0xA7, 0x45)
ORANGE = RGBColor(0xFD, 0x7E, 0x14)
RED = RGBColor(0xDC, 0x35, 0x45)


# ═══════════════════════════════════════════════════════════
# DOCX BUILDER CLASS
# ═══════════════════════════════════════════════════════════

class DocxBuilder:
    """
    Builder class for creating professional DOCX documents.

    Usage:
        builder = DocxBuilder("Feature X — Product Requirements")
        builder.add_heading("1. Overview", level=1)
        builder.add_paragraph("Feature X enables...")
        builder.add_table(["Col A", "Col B"], [["val1", "val2"]])
        builder.add_image("arch_diagram.png", caption="Architecture")
        builder.save("output/feature_x_prd.docx")
    """

    def __init__(self, title, subtitle="Product Requirements Document"):
        self.doc = Document()
        self.title = title
        self.subtitle = subtitle
        self._headings = []  # (text, level, bookmark_name), in document order
        self._toc_anchor = None  # paragraph the real TOC gets inserted before, at save() time
        self._bookmark_id = 1000
        self._setup_styles()
        self._setup_page()

    def _setup_page(self):
        """Configure page margins and layout."""
        for section in self.doc.sections:
            section.top_margin = Cm(2.5)
            section.bottom_margin = Cm(2.5)
            section.left_margin = Cm(2.5)
            section.right_margin = Cm(2.5)
            section.header_distance = Cm(1.2)
            section.footer_distance = Cm(1.2)

    def _setup_styles(self):
        """Configure professional document styles."""
        # Normal text
        style = self.doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)
        style.font.color.rgb = DARK_GRAY
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.15

        # Heading styles
        for i, (size, spacing_before) in enumerate(
            [(26, 24), (20, 18), (15, 14), (13, 12)], start=1
        ):
            if i <= 3:
                h = self.doc.styles[f'Heading {i}']
                h.font.color.rgb = BRAND_BLUE
                h.font.name = 'Calibri'
                h.font.size = Pt(size)
                h.font.bold = True
                h.paragraph_format.space_before = Pt(spacing_before)
                h.paragraph_format.space_after = Pt(8)

        # Create a "Callout" style for blockquotes
        try:
            callout = self.doc.styles.add_style('Callout', WD_STYLE_TYPE.PARAGRAPH)
            callout.font.name = 'Calibri'
            callout.font.size = Pt(11)
            callout.font.italic = True
            callout.font.color.rgb = MID_GRAY
            callout.paragraph_format.left_indent = Cm(1.0)
            callout.paragraph_format.space_before = Pt(6)
            callout.paragraph_format.space_after = Pt(6)
        except ValueError:
            pass  # Style already exists

    def save(self, path):
        """Save the document. Fills in the real Table of Contents (if
        add_table_of_contents() was called) from every heading added via
        add_heading() — regardless of call order, since headings are only
        known once the whole document has been built."""
        if self._toc_anchor is not None:
            self._fill_table_of_contents()
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(output_path))
        print(f"✅ Generated: {output_path}")

    # ─── TITLE & STRUCTURE ─────────────────────────────────

    def add_title_page(self):
        """Add a professional title page."""
        for _ in range(4):
            self.doc.add_paragraph()

        # Title
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(self.title)
        run.font.size = Pt(32)
        run.font.bold = True
        run.font.color.rgb = BRAND_BLUE

        # Blue accent line
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('━' * 40)
        run.font.color.rgb = BRAND_BLUE
        run.font.size = Pt(8)

        # Subtitle
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(self.subtitle)
        run.font.size = Pt(18)
        run.font.color.rgb = MID_GRAY

        self.doc.add_paragraph()
        self.doc.add_paragraph()

        # Metadata table
        table = self.doc.add_table(rows=4, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        metadata = [
            ("Author", "Deepu S"),
            ("Status", "Draft"),
            ("Last Updated", "2026"),
            ("Version", "1.0"),
        ]
        for i, (key, value) in enumerate(metadata):
            cells = table.rows[i].cells
            cells[0].text = key
            cells[1].text = value
            for paragraph in cells[0].paragraphs:
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(11)
            for paragraph in cells[1].paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(11)

        self.doc.add_page_break()

    def add_table_of_contents(self):
        """Reserve a Table of Contents page. The real entries — one per
        add_heading() call, each a clickable internal link — are filled in
        at save() time, once every heading in the document is known. This
        deliberately does not use a Word TOC field: those need a manual
        right-click → Update Field in Word before they show anything, which
        is not acceptable for a document meant to be opened and read as-is.
        There are no page numbers (python-docx cannot compute real page
        numbers without Word's own layout pass) — entries are indented by
        heading level instead, which is what actually orients a reader in a
        document this size."""
        self.doc.add_heading('Table of Contents', level=1)
        self._toc_anchor = self.doc.add_paragraph()
        self.doc.add_page_break()

    def _add_bookmark(self, paragraph, name):
        self._bookmark_id += 1
        bm_id = str(self._bookmark_id)
        start = OxmlElement('w:bookmarkStart')
        start.set(qn('w:id'), bm_id)
        start.set(qn('w:name'), name)
        end = OxmlElement('w:bookmarkEnd')
        end.set(qn('w:id'), bm_id)
        paragraph._p.insert(0, start)
        paragraph._p.append(end)

    def _fill_table_of_contents(self):
        for text, level, bookmark in self._headings:
            entry = self._toc_anchor.insert_paragraph_before()
            entry.paragraph_format.left_indent = Cm(0.6 * (level - 1))
            entry.paragraph_format.space_after = Pt(4 if level == 1 else 2)

            hyperlink = OxmlElement('w:hyperlink')
            hyperlink.set(qn('w:anchor'), bookmark)
            run = OxmlElement('w:r')
            rPr = OxmlElement('w:rPr')
            color = OxmlElement('w:color')
            color.set(qn('w:val'), '0078D4')
            rPr.append(color)
            if level == 1:
                b = OxmlElement('w:b')
                rPr.append(b)
            underline = OxmlElement('w:u')
            underline.set(qn('w:val'), 'single')
            rPr.append(underline)
            sz = OxmlElement('w:sz')
            sz.set(qn('w:val'), '22' if level == 1 else '20')
            rPr.append(sz)
            run.append(rPr)
            t = OxmlElement('w:t')
            t.text = text
            run.append(t)
            hyperlink.append(run)
            entry._p.append(hyperlink)

    def add_header_footer(self, header_text="", include_page_numbers=True):
        """Add header text and page numbers to all sections."""
        for section in self.doc.sections:
            # Header
            if header_text:
                header = section.header
                header.is_linked_to_previous = False
                p = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
                p.text = header_text
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.color.rgb = MID_GRAY
                    run.font.italic = True

            # Footer with page numbers
            if include_page_numbers:
                footer = section.footer
                footer.is_linked_to_previous = False
                p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

                run = p.add_run()
                fldChar1 = run._r.makeelement(qn('w:fldChar'), {qn('w:fldCharType'): 'begin'})
                run._r.append(fldChar1)

                run2 = p.add_run()
                instrText = run2._r.makeelement(qn('w:instrText'), {})
                instrText.text = ' PAGE '
                run2._r.append(instrText)

                run3 = p.add_run()
                fldChar2 = run3._r.makeelement(qn('w:fldChar'), {qn('w:fldCharType'): 'end'})
                run3._r.append(fldChar2)

                for r in [run, run2, run3]:
                    r.font.size = Pt(9)
                    r.font.color.rgb = MID_GRAY

    # ─── CONTENT ELEMENTS ─────────────────────────────────

    def add_heading(self, text, level=1):
        """Add a heading. Bookmarked and recorded so add_table_of_contents()
        can link to it, regardless of which was called first."""
        heading = self.doc.add_heading(text, level=level)
        if level <= 3:
            bookmark = f"h{len(self._headings) + 1}"
            self._add_bookmark(heading, bookmark)
            self._headings.append((text, level, bookmark))
        return heading

    def add_paragraph(self, text, bold=False, italic=False, color=None):
        """Add a paragraph with optional formatting."""
        p = self.doc.add_paragraph()
        # Handle inline bold (**text**)
        parts = re.split(r'\*\*(.+?)\*\*', text)
        for j, part in enumerate(parts):
            if part:
                run = p.add_run(part)
                if j % 2 == 1 or bold:
                    run.bold = True
                if italic:
                    run.italic = True
                if color:
                    run.font.color.rgb = color
        return p

    def add_blockquote(self, text):
        """Add a styled blockquote/callout."""
        try:
            p = self.doc.add_paragraph(style='Callout')
        except KeyError:
            p = self.doc.add_paragraph()
        run = p.add_run(text)
        run.font.italic = True
        run.font.color.rgb = MID_GRAY
        p.paragraph_format.left_indent = Cm(1.0)

        # Add left border via XML
        pPr = p._p.get_or_add_pPr()
        pBdr = pPr.makeelement(qn('w:pBdr'), {})
        left_border = pBdr.makeelement(qn('w:left'), {
            qn('w:val'): 'single',
            qn('w:sz'): '12',
            qn('w:space'): '8',
            qn('w:color'): '0078D4',
        })
        pBdr.append(left_border)
        pPr.append(pBdr)

        return p

    def add_bullet(self, text, level=0):
        """Add a bullet point item."""
        p = self.doc.add_paragraph(style='List Bullet')
        p.clear()
        # Handle inline bold
        parts = re.split(r'\*\*(.+?)\*\*', text)
        for j, part in enumerate(parts):
            if part:
                run = p.add_run(part)
                if j % 2 == 1:
                    run.bold = True
        if level > 0:
            p.paragraph_format.left_indent = Cm(1.2 * level)
        return p

    def add_numbered_item(self, text):
        """Add a numbered list item."""
        return self.doc.add_paragraph(text, style='List Number')

    def add_table(self, headers, rows, col_widths=None, highlight_header=True,
                  zebra_stripe=True, compact=False):
        """
        Add a professionally formatted table.
        col_widths: list of widths in inches
        """
        if not headers or not rows:
            return

        num_cols = len(headers)
        table = self.doc.add_table(rows=len(rows) + 1, cols=num_cols)
        table.style = 'Table Grid'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Column widths
        if col_widths:
            for i, w in enumerate(col_widths[:num_cols]):
                for row in table.rows:
                    row.cells[i].width = Inches(w)

        # Header row
        for i, header in enumerate(headers):
            cell = table.rows[0].cells[i]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(header)
            run.bold = True
            run.font.size = Pt(10 if compact else 11)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            if highlight_header:
                shading = cell._element.makeelement(qn('w:shd'), {
                    qn('w:fill'): '0078D4',
                    qn('w:val'): 'clear',
                })
                cell._element.get_or_add_tcPr().append(shading)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Data rows
        for row_idx, row_data in enumerate(rows):
            for col_idx in range(min(len(row_data), num_cols)):
                cell = table.rows[row_idx + 1].cells[col_idx]
                cell_text = str(row_data[col_idx])
                cell.text = ''

                p = cell.paragraphs[0]
                # Handle status emoji coloring
                run = p.add_run(cell_text)
                run.font.size = Pt(9 if compact else 10)

                # Zebra stripe
                if zebra_stripe and row_idx % 2 == 0:
                    shading = cell._element.makeelement(qn('w:shd'), {
                        qn('w:fill'): 'F8F9FA',
                        qn('w:val'): 'clear',
                    })
                    cell._element.get_or_add_tcPr().append(shading)

        self.doc.add_paragraph()  # spacing
        return table

    def add_colored_table(self, headers, rows, status_col=None,
                           status_colors=None):
        """
        Table with color-coded status column.
        status_col: column index to color-code
        status_colors: dict mapping cell values to hex colors
        """
        if not status_colors:
            status_colors = {
                '✅': 'C8E6C9', '⚠️': 'FFF3E0', '❌': 'FFCDD2',
                '🌟': 'BBDEFB', 'P0': 'FFCDD2', 'P1': 'FFF3E0',
                'P2': 'C8E6C9', 'High': 'FFCDD2', 'Medium': 'FFF3E0',
                'Low': 'C8E6C9',
            }

        table = self.add_table(headers, rows)
        if table and status_col is not None:
            for row_idx, row_data in enumerate(rows):
                if status_col < len(row_data):
                    cell_text = str(row_data[status_col])
                    cell = table.rows[row_idx + 1].cells[status_col]
                    for status_key, color_hex in status_colors.items():
                        if status_key in cell_text:
                            shading = cell._element.makeelement(qn('w:shd'), {
                                qn('w:fill'): color_hex,
                                qn('w:val'): 'clear',
                            })
                            cell._element.get_or_add_tcPr().append(shading)
                            break
        return table

    def add_image(self, image_path, caption="", width=Inches(5.5)):
        """Add an image with optional caption, centered."""
        img_path = Path(image_path)
        if not img_path.exists():
            self.add_paragraph(f"[Image not found: {image_path}]", italic=True,
                               color=RED)
            return

        # Scale proportionally if PIL is available
        if HAS_PIL:
            with PILImage.open(str(img_path)) as img:
                img_w, img_h = img.size
                aspect = img_w / img_h
                max_width = width
                calc_height = Inches(max_width / Inches(1) / aspect)
                max_height = Inches(4.5)
                if calc_height > max_height:
                    width = Inches(max_height / Inches(1) * aspect)

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(str(img_path), width=width)

        if caption:
            cap = self.doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = cap.add_run(f"Figure: {caption}")
            run.font.size = Pt(9)
            run.font.italic = True
            run.font.color.rgb = MID_GRAY

    def add_page_break(self):
        """Add a page break."""
        self.doc.add_page_break()

    def add_horizontal_rule(self):
        """Add a horizontal line separator."""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('━' * 60)
        run.font.size = Pt(6)
        run.font.color.rgb = RGBColor(0xDE, 0xE2, 0xE6)

    def add_callout_box(self, title, content, color_hex='0078D4'):
        """Add a highlighted callout box with border."""
        # Title
        p = self.doc.add_paragraph()
        run = p.add_run(f"  {title}")
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(
            int(color_hex[0:2], 16),
            int(color_hex[2:4], 16),
            int(color_hex[4:6], 16)
        )
        # Left border
        pPr = p._p.get_or_add_pPr()
        pBdr = pPr.makeelement(qn('w:pBdr'), {})
        left_border = pBdr.makeelement(qn('w:left'), {
            qn('w:val'): 'single',
            qn('w:sz'): '18',
            qn('w:space'): '12',
            qn('w:color'): color_hex,
        })
        pBdr.append(left_border)
        pPr.append(pBdr)

        # Background shading
        shading = pPr.makeelement(qn('w:shd'), {
            qn('w:fill'): 'F8F9FA',
            qn('w:val'): 'clear',
        })
        pPr.append(shading)

        # Content
        p2 = self.doc.add_paragraph()
        run2 = p2.add_run(f"  {content}")
        run2.font.size = Pt(10)
        run2.font.color.rgb = DARK_GRAY
        pPr2 = p2._p.get_or_add_pPr()
        pBdr2 = pPr2.makeelement(qn('w:pBdr'), {})
        left_border2 = pBdr2.makeelement(qn('w:left'), {
            qn('w:val'): 'single',
            qn('w:sz'): '18',
            qn('w:space'): '12',
            qn('w:color'): color_hex,
        })
        pBdr2.append(left_border2)
        pPr2.append(pBdr2)
        shading2 = pPr2.makeelement(qn('w:shd'), {
            qn('w:fill'): 'F8F9FA',
            qn('w:val'): 'clear',
        })
        pPr2.append(shading2)


# ═══════════════════════════════════════════════════════════
# LEGACY FUNCTIONS (backward-compatible)
# ═══════════════════════════════════════════════════════════


def setup_document():
    """Create and configure the document with professional styling. (Legacy)"""
    builder = DocxBuilder("Document")
    return builder.doc


def add_title_page(doc, title, subtitle="Product Requirements Document"):
    """Add a professional title page."""
    # Add spacing
    for _ in range(4):
        doc.add_paragraph()

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.size = Pt(32)
    run.font.bold = True
    run.font.color.rgb = BRAND_BLUE

    # Subtitle
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(subtitle)
    run.font.size = Pt(18)
    run.font.color.rgb = DARK_GRAY

    # Spacing
    doc.add_paragraph()
    doc.add_paragraph()

    # Metadata table
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    metadata = [
        ("Author", "Deepu S"),
        ("Status", "Draft"),
        ("Last Updated", "2026"),
        ("Version", "1.0"),
    ]

    for i, (key, value) in enumerate(metadata):
        cells = table.rows[i].cells
        cells[0].text = key
        cells[1].text = value
        # Bold the key
        for paragraph in cells[0].paragraphs:
            for run in paragraph.runs:
                run.bold = True

    # Page break after title
    doc.add_page_break()


def add_table_of_contents(doc):
    """Add a Table of Contents placeholder."""
    doc.add_heading('Table of Contents', level=1)
    p = doc.add_paragraph()
    p.add_run('[Table of Contents — update field after opening in Word]').italic = True
    doc.add_page_break()


def parse_markdown_table(lines, start_idx):
    """Parse a markdown table starting at the given line index."""
    headers = []
    rows = []

    if start_idx < len(lines) and lines[start_idx].startswith('|'):
        # Parse header
        headers = [cell.strip() for cell in lines[start_idx].split('|')[1:-1]]
        # Skip separator line
        start_idx += 2
        # Parse rows
        while start_idx < len(lines) and lines[start_idx].startswith('|'):
            row = [cell.strip() for cell in lines[start_idx].split('|')[1:-1]]
            rows.append(row)
            start_idx += 1

    return headers, rows, start_idx


def add_formatted_table(doc, headers, rows):
    """Add a professionally formatted table to the document. (Legacy)"""
    if not headers or not rows:
        return

    num_cols = len(headers)
    table = doc.add_table(rows=len(rows) + 1, cols=num_cols)
    table.style = 'Table Grid'

    # Header row with blue background
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(header)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Blue header shading
        shading = cell._element.makeelement(qn('w:shd'), {
            qn('w:fill'): '0078D4',
            qn('w:val'): 'clear',
        })
        cell._element.get_or_add_tcPr().append(shading)

    # Data rows with zebra striping
    for row_idx, row_data in enumerate(rows):
        for col_idx in range(min(len(row_data), num_cols)):
            cell = table.rows[row_idx + 1].cells[col_idx]
            cell.text = row_data[col_idx]
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

            # Zebra stripe
            if row_idx % 2 == 0:
                shading = cell._element.makeelement(qn('w:shd'), {
                    qn('w:fill'): 'F8F9FA',
                    qn('w:val'): 'clear',
                })
                cell._element.get_or_add_tcPr().append(shading)

    doc.add_paragraph()  # Spacing after table


def markdown_to_docx(md_content, doc):
    """Convert markdown content to DOCX elements with full formatting support."""
    lines = md_content.split('\n')
    i = 0
    in_code_block = False
    code_block_lines = []

    while i < len(lines):
        line = lines[i]

        # Skip document title (# Title) — already on title page
        if line.startswith('# ') and i < 5:
            i += 1
            continue

        # Code blocks (``` fenced)
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block — render collected lines
                code_text = '\n'.join(code_block_lines)
                p = doc.add_paragraph()
                run = p.add_run(code_text)
                run.font.name = 'Consolas'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                # Add background shading
                pPr = p._p.get_or_add_pPr()
                shading = pPr.makeelement(qn('w:shd'), {
                    qn('w:fill'): 'F5F5F5',
                    qn('w:val'): 'clear',
                })
                pPr.append(shading)
                p.paragraph_format.left_indent = Cm(0.5)
                code_block_lines = []
                in_code_block = False
            else:
                in_code_block = True
                code_block_lines = []
            i += 1
            continue

        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue

        # Headings
        if line.startswith('#### '):
            # Render as bold paragraph (H4 not always styled)
            p = doc.add_paragraph()
            run = p.add_run(line[5:].strip())
            run.bold = True
            run.font.size = Pt(12)
            run.font.color.rgb = BRAND_BLUE
            i += 1
            continue
        elif line.startswith('### '):
            doc.add_heading(line[4:].strip(), level=3)
            i += 1
            continue
        elif line.startswith('## '):
            doc.add_heading(line[3:].strip(), level=2)
            i += 1
            continue
        elif line.startswith('# '):
            doc.add_heading(line[2:].strip(), level=1)
            i += 1
            continue

        # Horizontal rule
        if line.strip() in ('---', '***', '___'):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run('━' * 50)
            run.font.size = Pt(6)
            run.font.color.rgb = RGBColor(0xDE, 0xE2, 0xE6)
            i += 1
            continue

        # Blockquotes
        if line.startswith('> '):
            quote_text = line[2:].strip()
            # Collect multi-line blockquote
            while i + 1 < len(lines) and lines[i + 1].startswith('> '):
                i += 1
                quote_text += '\n' + lines[i][2:].strip()

            p = doc.add_paragraph()
            run = p.add_run(quote_text)
            run.font.italic = True
            run.font.color.rgb = MID_GRAY
            p.paragraph_format.left_indent = Cm(1.0)
            # Blue left border
            pPr = p._p.get_or_add_pPr()
            pBdr = pPr.makeelement(qn('w:pBdr'), {})
            left_border = pBdr.makeelement(qn('w:left'), {
                qn('w:val'): 'single',
                qn('w:sz'): '12',
                qn('w:space'): '8',
                qn('w:color'): '0078D4',
            })
            pBdr.append(left_border)
            pPr.append(pBdr)
            i += 1
            continue

        # Tables
        if line.startswith('|'):
            headers, rows, new_i = parse_markdown_table(lines, i)
            if headers and rows:
                add_formatted_table(doc, headers, rows)
            i = new_i
            continue

        # Nested bullet points (indented)
        indent_match = re.match(r'^(\s{2,}|\t+)[-*]\s+(.+)', line)
        if indent_match:
            text = indent_match.group(2).strip()
            p = doc.add_paragraph(style='List Bullet')
            p.clear()
            # Handle inline bold
            parts = re.split(r'\*\*(.+?)\*\*', text)
            for j, part in enumerate(parts):
                if part:
                    run = p.add_run(part)
                    if j % 2 == 1:
                        run.bold = True
            indent_level = len(indent_match.group(1).replace('\t', '  ')) // 2
            p.paragraph_format.left_indent = Cm(1.2 * indent_level)
            i += 1
            continue

        # Bullet points
        if line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.clear()
            # Handle inline bold
            parts = re.split(r'\*\*(.+?)\*\*', text)
            for j, part in enumerate(parts):
                if part:
                    run = p.add_run(part)
                    if j % 2 == 1:
                        run.bold = True
            i += 1
            continue

        # Numbered list
        numbered_match = re.match(r'^(\d+)\.\s+(.+)', line)
        if numbered_match:
            text = numbered_match.group(2).strip()
            p = doc.add_paragraph(style='List Number')
            p.clear()
            parts = re.split(r'\*\*(.+?)\*\*', text)
            for j, part in enumerate(parts):
                if part:
                    run = p.add_run(part)
                    if j % 2 == 1:
                        run.bold = True
            i += 1
            continue

        # Bold text paragraph
        if line.startswith('**') and line.endswith('**'):
            p = doc.add_paragraph()
            run = p.add_run(line.strip('*'))
            run.bold = True
            i += 1
            continue

        # Regular paragraph
        if line.strip():
            text = line.strip()
            p = doc.add_paragraph()

            # Handle inline formatting (bold + inline code)
            parts = re.split(r'(\*\*.+?\*\*|`.+?`)', text)
            for part in parts:
                if not part:
                    continue
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.bold = True
                elif part.startswith('`') and part.endswith('`'):
                    run = p.add_run(part[1:-1])
                    run.font.name = 'Consolas'
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(0xD6, 0x33, 0x84)
                else:
                    run = p.add_run(part)

            i += 1
            continue

        # Empty line — skip
        i += 1


def generate_docx(input_file, output_file):
    """Main function to generate DOCX from markdown."""
    md_content = Path(input_file).read_text(encoding='utf-8')

    # Extract title
    title_match = re.search(r'^# (.+)', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Product Requirements Document"

    doc = setup_document()
    add_title_page(doc, title)
    add_table_of_contents(doc)

    # Convert markdown body
    markdown_to_docx(md_content, doc)

    # Save
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    print(f"✅ Generated: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate DOCX from markdown PRD")
    parser.add_argument("--input", required=True, help="Input markdown file")
    parser.add_argument("--output", required=True, help="Output DOCX file path")
    args = parser.parse_args()

    generate_docx(args.input, args.output)
