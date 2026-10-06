---
name: sdlc-harness
description: Phase 3 — define the harness: permissions, boundaries, autonomy tier and security rules for Claude Code in this repo and, if the product is an agent, for that agent; plus context-window and memory settings. Produces .claude/settings.json, .claude/hooks/ and an ADR. Use after architecture is approved, or whenever permissions, hooks, compaction or memory need to change.
---
# Phase 3 — Harness

The harness is everything around a model that decides what it can see, touch and remember. There can be two: Claude Code's own harness in this repo (always) and the product agent's harness (only if the product is or contains an agent).

## Before you start
- Gate: phase 2 `approved`. Read the accepted ADRs — the chosen stack decides which commands are safe to pre-approve.
- Read sdlc/design/memory-and-context.md and ADR-0004: the engine-level memory mechanics are decided there; this phase only tunes them.
- Read sdlc/design/ai-security.md, layers 1–3.

## 1. Claude Code harness (this repo)
One topic per question round, in Georgian, each with a recommendation:
1. Autonomy tier per environment — read-only / propose / act / deploy. Default: act locally on a branch; never deploy or push without the owner.
2. Permissions — `allow` the safe inner loop of the chosen stack (test, lint, build, git status/diff/log); `ask` for installs, network calls and pushes; `deny` reading secrets (.env*, secrets/**), destructive commands and pushes to main.
3. Protected paths — what a hook must block (generated code, migrations, CI config, test files during a fix task).
4. Deterministic guards (hooks) — fast, scoped to the changed file; every block explains its reason and the route to approval.
5. Context and memory — compaction window and the memory hooks from ADR-0004.
Write `.claude/settings.json` and `.claude/hooks/*`, then record every choice in an ADR (`scope: engine` for Claude Code, `scope: product` for the agent).

## 2. Product agent harness (only if the product is or contains an agent)
Specify, ready to paste into docs/spec.md: tool allowlist; data it may read and write; actions that need human approval; spend and rate limits; memory scope and retention; prompt-injection defences (untrusted input stays data); a kill switch.

## 3. Prove it — an undrilled gate is not evidence
For every blocking hook or deny rule: a clean control that passes and a seeded violation that is blocked (exit code 2 or a deny). Paste both outputs into the ADR's Verification section.

## Close
`auditor` (gate: harness) → owner approval → phase 3 `approved` + a gate-log line → commit. Next step: `/sdlc-spec`.

## Done when
Settings and hooks are committed, every blocking control has a recorded drill, and the ADR explains each choice in plain language.
