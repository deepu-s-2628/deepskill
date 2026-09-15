---
"deepskill": patch
---

Fixed `ask-deepu` and the whole pipeline being unusable outside a checkout of this repo. `npx skills add` installs each skill as an independent, flattened package with no `context/`/`scripts/` alongside it, so a PM running `/ask-deepu` from a real project folder hit a hard failure looking for files that were never installed. Added a native Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) so `/plugin install deepskill@deepskill` brings the whole repo tree along as one unit, and rewrote every internal reference to `context/`, `scripts/`, and the vendored Archify/frontend-slides/unlazy-gates tools to resolve via `${CLAUDE_PLUGIN_ROOT}` instead of a repo-relative path — works identically whether this is a real plugin install or a local checkout. Python dependency bootstrap (`uv sync`) is now automatic on first use instead of a manual PM-facing step.
