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
- [x] Handoff / session-summary principles → memory/README.md (owner chose Claude's eight principles, 2026-10-07)
- [x] Collaborator access + standalone repo: lashavamleti invited with write access (GitHub invitation 2026-10-07); CONTRIBUTING.md, docs/FILES.md; CLAUDE.md/PROCESS.md People + Safety
- [x] Scaffold merged into `main` as the shared base — PR #1, merge commit (owner's decision 2026-10-07)
- [x] Harness v0 (ADR-0005): .claude/settings.json + guard / commit-secrets / memory hooks — drill 89 cases ARMED, stub DEAD; live: `.env.probe` write and verifier `touch` blocked (2026-10-07)
- [x] Structure check in the repo (`sdlc/checks/check_structure.py`) — 269 checks PASS; seeded copy: 3/3 defects caught (now a drill case)
- [ ] CI: `.github/workflows/checks.yml` (structure, drill, stub drill, gitleaks) — tick when it is green on its own pull request
- [ ] Live `/compact` → handoff appears in memory/episodic/handoffs/ (hook logic drilled with synthetic input only)
- [ ] Owner reviews ADR-0001…0003, ADR-0005 and PROCESS.md → accepted (Phase 0 gate, after the dry run)
- [ ] Engine dry run: a toy intent through phases 1–6, every gate exercised
- [ ] Start the real product: `/sdlc-intent`

## Parked (გადადებული)
- [ ] Stage-2 orchestration (Fable 5.1, ChatGPT 6.1 Astra via Codex) — when the owner decides (ADR-0003)
- [ ] Engine regression evals: 20–50 real tasks, run on every change to CLAUDE.md / .claude/** — needs a GitHub remote + CI
- [ ] Terminal CLI `~/.local/bin/claude` is 2.1.92; the VS Code extension bundles 2.1.289 — update the CLI (owner's call)
- [ ] Global UserPromptSubmit hook calls MemPalace, but the package is not installed → fails silently on every prompt (owner's call; global config)

## Done log
- 2026-10-06 — repository initialised; branch `engine/v0-scaffold`.
- 2026-10-07 — lashavamleti invited; repo made standalone; PR #1 merged into `main`.
- 2026-10-07 — harness v0 built on `engine/v1` (ADR-0005); lashavamleti accepted the invitation.
