# Gates: <step name>

Scope: <one sentence — the complete deliverable this step produces>

- [ ] G1: <observable outcome measured directly from the step's own output>
  CHECK: node scripts/verify-outcome.mjs
  EXPECT: outcome verification passed
  EVIDENCE: pending

- [ ] G2: <manual outcome that no command can decide>
  EVIDENCE: pending

<!--
Simplified from unlazy's own gates-leaf.md for this repo's Solo-only use:
no OWNS or CWD fields — those coordinate concurrent writers across parallel
leaves, which never happens in this pipeline (one continuous session, steps
run sequentially). Full authoring rules are in ../references/gates.md.

Strict format:
- Use a unique explicit id for every gate.
- Indent CHECK, EXPECT, and EVIDENCE.
- Give a runnable gate both CHECK and EXPECT; give a manual gate neither.
- Success requires process exit 0 and EXPECT.
- Make EXPECT a success-only marker produced after every assertion passes.
- For an absence or negative assertion, test the same checker against a known
  positive fixture and record that control in the gate's manual review.
- Measure supplied figures from source. Do not copy a supplied number into
  EXPECT as its own proof.
- Use repository-owned Node scripts for portable examples.
- Record exact manual evidence and review consequential manual gates by risk.

Do NOT use ABANDON: this repo's own resolution rule (see ../SKILL.md) never
abandons or halts on an unmet gate — after 2-3 self-correction retries, an
unmet gate gets documented as a stated gap in the step's own output, and the
run continues.
-->
