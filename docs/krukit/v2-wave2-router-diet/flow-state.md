# Krukit Flow: v2-wave2-router-diet
Started: 2026-07-11 | Route: full
Task: Wave 2 of HARNESS-IMPROVEMENTS-DRAFT v2 plan — (a) route table v2: `direct` route for task-TYPE mismatch + capability self-check at Stage 0 + README minimum-capability bar (item 12a,b); (b) cost diet: bookkeeping batching, artifact-once-per-stage, verify depth by risk, slim fix-route instructions (item 10, target fix ≤ 2× baseline). Spec: HARNESS-IMPROVEMENTS-DRAFT.md "Synthesis & v2 architecture".
- [x] 1 recon — done 2026-07-11, artifact: context.md
- [x] 2 grill — done 2026-07-11, artifact: flow-state.md
- [x] 3 design — done 2026-07-11, artifact: design.md
- [x] 4 plan — done 2026-07-11, artifact: plan.md
- [x] 5 act — done 2026-07-11, artifact: plan.md (7 tasks, commits 96bb4c0..+README)
- [x] 6 verify — done 2026-07-11, artifact: verify.md
- [x] 7 review — done 2026-07-11, artifact: flow-state.md

Route gate evidence:
> "full (Recommended)" — 2026-07-11

Constitution: bootstrapped v1.0.0 this flow (grilled setup, 4 interview answers all "(Recommended)", draft approved):
> "Затвердити (Recommended)" — 2026-07-11

Validation plan (for stage 6): krukit-bench as krukit-v2 — cobol-modernization cost ≤ 2× baseline ($0.48 → target ≤ $0.96-1.00); hard-pair password-recovery + write-compressor to observe direct-route behavior (choice logged, Layer-0 invariants still applied).

## Grill summary (2026-07-11)

Resolved decisions (gate evidence — user picked each "(Recommended)" in 2 batched rounds):
1. **Route table:** keep `trivial` (SIZE) AND add `direct` (TYPE: not feature work). ALL routing decisions append one line to `docs/krukit/route-log.md` (`YYYY-MM-DD | <task> | <route> | <reason>`, append-only, new file — P4-safe). Telemetry for route-vs-cost.
   > "Тип≠розмір + route-log (Recommended)" — 2026-07-11
2. **Capability self-check:** categorical harness-declared model tier (never self-assessment); below Sonnet-class → `full` forbidden, cap = `fix`; `direct`/`trivial` open to all tiers. README gets Requirements section.
   > "Модель-tier з харнеса (Recommended)" — 2026-07-11
3. **Verify depth:** minimal SHOULD-rule only — exact oracle green ⇒ one verification cycle; recorded as IMPROVE-LOG candidate pending a second DISTINCT trace (P6 honesty). Full risk-matrix DEFERRED to Wave 4 (reason: only 2 traces of the same task today).
   > "Мінімальне SHOULD-правило (Recommended)" — 2026-07-11
4. **Act/flow diet, full package:** (a) act's two AskUserQuestion → one batched call; (b) flow-state becomes the single tracker, TodoWrite steps removed from flow; (c) Learnings only when tasks >1; (d) commit-per-task stays (P10). Persist-first untouched — only recoverable bookkeeping batches, never the resume source.
   > "Весь пакет (Recommended)" — 2026-07-11
5. **README P3 debt:** mini-compliance in this wave — source/date the sourced claims, rewrite "simpler/clearer/lighter" as mechanism claims.
   > "Міні-комплаєнс зараз (Recommended)" — 2026-07-11

Sharpened terms → CONTEXT.md created (glossary: route, direct, trivial, route-log, capability bar, Layer-0, exact oracle).
ADRs: none — no decision met all three bar criteria (hard-to-reverse + surprising + real trade-off).
Deferred: full verify risk-matrix → Wave 4 (P6: needs recurring pattern across distinct tasks).
Process note (trace for krukit-improve): grill's "one question per turn" was consciously batched into 2 rounds of 3+2 — approval-fatigue evidence (item 11); candidate edit for krukit-grill.

Design gate evidence:
> "Затвердити (Recommended)" — 2026-07-11

## Review summary (2026-07-11)

Independent fresh-context review of diff 9c9f5bf..HEAD: 0 Critical, 2 Important, 8 Minor.
- Fixed (4 commits 377670e..38c0cc6): Important-1 act Learnings gate contradiction + fix-route Learnings home; Important-2 README uncited "demonstrably" + Minor-10 casing; Minors 3/5/6 glossary term+override, IMPROVE-LOG renumbering note, trivial-cell wording; Minor-4 lint regex-dark fail-loud.
- Declined with reasons: Minor-7 (autonomous evidence for artifactless routes — route-log line IS the designed evidence home; revisit with the V2 telemetry candidate); Minor-8 (hardcoded "five routes" counts — adjacent to the table they describe, low drift risk, P2/P6 against a lint knob now); Minor-9 (list-revision-across-boundary edge in the merged round — no trace of it occurring, P6; persist-first re-confirmation handles it naturally).
- Branch outcome: all work on main by session convention (private repo, user-observed); nothing pushed. No worktrees created.
- Knowledge capture: no .valis.json in repo — Valis skipped; durable lessons routed to IMPROVE-LOGs instead (grill question-batching deviation; act fresh-context threshold by task SIZE not count — both recorded as candidates in this flow's trace).

## Constitution close (2026-07-11)

No amendment this time. Candidates considered and routed elsewhere: "telemetry is never state" (corollary of P4, would duplicate); "batch questions at stage boundaries" (skill-level improvement for krukit-grill/design, not project-wide); "fresh-context threshold by task size" (krukit-act IMPROVE-LOG candidate). Constitution stays at v1.0.0.
