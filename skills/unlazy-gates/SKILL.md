---
name: unlazy-gates
description: "Mechanically-verified completion gates for a single pipeline step. Vendored, Solo-mode-only adaptation of unlazy — write GATES.md, run gate-check.mjs, self-correct or document the gap, never pause the run."
license: MIT
metadata:
  source: "unlazy v2.1.0 by Leonxlnx, MIT-licensed (see vendored LICENSE) — no public repository URL was discoverable in the local install; its own README states it is not identified there as a tagged GitHub release"
  vendored_from: Solo mode only
---

# unlazy-gates

Curated from `unlazy` (v2.1.0, MIT, Copyright (c) 2026 Leonxlnx — see the vendored `LICENSE`; no public repository URL was discoverable in the local install) — **Solo mode only**, adapted for this repo's own resolution rule. Not a full copy: `unlazy`'s Depth Tree, `PLAN.md`, orchestrated/parallel dispatch machinery (`references/method.md`, `orchestration.md`, `dispatch.md`, `parallel.md`), and the optional Claude Code Stop hook (`scripts/install-hooks.mjs`) are all deliberately excluded. None of that applies here: every pipeline run in `deepskill` is a single continuous agent session running its steps sequentially, never split across parallel leaves or orchestrated dispatch — Solo is the only mode this repo ever needs. The Stop hook specifically must never be installed for this pipeline; see "Resolution rule" below for why.

## What's vendored

- `scripts/gate-check.mjs`, `scripts/gate-lint.mjs`, and their `scripts/lib/` dependencies (`gates.mjs`, `check-supervisor.mjs`, `process-tree.mjs`, `dispatch.mjs`, `regex-worker.mjs` — `gate-check.mjs` imports `dispatch.mjs` internally even for non-orchestrated runs, so it's included as a real dependency, not orchestration content in its own right). Pure Node.js, zero npm dependencies — confirmed by running both scripts standalone against a hand-written `GATES.md` before vendoring.
- `templates/gates-leaf.md` — this repo's own Solo-only template (below), simplified from `unlazy`'s original: no `OWNS`/`CWD` fields, since those coordinate concurrent writers across parallel leaves, which never happens here.
- `references/gates.md` — the full gate-format and authoring-rules reference, unmodified.

## Write gates before the step's real work

Create `.steps/GATES-N.md` (where `N` is the step number, e.g. `GATES-3.md` for Step 3) from `templates/gates-leaf.md` before producing that step's content. One observable outcome per gate. A **runnable** gate gets an indented `CHECK:` and `EXPECT:`; use a **manual** gate only when no command can decide the outcome (`unlazy`'s own rule, kept as-is — see `references/gates.md`).

Check status without executing anything:
```bash
node <path-to>/skills/unlazy-gates/scripts/gate-check.mjs --status .steps/GATES-N.md
```

Approve and run (first time only — subsequent identical checks reuse the approval, bound to the exact `CHECK:`/`EXPECT:`/`CWD:`/shell/`PATH`, stored under `~/.unlazy/approved`):
```bash
node <path-to>/skills/unlazy-gates/scripts/gate-check.mjs --approve .steps/GATES-N.md
```

Lint before running, so an oracle that can't fail is caught at authoring time:
```bash
node <path-to>/skills/unlazy-gates/scripts/gate-lint.mjs .steps/GATES-N.md
```

## Resolution rule — this repo's own addition, not `unlazy`'s native behavior

`unlazy`'s native behavior for an unsatisfiable gate is `ABANDON: <id> <reason>`, which makes the checker exit `1` with `HANDOFF REQUIRED` — a stop signal, built for a human-supervised session. **`deepskill`'s pipeline never pauses except at its two sanctioned checkpoints** (wayfinding, and the Step 6 opt-in choice — see `$CLAUDE_PLUGIN_ROOT/context/pm-operating-system.md` §8). A quality gate is neither of those, so `ABANDON`/handoff semantics are never used here. Instead:

1. Produce the step's content, then run its gates (`--approve` the first time; `--status`/re-run on later checks).
2. **A failing runnable gate**: revise the specific failing content (e.g. a persona-count gate short by one → add another persona story) and re-check. Bound this to **2–3 retries** — a gate that still fails after that is either malformed or the content genuinely can't meet it; either way, looping forever is worse than moving on.
3. **Still unmet after retries**: do not abandon, do not stop the run. Document the specific gap in that step's own `.steps/*.md` output — the same pattern `current-state-analysis/SKILL.md` already uses for an unavailable screenshot: state the gap as a plain assumption/limitation, then continue. Never leave it silently unmentioned.
4. **Manual gates** stay self-attested, exactly as today's Quality Gate checklists already are — `unlazy-gates` gives them the same explicit, single-outcome structure as runnable gates, not script verification.

Never install `scripts/install-hooks.mjs`'s Stop hook for this repo — it exists specifically to block a session on unmet gates, which directly contradicts the never-pause contract above.

## Solo template

```markdown
# Gates: <step name>

Scope: <one sentence — the complete deliverable this step produces>

- [ ] G1: <observable outcome measured directly from the step's own output>
  CHECK: node scripts/verify-outcome.mjs
  EXPECT: outcome verification passed
  EVIDENCE: pending

- [ ] G2: <manual outcome that no command can decide>
  EVIDENCE: pending
```

Full authoring rules — unique gate ids, `CHECK:`/`EXPECT:` indentation, negative-assertion controls, measuring figures independently rather than copying a supplied number into `EXPECT:` — are in `references/gates.md`, unmodified from `unlazy`'s own.
