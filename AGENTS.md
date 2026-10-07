# AGENTS.md — rules for every AI coding agent in this repo

This file is for agents that do not read `CLAUDE.md`: Codex / GPT, Cursor, Kilo, Gemini CLI and the like. Claude Code reads `CLAUDE.md` instead.

The full working rules are in [CLAUDE.md](CLAUDE.md) (English) and [PROCESS.md](PROCESS.md) (Georgian, the owner's version). Read `CLAUDE.md` before you change anything. If this file and `CLAUDE.md` ever disagree, `CLAUDE.md` wins — report the mismatch to the owner.

## People
- The owner (GitHub: tornikebolokadze1-cyber) writes Georgian and does not read code. Answer in Georgian prose, keep technical terms but explain each one the first time, and say what and why before how.
- Collaborators are listed in [CONTRIBUTING.md](CONTRIBUTING.md). Answer every person in the language they write in.
- Only the owner approves gates and merges into `main`. Never approve your own work or record an approval on someone else's behalf.

## Safety — copied from CLAUDE.md, always in force
The guards in `.claude/hooks/` run only inside Claude Code, so for you these rules hold on your word; CI (structure check, hook drills, gitleaks) still runs on every pull request.
- Work on a branch and push working branches freely; never push to `main` — `main` changes only through a pull request that the owner approves and merges.
- Ask the person you work with before you install anything or fetch from the internet. Changes to permissions, hooks, settings or CI affect everyone, so they need the owner's yes.
- Never force-push, rewrite pushed history, or run `rm -rf`, `git reset --hard` or `git clean -f`.
- Delete a file only after the person you work with agrees; a deletion reaches `main` only through a pull request the owner approves.
- Secrets never enter git: `.env*` is ignored. The names of the settings the project needs (no values) go in [env.example](env.example) — no leading dot, so the deny rule on `.env.*` keeps guarding real secret files.
- Stage explicit paths (never `git add -A`) and commit in a separate command.

## Before you open a pull request
- Adding, moving or renaming a file: update [docs/FILES.md](docs/FILES.md) in the same change.
- Run `python3 sdlc/checks/check_structure.py` — it must say PASS.
- After changing anything in `.claude/hooks/`: `python3 sdlc/checks/drill_hooks.py` must say ARMED, and the same with `ASTERBIT_DRILL_STUB=1` must say DEAD.
- "Done" means the check ran and you show its output; "could not run" is not a pass.

## Where things are
- [docs/FILES.md](docs/FILES.md) — what every file does.
- [docs/sdlc-state.md](docs/sdlc-state.md) — the current phase; no phase starts before the previous one is approved, and no product code is written before `docs/plan.md` is approved.
- [PROGRESS.md](PROGRESS.md) and [memory/now.md](memory/now.md) — where the work stands.
