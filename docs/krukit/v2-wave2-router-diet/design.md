# Design: v2-wave2-router-diet

Date: 2026-07-11 | Route: full | Sources: context.md, Grill summary (5 decisions), cap-override clarification ("Cap за режимом")

## Approaches considered

- **A. Surgical in-place edits (RECOMMENDED).** Route row + reference updates + capability/log rules inline in krukit-flow; act/verify/README edited in place. Minimal prompt growth (P2), no new load-bearing prompt files (route-log.md is data, not instructions), drift surface unchanged (P8).
- **B. Stage-0 extraction.** Routing as its own skill/section + slim fix-route instruction variants as separate files. Cleaner separation but: new files = new drift surface needing pins, more loaded prompt bytes, and "slim variants" is a knob without a second trace (P6).
- **C. JSON route telemetry.** Machine-first log format. Overkill: a one-line markdown append is greppable by miner and bench; structure can be added when a consumer demands it (P6).

A chosen. B's "slim variants" idea recorded as a Wave-4 candidate only.

## 1. Route table v2 (skills/krukit-flow/SKILL.md)

New row (after `trivial`), plus `+ log the route` appended to trivial's Stages cell:

| Route | When | Stages |
|---|---|---|
| direct | task is NOT feature work — forensics/recovery, ops/investigation, puzzle/algorithmic one-off — pipeline stages don't fit regardless of size | no pipeline — do the work directly, verify against the task's own success criteria; Layer-0 invariants apply; log the route |

Reference updates (all 9 + README:9, from context.md): Invariants enumeration L12 adds `direct`; step 2 "four routes" → "five routes"; gate L85 adds direct to "produce no flow-state by design"; discovery-routing L47: when a confirmed discovery.md exists, `direct` is NOT offered (discovery implies feature work; minimum stays fix). Steps 3/4/6/10 unchanged (direct produces no flow-state).

## 2. Capability self-check (folded into Stage 0, no extra rounds)

Before presenting routes, read the **harness-declared model name** (system prompt / env). Never ask the model to rate its own capability (P7; self-report miscalibration). Below Sonnet-class (Haiku-class or unknown lightweight tier):

- **Autonomous mode:** hard cap — `full` is not offered and not chosen; route-log line notes `(cap: below-bar)`.
- **Interactive mode:** `full` stays visible with an explicit warning in its description; the user's explicit pick is an override, logged as `full (override: below-bar)`.
- Unknown model name: autonomous → treat as below-bar (safe default); interactive → note "tier unknown" in the warning.

## 3. Route-log contract (docs/krukit/route-log.md)

Append-only, created on first use, one line per Stage-0 decision, EVERY route:

```
YYYY-MM-DD | <task one-liner> | <route> | <reason>
```

Telemetry only: nothing parses it for state (flow-state header remains the state source — P4-safe). Write failure is non-fatal: note it and continue; telemetry never blocks work.

**New lint check (P8, red→green per P1):** route-name consistency — the route set in the krukit-flow table == the Invariants-section enumeration == README's route enumeration. Catches the "added a route in one place" drift class.

## 4. Act/flow diet

- **flow:** step 5 (TodoWrite) REMOVED; step 7 "update the todo" and step 1 "recreate todos" re-pointed at flow-state rows. Flow-state becomes the single tracker (also fixes no-todo-tool harnesses, IMPROVE-LOG c1).
- **act (fix route):** persist-first unchanged; the task-list confirmation and the inline-vs-fresh-context pick become ONE AskUserQuestion call (two questions, one round). >3-task case keeps fresh-context execution without asking (unchanged).
- **act step 7:** Learnings appended only when the task list has >1 task.
- **commit-per-task:** unchanged (P10).

Projected fix-route saving: −1 user round, −2..4 todo calls, −1 write on single-task fixes; combined with §5 targets the ≤2×-baseline goal.

## 5. Verify exact-oracle rule (skills/krukit-verify/SKILL.md)

One SHOULD sentence in step 2: *when an exact oracle exists (byte-identical diff, golden file) and it passes fresh, one verification cycle suffices — do not re-run variations of the same proof; name the oracle in verify.md.* Recorded in krukit-verify IMPROVE-LOG as a candidate pending a second DISTINCT trace (P6 honesty). Full risk-matrix: deferred (Wave 4).

## 6. README

- New `## Requirements` section (after "What it is"): full route needs a Sonnet-class or stronger model (below-bar behavior per §2); assumes a skills-capable harness with arrow-key questions (AskUserQuestion) for interactive gates.
- P3 mini-compliance: the three sourced claims ("12 validated pain points", "six tools", "most-reacted") gain a source pointer + collection date; "simpler to use, clearer to follow, and lighter to run" is rewritten as a mechanism claim (what krukit does differently), not an unmeasured comparative.

## Error handling

- route-log unwritable → non-fatal note, continue.
- Model name absent → §2 unknown-tier defaults.

## Testing / falsifiable predictions (P1)

1. Lint route-consistency check: RED on current tree (README enumeration lacks `direct`) → GREEN after edits.
2. Existing flow-states (wave1, wave2) still parse: resume semantics unaffected (P4) — checked by re-reading with the updated instructions.
3. Bench (stage 6, krukit-v2 re-vendor): (i) cobol-modernization fix-route cost ≤ 2× baseline ($0.48 → ≤ $0.96-1.00); (ii) hard-pair password-recovery + write-compressor: route-log line exists with direct/trivial, no pipeline ceremony in trace, Layer-0 honored; (iii) optional if budget allows: haiku cobol — route-log shows `(cap: below-bar)`, no full route.

## Definition of Done

All 5 grill decisions implemented (files per Affected map); lint green including the new route-consistency check; README updated; stage-6 bench predictions (1)-(2) and (3.i)-(3.ii) met; constitution check below has zero violations.

## Constitution check

| Principle (MUST) | Verdict |
|---|---|
| 1 Falsifiable edits | pass — predictions §Testing recorded before act |
| 2 Prompt budget | pass — flow grows ~12 lines (route row + cap + log), flow/act shrink ~10 (todo steps, learnings rule); README not session-loaded; commits justify each |
| 3 Proof or silence | pass — README rewrite IS the compliance work |
| 4 Resume compatibility | pass — additions only: new route value (absent from old files), new data file; no renames/removals of parsed markers |
| 5 Layer-0 untouchable | pass — floor text unchanged; direct ADDED to its enumeration; invariants apply on direct explicitly |
| 6 Knobs earn existence | pass — direct: 2 skip + 3 light hard-grid traces; cap: 3 Haiku damage traces; oracle rule: SHOULD + candidate marker (borderline, honestly labeled) |
| 7 Rules, not scores | pass — categorical tier rule from harness declaration; no numeric scores anywhere |
| 8 Structure pinned by lint | pass — new route-consistency lint check pins the enumerations |
| 9 Pinned-vendor benchmarking | pass — edits land in repo; bench measures them as re-vendored krukit-v2; pinned v1 untouched |
| 10 Git discipline | pass — one commit per deliverable planned; no push |
