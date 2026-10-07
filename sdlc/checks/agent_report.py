#!/usr/bin/env python3
"""Agent report: what the agent did, what failed, what it cost (ADR-0006, P5).

Reads the event log that .claude/hooks/event_log.py writes (.claude/logs/events-*.jsonl)
and, optionally, a session transcript for token counts.

    python3 sdlc/checks/agent_report.py [--date YYYY-MM-DD] [--session KEY] [--transcript PATH]

Exit codes: 0 = report printed · 2 = inconclusive (no events found — an empty log is
not evidence that nothing happened).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_events(logs: Path, date: str | None, session: str | None) -> list[dict]:
    events = []
    for path in sorted(logs.glob(f"events-{date or '*'}.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                if not session or record.get("session") == session:
                    events.append(record)
    return events


def token_totals(transcript: Path) -> tuple[int, int]:
    """(last context size, total output tokens) from a transcript's usage fields."""
    last, output = 0, 0
    for line in transcript.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            usage = (json.loads(line).get("message") or {}).get("usage")
        except (json.JSONDecodeError, AttributeError):
            continue
        if usage:
            last = sum(int(usage.get(k) or 0) for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
            output += int(usage.get("output_tokens") or 0)
    return last, output


def report(events: list[dict]) -> None:
    by_tool = collections.Counter(e.get("tool", "?") for e in events)
    by_agent = collections.Counter(e.get("agent", "?") for e in events)
    failed = [e for e in events if e.get("outcome") == "failed"]
    touched = sorted({e["summary"] for e in events if e.get("tool") in ("Edit", "Write", "MultiEdit", "NotebookEdit")
                      and e.get("outcome") == "ok" and e.get("summary")})
    print(f"AGENT-REPORT: {len(events)} tool calls in {len({e.get('session') for e in events})} session(s), {len(failed)} failed")
    print("  by tool:  " + ", ".join(f"{tool} {n}" for tool, n in by_tool.most_common()))
    print("  by agent: " + ", ".join(f"{agent} {n}" for agent, n in by_agent.most_common()))
    for event in failed[:10]:
        print(f"  failed: {event.get('ts')} {event.get('tool')} — {event.get('summary')}")
    print(f"  files changed ({len(touched)}): " + ", ".join(touched[:15]) + (" …" if len(touched) > 15 else ""))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Summarise the agent event log")
    parser.add_argument("--logs", type=Path, default=ROOT / ".claude/logs")
    parser.add_argument("--date")
    parser.add_argument("--session")
    parser.add_argument("--transcript", type=Path)
    args = parser.parse_args(argv)
    try:
        events = load_events(args.logs, args.date, args.session)
        tokens = token_totals(args.transcript) if args.transcript else None
    except (OSError, ValueError) as error:
        print(f"AGENT-REPORT: INCONCLUSIVE — {type(error).__name__}: {error}")
        return 2
    if not events:
        print(f"AGENT-REPORT: INCONCLUSIVE — no events in {args.logs} for the given filter")
        return 2
    report(events)
    if tokens:
        print(f"  tokens: context now {tokens[0]:,}; output so far {tokens[1]:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
