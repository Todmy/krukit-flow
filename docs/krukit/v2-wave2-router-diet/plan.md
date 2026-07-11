# Plan: v2-wave2-router-diet

Goal (from design.md): route table v2 (`direct` + capability cap + route-log) and the act/flow cost diet, via surgical in-place edits (Approach A). Tech: markdown SKILL.md prompt-code + one Python lint script. Global constraint: every SKILL.md growth justified in its commit message (P2).

**MUST NOT break (invariants from context.md):**
- P4 resume compat: existing flow-state files parse unchanged; `Route: direct` is a new value, never a rename; no removals of parsed markers (header formats, row markers, gate-evidence line formats).
- P5: §Invariants (all routes) stays intact and lint-pinned; `direct` is ADDED to its route enumeration.
- Route question stays ONE AskUserQuestion round (flow-c2 precedent); capability check folds into it.
- Persist-first in krukit-act (IMPROVE-LOG accepted): the inline task list persists to flow-state BEFORE any confirmation — the diet merges the confirmation rounds, never the persist.
- Lint pins survive: §Invariants, §Autonomous mode, 7 template rows, frontmatter checks.

Red-window note: T2 intentionally turns the T1 lint check RED (flow enumerations gain `direct`, README lags until T6). This is the designed red→green proof of the new check (P1); the window is intra-flow and closes at T6.

## Tasks

### T1: lint route-consistency check
- Modifies: `scripts/lint-consistency.py`. Tests: run on current tree.
- Contract: extract three route-name sets — (a) route-table rows in `skills/krukit-flow/SKILL.md` (first cell of each `| <name> |` row in the table under step 2), (b) the §Invariants enumeration line ("EVERY route — <list>"), (c) README's route enumeration line ("routes a task (<list>)"). Error unless (a) == (b) == (c).
- Test cases: `lint_green_on_current_tree` (all three currently list the same 4 routes → exit 0); parser must not match table header/separator rows.
- Commit: `Lint: route-name consistency across flow table, invariants, README`.

### T2: route table v2 in krukit-flow (design §1)
- Modifies: `skills/krukit-flow/SKILL.md`.
- Contract: add `direct` row exactly per design §1; append `; log the route` to trivial's Stages cell; update references: §Invariants L12 enumeration adds direct; step 2 "four routes" → "five routes"; gate line adds direct to "produce no flow-state by design"; discovery-routing: with confirmed discovery.md, `direct` is not offered (minimum stays fix).
- Test cases: lint now RED with exactly one route-consistency error (README lags — designed window); §Invariants/§Autonomous pins still green; no other lint errors.
- Commit: `Route table v2: direct route (type≠size) — flow side` (message notes designed red window + P2 justification).

### T3: capability self-check + route-log instruction in Stage 0 (design §2+§3)
- Modifies: `skills/krukit-flow/SKILL.md` (step 2 area only).
- Contract: (i) capability rule — read harness-declared model name; below Sonnet-class/unknown: autonomous → cap = fix, `full` neither offered nor chosen, route-log reason gets `(cap: below-bar)`; interactive → full visible with warning, explicit pick logged as `full (override: below-bar)`; never model self-assessment. (ii) route-log — at Stage 0 decision, append one line `YYYY-MM-DD | <task> | <route> | <reason>` to `docs/krukit/route-log.md` (create on first use, append-only, EVERY route incl. external-spec); write failure = non-fatal note; nothing reads it for state.
- Test cases: lint unchanged (still the one designed error); grep asserts: "below-bar", "route-log.md", "never.*self-assess" (case-insensitive) present in step 2; route question remains a single AskUserQuestion instruction.
- Commit: `Stage 0: capability cap by harness-declared tier + route-log telemetry` (P2 justification: this is the wave's core growth; offset by T4/T5 shrink).

### T4 [P]: flow diet — flow-state as the single tracker
- Modifies: `skills/krukit-flow/SKILL.md`.
- Contract: delete step 5 (TodoWrite); renumber or absorb so stage sequence keeps working references; step 7 "update the todo" → tick/report against the flow-state row only; step 1 resume "recreate todos for the remaining stages" → "re-read the remaining flow-state rows". No TodoWrite mention remains in the file.
- Test cases: `grep -ci todowrite skills/krukit-flow/SKILL.md` == 0; lint pins green; step numbering internally consistent after removal (references to renumbered steps updated — verify by grep "step N").
- Commit: `Flow diet: drop TodoWrite double-tracking; flow-state is the single tracker` (net-shrink, P2).

### T5 [P]: act diet — one confirmation round + Learnings rule
- Modifies: `skills/krukit-act/SKILL.md`.
- Contract: (i) fix-route step 2: persist-first sentence UNCHANGED; the confirmation AskUserQuestion and step 3's inline-vs-fresh-context pick (≤3 tasks case) merge into ONE AskUserQuestion call carrying both questions (task content still embedded in the question/preview); >3-tasks path unchanged (fresh-context, no question). (ii) step 7 Learnings: append only when the task list has >1 task; single-task fixes skip the section. Commit-per-task text untouched.
- Test cases: exactly ONE AskUserQuestion instruction remains on the ≤3-tasks fix path (grep count in the affected steps); "Persist it FIRST" (or equivalent original wording) still present verbatim; Learnings step contains the >1 condition.
- Commit: `Act diet: single batched confirmation round; Learnings only when tasks >1` (net-shrink, P2).

### T6 [P]: verify exact-oracle rule + IMPROVE-LOG candidate
- Modifies: `skills/krukit-verify/SKILL.md`; creates `skills/krukit-verify/IMPROVE-LOG.md`.
- Contract: one SHOULD sentence in step 2 per design §5 (exact oracle green ⇒ one verification cycle; name the oracle in verify.md); IMPROVE-LOG.md entry: candidate, evidence = cobol v1+v2 over-verification traces (same task — below P6 bar for MUST), promotion condition = second DISTINCT trace.
- Test cases: grep "exact oracle" in verify SKILL.md; IMPROVE-LOG has candidate + promotion condition; lint green on new file (frontmatter check applies only to SKILL.md — confirm no false positive).
- Commit: `Verify: exact-oracle SHOULD rule (IMPROVE-LOG candidate, P6-honest)`.

### T7: README — enumeration, Requirements, P3 compliance
- Modifies: `README.md`.
- Contract: (i) route enumeration line gains `direct` (this turns the T1 lint check GREEN — closes the red window). (ii) New `## Requirements` after "What it is": full route needs Sonnet-class+; below-bar behavior one-liner; skills-capable harness with arrow-key questions assumed. (iii) P3 compliance, per user decision "Артефакта немає — дата+метод": the three sourced claims get method+date attribution ("collected from the public issue trackers of six workflow tools — spec-kit, superpowers, OpenSpec, BMAD, Taskmaster, GSD — June 2026"); "the #1 cross-tool pain"/"most-reacted" soften to the verifiable form ("the most-reacted pain in that collection"); "simpler to use, clearer to follow, and lighter to run" rewritten as a mechanism claim (states what krukit does — one orchestrator + stage skills, no CLI/template pack — with no unmeasured comparative adjectives).
- Test cases: lint fully GREEN (route consistency restored); `grep -ci "simpler to use" README.md` == 0; Requirements section present; attribution string present.
- Commit: `README: direct route, Requirements (capability bar), P3 claim compliance`.

## Order & tags

T1 → T2 → T3 → {T4, T5, T6} `[P]` (mutually disjoint files; T4 merely must not start before T3 finishes the same file — satisfied by the phase order) → T7 last (closes the red window). No `[mechanical]` tags: every task is wording-sensitive prompt-code.

## Stage-6 validation (carried from design §Testing, not re-planned here)

Lint green end-state; bench krukit-v2 re-vendor: cobol ≤ 2× baseline; hard-pair password-recovery + write-compressor route-log + Layer-0; optional haiku cap probe.
