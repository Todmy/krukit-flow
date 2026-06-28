---
name: krukit-discovery
description: Pre-flow discovery — collects every available artifact and interrogates the problem space until the user can state what they want, what it looks like, and how they will validate it, producing discovery.md for /krukit-flow. Use when the user says "krukit-discovery", "крукіт discovery", "крукіт діскавері", when a task is vague, or when the user cannot state the desired outcome or how to validate it. Companion skill of the krukit pipeline.
---

# Krukit Discovery — Problem-Space Interrogation

Companion skill of the krukit pipeline, run BEFORE /krukit-flow when the "what" is fuzzy. Two deliverables: (1) a clear picture of what to do — `discovery.md`, handed to /krukit-flow as the task description; (2) a user-owned **Definition of Done** — what the result is, what it looks like, how the user will validate it. Grounding: Addy Osmani's **cognitive surrender** — developers working with AI hand over not only the "how" but the "what"; whoever cannot state the outcome and its validation does not control the task. Discovery keeps the "what" with the user; the pipeline owns only the "how". Interact with the user in the user's language.

## Inputs

- A raw task idea — however vague ("something about X" is enough to start).
- Everything already said in this conversation — prior questions and answers count as coverage; never re-ask them.
- Artifacts the user can provide (step 2 actively solicits them): tickets/issues, docs, links, screenshots/mockups, code pointers, chat fragments, examples of similar solutions.

## Process

1. **Resolve target.** When invoked from /krukit-flow, reuse the caller's already-confirmed slug; derive a kebab-case slug (and confirm it) only when running pre-flow. Create `docs/krukit/<slug>/`. No flow-state.md — discovery is pre-flow; /krukit-flow owns pipeline state. If `flow-state.md` already exists for this slug, warn that the flow is in progress: a Definition of Done added now becomes binding only after the affected stages are reopened through flow's reopen markers.

2. **Collect artifacts.** One solicitation round listing the categories above — more is better; partial or outdated artifacts still carry signal. If the user has nothing, record one row "none provided — proceeding from conversation only" and move on. Read everything provided (verbose sources → Explore subagents; raw dumps stay out of the main context). Record each in an Artifacts table: `| Source | What it tells us | Questions it raised |`.

3. **Build the coverage map** BEFORE asking anything, and SHOW it to the user — one line of evidence per mark; marks inferred from artifacts rather than the user's own words are flagged `(inferred from <source>)` so they can be contested. Mark each domain **covered / open / n-a**; never ask what is already answered:

   | Domain (form header) | Nails down |
   |---|---|
   | Problem & trigger (Problem) | what hurts, for whom, why now |
   | Users & stakeholders (Stakeholders) | who touches the result, who judges it |
   | Desired outcome (Outcome) | what exists when done → DoD: Result |
   | Observable form (Form) | what it looks like in use → DoD: Looks like |
   | Validation (Validation) | how the user will check → DoD: Validation plan |
   | Scope boundaries (Scope) | what is explicitly NOT included |
   | Constraints (Constraints) | time, stack, budget, compatibility |
   | Prior art (Prior art) | existing artifacts, similar solutions, earlier attempts |
   | Risks & unknowns (Risks) | what could invalidate the idea |

   Fast path: ONLY when every domain is covered or n-a, the Artifacts table raised no unresolved questions, AND nothing contradicts — jump to step 5. Otherwise interrogate the open items.

4. **Interrogate.** One question at a time, no hard cap — announce a soft estimate upfront, include a progress line in each question ("domain 4/9, ~6 questions left"), and continue while ANY generator still yields a material question. Four generators; the highest-priority hit wins each round:

   | Priority | Generator | Finds |
   |---|---|---|
   | 1 | Contradiction scan | conflicts between answers, between artifacts, or between the two → ask |
   | 2 | Assumption audit | assumptions you are silently making; each unconfirmed one → ask |
   | 3 | Artifact interrogation | what each artifact implies, contradicts, or leaves unsaid → ask |
   | 4 | Coverage walk | the first domain still open → ask it |

   Every question is an `AskUserQuestion` arrow-key form: header = the domain's form-header alias (≤12 chars); question text = problem-first (the concrete risk of leaving this unanswered, then the one decision) plus the progress line; recommended option FIRST, label ending "(Recommended)", reason in its description; ≤4 options, the LAST always **"All recommended"** ("accept this and every remaining question's recommendation"); the built-in "Other" covers free text and the **"done"** exit (stop interrogating, synthesize from what we have — still-open domains become explicit deferrals in the Coverage section). Fallback on harnesses without the tool: same content as a markdown block with a `**Recommended:**` line and an options table.

   **"All recommended" scope:** it never fills the three DoD-feeding domains (Desired outcome, Observable form, Validation — they pass to step 5 unanswered) and never resolves contradiction-scan questions (a conflict between the user's own statements cannot be auto-resolved); those are asked individually regardless. Auto-accepted answers are marked `(auto-accepted recommendation)` in Decisions.

5. **Definition of Done — the anti-surrender core.** Three questions, asked individually, ALWAYS — neither "done" nor "All recommended" skips them. **Free-text, not option forms** — the one deliberate exemption from the arrow-key convention: show no recommendation before the user's own attempt. You may offer hypotheses to react to when the user is stuck, but the recorded answer must be the user's own substantive restatement — a picked option label or bare assent ("yes", "ok", "так") is not valid gate evidence.
   1. **Result** — what exists when this is done?
   2. **Looks like** — the observable form: "describe the 2-minute demo".
   3. **Validation plan** — numbered steps the USER will run to check it ("what evidence would convince a skeptic?"). Each step needs an observable pass/fail outcome and a class: machine-runnable (command/check named) or user-runnable (action + expected result). A step with no failure mode gets one push-back: "what would a failing run look like?"

   Quote each confirmation verbatim in discovery.md (`> "<reply>" — YYYY-MM-DD`). If the user cannot answer a field, that inability IS the finding — return to step 4 and dig the problem space further; never fill the field for them. After the second failed return for the same field, stop: write discovery.md with `Status: incomplete — DoD unconfirmed (<field>)`, recommend parking the task or running a spike/prototype first, and end without handoff. This is a named, legitimate outcome — not a gate violation.

6. **Synthesize `docs/krukit/<slug>/discovery.md`** (≤2 pages) with exactly these sections:

   ```markdown
   # Discovery: <slug>
   Date: YYYY-MM-DD | Status: confirmed | incomplete — <what is missing>

   ## Problem               ← what hurts, for whom, why now (2-5 sentences)
   ## Coverage              ← the step-3 map: domain | status | one-line evidence; deferrals as `deferred: <domain> — <reason>`
   ## Artifacts             ← the table from step 2
   ## Decisions             ← answered questions, one line each: question → decision (with `(inferred from <source>)` / `(auto-accepted recommendation)` marks)
   ## Definition of Done    ← Result / Looks like / Validation plan (numbered, classed steps), each with its verbatim quote
   ## Out of scope
   ## Open questions        ← technical unknowns — feed krukit-recon and krukit-grill
   ## Comprehension trace   ← step-7 result: axis | correct/miss | resolution (no distractor bodies; on the incomplete path: "not run — DoD unconfirmed")
   ## Handoff               ← one-paragraph task description + recommended route + why + the exact invocation: `/krukit-flow <slug>`
   ```

7. **Comprehension trace** — verify the picture actually landed; "all clear" is a false signal until tested. Build THREE check questions from this session's own material, one per axis: the **outcome** (what exists at the end), the **scope boundary** (what is NOT included), the **validation** (which step proves it works, or what a failing run looks like). Each is an `AskUserQuestion` form with EXACTLY 3 options and NONE of step 4's form conventions — no recommended marker, no "All recommended", no progress line; a marked answer or an escape hatch would test nothing. Options = the statement that is true per discovery.md plus 2 plausible distractors drawn from material this session explicitly rejected, deferred, or scoped out; when an axis yields no such material, synthesize a plausible-but-false variant of the true statement (changed deliverable, inverted boundary, wrong pass/fail signal). Never place the true option first. An "Other" free-text reply counts as correct only if it restates the true statement; anything else is a miss. A miss is a comprehension gap, not a failure: show the relevant discovery.md fragment, reopen the underlying question (step 4 or 5), update every discovery.md section the new answer changes, then re-trace that axis with a REBUILT question — fresh distractors or a different probe, never the one whose answer was just shown. A second miss on the same axis → stop: `Status: incomplete — comprehension unverified (<axis>)`, park as in step 5. Record each axis in the Comprehension trace section — axis, correct/miss, resolution; never the distractor bodies. Fallback without the tool: an options table only, no Recommended line.

8. **Handoff** (`Status: confirmed` only). Give the user the exact invocation including the slug (a `/clear` first is safe — discovery.md makes the reset lossless). Flow reads discovery.md as the task description and recommends its Handoff route; recon seeds exploration with the Open questions and Prior art; grill consumes the Open questions; verify executes the Validation plan.

## Outputs

- `docs/krukit/<slug>/discovery.md` — coverage, artifacts, decisions, user-confirmed Definition of Done, comprehension trace, handoff. `Status: confirmed`, or `Status: incomplete` when the user could not yet own the "what" (task parked, no handoff).
- A user who can state, in their own words, what they want, what it looks like, and how they will validate it — verified by the comprehension trace, not self-reported.

## Gate

Handoff requires ALL of these. An explicit `Status: incomplete` file is the one legitimate alternative ending — retained on disk, never handed off, never consumed downstream.

- [ ] `discovery.md` exists with all nine sections and `Status: confirmed`.
- [ ] Coverage section shows every domain covered / n-a / deferred-with-reason, each with one-line evidence — no silent gaps.
- [ ] Every collected artifact was read and appears in the Artifacts table.
- [ ] All three Definition of Done fields confirmed individually — verbatim user-typed quotes that restate the content (no option labels, no bare assent, none auto-accepted).
- [ ] Every Validation plan step is falsifiable and classed machine-runnable or user-runnable.
- [ ] Comprehension trace run on all three axes — every miss resolved by reopening, updating the affected sections, and re-tracing with a rebuilt question; results recorded (a second miss on one axis = `Status: incomplete`, the legitimate stop).
- [ ] Handoff names the recommended route, the exact `/krukit-flow` invocation with this slug, and the open questions for recon/grill.

If any condition fails: say what failed and stop — do not hand off to /krukit-flow.
