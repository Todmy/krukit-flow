---
name: krukit-flow
description: Orchestrates the full krukit feature pipeline end-to-end with task routing, stage gates, and resume. Use when the user says "krukit-flow", "krukit flow", "крукіт флоу", or "давай krukit flow", or wants the whole disciplined feature pipeline run on a task. Stage 0 (orchestrator) of the krukit pipeline.
---

# Krukit Flow

Orchestrator of the 7-stage krukit pipeline: recon → grill → design → plan → act → verify → review. It routes the task, then runs the stage skills in order, enforcing each stage's gate, recording state in flow-state.md, and supporting resume and per-stage skips. Stage skills own their own process and gates; this skill only sequences and records. Interact with the user in the user's language.

## Invariants (all routes)

The Layer-0 floor. These hold on EVERY route — trivial, direct, fix, full, external-spec — and during any inspection done before routing. The constitution may extend them; its absence never disables them.

- **Snapshot before touch.** Irrecoverable mutable state (DB files and their journals/WAL, logs, state files — anything a tool can rewrite on open) → copy first, inspect the copy; read-only tools before stateful ones; NEVER batch read-only inspection and a stateful tool in one command over such state. A guardrail counts only if it fires before the first careless command.
- **Deliverable gate.** The flow may not end while the task's declared observable deliverable is missing. Produce it best-effort from verified data ONLY — never fabricate content to fill gaps; state the gaps explicitly in the artifact instead. Unexplained completeness (data present that should not have been recoverable) is a defect to investigate, not a success.
- **Deadline gate.** On long-running, search, or compute-bound work (render, brute-force, training, build, open-ended fit), assume the run may be cut off before it finishes. Launch the expensive job first and backgrounded, then explore/verify/prepare a fallback alongside it instead of busy-waiting; wrap anything that can hang so it returns control (bounded `timeout`), never an unbounded blocking call. The moment you hold any result better than empty, write the declared deliverable to disk from what you've verified so far (marked partial if incomplete) and improve it in place — never leave it only inside a process a cutoff can kill. Adds to, never overrides, the invariants above (still snapshot before touch; best-effort is never fabricated).

## Autonomous mode

When no human can answer mid-run (headless / one-shot session, CI, benchmark) or the user explicitly declares it, append ` | Mode: autonomous` to the flow-state header line and switch gate semantics:

- **Gates become logged checkpoints.** At every user-facing gate, choose the recommended option, record it, and proceed — never stop to wait for a reply that cannot come.
- **Questions are forbidden until the deliverable exists.** In a one-shot session, asking IS termination — dying with an open question violates the deliverable gate above. Only after the declared deliverable exists may a question be raised, as a last resort.
- **Auto-answers are logged, never disguised.** Evidence line format in flow-state.md: `> [auto-answer] <gate>: <chosen default> — <one-line reason> — YYYY-MM-DD`. This is the ONLY valid gate evidence in autonomous mode; writing it as if a user replied remains structurally invalid (step 7's audit rule: no fabricated user quotes, ever).

- A task description (feature, bugfix, or change) from the user.
- A feature slug — short kebab-case name; derive and confirm one if not given.
- Optional: existing `docs/krukit/<feature-slug>/flow-state.md` (resume case).
- Optional: `docs/krukit/<feature-slug>/discovery.md` — pre-flow output of `krukit-discovery`. If present with `Status: confirmed`, use it as the task description and Definition of Done source; do not re-ask what its Decisions already answer. `Status: incomplete` → treat as absent and offer to re-run krukit-discovery. Before deriving a fresh slug, glob `docs/krukit/*/discovery.md` for confirmed files without a sibling flow-state.md — an orphan is offered as the task candidate and its slug becomes the flow slug (never let a slug mismatch silently sever the discovery contract).

## Process

1. **Resume check.** If `docs/krukit/<feature-slug>/flow-state.md` exists with unticked boxes:
   - Resume point = the first row that is not ticked (done and skipped rows are both ticked `- [x]`).
   - On resume: read Route from the flow-state header — do not re-ask; re-read the remaining flow-state rows; skip to step 5 at the resume point.
   - On declined resume: confirm, then overwrite flow-state.md and start over.
2. **Stage 0 — Route.** Classify the task with the user: one question via the `AskUserQuestion` tool (arrow-key form). Options = the five routes below, your recommended route FIRST with the label ending "(Recommended)" and the reason in its description. If invoked without a task description, derive the likely candidate task(s) from session context / the tracker FIRST and fold them into this SAME question (name the recommended candidate in the route-option descriptions, or ask one combined task+route question) — never spend a separate AskUserQuestion round on task selection alone.

   | Route | When | Stages |
   |---|---|---|
   | trivial | typo/config/one obvious file | no pipeline — do it + run the relevant test; no artifacts, no flow-state (route-log line only) |
   | direct | task is NOT feature work — forensics/recovery, ops/investigation, puzzle/algorithmic one-off — pipeline stages don't fit regardless of size | no pipeline — do the work directly, verify against the task's own success criteria; Layer-0 invariants apply; log the route |
   | fix | small well-scoped change (bugfix or tiny feature), behavior known | 5 act (TDD) → 6 verify |
   | full | feature or change in existing code | 1→7 all stages |
   | external-spec | big greenfield where the spec is a human deliverable in Git | recommend spec-kit/OpenSpec, explain why, stop |

   **Discovery escape hatch:** if no confirmed `discovery.md` exists and the user cannot state what the result is or how they would validate it, recommend `krukit-discovery` first (invoke it via the Skill tool on agreement, passing the already-confirmed feature slug so discovery.md lands in this feature's folder), then return here and route with `discovery.md` as the task description — routing a task without a known "what" only launders ambiguity into the pipeline.

   **Routing with a confirmed discovery.md:** its Handoff route is the recommended option. The minimum route is fix — `direct` is not offered (confirmed discovery output is feature work by definition), and krukit-verify must execute the Validation plan; offer trivial only with the explicit caveat that the Validation plan then runs inline as the route's "relevant test" and its results are reported. If its Open questions section is non-empty, recommend full.

   **Capability cap:** before presenting routes, read the model name the harness declares (system prompt / environment) — NEVER ask the model to assess its own capability. Below Sonnet-class (Haiku-class or unknown lightweight tier): in autonomous mode cap the route at `fix` — `full` is neither offered nor chosen, and the route-log reason notes `(cap: below-bar)`; in interactive mode keep `full` visible with an explicit warning in its description — the user's explicit pick is an override, logged as `full (override: below-bar)`. Unknown model name: autonomous → treat as below-bar; interactive → say "tier unknown" in the warning.

   **Route log:** record EVERY Stage-0 decision (all five routes) as one appended line in `docs/krukit/route-log.md` (create on first use, append-only): `YYYY-MM-DD | <task one-liner> | <route> | <reason>`. Telemetry only — nothing reads it for state; if the write fails, note it and continue.

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

5. **Run stages in order** via the Skill tool, exact names: `krukit-recon` → `krukit-grill` → `krukit-design` → `krukit-plan` → `krukit-act` → `krukit-verify` → `krukit-review`. Fix route runs only `krukit-act` → `krukit-verify`.
6. **Between stages:** confirm the stage's gate passed and the stage ticked its row as `- [x] N <stage> — done YYYY-MM-DD, artifact: <file>`; report a 2-3 line stage summary. If a gate fails, say what failed and stop — do not silently proceed.
   - **Reopen:** if krukit-verify unticks earlier rows as `— reopened YYYY-MM-DD (<reason>) [was: <previous marker>]`, resume from the first reopened stage (same rule as step 1: first row not ticked). The `[was: ...]` part preserves the row's prior done/skipped annotation.
   - **Context resets:** on long features, stage boundaries are safe reset points — suggest `/clear` and re-invoking krukit-flow for the slug; flow-state makes the reset lossless.
7. **User-facing gates** — grill completion (stage 2), design approval (stage 3), HIGH-finding acceptance (stage 6) — wait for the user. Never self-approve. **Audit rule:** record the user's verbatim reply in flow-state.md as quoted gate evidence (`> "<reply>" — YYYY-MM-DD`); if there is no quotable user message, the gate has NOT passed — a phantom or self-generated answer is structurally invalid. Sole exception: autonomous mode, where the explicitly-marked `[auto-answer]` line is the valid evidence form (see ## Autonomous mode). For gates resolved inside a delegated stage skill (grill completion, design approval), quote the user's reply from that stage's session; if flow itself saw no direct reply, the evidence line is the stage's gate-pass marker: `> [stage N gate passed, artifact: <file>] — YYYY-MM-DD`.
8. **Skips.** When the user says "skip <stage>", mark that row `- [x] N <stage> — skipped (user) YYYY-MM-DD` and continue. Gates that depend on a skipped artifact degrade gracefully: note the missing input, do not fail.
9. **Constitution — close** (full route only): invoke `krukit-rules` in close mode — it distills at most one constitution-grade principle from the feature trail and proposes it. "No amendment this time" is a normal outcome.
10. **Finish.** Final summary listing all artifacts produced in `docs/krukit/<feature-slug>/`.

## Outputs

- `docs/krukit/<feature-slug>/flow-state.md` — route + per-stage ticks/skips.
- Stage artifacts produced by stage skills: `context.md`, `design.md`, `plan.md`, `verify.md`, implementation commits (plus pre-flow `discovery.md` when krukit-discovery ran).
- Final summary of artifacts.

## Gate

- [ ] Route chosen; recorded in flow-state.md for full and fix routes (trivial, direct, and external-spec produce no flow-state by design).
- [ ] Full route: all seven stages ticked (done or skipped).
- [ ] Fix route: act and verify ticked.
- [ ] Final summary lists the artifacts produced.
