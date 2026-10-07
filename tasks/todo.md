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
- [x] CI: `.github/workflows/checks.yml` (structure, drill, stub drill, gitleaks) — green on PR #2, all 7 steps ran (https://github.com/tornikebolokadze1-cyber/Asterbit/actions/runs/37601321945)
- [x] Live compaction → handoff appears in memory/episodic/handoffs/ — proven 2026-10-07 23:00 by a real auto compaction: the checkpoint went to `memory/archive/handoffs/2026-10-07-df3e2417.v2.md`, the new live handoff has `compaction: 3` and `injection_flags:`, SessionStart re-injected memory inside a nonce fence. Found on the way: subagent compactions overwrite it (A2)
- [x] Research of Anthropic's current guidance + independent engine assessment (2026-10-08): `sdlc/research/anthropic-guidance-2026-10.md`, `claude-models-2026-10.md`, `engine-assessment-2026-10.md` (auditor: "READY FOR DRY RUN: no — 6 blocking items"); ADR-0007 proposed
- [ ] Owner chooses ADR-0007's roles (A / B / C) and what happens to the Codex plugin
- [ ] Owner reviews ADR-0001…0003, ADR-0005, ADR-0006, ADR-0007 and PROCESS.md → accepted (Phase 0 gate, after the dry run)
- [ ] Engine dry run (new session): expense calculator web page, phases 1–6, branch `dryrun/expense-calculator` never merged, every gate exercised with approvals marked DRY-RUN (owner's choice 2026-10-07)
- [ ] Start the real product: `/sdlc-intent`

## Before the dry run (auditor, 2026-10-08 — details in `sdlc/research/engine-assessment-2026-10.md`)
> Hook, settings and CLAUDE.md changes need the owner's yes (CLAUDE.md Safety).
- [ ] A1 (HIGH) Dry-run rule in CLAUDE.md and PROCESS.md: on `dryrun/*`, phases 1–6 run while Phase 0 is in progress; approvals `owner (DRY-RUN), <date>`; Phase 3 proposes a settings diff but does not change the live `.claude/`; the branch is never merged
- [ ] A2 (HIGH) `memory_handoff.py`: a subagent's compaction must not replace the main session's handoff (log the PostCompact input keys once to confirm `agent_id`); drill case
- [ ] A3 (MEDIUM) `memory_context.py`: on `compact` skip the handoff (the summary is already in context); on `startup` pick the newest by time, not by file name; drill cases
- [ ] A4 (MEDIUM) `context_monitor.py` and `agent_report.py`: measure the last `usage.iterations` item of type `message`; de-duplicate by `message.id`; drill with an advisor-shaped line
- [ ] A5 (MEDIUM) `check_structure.py`: do not link-check `memory/episodic/**` and `memory/archive/**`; drill case
- [ ] A6 (MEDIUM) Before the run: `claude update` (≥ 2.1.293, owner's yes), a new session without `/model`, then record `/status` (model, version) and `/tasks` (subagent models) in PROGRESS.md

## Parked (გადადებული)
- [ ] **Security gap, owner's yes needed (found 2026-10-07):** `.claude/hooks/commit_secrets.py` scans the repository of the session's `cwd`, not the one a command switches to — `cd <other repo> && git commit …` or `git -C <dir> commit …` is not scanned (ADR-0005 hook). Seen while committing from a git worktree; the commits were then scanned by hand (gitleaks 3 commits, built-in patterns: no leaks). Fix: resolve the target directory from `cd`/`-C` in the command, plus drill cases
- [ ] Flaky drill case (found 2026-10-07): `commit_secrets` "generic key only gitleaks knows" MISSED in 1 of 4 local runs, so CI can turn red at random. Likely cause UNVERIFIED: the random value can hit a gitleaks stopword or entropy limit. Fix: a deterministic high-entropy value assembled at run time, then 20 repeated runs
- [ ] Auditor LOW (ENG-v2-P1P2 review 1): requirements in `docs/changes/<n>/` are traced against the root `tasks/todo.md`, so a change's requirement can look traced by an unrelated product task with the same ID — use a change-local todo or prefixed IDs when the first change folder appears
- [ ] Auditor note (ENG-v2-P1P2 review 1): `review_rounds.py` checks SHA format only, not that the commits exist or that base is an ancestor of head — add a `git merge-base --is-ancestor` check if a wrong range is ever recorded
- [ ] Stage-2 orchestration (Fable 5.1; OpenAI `gpt-6.1-sol`, `gpt-6-astra` for milestone audits, via Codex; an open-weight model through a hosted API first) — when the owner decides (ADR-0003, ADR-0006, sdlc/research/models-gpu-graphs.md)
- [ ] Code graph: Graphify when product code exists, codebase-memory-mcp at ~50 source files — new ADR at that point (owner's choice 2026-10-07, ADR-0006)
- [ ] Engine regression evals: 20–50 real tasks, run on every change to CLAUDE.md / .claude/** — CI exists (PR #2); built from the dry run's real tasks (sdlc/design/evals-and-gates.md §5)
- [ ] Auditor LOWs (ENG-v2-P3P6 review 1), parked: `run_gates.py` reports a bad gate config (invalid regex, missing group, unreadable file) as FAIL (exit 1) instead of INCONCLUSIVE; `agent_report.py` turns the whole report INCONCLUSIVE on one corrupt log line and prints "context now 0" when a transcript has no usage; `memory_handoff.py` archives a hand-written checkpoint as a version, so the first real compaction reads `compaction: 2`
- [ ] Auditor LOW (ENG-v2-P3P6 review 2), parked: `context_monitor.py` skips any event with `agent_type`; if Claude Code also sets it on the main thread of a `claude --agent <name>` session (unverified), the monitor would stay silent there — `agent_id` alone marks a subagent. Verify against real hook input before changing; the project sets no `agent` today
- [ ] Observation (ENG-v2-P3P6 review 2, owner's yes needed — ADR-0005 hook): `guard.py` blocks the read-only `git stash list` for read-only agents ("a git command that changes the repo")
- [ ] Claude Code is 2.1.292 here, both the terminal CLI and the VS Code extension (checked 2026-10-07); 2.1.293 adds Haiku 5.5 and fixes Claude misreading its own pre-compaction actions — see A6 (owner's call)
- [ ] Auditor recommendations B1–B11 (2026-10-08), not blocking — `sdlc/research/engine-assessment-2026-10.md`. B4 is the `commit_secrets` item above; B10 (`AGENT_MODELS` allows only Opus and Sonnet) becomes blocking if the owner picks ADR-0007 option B or C
- [ ] Global UserPromptSubmit hook calls MemPalace, but the package is not installed → fails silently on every prompt (owner's call; global config)

## Done log
- 2026-10-06 — repository initialised; branch `engine/v0-scaffold`.
- 2026-10-07 — lashavamleti invited; repo made standalone; PR #1 merged into `main`.
- 2026-10-07 — harness v0 built on `engine/v1` (ADR-0005); lashavamleti accepted the invitation.
