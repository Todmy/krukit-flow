# Verify: v2-wave1-layer0

Date: 2026-07-11 | Route: fix (design.md/plan.md absent by route — verified against inline task list + HARNESS-IMPROVEMENTS-DRAFT.md item texts)

## Evidence (fresh runs, output read)

| Claim | Command | Result |
|---|---|---|
| Lint green on whole skills tree | `python3 scripts/lint-consistency.py` | `OK: 11 skills checked, no consistency issues`, exit 0 |
| Lint catches drift (red proven) | same, at commit 437da4a | 6 issues (Task:-line drift), exit 1 — red for the right reason |
| db-wal-recovery flips to PASS | krukit-bench `jobs/sonnet-5-v2check/krukit-v2-r1` (Sonnet 5, condition file byte-identical to v1) | reward **1.0** (v1: 0.0), $0.83, 1.2M input |
| Snapshot rule fires BY MECHANISM, not luck | trace inspection, first Bash calls | cmd[1] read-only `ls`; cmd[2] `cp -p main.db + main.db-wal → work/` BEFORE any stateful tool; all inspection/decryption on `.orig` copies; originals never opened by sqlite3 |
| No asked-the-void terminations | AskUserQuestion count in both traces | 0 and 0 (v1: died asking for a reset) |
| cobol regression guard | same job | reward 1.0, $2.07 / 3.2M input (v1: $3.34 / 5.2M — −38% cost side effect; item-10 target ≤2× baseline still open: baseline $0.48) |

## Reality-check (read-only)

- Item-8 rule phrases verbatim in preamble ("copy first, inspect the copy"; "read-only tools before stateful ones"; "NEVER batch read-only inspection…") — confirmed by grep.
- Item-9 clauses present: deliverable gate, never-fabricate, gaps-stated, unexplained-completeness-as-defect.
- Item-11 autonomous half present; step-8 audit rule carve-out explicit — no contradiction remains.
- Both new sections pinned by lint (cannot silently vanish).
- No TODO/placeholder residue in changed files.
- Constitution absent in this repo (expected: skills define it for target projects); discovery order checked.

## Findings

| ID | Severity | Location | Summary | Recommendation |
|---|---|---|---|---|
| V1 | LOW | scripts/lint-consistency.py | "Duplicated templates identical" implemented as structural-row check, not byte-identity (placeholders legitimately differ: `Route: full` vs `<full or fix>`) | Keep; document if item 4 is ever revisited |
| V2 | LOW | scripts/lint-consistency.py | Item 4's "gate wording across skills" sub-check not implemented (scoped out of Wave 1) | Candidate for Wave 4 lint extension |

Metrics: requirements 3 (T1-T3) / implemented 3 / findings 2 (0 CRITICAL, 0 HIGH, 2 LOW).

## Gate

- [x] Full test suite ran (lint), output read, passing.
- [x] Validation plan executed: all three falsifiable predictions confirmed (db-wal PASS by mechanism; zero question-deaths; cobol PASS).
- [x] verify.md exists with findings table + metrics.
- [x] Zero CRITICAL, zero HIGH.
