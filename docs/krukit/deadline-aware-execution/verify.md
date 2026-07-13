# Verify: deadline-aware-execution

Date: 2026-07-13 | Route: full | Autonomous | Verified: commits 799ee4c..04e343b vs design.md + plan.md | Constitution v1.0.0

## Evidence (fresh runs, output read)

| Claim | Command / source | Result |
|---|---|---|
| Full lint green (end state) | `python3 scripts/lint-consistency.py` | `OK: 11 skills checked`, exit 0 |
| Lint pin red→green (P1/P8) | `git show 787428b` | @787428b: Deadline-gate bullet count **0** (absent), lint-assertion count **2** (present) → RED genuine; 53767bd adds bullet → GREEN. Re-proven fresh. |
| Bullet is live (not just repo) | `readlink ~/.claude/skills/krukit-flow` | → `…/github/krukit/skills/krukit-flow` (dir symlink); live file Deadline-gate count 1. No sync step needed (Learnings). |
| Bullet verbatim vs design | Python exact compare | 748 chars both, **identical** — no drift |
| Terminology consistent | grep | bullet "Deadline gate" / glossary "deadline gate" (×2) / lint pins `**Deadline gate.**` — aligned; 0 new TODO/TBD |
| P7 no numeric timer | grep on bullet | 0 numeric-timer tokens (behavioral heuristic only) |
| P5 composes, not weakens | read bullet final sentence | "Adds to, never overrides… still snapshot before touch; best-effort is never fabricated" — strengthens the floor |
| krukit-v4 vendored (P9) | grep | v4 Deadline-gate count **1**; v3 count **0** (frozen); v3 flow SKILL.md 11,107 B unchanged |
| krukit-v4 wired | `make -n krukit-v4-hard` | expands to `TASKSET=hard ONLY=krukit-v4 MAX_NEW_JOBS=1 ./run.sh`; status.py lists krukit-v4; run.sh:34 + Makefile:16 + PINS.txt updated |

## Reality-check (design ↔ plan ↔ code)
All plan.md paths exist (scripts/lint-consistency.py, skills/krukit-flow/SKILL.md, CONTEXT.md). Every DoD item implemented: DoD1 bullet → 53767bd; DoD2 lint pin red→green → 787428b→53767bd; DoD3 glossary → b3539bb; DoD4 krukit-v4 + prediction → this stage; DoD5 full lint green → fresh. No placeholders, no terminology drift, constitution MUST (P5/P7/P8) hold in the actual code.

## Findings

| ID | Severity | Location | Summary | Recommendation |
|---|---|---|---|---|
| V1 | MEDIUM | whole change (behavioral) | Efficacy is UNVERIFIED until the bench runs — prompt-code behavior claims are only honest post-bench. Diagnosis rests on n=2 / 3 tasks. | By design: prediction pre-registered below; krukit-v4 is the n=3 probe. Carry to review; NO efficacy claim before the grid returns. |
| V2 | LOW | krukit-flow bullet + Layer-0 ordering | "Launch the expensive job first and backgrounded" could tension with snapshot-before-touch on a task that is BOTH long-running AND mutates irrecoverable state. | Guarded by the explicit composition clause ("still snapshot before touch") and snapshot is listed first. Review should eyeball the precedence wording; no change needed now. |
| V3 | LOW | krukit-bench (setup edits) | krukit-v4 condition edits (vendor tree, PINS.txt, run.sh, Makefile, status.py, conditions/krukit-v4.md) are UNCOMMITTED — krukit-bench is not a git repo (no VCS to commit to). | State plainly; the bench repo has never been version-controlled (v2/v3 same). Not a defect. |
| V4 | LOW | krukit-flow SKILL.md | P2 recurring cost: +~95 words / +753 B (11,114→11,867) to the highest-traffic file. | Accepted & justified in design + commit body (3 recoverable hard tasks; no non-weakening compression available). |

Metrics: requirements 5 (design DoD) / implemented 5 / findings 4 (0 CRITICAL, 0 HIGH, 1 MEDIUM, 3 LOW).

## Pre-registered prediction (P1/P3 — record BEFORE the run)
**Setup:** krukit-v4 = current krukit HEAD (04e343b) skills vendored; run `cd /Users/todmy/github/krukit-bench && make krukit-v4-hard` (one rep; drop `MAX_NEW_JOBS=1` or loop for the ≥3 reps P3 requires before any public number).

**Falsifiable exit criterion:** on the 3 flappy tasks — **password-recovery, path-tracing, torch-tensor-parallelism** — `AgentTimeoutError` trials show **reward > 0** (a best-effort deliverable was materialized to disk before the cutoff, the same valid semantics torch-tensor-parallelism and fix-ocaml-gc already showed in krukit-v3 r1) instead of **reward = 0** (empty timeout, as in r2). The **mips pair** (make-doom-for-mips, make-mips-interpreter) is predicted to **stay FAIL** = capability wall, documenting the scope boundary.

**Honest caveat:** the whole diagnosis is n=2 on 3 tasks. This wave IS the n=3 probe of whether the timeout pattern even reproduces. If the flappy-3 pass or timeout-with-reward>0 in r1 of v4, the mechanism is supported (still needs r2/r3). If they time out empty again, the deadline-gate wording did not change behavior and the wave is falsified — that is an acceptable, informative outcome, not a failure to hide.

**Attribution confound (review finding I-1, recorded 2026-07-13):** v4 is vendored cumulatively at HEAD, so vs v3 (@0f6a63c) it carries not only the deadline gate but also the wave-2 review-close edit to krukit-act/SKILL.md (377670e, Learnings-gate wording). A v3→v4 reward delta is therefore NOT attributable to the deadline gate alone. The specific pre-registered criterion above is largely immune (it keys on timeout-trials materializing a deliverable, which the krukit-act wording doesn't touch), but any broader "v4 beats v3" claim must carry this footnote. Mirrored in krukit-bench vendor/PINS.txt.

**Outcome (recorded 2026-07-13, post-run): FALSIFIED at the trace level.** krukit-v4-r1 was aborted by the user after 3/10 trials, all reward 0.0. password-recovery timed out empty again — its trace shows 0 backgrounded jobs, 0 bounded `timeout` wraps, no early deliverable write: the bullet did not change mid-run behavior at all. torch-tensor-parallelism finished early (12 of 15 min) with an unverified deliverable — no interpreter-install attempt (v3-r2's agent did apt-get + pip), a manual trace passed a bug, and the partial-satisfies-deliverable-gate loophole licensed the exit. write-compressor regressed from stable PASS (over-engineering with no secured baseline). Additional correction: the real agent budget is 900 s, not the ~1 h assumed during design. Mechanistic diagnosis and rework: **deadline-gate-v2** (supersedes this prediction; aborted r1 trials retained as trace material only, not P3 data).

## Gate
- [x] Full test suite (lint) ran fresh, output read, passing (exit 0, 11 skills).
- [x] verify.md exists with findings table + metrics line.
- [x] Zero CRITICAL findings.
- [x] Zero HIGH findings (nothing requires user acceptance).
- [ ] No confirmed discovery.md exists (no Validation-plan step to run) — not applicable.
