---
name: krukit-grill
description: Interrogate a feature idea against recon findings and the project's domain model before any design work. Use when the user says "krukit-grill", "крукіт гриль", or wants the idea grilled after recon. Stage 2 of the krukit pipeline.
---

# Krukit Grill

Stage 2 of 7 in the krukit pipeline: recon → grill → design → plan → act → verify → review. Takes the recon map produced by krukit-recon and interrogates the stated idea against it — resolving every open question and every contradiction between what the user wants and what the code and docs actually say, before krukit-design spends effort on it.

Interact with the user in the user's language.

## Inputs

- `docs/krukit/<feature-slug>/context.md` — recon output from krukit-recon. **Required.** If missing, tell the user and run krukit-recon first; do not grill without it.
- `docs/krukit/<feature-slug>/flow-state.md` — pipeline state. If absent (standalone invocation), create the folder and file per the flow-state contract:

  ```markdown
  # Krukit Flow: <feature-slug>
  Started: YYYY-MM-DD | Route: full
  - [ ] 1 recon
  - [ ] 2 grill
  - [ ] 3 design
  - [ ] 4 plan
  - [ ] 5 act
  - [ ] 6 verify
  - [ ] 7 review
  ```

  Set Route to the single applicable value (standalone default: full).

## Process

1. Read `flow-state.md` (create as above if standalone) and `context.md`. If `context.md` is missing, stop and route the user to krukit-recon. Locate the project's domain model (a `CONTEXT.md` glossary, or `CONTEXT-MAP.md` in multi-context repos) and its ADR location.

2. **Seed the interrogation** with the recon findings: Goal, Affected map, Patterns to follow, Invariants, Risks from `context.md`. If `docs/krukit/<feature-slug>/discovery.md` exists with `Status: confirmed`: treat its Decisions and Definition of Done as already-answered — re-open one ONLY when recon findings or code contradict it, presenting the contradiction as evidence — and add its Open questions to the grilling queue. When a resolved grill decision changes a DoD field, re-confirm that field with the user and amend discovery.md's DoD in place with provenance (`amended YYYY-MM-DD during grill: <reason>`, original quote preserved).

3. **Interrogate, one question per turn.** Start from the **Open questions** section of `context.md` (plus discovery.md Open questions, if any), then walk the rest of the decision tree depth-first, resolving dependencies as they surface. For each question, offer your own recommended answer and make the user react to it — a default to push against surfaces more than an open prompt. While grilling:
   - **Prefer code over questions.** When a question is answerable by reading the code, inspect it instead of asking.
   - **Cross-reference claims.** When the user asserts something about existing behavior, check it against the Affected map and Invariants before accepting it; if it contradicts the codebase, surface the contradiction immediately rather than letting it pass.
   - **Sharpen terminology.** When the user's wording conflicts with the CONTEXT.md glossary, call it out and force a single canonical term before moving on — no fuzzy term survives into design.
   - **Stress-test.** Invent concrete edge cases to probe the boundaries of the idea against the domain.

4. Track each Open question to one of two terminal states: **resolved** (decision recorded) or **deferred** (with an explicit reason). No silent drops.

5. **Update the docs inline.** As terms crystallize, resolve them in `CONTEXT.md` (glossary only — no specs, scratch, or implementation detail), keeping every entry in a consistent term → definition shape. Record an ADR only when a decision is all three of: hard to reverse, surprising without context, and the result of a real trade-off — otherwise skip it; keep ADRs in a consistent context / decision / consequences shape.

6. On completion, append a short **Grill summary** to `flow-state.md`: resolved decisions, sharpened terms, created ADRs, deferred questions with reasons.

7. If the gate passes, tick the stage row in `flow-state.md`:

   ```markdown
   - [x] 2 grill — done YYYY-MM-DD, artifact: flow-state.md
   ```

## Outputs

- **Grill summary** section appended to `docs/krukit/<feature-slug>/flow-state.md`.
- `CONTEXT.md` updated inline where terminology was sharpened.
- ADRs in the project's ADR location, only where the decision met the bar.
- Stage 2 checkbox ticked in `flow-state.md`.

## Gate

All must be true before the stage is complete. If any fails, state what failed and stop — do not proceed to krukit-design.

- [ ] No unresolved contradiction remains between the stated idea and the code or docs.
- [ ] Every Open question from `context.md` — and from `discovery.md`, if present — is resolved or explicitly deferred with a reason.
- [ ] Grill summary appended to `flow-state.md`.
