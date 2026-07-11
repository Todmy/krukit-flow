---
name: krukit-act
description: Execute a krukit implementation plan task by task under TDD discipline, with fresh-context execution per task and root-cause debugging on failure. Use when the user says "krukit-act", "крукіт act", or "крукіт акт", or when stage 5 runs inside /krukit-flow. Stage 5 of the krukit pipeline.
---

# Krukit Act

Stage 5 of 7 in the krukit pipeline: recon → grill → design → plan → act → verify → review. Takes the approved `plan.md` and implements it task by task under strict TDD, executing each task in a clean context and resolving every unexpected failure by root cause rather than guesswork. Interact with the user in the user's language.

## Inputs

| Input | Path | Required |
|---|---|---|
| Plan | `docs/krukit/<feature-slug>/plan.md` | Full route: yes — if missing, run krukit-plan first and stop. Fix route (flow-state `Route: fix`): absent by design — see step 2 |
| Recon invariants | `docs/krukit/<feature-slug>/context.md` (Invariants section) | Recommended — note if absent, continue |
| Flow state | `docs/krukit/<feature-slug>/flow-state.md` | Read if exists; create if standalone (step 1) |

## Process

1. **Load state.** Read the route from `flow-state.md`, then `plan.md` (full route) and the Invariants section of `context.md`. If `flow-state.md` is missing (standalone invocation), create it:

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

   Set Route to the single applicable value (standalone default: full; for a standalone small bugfix: fix).

2. **Build the task list.**
   - **Full route:** the task list is `plan.md`.
   - **Fix route** (`Route: fix` in flow-state — plan.md is absent by design; covers any small well-scoped change, not only bugs): derive a minimal inline task list from the change description — (1) failing test specifying the new/correct behavior, (2) minimal change, (3) refactor if needed. If a confirmed `discovery.md` exists, fold its Open questions into the task-list confirmation — each resolved or explicitly deferred before implementation. Persist it FIRST into flow-state.md under `## Act — inline task list` (survives interruptions; resume source), THEN confirm via ONE AskUserQuestion call that carries BOTH the task-list confirmation (content embedded in the question itself — option `preview` fields or the question text) AND, when the list is 3 tasks or fewer, the execution-mode pick from step 3 — one round, two questions. Assistant prose between tool calls may not be visible next to the question UI — the user must be able to read WHAT they confirm inside the prompt. Tick the list in flow-state.md as tasks complete.

3. **Pick execution mode.** Count the tasks:
   - **More than 3 tasks — fresh-context execution.** Run each task in its own clean context (a dedicated subagent per task) and review each task's result — for both spec compliance and code quality — before starting the next; fresh context per task keeps one task's noise out of the next. Three rules:
     - **Terminal step**: stop after the full test suite (step 7). Do NOT finish the branch or run the final independent review here — krukit-review (stage 7) owns both.
     - **`[mechanical]` tasks** (tagged in plan.md): skip the per-task review loop — tests still run, commit still per task. May be dispatched to a cheaper/faster model; the task is mechanical by definition, senior judgment isn't what it needs.
     - **`[P]` tasks** (tagged in plan.md — independent, disjoint file sets): may run as parallel subagents in a single message. Review their results together; commits stay one per task, applied in plan order. If two `[P]` tasks turn out to touch the same file, fall back to sequential — the tag was wrong; note it in Learnings.
     - **Worktrees are optional**: default to the current branch/workspace for solo work; create a worktree only when the user asks or parallel workstreams exist.
   - **3 or fewer — ask inline vs fresh-context**: first option "Inline (Recommended)" with description "subagent overhead isn't worth it for a small plan." On the fix route this pick is already folded into step 2's batched confirmation — do not ask again; on the full route ask it now via the `AskUserQuestion` tool. Run whichever the user picks, with the same terminal-step rule.

4. **Execute with TDD.** Every task follows red → green → refactor:
   - **Red:** write one minimal failing test for the next behavior; run it and confirm it fails for the right reason (not a typo or import error).
   - **Green:** write the simplest code that makes it pass; run the test and confirm it passes and nothing else broke.
   - **Refactor:** remove duplication and improve names while the tests stay green.

   Iron law: **no production code before a failing test.** If code gets written first, delete it and start from the test. A test that passes the moment you write it is testing existing behavior — fix the test, not the code. The Invariants from context.md MUST NOT break — treat them as untouchable while implementing.

5. **On any unexpected failure** (test fails for the wrong reason, behavior contradicts the plan, flaky output): find the root cause before changing anything. Read the error in full, reproduce it consistently, check what recently changed, and compare against a working example — find similar code that works, read it fully, and list the differences. Trace the bad value back to where it originates, instrumenting component boundaries with entry/exit logging when the origin isn't obvious. Form one hypothesis, state it, and test one variable at a time. No guess-and-retry. If three fixes in a row fail, stop and question the approach (likely an architectural assumption, not a hypothesis) — raise it with the user rather than attempting a fourth.

6. **Commit per task.** One small, discrete commit per completed task — single logical change each. Never push to remote without explicit user permission.

7. **Accumulate learnings** (only when the task list has more than one task — a single-task fix skips Learnings). After each completed task, if a codebase gotcha was discovered (quirky API, hidden coupling, surprising test setup), append it as one line to a `## Learnings` section — at the bottom of plan.md (full route) or under `## Act — inline task list` in flow-state.md (fix route, which has no plan.md) — and include that section in every subsequent task's context — later tasks must not re-debug the same quirks. Append-only, dies with the feature.

8. **Finish.** Tick every completed task checkbox (plan.md on the full route, the inline list on the fix route). Run the FULL test suite and read the actual output — do not infer success from a subagent's claim.

9. **Update flow state.** On gate pass, tick the stage row in flow-state.md:

   ```markdown
   - [x] 5 act — done YYYY-MM-DD, artifact: plan.md
   ```

## Outputs

- Implemented code, one commit per task (not pushed).
- `plan.md` with all task checkboxes ticked.
- `flow-state.md` stage 5 ticked with the done line.

## Gate

All of these MUST be true before the stage is complete:

- [ ] Every task ticked — in plan.md (full route) or in the inline task list (fix route).
- [ ] Full test suite was run and is passing — actual output read, not assumed.
- [ ] One commit per task exists; nothing pushed without permission.
- [ ] If codebase gotchas were found during execution AND the task list has more than one task, the `## Learnings` section exists (plan.md on the full route, flow-state.md on the fix route).

After the items above pass, tick row 5 in flow-state.md (step 9) — the tick is the post-gate action, not a gate condition.

If any condition fails: state exactly what failed and stop. Do not silently proceed to krukit-verify.
