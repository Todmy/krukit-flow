# Context: deadline-aware-execution

## Goal
Extend the Layer-0 "deliverable gate" invariant in `skills/krukit-flow/SKILL.md` with proactive deadline-aware behavior so a wall-clock timeout can no longer kill the agent before it materializes a best-effort deliverable — targeting the 3 compute/search-bound hard tasks that flapped PASS→timeout between krukit-v3 r1 and r2.

## Affected map
| File | Role | Who depends on it |
|---|---|---|
| `skills/krukit-flow/SKILL.md` (92 lines, 11,114 B) | Canonical Layer-0 invariants (L10–15) + Autonomous mode (L17–23). Insertion point: after deliverable-gate bullet L15 | Every session of every user; vendored to bench conditions; restated (names only) in P5 + CONTEXT.md |
| `scripts/lint-consistency.py` (L65–69) | Pins krukit-flow section **headings** only (tuple on L67); bullet text is NOT independently protected | CI/relevant-test for structural skill edits (P1, P8) |
| `docs/krukit/constitution.md:10` (P5) | Hand-restates invariant **names** (`snapshot-before-touch, deliverable gate, never-fabricate`) — NOT lint-covered | Drift risk MEDIUM: mirror only if a NEW named invariant is added |
| `CONTEXT.md:8` (glossary) | Hand-restates invariant names — NOT lint-covered | Drift risk MEDIUM: same condition as P5 |
| bench: `run.sh` L27–34, `Makefile` L16, `status.py` L8 | 3 sources of truth defining a condition; `vendor/krukit-v3/` = flat copy of `skills/` @ 0f6a63c, pin in `vendor/PINS.txt` | The A/B grid; krukit-v4 = new condition (P9) |

## Patterns to follow
- **Layer-0 bullet shape** (L14–15): `- **<Name>.** <one imperative rule> <one sharp rationale/failure-mode>.` Terse, imperative, one failure-mode clause. Match it.
- **Lint pin for load-bearing structure** (L67 tuple): protection = exact heading/substring must be present in the file. A bare bullet under an existing heading is unprotected — to pin the deadline rule (P8), add a **distinctive substring assertion** for its bold lead phrase, OR give it a `###` subheading string in the tuple. Recommend a substring assertion on the bold lead (keeps the flat bullet shape, no new heading).
- **Route enumeration is regex-parsed** (lint L74–75): do NOT reword L12's `EVERY route — trivial, direct, fix, full, external-spec —`, and do NOT introduce a markdown table whose first cell is a bare lowercase token inside the new rule (would register a phantom route).
- **New bench condition** (mirror how v3 was made): `cp -r skills vendor/krukit-v4`; append `vendor/PINS.txt` (`krukit-v4  local:/Users/todmy/github/krukit  @ <sha>  (Wave 3: deadline-aware)`); `cp conditions/krukit-v3.md conditions/krukit-v4.md`; add `"krukit-v4:vendor/krukit-v4:"` to run.sh CONDITIONS, `krukit-v4` to Makefile L16 and status.py L8. Run: `make krukit-v4-hard`.

## Invariants (must not break)
- **Constitution P5** — Layer-0 may not be WEAKENED; extending/strengthening is allowed and expected. The deadline rule must strictly add obligation, never relax snapshot/deliverable/never-fabricate.
- **P2 prompt budget** — flow SKILL.md grows; the addition must be tight (one bullet + optional autonomous-mode clause) and justify its recurring cost in the commit message; compression elsewhere preferred if room is tight.
- **P4 resume-compat** — flow-state.md format is untouched by this change (no new required header/rows); existing running flows must parse unchanged.
- **P8 structure-pinned-by-lint** — if the deadline rule is load-bearing (it is: Layer-0), it must be lint-pinned, and the pin must be proven red→green (P1).
- **P9 pinned-vendor** — `vendor/krukit-v3/` is frozen; changes land only as `krukit-v4`. Never edit v3.
- **P1 falsifiable edits** — structural change lands with a red→green lint proof; behavior change records a falsifiable bench prediction BEFORE implementation (the flappy-3 timeout→committed-answer criterion).

## Risks
- **No wall-clock readout.** The agent cannot reliably read "time remaining," so the rule must be a *behavioral heuristic* ("materialize the deliverable early, then improve"), not a timer/percentage — a timer would be un-actionable and un-verifiable (violates P7 rules-not-scores if phrased numerically).
- **Over-scoping the floor.** `bound-every-subprocess` is tactical; forcing it into Layer-0 (which applies to EVERY route incl. trivial) may bloat the floor a weaker model must execute (P6 knobs-earn-existence). Grill must decide: universal Layer-0 vs. an autonomous-mode/compute-task clause.
- **Silent drift.** P5 (constitution) and CONTEXT.md restate invariant names outside lint coverage. Adding a *new named* invariant obligates mirroring both; extending the deliverable-gate wording (no new name) avoids that but may be less discoverable.
- **Unfalsifiable behavior claim.** Prompt-code "improvements" are only honest if bench-tested. n=2 diagnosis on 3 tasks — krukit-v4 is itself the n=3 probe; the exit criterion must be pre-registered, not judged post-hoc.

## Open questions (→ grill)
1. **Placement** — new third Layer-0 bullet after L15 (recon's recommendation, keeps it adjacent to the gate it extends) vs. extend the deliverable-gate bullet's wording vs. an Autonomous-mode-only clause? Trade-off: Layer-0 = universal + pinnable but heavier; autonomous-only = lighter but misses interactive long tasks.
2. **Phrasing without a clock** — how to word "commit a best-effort deliverable before the deadline" as a behavioral trigger with no timer (e.g. "the moment you have ANY answer better than empty, write it; treat every long/looping op as if it may be your last")?
3. **Scope** — all routes (true Layer-0), or gated to compute/search/long-running tasks (direct + full)? trivial/fix rarely hit timeouts.
4. **`bound-every-subprocess`** — is it Layer-0-universal, or too tactical for the floor (belongs in act's TDD guidance / autonomous mode instead)?
5. **Lint pin** — substring assertion on the new rule's bold lead phrase (recommended, keeps flat bullet) vs. `###` subheading; and: new NAMED invariant (mirror P5 + CONTEXT.md) vs. extend deliverable-gate (no mirror needed)?
