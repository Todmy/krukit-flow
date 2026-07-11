# Krukit Flow: v2-wave1-layer0
Started: 2026-07-11 | Route: fix
Task: Wave 1 of HARNESS-IMPROVEMENTS-DRAFT v2 plan — Layer-0 invariants preamble (items 8+9) + autonomous-mode addendum (item 11, autonomous half) in skills/krukit-flow/SKILL.md + consistency lint script (item 4). Spec: HARNESS-IMPROVEMENTS-DRAFT.md "Synthesis & v2 architecture".
- [x] 1 recon — skipped (route) 2026-07-11
- [x] 2 grill — skipped (route) 2026-07-11
- [x] 3 design — skipped (route) 2026-07-11
- [x] 4 plan — skipped (route) 2026-07-11
- [x] 5 act — done 2026-07-11, artifact: inline task list below (4 commits 437da4a..88749e8)
- [x] 6 verify — done 2026-07-11, artifact: verify.md
- [x] 7 review — skipped (route) 2026-07-11

Route gate evidence:
> "fix (Recommended)" — 2026-07-11

Act task-list gate evidence:
> "Підтверджую (Recommended)" + "Inline (Recommended)" — 2026-07-11

Validation plan (for stage 6): krukit-bench re-run of db-wal-recovery + cobol-modernization as new `krukit-v2` condition. Falsifiable predictions: db-wal-recovery flips to PASS; no asked-the-void terminations; plus lint script passes on the whole skills/ tree.

## Act — inline task list

- [x] T1: `scripts/lint-consistency.py` (item 4) — checks: frontmatter valid on every skills/*/SKILL.md; duplicated flow-state templates identical across skills; referenced `references/`/docs paths exist; "Stage N of 7" numbering consistent with canonical order. RED: expected to catch the known krukit-verify template drift (missing `Task:` line, logged 2026-07-06). GREEN: fix the drift lint catches. Commit 1.
- [x] T2: Layer-0 invariants preamble in `skills/krukit-flow/SKILL.md` (items 8+9, route-independent, incl. trivial/external-spec): snapshot-before-touch for irrecoverable mutable state + deliverable-existence gate with never-fabricate. Test: lint still green + content matches draft item text. Commit 2.
- [x] T3: `## Autonomous mode` addendum in `skills/krukit-flow/SKILL.md` (item 11, autonomous half): gates → logged checkpoints; questions forbidden until deliverable exists; self-answer with recommended default logged as `[auto-answer]` evidence line (amends step 8 audit rule, which currently declares self-generated answers structurally invalid — autonomous carve-out must be explicit). Test: lint green + no contradiction with step 8 wording. Commit 3.

## Learnings

- The Task:-line drift was wider than IMPROVE-LOG recorded: all SIX standalone templates lacked it (grill/design/plan/act/verify/review), not only krukit-verify. Duplicated-template drift compounds silently — exactly why the lint pins structure, not instances.
