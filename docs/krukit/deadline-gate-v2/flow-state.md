# Krukit Flow: deadline-gate-v2
Started: 2026-07-13 | Route: full | Mode: autonomous
Task: Rework Deadline gate from krukit-v4-r1 trace evidence — W1 deadline-plan checkpoint, W2 baseline-first ladder, W3 close partial-loophole, W4 environment rule (act/verify); W5 harness-hooks recorded as note only
- [x] 1 recon — done 2026-07-13, artifact: context.md
- [x] 2 grill — done 2026-07-13, artifact: flow-state.md
- [ ] 3 design
- [ ] 4 plan
- [ ] 5 act
- [ ] 6 verify
- [ ] 7 review

> [auto-answer] Stage-0 route: full — reworks Layer-0 invariant wording (P5, load-bearing) + edits krukit-act/krukit-verify; user approved the W1-W4 plan with "+" but is not steering stage-by-stage (established wave precedent) — 2026-07-13
> [constitution] v1.1.0, 10 principles — loaded (open mode: existing constitution → no-op)

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

