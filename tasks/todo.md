# Tasks — Engine v0

> ახლა ეს ფაილი ძრავის აწყობას ემსახურება. Phase 5-ში (Plan) აქ პროდუქტის დავალებები ჩაიწერება, ძრავის დასრულებული დავალებები კი „Done log"-ში დარჩება.
> Rule: a box is ticked only with evidence (command + result, or commit).

## Engine v0
- [x] Study Anthropic's AI-native SDLC playbook (2026-08-21) → sdlc/research/playbook-notes.md
- [x] Evaluate the awesome-ai-pulse-georgia collection → sdlc/research/engine-selection.md
- [x] Verify harness facts in the Claude Code docs (bundled v2.1.289): compaction window, PreCompact/PostCompact, advisor, effort, subagent and skill front matter
- [x] Create the directory: CLAUDE.md, README.md, phase skills, subagents, templates, design docs, ADR-0001…0004
- [x] PROCESS.md (working agreement) + PROGRESS.md (work log) — added 2026-10-06 after the owner noticed they were missing
- [x] Memory & context interview → ADR-0004 accepted (2026-10-06: 65% · Obsidian vault · grep → QMD at trigger · ADR + git + wrap check)
- [ ] Owner writes the handoff / session-summary principles → memory/README.md
- [ ] Owner reviews the scaffold → ADR-0001…0003 accepted → merge `engine/v0-scaffold` into `main`
- [ ] Harness v0: .claude/settings.json (models, effort, advisor, compaction window, permissions baseline) + memory hooks (PostCompact → memory/, SessionStart → now.md + handoff)
- [ ] Drill every hook: clean control passes, seeded case fails
- [ ] Engine dry run: a toy intent through phases 1–6, every gate exercised
- [ ] Start the real product: `/sdlc-intent`

## Parked (გადადებული)
- [ ] Stage-2 orchestration (Fable 5.1, ChatGPT 6.1 Astra via Codex) — when the owner decides (ADR-0003)
- [ ] Engine regression evals: 20–50 real tasks, run on every change to CLAUDE.md / .claude/** — needs a GitHub remote + CI
- [ ] Terminal CLI `~/.local/bin/claude` is 2.1.92; the VS Code extension bundles 2.1.289 — update the CLI (owner's call)
- [ ] Global UserPromptSubmit hook calls MemPalace, but the package is not installed → fails silently on every prompt (owner's call; global config)

## Done log
- 2026-10-06 — repository initialised; branch `engine/v0-scaffold`.
