---
name: krukit-recon
description: Maps an existing codebase before any design work — affected modules, patterns to follow, invariants — into a short context.md. Use when starting a feature on existing code, before design, when the user says "krukit-recon" or "крукіт recon". Stage 1 of the krukit pipeline.
---

# Krukit Recon — Codebase Reconnaissance

Stage 1 of 7 in the krukit pipeline: recon → grill → design → plan → act → verify → review. Recon maps the territory of an existing codebase so later stages don't invent parallel patterns or break invariants. Output is one short `context.md`. Runs standalone or inside /krukit-flow. Interact with the user in the user's language.

## Inputs
- A feature idea or one-sentence goal (ask for or derive it if absent).
- The target repo (existing code or greenfield).
- Optional: `docs/krukit/<feature-slug>/flow-state.md` when invoked inside the flow.
- Optional: `docs/krukit/<feature-slug>/discovery.md` with `Status: confirmed` — seed the Explore fan-out with its Open questions and Prior art.

## Process

1. **Resolve target.** If the slug/goal isn't given, derive a kebab-case feature slug and a one-sentence goal (confirm with the user). Create `docs/krukit/<slug>/`. If `flow-state.md` is absent (standalone run), create it; if present, leave it untouched:

   ```markdown
   # Krukit Flow: <slug>
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

2. **Fan out exploration.** If the repo is greenfield (little or no existing code): skip the fan-out, do a 5-minute light pass over structure, stack, and conventions, state that recon is trivially small, and go to step 3 (sections may be short or "none"). Otherwise dispatch 2–3 parallel subagents (Agent tool, Explore type) in a single message, read-only. Keep raw file dumps inside the subagents; only their summaries return to main context.

   | Agent | Maps |
   |---|---|
   | A | Affected modules + their callers/dependents |
   | B | Existing patterns & conventions to follow (similar features, naming, test style) |
   | C | Invariants & constraints — tests that encode behavior, configs, `CONTEXT.md`, `docs/adr/`, constitution |

3. **Synthesize `context.md`** (≤ 2 pages) with exactly these six sections:
   - **Goal** — the one-sentence goal.
   - **Affected map** — table: file → role → who depends on it.
   - **Patterns to follow** — concrete examples with file paths.
   - **Invariants** — what must not break.
   - **Risks** — what could go wrong.
   - **Open questions** — feed stage 2 (krukit-grill); list explicitly, write "none" if truly none.

4. **On gate pass**, tick the flow-state row: change `- [ ] 1 recon` to `- [x] 1 recon — done YYYY-MM-DD, artifact: context.md`.

## Outputs
- `docs/krukit/<slug>/context.md` — the recon brief (≤ 2 pages, the six sections above).
- `docs/krukit/<slug>/flow-state.md` — created if standalone, stage 1 row ticked.

## Gate
- [ ] `context.md` exists.
- [ ] All six sections present (Goal, Affected map, Patterns to follow, Invariants, Risks, Open questions).
- [ ] Open questions explicitly listed (may be "none").

If any condition fails: say what's missing and stop — do not advance to krukit-grill.
