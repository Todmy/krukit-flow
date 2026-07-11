# Krukit Flow: v2-wave2-router-diet
Started: 2026-07-11 | Route: full
Task: Wave 2 of HARNESS-IMPROVEMENTS-DRAFT v2 plan — (a) route table v2: `direct` route for task-TYPE mismatch + capability self-check at Stage 0 + README minimum-capability bar (item 12a,b); (b) cost diet: bookkeeping batching, artifact-once-per-stage, verify depth by risk, slim fix-route instructions (item 10, target fix ≤ 2× baseline). Spec: HARNESS-IMPROVEMENTS-DRAFT.md "Synthesis & v2 architecture".
- [x] 1 recon — done 2026-07-11, artifact: context.md
- [x] 2 grill — done 2026-07-11, artifact: flow-state.md
- [x] 3 design — done 2026-07-11, artifact: design.md
- [x] 4 plan — done 2026-07-11, artifact: plan.md
- [x] 5 act — done 2026-07-11, artifact: plan.md (7 tasks, commits 96bb4c0..+README)
- [ ] 6 verify
- [ ] 7 review

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
