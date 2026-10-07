#!/usr/bin/env python3
"""PostCompact hook: save the compaction summary as this session's rolling handoff.

One session = one handoff file in memory/episodic/handoffs/<date>-<session>.md.
A newer compaction replaces it; the previous version moves to
memory/archive/handoffs/ (never deleted). Known secret patterns are redacted
before anything is written. Missing input is reported, never written as a
silent empty handoff.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from secret_patterns import count_secret_like, redact  # noqa: E402

MARKER = "ASTERBIT-MEMORY"


def session_key(session_id: str) -> str:
    key = re.sub(r"[^A-Za-z0-9]", "", session_id)[:8]
    return key or "unknown"


def archive_previous(current: Path, archive_dir: Path) -> int:
    """Move the existing handoff to the archive; return how many versions exist now."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    versions = len(list(archive_dir.glob(f"{current.stem}.v*.md")))
    current.rename(archive_dir / f"{current.stem}.v{versions + 1}.md")
    return versions + 1


def main() -> int:
    event = json.load(sys.stdin)
    summary = (event.get("compact_summary") or "").strip()
    if not summary:
        print(f"{MARKER}: no compact_summary in the PostCompact input — handoff NOT saved.", file=sys.stderr)
        return 1
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())
    handoffs = project / "memory/episodic/handoffs"
    handoffs.mkdir(parents=True, exist_ok=True)
    key = session_key(event.get("session_id", ""))
    existing = sorted(handoffs.glob(f"*-{key}.md"))
    previous_versions = archive_previous(existing[-1], project / "memory/archive/handoffs") if existing else 0
    now = dt.datetime.now(dt.timezone.utc)
    target = existing[-1] if existing else handoffs / f"{now:%Y-%m-%d}-{key}.md"
    redactions = count_secret_like(summary)
    target.write_text(
        "---\n"
        f"session: {key}\nupdated: {now:%Y-%m-%dT%H:%M:%SZ}\ntrigger: {event.get('trigger', 'unknown')}\n"
        f"compaction: {previous_versions + 1}\n---\n\n"
        f"# Handoff — {now:%Y-%m-%d} · session {key}\n\n{redact(summary)}\n",
        encoding="utf-8",
    )
    note = f" ({redactions} secret-looking value(s) redacted)" if redactions else ""
    message = f"{MARKER}: handoff saved to {target.relative_to(project)} (compaction {previous_versions + 1}){note}."
    print(json.dumps({"systemMessage": message}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"{MARKER}: handoff NOT saved ({type(error).__name__}: {error}).", file=sys.stderr)
        sys.exit(1)
