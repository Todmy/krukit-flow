# Plan: deadline-aware-execution

Route: full | Autonomous | 2026-07-13 | consumes design.md (approved, committed 799ee4c)

## Goal
Extend the Layer-0 floor with a **Deadline gate** invariant so a wall-clock cutoff can no longer strand the deliverable on long/compute-bound tasks. Single-bullet prompt-code change + lint pin + glossary mirror; bench validation deferred to verify.

## MUST NOT break (from context.md / constitution v1.0.0)
- **P5 Layer-0 add-not-weaken** — the new bullet strictly ADDS obligation; snapshot-before-touch, deliverable gate, never-fabricate stay intact and take precedence (the bullet's own last sentence enforces composition).
- **P2 prompt budget** — one bullet (~95 words) into the highest-traffic file; commit body must carry the cost justification.
- **P4 resume-compat** — no flow-state/template format change; purely additive. Existing running flows parse unchanged.
- **P8 lint-pin** — the bullet is load-bearing → pinned; the pin is proven red→green (P1).
- **P9 pinned-vendor** — krukit-v3 frozen; changes land only as krukit-v4.
- **Route-name lint** (L74-75) — do NOT reword L12's `EVERY route — …` enumeration; the new bullet must not be a lowercase-first-cell table row (verified: prose bullet is invisible to the regex).

Note: **krukit-v4 bench-condition setup is a VERIFY activity** (design §Testing), not an act task — it vendors the repo at the final commit.

## Tasks

### T1 [TDD — two commits, red→green provenance] — Deadline-gate lint pin + bullet
- **Files:** `scripts/lint-consistency.py` (modify), `skills/krukit-flow/SKILL.md` (modify).
- **Commit 1 (RED):** inside the existing `if skill_md.parent.name == "krukit-flow":` block, after the `for section in (...)` heading-pin loop, add:
  ```python
  if "**Deadline gate.**" not in text:
      err(skill_md, "missing pinned Layer-0 bullet '**Deadline gate.**' (deadline-aware-execution)")
  ```
  Run `python3 scripts/lint-consistency.py` → MUST fail with exactly that pinned message (bullet absent) = RED proof. Commit: `test: pin Deadline-gate Layer-0 bullet in lint (RED)`.
- **Commit 2 (GREEN):** insert this EXACT bullet after L15 (the deliverable-gate bullet) in `skills/krukit-flow/SKILL.md`:
  > - **Deadline gate.** On long-running, search, or compute-bound work (render, brute-force, training, build, open-ended fit), assume the run may be cut off before it finishes. Launch the expensive job first and backgrounded, then explore/verify/prepare a fallback alongside it instead of busy-waiting; wrap anything that can hang so it returns control (bounded `timeout`), never an unbounded blocking call. The moment you hold any result better than empty, write the declared deliverable to disk from what you've verified so far (marked partial if incomplete) and improve it in place — never leave it only inside a process a cutoff can kill. Adds to, never overrides, the invariants above (still snapshot before touch; best-effort is never fabricated).

  Run `python3 scripts/lint-consistency.py` → MUST pass (11 skills, exit 0) = GREEN. Commit: `feat: add Deadline-gate Layer-0 invariant (deadline-aware-execution)` with a P2 cost-justification line in the body.
- **Contract:** lint fails iff the `**Deadline gate.**` substring is absent from krukit-flow, passes with it present; no other lint check regresses (route-name check unaffected).
- **Test cases:** (a) bullet reverted → lint red with the pinned message; (b) bullet present → lint green, exit 0, 11 skills.

### T2 [mechanical] — CONTEXT.md glossary mirror
- **File:** `CONTEXT.md` (modify, the `Layer-0 invariants` entry ~line 8).
- Add "deadline gate" to the Layer-0 enumeration: `... (snapshot-before-touch, deliverable gate, never-fabricate)` → include `deadline gate`. Keep the existing term→definition shape.
- **Contract:** the glossary Layer-0 entry names the deadline gate alongside the other three. No lint dependency (lint does not cross-check the glossary enumeration).
- Commit: `docs: mirror deadline gate into CONTEXT.md glossary`.

### T3 [mechanical] — sync installed skill copy
- The live skill at `~/.claude/skills/krukit-flow/SKILL.md` is a plain COPY (not a symlink), identical to the repo before T1; after T1c2 the repo diverges. For the improvement to reach the user's real krukit-flow runs, sync it.
- Procedure: `diff skills/krukit-flow/SKILL.md ~/.claude/skills/krukit-flow/SKILL.md`; if a krukit install/sync target or script exists, use it; else `cp skills/krukit-flow/SKILL.md ~/.claude/skills/krukit-flow/SKILL.md`. Additive change = P4-safe mid-session.
- **Contract:** installed copy is byte-identical to the repo after sync. NOT a git commit (outside the repo) — record in `## Learnings`.

## Spec coverage (self-review)
- DoD1 (new bullet) → T1 commit 2. DoD2 (lint pin red→green) → T1 commit 1. DoD3 (glossary mirror) → T2. DoD5 (full lint green) → T1 commit 2 + verify. DoD4 (krukit-v4 setup + prediction) → verify (design §Testing). Deliverability (live skill reflects change) → T3.
- Placeholder scan: no TODO/TBD/`...`; the only code block is the exact lint assertion; the bullet is verbatim from design.md. All decisions grilled — zero unresolved slots.
- Type consistency: T1 touches lint + SKILL.md (paired red→green); T2/T3 disjoint mechanical edits. No cross-task interface drift.

## Status (act, 2026-07-13)
- **T1 — DONE.** RED: 787428b (lint fails, bullet absent). GREEN: 53767bd (bullet added, full lint 11 skills exit 0).
- **T2 — DONE.** b3539bb (glossary mirror; lint unaffected, still green).
- **T3 — DONE (no-op).** No sync needed — see Learnings.

## Learnings
- **T3 premise was wrong: the live skill is a directory symlink, not a plain copy.** `~/.claude/skills/krukit-flow -> /Users/todmy/github/krukit/skills/krukit-flow` (same inode 236456938). The earlier `ls -l` on the *file* showed a regular file because only the *parent dir* is symlinked — misread as "plain copy." Consequence: the repo edit (T1c2) updated the live skill instantly (P4 "symlinked skills hit live sessions"); no `cp` required. Verify: `readlink ~/.claude/skills/krukit-flow`. This means ALL krukit skills likely live-mirror the repo via dir symlinks — future waves need no sync step.
