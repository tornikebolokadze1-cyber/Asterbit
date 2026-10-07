#!/usr/bin/env python3
"""Review-loop ledger for the build loop (ADR-0006).

The loop, per milestone and per [high-risk] task:
    review 1 → fix 1 → review 2 → fix 2 → review 3 (final) → the owner.
Rounds are counted from an append-only ledger, never from the model's memory.
LOW findings are logged but never keep the loop open. If HIGH+MEDIUM do not
fall between two reviews, the loop stops early and goes to the owner.

Usage:
    review_rounds.py review <loop> --base SHA --head SHA --high N --medium N --low N
    review_rounds.py fix <loop> --head SHA
    review_rounds.py status <loop>
Options: --ledger PATH (default: tasks/review-log.jsonl in this repo).

Exit codes. status: 0 = closed clean, 1 = escalate to the owner, 2 = inconclusive
(ledger unreadable), 3 = continue (the next step is printed).
review / fix: 0 = recorded, 1 = step not allowed now (nothing written), 2 = inconclusive.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MAX_FIXES = 2
DEFAULT_LEDGER = Path(__file__).resolve().parents[2] / "tasks/review-log.jsonl"
LOOP_ID = re.compile(r"^[A-Za-z0-9._-]{1,40}$")
SHA = re.compile(r"^[0-9a-f]{7,40}$")


def load(ledger: Path, loop: str) -> list[dict]:
    if not ledger.exists():
        return []
    entries = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [e for e in entries if e.get("loop") == loop]


def blocking(entry: dict) -> int:
    return int(entry["high"]) + int(entry["medium"])


def next_step(entries: list[dict]) -> tuple[str, int]:
    reviews = [e for e in entries if e["step"] == "review"]
    fixes = [e for e in entries if e["step"] == "fix"]
    if not entries or entries[-1]["step"] == "fix":
        number = len(reviews) + 1
        return f"review {number}" + (" (final)" if number == MAX_FIXES + 1 else ""), 3
    if blocking(reviews[-1]) == 0:
        return "done: no HIGH or MEDIUM finding left", 0
    if len(reviews) >= 2 and blocking(reviews[-1]) >= blocking(reviews[-2]):
        return "escalate to the owner: HIGH+MEDIUM did not fall between reviews", 1
    if len(fixes) >= MAX_FIXES:
        return "escalate to the owner: findings remain after the final review", 1
    return f"fix {len(fixes) + 1}", 3


def record(args: argparse.Namespace, entries: list[dict]) -> int:
    expected, _ = next_step(entries)
    if not expected.startswith(args.command):
        print(f"REVIEW-LOOP: '{args.command}' is not allowed now for {args.loop} — next step is: {expected}")
        return 1
    if not SHA.match(args.head) or (args.command == "review" and not SHA.match(args.base)):
        print("REVIEW-LOOP: --base/--head must be git commit SHAs (7–40 hex characters)")
        return 1
    if args.command == "review" and args.base == args.head:
        print("REVIEW-LOOP: empty diff range (base == head) — record BASE before the work, then review base..head")
        return 1
    entry = {"ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "loop": args.loop,
             "step": args.command, "round": sum(e["step"] == args.command for e in entries) + 1, "head": args.head}
    if args.command == "review":
        entry.update(base=args.base, high=args.high, medium=args.medium, low=args.low)
    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    with args.ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
    print(f"REVIEW-LOOP: recorded {args.command} {entry['round']} for {args.loop}; next: {next_step(entries + [entry])[0]}")
    return 0


def parse(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review-loop ledger (ADR-0006)")
    parser.add_argument("command", choices=("review", "fix", "status"))
    parser.add_argument("loop", help="milestone or task id, e.g. M1 or M1-T4")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--base", default="")
    parser.add_argument("--head", default="")
    for level in ("high", "medium", "low"):
        parser.add_argument(f"--{level}", type=int, default=None)
    args = parser.parse_args(argv)
    if not LOOP_ID.match(args.loop):
        parser.error("loop id: 1–40 characters from A-Z a-z 0-9 . _ -")
    if args.command == "review" and None in (args.high, args.medium, args.low):
        parser.error("review needs --high, --medium and --low (counts from the auditor's report)")
    return args


def main(argv: list[str]) -> int:
    args = parse(argv)
    try:
        entries = load(args.ledger, args.loop)
        if args.command != "status":
            return record(args, entries)
        step, code = next_step(entries)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"REVIEW-LOOP: INCONCLUSIVE — ledger {args.ledger} unreadable ({type(error).__name__}: {error})")
        return 2
    print(f"REVIEW-LOOP: {args.loop} — {len(entries)} entries in {args.ledger.name}; next: {step}")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
