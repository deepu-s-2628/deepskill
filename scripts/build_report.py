#!/usr/bin/env python3
"""Assemble one navigable HTML report from a PM pipeline run's hidden step markdown.

Usage:
  python build_report.py <topic-folder>

The topic folder (e.g. `vxlan-monitoring/` or `vxlan-monitoring-enhancement/`)
lives directly in the workspace — there is no wrapper folder around it.

Reads every <topic-folder>/.steps/*.md in filename order (0_wayfinding.md
first, then 1_..., 2_..., etc.), converts each to HTML, and writes a single
<topic-folder>/analysis.html with a sidebar table of contents (nested to each
step's own subsections, with scroll-position highlighting) and one anchored
section per step. `analysis.html` is a fixed name — the same file name in
every topic folder, same idea as `README.md` — so it's always obvious which
file to open first, next to `Progress.md`, `architecture.html`, the two slide
decks, and `product-requirements.docx`.

A step's markdown can embed a diagram — typically an Archify-rendered HTML
file that also exists as its own visible deliverable in the topic folder,
e.g. `architecture.html` — by putting a marker line on its own:

  <!-- diagram: architecture.html -->

Each marker becomes an <iframe> at that point in the section, sized to fit
the diagram's own viewport. Paths in the marker are relative to the topic
folder.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from md_to_html import md_to_body_html

CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  color: #1f2937;
  background: #f8fafc;
  display: flex;
  min-height: 100vh;
}
nav {
  width: 280px;
  flex: 0 0 280px;
  background: #0f172a;
  color: #e2e8f0;
  padding: 24px 16px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
nav .title { font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 4px; }
nav .subtitle { font-size: 12px; color: #94a3b8; margin-bottom: 20px; }
nav a {
  display: block;
  color: #cbd5e1;
  text-decoration: none;
  font-size: 13px;
  padding: 7px 10px;
  border-radius: 6px;
  margin-bottom: 2px;
}
nav a:hover { background: #1e293b; color: #fff; }
nav a.active { background: #1d4ed8; color: #fff; font-weight: 600; }
nav .subnav { margin: 0 0 4px 10px; border-left: 1px solid #334155; }
nav .subnav a { font-size: 12px; padding: 5px 10px; color: #94a3b8; }
nav .subnav a.active { background: #1e3a8a; color: #fff; font-weight: 500; }
main { flex: 1; padding: 40px 56px 96px; max-width: 1400px; }
section { margin-bottom: 56px; padding-top: 8px; border-top: 1px solid #e2e8f0; }
section:first-of-type { border-top: none; }
h1, h2, h3, h4 { color: #0f172a; line-height: 1.25; }
h1 { font-size: 1.7rem; }
h2 { font-size: 1.3rem; margin-top: 1.4em; }
h3 { font-size: 1.05rem; }
p, li { font-size: 15px; line-height: 1.6; }
a { color: #2563eb; }
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: #f1f5f9;
  padding: .1em .35em;
  border-radius: 4px;
  font-size: .92em;
}
pre { background: #0f172a; color: #e2e8f0; padding: 14px 16px; border-radius: 8px; overflow-x: auto; }
pre code { background: transparent; color: inherit; padding: 0; }
blockquote { margin: 1em 0; padding: .6em 1em; border-left: 4px solid #3b82f6; background: #eff6ff; color: #1e3a8a; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 14px; }
th, td { border: 1px solid #e5e7eb; padding: 8px 10px; text-align: left; vertical-align: top; }
th { background: #f1f5f9; font-weight: 600; }
tr:nth-child(even) td { background: #fafafa; }
.diagram-frame {
  width: 100%;
  height: 640px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  margin: 1.2em 0;
}
.banner { font-size: 12px; color: #94a3b8; margin-bottom: 8px; }
"""

# Highlights whichever nav link (top-level or nested) points at the section
# currently nearest the top of the viewport. Plain scroll listener rather than
# IntersectionObserver thresholds, since sections/subsections vary wildly in
# height and a simple "closest heading above the fold" rule is more robust
# than tuning intersection ratios per element.
SCROLLSPY_JS = """
<script>
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('nav a[href^="#"]'));
  var targets = links
    .map(function (a) {
      var el = document.getElementById(a.getAttribute('href').slice(1));
      return el ? { link: a, el: el } : null;
    })
    .filter(Boolean);

  function onScroll() {
    var current = null;
    for (var i = 0; i < targets.length; i++) {
      if (targets[i].el.getBoundingClientRect().top - 96 <= 0) {
        current = targets[i];
      } else {
        break;
      }
    }
    links.forEach(function (a) { a.classList.remove('active'); });
    if (current) current.link.classList.add('active');
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();
</script>
"""

DIAGRAM_MARKER = re.compile(r"^\s*<!--\s*diagram:\s*(.+?)\s*-->\s*$", re.M)
H2_TAG = re.compile(r'<h2(?:\s+id="([^"]*)")?[^>]*>(.*?)</h2>', re.I | re.S)

# Display titles for known step slugs, in case a file's H1 is missing/generic.
STEP_TITLES = {
    "0_wayfinding": "Scope & Requirements",
    "1_brainstorm": "Step 1 — Brainstorm",
    "1_current_state": "Step 1 — Current State Analysis",
    "2_competitive_analysis": "Step 2 — Competitive Analysis",
    "2_cross_module_analysis": "Step 2 — Cross-Module Analysis",
    "3_technical_analysis": "Step 3 — Technical Analysis",
    "3_competitive_analysis": "Step 3 — Competitive Analysis",
    "4_feature_definition": "Step 4 — Feature Definition",
    "4_enhancement_findings": "Step 4 — Enhancement Findings",
    "6_lovable_wireframe": "Step 6 — Lovable Wireframe Prompt",
}


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", text.lower()).strip("-") or "section"


def _title_for(stem: str, md_text: str) -> str:
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    if m:
        return m.group(1).strip()
    return STEP_TITLES.get(stem, stem.replace("_", " ").title())


def _tag_text(raw_inner_html: str) -> str:
    return re.sub(r"<[^>]+>", "", raw_inner_html).strip()


def build_section(md_path: Path, result_dir: Path) -> tuple[str, str, str, list[tuple[str, str]]]:
    """Returns (anchor_id, nav_title, section_html, subheadings)."""
    stem = md_path.stem
    md_text = md_path.read_text(encoding="utf-8")
    title = _title_for(stem, md_text)
    anchor = _slugify(stem)

    # Replace diagram markers with a unique inline token *before* markdown
    # conversion, so we can safely swap it for a real <iframe> afterward
    # without depending on how the markdown renderer treats HTML comments.
    diagrams: list[str] = []

    def _stash(match: re.Match[str]) -> str:
        diagrams.append(match.group(1))
        return f"\n\n%%DIAGRAM_{len(diagrams) - 1}%%\n\n"

    md_text_stashed = DIAGRAM_MARKER.sub(_stash, md_text)
    body = md_to_body_html(md_text_stashed)

    for i, rel_path in enumerate(diagrams):
        diagram_path = (result_dir / rel_path).resolve()
        if diagram_path.is_file():
            frame = f'<iframe class="diagram-frame" src="{html.escape(rel_path)}" loading="lazy"></iframe>'
        else:
            frame = f'<p style="color:#b91c1c">Missing diagram: {html.escape(rel_path)}</p>'
        body = re.sub(rf"<p>%%DIAGRAM_{i}%%</p>", frame, body)

    # Assign our own ids to every H2 (overriding any the markdown renderer's
    # "toc" extension already added) so section + subheading anchors follow
    # one consistent scheme regardless of whether the `markdown` package is
    # installed — the builtin fallback converter never adds ids at all.
    subheadings: list[tuple[str, str]] = []
    seen: set[str] = set()

    def _tag_h2(match: re.Match[str]) -> str:
        text = _tag_text(match.group(2))
        base = f"{anchor}--{_slugify(text)}"
        sub_id = base
        n = 2
        while sub_id in seen:
            sub_id = f"{base}-{n}"
            n += 1
        seen.add(sub_id)
        subheadings.append((sub_id, text))
        return f'<h2 id="{sub_id}">{match.group(2)}</h2>'

    body = H2_TAG.sub(_tag_h2, body)

    section_html = f'<section id="{anchor}">\n{body}\n</section>'
    return anchor, title, section_html, subheadings


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    result_dir = Path(argv[1]).expanduser().resolve()
    if not result_dir.is_dir():
        print(f"error: no such topic folder: {result_dir}", file=sys.stderr)
        return 1
    steps_dir = result_dir / ".steps"
    if not steps_dir.is_dir():
        print(f"error: no .steps/ under {result_dir}", file=sys.stderr)
        return 1

    md_files = sorted(steps_dir.glob("*.md"))
    if not md_files:
        print(f"error: no step markdown found in {steps_dir}", file=sys.stderr)
        return 1

    nav_items: list[str] = []
    sections: list[str] = []
    for md_path in md_files:
        anchor, title, section_html, subheadings = build_section(md_path, result_dir)
        nav_items.append(f'<a href="#{anchor}">{html.escape(title)}</a>')
        if subheadings:
            sub_links = "\n".join(
                f'<a href="#{sub_id}">{html.escape(sub_title)}</a>' for sub_id, sub_title in subheadings
            )
            nav_items.append(f'<div class="subnav">{sub_links}</div>')
        sections.append(section_html)

    slug = result_dir.name
    feature_name = slug.replace("-enhancement", "").replace("-", " ").title()

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(feature_name)} — ITOM PM Analysis</title>
  <style>{CSS}</style>
</head>
<body>
  <nav>
    <div class="title">{html.escape(feature_name)}</div>
    <div class="subtitle">ITOM PM pipeline analysis</div>
    {chr(10).join(nav_items)}
  </nav>
  <main>
    <div class="banner">Generated by scripts/build_report.py from .steps/*.md — that markdown remains the source of truth.</div>
    {chr(10).join(sections)}
  </main>
  {SCROLLSPY_JS}
</body>
</html>
"""

    out_path = result_dir / "analysis.html"
    out_path.write_text(doc, encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
