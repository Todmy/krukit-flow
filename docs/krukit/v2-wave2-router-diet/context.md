# Context: v2-wave2-router-diet

## Goal

Add a `direct` route + capability self-check to Stage 0 and cut fix-route turn cost (target ≤2× baseline, now ~4.3×) — without breaking resume compatibility (P4) or the Layer-0 floor (P5).

## Affected map

| File | Role | Who depends on it |
|---|---|---|
| skills/krukit-flow/SKILL.md | Route table L38-43 + **9 route-name references** (L12 invariants, L36 "four routes", L47 discovery-routing, L49/64 flow-state creation, L65/74 constitution open/close, L68 stage order, L85/87 gate) + TodoWrite steps 5/7 | Every stage skill reads the flow-state it creates; lint pins §Invariants + §Autonomous mode |
| skills/krukit-act/SKILL.md | Fix-route inline list: persist-FIRST + confirm (2 AskUserQuestion rounds), per-task ticks, per-task Learnings append, commit-per-task | IMPROVE-LOG accepted entry (2026-06-12) mandates persist-before-confirm |
| skills/krukit-verify/SKILL.md | Uniform 6-point reality-check + full-suite + red-then-green; no risk scaling | Fix route: "verify against whatever exists" |
| skills/krukit-grill/SKILL.md, krukit-design/SKILL.md | Mid-stage incremental writes (grill: inline CONTEXT.md/ADR; design: 3 sequential passes on design.md) | Full route only — secondary diet targets |
| README.md | L9 route enumeration ("trivial / fix / full / external-spec"); no capability section; **4 claims P3 would flag** (L11 "12 validated pain points"/"#1", L37 "simpler/clearer/lighter", L41 "six tools", L43 "most-reacted") | Public-facing |
| scripts/lint-consistency.py | Pins: 2 flow sections, 7 template rows, frontmatter, Stage-N. **Does NOT validate the route table** | Constitution P8 |

## Patterns to follow

- **Wave-1 pin pattern:** new load-bearing sections land with a lint pin proven red→green (P1, P8) — `docs/krukit/v2-wave1-layer0/` is the worked example.
- **Fold, never add rounds:** IMPROVE-LOG flow-c2 (ACCEPTED) folds task-candidate derivation into the SAME routing question — the capability self-check must fold into the existing route question, not add a round.
- **Persist-first:** IMPROVE-LOG act entry (ACCEPTED) — task list persists to flow-state BEFORE confirmation; any bookkeeping batching keeps interruption-survival.
- **Additions-only formats (P4):** header appends (`| Mode:`, `| Discovery:`) are the precedent for extending flow-state without migration.

## Invariants

- P4: existing flow-state files (headers, row markers, gate-evidence formats — full inventory in recon agent-C report) must parse unchanged; `Route: direct` is a new value, never a rename.
- P5: §Invariants (all routes) applies to `direct` too — its L12 route enumeration must include the new route.
- Lint pins survive: §Invariants, §Autonomous mode, 7 template rows, frontmatter.
- Route question stays ONE AskUserQuestion round (flow-c2 precedent).
- P2: krukit-flow SKILL.md will GROW (new row + self-check) — commit must justify; the diet must net-shrink act/verify to compensate.
- IMPROVE-LOG flow-c3 deferred "full-then-collapse re-route checkpoint" is item 1 / Wave 4 — NOT this wave's scope.

## Risks

- **Batching vs crash-recovery:** batching flow-state writes to stage boundaries could lose mid-act tick state — direct tension with the persist-first pattern; diet edits must distinguish "recoverable bookkeeping" (batch) from "resume source" (persist immediately).
- **Capability self-check signal:** model self-report is miscalibrated (deep-research corroborated); P7 bans numeric scores → the check must be a categorical, externally-observable rule, and its wording must not insult the runtime model into pathological behavior.
- **README P3 debt:** the 4 flagged claims predate the constitution; touching README for the capability bar surfaces them — fix or record as explicit debt, but not silently.
- **direct/trivial confusion:** two "light" routes with fuzzy boundary would reproduce the routing ambiguity the bench punished; the table wording must make TYPE (direct) vs SIZE (trivial) unmistakable.
- **TodoWrite dependency:** flow steps 5/7 assume a todo tool; IMPROVE-LOG flow-c1 already logged harnesses where it's absent — diet direction (flow-state as single tracker) also fixes portability.

## Open questions

1. `direct` vs `trivial`: keep both (type vs size) or merge into one non-pipeline route? Where does direct's one-line log live if the route produces "no artifacts, no flow-state"?
2. Capability self-check: what categorical signal decides "below the bar" (declared model tier? harness env? user statement?), and what does it cap — full→fix only, or also fix→direct?
3. Verify-depth-by-risk: what categorical trigger (byte-identical oracle exists / route==fix / diff ≤ N files)? Does it clear P6's ≥2-trace bar today (cobol v1 over-verification + which second trace)?
4. Cost-diet scope in act: merge the two AskUserQuestion rounds into one? Drop per-task Learnings on single-task fixes? Keep commit-per-task (P10 says yes)?
5. README claims: fix the 4 P3-flagged claims in this wave or record as debt with owner/date?
6. Does `direct` write the route decision anywhere machine-readable for the bench/miner (route-vs-cost metric needs it), and is one appended line to a shared log P4-safe?
