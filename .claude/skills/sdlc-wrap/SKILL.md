---
name: sdlc-wrap
description: End-of-session wrap-up — merge this session's handoffs into one session summary that follows the owner's principles, record lessons and changed decisions, refresh memory/now.md, and save a checkpoint. Use when the owner says goodbye, "დავასრულოთ", "wrap up", or before stopping a long piece of work.
---
# Session wrap

1. Gather the material: this session's handoff in `memory/episodic/handoffs/` and any `.claude/handoff-<today>.md` written by the global hook; `git log` since the session started; `docs/sdlc-state.md`.
2. Write `memory/episodic/sessions/<YYYY-MM-DD>-<slug>.md` from `sdlc/templates/session-summary.md`, following the owner's principles in `memory/README.md`. Merge, do not concatenate: one coherent story, superseded content dropped.
3. Changed minds: compare today's decisions and instructions with the accepted ADRs and `memory/now.md`. List every reversal under "Changed minds" with the old and the new position, and propose a superseding ADR — do not write it without the owner's yes.
4. Lessons: corrections the owner made today go into `tasks/lessons.md` (date · what went wrong · rule · check). If a lesson repeats an earlier one, propose promoting it into CLAUDE.md.
5. Refresh `memory/now.md` (at most 120 lines): current phase, active decisions, open loops, next step. Delete what is no longer true.
6. If a phase, gate or milestone finished this session, append a dated entry to `PROGRESS.md` and refresh its Current State, In Progress and Next Steps. Never rewrite old entries.
7. Move merged handoffs to `memory/archive/handoffs/` — never delete them.
8. Checkpoint commit: `chore(memory): wrap session <date>`.
9. Tell the owner in 3–4 Georgian sentences what we did, what comes next, and how to resume (`/sdlc-status`).
