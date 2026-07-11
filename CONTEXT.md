# CONTEXT — krukit glossary

- **route** — Stage-0 classification of a task: `direct | trivial | fix | full | external-spec`. Decides which pipeline stages run.
- **direct route** — escape hatch by task TYPE: the task is not feature work (forensics, puzzle, ops). No pipeline stages; Layer-0 invariants still apply; decision logged to route-log.
- **trivial route** — escape hatch by SIZE: feature work small enough for "do it + run the relevant test". No pipeline stages; Layer-0 invariants still apply; decision logged to route-log.
- **route-log** — `docs/krukit/route-log.md`, append-only, one line per routing decision (`YYYY-MM-DD | <task> | <route> | <reason>`), written at Stage 0 for EVERY route. Telemetry source for route-vs-cost analysis.
- **capability cap** — categorical minimum model tier per route: `full` requires a Sonnet-class or stronger model, as declared by the harness (never model self-assessment). Below the bar: autonomous runs cap the route at `fix`; interactive runs warn and allow an explicit, logged user override.
- **Layer-0 invariants** — route-independent floor in krukit-flow (snapshot-before-touch, deliverable gate, never-fabricate). Apply on every route, lint-pinned.
- **exact oracle** — a deterministic, binary completion check (byte-identical diff, golden file). When green, one verification cycle suffices.
