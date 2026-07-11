# Verify: v2-wave2-router-diet

Date: 2026-07-11 | Route: full | Verified: commits 96bb4c0..0f6a63c vs design.md + plan.md

## Evidence (fresh runs, output read)

| Claim | Command / source | Result |
|---|---|---|
| Lint green end-state | `python3 scripts/lint-consistency.py` | `OK: 11 skills checked`, exit 0 |
| New route-consistency check red→green | commit history eba972c (RED by design, 1 error) → 3666446 (GREEN) | proven |
| P4 resume compat | parse simulation over both existing flow-states | headers parse, 7/7 rows, resume points correct (wave1=COMPLETE, wave2=verify) |
| db-wal-recovery (Layer-0 regression) | bench `sonnet-5-v2check/krukit-v3-r1` | PASS $0.46 — **explicitly named the direct route** ("forensics/recovery task, maps to the **direct** route"), route-log written ×2, 16 calls |
| password-recovery | bench `sonnet-5-w2pair/krukit-v3-r1` | PASS $0.61, 21 calls, route-log line written (cmd[3]), read-only tools first (Layer-0 honored) |
| write-compressor | same grid | PASS $1.40, 16 calls — **hard-grid v1 timeout-fail FLIPPED to PASS**; but Stage 0 bypassed → no route-log (finding V2) |
| cobol-modernization cost | bench `sonnet-5-v2check/krukit-v3-r1` | PASS $1.91 / 2.4M input / **34 calls (v1: 73)**; oracle: byte-identical diff, single verify cycle applied. Target ≤$0.96-1.00 NOT met (finding V1) |

Cost trajectory cobol (fix route): v1 $3.34 (7.0× baseline) → Wave-1 $2.07 (4.3×) → Wave-2 $1.91 (**4.0×**). Call anatomy v3: 3 Skill loads, 21 Bash (TDD + verify cycles), 6 Write / 3 Edit (bookkeeping now 4 writes: flow-state ×3 + route-log ×1 — was 18 TaskCreate/Update + 15 artifact writes), 1 Read.

## Findings

| ID | Severity | Location | Summary | Recommendation |
|---|---|---|---|---|
| V1 | HIGH | design.md §Testing (3.i) | Fix-route cost target ≤2× baseline not reached: $1.91 = 4.0× (halved calls 73→34, −54% input tokens, but floor = 3 SKILL.md loads + TDD + evidence-verify) | Accept revised exit (~4× after diet; ≤2× moves to Wave 4 with fresh-context subagents — the biggest untried lever) via design amendment, or push more diet now (reopens design: slim variants were explicitly deferred) |
| V2 | MEDIUM | conditions + krukit-flow Stage 0 | write-compressor bypassed Stage 0 wholesale (model-level skip before the route table engaged) → correct decision, PASS, but NO route-log line — telemetry coverage is not guaranteed by skill text alone | IMPROVE-LOG candidate: strengthen condition/preamble "even when skipping the pipeline, record the route-log line"; monitor rate in future grids |
| V3 | LOW | scripts/lint-consistency.py | Route-table regex assumes exactly one markdown table in krukit-flow SKILL.md (recorded in plan Learnings) | Add section anchor if a second table ever appears |

Metrics: requirements 6 (design §1-§6) / implemented 6 / findings 3 (0 CRITICAL, 1 HIGH, 1 MEDIUM, 1 LOW).

## Wins beyond predictions

- direct route worked textbook-style on db-wal ($0.46, was $0.83 in Wave 1 — direct is cheaper than fix for non-feature work).
- write-compressor: hard-grid timeout-fail → PASS at $1.40.
- Bookkeeping churn eliminated: 18 tracker calls → 4 file writes.

## Gate

- [x] Full test suite (lint) ran, output read, passing.
- [x] verify.md exists with findings table + metrics line.
- [x] Zero CRITICAL.
- [x] HIGH V1 — explicitly accepted by the user in writing:
  > "Прийняти ~4×, ≤2× → Wave 4 (Recommended)" — 2026-07-11
  Design §Testing (3.i) amended accordingly (provenance preserved below).
