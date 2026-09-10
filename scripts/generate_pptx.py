"""
PPTX Utility Library for PM Feature Agent.

This module provides helper functions for creating professional, visually
appealing PowerPoint presentations. The LLM should import these helpers
when writing custom per-feature build scripts.

Usage (in a custom build_documents.py):
    import sys
    sys.path.insert(0, '/path/to/Templates')
    from generate_pptx import PresentationBuilder

Requirements:
    pip install python-pptx Pillow matplotlib
"""

import re
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR_TYPE
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml.ns import qn

try:
    from PIL import Image as PILImage
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# ═══════════════════════════════════════════════════════════
# BRAND PALETTE
# ═══════════════════════════════════════════════════════════

class Colors:
    BRAND_BLUE = RGBColor(0x00, 0x78, 0xD4)
    DARK_NAVY = RGBColor(0x1A, 0x1A, 0x2E)
    LIGHT_NAVY = RGBColor(0x2D, 0x2D, 0x44)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    LIGHT_GRAY = RGBColor(0xF8, 0xF9, 0xFA)
    MID_GRAY = RGBColor(0x6C, 0x75, 0x7D)
    DARK_GRAY = RGBColor(0x21, 0x25, 0x29)
    GREEN = RGBColor(0x28, 0xA7, 0x45)
    ORANGE = RGBColor(0xFD, 0x7E, 0x14)
    RED = RGBColor(0xDC, 0x35, 0x45)
    TEAL = RGBColor(0x17, 0xA2, 0xB8)
    PURPLE = RGBColor(0x6F, 0x42, 0xC1)
    GRADIENT_START = RGBColor(0x0F, 0x0C, 0x29)
    GRADIENT_MID = RGBColor(0x30, 0x2B, 0x63)
    GRADIENT_END = RGBColor(0x24, 0x24, 0x3E)

    # Accent palette for charts and data visualization
    LIGHT_BLUE = RGBColor(0xBB, 0xDE, 0xFB)
    LIGHT_GREEN = RGBColor(0xC8, 0xE6, 0xC9)
    LIGHT_ORANGE = RGBColor(0xFF, 0xF3, 0xE0)
    LIGHT_RED = RGBColor(0xFF, 0xCD, 0xD2)
    LIGHT_PURPLE = RGBColor(0xE1, 0xBE, 0xE7)
    LIGHT_TEAL = RGBColor(0xB2, 0xDF, 0xDB)
    AMBER = RGBColor(0xFF, 0xC1, 0x07)
    INDIGO = RGBColor(0x3F, 0x51, 0xB5)
    DEEP_ORANGE = RGBColor(0xFF, 0x57, 0x22)
    CYAN = RGBColor(0x00, 0xBC, 0xD4)

    # Chart series colors (ordered for visual contrast)
    SERIES = [
        RGBColor(0x00, 0x78, 0xD4),  # Blue
        RGBColor(0x28, 0xA7, 0x45),  # Green
        RGBColor(0xFD, 0x7E, 0x14),  # Orange
        RGBColor(0x6F, 0x42, 0xC1),  # Purple
        RGBColor(0xDC, 0x35, 0x45),  # Red
        RGBColor(0x17, 0xA2, 0xB8),  # Teal
        RGBColor(0xFF, 0xC1, 0x07),  # Amber
        RGBColor(0x3F, 0x51, 0xB5),  # Indigo
    ]


# ═══════════════════════════════════════════════════════════
# PRESENTATION BUILDER
# ═══════════════════════════════════════════════════════════

class PresentationBuilder:
    """Builder class for creating professional presentations."""

    # Standard 16:9 widescreen in exact EMU (avoids float rounding)
    WIDESCREEN_16_9 = (Emu(12192000), Emu(6858000))  # 13⅓" × 7½"

    def __init__(self, width_inches=None, height_inches=None):
        self.prs = Presentation()
        # Use exact standard EMU values for Keynote/PowerPoint compatibility
        if width_inches is None and height_inches is None:
            self.prs.slide_width, self.prs.slide_height = self.WIDESCREEN_16_9
        else:
            w = width_inches or 13.333
            h = height_inches or 7.5
            self.prs.slide_width = Emu(int(w * 914400))
            self.prs.slide_height = Emu(int(h * 914400))
        self.slide_width = self.prs.slide_width
        self.slide_height = self.prs.slide_height
        # Fix slide size type for Keynote compatibility — default template
        # has type="screen4x3" which conflicts with widescreen dimensions
        sldSz = self.prs.part._element.find(qn('p:sldSz'))
        if sldSz is not None:
            sldSz.set('type', 'custom')

    def save(self, path):
        """Save the presentation."""
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(str(output_path))
        print(f"✅ Generated: {output_path}")

    # ─── SLIDE TYPES ───────────────────────────────────────

    def add_title_slide(self, title, subtitle="", date=""):
        """Dark background title slide with accent bar."""
        slide = self._blank_slide()
        self._fill_background(slide, Colors.DARK_NAVY)

        # Accent gradient bar (left edge)
        self._add_shape(slide, 0, 0, Inches(0.15), self.slide_height,
                        Colors.BRAND_BLUE)

        # Title
        self._add_text(slide, title, Inches(1.5), Inches(2.2), Inches(10), Inches(1.8),
                       font_size=44, bold=True, color=Colors.WHITE)

        # Accent line under title
        self._add_shape(slide, Inches(1.5), Inches(4.0), Inches(3), Inches(0.06),
                        Colors.BRAND_BLUE)

        # Subtitle
        if subtitle:
            self._add_text(slide, subtitle, Inches(1.5), Inches(4.3), Inches(10), Inches(1),
                           font_size=20, color=Colors.TEAL)

        # Date
        if date:
            self._add_text(slide, date, Inches(1.5), Inches(6.2), Inches(5), Inches(0.5),
                           font_size=12, color=Colors.MID_GRAY)

        return slide

    def add_section_slide(self, title, subtitle="", number=None):
        """Section divider slide with large number."""
        slide = self._blank_slide()
        self._fill_background(slide, Colors.BRAND_BLUE)

        # Large section number (faded)
        if number:
            self._add_text(slide, str(number).zfill(2), Inches(8.5), Inches(0.5),
                           Inches(4.5), Inches(6), font_size=150,
                           color=RGBColor(0x00, 0x5A, 0xA0), bold=True,
                           alignment=PP_ALIGN.RIGHT)

        # Title
        self._add_text(slide, title, Inches(1.5), Inches(2.8), Inches(8), Inches(1.5),
                       font_size=36, bold=True, color=Colors.WHITE)

        # Subtitle
        if subtitle:
            self._add_text(slide, subtitle, Inches(1.5), Inches(4.3), Inches(8), Inches(1),
                           font_size=16, color=RGBColor(0xBB, 0xDE, 0xFB))

        return slide

    def add_content_slide(self, title, bullets, notes=""):
        """Standard content slide with title bar and bullets."""
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)

        # Title
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        # Bullets
        top = Inches(1.7)
        left = Inches(1.0)
        width = Inches(11)
        height = Inches(5.3)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True

        for i, bullet in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()

            # Sub-bullets (indented)
            if bullet.startswith("  ") or bullet.startswith("\t"):
                p.text = bullet.strip().lstrip("•-▸ ")
                p.level = 1
                p.font.size = Pt(15)
                p.font.color.rgb = Colors.MID_GRAY
            else:
                p.text = bullet.strip().lstrip("•-▸ ")
                p.level = 0
                p.font.size = Pt(18)
                p.font.color.rgb = Colors.DARK_GRAY
            p.space_after = Pt(10)

        # Speaker notes (disabled — Keynote rejects python-pptx notesMaster XML)
        # if notes:
        #     slide.notes_slide.notes_text_frame.text = notes

        return slide

    def add_two_column_slide(self, title, left_title, left_bullets, right_title, right_bullets):
        """Two-column layout for comparison or dual content."""
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        # Left column
        self._add_text(slide, left_title, Inches(0.8), Inches(1.6), Inches(5.5), Inches(0.6),
                       font_size=18, bold=True, color=Colors.BRAND_BLUE)
        self._add_bullet_list(slide, left_bullets, Inches(0.8), Inches(2.3), Inches(5.5), Inches(4.5))

        # Divider line
        self._add_shape(slide, Inches(6.5), Inches(1.6), Inches(0.02), Inches(5.2), Colors.MID_GRAY)

        # Right column
        self._add_text(slide, right_title, Inches(7.0), Inches(1.6), Inches(5.5), Inches(0.6),
                       font_size=18, bold=True, color=Colors.BRAND_BLUE)
        self._add_bullet_list(slide, right_bullets, Inches(7.0), Inches(2.3), Inches(5.5), Inches(4.5))

        return slide

    def add_kpi_slide(self, title, kpis):
        """
        KPI/metrics highlight slide with large numbers.
        kpis: list of dicts with 'value', 'label', optional 'color'
        """
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        # KPI cards
        num_kpis = len(kpis)
        card_width = Inches(10.5 / num_kpis)
        start_left = Inches(1.2)

        for i, kpi in enumerate(kpis):
            left = start_left + card_width * i
            top = Inches(2.5)

            # Card background
            shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_width - Inches(0.3), Inches(3.5)
            )
            shape.fill.solid()
            shape.fill.fore_color.rgb = Colors.LIGHT_GRAY
            shape.line.color.rgb = RGBColor(0xDE, 0xE2, 0xE6)
            shape.line.width = Pt(1)

            # Value (large number)
            color = kpi.get('color', Colors.BRAND_BLUE)
            self._add_text(slide, str(kpi['value']), left + Inches(0.2), top + Inches(0.5),
                           card_width - Inches(0.5), Inches(1.8),
                           font_size=40, bold=True, color=color, alignment=PP_ALIGN.CENTER)

            # Label
            self._add_text(slide, kpi['label'], left + Inches(0.2), top + Inches(2.3),
                           card_width - Inches(0.5), Inches(1),
                           font_size=13, color=Colors.MID_GRAY, alignment=PP_ALIGN.CENTER)

        return slide

    def add_table_slide(self, title, headers, rows, col_widths=None):
        """Professionally styled table slide."""
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        # Table
        num_rows = len(rows) + 1
        num_cols = len(headers)
        left = Inches(0.8)
        top = Inches(1.7)
        width = Inches(11.5)
        height = min(Inches(5.5), Pt(35) * num_rows)

        table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
        table = table_shape.table

        # Column widths
        if col_widths:
            for i, w in enumerate(col_widths):
                table.columns[i].width = Inches(w)

        # Header row styling
        for i, header in enumerate(headers):
            cell = table.cell(0, i)
            cell.text = header
            cell.fill.solid()
            cell.fill.fore_color.rgb = Colors.BRAND_BLUE
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                p.font.color.rgb = Colors.WHITE
                p.font.bold = True
                p.font.size = Pt(12)
                p.alignment = PP_ALIGN.CENTER

        # Data rows
        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_text in enumerate(row_data):
                cell = table.cell(row_idx + 1, col_idx)
                cell.text = str(cell_text)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                if row_idx % 2 == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = Colors.LIGHT_GRAY
                for p in cell.text_frame.paragraphs:
                    p.font.size = Pt(11)
                    p.font.color.rgb = Colors.DARK_GRAY

        return slide

    def add_image_slide(self, title, image_path, caption=""):
        """Slide with a centered image (diagram, chart, architecture)."""
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        # Image (centered, scaled proportionally)
        img_path = Path(image_path)
        if img_path.exists():
            max_width = Inches(10)
            max_height = Inches(5.0)
            self._add_scaled_image(slide, str(img_path),
                                    Inches(1.5), Inches(1.6),
                                    max_width, max_height)

        # Caption
        if caption:
            self._add_text(slide, caption, Inches(1), Inches(6.8), Inches(11), Inches(0.5),
                           font_size=11, color=Colors.MID_GRAY, alignment=PP_ALIGN.CENTER)

        return slide

    def add_quote_slide(self, quote, attribution=""):
        """Customer quote or key insight slide."""
        slide = self._blank_slide()
        self._fill_background(slide, Colors.LIGHT_GRAY)

        # Large quote mark
        self._add_text(slide, "❝", Inches(1), Inches(1.5), Inches(2), Inches(2),
                       font_size=80, color=Colors.BRAND_BLUE)

        # Quote text
        self._add_text(slide, quote, Inches(1.5), Inches(3), Inches(10), Inches(2.5),
                       font_size=22, color=Colors.DARK_GRAY, italic=True)

        # Attribution
        if attribution:
            self._add_text(slide, f"— {attribution}", Inches(1.5), Inches(5.5),
                           Inches(10), Inches(0.5), font_size=14, color=Colors.MID_GRAY)

        return slide

    def add_closing_slide(self, title="Thank You", subtitle="", contact=""):
        """Closing slide."""
        slide = self._blank_slide()
        self._fill_background(slide, Colors.DARK_NAVY)

        self._add_shape(slide, 0, 0, Inches(0.15), self.slide_height, Colors.BRAND_BLUE)

        self._add_text(slide, title, Inches(1.5), Inches(2.5), Inches(10), Inches(1.5),
                       font_size=40, bold=True, color=Colors.WHITE)

        if subtitle:
            self._add_text(slide, subtitle, Inches(1.5), Inches(4.2), Inches(10), Inches(1),
                           font_size=18, color=Colors.TEAL)

        if contact:
            self._add_text(slide, contact, Inches(1.5), Inches(5.5), Inches(10), Inches(0.5),
                           font_size=12, color=Colors.MID_GRAY)

        return slide

    # ─── DIAGRAM HELPERS ───────────────────────────────────

    def add_architecture_diagram(self, slide, boxes, arrows, left=Inches(1), top=Inches(1.6)):
        """
        Draw an architecture diagram with boxes and arrows.
        boxes: list of dicts with 'name', 'x', 'y', 'w', 'h', 'color' (optional)
        arrows: list of tuples (from_box_name, to_box_name, label)
        """
        box_shapes = {}
        box_positions = {}

        for box in boxes:
            x = left + Inches(box['x'])
            y = top + Inches(box['y'])
            w = Inches(box.get('w', 2))
            h = Inches(box.get('h', 0.8))
            color = box.get('color', Colors.BRAND_BLUE)

            shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
            shape.fill.solid()
            shape.fill.fore_color.rgb = color
            shape.line.color.rgb = color
            shape.text_frame.text = box['name']
            for p in shape.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.color.rgb = Colors.WHITE
                p.font.bold = True
                p.alignment = PP_ALIGN.CENTER
            shape.text_frame.word_wrap = True

            box_shapes[box['name']] = shape
            box_positions[box['name']] = {
                'x': x, 'y': y, 'w': w, 'h': h,
                'cx': x + w // 2, 'cy': y + h // 2
            }

        # Draw arrows between boxes
        for arrow in arrows:
            from_name = arrow[0]
            to_name = arrow[1]
            label = arrow[2] if len(arrow) > 2 else ""

            if from_name not in box_positions or to_name not in box_positions:
                continue

            fp = box_positions[from_name]
            tp = box_positions[to_name]

            # Determine connection points (bottom of source → top of target by default)
            from_x = fp['cx']
            from_y = fp['y'] + fp['h']  # bottom center
            to_x = tp['cx']
            to_y = tp['y']  # top center

            # If target is to the right, use right-to-left
            if abs(tp['x'] - fp['x']) > abs(tp['y'] - fp['y']):
                if tp['x'] > fp['x']:
                    from_x = fp['x'] + fp['w']  # right edge
                    from_y = fp['cy']
                    to_x = tp['x']  # left edge
                    to_y = tp['cy']
                else:
                    from_x = fp['x']  # left edge
                    from_y = fp['cy']
                    to_x = tp['x'] + tp['w']  # right edge
                    to_y = tp['cy']

            # Draw arrow line using a thin shape
            dx = to_x - from_x
            dy = to_y - from_y
            line_left = min(from_x, to_x)
            line_top = min(from_y, to_y)

            connector = slide.shapes.add_connector(
                MSO_CONNECTOR_TYPE.STRAIGHT,
                from_x, from_y, to_x, to_y
            )
            connector.line.color.rgb = Colors.MID_GRAY
            connector.line.width = Pt(1.5)

            # Add arrowhead
            connector.end_x = to_x
            connector.end_y = to_y

            # Add label at midpoint
            if label:
                mid_x = (from_x + to_x) // 2 - Inches(0.5)
                mid_y = (from_y + to_y) // 2 - Inches(0.15)
                self._add_text(slide, label, mid_x, mid_y,
                               Inches(1.5), Inches(0.3),
                               font_size=8, color=Colors.MID_GRAY,
                               alignment=PP_ALIGN.CENTER)

        return box_shapes

    # ─── ADVANCED SLIDE TYPES ──────────────────────────────

    def add_agenda_slide(self, title, items, current_index=None):
        """Agenda/TOC slide with optional current step highlight."""
        slide = self._blank_slide()
        self._fill_background(slide, Colors.DARK_NAVY)
        self._add_shape(slide, 0, 0, Inches(0.15), self.slide_height, Colors.BRAND_BLUE)

        self._add_text(slide, title, Inches(1.5), Inches(0.5), Inches(10), Inches(1),
                       font_size=32, bold=True, color=Colors.WHITE)

        for i, item in enumerate(items):
            top = Inches(1.8) + Inches(i * 0.75)
            num_color = Colors.BRAND_BLUE if i == current_index else Colors.MID_GRAY
            text_color = Colors.WHITE if i == current_index else RGBColor(0xAA, 0xAA, 0xAA)

            # Number circle
            circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, Inches(1.5), top, Inches(0.5), Inches(0.5)
            )
            circle.fill.solid()
            circle.fill.fore_color.rgb = num_color
            circle.line.fill.background()
            circle.text_frame.text = str(i + 1)
            for p in circle.text_frame.paragraphs:
                p.font.size = Pt(14)
                p.font.bold = True
                p.font.color.rgb = Colors.WHITE
                p.alignment = PP_ALIGN.CENTER

            # Item text
            self._add_text(slide, item, Inches(2.3), top + Inches(0.05),
                           Inches(9), Inches(0.45),
                           font_size=18, color=text_color,
                           bold=(i == current_index))

        return slide

    def add_timeline_slide(self, title, phases):
        """
        Visual horizontal timeline/roadmap slide.
        phases: list of dicts with 'name', 'timeline', 'items' (list of strings), optional 'color'
        """
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        num_phases = len(phases)
        phase_width = Inches(10.5 / num_phases)
        start_left = Inches(1.2)
        track_y = Inches(2.3)

        # Timeline track (horizontal line)
        self._add_shape(slide, start_left, track_y + Inches(0.2),
                        phase_width * num_phases, Inches(0.04), Colors.MID_GRAY)

        for i, phase in enumerate(phases):
            left = start_left + phase_width * i
            color = phase.get('color', [Colors.BRAND_BLUE, Colors.TEAL, Colors.PURPLE,
                                         Colors.GREEN, Colors.ORANGE][i % 5])

            # Milestone circle
            circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, left + phase_width // 2 - Inches(0.2),
                track_y, Inches(0.45), Inches(0.45)
            )
            circle.fill.solid()
            circle.fill.fore_color.rgb = color
            circle.line.fill.background()

            # Phase name
            self._add_text(slide, phase['name'], left, track_y + Inches(0.7),
                           phase_width - Inches(0.2), Inches(0.5),
                           font_size=14, bold=True, color=color,
                           alignment=PP_ALIGN.CENTER)

            # Timeline label
            self._add_text(slide, phase.get('timeline', ''), left, track_y + Inches(1.1),
                           phase_width - Inches(0.2), Inches(0.4),
                           font_size=11, color=Colors.MID_GRAY,
                           alignment=PP_ALIGN.CENTER)

            # Items card
            if phase.get('items'):
                card_top = track_y + Inches(1.6)
                card = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.1), card_top,
                    phase_width - Inches(0.4), Inches(3.2)
                )
                card.fill.solid()
                card.fill.fore_color.rgb = Colors.LIGHT_GRAY
                card.line.color.rgb = color
                card.line.width = Pt(1.5)

                items_text = "\n".join(f"• {item}" for item in phase['items'])
                self._add_text(slide, items_text, left + Inches(0.25), card_top + Inches(0.15),
                               phase_width - Inches(0.6), Inches(2.9),
                               font_size=11, color=Colors.DARK_GRAY)

        return slide

    def add_comparison_slide(self, title, headers, rows, highlight_col=None):
        """
        Color-coded comparison matrix slide with optional highlighted column.
        rows: list of lists where cells can be '✅', '⚠️', '❌', or text
        highlight_col: index of column to emphasize (e.g., "our product")
        """
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        num_rows = len(rows) + 1
        num_cols = len(headers)
        left = Inches(0.8)
        top = Inches(1.7)
        width = Inches(11.5)
        height = min(Inches(5.5), Pt(40) * num_rows)

        table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
        table = table_shape.table

        # Header row
        for i, header in enumerate(headers):
            cell = table.cell(0, i)
            cell.text = header
            cell.fill.solid()
            if i == highlight_col:
                cell.fill.fore_color.rgb = Colors.GREEN
            else:
                cell.fill.fore_color.rgb = Colors.BRAND_BLUE
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                p.font.color.rgb = Colors.WHITE
                p.font.bold = True
                p.font.size = Pt(11)
                p.alignment = PP_ALIGN.CENTER

        # Data rows with color-coded status cells
        status_colors = {
            '✅': RGBColor(0xC8, 0xE6, 0xC9),  # light green
            '⚠️': RGBColor(0xFF, 0xF3, 0xE0),   # light orange
            '❌': RGBColor(0xFF, 0xCD, 0xD2),    # light red
            '🌟': RGBColor(0xBB, 0xDE, 0xFB),   # light blue
        }

        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_text in enumerate(row_data):
                cell = table.cell(row_idx + 1, col_idx)
                text_str = str(cell_text)
                cell.text = text_str
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE

                # Color-code status cells
                status_match = False
                for status, bg_color in status_colors.items():
                    if status in text_str:
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = bg_color
                        status_match = True
                        break

                if not status_match:
                    if col_idx == highlight_col:
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = RGBColor(0xE8, 0xF5, 0xE9)
                    elif row_idx % 2 == 0:
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = Colors.LIGHT_GRAY

                for p in cell.text_frame.paragraphs:
                    p.font.size = Pt(10)
                    p.font.color.rgb = Colors.DARK_GRAY
                    p.alignment = PP_ALIGN.CENTER

        return slide

    def add_before_after_slide(self, title, before_title, before_content,
                                after_title, after_content, before_image=None,
                                after_image=None):
        """
        Before/after comparison slide for enhancements.
        content: list of bullet strings or a single text string
        """
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        # BEFORE panel
        # Header bar
        self._add_shape(slide, Inches(0.5), Inches(1.6), Inches(5.8), Inches(0.5),
                        Colors.MID_GRAY)
        self._add_text(slide, before_title, Inches(0.7), Inches(1.63),
                       Inches(5.4), Inches(0.45),
                       font_size=14, bold=True, color=Colors.WHITE)

        # Before content area
        before_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(2.15),
            Inches(5.8), Inches(4.8)
        )
        before_card.fill.solid()
        before_card.fill.fore_color.rgb = Colors.LIGHT_GRAY
        before_card.line.color.rgb = Colors.MID_GRAY
        before_card.line.width = Pt(1)

        if before_image and Path(before_image).exists():
            self._add_scaled_image(slide, before_image,
                                    Inches(0.7), Inches(2.3), Inches(5.4), Inches(4.5))
        elif isinstance(before_content, list):
            self._add_bullet_list(slide, before_content,
                                   Inches(0.7), Inches(2.3), Inches(5.4), Inches(4.5))
        else:
            self._add_text(slide, str(before_content), Inches(0.7), Inches(2.3),
                           Inches(5.4), Inches(4.5), font_size=13, color=Colors.DARK_GRAY)

        # Arrow divider
        arrow = slide.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW, Inches(6.35), Inches(4.0),
            Inches(0.65), Inches(0.5)
        )
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = Colors.BRAND_BLUE
        arrow.line.fill.background()

        # AFTER panel
        # Header bar
        self._add_shape(slide, Inches(7.1), Inches(1.6), Inches(5.8), Inches(0.5),
                        Colors.BRAND_BLUE)
        self._add_text(slide, after_title, Inches(7.3), Inches(1.63),
                       Inches(5.4), Inches(0.45),
                       font_size=14, bold=True, color=Colors.WHITE)

        # After content area
        after_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(2.15),
            Inches(5.8), Inches(4.8)
        )
        after_card.fill.solid()
        after_card.fill.fore_color.rgb = RGBColor(0xE8, 0xF5, 0xE9)
        after_card.line.color.rgb = Colors.BRAND_BLUE
        after_card.line.width = Pt(2)

        if after_image and Path(after_image).exists():
            self._add_scaled_image(slide, after_image,
                                    Inches(7.3), Inches(2.3), Inches(5.4), Inches(4.5))
        elif isinstance(after_content, list):
            self._add_bullet_list(slide, after_content,
                                   Inches(7.3), Inches(2.3), Inches(5.4), Inches(4.5))
        else:
            self._add_text(slide, str(after_content), Inches(7.3), Inches(2.3),
                           Inches(5.4), Inches(4.5), font_size=13, color=Colors.DARK_GRAY)

        return slide

    def add_stat_slide(self, title, stat_value, stat_label, context=""):
        """Large single statistic highlight slide."""
        slide = self._blank_slide()
        self._fill_background(slide, Colors.DARK_NAVY)

        # Title
        self._add_text(slide, title, Inches(1.5), Inches(1.0), Inches(10), Inches(0.8),
                       font_size=20, color=Colors.TEAL)

        # Large stat value
        self._add_text(slide, str(stat_value), Inches(1.5), Inches(2.3), Inches(10), Inches(2.5),
                       font_size=96, bold=True, color=Colors.WHITE,
                       alignment=PP_ALIGN.CENTER)

        # Stat label
        self._add_text(slide, stat_label, Inches(1.5), Inches(4.8), Inches(10), Inches(0.8),
                       font_size=22, color=Colors.BRAND_BLUE,
                       alignment=PP_ALIGN.CENTER)

        # Context
        if context:
            self._add_text(slide, context, Inches(2), Inches(5.8), Inches(9), Inches(1),
                           font_size=14, color=Colors.MID_GRAY,
                           alignment=PP_ALIGN.CENTER)

        return slide

    def add_process_flow_slide(self, title, steps):
        """
        Horizontal process flow slide with connected steps.
        steps: list of dicts with 'name', optional 'description', optional 'color'
        """
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        num_steps = len(steps)
        step_width = Inches(min(2.2, 10.5 / num_steps))
        gap = Inches(0.6)
        total_width = step_width * num_steps + gap * (num_steps - 1)
        start_left = (self.slide_width - total_width) // 2
        center_y = Inches(3.0)

        for i, step in enumerate(steps):
            left = start_left + (step_width + gap) * i
            color = step.get('color', Colors.BRAND_BLUE)

            # Step circle with number
            circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, left + step_width // 2 - Inches(0.35),
                center_y, Inches(0.7), Inches(0.7)
            )
            circle.fill.solid()
            circle.fill.fore_color.rgb = color
            circle.line.fill.background()
            circle.text_frame.text = str(i + 1)
            for p in circle.text_frame.paragraphs:
                p.font.size = Pt(16)
                p.font.bold = True
                p.font.color.rgb = Colors.WHITE
                p.alignment = PP_ALIGN.CENTER

            # Step name
            self._add_text(slide, step['name'], left, center_y + Inches(0.9),
                           step_width, Inches(0.6),
                           font_size=13, bold=True, color=Colors.DARK_GRAY,
                           alignment=PP_ALIGN.CENTER)

            # Description
            if step.get('description'):
                self._add_text(slide, step['description'], left, center_y + Inches(1.5),
                               step_width, Inches(1.5),
                               font_size=10, color=Colors.MID_GRAY,
                               alignment=PP_ALIGN.CENTER)

            # Arrow to next step
            if i < num_steps - 1:
                arrow_left = left + step_width
                arrow = slide.shapes.add_shape(
                    MSO_SHAPE.RIGHT_ARROW,
                    arrow_left + Inches(0.05), center_y + Inches(0.2),
                    gap - Inches(0.1), Inches(0.3)
                )
                arrow.fill.solid()
                arrow.fill.fore_color.rgb = Colors.MID_GRAY
                arrow.line.fill.background()

        return slide

    def add_icon_grid_slide(self, title, items):
        """
        Grid of capability icons with labels (2x3 or 3x3 layout).
        items: list of dicts with 'name', 'description', optional 'icon' (emoji/symbol)
        """
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        num_items = len(items)
        cols = 3 if num_items > 4 else 2
        rows = (num_items + cols - 1) // cols
        card_w = Inches(3.2)
        card_h = Inches(2.2)
        h_gap = Inches(0.5)
        v_gap = Inches(0.4)
        total_w = card_w * cols + h_gap * (cols - 1)
        start_left = (self.slide_width - total_w) // 2
        start_top = Inches(1.8)

        for idx, item in enumerate(items):
            row = idx // cols
            col = idx % cols
            left = start_left + (card_w + h_gap) * col
            top = start_top + (card_h + v_gap) * row

            # Card
            card = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_w, card_h
            )
            card.fill.solid()
            card.fill.fore_color.rgb = Colors.LIGHT_GRAY
            card.line.color.rgb = RGBColor(0xDE, 0xE2, 0xE6)
            card.line.width = Pt(1)

            # Icon/symbol
            icon = item.get('icon', '●')
            self._add_text(slide, icon, left + Inches(0.15), top + Inches(0.15),
                           card_w - Inches(0.3), Inches(0.6),
                           font_size=28, color=Colors.BRAND_BLUE,
                           alignment=PP_ALIGN.CENTER)

            # Name
            self._add_text(slide, item['name'], left + Inches(0.15), top + Inches(0.75),
                           card_w - Inches(0.3), Inches(0.5),
                           font_size=13, bold=True, color=Colors.DARK_GRAY,
                           alignment=PP_ALIGN.CENTER)

            # Description
            if item.get('description'):
                self._add_text(slide, item['description'],
                               left + Inches(0.15), top + Inches(1.25),
                               card_w - Inches(0.3), Inches(0.8),
                               font_size=10, color=Colors.MID_GRAY,
                               alignment=PP_ALIGN.CENTER)

        return slide

    def add_risk_matrix_slide(self, title, risks):
        """
        Risk matrix (probability vs impact grid) with plotted risks.
        risks: list of dicts with 'name', 'probability' (1-3), 'impact' (1-3), optional 'mitigation'
        """
        slide = self._blank_slide()

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        grid_left = Inches(2.5)
        grid_top = Inches(2.0)
        cell_w = Inches(2.2)
        cell_h = Inches(1.5)

        # Grid colors (probability x impact)
        grid_colors = {
            (1, 1): RGBColor(0xC8, 0xE6, 0xC9),  # green - low
            (1, 2): RGBColor(0xC8, 0xE6, 0xC9),
            (1, 3): RGBColor(0xFF, 0xF3, 0xE0),   # orange - medium
            (2, 1): RGBColor(0xC8, 0xE6, 0xC9),
            (2, 2): RGBColor(0xFF, 0xF3, 0xE0),
            (2, 3): RGBColor(0xFF, 0xCD, 0xD2),   # red - high
            (3, 1): RGBColor(0xFF, 0xF3, 0xE0),
            (3, 2): RGBColor(0xFF, 0xCD, 0xD2),
            (3, 3): RGBColor(0xFF, 0xCD, 0xD2),
        }

        # Draw grid
        for prob in range(3):
            for imp in range(3):
                x = grid_left + cell_w * imp
                y = grid_top + cell_h * (2 - prob)
                color = grid_colors.get((prob + 1, imp + 1), Colors.LIGHT_GRAY)
                cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, cell_w, cell_h)
                cell.fill.solid()
                cell.fill.fore_color.rgb = color
                cell.line.color.rgb = Colors.WHITE
                cell.line.width = Pt(2)

        # Axis labels
        self._add_text(slide, "IMPACT →", grid_left, grid_top + cell_h * 3 + Inches(0.1),
                       cell_w * 3, Inches(0.4), font_size=12, bold=True,
                       color=Colors.MID_GRAY, alignment=PP_ALIGN.CENTER)
        self._add_text(slide, "Low", grid_left, grid_top + cell_h * 3 + Inches(0.4),
                       cell_w, Inches(0.3), font_size=10, color=Colors.MID_GRAY,
                       alignment=PP_ALIGN.CENTER)
        self._add_text(slide, "Medium", grid_left + cell_w, grid_top + cell_h * 3 + Inches(0.4),
                       cell_w, Inches(0.3), font_size=10, color=Colors.MID_GRAY,
                       alignment=PP_ALIGN.CENTER)
        self._add_text(slide, "High", grid_left + cell_w * 2, grid_top + cell_h * 3 + Inches(0.4),
                       cell_w, Inches(0.3), font_size=10, color=Colors.MID_GRAY,
                       alignment=PP_ALIGN.CENTER)

        # Y-axis
        self._add_text(slide, "P\nR\nO\nB\nA\nB\nI\nL\nI\nT\nY",
                       grid_left - Inches(0.8), grid_top + Inches(0.5),
                       Inches(0.5), cell_h * 3 - Inches(1),
                       font_size=8, bold=True, color=Colors.MID_GRAY,
                       alignment=PP_ALIGN.CENTER)

        # Plot risks
        for risk in risks:
            prob = min(max(risk.get('probability', 1), 1), 3)
            imp = min(max(risk.get('impact', 1), 1), 3)
            x = grid_left + cell_w * (imp - 1) + Inches(0.2)
            y = grid_top + cell_h * (3 - prob) + Inches(0.2)

            # Risk marker
            marker = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, x, y, Inches(0.35), Inches(0.35)
            )
            marker.fill.solid()
            marker.fill.fore_color.rgb = Colors.DARK_NAVY
            marker.line.fill.background()

            # Risk label
            self._add_text(slide, risk['name'], x + Inches(0.45), y,
                           cell_w - Inches(0.8), Inches(0.35),
                           font_size=9, bold=True, color=Colors.DARK_GRAY)

        # Risk legend on right side
        if risks:
            legend_left = grid_left + cell_w * 3 + Inches(0.5)
            self._add_text(slide, "Risks:", legend_left, grid_top,
                           Inches(3), Inches(0.4), font_size=12, bold=True,
                           color=Colors.DARK_GRAY)
            for i, risk in enumerate(risks):
                y = grid_top + Inches(0.5) + Inches(i * 0.6)
                self._add_text(slide, f"• {risk['name']}", legend_left, y,
                               Inches(3), Inches(0.3), font_size=10,
                               color=Colors.DARK_GRAY)
                if risk.get('mitigation'):
                    self._add_text(slide, f"  ↳ {risk['mitigation']}",
                                   legend_left, y + Inches(0.25),
                                   Inches(3), Inches(0.3), font_size=8,
                                   color=Colors.MID_GRAY)

        return slide

    def add_next_steps_slide(self, title, action_items):
        """
        Action items / next steps slide.
        action_items: list of dicts with 'action', 'owner', 'date', optional 'status'
        """
        headers = ["#", "Action Item", "Owner", "Target Date", "Status"]
        rows = []
        for i, item in enumerate(action_items):
            status = item.get('status', 'Pending')
            rows.append([
                str(i + 1),
                item['action'],
                item.get('owner', 'TBD'),
                item.get('date', 'TBD'),
                status
            ])

        slide = self.add_table_slide(title, headers, rows,
                                      col_widths=[0.5, 5.5, 2.0, 1.8, 1.5])

        # Color-code the status column
        table = slide.shapes[-1].table if hasattr(slide.shapes[-1], 'table') else None
        if table:
            status_colors = {
                'Done': Colors.GREEN,
                'In Progress': Colors.ORANGE,
                'Pending': Colors.MID_GRAY,
                'Blocked': Colors.RED,
            }
            for row_idx, row_data in enumerate(rows):
                cell = table.cell(row_idx + 1, 4)
                for p in cell.text_frame.paragraphs:
                    color = status_colors.get(row_data[4], Colors.MID_GRAY)
                    p.font.color.rgb = color
                    p.font.bold = True

        return slide

    # ─── ADVANCED VISUAL SLIDE TYPES ───────────────────────

    def add_persona_callout_slide(self, title, persona_name, persona_role,
                                   story_bullets, call_to_action="",
                                   variant="pain"):
        """
        Persona story callout slide — the emotional anchor.
        variant: 'pain' (red/orange tones) or 'resolution' (green/blue tones)
        """
        slide = self._blank_slide()

        if variant == "resolution":
            bg_color = RGBColor(0xE8, 0xF5, 0xE9)
            accent_color = Colors.GREEN
            card_border = Colors.GREEN
            icon = "✨"
        else:
            bg_color = RGBColor(0xFF, 0xF8, 0xE1)
            accent_color = Colors.ORANGE
            card_border = Colors.ORANGE
            icon = "⚡"

        self._fill_background(slide, bg_color)

        # Top bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.1), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.2), Inches(11), Inches(0.7),
                       font_size=24, bold=True, color=Colors.WHITE)

        # Persona card with shadow effect
        shadow_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(1.35), Inches(1.55), Inches(10.7), Inches(5.35)
        )
        shadow_card.fill.solid()
        shadow_card.fill.fore_color.rgb = RGBColor(0xDE, 0xDE, 0xDE)
        shadow_card.line.fill.background()

        main_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(1.2), Inches(1.4), Inches(10.7), Inches(5.35)
        )
        main_card.fill.solid()
        main_card.fill.fore_color.rgb = Colors.WHITE
        main_card.line.color.rgb = card_border
        main_card.line.width = Pt(2.5)

        # Icon + persona header
        self._add_text(slide, icon, Inches(1.6), Inches(1.6), Inches(0.6), Inches(0.6),
                       font_size=28, alignment=PP_ALIGN.CENTER)
        self._add_text(slide, persona_name, Inches(2.3), Inches(1.6),
                       Inches(9), Inches(0.5),
                       font_size=22, bold=True, color=Colors.DARK_GRAY)
        self._add_text(slide, persona_role, Inches(2.3), Inches(2.1),
                       Inches(9), Inches(0.4),
                       font_size=14, color=accent_color, italic=True)

        # Accent line
        self._add_shape(slide, Inches(2.3), Inches(2.55), Inches(2), Inches(0.04), accent_color)

        # Story bullets
        bullet_top = Inches(2.8)
        for i, bullet in enumerate(story_bullets):
            self._add_text(slide, f"▸ {bullet}", Inches(2.3), bullet_top + Inches(i * 0.55),
                           Inches(9), Inches(0.5),
                           font_size=15, color=Colors.DARK_GRAY)

        # Call to action at bottom
        if call_to_action:
            cta_shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(2.3), Inches(5.9), Inches(8.5), Inches(0.6)
            )
            cta_shape.fill.solid()
            cta_shape.fill.fore_color.rgb = accent_color
            cta_shape.line.fill.background()

            self._add_text(slide, call_to_action, Inches(2.5), Inches(5.95),
                           Inches(8.2), Inches(0.5),
                           font_size=14, bold=True, color=Colors.WHITE,
                           alignment=PP_ALIGN.CENTER)

        return slide

    def add_chart_slide(self, title, chart_type, data, chart_title="",
                        x_label="", y_label=""):
        """
        Generate a matplotlib chart and embed it as an image.
        chart_type: 'bar', 'hbar', 'line', 'pie', 'stacked_bar'
        data: dict with 'labels', 'values' (list or list of lists for multi-series),
              optional 'series_names', 'colors'
        """
        if not HAS_MATPLOTLIB:
            return self.add_content_slide(title,
                ["[Chart could not be generated — matplotlib not installed]"])

        slide = self._blank_slide()
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        fig, ax = plt.subplots(figsize=(10, 5))
        labels = data.get('labels', [])
        values = data.get('values', [])
        series_names = data.get('series_names', [])
        colors = data.get('colors', [
            f'#{c.red:02x}{c.green:02x}{c.blue:02x}' for c in Colors.SERIES[:8]
        ])

        if chart_type == 'bar':
            if isinstance(values[0], (list, tuple)):
                x = range(len(labels))
                width = 0.8 / len(values)
                for i, series in enumerate(values):
                    offset = (i - len(values) / 2 + 0.5) * width
                    bars = ax.bar([xi + offset for xi in x], series, width,
                                  label=series_names[i] if i < len(series_names) else f'Series {i+1}',
                                  color=colors[i % len(colors)])
                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=30, ha='right')
                ax.legend()
            else:
                ax.bar(labels, values, color=colors[:len(labels)])
                ax.set_xticklabels(labels, rotation=30, ha='right')

        elif chart_type == 'hbar':
            ax.barh(labels, values, color=colors[:len(labels)])

        elif chart_type == 'line':
            if isinstance(values[0], (list, tuple)):
                for i, series in enumerate(values):
                    ax.plot(labels, series,
                            label=series_names[i] if i < len(series_names) else f'Series {i+1}',
                            color=colors[i % len(colors)], marker='o', linewidth=2)
                ax.legend()
            else:
                ax.plot(labels, values, color=colors[0], marker='o', linewidth=2)

        elif chart_type == 'pie':
            ax.pie(values, labels=labels, colors=colors[:len(labels)],
                   autopct='%1.0f%%', startangle=90, textprops={'fontsize': 10})

        elif chart_type == 'stacked_bar':
            x = range(len(labels))
            bottom = [0] * len(labels)
            for i, series in enumerate(values):
                ax.bar(x, series, bottom=bottom,
                       label=series_names[i] if i < len(series_names) else f'Series {i+1}',
                       color=colors[i % len(colors)])
                bottom = [b + s for b, s in zip(bottom, series)]
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=30, ha='right')
            ax.legend()

        if chart_title:
            ax.set_title(chart_title, fontsize=13, fontweight='bold', pad=12)
        if x_label:
            ax.set_xlabel(x_label)
        if y_label:
            ax.set_ylabel(y_label)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.tight_layout()

        # Save to temp file and embed
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            fig.savefig(tmp.name, dpi=200, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
            plt.close(fig)
            self._add_scaled_image(slide, tmp.name,
                                    Inches(1.5), Inches(1.6), Inches(10), Inches(5.2))
            Path(tmp.name).unlink(missing_ok=True)

        return slide

    def add_three_column_slide(self, title, columns):
        """
        Three-column layout for comparing approaches or showing phases.
        columns: list of 3 dicts with 'title', 'bullets', optional 'icon', 'color'
        """
        slide = self._blank_slide()
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        num_cols = min(len(columns), 4)
        col_width = Inches(10.5 / num_cols)
        start_left = Inches(1.2)

        for i, col in enumerate(columns[:num_cols]):
            left = start_left + col_width * i
            color = col.get('color', Colors.BRAND_BLUE)

            # Column header card
            header_shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left + Inches(0.1), Inches(1.6),
                col_width - Inches(0.3), Inches(0.6)
            )
            header_shape.fill.solid()
            header_shape.fill.fore_color.rgb = color
            header_shape.line.fill.background()

            header_text = col.get('icon', '') + ' ' + col['title'] if col.get('icon') else col['title']
            self._add_text(slide, header_text.strip(),
                           left + Inches(0.2), Inches(1.65),
                           col_width - Inches(0.5), Inches(0.5),
                           font_size=14, bold=True, color=Colors.WHITE,
                           alignment=PP_ALIGN.CENTER)

            # Content card
            content_card = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left + Inches(0.1), Inches(2.3),
                col_width - Inches(0.3), Inches(4.5)
            )
            content_card.fill.solid()
            content_card.fill.fore_color.rgb = Colors.LIGHT_GRAY
            content_card.line.color.rgb = color
            content_card.line.width = Pt(1.5)

            # Bullets
            self._add_bullet_list(slide, col.get('bullets', []),
                                   left + Inches(0.25), Inches(2.5),
                                   col_width - Inches(0.5), Inches(4.1))

        return slide

    def add_callout_banner_slide(self, title, main_text, sub_text="",
                                  banner_color=None):
        """Large centered callout for key messages, transitions, or decisions."""
        slide = self._blank_slide()
        color = banner_color or Colors.BRAND_BLUE
        self._fill_background(slide, Colors.DARK_NAVY)

        # Top accent bar
        self._add_shape(slide, 0, 0, self.slide_width, Inches(0.08), color)

        # Title
        self._add_text(slide, title, Inches(1.5), Inches(1.5), Inches(10), Inches(0.8),
                       font_size=18, color=Colors.MID_GRAY,
                       alignment=PP_ALIGN.CENTER)

        # Main message (large)
        self._add_text(slide, main_text, Inches(1.5), Inches(2.5), Inches(10), Inches(2.5),
                       font_size=36, bold=True, color=Colors.WHITE,
                       alignment=PP_ALIGN.CENTER)

        # Sub-text
        if sub_text:
            self._add_text(slide, sub_text, Inches(2), Inches(5.3), Inches(9), Inches(1),
                           font_size=16, color=color,
                           alignment=PP_ALIGN.CENTER)

        # Bottom accent bar
        self._add_shape(slide, 0, self.slide_height - Inches(0.08),
                        self.slide_width, Inches(0.08), color)

        return slide

    def add_slide_number(self, slide, number, total=None):
        """Add a slide number to the bottom-right corner."""
        text = f"{number}" if total is None else f"{number} / {total}"
        self._add_text(slide, text,
                       self.slide_width - Inches(1.5), self.slide_height - Inches(0.45),
                       Inches(1.2), Inches(0.3),
                       font_size=9, color=Colors.MID_GRAY,
                       alignment=PP_ALIGN.RIGHT)

    def add_slide_numbers_all(self, start=1):
        """Add slide numbers to all slides in the presentation."""
        total = len(self.prs.slides)
        for i, slide in enumerate(self.prs.slides):
            self.add_slide_number(slide, start + i, total)

    def add_logo(self, slide, logo_path, position="top-right", max_height=Inches(0.5)):
        """
        Add a logo image to a slide.
        position: 'top-right', 'top-left', 'bottom-right', 'bottom-left'
        """
        logo = Path(logo_path)
        if not logo.exists():
            return

        positions = {
            'top-right': (self.slide_width - Inches(2), Inches(0.15)),
            'top-left': (Inches(0.3), Inches(0.15)),
            'bottom-right': (self.slide_width - Inches(2), self.slide_height - Inches(0.6)),
            'bottom-left': (Inches(0.3), self.slide_height - Inches(0.6)),
        }
        left, top = positions.get(position, positions['top-right'])
        slide.shapes.add_picture(str(logo), left, top, height=max_height)

    def add_shadow_card(self, slide, left, top, width, height, color=None,
                        border_color=None):
        """Add a card shape with drop-shadow effect."""
        # Shadow
        shadow = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left + Inches(0.08), top + Inches(0.08), width, height
        )
        shadow.fill.solid()
        shadow.fill.fore_color.rgb = RGBColor(0xD0, 0xD0, 0xD0)
        shadow.line.fill.background()

        # Main card
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
        )
        card.fill.solid()
        card.fill.fore_color.rgb = color or Colors.WHITE
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
            card.line.width = Pt(1)

        return card

    def add_gradient_shape(self, slide, left, top, width, height,
                            color_start, color_end):
        """Add a shape with gradient fill."""
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
        )
        fill = shape.fill
        fill.gradient()
        fill.gradient_stops[0].color.rgb = color_start
        fill.gradient_stops[0].position = 0.0
        fill.gradient_stops[1].color.rgb = color_end
        fill.gradient_stops[1].position = 1.0
        shape.line.fill.background()
        return shape

    def add_donut_chart_slide(self, title, data, center_text="",
                               center_subtext=""):
        """
        Donut/ring chart slide using matplotlib.
        data: dict with 'labels' and 'values', optional 'colors'
        """
        if not HAS_MATPLOTLIB:
            return self.add_content_slide(title,
                ["[Donut chart unavailable — matplotlib not installed]"])

        slide = self._blank_slide()
        self._add_shape(slide, 0, 0, self.slide_width, Inches(1.3), Colors.DARK_NAVY)
        self._add_text(slide, title, Inches(0.8), Inches(0.25), Inches(11), Inches(0.9),
                       font_size=26, bold=True, color=Colors.WHITE)

        labels = data.get('labels', [])
        values = data.get('values', [])
        colors = data.get('colors', [
            f'#{c.red:02x}{c.green:02x}{c.blue:02x}' for c in Colors.SERIES[:len(values)]
        ])

        fig, ax = plt.subplots(figsize=(6, 5))
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, colors=colors,
            autopct='%1.0f%%', startangle=90,
            pctdistance=0.8, textprops={'fontsize': 10}
        )
        # Donut hole
        centre_circle = plt.Circle((0, 0), 0.55, fc='white')
        ax.add_artist(centre_circle)

        if center_text:
            ax.text(0, 0.05, center_text, ha='center', va='center',
                    fontsize=18, fontweight='bold', color='#212529')
        if center_subtext:
            ax.text(0, -0.15, center_subtext, ha='center', va='center',
                    fontsize=10, color='#6c757d')

        fig.tight_layout()

        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            fig.savefig(tmp.name, dpi=200, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
            plt.close(fig)
            self._add_scaled_image(slide, tmp.name,
                                    Inches(3.5), Inches(1.6), Inches(6), Inches(5.2))
            Path(tmp.name).unlink(missing_ok=True)

        return slide

    def add_metric_highlight_slide(self, title, metrics):
        """
        Row of large metric callouts with trend indicators.
        metrics: list of dicts with 'value', 'label', 'trend' (up/down/flat),
                 optional 'color', 'trend_text'
        """
        slide = self._blank_slide()
        self._fill_background(slide, Colors.DARK_NAVY)

        self._add_text(slide, title, Inches(0.8), Inches(0.8), Inches(11), Inches(0.7),
                       font_size=22, color=Colors.TEAL, alignment=PP_ALIGN.CENTER)

        num = len(metrics)
        card_w = Inches(min(3.0, 10.5 / num))
        total_w = card_w * num + Inches(0.4) * (num - 1)
        start_left = (self.slide_width - total_w) // 2

        trend_symbols = {'up': '▲', 'down': '▼', 'flat': '▸'}
        trend_colors = {
            'up': Colors.GREEN, 'down': Colors.RED, 'flat': Colors.MID_GRAY
        }

        for i, m in enumerate(metrics):
            left = start_left + (card_w + Inches(0.4)) * i
            top = Inches(2.0)
            color = m.get('color', Colors.BRAND_BLUE)

            # Card with gradient accent
            self.add_shadow_card(slide, left, top, card_w, Inches(4.0),
                                 color=Colors.LIGHT_NAVY, border_color=color)

            # Color accent bar at top
            self._add_shape(slide, left + Inches(0.1), top + Inches(0.1),
                            card_w - Inches(0.2), Inches(0.06), color)

            # Large value
            self._add_text(slide, str(m['value']),
                           left + Inches(0.2), top + Inches(0.5),
                           card_w - Inches(0.4), Inches(1.5),
                           font_size=42, bold=True, color=Colors.WHITE,
                           alignment=PP_ALIGN.CENTER)

            # Label
            self._add_text(slide, m['label'],
                           left + Inches(0.2), top + Inches(2.0),
                           card_w - Inches(0.4), Inches(0.8),
                           font_size=12, color=Colors.MID_GRAY,
                           alignment=PP_ALIGN.CENTER)

            # Trend indicator
            trend = m.get('trend', 'flat')
            trend_text = m.get('trend_text', '')
            t_color = trend_colors.get(trend, Colors.MID_GRAY)
            symbol = trend_symbols.get(trend, '▸')
            display = f"{symbol} {trend_text}" if trend_text else symbol
            self._add_text(slide, display,
                           left + Inches(0.2), top + Inches(3.0),
                           card_w - Inches(0.4), Inches(0.5),
                           font_size=13, bold=True, color=t_color,
                           alignment=PP_ALIGN.CENTER)

        return slide

    # ─── PRIVATE HELPERS ───────────────────────────────────

    def _blank_slide(self):
        return self.prs.slides.add_slide(self.prs.slide_layouts[6])

    def _fill_background(self, slide, color):
        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = color

    def _fill_gradient(self, slide, color_start, color_end, angle=270):
        """Fill slide background with a gradient."""
        bg = slide.background.fill
        bg.gradient()
        bg.gradient_stops[0].color.rgb = color_start
        bg.gradient_stops[0].position = 0.0
        bg.gradient_stops[1].color.rgb = color_end
        bg.gradient_stops[1].position = 1.0

    def _add_shape(self, slide, left, top, width, height, color):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        return shape

    def _add_scaled_image(self, slide, image_path, left, top, max_width, max_height):
        """Add an image scaled proportionally to fit within max bounds."""
        img_path = Path(image_path)
        if not img_path.exists():
            return None

        if HAS_PIL:
            with PILImage.open(str(img_path)) as img:
                img_w, img_h = img.size
            aspect = img_w / img_h

            # Calculate scaled dimensions
            width = max_width
            height = int(width / aspect) if aspect > 0 else max_height

            if height > max_height:
                height = max_height
                width = int(height * aspect)

            # Center within the available space
            x_offset = left + (max_width - width) // 2
            y_offset = top + (max_height - height) // 2

            return slide.shapes.add_picture(str(img_path), x_offset, y_offset,
                                             width=width, height=height)
        else:
            # Fallback: use max_width only (no aspect ratio correction)
            return slide.shapes.add_picture(str(img_path), left, top, width=max_width)

    def _add_text(self, slide, text, left, top, width, height,
                  font_size=18, bold=False, italic=False,
                  color=Colors.DARK_GRAY, alignment=PP_ALIGN.LEFT):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.italic = italic
        p.font.color.rgb = color
        p.alignment = alignment
        return txBox

    def _add_bullet_list(self, slide, bullets, left, top, width, height):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, bullet in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = f"• {bullet.strip().lstrip('•-▸ ')}"
            p.font.size = Pt(15)
            p.font.color.rgb = Colors.DARK_GRAY
            p.space_after = Pt(8)
        return txBox
