# Roadmap

Krukit is built and used daily. This is where it's headed.

## Near-term

- **Fewer moving parts.** Vendor the trace miner into `scripts/`, add an
  install script for the skill symlinks — the suite becomes self-contained.
- **Adversarial verify.** Reality-check invariants verified by a fresh
  subagent under a refutation framing ("try to refute that X holds"),
  not a confirmation one — closing the loop the honest way.
- **Reusable primitives.** Pull the building blocks — reality-check,
  constitution-check, clarification budget, resumable flow-state — out
  as skills in their own right.

## Direction

- Keep it simple and light: routing that keeps small changes small, gates
  that require real evidence, lossless resume across stages.
- Telemetry: `route-log.md` already records every routing decision;
  next is route-vs-cost analysis and published head-to-head numbers.
- Cost: light routes should stay within ~2× of a bare agent run —
  fresh-context stage subagents are the main lever.
- Portability to other agent runtimes once the core is self-contained.

Have an idea or a pain point? Open an issue.
