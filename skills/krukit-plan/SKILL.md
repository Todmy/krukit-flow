---
name: krukit-plan
description: Turn an approved krukit design into a bite-sized, TDD-ready implementation plan. Use when the user says "krukit-plan", "крукіт план", or asks to plan implementation of a krukit feature. Stage 4 of the krukit pipeline.
---

# Krukit Plan

Stage 4 of 7 in the krukit pipeline: recon → grill → design → plan → act → verify → review. Converts the approved `design.md` into a `plan.md` an engineer with zero prior context could execute: a scoped, file-mapped, bite-sized task list where each task carries its behavior contract and test cases. Planning only — krukit-act (stage 5) owns execution.

Interact with the user in the user's language.

## Inputs

- `docs/krukit/<feature-slug>/design.md` — approved design (required). If missing, tell the user to run krukit-design first and stop.
- `docs/krukit/<feature-slug>/context.md` — recon output with Invariants and Affected map (use if present; note its absence if not).
- `docs/krukit/<feature-slug>/flow-state.md` — pipeline state. If missing (standalone invocation), create the folder and file:

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

1. Read `flow-state.md` (create as above if standalone). Read `design.md` and `context.md`.

2. **Scope check.** If the design spans multiple independent subsystems, flag it and suggest splitting into separate plans rather than one sprawling file.

3. **Map the work.** Write `docs/krukit/<feature-slug>/plan.md` with:
   - **Header** — goal, target architecture, tech stack, and global constraints, carried verbatim from design.md. List the Invariants from `context.md` as an explicit "MUST NOT break" block (or note context.md is absent).
   - **Task list** — decompose into bite-sized tasks (a few minutes each, one logical change apiece). For each task give: the files it creates / modifies / tests; the interfaces it consumes and produces with exact signatures; and the behavior contract plus named test cases.

4. **Apply the krukit task conventions** while writing the task list:
   - Any task touching a file in the Affected map of `context.md` must name and follow the pattern that `context.md` prescribes for it.
   - **Behavior contract, not full code.** Tasks specify the behavior contract + named test cases; include code blocks only for signatures, interfaces, and genuinely non-obvious algorithms — never full function bodies the executor can derive from the contract. plan.md is re-read by every fresh subagent in stage 5, so bloat is paid N times. A contract must be specific and testable: "add appropriate error handling" or "handle the edge cases" is vague prose, not a contract, and counts as a placeholder.
   - **Tag mechanical tasks** with `[mechanical]` in the title (renames, config changes, boilerplate moves) — krukit-act runs them without the per-task review loop and may use a cheaper/faster model.
   - **Tag parallel-safe tasks** with `[P]` in the title (no mutual dependency, disjoint file sets) — krukit-act may run them as parallel subagents.
   - **Unresolved decision slots are never bare placeholders.** If a decision can't be made from design.md/context.md, ask the user (AskUserQuestion, problem-first, recommended option first). ONLY if the user explicitly said "all recommended" for this run may you fill the slot with your recommended value — marked `(auto-accepted recommendation)` so it's visible at the gate. A TODO/TBD without either a user answer or that marker is a plan failure.

5. **Self-review the plan** and fix inline: spec coverage (every `design.md` requirement maps to a task), placeholder scan, type consistency across tasks. The placeholder scan applies to code blocks and unresolved decision slots — behavior-contract prose in task bodies is NOT a placeholder. The plan stops here; it offers no execution options and invokes no executor — krukit-act owns that.

6. On gate pass, update `flow-state.md`: tick `- [x] 4 plan` and append ` — done YYYY-MM-DD, artifact: plan.md` to that row.

## Outputs

- `docs/krukit/<feature-slug>/plan.md` — TDD implementation plan, consumed by krukit-act (stage 5).
- Updated `flow-state.md` with stage 4 ticked.

## Gate

- [ ] `plan.md` exists at `docs/krukit/<feature-slug>/plan.md`.
- [ ] Self-review passed (spec coverage, placeholder scan, type consistency).
- [ ] Every requirement in `design.md` maps to a task in `plan.md`.
- [ ] Zero placeholders in `plan.md` — no TODO/TBD/`...` stubs in code blocks or unresolved decision slots; behavior-contract prose is not a placeholder, and slots filled as `(auto-accepted recommendation)` are valid ONLY if the user explicitly said "all recommended" this run.
- [ ] Plan header lists the `context.md` invariants as MUST NOT break (or notes context.md is absent).

If any item fails: state what failed and stop. Do not tick flow-state or proceed to krukit-act.
