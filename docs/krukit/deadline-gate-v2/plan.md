# Plan: deadline-gate-v2

Goal (from design): make the Deadline gate fire in real trajectories — bullet rewrite (W1 deadline plan, W2 baseline-first ladder, W3 never-an-exit) + W4 environment rules in act/verify, all pinned red→green. Stack: markdown prompt-code + Python lint. Global constraints carried from design: replace-not-add (P2), label `**Deadline gate.**` kept, exact texts in design.md §Design are normative.

MUST NOT break (context.md Invariants):
- Route-name regex anchors: `EVERY route — trivial, direct, fix, full, external-spec —`, route-table first cells, README `routes a task (...)`.
- Flow-state template blocks inside act/verify SKILL.md (validated against canonical constants).
- Old-wave artifacts (deadline-aware-execution design/plan) keep the OLD bullet verbatim — provenance, never retro-edited.
- krukit-v3/v4 bench vendor trees frozen (P9). Constitution P5/P7/P4 as checked in design.

## Tasks

- [ ] **T1 — lint pins (RED).** Modify `scripts/lint-consistency.py`: extend krukit-flow branch with `for needle in ("deadline plan", "never an exit")` check; add `krukit-act` branch pinning `part of the task, not a blocker`; add `krukit-verify` branch pinning `recorded as unverified` (exact code in design.md). Test: run lint, expect exit 1 with EXACTLY 4 new errors (2 flow, 1 act, 1 verify) and no others. Commit (red).
- [ ] **T2 — skill edits (GREEN).** Replace the Deadline-gate bullet in `skills/krukit-flow/SKILL.md:16` with design's normative text; append the environment sentence to act step 4 iron-law paragraph; append the manual-trace clause to verify step 2 main paragraph (both normative texts in design.md). Test: lint exit 0, `OK: 11 skills`. One logical change (the four pins turn green together). Commit; message carries the P2 cost line (+158 B flow, +1 sentence act, +1 clause verify).
- [ ] **T3 — CONTEXT.md glossary.** Reword line 9 (`**deadline gate**`) to ladder semantics; add `**deadline plan**` and `**baseline-first ladder**` entries (texts in design.md). Test: lint still green; grep shows the three entries. Commit.
- [ ] **T4 [mechanical] — old-wave outcome addendum.** Append the v4-r1 outcome paragraph after the attribution-confound paragraph in `docs/krukit/deadline-aware-execution/verify.md` (content per design: aborted 3/10 at 0.0, trace-level falsification, superseded by deadline-gate-v2). Test: section reads Setup → criterion → caveat → confound → outcome. Commit.
- [ ] **T5 [mechanical] — W5 note, NO COMMIT.** Append `### 15. Harness-level time triggers (hook/heartbeat) — deadline-gate-v2 finding` to HARNESS-IMPROVEMENTS-DRAFT.md (content per design). Test: file remains untracked (`git status` shows `??`).

Stage-6 (verify) owns: fresh full-lint evidence, verbatim-bullet check, bench condition krukit-v5 (vendor at final HEAD, PINS.txt, run.sh/Makefile/status.py wiring) + the two-tier pre-registered prediction.

## Self-review
Spec coverage: DoD1→T2, DoD2→T1+T2, DoD3→T2, DoD4→T3, DoD5→T4, DoD6→T5, DoD7→stage 6 (by design). No placeholders; all task texts resolve to normative snippets in design.md. Types n/a (prose + one Python loop).
