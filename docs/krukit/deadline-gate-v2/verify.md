# Verify: deadline-gate-v2

Date: 2026-07-13 | Route: full | Autonomous | Verified: commits feecfef..632fcc5 vs design.md + plan.md | Constitution v1.1.0

## Evidence (fresh runs, output read)

| Claim | Command / source | Result |
|---|---|---|
| Full lint green (end state) | `python3 scripts/lint-consistency.py` | `OK: 11 skills checked`, exit 0 |
| Lint pins red→green (P1/P8) | `git show c12f1f1:*` | @c12f1f1 (RED): all 4 pinned clauses absent from skills, lint carries 3 `deadline-gate-v2` err branches → 4 genuine errors (run output recorded in act); dd6c0c2 turns all green. |
| Bullet verbatim vs design | Python exact compare | 937 chars both, **identical** — no drift |
| W4 clauses placed correctly | substring check | act clause in act only; verify clause in verify only; both match design verbatim |
| Live immediately | `realpath ~/.claude/skills/krukit-flow` | → repo dir (symlink); live file carries v2 clauses. No sync step (prior-wave Learnings). |
| Terminology | grep CONTEXT.md | `**deadline gate**` (v2 semantics), `**deadline plan**`, `**baseline-first ladder**` present; old "background the expensive job" phrasing gone |
| P7 no numeric timers | regex on bullet | zero digits in the bullet ("minutes" is a scale word, no threshold) |
| P5 composes, not weakens | read bullet | survivors intact: cut-off assumption, snapshot subordination, bounded `timeout`, busy-waiting anti-pattern, write-early/improve-in-place, composition clause |
| krukit-v5 vendored (P9) | vendor greps | v5 carries `deadline plan`/`never an exit`/act env rule; v4 frozen (old bullet intact); v3 frozen (11,107 B) |
| krukit-v5 wired | `make -n krukit-v5-hard` | expands to `TASKSET=hard ONLY=krukit-v5 MAX_NEW_JOBS=1 ./run.sh`; run.sh/Makefile/status.py/PINS.txt each carry krukit-v5 |
| W5 note uncommitted | `git status` | `?? HARNESS-IMPROVEMENTS-DRAFT.md` (standing instruction honored) |

## Reality-check (design ↔ plan ↔ code)
All plan paths exist; DoD1→dd6c0c2, DoD2→c12f1f1+dd6c0c2, DoD3→dd6c0c2, DoD4→ba56e9a, DoD5→d854367, DoD6→uncommitted append (verified `??`), DoD7→this stage. No placeholders, no terminology drift; P5/P7/P8 hold in the actual text. Old-wave artifacts untouched except the sanctioned verify.md outcome addendum.

## Findings

| ID | Severity | Location | Summary | Recommendation |
|---|---|---|---|---|
| V1 | MEDIUM | whole change (behavioral) | Efficacy UNVERIFIED until krukit-v5 runs; evidence base is 3 aborted trials (mechanistic, trace-confirmed — valid for mechanism claims per P3, not for numbers). | Prediction pre-registered below; krukit-v5 r1 is the probe. NO efficacy claim before the grid returns. |
| V2 | LOW | flow bullet | "plan as if the budget were minutes" could inject false urgency on genuinely long-budget interactive work. | Trigger list unchanged (self-scoped); review should eyeball; revisit only on a field trace showing harm. |
| V3 | LOW | krukit-bench | v5 condition edits uncommitted — bench repo has never been version-controlled (same as v2/v3/v4). | Not a defect; state plainly. |
| V4 | LOW | flow SKILL.md | P2 recurring cost +158 B in the highest-traffic file. | Justified in design + commit body (replace-not-add; 3 mechanistic fixes). |
| V5 | LOW | W4 scope | Environment rule lives in act/verify — direct-route tasks (no stage skills loaded) get only the bullet's "verifiable" baseline wording. | Accepted at grill Q4 (torch = fix route). Candidate for a future wave if a direct-route trace shows the gap. |

Metrics: requirements 7 (design DoD) / implemented 7 / findings 5 (0 CRITICAL, 0 HIGH, 1 MEDIUM, 4 LOW).

## Pre-registered prediction (P1/P3 — record BEFORE the run)
**Setup:** krukit-v5 = krukit skills vendored @ 632fcc5 (pre-review) (re-vendored at final HEAD after review, same as prior waves); run `cd /Users/todmy/github/krukit-bench && make krukit-v5-hard` (one rep; ≥3 reps before any public number, P3).

**Mechanistic criterion (primary, trace-falsifiable):** in the r1 trajectories of **write-compressor, password-recovery, path-tracing**: (a) a deadline-plan line exists (route-log line or first artifact) AND (b) the first write of the declared deliverable lands in the first half of the agent's used wall-clock. In **torch-tensor-parallelism**: an interpreter-install attempt (apt-get/pip or equivalent) precedes any manual-trace verification claim. **Falsified** if the traces again show no plan and no early deliverable write — that would mean prompt-text cannot carry this behavior and W5 (harness hooks) becomes the primary path.

**Outcome criterion (secondary, directional):** write-compressor returns to PASS; hard-10 r1 mean ≥ 0.5 (v3 band). The **mips pair** stays FAIL (capability wall, unchanged claim).

**Attribution note:** v5 vs v3 is cumulative (carries 377670e and the v4→v5 bullet lineage); v5 vs the aborted v4 isolates this wave's rewrite but v4 has no full-grid data. Deltas are attributed to the wave only via the mechanistic criterion, not raw means.

## Gate
- [x] Full test suite (lint) ran fresh, output read, passing (exit 0, 11 skills).
- [x] verify.md exists with findings table + metrics line.
- [x] Zero CRITICAL findings.
- [x] Zero HIGH findings.
- [x] No confirmed discovery.md exists — Validation-plan step n/a.
