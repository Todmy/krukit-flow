---
name: krukit-review
description: Independent fresh-eyes code review of the final feature diff, then clean branch finish with knowledge capture. Use when the user says "krukit-review", "крукіт рев'ю", "крукіт review", or wants to review and close out a krukit feature branch. Stage 7 of the krukit pipeline.
---

# Krukit Review

Stage 7 of 7 in the krukit pipeline: recon → grill → design → plan → act → verify → review. Runs an independent review of the full feature diff, resolves every finding on its technical merits, then closes the branch cleanly and captures any durable knowledge. Interact with the user in the user's language.

## Inputs

- Feature branch with the implemented change, all `plan.md` tasks done.
- `docs/krukit/<feature-slug>/verify.md` — zero CRITICAL findings, HIGH findings fixed or user-accepted (missing-file behavior: step 1).
- `docs/krukit/<feature-slug>/flow-state.md` — read on start. If absent (standalone invocation), create the folder and file, and mark rows 1–6 as `- [x] N <stage> — skipped (standalone) YYYY-MM-DD`:

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

1. Read `flow-state.md` (create as above if standalone). Check the verify gate: `verify.md` exists with zero CRITICAL findings. If not, report the degraded input and ask the user whether to proceed.

2. Compute the full feature diff: `git diff $(git merge-base <default-branch> HEAD)...HEAD`.

3. **Independent review.** Hand the diff to a fresh reviewer with no prior context from this session (a dedicated subagent), with the feature description and the design/plan requirements. The review returns findings stratified by severity — Critical / Important / Minor — plus an overall assessment. Never skip the review because the change "looks simple."

4. **Resolve every finding on its merits.** Read each finding fully before reacting; restate the requirement, and check it against the codebase (does it break something? contradict the architecture?) before acting. Clarify any unclear finding before implementing anything — findings may be related — and test each fix individually rather than batching. Then either fix it (one small discrete commit per fix) or decline it with a stated technical reason — no finding is silently dropped, and no performative agreement. Critical findings are fixed immediately; Important before the branch is closed; Minor may be deferred with a note.

5. **Finish the branch.** First confirm the full test suite passes on the final state — if it fails, show the failures and stop. Then present the user the branch options (merge locally / push and open a PR / keep as-is / discard) and execute their choice. When merging, re-run the full test suite on the merged result before deleting the branch — a clean branch can still break the base on a non-trivial merge. Remove any worktrees this pipeline created. Never push to remote without explicit user permission; discarding requires the user to type `discard` exactly.

6. **Knowledge capture:** if a durable decision, lesson, or pattern emerged from this feature, store ONE grouped entry via `valis_store` (status=proposed) when Valis is available. Skip silently otherwise.

7. Append a short **Review summary** to `flow-state.md` (findings fixed/declined counts, branch outcome, knowledge entry yes/no). Tick the stage row:
   `- [x] 7 review — done YYYY-MM-DD, artifact: flow-state.md`

## Outputs

- Review findings resolved on the branch (fix commits or written declines).
- Branch finished: merged/cleaned, worktrees removed.
- Review summary appended to `flow-state.md`; stage 7 ticked.
- Optional single Valis knowledge entry (proposed).

## Gate

- [ ] Every review finding fixed or explicitly declined with a reason.
- [ ] Full test suite passed before the branch was finished — on the merged result when merging, not just the pre-merge branch; worktrees this pipeline created are removed.
- [ ] Nothing pushed to remote without explicit user permission.
- [ ] `flow-state.md` fully resolved — every stage done or marked `skipped (route|user|standalone) YYYY-MM-DD`.

If any condition fails: state what failed and stop. Do not silently proceed.
