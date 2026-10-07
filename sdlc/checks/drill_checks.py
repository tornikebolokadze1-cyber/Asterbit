#!/usr/bin/env python3
"""Drills for the engine's check scripts (not hooks): clean controls pass, seeded defects are caught.

Imported by drill_hooks.py, which owns the Drill harness, the report and the exit code
(ADR-0006). Every verdict is tied to the checked script's own exit code and output marker.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKS = ROOT / "sdlc/checks"
SHA = ("a1b2c3d", "b2c3d4e", "c3d4e5f", "d4e5f60")


def tracked_copy(dst: Path) -> Path:
    """A hermetic copy: only files git tracks (with their working-tree content) plus .git.

    Untracked work in progress or a local .env never leaks into a drill.
    """
    files = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--cached"], capture_output=True, text=True, check=True).stdout
    for rel in files.splitlines():
        if (ROOT / rel).is_file():
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst / rel)
    shutil.copytree(ROOT / ".git", dst / ".git")
    return dst


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
    before = line_count(ledger)
    third = rounds(ledger, "fix", "M4", "--head", a)
    final = rounds(ledger, "status", "M4")
    drill.expect_bool(gate, "findings after the final review → 3rd fix refused, nothing written, status escalates (exit 1)",
                      full == [0] * 5 and third.returncode == 1 and "not allowed" in third.stdout and line_count(ledger) == before
                      and final.returncode == 1 and "final review" in final.stdout)
    play(ledger, "M6", [("review", a, b, 1, 0), ("fix", c)])
    before = line_count(ledger)
    shifted = rounds(ledger, "review", "M6", "--base", a, "--head", c, "--high", "0", "--medium", "0", "--low", "0")
    drill.expect_bool(gate, "review 2 not covering exactly the fix (base ≠ previous head) → refused, nothing written",
                      shifted.returncode == 1 and "must cover exactly the fix" in shifted.stdout and line_count(ledger) == before)
    play(ledger, "M7", [("review", a, b, 1, 0)])
    no_commit = rounds(ledger, "fix", "M7", "--head", b)
    drill.expect_bool(gate, "fix with no new commit → refused", no_commit.returncode == 1 and "no new commit" in no_commit.stdout)
    negative = rounds(ledger, "review", "M8", "--base", a, "--head", b, "--high", "1", "--medium", "-1", "--low", "0")
    drill.expect_bool(gate, "negative finding count → rejected, nothing written",
                      negative.returncode == 2 and "0 or more" in negative.stderr and "M8" not in ledger.read_text(encoding="utf-8"))
    play(ledger, "M5", [("review", a, b, 0, 2), ("fix", c), ("review", b, c, 1, 1)])
    stuck = rounds(ledger, "status", "M5")
    drill.expect_bool(gate, "HIGH+MEDIUM did not fall → escalates early (exit 1)",
                      stuck.returncode == 1 and "did not fall" in stuck.stdout)
    bad_lines = {"not json": "not json", "a list": "[]", "an unknown step": json.dumps({"loop": "M1", "step": "Review"}),
                 "a negative count": json.dumps({"loop": "M1", "step": "review", "high": 1, "medium": -1, "low": 0})}
    for label, line in bad_lines.items():
        broken = scratch / "broken-log.jsonl"
        broken.write_text(line + "\n", encoding="utf-8")
        unreadable = rounds(broken, "status", "M1")
        drill.expect_bool(gate, f"ledger line with {label} → INCONCLUSIVE (exit 2), never escalate or pass",
                          unreadable.returncode == 2 and "INCONCLUSIVE" in unreadable.stdout)


PRD = "---\ntitle: drill\nstatus: approved\n---\n# PRD\n| ID | Feature | Journeys | Priority | Why |\n|---|---|---|---|---|\n" \
      "| P-1 | add an expense | J-1 | must | core |\n| P-2 | export | J-1 | could | later |\n"
SPEC = "---\ntitle: drill\nstatus: approved\n---\n# Spec\n- FR-1 — add an expense. Source: P-1\n- NFR-1 — fast. Source: TR-1\n"
PLAN = "---\ntitle: drill\nstatus: approved\n---\n# Plan\nM1 covers FR-1 and NFR-1.\n"
TODO = "# Tasks\n- [ ] T1 — drill task · proof: `true` → exit 0\n"  # the copy's own todo: the live one may mention any ID


def approved_from_template(name: str, fill: tuple[str, str] = ("", "")) -> str:
    text = (ROOT / f"sdlc/templates/{name}.md").read_text(encoding="utf-8").replace("status: draft", "status: approved", 1)
    return text.replace(*fill, 1) if fill[0] else text


def drill_artifact_checks(drill, scratch: Path) -> None:
    gate = "check_structure"
    real = tracked_copy(scratch / "templates")
    docs = {"prd": approved_from_template("prd"), "trd": approved_from_template("trd"),
            "spec": approved_from_template("spec", ("Source: P-n / J-n", "Source: P-1")),
            "plan": approved_from_template("plan") + "\nM1 covers FR-1 and NFR-1.\n"}
    for name, text in docs.items():
        (real / f"docs/{name}.md").write_text(text, encoding="utf-8")
    (real / "tasks/todo.md").write_text(TODO, encoding="utf-8")
    with (real / "docs/FILES.md").open("a", encoding="utf-8") as handle:
        handle.write("\n- [prd](prd.md) · [trd](trd.md) · [spec](spec.md) · [plan](plan.md)\n")
    from_templates = subprocess.run([sys.executable, str(real / "sdlc/checks/check_structure.py"), str(real)],
                                    capture_output=True, text=True, timeout=120)
    drill.expect_clean(gate, "clean control: approved PRD/TRD/spec/plan built from the real templates",
                       from_templates.returncode == 0 and "PASS" in from_templates.stdout)
    copy = tracked_copy(scratch / "artifacts")
    for name, text in (("prd", PRD), ("spec", SPEC), ("plan", PLAN)):
        (copy / f"docs/{name}.md").write_text(text, encoding="utf-8")
    (copy / "tasks/todo.md").write_text(TODO, encoding="utf-8")
    with (copy / "docs/FILES.md").open("a", encoding="utf-8") as handle:
        handle.write("\n- [prd](prd.md) · [spec](spec.md) · [plan](plan.md)\n")
    check = [sys.executable, str(copy / "sdlc/checks/check_structure.py"), str(copy)]
    clean = subprocess.run(check, capture_output=True, text=True, timeout=120)
    drill.expect_clean(gate, "clean control: approved PRD → spec → plan, fully traced", clean.returncode == 0 and "PASS" in clean.stdout)
    (copy / "docs/prd.md").write_text(PRD + "| P-3 | monthly budget | J-1 | must | core |\n\nCurrency: [NEEDS CLARIFICATION: which?]\n", encoding="utf-8")
    (copy / "docs/spec.md").write_text(SPEC + "- FR-2 — export to CSV. Source: P-2\n", encoding="utf-8")
    seeded = subprocess.run(check, capture_output=True, text=True, timeout=120)
    expected = ("docs/prd.md: approved but still has [NEEDS CLARIFICATION]", "must-priority feature P-3 reaches no requirement line",
                "requirement FR-2 reaches no plan.md / todo.md")
    drill.expect_bool(gate, "approved artifacts: open marker, untraced must-feature, untraced requirement all reported",
                      seeded.returncode == 1 and all(e in seeded.stdout for e in expected))
    (copy / "docs/spec.md").write_text("---\ntitle: drill\nstatus: Approved  # x\n---\n# Spec\nRequirements are in a table elsewhere.\n", encoding="utf-8")
    (copy / "docs/plan.md").write_text("---\ntitle: drill\nstatus: final\n---\n# Plan\n", encoding="utf-8")
    empty = subprocess.run(check, capture_output=True, text=True, timeout=120)
    drill.expect_bool(gate, "approved spec with no requirement, and an unknown status, are reported — never a silent pass",
                      empty.returncode == 1 and "no FR-n/NFR-n requirement found" in empty.stdout and "unknown status 'final'" in empty.stdout)
    (copy / "docs/prd.md").write_text(PRD + "\n> [!question] Currency [NEEDS CLARIFICATION: GEL or USD?]\n", encoding="utf-8")
    callout = subprocess.run(check, capture_output=True, text=True, timeout=120)
    drill.expect_bool(gate, "open question hidden in an Obsidian callout of an approved PRD → reported",
                      callout.returncode == 1 and "docs/prd.md: approved but still has [NEEDS CLARIFICATION]" in callout.stdout)


def drill_engine_checks(drill, scratch: Path) -> None:
    drill_review_rounds(drill, scratch)
    drill_artifact_checks(drill, scratch)
