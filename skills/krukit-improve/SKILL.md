---
name: krukit-improve
description: Auto-improve a skill or command from its real execution traces — diagnose first decisive deviations, reflect, propose evidence-cited delta edits, verify behaviorally. One improvement cycle per run, human-gated. Use when the user says "krukit-improve", "autoimprove", "auto-improve", "крукіт імпрув", "покращ скіл", or wants a skill/command improved from how it actually performed. Companion skill of the krukit pipeline.
---

# Krukit Improve — Trace-Driven Skill Improvement

Companion skill of the krukit pipeline. Improves any skill or command (default candidates: the krukit suite itself) from evidence — real execution traces — not from vibes. One bounded improvement cycle per invocation; every edit cites a trace; the user is the acceptance gate. Research grounding: GEPA (reflect in language before editing), ACE (delta updates only — full rewrites cause context collapse and brevity bias), AgentDebug (fix the FIRST decisive deviation, not the last loud error), HarnessFix (attribute the failure layer before editing), CTA (verify by behavioral diff, not pass/fail), ReasoningBank (mine failures, not only successes). Interact with the user in the user's language.

## Inputs

- Target: a skill name (in `~/.claude/skills/`, project `.claude/skills/`, or plugins) or a command (`~/.claude/commands/`). Resolve like /halo does.
- Real traces: mined via `~/.claude/scripts/halo-collect-traces.py --skill <name> --max-traces 12 --follow 14 --truncate 600` (or `--command <name>`; raise `--follow` for skills with long execution chains — late-manifesting gate failures need more captured events). **Minimum 3 traces or refuse** — tell the user to use the skill more first; n=1 editing overfits to one bad day.
- For krukit-suite targets, extra evidence: `docs/krukit/*/flow-state.md` trails, `verify.md` findings, `## Learnings` sections in plan.md files.
- `<target-dir>/IMPROVE-LOG.md` if it exists — past accepted AND rejected edits (rejected proposals are negative feedback: never re-propose them).

## Process

1. **Collect.** Run the halo trace miner. Take successes AND failures — at low volume, failures carry most of the signal. If fewer than 3 traces: stop, report the guard.

2. **Diagnose** (per problematic trace): find the **first decisive deviation** — the earliest point where execution departed from what the skill instructs — not the final visible error, which is usually downstream. Classify each deviation by layer before any edit:

   | Layer | Symptom | Edit target |
   |---|---|---|
   | Trigger | skill never fired / fired wrongly | frontmatter description |
   | Instruction | body ambiguous, two readings at execution time | the specific body line |
   | Gate | gate passed when it shouldn't (or blocked wrongly) | gate item wording |
   | Harness | missing tool/permission, environment issue | not a skill edit — report separately |
   | Model | instructions fine, model erred anyway | no edit — note it; don't legislate one-off model errors |

3. **Reflect** in natural language BEFORE editing: for each diagnosed deviation, write 2-3 sentences — what in the file caused it, what change would have prevented it, what the change might break. Shallow diagnosis = bad mutation; this step is where the quality lives.

4. **Propose delta edits** — never a rewrite:
   - Each edit = add / update / replace of a specific line or bullet, with provenance: `(improve: <date>, trace <session-ref> — <one-line reason>)` recorded in IMPROVE-LOG.md (not inline in the skill — keep the skill clean).
   - Each edit cites its trace evidence. No trace citation = no proposal.
   - Edits over ~25 lines: flag NEEDS-MANUAL-REVIEW instead of proposing.
   - Check IMPROVE-LOG.md: previously rejected edits are not re-proposed.
   - **Hard line:** never propose weakening a Gate section, git rules, audit rules, or safety constraints of the target — making the gate easier to pass is objective hacking (the Darwin Gödel Machine failure), not improvement. This constraint applies to ITSELF: when the target is krukit-improve or any krukit skill, this hard line and the targets' gates may not be narrowed, qualified, reworded, or removed — not even as a "clarity edit".
   - Present each edit via AskUserQuestion (arrow-key form): problem-first text (the deviation + trace), options: Apply (Recommended, with reason) / Skip / Apply all remaining recommended. Final batch is shown before writing regardless of delegation.

5. **Apply + verify behaviorally.** Apply accepted edits. Then verify — pass/fail is nearly useless at n=few; behavior is the signal:
   - Reconstruct ONE representative scenario from a trace: take the earliest user-role message before the skill's invocation index (plus a 2-3 sentence summary of the session context) and feed it to a fresh subagent running with the EDITED skill. If no user turn is recoverable from the trace, skip the re-run and record `verification-skipped (trace-incomplete)` in IMPROVE-LOG.md — never fabricate a scenario.
   - Diff the new run against the original trace phase-by-phase: did the diagnosed deviation disappear? Did anything else change that shouldn't have?
   - If the target has a skill-creator eval set (`evals/evals.json`), offer running it instead (with-skill vs old-skill snapshot).
   - Regression in the diff → confirm the revert with the user (AskUserQuestion: revert (Recommended) / keep anyway), then record it in IMPROVE-LOG.md as `REVERTED` with the regression.

6. **Log.** Append to `<target-dir>/IMPROVE-LOG.md` in EXACTLY this format (re-runs parse `REJECTED:` lines by prefix to honor never-re-propose):

   ```markdown
   ## YYYY-MM-DD | traces: <n> | sessions: <refs>
   - ACCEPTED: <edit title> — <reason, trace ref>
   - REJECTED: <edit title> — <user's reason>
   - REVERTED: <edit title> — regression: <what>
   - VERIFICATION: <behavioral-diff result | verification-skipped (trace-incomplete)>
   ```

   One `##` block per cycle, one line per edit. One cycle per invocation — re-run later for the next cycle; do not loop autonomously (unverified reflections poison subsequent cycles).

## Outputs

- Edited target skill/command file (accepted, verified delta edits only).
- `<target-dir>/IMPROVE-LOG.md` — append-only history: accepted, rejected (negative feedback), reverted.
- Report: deviations found per layer, edits applied, verification result.

## Gate

- [ ] ≥ 3 real traces were mined and read; every proposed edit cites at least one.
- [ ] Every edit was a delta (add/update/replace of specific lines), no full-file rewrite.
- [ ] No Gate/git/audit/safety line of the target was weakened.
- [ ] User explicitly accepted each applied edit (or delegated via "all recommended"; final batch shown either way).
- [ ] Behavioral verification ran; regressions reverted and logged.
- [ ] IMPROVE-LOG.md updated.

If any condition fails: say what failed and stop.
