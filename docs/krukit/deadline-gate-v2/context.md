# Context: deadline-gate-v2

## Goal
Rework the Deadline gate so it actually changes mid-run behavior — trace evidence from aborted krukit-v4-r1 (3/3 trials 0.0) shows the current bullet never fired: no classification moment, no early deliverable, a partial-satisfies-deliverable-gate loophole, and no environment-building rule.

## Affected map
| File | Role | Who depends on it |
|---|---|---|
| skills/krukit-flow/SKILL.md:16 | canonical Deadline-gate bullet (file 11,896 B) | every route on every task; lint pin `**Deadline gate.**` (lint-consistency.py:71) |
| skills/krukit-act/SKILL.md steps 4-5 (8,018 B) | TDD iron law + failure handling — W4 anchor (install-before-fallback) | full+fix routes; NO body pins today |
| skills/krukit-verify/SKILL.md step 2 (6,779 B) | verify-by-evidence — W4 anchor (manual trace = last resort, marked unverified) | full+fix routes; NO body pins today |
| scripts/lint-consistency.py | pins: flow sections + `**Deadline gate.**` substring; route-name regexes | P1/P8 proof harness |
| CONTEXT.md:8-9 | Layer-0 enumeration + deadline-gate glossary entry | must mirror the reworded semantics |
| docs/krukit/constitution.md:10 | P5 names "deadline gate" (name survives reword — no amendment) | design/verify constitution checks |
| docs/krukit/deadline-aware-execution/verify.md:33-40 | old pre-registered prediction — outcome addendum appends after L40 | scientific hygiene (P1/P3) |
| HARNESS-IMPROVEMENTS-DRAFT.md (untracked) | W5 harness-hooks note is NET-NEW there (no hooks/heartbeat section exists) | stays uncommitted |
| krukit-bench (not git) | edits become NEW condition krukit-v5 (P9); v4 stays pinned @7ed9b99 | grid comparability |

## Patterns to follow
- Named-invariant + dedicated lint substring pin, proven red→green (deadline-aware-execution wave; lint-consistency.py:65-72).
- Composition clause at bullet end ("Adds to, never overrides…") — keep (review I-2 precedent).
- Historical wave artifacts (old design.md/plan.md quoting the old bullet verbatim) are provenance — never retro-edited.
- Route-log one-liner contract (flow step 2 L53) — W1's deadline plan can ride on it without new ceremony.

## Invariants (MUST NOT break)
- Lint substring `**Deadline gate.**` stays or lint updated in the SAME red→green commit pair (P8).
- Route-name regexes: do not touch `EVERY route — trivial, direct, fix, full, external-spec —` phrase, route table first cells, README `routes a task (...)` (lint checks 9-10).
- Flow-state template markers in act/verify SKILL.md (validated against canonical constants) — W4 edits must not touch template blocks.
- P5: reword may not weaken snapshot-before-touch / deliverable gate / never-fabricate; P7: no numeric timers; P2: replace-not-add in the 11.9 KB highest-traffic file; P4: no flow-state format changes.
- krukit-v3/v4 vendor trees in bench stay frozen (P9).

## Risks
- Over-stuffing the bullet: 4 fixes into one paragraph → prompt bloat + dilution (P2). Mitigation: ladder wording subsumes W1-W3; W4 lives in act/verify.
- "Baseline-first" could over-trigger on quick tasks → wasted ceremony; bullet must stay self-scoped to long/search/compute-bound work (P6).
- W3 wording could be read as forbidding legitimate early finish when verification HAS passed — must key on "verification not passed AND budget remains".
- Evidence is n=1×3 trials (mechanistic, trace-confirmed — legitimate per P3 for mechanism claims, not for public numbers).
- 900s real budget: "background the expensive job" advice barely applies at minutes scale — rungs must be minutes-scale; keep bounded-`timeout` clause (torch v3 hang evidence).

## Open questions
1. W1 placement: inside the bullet (single pinned locus) vs extending the route-log contract in flow step 2?
2. Which clauses of the current 748-char bullet survive the rewrite (P2 replace-not-add)?
3. W3 exact wording that closes the loophole without contradicting the deliverable gate or forbidding legitimate early completion?
4. W4 placement and pinning: act step 4 vs step 5 vs verify step 2 — one place or split; new lint substring pins for act/verify (first-ever body pins there)?
5. New pre-registered prediction: trace-level (early write, install attempt) vs outcome-level (write-compressor back to PASS; mean band) — what exactly is falsifiable?
6. W5 note: exact location/shape in HARNESS-IMPROVEMENTS-DRAFT.md (stays uncommitted)?
