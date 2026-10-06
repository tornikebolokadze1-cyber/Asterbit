---
name: sdlc-observe
description: Phase 9 — build AI observability: what the agent (Claude Code and/or the product agent) did, why, at what cost, and whether it worked — through structured logs, traces, dashboards and control-band alerts. Use when setting up logging or monitoring, when investigating what an agent did, or before release.
---
# Phase 9 — AI observability

Read `sdlc/design/ai-observability.md` first — it holds the event schema and the stack options.

## Steps
1. Agree with the owner which questions must be answerable later — for example: What did the agent do? Why? How much did it cost? Did it break anything? Who approved it?
2. Choose the stack from the design doc's options (AskUserQuestion, recommendation first) and record an ADR.
3. Instrument: Claude Code's OpenTelemetry export (if chosen — exporter variables belong in user settings or the environment, because Claude Code ignores them in a repo's .claude/settings.json) and/or product-agent traces following the event schema in the design doc. Never log secrets or personal data.
4. Define control bands for 1–3 metrics (e.g. eval pass rate, cost per day, error rate) and the response tier for each breach: log → diagnose read-only → propose a fix as a new intent.
5. Drill: emit a known event and find it in the store; breach a band on purpose and see the alert.
6. `auditor` (gate: observability) → owner approval → phase 9 `approved` + a gate-log line.

## Done when
Every question from step 1 is answerable from the store, logs are checked free of secrets and personal data, and at least one band alert was drilled end to end.
