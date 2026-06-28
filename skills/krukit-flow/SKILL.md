---
name: krukit-flow
description: Orchestrates the full krukit feature pipeline end-to-end with task routing, stage gates, and resume. Use when the user says "krukit-flow", "krukit flow", "крукіт флоу", or "давай krukit flow", or wants the whole disciplined feature pipeline run on a task. Stage 0 (orchestrator) of the krukit pipeline.
---

# Krukit Flow

Orchestrator of the 7-stage krukit pipeline: recon → grill → design → plan → act → verify → review. It routes the task, then runs the stage skills in order, enforcing each stage's gate, recording state in flow-state.md, and supporting resume and per-stage skips. Stage skills own their own process and gates; this skill only sequences and records. Interact with the user in the user's language.

## Inputs

- A task description (feature, bugfix, or change) from the user.
- A feature slug — short kebab-case name; derive and confirm one if not given.
- Optional: existing `docs/krukit/<feature-slug>/flow-state.md` (resume case).
- Optional: `docs/krukit/<feature-slug>/discovery.md` — pre-flow output of `krukit-discovery`. If present with `Status: confirmed`, use it as the task description and Definition of Done source; do not re-ask what its Decisions already answer. `Status: incomplete` → treat as absent and offer to re-run krukit-discovery. Before deriving a fresh slug, glob `docs/krukit/*/discovery.md` for confirmed files without a sibling flow-state.md — an orphan is offered as the task candidate and its slug becomes the flow slug (never let a slug mismatch silently sever the discovery contract).

## Process

1. **Resume check.** If `docs/krukit/<feature-slug>/flow-state.md` exists with unticked boxes:
   - Resume point = the first row that is not ticked (done and skipped rows are both ticked `- [x]`).
   - On resume: read Route from the flow-state header — do not re-ask; recreate todos for the remaining stages; skip to step 5 at the resume point.
   - On declined resume: confirm, then overwrite flow-state.md and start over.
2. **Stage 0 — Route.** Classify the task with the user: one question via the `AskUserQuestion` tool (arrow-key form). Options = the four routes below, your recommended route FIRST with the label ending "(Recommended)" and the reason in its description. If invoked without a task description, derive the likely candidate task(s) from session context / the tracker FIRST and fold them into this SAME question (name the recommended candidate in the route-option descriptions, or ask one combined task+route question) — never spend a separate AskUserQuestion round on task selection alone.

   | Route | When | Stages |
   |---|---|---|
   | trivial | typo/config/one obvious file | no pipeline — do it + run the relevant test; no artifacts, no flow-state |
   | fix | small well-scoped change (bugfix or tiny feature), behavior known | 5 act (TDD) → 6 verify |
   | full | feature or change in existing code | 1→7 all stages |
   | external-spec | big greenfield where the spec is a human deliverable in Git | recommend spec-kit/OpenSpec, explain why, stop |

   **Discovery escape hatch:** if no confirmed `discovery.md` exists and the user cannot state what the result is or how they would validate it, recommend `krukit-discovery` first (invoke it via the Skill tool on agreement, passing the already-confirmed feature slug so discovery.md lands in this feature's folder), then return here and route with `discovery.md` as the task description — routing a task without a known "what" only launders ambiguity into the pipeline.

   **Routing with a confirmed discovery.md:** its Handoff route is the recommended option. The minimum route is fix — krukit-verify must execute the Validation plan; offer trivial only with the explicit caveat that the Validation plan then runs inline as the route's "relevant test" and its results are reported. If its Open questions section is non-empty, recommend full.

3. **Create flow-state** (full and fix routes only). Write `docs/krukit/<feature-slug>/flow-state.md` with Route set to the single chosen route:

   ```markdown
   # Krukit Flow: <feature-slug>
   Started: YYYY-MM-DD | Route: <full or fix>
   Task: <one-line description + issue ref>
   - [ ] 1 recon
   - [ ] 2 grill
   - [ ] 3 design
   - [ ] 4 plan
   - [ ] 5 act
   - [ ] 6 verify
   - [ ] 7 review
   ```

   For the fix route, mark rows 1–4 and 7 as `- [x] N <stage> — skipped (route) YYYY-MM-DD`. When a confirmed discovery.md exists, append ` | Discovery: discovery.md` to the header line — the binding is recorded, not assumed.
4. **Constitution — open** (full route only): invoke `krukit-rules` in open mode. Existing constitution → one-line load report, move on. None (first run) → it offers a grilled setup interview; on decline, note it and continue (stages 3 and 6 will record the absence).

5. **Todos.** TodoWrite: one todo per stage in the route; mark in_progress/completed as you go.
6. **Run stages in order** via the Skill tool, exact names: `krukit-recon` → `krukit-grill` → `krukit-design` → `krukit-plan` → `krukit-act` → `krukit-verify` → `krukit-review`. Fix route runs only `krukit-act` → `krukit-verify`.
7. **Between stages:** confirm the stage's gate passed and the stage ticked its row as `- [x] N <stage> — done YYYY-MM-DD, artifact: <file>`; report a 2-3 line stage summary; update the todo. If a gate fails, say what failed and stop — do not silently proceed.
   - **Reopen:** if krukit-verify unticks earlier rows as `— reopened YYYY-MM-DD (<reason>) [was: <previous marker>]`, resume from the first reopened stage (same rule as step 1: first row not ticked). The `[was: ...]` part preserves the row's prior done/skipped annotation.
   - **Context resets:** on long features, stage boundaries are safe reset points — suggest `/clear` and re-invoking krukit-flow for the slug; flow-state makes the reset lossless.
8. **User-facing gates** — grill completion (stage 2), design approval (stage 3), HIGH-finding acceptance (stage 6) — wait for the user. Never self-approve. **Audit rule:** record the user's verbatim reply in flow-state.md as quoted gate evidence (`> "<reply>" — YYYY-MM-DD`); if there is no quotable user message, the gate has NOT passed — a phantom or self-generated answer is structurally invalid. For gates resolved inside a delegated stage skill (grill completion, design approval), quote the user's reply from that stage's session; if flow itself saw no direct reply, the evidence line is the stage's gate-pass marker: `> [stage N gate passed, artifact: <file>] — YYYY-MM-DD`.
9. **Skips.** When the user says "skip <stage>", mark that row `- [x] N <stage> — skipped (user) YYYY-MM-DD` and continue. Gates that depend on a skipped artifact degrade gracefully: note the missing input, do not fail.
10. **Constitution — close** (full route only): invoke `krukit-rules` in close mode — it distills at most one constitution-grade principle from the feature trail and proposes it. "No amendment this time" is a normal outcome.
11. **Finish.** Final summary listing all artifacts produced in `docs/krukit/<feature-slug>/`.

## Outputs

- `docs/krukit/<feature-slug>/flow-state.md` — route + per-stage ticks/skips.
- Stage artifacts produced by stage skills: `context.md`, `design.md`, `plan.md`, `verify.md`, implementation commits (plus pre-flow `discovery.md` when krukit-discovery ran).
- Final summary of artifacts.

## Gate

- [ ] Route chosen; recorded in flow-state.md for full and fix routes (trivial and external-spec produce no flow-state by design).
- [ ] Full route: all seven stages ticked (done or skipped).
- [ ] Fix route: act and verify ticked.
- [ ] Final summary lists the artifacts produced.
