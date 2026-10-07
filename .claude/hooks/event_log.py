#!/usr/bin/env python3
"""PostToolUse / PostToolUseFailure hook: one line per tool call in the agent's event log (ADR-0006, P5).

Writes .claude/logs/events-<date>.jsonl (not in git). Each line: time, session,
event, agent, tool, a short summary of the input (command, file path, pattern…)
and the outcome. Tool input is untrusted data: secrets are redacted, invisible
characters stripped and the summary cut to 200 characters. The hook never
blocks a tool; if it cannot write, it says so on stderr.
Known limit: calls the guard blocks never reach PostToolUse, so they are not here.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_handoff import session_key  # noqa: E402
from secret_patterns import redact  # noqa: E402
from untrusted import strip_invisible  # noqa: E402

MARKER = "ASTERBIT-EVENT-LOG"
MAX_SUMMARY = 200
SUMMARY_FIELDS = ("command", "file_path", "notebook_path", "pattern", "url", "query", "subagent_type", "description")


def summarise(tool_input: object) -> str:
    if not isinstance(tool_input, dict):
        return ""
    value = next((str(tool_input[k]) for k in SUMMARY_FIELDS if tool_input.get(k)), "")
    return strip_invisible(redact(value)).replace("\n", " ")[:MAX_SUMMARY]


def main() -> int:
    event = json.load(sys.stdin)
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())
    now = dt.datetime.now(dt.timezone.utc)
    name = event.get("hook_event_name", "PostToolUse")
    record = {
        "ts": f"{now:%Y-%m-%dT%H:%M:%SZ}",
        "session": session_key(event.get("session_id", "")),
        "event": "tool_call",
        "agent": event.get("agent_type") or "main",
        "tool": event.get("tool_name", ""),
        "summary": summarise(event.get("tool_input")),
        "outcome": "failed" if name == "PostToolUseFailure" else "ok",
    }
    log = project / f".claude/logs/events-{now:%Y-%m-%d}.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # never block a tool; a missing log line must still be visible
        print(f"{MARKER}: event NOT logged ({type(error).__name__}: {error}).", file=sys.stderr)
        sys.exit(1)
