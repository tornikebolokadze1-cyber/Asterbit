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
- [x] Owner chose ADR-0007's roles: **A** (2026-10-08); Codex and CodeRabbit stay installed for now; `scout` (Haiku 5.5) created after `claude update` (CLI 2.1.293, VS Code extension 2.1.294)
- [ ] Owner reviews ADR-0001…0003, ADR-0005, ADR-0006, ADR-0007 and PROCESS.md → accepted (Phase 0 gate, after the dry run)
- [ ] Engine dry run (new session): expense calculator web page, phases 1–6, branch `dryrun/expense-calculator` never merged, every gate exercised with approvals marked DRY-RUN (owner's choice 2026-10-07)
- [ ] Start the real product: `/sdlc-intent`

## Before the dry run (auditor, 2026-10-08 — details in `sdlc/research/engine-assessment-2026-10.md`)
> Hook, settings and CLAUDE.md changes need the owner's yes (CLAUDE.md Safety).
> Fixed 2026-10-08 on `engine/dryrun-blockers` (owner's yes). Every new drill case below was run against the old code from `origin/main` first and was MISSED there (7 of 7), then WORKS on the new code.
- [x] A1 (HIGH) Dry-run rule in CLAUDE.md (gate rules) and PROCESS.md §2 (stage 0), and a line in `sdlc-harness/SKILL.md`: on `dryrun/*` phases 1–6 run while Phase 0 is in progress; approvals `owner (DRY-RUN), <date>`; Phase 3 proposes a `.claude/` diff in docs/ and changes nothing live; the branch is never merged
- [x] A2 (HIGH) `memory_handoff.py`: a compaction with `agent_id` or a `subagents/` transcript is skipped and logged; every PostCompact writes its input key names to `.claude/logs/compactions.jsonl` (the next real compaction confirms which fields Claude Code sends). Drill: "subagent compaction … left as it is" + clean control "agent_type alone → handoff replaced"
- [x] A3 (MEDIUM) `memory_context.py`: `compact` → no handoff; `resume` → own handoff; `startup` → newest by time. The two old `compact` drill cases now use `resume` (same checks); new cases "compact: … no handoff" and "startup → the newest handoff by time"
- [x] A4 (MEDIUM) New shared helper `.claude/hooks/transcript_usage.py` (last `type == "message"` round) used by `context_monitor.py` and `agent_report.py`; output counted once per `message.id`. Drills: two 300k rounds → silent; a real 56% → "56%", not 112%; agent_report → "context now 300,000; output so far 200"
- [x] A5 (MEDIUM) `check_structure.py`: `memory/episodic/` and `memory/archive/` are stored data, not link-checked. Drill: a broken link in docs is reported, one inside archived memory is not
- [x] A6 (MEDIUM) `claude update` done (CLI 2.1.293, VS Code extension 2.1.294 — active after a VS Code reload). The new-session, `/status` and `/tasks` steps are now part of the dry-run rule (A1); CLAUDE.md Models: engine agents are spawned without a `model` parameter

## Parked (გადადებული)
- [x] **Security gap (found 2026-10-07, fixed 2026-10-08 with the owner's yes, branch `engine/commit-secrets-cwd`):** `commit_secrets.py` scanned the session's `cwd`, not the repository a command switches to — `cd <other repo> && git commit …`, `git -C <dir> commit …` and `bash -c 'git commit …'` (never seen at all) were not scanned. Now the target folder is resolved from `-C`/`cd`/`bash -c`; an unknowable folder (`$VAR`, `--git-dir`, `GIT_DIR=`) blocks. 14 new drill cases tied to the hook's own finding text, not to a marker a crash would also print; verified RED on the old hook (12 MISSED, 2 FALSE-BLOCK), GREEN after (158 cases ARMED, 5 repeated runs), stub and crash-mutant both DEAD, plus one live block through the real harness
- [ ] **Same blind spot in `guard.py`, owner's yes needed (measured 2026-10-08):** `push_problem` reads the branch of the session's `cwd`, so `git -C <repo on main> push origin HEAD` and `cd <repo on main> && git push origin HEAD` from a session on another branch exit 0 (controls: push on main in `cwd` → blocked, on a feature branch → allowed). `main` has no technical protection (GitHub Pro), so this guard is the only net. Fix: reuse the folder resolution of `commit_secrets.py` (`git_runs`) for `current_branch`, with the same drill style
- [ ] **Session-start handoff is cut (found 2026-10-08):** a compaction of session `df3e2417` replaced the short hand-written wrap handoff (archived as `…df3e2417.v1.md`, 5 469 chars) with a 26 037-char automatic one, while `memory_context.py` injects only `MAX_CHARS = 12000`. The next session therefore sees the stale head — and its last lines still say "start the dry run on `dryrun/expense-calculator`", which the owner cancelled. Same shape as the 2026-10-08 `v6` incident. Needs a fix in the hook (summarise or tail-cut, never head-cut a handoff) and a drill; the live handoff and `v1` are uncommitted and left as they are
- [ ] Non-blocking, `commit_secrets.py` (2026-10-08): `GIT_ENV` and `FANCY_SHELL` search the whole command text, so a commit message containing `GIT_DIR=` or `(` / `|` blocks or scans wider than needed (fails safe); `git -c core.worktree=… commit` is not treated as a redirect
- [ ] Context monitor reports "could not measure context use (no token usage found in the transcript tail)" on the very first command of a fresh session (observed 2026-10-08); reminders stay off until a usage line exists. Check whether a new session's first minutes are unprotected
- [ ] Flaky drill case (found 2026-10-07): `commit_secrets` "generic key only gitleaks knows" MISSED in 1 of 4 local runs, so CI can turn red at random. Likely cause UNVERIFIED: the random value can hit a gitleaks stopword or entropy limit. Fix: a deterministic high-entropy value assembled at run time, then 20 repeated runs
- [ ] Auditor LOW (ENG-v2-P1P2 review 1): requirements in `docs/changes/<n>/` are traced against the root `tasks/todo.md`, so a change's requirement can look traced by an unrelated product task with the same ID — use a change-local todo or prefixed IDs when the first change folder appears
- [ ] Auditor note (ENG-v2-P1P2 review 1): `review_rounds.py` checks SHA format only, not that the commits exist or that base is an ancestor of head — add a `git merge-base --is-ancestor` check if a wrong range is ever recorded
- [x] ~~Stage-2 orchestration (Fable 5.1; OpenAI `gpt-6.1-sol`, `gpt-6-astra` via Codex; an open-weight model)~~ — dropped: the owner decided Claude-only (2026-10-07) and chose ADR-0007 option A (2026-10-08)
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
