# CONTEXT — krukit glossary

- **route** — Stage-0 classification of a task: `direct | trivial | fix | full | external-spec`. Decides which pipeline stages run.
- **direct route** — escape hatch by task TYPE: the task is not feature work (forensics, puzzle, ops). No pipeline stages; Layer-0 invariants still apply; decision logged to route-log.
- **trivial route** — escape hatch by SIZE: feature work small enough for "do it + run the relevant test". No pipeline stages; Layer-0 invariants still apply; decision logged to route-log.
- **route-log** — `docs/krukit/route-log.md`, append-only, one line per routing decision (`YYYY-MM-DD | <task> | <route> | <reason>`), written at Stage 0 for EVERY route. Telemetry source for route-vs-cost analysis.
- **capability cap** — categorical minimum model tier per route: `full` requires a Sonnet-class or stronger model, as declared by the harness (never model self-assessment). Below the bar: autonomous runs cap the route at `fix`; interactive runs warn and allow an explicit, logged user override.
- **Layer-0 invariants** — route-independent floor in krukit-flow (snapshot-before-touch, deliverable gate, deadline gate, never-fabricate). Apply on every route, lint-pinned.
- **deadline gate** — Layer-0 invariant: on long/search/compute-bound work, write a one-line deadline plan, then climb baseline-first — simplest verifiable deliverable on disk first, improved in place, long rungs backgrounded/bounded. A partial on disk is a safety net against the cutoff, never an exit while budget remains (assumed unless the harness says otherwise) and verification has not passed against the task's declared success criteria. Composes with (never overrides) the other invariants.
- **deadline plan** — one line, written before committing to an approach on deadline-gate work: cheapest end-to-end baseline → escalation rungs → when the first write hits disk. Lives in the route-log line or the first artifact.
- **baseline-first ladder** — execution order under the deadline gate: secure the simplest verifiable end-to-end deliverable before any deep approach; escalate only from a secured rung.
- **exact oracle** — a deterministic, binary completion check (byte-identical diff, golden file). When green, one verification cycle suffices.
