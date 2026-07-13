# Design: deadline-aware-execution

Route: full | Autonomous | 2026-07-13 | Constitution v1.0.0

## Goal / Definition of Done
Extend the Layer-0 floor with a **Deadline gate** invariant so a wall-clock cutoff can no longer strand the deliverable on long/compute-bound tasks. Motivated by krukit-v3 hard-grid: 3 tasks (password-recovery, path-tracing, torch-tensor-parallelism) passed in r1 and hit AgentTimeoutError with reward=0 in r2 — killed mid-work with an empty deliverable.

DoD:
1. New "Deadline gate" bullet in krukit-flow Layer-0.
2. Lint substring pin for the bullet, proven red→green.
3. CONTEXT.md glossary mirrors the term.
4. krukit-v4 bench condition set up; falsifiable prediction pre-registered.
5. Full lint suite green (11 skills).

## Approaches
- **A — Autonomous-mode-only clause.** REJECTED: password-recovery timed out on the **direct** route, not full/autonomous-only; a mode-scoped clause misses direct + interactive long tasks.
- **B — Extend the existing deliverable-gate bullet in place.** REJECTED: not independently lint-pinnable (P8), less discoverable, conflates two distinct obligations (end-state gate vs. proactive-during-run behavior).
- **C — New named Layer-0 bullet "Deadline gate" + dedicated lint substring pin. (RECOMMENDED)** Route-independent (matches the observed failure), pinnable, discoverable, composes with the existing invariants without weakening them.

## Design — the exact change
**krukit-flow/SKILL.md**, insert as the third Layer-0 bullet immediately after the deliverable-gate bullet (L15):

> - **Deadline gate.** On long-running, search, or compute-bound work (render, brute-force, training, build, open-ended fit), assume the run may be cut off before it finishes. After any required snapshot, launch the expensive job early and backgrounded, then explore/verify/prepare a fallback alongside it instead of busy-waiting; wrap anything that can hang so it returns control (bounded `timeout`), never an unbounded blocking call. The moment you hold any result better than empty, write the declared deliverable to disk from what you've verified so far (marked partial if incomplete) and improve it in place — never leave it only inside a process a cutoff can kill. Adds to, never overrides, the invariants above (still snapshot before touch; best-effort is never fabricated).

(amended 2026-07-13 during review, finding I-2: original read "Launch the expensive job first and backgrounded" — the competing "first" could race snapshot-before-touch on a long task that mutates irrecoverable state; launch is now explicitly subordinated to the snapshot. Obligation strengthened, nothing weakened.)

Design rationale, per grilled decision:
- **Placement** — Layer-0 (route-independent): the failure is route-independent, so the floor is the correct home; the bullet self-scopes to long/compute work, staying inert for trivial/quick tasks (P6).
- **Phrasing** — behavioral heuristic, zero numeric timers (P7): the agent has no reliable wall-clock readout, so the trigger is "the moment you hold any result better than empty," trace-verifiable (did it write early? did it background the job?).
- **Three facets, one bullet** (P2): (a) deliverable-before-cutoff, (b) background-and-parallelize, (c) bound-hangable-ops — one principle (don't strand the deliverable in a killable/hung process).
- **Composition** — the final sentence pins that it adds to, never overrides, snapshot-before-touch and never-fabricate (stress-tested in grill).

**scripts/lint-consistency.py** — inside the existing `if skill_md.parent.name == "krukit-flow":` block, add a substring pin (headings-tuple doesn't cover bullet text):
```python
if "**Deadline gate.**" not in text:
    err(skill_md, "missing pinned Layer-0 bullet '**Deadline gate.**' (deadline-aware-execution)")
```

**CONTEXT.md** — add "deadline gate" to the Layer-0 glossary enumeration (:8).

**Bench (krukit-bench repo, set up in verify at the final commit)** — krukit-v4 = `cp -r skills vendor/krukit-v4`; append `vendor/PINS.txt`; `cp conditions/krukit-v3.md conditions/krukit-v4.md`; add `"krukit-v4:vendor/krukit-v4:"` to run.sh CONDITIONS, `krukit-v4` to Makefile L16 + status.py L8. Run: `make krukit-v4-hard`.

## Testing (falsifiable, P1)
- **Structural:** lint `**Deadline gate.**` assertion RED before the bullet exists → GREEN after; full lint suite green (11 skills).
- **Behavioral (pre-registered):** re-vendor krukit-v4, run `make krukit-v4-hard`. **Exit criterion** — on the 3 flappy tasks (password-recovery, path-tracing, torch-tensor-parallelism), AgentTimeoutError trials show **reward>0** (deliverable materialized in the container — the same valid semantics torch/fix-ocaml already showed in r1) instead of reward=0 (empty timeout). The mips pair (make-doom-for-mips, make-mips-interpreter) is predicted to **stay fail** = capability wall, documenting scope.
- **Honest caveat:** n=2 diagnosis on 3 tasks — krukit-v4 is itself the n=3 probe of whether the timeout pattern reproduces. No claimed win before ≥3 reps (P3).

## Constitution check (v1.0.0)
| Principle (MUST) | Verdict |
|---|---|
| P1 Falsifiable edits | pass — lint red→green + pre-registered bench prediction |
| P2 Prompt budget | pass (justified) — +1 bullet (~95 words) to the highest-traffic file; justified by 3 recoverable hard tasks; commit message carries the cost line; no non-weakening compression available |
| P3 Proof or silence | pass — no public numbers claimed; krukit-v4 is n=1 until ≥3 reps |
| P4 Resume compatibility | pass — no flow-state/template format change; purely additive |
| P5 Layer-0 untouchable | pass — strictly ADDS obligation; composes with and does not weaken snapshot/deliverable/never-fabricate ("the constitution may extend them" is explicit) |
| P6 Knobs earn existence | pass — recurring pattern (3 tasks flapped r1→r2, ≥2 traces); single bullet, no new route/gate/ceremony |
| P7 Rules, not scores | pass — behavioral heuristic, zero numeric timers/thresholds |
| P8 Structure pinned by lint | pass — dedicated substring pin, proven red→green |
| P9 Pinned-vendor benchmarking | pass — lands as krukit-v4; krukit-v3 untouched |
| P10 Git discipline | pass — small discrete commits; no push without permission |

Zero violations.

## Approval
> [auto-answer] design approval: approved (recommended approach C) — autonomous mode, user directive "зроби ці покращення"; zero constitution violations; falsifiable prediction pre-registered — 2026-07-13
