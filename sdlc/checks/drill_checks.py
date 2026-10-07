#!/usr/bin/env python3
"""Drills for the engine's check scripts (not hooks): clean controls pass, seeded defects are caught.

Imported by drill_hooks.py, which owns the Drill harness, the report and the exit code
(ADR-0006). Every verdict is tied to the checked script's own exit code and output marker.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKS = ROOT / "sdlc/checks"
SHA = ("a1b2c3d", "b2c3d4e", "c3d4e5f", "d4e5f60")


def rounds(ledger: Path, *args: str) -> subprocess.CompletedProcess:
    command = [sys.executable, str(CHECKS / "review_rounds.py"), *args, "--ledger", str(ledger)]
    return subprocess.run(command, capture_output=True, text=True, timeout=30)


def play(ledger: Path, loop: str, steps: list[tuple]) -> list[int]:
    """Steps: ("review", base, head, high, medium[, low]) or ("fix", head). Returns the exit codes."""
    codes = []
    for step in steps:
        if step[0] == "review":
            low = str(step[5]) if len(step) > 5 else "0"
            args = ["review", loop, "--base", step[1], "--head", step[2], "--high", str(step[3]), "--medium", str(step[4]), "--low", low]
        else:
            args = ["fix", loop, "--head", step[1]]
        codes.append(rounds(ledger, *args).returncode)
    return codes


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0


def drill_review_rounds(drill, scratch: Path) -> None:
    gate, ledger = "review_rounds", scratch / "review-log.jsonl"
    a, b, c, d = SHA
    clean = play(ledger, "M1", [("review", a, b, 1, 2), ("fix", c), ("review", b, c, 0, 0, 3)])
    status = rounds(ledger, "status", "M1")
    drill.expect_bool(gate, "clean control: review → fix → review with only LOW → done (exit 0)",
                      clean == [0, 0, 0] and status.returncode == 0 and "done" in status.stdout)
    before = line_count(ledger)
    early = rounds(ledger, "fix", "M2", "--head", a)
    drill.expect_bool(gate, "fix before any review → refused, nothing written",
                      early.returncode == 1 and "not allowed" in early.stdout and line_count(ledger) == before)
    empty = rounds(ledger, "review", "M3", "--base", a, "--head", a, "--high", "1", "--medium", "0", "--low", "0")
    drill.expect_bool(gate, "review with base == head → refused", empty.returncode == 1 and "empty diff range" in empty.stdout)
    full = play(ledger, "M4", [("review", a, b, 3, 2), ("fix", c), ("review", b, c, 2, 1), ("fix", d), ("review", c, d, 1, 0)])
    third = rounds(ledger, "fix", "M4", "--head", a)
    final = rounds(ledger, "status", "M4")
    drill.expect_bool(gate, "findings after the final review → 3rd fix refused, status escalates (exit 1)",
                      full == [0] * 5 and third.returncode == 1 and final.returncode == 1 and "final review" in final.stdout)
    play(ledger, "M5", [("review", a, b, 0, 2), ("fix", c), ("review", b, c, 1, 1)])
    stuck = rounds(ledger, "status", "M5")
    drill.expect_bool(gate, "HIGH+MEDIUM did not fall → escalates early (exit 1)",
                      stuck.returncode == 1 and "did not fall" in stuck.stdout)
    broken = scratch / "broken-log.jsonl"
    broken.write_text("not json\n", encoding="utf-8")
    unreadable = rounds(broken, "status", "M1")
    drill.expect_bool(gate, "unreadable ledger → INCONCLUSIVE (exit 2), never a pass",
                      unreadable.returncode == 2 and "INCONCLUSIVE" in unreadable.stdout)


PRD = "---\ntitle: drill\nstatus: approved\n---\n# PRD\n| ID | Feature | Journeys | Priority | Why |\n|---|---|---|---|---|\n" \
      "| P-1 | add an expense | J-1 | must | core |\n| P-2 | export | J-1 | could | later |\n"
SPEC = "---\ntitle: drill\nstatus: approved\n---\n# Spec\n- FR-1 — add an expense. Source: P-1\n- NFR-1 — fast. Source: TR-1\n"
PLAN = "---\ntitle: drill\nstatus: approved\n---\n# Plan\nM1 covers FR-1 and NFR-1.\n"


def drill_artifact_checks(drill, scratch: Path) -> None:
    gate, copy = "check_structure", scratch / "artifacts"
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".kilo", "__pycache__", "node_modules", ".omc"))
    for name, text in (("prd", PRD), ("spec", SPEC), ("plan", PLAN)):
        (copy / f"docs/{name}.md").write_text(text, encoding="utf-8")
    with (copy / "docs/FILES.md").open("a", encoding="utf-8") as handle:
        handle.write("\n- [prd](prd.md) · [spec](spec.md) · [plan](plan.md)\n")
    check = [sys.executable, str(copy / "sdlc/checks/check_structure.py"), str(copy)]
    clean = subprocess.run(check, capture_output=True, text=True, timeout=120)
    drill.expect_bool(gate, "clean control: approved PRD → spec → plan, fully traced", clean.returncode == 0 and "PASS" in clean.stdout)
    (copy / "docs/prd.md").write_text(PRD + "| P-3 | monthly budget | J-1 | must | core |\n\nCurrency: [NEEDS CLARIFICATION: which?]\n", encoding="utf-8")
    (copy / "docs/spec.md").write_text(SPEC + "- FR-2 — export to CSV. Source: P-2\n", encoding="utf-8")
    seeded = subprocess.run(check, capture_output=True, text=True, timeout=120)
    expected = ("docs/prd.md: approved but still has [NEEDS CLARIFICATION]", "must-priority feature P-3 reaches no spec.md",
                "requirement FR-2 reaches no plan.md / todo.md")
    drill.expect_bool(gate, "approved artifacts: open marker, untraced must-feature, untraced requirement all reported",
                      seeded.returncode == 1 and all(e in seeded.stdout for e in expected))


def drill_engine_checks(drill, scratch: Path) -> None:
    drill_review_rounds(drill, scratch)
    drill_artifact_checks(drill, scratch)
