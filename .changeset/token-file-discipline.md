---
"deepskill": minor
---

Token/file-discipline pass, grilled and verified before implementing (not just a size cleanup):

**Fixed a real correctness bug found along the way.** `deliverables/SKILL.md` and `enhancement-deliverables/SKILL.md` still instructed the model to design slides around `python-pptx`/`PresentationBuilder` method names (`add_kpi_slide()`, `add_icon_grid_slide()`, etc.) from `generate_pptx.py` — deleted two releases ago when this pipeline moved to frontend-slides. This almost certainly contributed to the earlier "slides are too thin" feedback: the design-notes sections were still steering toward a rigid PPTX function-call model instead of genuine frontend-slides authoring. Rewrote both files' layout-variety guidance in the same content-shape vocabulary `generate-documents`/`enhancement-generate-documents` already use (two-column, comparison matrix, icon grid, KPI cards, before/after panels — described as layouts, not API calls). Also fixed a second bug found in the same pass: existing/new/modified color-coding (an enhancement-only concept) had leaked into the *feature* pipeline's engineering-deck instructions via copy-paste — removed, since a net-new feature has nothing "existing" to color-code against.

**Deduped the "Report rebuild" boilerplate.** The same ~19-line procedure was copy-pasted verbatim across all 14 pipeline skills (~266 lines of pure redundancy), duplicating what `pm-operating-system.md` §6 already documents once — and which every step already loads as mandatory context regardless. Replaced with a one-paragraph pointer in each file.

**Verified the two largest files (`deliverables`, `enhancement-deliverables`, the two biggest `SKILL.md` files installed on this machine) should NOT be split into on-demand references.** Confirmed their four deliverable templates (5a-5d) are unconditionally read in the same Step 5 pass with no cross-template dependencies — splitting a file whose every branch always fires adds tool-call overhead with no token savings (the opposite of what progressive disclosure is for). Left whole; fixed the real defects inside them instead.

**Added `pm-operating-system.md` §17** codifying this as a standing authoring convention for future skills: don't duplicate what's already mandatory context, only split content that's genuinely conditional, scope directory reads narrowly (matching Archify's own `SKILL.md` discipline), and verify a referenced file/method/format still exists rather than trusting prose that merely reads plausibly.
