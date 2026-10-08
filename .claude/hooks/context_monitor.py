#!/usr/bin/env python3
"""PostToolUse hook: ask for a handoff checkpoint BEFORE compaction (ADR-0006).

Context use = the token counts of the last assistant message in the session
transcript (input + cache read + cache creation), read through
transcript_usage.context_size so an advisor turn is not counted twice. The compaction point is read
from autoCompactWindow in .claude/settings.json, so a later ADR that moves it
cannot silently break this monitor. From MARGIN tokens before that point, Claude
is asked — once per STEP-token band — to write a checkpoint into this session's
single handoff file, the same file memory_handoff.py replaces at compaction.
If the use cannot be measured, Claude is told so once per session; the monitor
never blocks a tool. A subagent's tool call is skipped: it shares the parent's
session id (the live event log showed agent_type "auditor" with the parent's
session), so it would spend the main session's reminder band on an agent that
cannot write the checkpoint.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_handoff import session_key  # noqa: E402
from transcript_usage import context_size  # noqa: E402

MARKER = "ASTERBIT-CONTEXT-MONITOR"
WINDOW = 1_000_000          # Sonnet 5.5 / Opus 5.5 context window, used only for the percentage shown
MARGIN = 100_000            # 10 points of the window before compaction
STEP = 50_000               # one reminder per 5-point band
TAIL_BYTES = 4_000_000      # one transcript record can exceed 1 MB


def compaction_point(project: Path) -> int:
    settings = json.loads((project / ".claude/settings.json").read_text(encoding="utf-8"))
    return int(settings["autoCompactWindow"])


def context_tokens(transcript: Path) -> int:
    with transcript.open("rb") as handle:
        handle.seek(max(0, transcript.stat().st_size - TAIL_BYTES))
        lines = handle.read().decode("utf-8", errors="ignore").splitlines()
    for line in reversed(lines):
        try:
            usage = (json.loads(line).get("message") or {}).get("usage")
        except (json.JSONDecodeError, AttributeError):
            continue
        if isinstance(usage, dict) and usage:
            return context_size(usage)
    raise ValueError("no token usage found in the transcript tail")


def handoff_path(project: Path, key: str) -> str:
    existing = sorted((project / "memory/episodic/handoffs").glob(f"*-{key}.md"))
    target = existing[-1] if existing else project / f"memory/episodic/handoffs/{dt.date.today():%Y-%m-%d}-{key}.md"
    return target.relative_to(project).as_posix()


def decide(project: Path, event: dict, state: dict) -> str:
    """Return the reminder text, or "" when nothing is due. Updates state in place."""
    try:
        point = compaction_point(project)
        used = context_tokens(Path(event.get("transcript_path", "")))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        if state.get("unmeasured"):
            return ""
        state["unmeasured"] = True
        return f"{MARKER}: could not measure context use ({type(error).__name__}: {error}). Checkpoint reminders are off until it can be measured again — write the handoff by hand before a long step."
    if used < point - MARGIN:
        state["band"] = -1          # below the threshold again, e.g. after a compaction
        return ""
    band = (used - (point - MARGIN)) // STEP
    if band <= state.get("band", -1):
        return ""
    state["band"] = band
    path = handoff_path(project, session_key(event.get("session_id", "")))
    return (f"{MARKER}: context ≈ {used * 100 // WINDOW}% ({used:,} tokens); compaction at {point * 100 // WINDOW}% ({point:,}). "
            f"At the next natural pause write a checkpoint into this session's handoff `{path}` (one file per session; create it if missing), "
            "following the owner's principles in memory/README.md: where we are, what is done, the exact next step, decisions with reasons, verbatim facts.")


def main() -> int:
    event = json.load(sys.stdin)
    if event.get("agent_id") or event.get("agent_type"):
        return 0                    # a subagent's call: the reminder belongs to the main session
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())
    state_file = project / f".claude/logs/context-monitor-{session_key(event.get('session_id', ''))}.json"
    state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
    message = decide(project, event, state)
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state), encoding="utf-8")
    if message:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # never block a tool; say that the monitor itself failed
        print(f"{MARKER}: monitor failed ({type(error).__name__}: {error}).", file=sys.stderr)
        sys.exit(1)
