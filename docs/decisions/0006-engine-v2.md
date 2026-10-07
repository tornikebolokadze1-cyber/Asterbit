---
id: "0006"
title: Engine v2 — PRD and TRD, the Sonnet↔Opus review loop, memory v2, self-improvement, gates and event log, stage-2 notes
status: proposed
scope: engine
date: 2026-10-07
deciders: owner (choices on 2026-10-07), Claude (drafted; advisor Opus 5.5 — verdicts in Rationale)
supersedes: —
superseded_by: —
review_by: after the engine dry run
tags: [process, orchestration, memory, gates, observability]
---
# 0006 — Engine v2

## Context (კონტექსტი)
On 2026-10-07 the owner re-sent the original engine prompt and asked to add everything the engine still lacks, agreeing first on any fragment taken from other repositories. Research: `sdlc/research/repo-study.md` (nine repos studied at code level, fragments F1–F18), `sdlc/research/models-gpu-graphs.md` (web research, 2026-10-07) and `sdlc/research/engine-v2-gaps.md` (the prompt compared with the engine, packages P1–P6). Thin-engine goal from the prompt: "not a large engine with thick layers, but a concrete, targeted, thin one".

## Options considered (განხილული ვარიანტები)
Asked with AskUserQuestion on 2026-10-07 (owner's choice in bold):
- Compaction threshold — the prompt says 70%, ADR-0004 accepted 65%: **keep 65%** / move to 70% (new ADR).
- PRD and TRD: **separate files in Phase 2** (docs/prd.md before the ADRs, docs/trd.md after them; the spec references both) / two sections inside docs/spec.md / folded into intent.md and the ADR index.
- Scope of the review loop: **every milestone plus every `[high-risk]` task** / every task / milestones only.
- Packages to build: **P1+P2, P3+P4, P5, P6 — all**; P3 and P5 change hooks and settings, and the owner's selection is the required yes.
- Code graph (ADR-0004 chose "Obsidian vault only"): **wait for code** (Graphify when product code exists, codebase-memory-mcp at ~50 source files, decided by a new ADR then) / Graphify now / neither until needed.
Per-option trade-offs: `sdlc/research/engine-v2-gaps.md` §1–§3.

## Decision (გადაწყვეტილება)
1. **PRD and TRD (P1).** Phase 2 runs PRD → ADRs → TRD (templates `sdlc/templates/prd.md`, `trd.md`). The spec is the agreed contract built from both and references them by ID (P-n, J-n, TR-n). Each of PRD, TRD and spec gets a cold-reader test: a fresh subagent reads only that document and answers a builder's questions (F3). Unknowns are marked `[NEEDS CLARIFICATION: …]`; `check_structure.py` fails an approved artifact that still has one, an approved PRD whose must-priority feature reaches no requirement, and an approved plan that leaves a requirement out (F8, F9).
2. **Review loop (P2).** The Sonnet↔Opus code review runs at every milestone and on every `[high-risk]` task, and every auditor loop — gate audit, milestone, `[high-risk]` task or engine change — has the same shape: review 1 → fix 1 → review 2 → fix 2 → review 3 (final) → the owner. Loop ids: `M1`, `M1-T4`, `gate-spec`, `ENG-…`; work the owner asks for after an escalation is a new loop (`<id>-r2`). Reviews 2 and 3 judge only the fix — ADDRESSED / NOT ADDRESSED — and keep anything outside the fix diff as out-of-scope observations (F4). LOW findings never use a round; the author's report counts as unverified claims (F5). If HIGH+MEDIUM do not fall between two reviews, the loop stops early (F7). Rounds are counted by `sdlc/checks/review_rounds.py` in the append-only ledger `tasks/review-log.jsonl`, never from memory (F6); it refuses a review 2 or 3 whose range is not exactly the fix (previous review's head → fix commit), a fix without a new commit, and negative counts, and reports a malformed ledger as INCONCLUSIVE. This refines the loop limit of ADR-0003 ("2 auditor fix rounds, then UNVERIFIED"), which had no final re-review. Every changed line traces to the task (F15); deliberate shortcuts carry an `asterbit-debt:` marker (F16).
3. **Memory v2 (P3).** A PostToolUse hook computes context use from the transcript's token counts and, 10 points before the compaction threshold it reads from `.claude/settings.json` (55% today), asks for a checkpoint written into this session's single rolling handoff file. Injected memory is fenced on both sides and scanned for injection patterns before it is saved (F10, F12). A hygiene check reports what to archive or revisit; `/sdlc-wrap` consolidates when the ADR-0004 trigger is reached. A live `/compact` test closes ADR-0004's open verification.
4. **Self-improvement (P4).** The memory map names the procedural layer (CLAUDE.md rules, skills, checks, lessons). Every correction is classified: mechanical → a check; judgement → a rule (F1). A script groups lessons and proposes a rule once a lesson repeats across 2 sessions — the existing "corrected twice" rule, owner approves (F11). New engine parts need an observed failure or the owner's explicit request (F2).
5. **Gates and event log (P5).** One gate runner reports PASS / FAIL / INCONCLUSIVE separately and never counts "0 tests" as green (F13, F14). A hook appends redacted agent events to `.claude/logs/` (not in git) and a report summarises a session (F18).
6. **Stage 2, documented only (P6).** The real OpenAI IDs are `gpt-6-astra` and `gpt-6.1-sol` (ADR-0003 said "ChatGPT 6.1 Astra"); cross-vendor review via the Codex plugin with `gpt-6.1-sol`, `gpt-6-astra` for milestone audits. A local open-weight model is tried through a hosted API first; a GPU is rented only for privacy (RunPod RTX PRO 6000, Hetzner as EU fallback). Activation still needs its own ADR.
7. **Not adopted:** typesafe.ai (probabilistic, not a deterministic gate; no published data-retention policy), Neo4j / Graphiti / Cognee, and the thick parts listed in `repo-study.md` §4.

## Rationale (რატომ)
Advisor (Opus 5.5) verdicts in the coder's session: before the research — split the repo study across agents, ask the owner the 65%/70% conflict instead of acting, keep this turn to research; after the research — move Graphify for code into its own question (ADR-0004 chose Obsidian only), keep lesson graduation at 2 (the CLAUDE.md rule), run the context monitor on PostToolUse with the threshold read from settings, keep logs in `.claude/logs/`, ship packages as separate milestones and PRs. All were applied.

Every addition closes a gap the owner named in the prompt, and each one lands as a few lines in an existing skill, agent or check, or as one small standard-library script — the thin-engine goal. Limits that used to be prose ("2 rounds", "no unknowns left", "traced to a task") become machine checks, because a rule the model remembers is a rule the model can forget.

## Consequences (შედეგები)
- Positive: the owner's exact review loop is enforced by a counter; PRD/TRD are testable for clarity; memory checkpoints happen before compaction, not only at it; lessons become checks.
- Negative: Phase 2 grows by two documents; the auditor runs up to three times per milestone (Opus cost, accepted by design in ADR-0003); hooks gain two scripts to maintain.
- Harder: the review ledger must be fed by the coder after every review and fix — `status` exits 2 rather than guessing if the ledger is unreadable.
- ADR-0004's Verification line "None of these exist yet" is out of date — the `memory/now.md ≤120` check already runs in `check_structure.py`. ADR-0004 is accepted and is not rewritten; this note records it.

## Verification (როგორ შევამოწმებთ)
- P1+P2: `python3 sdlc/checks/check_structure.py` PASS; `python3 sdlc/checks/drill_hooks.py` ARMED (105 cases), including 12 `review_rounds` cases and 5 artifact cases — two clean controls (one built from the real templates) and three seeded sets (open marker, untraced must-feature, untraced requirement; an approved spec with no requirement and an unknown status; an open question hidden in an Obsidian callout). Only the templates' exact placeholder `[NEEDS CLARIFICATION: <question>]` is exempt from the marker check.
- Stub mode (`ASTERBIT_DRILL_STUB=1`) stubs hooks only, so it proves nothing about these check drills. They were proved by mutants in a scratch copy, one at a time: blockquotes counted in `content_lines()` → the template clean control reported FALSE-BLOCK; the fix-range rule disabled in `review_rounds.py` → its case MISSED; finding counts typed `int` instead of `count` → the negative-count case MISSED; earlier, `MAX_FIXES = 3` and a removed `check_artifacts()` call → their cases MISSED. Each run exited 1. The review loop for this package is recorded in `tasks/review-log.jsonl` (loop `ENG-v2-P1P2`).
- P3–P5: `drill_hooks.py` adds 7 hook cases — plain handoff not flagged; injection-like summary flagged and its invisible character stripped; context fenced with one nonce and a forged fence neutralised; context monitor silent at 30%, one reminder at 56% that is not repeated, 'could not measure' said once; event log redacts a secret and marks a failure — and `drill_checks.py` adds 11 script cases (memory_hygiene, lessons_graduate, run_gates, agent_report: a clean control for each, seeded defects caught, missing input INCONCLUSIVE).
- Live, in the session that built them (2026-10-07): with the new settings loaded, `event_log.py` wrote 6 lines including one attributed to the `auditor` subagent, and `context_monitor.py` measured the real transcript (below 55%, no reminder). Still open: a real `/compact` to confirm the checkpoint → summary → archive chain end to end.
- P6 is documentation only; `grep -rn "6\.1 Astra"` leaves only lines that explain the name does not exist.

## Links
- sdlc/research/engine-v2-gaps.md · sdlc/research/repo-study.md · sdlc/research/models-gpu-graphs.md
- ADR-0003 (loop limit refined), ADR-0004 (compaction kept at 65%; graph unchanged)
