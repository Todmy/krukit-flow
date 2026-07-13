# Krukit Flow: deadline-aware-execution
Started: 2026-07-13 | Route: full | Mode: autonomous
Task: Extend Layer-0 with deadline-aware execution (deliverable-before-deadline, background-and-parallelize, bound-every-subprocess) — from krukit-v3 hard-grid timeout analysis
- [x] 1 recon — done 2026-07-13, artifact: context.md
- [x] 2 grill — done 2026-07-13, artifact: flow-state.md
- [x] 3 design — done 2026-07-13, artifact: design.md
- [x] 4 plan — done 2026-07-13, artifact: plan.md
- [x] 5 act — done 2026-07-13, artifact: plan.md (T1 red→green 787428b→53767bd, T2 b3539bb, T3 no-op/symlink)
- [x] 6 verify — done 2026-07-13, artifact: verify.md
- [x] 7 review — done 2026-07-13, artifact: flow-state.md

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

## Review summary (2026-07-13)
Independent fresh-context review of 32cb567..HEAD: **0 Critical / 2 Important / 4 Minor**. Reviewer independently re-proved the lint red→green (stripped bullet → exit 1 with pinned message; restored → exit 0/11 skills, correctly scoped to krukit-flow only) and traced bench wiring end-to-end.

Resolutions (every finding, on merits):
- **I-1 FIXED (by documentation)** — v3→v4 vendor confound (wave-2 krukit-act fix 377670e rides along): recorded next to the pre-registered prediction in verify.md (7ed9b99) and in bench vendor/PINS.txt. Re-pinning v3 rejected (P9 would destroy existing grid data).
- **I-2 FIXED** — "launch first" vs "snapshot first" ordering race: bullet now reads "After any required snapshot, launch the expensive job early and backgrounded" (5341a4a); design.md quote amended with provenance. Also dissolves M-4.
- **M-1 RECORDED** — substring pin guards deletion, not body-weakening; consistent with sibling bullets (Deliverable gate isn't body-pinned either), P8 satisfied. Do not over-trust the pin as a P5 guard.
- **M-2 DECLINED** — keep "instead of busy-waiting": it names the exact observed failure mode (password-recovery sleep-poll loops); the 3 words anchor the anti-pattern for a weaker model.
- **M-3 FIXED (bench)** — status.py help hint now lists krukit-v3/krukit-v4 (my edit had made the stale hint staler).
- krukit-v4 re-vendored at final HEAD 7ed9b99 (never run → refresh before first use is P9-clean); pin updated.

Branch outcome: work done directly on main (established wave pattern, no feature branch, no worktrees created); final lint green on merged-equivalent state; NOTHING pushed.
> [auto-answer] branch options: keep on main as committed, no push — autonomous mode; matches v2-wave1/v2-wave2 precedent — 2026-07-13
> [auto-answer] constitution close: approve P5 enumeration amendment (1.0.0→1.1.0, adds "deadline gate") — deferred here by grill Q5 as the proper amendment channel; refines an existing principle, no new principle added — 2026-07-13
Knowledge capture: no .valis.json in repo → Valis capture skipped silently (per skill contract).
