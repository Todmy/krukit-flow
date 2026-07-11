---
name: krukit-design
description: Turn a grilled feature idea into an approved design doc through budgeted clarification, approach exploration, and a constitution check. Use when the user says "krukit-design", "крукіт дизайн", or asks to design a feature inside the krukit pipeline. Stage 3 of the krukit pipeline.
---

# Krukit Design

Stage 3 of 7 in the krukit pipeline: recon → grill → design → plan → act → verify → review. Turns the grilled idea into an approved `design.md` through a collaborative design dialogue — a budgeted clarification phase, exploration of approaches with trade-offs, a sectioned design, a constitution check, and an explicit approval gate. No implementation and no planning begin here; krukit-plan (stage 4) owns the transition to planning.

Interact with the user in the user's language.

## Inputs

- `docs/krukit/<feature-slug>/context.md` — recon output (Affected map, Patterns, Invariants, Open questions). If missing, tell the user and suggest running krukit-recon first; proceed only if they insist.
- Grill outcomes — resolved decisions from stage 2, recorded in flow-state.md and CONTEXT.md/ADRs. Optional but expected on the full route.
- `docs/krukit/<feature-slug>/discovery.md` with `Status: confirmed` — optional; its Decisions and Definition of Done count as already-answered questions.
- `docs/krukit/<feature-slug>/flow-state.md` — read it if it exists; if invoked standalone, create the folder and file:

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

## Process

1. **Load context.** Read context.md, the Grill summary in flow-state.md, any ADRs created by the grill, and — if present with `Status: confirmed` — discovery.md (Decisions + Definition of Done). These count as already-answered questions — do not re-ask them.

2. **Budgeted clarification.** Before proposing anything, scan the idea for ambiguity across these categories: scope/behavior, domain & data, UX flow, non-functional, integrations, edge cases, constraints, terminology, completion signals. Mark each Clear / Partial / Missing. Budget = 2 + (number of Partial or Missing categories), hard cap 10.
   - Ask one question at a time via the `AskUserQuestion` tool (arrow-key form): recommended option FIRST with label ending "(Recommended)" and the reason in its description; ≤ 4 options.
   - Skip anything context.md, the grill session, or a confirmed discovery.md already answers — when discovery.md exists, pre-mark the categories it covers (typically completion signals, scope/behavior, constraints) as Clear.
   - Stop early once critical ambiguity is resolved or the user says done. Never exceed the budget.

3. **Explore approaches.** Propose 2–3 viable approaches with their trade-offs and a clear recommendation. Ground each in the recon findings — an approach that breaks an Invariant or ignores a Pattern from context.md is not viable and is not offered.

4. **Draft the design.** Write the recommended design to `docs/krukit/<feature-slug>/design.md`, in sections scaled to the feature's complexity — architecture, components, data flow, error handling, testing. Design for isolation and clarity: components with clear boundaries and explicit interfaces, each unit doing one thing and testable on its own; if a module would end up doing too much, split it. Apply YAGNI — design only what the grilled idea needs, nothing speculative. A straightforward feature needs a few sentences per section; a nuanced one needs more — and for a complex design, walk the user through it section by section and confirm as you go rather than waiting for one final verdict. State a Definition of Done explicitly (or inherit it from a confirmed discovery.md). No code is written in this stage.

5. **Self-review the design.** Re-read design.md and fix inline: placeholders/TBDs, internal contradictions, ambiguous terms, scope that drifted beyond the grilled idea.

6. **Constitution check.** Find the constitution in this order: `.specify/memory/constitution.md` → `docs/krukit/constitution.md` → project `CONTEXT.md` principles section → none. Append a `## Constitution check` section to design.md:

   | Principle (MUST) | Verdict |
   |---|---|
   | <principle> | pass / VIOLATION: <what> |

   A violation must change the design — revise design.md and re-check. Never argue a violation away. If no constitution exists, write "No constitution found (checked all discovery locations)" in the section and continue.

7. **Approval.** Present the final design.md to the user. Hard gate: NO implementation, no planning, no code before explicit user approval.

8. **Commit** design.md (one discrete commit, e.g. `docs: design for <feature-slug>`). Never push without explicit permission.

9. **Update flow-state.** Tick the stage row and append the done marker:

   `- [x] 3 design — done YYYY-MM-DD, artifact: design.md`

## Outputs

- `docs/krukit/<feature-slug>/design.md` — approved design doc with a `## Constitution check` section, committed.
- Updated `flow-state.md` with stage 3 ticked.

## Gate

All must be true before the stage is complete. If any fails, say what failed and stop — do not silently proceed.

- [ ] User explicitly approved the design
- [ ] design.md exists at `docs/krukit/<feature-slug>/design.md` and is committed
- [ ] `## Constitution check` section present with zero unresolved violations (or noted absence of a constitution)

After the items above pass, tick row 3 in flow-state.md (step 9) — the tick is the post-gate action, not a gate condition.
