#!/usr/bin/env python3
"""Convert a PM step markdown file to a readable standalone HTML sibling.

Usage:
  python md_to_html.py <input.md> [output.html]

If output is omitted, writes <input>.html next to the markdown file.
Prefers the `markdown` package when installed; otherwise uses a small
built-in converter good enough for PM step drafts (headings, lists,
tables, code fences, blockquotes, bold/italic, links).
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path


CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.55;
  max-width: 920px;
  margin: 0 auto;
  padding: 32px 24px 64px;
  color: #1f2937;
  background: #f8fafc;
}
main {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 32px 36px;
  box-shadow: 0 1px 2px rgba(0,0,0,.04);
}
.banner {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 16px;
}
h1, h2, h3, h4 { color: #0f172a; line-height: 1.25; }
h1 { font-size: 1.85rem; margin-top: 0; border-bottom: 2px solid #e2e8f0; padding-bottom: .4em; }
h2 { font-size: 1.35rem; margin-top: 1.6em; border-bottom: 1px solid #eef2f7; padding-bottom: .3em; }
h3 { font-size: 1.1rem; margin-top: 1.3em; }
h4 { font-size: 1rem; margin-top: 1.1em; }
p, li { font-size: 15px; }
a { color: #2563eb; }
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: #f1f5f9;
  padding: .1em .35em;
  border-radius: 4px;
  font-size: .92em;
}
pre {
  background: #0f172a;
  color: #e2e8f0;
  padding: 14px 16px;
  border-radius: 8px;
  overflow-x: auto;
}
pre code { background: transparent; color: inherit; padding: 0; }
blockquote {
  margin: 1em 0;
  padding: .6em 1em;
  border-left: 4px solid #3b82f6;
  background: #eff6ff;
  color: #1e3a8a;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  font-size: 14px;
}
th, td {
  border: 1px solid #e5e7eb;
  padding: 8px 10px;
  text-align: left;
  vertical-align: top;
}
th { background: #f1f5f9; font-weight: 600; }
tr:nth-child(even) td { background: #fafafa; }
hr { border: 0; border-top: 1px solid #e5e7eb; margin: 2em 0; }
ul, ol { padding-left: 1.4em; }
.footer {
  margin-top: 28px;
  font-size: 12px;
  color: #94a3b8;
}
"""


def _inline(text: str) -> str:
    """Escape then apply a small set of inline markdown transforms."""
    s = html.escape(text)
    # code
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    # links [text](url)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" rel="noopener noreferrer">\1</a>',
        s,
    )
    # bold ** ** or __ __
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"__(.+?)__", r"<strong>\1</strong>", s)
    # italic * * or _ _
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", r"<em>\1</em>", s)
    return s


def _convert_builtin(md: str) -> str:
    lines = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    i = 0
    in_ul = in_ol = in_blockquote = False
    in_table = False
    table_rows: list[list[str]] = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def close_bq() -> None:
        nonlocal in_blockquote
        if in_blockquote:
            out.append("</blockquote>")
            in_blockquote = False

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        if table_rows:
            out.append("<table>")
            for ridx, row in enumerate(table_rows):
                tag = "th" if ridx == 0 else "td"
                # skip separator row like ---|---
                if ridx == 1 and all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in row):
                    continue
                out.append("<tr>" + "".join(f"<{tag}>{_inline(c.strip())}</{tag}>" for c in row) + "</tr>")
            out.append("</table>")
        table_rows = []
        in_table = False

    while i < len(lines):
        line = lines[i]

        # fenced code
        if line.strip().startswith("```"):
            close_lists()
            close_bq()
            flush_table()
            lang = line.strip()[3:].strip()
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # closing fence
            code = html.escape("\n".join(code_lines))
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{code}</code></pre>")
            continue

        # blank
        if not line.strip():
            close_lists()
            close_bq()
            flush_table()
            i += 1
            continue

        # table row
        if "|" in line and re.match(r"^\s*\|?.+\|", line):
            close_lists()
            close_bq()
            cells = [c for c in line.strip().strip("|").split("|")]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            i += 1
            continue
        else:
            flush_table()

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_lists()
            close_bq()
            level = len(m.group(1))
            out.append(f"<h{level}>{_inline(m.group(2).strip())}</h{level}>")
            i += 1
            continue

        # hr
        if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", line):
            close_lists()
            close_bq()
            out.append("<hr>")
            i += 1
            continue

        # blockquote
        if line.lstrip().startswith(">"):
            close_lists()
            content = re.sub(r"^\s*>\s?", "", line)
            if not in_blockquote:
                out.append("<blockquote>")
                in_blockquote = True
            out.append(f"<p>{_inline(content)}</p>")
            i += 1
            continue
        else:
            close_bq()

        # unordered list
        m = re.match(r"^\s*[-*+]\s+(.*)$", line)
        if m:
            close_bq()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{_inline(m.group(1))}</li>")
            i += 1
            continue

        # ordered list
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            close_bq()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{_inline(m.group(1))}</li>")
            i += 1
            continue

        # paragraph (merge continuation lines lightly)
        close_lists()
        close_bq()
        para = [line.strip()]
        j = i + 1
        while j < len(lines):
            nxt = lines[j]
            if (
                not nxt.strip()
                or nxt.strip().startswith("```")
                or re.match(r"^#{1,6}\s+", nxt)
                or re.match(r"^\s*[-*+]\s+", nxt)
                or re.match(r"^\s*\d+\.\s+", nxt)
                or nxt.lstrip().startswith(">")
                or ("|" in nxt and re.match(r"^\s*\|?.+\|", nxt))
            ):
                break
            para.append(nxt.strip())
            j += 1
        out.append(f"<p>{_inline(' '.join(para))}</p>")
        i = j

    close_lists()
    close_bq()
    flush_table()
    return "\n".join(out)


def md_to_body_html(md: str) -> str:
    try:
        import markdown  # type: ignore

        return markdown.markdown(
            md,
            extensions=["tables", "fenced_code", "sane_lists", "nl2br", "toc"],
            output_format="html5",
        )
    except Exception:
        return _convert_builtin(md)


def render_document(md_text: str, title: str, source_name: str) -> str:
    body = md_to_body_html(md_text)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="banner">ITOM PM draft · source: {html.escape(source_name)} · auto-generated for review</div>
  <main>
{body}
  </main>
  <div class="footer">Generated by scripts/ITOM-PM/md_to_html.py — markdown remains the source of truth.</div>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    src = Path(argv[1]).expanduser().resolve()
    if not src.is_file():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 1

    if len(argv) >= 3:
        dst = Path(argv[2]).expanduser().resolve()
    else:
        dst = src.with_suffix(".html")

    md_text = src.read_text(encoding="utf-8")
    # Title: first ATX H1 or filename
    title_match = re.search(r"^#\s+(.+)$", md_text, re.M)
    title = title_match.group(1).strip() if title_match else src.stem

    html_doc = render_document(md_text, title=title, source_name=src.name)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html_doc, encoding="utf-8")
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
