# Krukit

A disciplined, brownfield-first feature pipeline for Claude Code: **recon → grill → design → plan → act → verify → review**, orchestrated end-to-end by `/krukit-flow` with stage gates, lossless resume, a living project constitution, and a trace-driven self-improvement loop.

> **Status: PRIVATE / work-in-progress.** Not ready for public release. See `ROADMAP.md`.

## What it is

`krukit-flow` routes a task (trivial / direct / fix / full / external-spec), then runs the stage skills in order — enforcing each stage's gate, recording state in `flow-state.md`, and supporting resume and per-stage skips. The orchestrator and the recon stage are original; the connective tissue (constitution, reopen-rule, verbatim gate-evidence, trace-driven `krukit-improve`) is what differentiates it from a plain command chain.

The design was hardened against **12 pain points** collected from the public GitHub issue trackers of six workflow tools (spec-kit, superpowers, OpenSpec, BMAD, Taskmaster, GSD) in June 2026 — e.g. the most-reacted pain in that collection (one-way pipeline with no sanctioned backward path) is addressed by the reopen rule.

## Requirements

- **Model:** the `full` route needs a Sonnet-class or stronger model. Below that bar the router caps the route at `fix` in autonomous runs and warns in interactive ones — weaker models misroute and rubber-stamp verification in our bench traces.
- **Harness:** a skills-capable Claude Code (or compatible) harness with arrow-key questions (`AskUserQuestion`) for interactive gates. Headless runs use autonomous mode (see krukit-flow).

## Skills

| Skill | Role |
|---|---|
| `krukit-flow` | Stage 0 — orchestrator |
| `krukit-recon` | Stage 1 — map the existing code before design |
| `krukit-grill` | Stage 2 — interrogate the idea against recon + domain model |
| `krukit-design` | Stage 3 — design doc + constitution check |
| `krukit-plan` | Stage 4 — bite-sized TDD implementation plan |
| `krukit-act` | Stage 5 — implement task-by-task with TDD |
| `krukit-verify` | Stage 6 — evidence-based verification + reality-check |
| `krukit-review` | Stage 7 — fresh-eyes review + branch finish |
| `krukit-rules` | Companion — living project constitution |
| `krukit-improve` | Companion — trace-driven skill improvement |
| `krukit-discovery` | Companion — pre-flow problem-space interrogation |

## Prior art & credit

Krukit exists because of tools I used heavily and genuinely rate:

- **[Spec Kit](https://github.com/github/spec-kit)** (GitHub) — spec-driven development done properly: write the spec down first, treat it as the deliverable.
- **[superpowers](https://github.com/obra/superpowers)** by Jesse Vincent — a deep, composable library of engineering-discipline skills: brainstorming, TDD, systematic debugging, verification, code review.
- **[Matt Pocock's skills](https://github.com/mattpocock/skills)** — sharp interrogation methodology (grill-with-docs) for pressure-testing a plan before you build it.

All three are excellent and worth your time. I ran real features through them, then went and read what people actually complain about in their issue trackers — and built around what those complaints point at: **one orchestrator plus stage skills that each fit in a single read — no separate CLI, no template pack, no config surface** — while keeping the discipline that makes those tools good.

### What people keep running into

Pains collected from the public issue trackers of six workflow tools (spec-kit, superpowers, OpenSpec, BMAD, Taskmaster, GSD), June 2026:

- **One-way pipeline.** Once you're implementing, there's no sanctioned way back when the work proves the design wrong. The most-reacted pain in that collection.
- **No grounding in the existing code.** Specs and clarifying questions get written without reading the repo, so brownfield assumptions slip straight through to implementation.
- **Capped, code-blind clarification.** A fixed question limit, and no look at the actual source behind the answers.
- **No feedback loop.** Artifacts freeze at planning time; what you learn while building never flows back into the design.
- **Silent gate approvals.** "Did the user actually approve this?" gets answered by the model, not the user.

Krukit's takes: a brownfield recon pass *before* any design, a reopen rule so verification can send you back with the design and plan updated, gate approvals that require a real quoted user reply, and routing that keeps small changes small instead of forcing full ceremony.

## License

MIT © 2026 Dmytro Tolok
