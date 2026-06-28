---
name: krukit-rules
description: Open/close constitution skill of the krukit pipeline. Open mode loads the project constitution before a feature — on first run it grills the user through a guided setup interview; close mode distills at most ONE constitution-grade principle from the finished feature and proposes it as an amendment. Idempotent — converges every repo to exactly one constitution, never two. Use when the user says "krukit-rules", "крукіт правила", "крукіт конституція", or when /krukit-flow starts or finishes a full-route feature.
---

# Krukit Rules — Living Project Constitution

Companion skill of the krukit pipeline, run twice per feature: **open** (before recon) and **close** (after review). The constitution is the short list of non-negotiable principles that krukit-design checks every design against (stage 3) and krukit-verify re-checks in code (stage 6). Idempotent in both modes: open never duplicates, close adds at most one principle and only with user approval. Interact with the user in the user's language.

## Modes

| Mode | When | Does |
|---|---|---|
| **open** (default) | Feature start, or standalone | Load the constitution; bootstrap if none; nothing else if already formed |
| **close** | Feature end (after stage 7) | Distill ≤1 constitution-grade principle from the feature, propose it |

## Discovery order (shared with krukit-design and krukit-verify)

`.specify/memory/constitution.md` → `docs/krukit/constitution.md` → project `CONTEXT.md` principles section.

## Process — open

1. **Discover.** Check the three locations in order. Also scan for stray duplicates.
2. **If a constitution exists:** load it, report one line ("Constitution vX.Y.Z, N principles — loaded"), and stop. Do NOT propose changes in open mode — that's close mode's job. This is the idempotent no-op path.
   - Duplicates found (e.g. both `.specify/memory/` and `docs/krukit/` versions) — the one real failure mode: ask the user which is authoritative, merge unique principles into it, delete the other. One file survives.
3. **If none exists — first run: grilled setup.** This is not a quick draft — it's a guided interview that helps the user set the constitution up properly.
   - **Seed.** Mine candidate principles from what the repo already says: project CLAUDE.md, `CONTEXT.md`, `docs/adr/`, README, lint/CI configs. Principles are discovered first, invented second.
   - **Grill the user** — one question at a time, for as long as real ambiguity remains. No hard cap: announce a soft estimate upfront ("looks like ~N questions"), but keep going while a domain is genuinely unclear, and stop early when nothing material is left. The user always has two exits: **"done"** (stop now, draft from what we have) and **"all recommended"** (accept the current recommendation AND every remaining question's recommendation — fast-forward to the draft).
   - **Every question is an arrow-key form, not typed text.** Present each question with the `AskUserQuestion` tool (Claude Code renders a selector; the user picks with arrows + Enter). Mapping — problem first, recommendation always visible, minimal cognitive load:
     - **question text** = `Problem: <1-2 lines — the concrete failure this rule prevents, with an example from THIS repo where possible>` followed by the one decision to make;
     - **header** = the domain (e.g. "Testing", "Security");
     - **first option** = your recommendation — label ends with "(Recommended)", description = the one-line reason;
     - **next options** = the real alternatives (keep the total ≤ 4), each with a one-line description of what it means;
     - **last option** = "All recommended" — description: "accept this and every remaining question's recommendation";
     - the built-in "Other" covers free-text answers; "done" via Other stops the interview and drafts from what we have.
     Fallback (non-Claude-Code harness without the tool): same content as a markdown block with `**Recommended:**` line and an options table.

   - On **"all recommended"**: stop asking, fill every remaining domain with your recommended answer, and mark those principles `(auto-accepted recommendation)` in the draft so they're visible at final approval.
   - Walk this domain checklist and ask only where repo evidence is missing or ambiguous:

     | Domain | What to nail down |
     |---|---|
     | Simplicity & scope | how aggressive is YAGNI; what counts as over-engineering |
     | Testing | TDD always or risk-based; coverage expectations |
     | Architecture boundaries | what must stay decoupled; forbidden dependencies |
     | Dependencies | when adding a library is OK; banned origins/licenses |
     | Security & data | secrets handling, PII rules, what never leaves the machine |
     | Cost | token/infra budgets that designs must respect |
     | Git & release | commit granularity, push policy, review requirements |
     | Domain-specific | anything unique to this repo (content rules, compliance, ...) |

   - Each answer becomes (or kills) a principle on the spot — confirm, sharpen, or reject the seeded candidates; capture implicit rules the repo never wrote down.
   - **Draft** ≤ 10 principles. Each: a bold name, one MUST/SHOULD sentence, one-line rationale. If you can't justify a principle in one line, it doesn't belong. Auto-accepted principles keep their `(auto-accepted recommendation)` marker until the user approves the draft.
   - On approval, write `docs/krukit/constitution.md` (format below) and commit. Never push without permission. Final approval of the full draft is always required — "all recommended" skips questions, never the approval.

## Process — close

1. **Load** the constitution (discovery order). If none exists, run open-mode bootstrap first — there is nothing to amend.
2. **Review the finished feature's trail:** flow-state.md (grill summary, review summary), verify.md findings, ADRs created during the feature, and what actually went wrong or saved the day during act/verify.
3. **Distill at most ONE candidate principle.** The bar — constitutional weight, equal to what's already recorded:
   - It would have changed a decision in THIS feature, AND it binds FUTURE features (project-wide, recurring — not feature-specific).
   - It does not duplicate an existing principle. If it refines one, propose amending that principle instead of adding.
   - Feature-specific lessons fail this bar — they belong in CONTEXT.md, an ADR, or Valis, not the constitution. Say where you're routing them instead.
   - **Nothing qualifies → say so and add nothing.** An honest "no amendment this time" is the expected common case; a forced weekly principle is how constitutions rot.
4. **Propose** the candidate to the user: the principle (name + MUST/SHOULD sentence + one-line why), the evidence from this feature, and — if the constitution is at the 10-principle cap — which weaker principle it should displace.
5. **On approval:** amend in place (addition = minor version bump, changed/displaced principle = major), append one Amendment-log line ending with the feature slug, commit. **On decline:** record nothing; optionally route the lesson to Valis/ADR.

## Format

```markdown
# Constitution: <project>
Version: 1.0.0 | Ratified: YYYY-MM-DD

## Principles
1. **<Name>** — MUST <rule>. <one-line why>

## Amendment log
- 1.0.0 (YYYY-MM-DD) — initial ratification
- 1.1.0 (YYYY-MM-DD) — added <Name> (from feature: <slug>)
```

## Outputs

- Open: constitution loaded (or bootstrapped + committed); exactly one file across discovery locations.
- Close: at most one approved amendment (committed), or an explicit "no amendment this time".

## Gate

- [ ] Exactly one constitution exists across all three discovery locations (zero duplicates).
- [ ] Version and Ratified date present; amendment log has one line per version.
- [ ] Any new or changed principle was explicitly approved by the user; close mode proposed at most one.
- [ ] File committed; nothing pushed without permission.

If any condition fails: say what failed and stop.
