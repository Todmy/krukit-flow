# Krukit Flow: deadline-aware-execution
Started: 2026-07-13 | Route: full | Mode: autonomous
Task: Extend Layer-0 with deadline-aware execution (deliverable-before-deadline, background-and-parallelize, bound-every-subprocess) — from krukit-v3 hard-grid timeout analysis
- [x] 1 recon — done 2026-07-13, artifact: context.md
- [x] 2 grill — done 2026-07-13, artifact: flow-state.md
- [ ] 3 design
- [ ] 4 plan
- [ ] 5 act
- [ ] 6 verify
- [ ] 7 review

> [auto-answer] Stage-0 route: full — edits Layer-0 (P5), load-bearing, needs design + bench validation; user directive "зроби ці покращення" — 2026-07-13
> [constitution] v1.0.0, 10 principles — loaded (krukit-rules open mode: existing constitution → no-op, no changes proposed)

## Grill summary (2026-07-13)
Resolved all 5 Open questions; code cross-checked; two stress-tests sharpened the wording.

- **[auto-answer] Q1 placement**: new third Layer-0 bullet "Deadline gate" after L15 — the observed failure (password-recovery timeout) was on the DIRECT route, so autonomous-only/full-only placement would miss it; Layer-0 (route-independent) is the correct home. Rejected extend-deliverable-gate (less pinnable) and autonomous-only (misses direct+interactive long tasks). — 2026-07-13
- **[auto-answer] Q2 phrasing**: behavioral heuristic, no numeric timer (P7) — "the moment you have any result better than empty, write the declared deliverable to disk and improve it in place; never let it exist only inside a process a timeout can kill." Trace-verifiable. — 2026-07-13
- **[auto-answer] Q3 scope**: Layer-0 universal, but bullet wording self-scopes to "long-running / search / compute-bound work" → inert for trivial/quick tasks (P6 floor-bloat addressed without narrowing route coverage). — 2026-07-13
- **[auto-answer] Q4 bound-every-subprocess**: folded into the deadline-gate bullet as one clause, NOT a separate floor invariant — single added bullet (P2/P6); the torch hang is the same failure family (deliverable stranded in a hung process). — 2026-07-13
- **[auto-answer] Q5 lint pin + drift**: dedicated substring assertion on `**Deadline gate.**` in lint (heading-tuple doesn't cover bullets), proven RED→GREEN (P1/P8). New named invariant → mirror into CONTEXT.md:8 glossary (act task); DEFER constitution P5 enumeration to krukit-rules CLOSE (proper amendment channel, not a mid-flow hand-edit). Lint doesn't cross-check P5/CONTEXT, so no lint dependency either way. — 2026-07-13

Code cross-checks: insertion anchor L15 confirmed; `- **Deadline gate.**` bullet produces no table-row match → invisible to lint route-name regex (L74-75); does not touch L12 route enumeration. ✓

Stress-tests (sharpened wording for design):
- **Composes with snapshot-before-touch**: "launch long work first" applies to expensive COMPUTE (render/search/build), never to skipping the snapshot on irrecoverable state — the other invariants still fire first.
- **Composes with never-fabricate**: "write the deliverable early" = best-effort from what is *verified so far*, clearly marked partial — never a plausible-but-unverified guess.

Canonical term: **Deadline gate** (pairs with Deliverable gate). No ADR (real trade-off but not surprising/hard-to-reverse — recorded here).
Deferred: constitution P5 enumeration mirror → krukit-rules close mode (step 10).
