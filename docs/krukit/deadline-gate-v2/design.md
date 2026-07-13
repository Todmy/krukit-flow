# Design: deadline-gate-v2

Route: full | Autonomous | 2026-07-13 | Constitution v1.1.0

## Goal / Definition of Done
Make the Deadline gate fire in real trajectories. Trace evidence (krukit-v4-r1, aborted, 3/3 trials 0.0): password-recovery — 0 backgrounded jobs, 0 bounded timeouts, no early deliverable (bullet never fired); torch — early quit at 12/15 min with an unverified deliverable, no install attempt (partial-loophole + missing environment rule); write-compressor — stable-PASS regression via over-engineering with no secured baseline.

DoD:
1. Reworded `**Deadline gate.**` bullet (W1 deadline plan + W2 baseline-first ladder + W3 partial-never-an-exit) in krukit-flow — label kept, replace-not-add.
2. Lint pins proven red→green: new flow clauses (`deadline plan`, `never an exit`) + first-ever body pins for act (`part of the task, not a blocker`) and verify (`recorded as unverified`).
3. W4: one sentence in krukit-act step 4 + one clause in krukit-verify step 2.
4. CONTEXT.md glossary mirrored: deadline gate reworded; new terms **deadline plan**, **baseline-first ladder**.
5. Outcome addendum appended to docs/krukit/deadline-aware-execution/verify.md (old prediction: falsified at trace level; superseded).
6. W5 harness-hooks note appended to HARNESS-IMPROVEMENTS-DRAFT.md as `### 15.` (file stays uncommitted).
7. Full lint green (11 skills); bench condition krukit-v5 + new pre-registered prediction set up in verify stage (P9/P1).

## Approaches
- **A — Add W1-W3 as three new Layer-0 bullets.** REJECTED: floor bloat (P2/P6), three pins, dilutes the four-invariant floor into seven.
- **B — Harness-level time-trigger hook now (W5).** REJECTED for this wave: bench conditions vendor skills only, a hook changes the harness contract and destroys condition comparability; recorded as an architectural note (grill Q6).
- **C — Rewrite the single bullet so the ladder subsumes W1-W3, plus two one-sentence rules in act/verify. (RECOMMENDED)** Single pinned locus, replace-not-add, each mechanism from the traces gets exactly one clause.

## Design — the exact changes

**skills/krukit-flow/SKILL.md:16** — replace the Deadline-gate bullet with:

> - **Deadline gate.** On long-running, search, or compute-bound work (render, brute-force, training, build, open-ended fit), assume the run can be cut off at any moment — plan as if the budget were minutes. Before committing to an approach, write a one-line deadline plan (route-log line or first artifact): cheapest end-to-end baseline → escalation rungs → when the first write hits disk. Climb baseline-first: after any required snapshot, secure the simplest verifiable deliverable on disk, then improve it in place; run long rungs backgrounded and bounded (`timeout`) instead of busy-waiting — never an unbounded blocking call, never a result living only in a process a cutoff can kill. A partial on disk is a safety net against the cutoff, never an exit: while budget remains and verification has not passed, keep climbing. Adds to, never overrides, the invariants above (still snapshot before touch; best-effort is never fabricated).

Survivors per grill Q2: trigger scope, cut-off assumption, snapshot subordination (I-2), bounded `timeout` (torch v3-r2 hang), "instead of busy-waiting" (M-2), write-early/improve-in-place (now ladder rung 1), composition clause. Demoted: "launch the expensive job early and backgrounded" → "run long rungs backgrounded and bounded" (900s-budget insight: rungs are minutes-scale). New: deadline plan (W1 — forces the classification moment), baseline-first climb (W2), never-an-exit conjunction "budget remains AND verification has not passed" (W3 — closes the loophole without forbidding legitimate early finish).

**skills/krukit-act/SKILL.md step 4** — append to the iron-law paragraph:

> A missing interpreter or test runner is part of the task, not a blocker: attempt to install it (system package manager, language toolchain) before any non-executable fallback.

**skills/krukit-verify/SKILL.md step 2** — append to the main paragraph (before the discovery.md sub-bullet):

> Reasoning in place of execution (a manual trace) is a last resort permitted only after an install attempt failed — and its conclusions are recorded as unverified, never as passing evidence.

**scripts/lint-consistency.py** — extend the krukit-flow branch and add two first-ever body-pin branches:

```python
        for needle in ("deadline plan", "never an exit"):
            if needle not in text:
                err(skill_md, f"missing pinned Deadline-gate clause '{needle}' (deadline-gate-v2)")
    if skill_md.parent.name == "krukit-act":
        if "part of the task, not a blocker" not in text:
            err(skill_md, "missing pinned environment rule 'part of the task, not a blocker' (deadline-gate-v2)")
    if skill_md.parent.name == "krukit-verify":
        if "recorded as unverified" not in text:
            err(skill_md, "missing pinned manual-trace rule 'recorded as unverified' (deadline-gate-v2)")
```

**CONTEXT.md** — reword glossary line 9 to the new semantics; add two entries:
- **deadline plan** — one line: cheapest baseline → escalation rungs → first-write moment; recorded in the route-log line or first artifact.
- **baseline-first ladder** — secure the simplest verifiable end-to-end deliverable before any deep approach; escalate only from a secured rung.

**docs/krukit/deadline-aware-execution/verify.md** — append outcome addendum after the attribution-confound paragraph: v4-r1 aborted 3/10 at 0.0; trace-level verdict — prediction falsified (bullet did not change mid-run behavior); superseded by deadline-gate-v2.

**HARNESS-IMPROVEMENTS-DRAFT.md** (uncommitted, stays uncommitted) — net-new `### 15. Harness-level time triggers (hook/heartbeat)`: prompt-text cannot reliably fire mid-run; the architecturally correct home for time triggers is the harness (periodic reminder injection: "elapsed X, deliverable on disk?"); out of bench scope because conditions vendor skills only.

## Testing (falsifiable, P1)
- **Structural:** the four new lint pins RED on the pre-edit tree (each named clause absent) → GREEN after; full suite green (11 skills). The old `**Deadline gate.**` pin stays green throughout (label survives) and is therefore NOT the proof — the new pins are.
- **Behavioral (pre-registered in verify stage, before any run):** two-tier —
  - *Mechanistic (primary):* in krukit-v5 hard-10 trials of write-compressor, password-recovery, path-tracing: the trajectory contains a deadline-plan line AND the first write of the declared deliverable lands in the first half of used agent wall-clock; in torch-class trials an install attempt precedes any manual-trace claim. Falsified if traces again show no plan and no early write.
  - *Outcome (secondary, directional):* write-compressor returns to PASS; krukit-v5 hard-10 r1 mean within/above the v3 band (≥0.5). No public numbers before ≥3 reps (P3).

## Constitution check (v1.1.0)
| Principle (MUST) | Verdict |
|---|---|
| P1 Falsifiable edits | pass — 4 new pins red→green + two-tier pre-registered prediction |
| P2 Prompt budget | pass (justified) — flow bullet +~160 chars (replace-not-add; 3 mechanistic fixes for 3/3 failed trials incl. a stable-PASS regression); act +1 sentence; verify +1 clause; commit messages carry cost lines |
| P3 Proof or silence | pass — mechanism claims are trace-confirmed (v4-r1); no public numbers; v5 is n=1 until ≥3 reps |
| P4 Resume compatibility | pass — no flow-state/template format change; deadline plan rides the existing route-log reason column (append-only telemetry, nothing parses it) |
| P5 Layer-0 untouchable | pass — every prior obligation survives or is strengthened (cut-off assumption, snapshot subordination, bounded timeout, write-early, composition clause); nothing weakened, loophole closed |
| P6 Knobs earn existence | pass — no new route/gate/stage; bullet stays self-scoped to long/search/compute-bound work; evidence = 3 trace-confirmed failures |
| P7 Rules, not scores | pass — zero numeric timers/thresholds; "plan as if the budget were minutes" is a categorical scale stance, no number, no threshold |
| P8 Structure pinned by lint | pass — 4 new substring pins incl. first body pins for act/verify |
| P9 Pinned-vendor benchmarking | pass — lands as krukit-v5; v3 and v4 vendor trees untouched; v4-r1 aborted trials kept as trace material |
| P10 Git discipline | pass — small discrete commits; no push |

Zero violations.

## Approval
> [auto-answer] design approval: approved (recommended approach C) — autonomous mode; user pre-approved the W1-W4 plan with "+"; zero constitution violations; falsifiable pins + prediction registered — 2026-07-13
