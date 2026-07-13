---
name: krukit-verify
description: Proves a feature is actually done — runs evidence-based verification plus a read-only reality check of design/plan artifacts against the real code, producing verify.md. Use when the user says "krukit-verify", "крукіт verify", asks to verify a krukit feature, or stage 5 (act) has just finished. Stage 6 of the krukit pipeline.
---

# Krukit Verify

Stage 6 of 7 in the krukit pipeline: recon → grill → design → plan → act → verify → review. Proves the feature is done with fresh evidence, then runs a reality-check pass that catches drift between the approved artifacts and what the code actually does. Interact with the user in the user's language.

## Inputs

- `docs/krukit/<feature-slug>/` with `design.md` and `plan.md` (best case). If either is missing (fix route, skipped stages), note it and verify against whatever exists.
- Implemented code from stage 5 (krukit-act).
- `flow-state.md` if it exists; if invoked standalone, create the folder and file:

  ```markdown
  # Krukit Flow: <feature-slug>
  Started: YYYY-MM-DD | Route: full
  Task: <one-line description + issue ref>
  - [ ] 1 recon
  - [ ] 2 grill
  - [ ] 3 design
  - [ ] 4 plan
  - [ ] 5 act
  - [ ] 6 verify
  - [ ] 7 review
  ```

  Set Route to the single applicable value (standalone default: full).
- Constitution, discovered in this order: `.specify/memory/constitution.md` → `docs/krukit/constitution.md` → project `CONTEXT.md` principles section → none (note its absence, continue).
- `docs/krukit/<feature-slug>/discovery.md` if it exists with `Status: confirmed` — the user-confirmed Definition of Done; its Validation plan is executed in step 2 (`Status: incomplete` files are never consumed).

## Process

1. Read `flow-state.md` (create folder + file if standalone). Confirm the feature slug and which artifacts exist.

2. **Verify by evidence, never from memory.** For each completion claim: identify the exact command that proves it, run that command fresh and in full, read the actual output (exit code, failure count), and only then state the claim with the evidence cited. Run the full test suite this way. Words like "should", "probably", or "seems to" are not verification — if you haven't read fresh output, you haven't verified. A regression fix must be shown red-then-green (the test fails when the fix is reverted). Three reminders hold the line: a passing linter is not a passing build (linter ≠ compiler), confidence is not evidence, and partial verification proves nothing — never declare done from satisfaction before the command output is in front of you. SHOULD: when an exact oracle exists (byte-identical diff, golden file) and it passes fresh, one verification cycle suffices — do not re-run variations of the same proof; name the oracle in verify.md. Reasoning in place of execution (a manual trace) is a last resort permitted only after an install attempt failed — and its conclusions are recorded as unverified, never as passing evidence.
   - If a confirmed `discovery.md` exists, also run its Definition of Done **Validation plan**, classifying each step three ways: machine-runnable (execute it), user-runnable now (hand it to the user as a checklist and record their verbatim reply), or infeasible in this environment (record as deferred with the user's explicit written sign-off — deferral is not a failure). Record each step's result in `verify.md`. A failed step is CRITICAL — the implementation contradicts the user's confirmed Definition of Done.

3. **Reality-check pass** — READ-ONLY analysis, no code changes. Compare `design.md` + `plan.md` + actual code:
   - Every file path referenced in `plan.md` exists or was explicitly created.
   - Every symbol design/plan treats as existing actually resolves — verify by searching the code, never from memory.
   - Each design requirement is implemented — spot-check by reading the code itself, not the plan.
   - Constitution MUST principles still hold in the implementation.
   - No vague placeholders or TODOs left in artifacts or new code.
   - No terminology drift between `design.md`, `plan.md`, and code.
   Delegate verbose searches to Explore subagents; keep raw dumps out of the main context.

4. Write `docs/krukit/<feature-slug>/verify.md`:
   - Findings table: `| ID | Severity (CRITICAL/HIGH/MEDIUM/LOW) | Location | Summary | Recommendation |`
   - Metrics line: requirements total / implemented / findings count.
   - Cap at 20 findings; aggregate the rest into one summary row.
   - CRITICAL = implemented behavior contradicts approved design, a constitution MUST is violated, referenced code does not exist, or a discovery Definition of Done Validation step failed.

5. Resolve findings: CRITICAL must be fixed (route fixes back through TDD discipline, small discrete commits, never push without permission). HIGH must be fixed or explicitly accepted by the user in writing — quote their acceptance in `verify.md`. MEDIUM/LOW are recorded for stage 7.
   - **Discovery amendment:** if a failed Validation step traces to a stale or wrong Definition of Done rather than the code, the user may amend `discovery.md` instead — the affected DoD field is re-confirmed individually (verbatim user quote, `amended YYYY-MM-DD during verify: <reason>`, original quote preserved), the amendment recorded in `verify.md`, and the plan re-executed. Never amend the DoD unprompted.
   - **Reopen rule:** if a CRITICAL finding shows the approved design (not the code) is wrong, the fix may — with explicit user approval — amend `design.md`/`plan.md` instead. Then untick the affected rows in flow-state.md as `- [ ] N <stage> — reopened YYYY-MM-DD (<reason>) [was: <previous marker>]` (preserve the prior done/skipped annotation in the `[was: ...]` part — provenance is never erased) and hand control back to krukit-flow to resume from the first reopened stage. Changes are never forced to masquerade as a new feature.

6. On gate pass, tick the flow-state checkbox:
   `- [x] 6 verify — done YYYY-MM-DD, artifact: verify.md`

## Outputs

- `docs/krukit/<feature-slug>/verify.md` — findings table + metrics line + any written HIGH acceptances.
- Updated `flow-state.md` with stage 6 ticked.
- Test-run evidence reported to the user (actual command + result summary).

## Gate

- [ ] Full test suite ran; output read, not assumed; all passing.
- [ ] If a confirmed `discovery.md` exists: every Validation plan step executed, user-answered, or deferred with written sign-off — all recorded in `verify.md`.
- [ ] `verify.md` exists with findings table and metrics line.
- [ ] Zero CRITICAL findings remain.
- [ ] Every HIGH finding fixed or explicitly accepted by the user in writing.

After the items above pass, tick row 6 in flow-state.md (step 6) — the tick is the post-gate action, not a gate condition.

If any condition fails: state exactly what failed and stop. Do not proceed to krukit-review.
