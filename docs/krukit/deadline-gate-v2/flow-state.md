# Krukit Flow: deadline-gate-v2
Started: 2026-07-13 | Route: full | Mode: autonomous
Task: Rework Deadline gate from krukit-v4-r1 trace evidence — W1 deadline-plan checkpoint, W2 baseline-first ladder, W3 close partial-loophole, W4 environment rule (act/verify); W5 harness-hooks recorded as note only
- [x] 1 recon — done 2026-07-13, artifact: context.md
- [x] 2 grill — done 2026-07-13, artifact: flow-state.md
- [x] 3 design — done 2026-07-13, artifact: design.md
- [x] 4 plan — done 2026-07-13, artifact: plan.md
- [x] 5 act — done 2026-07-13, artifact: plan.md (T1 red→green T2; T3-T4 committed; T5 uncommitted by design)
- [x] 6 verify — done 2026-07-13, artifact: verify.md
- [x] 7 review — done 2026-07-13, artifact: flow-state.md

> [auto-answer] Stage-0 route: full — reworks Layer-0 invariant wording (P5, load-bearing) + edits krukit-act/krukit-verify; user approved the W1-W4 plan with "+" but is not steering stage-by-stage (established wave precedent) — 2026-07-13
> [constitution] v1.1.0, 10 principles — loaded (open mode: existing constitution → no-op)

> [auto-answer] act execution mode: inline (5 small prompt-edit tasks with normative texts already in orchestrator context; fresh-context subagents would pay ~50K prefix each for zero noise-isolation benefit — token-discipline override of the >3-tasks rule, logged as deviation) — 2026-07-13

## Grill summary (2026-07-13)
All 6 Open questions from context.md resolved against code + v4-r1 traces.

- **[auto-answer] Q1 W1 placement**: inside the Deadline-gate bullet — single pinned locus; the plan itself lands "in the route-log line or first artifact", which exists on every route incl. direct (where password-recovery failed). Rejected extending the step-2 route-log contract (second locus, P2). — 2026-07-13
- **[auto-answer] Q2 survivors**: keep trigger scope ("On long-running, search, or compute-bound work (…)"), cut-off assumption, snapshot subordination (review I-2, hard-won), bounded-`timeout` clause (torch v3-r2 hang), "instead of busy-waiting" (review M-2 explicitly kept), write-early + improve-in-place (reframed as ladder rung 1), composition clause. DEMOTED: "launch the expensive job early and backgrounded" — absorbed into the ladder as "run long rungs backgrounded/bounded"; at the observed minutes-scale budgets it cannot lead the bullet. — 2026-07-13
- **[auto-answer] Q3 W3 wording**: key on the conjunction — "while budget remains AND verification has not passed"; partial on disk = safety net against the cutoff, never an exit criterion. Legitimate early finish (verification passed) stays legal; stress-tested. — 2026-07-13
- **[auto-answer] Q4 W4 placement**: split, one sentence each — krukit-act step 4 (missing interpreter/test runner is part of the task: attempt install before any non-executable fallback) + krukit-verify step 2 (manual reasoning in place of execution = last resort after a failed install attempt, results marked unverified). Two NEW lint substring pins (first body pins for act/verify), each proven red→green. Note: direct route loads neither skill — covered only by the bullet's "verifiable baseline"; accepted (torch = fix route, the W4 case). — 2026-07-13
- **[auto-answer] Q5 prediction shape**: two-tier — mechanistic primary (trace-falsifiable: deadline-plan line exists; first deliverable write in first half of used wall-clock; torch-class trials attempt install before manual-trace), outcome secondary (write-compressor back to PASS; hard-10 mean ≥ v3 band). Exact text registers in verify stage BEFORE the run. — 2026-07-13
- **[auto-answer] Q6 W5 note**: net-new `### 15.` section appended to HARNESS-IMPROVEMENTS-DRAFT.md (no hooks/heartbeat section exists; file stays uncommitted by standing instruction). — 2026-07-13

Code cross-checks: lint pin `**Deadline gate.**` survives the reword (label kept) — but it cannot prove the rewrite; P1 red→green therefore rides on a NEW pinned substring from the new semantics (registered in design). Route-name regex anchors (`EVERY route — … —`, table cells, README enumeration) untouched by all planned edits. ✓ Historical artifacts of the previous wave keep the old bullet verbatim — provenance, not drift. ✓

Sharpened terms (→ CONTEXT.md in act): **deadline plan** (one line: baseline → escalation rungs → first-write moment), **baseline-first ladder** (cheapest verifiable end-to-end deliverable secured on disk first, then climb). Stress-tests passed: quick tasks (self-scoped, inert), early finish with verification passed (legal), interactive long tasks (plan rides route-log/first artifact). No ADR (recorded here; reversible).


## Review summary (2026-07-13)
Independent fresh-context review of 25173f4..HEAD: **0 Critical / 2 Important / 7 Minor**. Reviewer independently re-proved red→green via `git archive c12f1f1` (exactly the 4 predicted errors) and probed pin sensitivity with 3 break-mutations; verified P2 (+158 B replace-not-add), P5 survivors, bench freeze (v3/v4), and design↔code verbatim.

Resolutions (every finding, on merits):
- **I-1 FIXED** — early-exit via rung-local self-chosen verification on open-ended work: exit now binds to "the task's own declared success criteria — open-ended or scored work has no early pass" (commit 0-of-day: see log). Same loophole class W3 targeted; leaving it half-closed would waste the paid probe run.
- **I-2 FIXED** — "budget remains" undecidable in-run: default polarity added, "(assume it does unless the harness says otherwise)". Same commit as I-1 (one clause).
- **M-1 DECLINED** — "plan as if minutes" misread as stopping rule: the actionable misreading is already closed by I-2's default; the proposed aphorism is redundant bytes (P2).
- **M-2 FIXED** — restored "(marked partial while incomplete)" dropped by the rewrite (never-fabricate hygiene; P5-adjacent regression the design missed).
- **M-3 FIXED** — flow clause pins scoped to the bullet line (presence AND placement); sensitivity re-probed. Act/verify pins stay file-scoped (single occurrence, no siblings) per reviewer's own condition.
- **M-4 RECORDED** — deadline-plan home elastic on full route / undefined pre-routing: watch item bound to v5 trace inspection; if plan lines are vacuous, pin the home to the approach-committing artifact (next wave, P6 needs the trace).
- **M-5 RECORDED** — baseline-first vs TDD iron law unarbitrated: named watch item for the v5 run (reviewer agrees P6 requires a trace first).
- **M-6 DECLINED (deferred)** — conditions/krukit-v5.md gate-evidence format conflicts with the skill's [auto-answer] contract: inherited verbatim from v3/v4; editing v5's condition file now would break v3↔v5 comparability for a conflict the prediction does not key on. Fix in the next condition GENERATION.
- **M-7 FIXED (disclosure + process fix)** — v4 vendored dirty (3 gitignored IMPROVE-LOG.md riders): disclosed in vendor/PINS.txt (v4 untouched per P9; v3 verified rider-free); v5 re-vendored via `git archive` at final HEAD 493e5d1 — byte-identical, rider-free; vendoring method noted in PINS.txt for future waves.

Branch outcome: work on main (established wave pattern), final lint green, NOTHING pushed. Reviewer's overall: "execution quality is high… recommend shipping as-is for the v5 probe run" — Important findings fixed anyway (cheap, and the probe is paid).
> [auto-answer] branch options: keep on main as committed, no push — autonomous mode; matches all prior wave precedent — 2026-07-13
> [auto-answer] constitution close: NO amendment — the wave refines Layer-0 content already protected by P5; no new project-wide principle emerged (honest common case per krukit-rules) — 2026-07-13
Knowledge capture: no .valis.json in repo → Valis capture skipped silently (per skill contract).
