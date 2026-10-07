#!/usr/bin/env python3
"""Structure check for the Asterbit engine.

Exit codes: 0 = every check passed, 1 = at least one defect, 2 = inconclusive
(a check could not run, so nothing was proved). Usage:

    python3 sdlc/checks/check_structure.py [repo-root]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REQUIRED_FILES = (
    "README.md", "CLAUDE.md", "PROCESS.md", "PROGRESS.md", "CONTRIBUTING.md",
    ".gitignore", ".claude/settings.json", "docs/FILES.md", "docs/sdlc-state.md",
    "docs/decisions/README.md", "tasks/todo.md", "tasks/lessons.md",
    "memory/README.md", "memory/now.md",
)
EXPECTED_SKILLS = 11
EXPECTED_AGENTS = 3
AGENT_MODELS = {"claude-opus-5-5", "claude-sonnet-5-5"}
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
NAMED_PATH = re.compile(
    r"(sdlc/(?:templates|design|checks)/[\w.-]+\.(?:md|py)|docs/sdlc-state\.md|"
    r"docs/decisions/README\.md|memory/(?:README|now)\.md|tasks/(?:todo|lessons)\.md)"
)
LINK = re.compile(r"\]\(([^)\s]+)\)")
CLARIFY = "[NEEDS CLARIFICATION"
CLARIFY_PLACEHOLDER = "[NEEDS CLARIFICATION: <question>]"  # exempt only on template guidance lines (">")
DONE_STATUSES = {"approved", "accepted"}
KNOWN_STATUSES = DONE_STATUSES | {"draft", "rejected"}
ARTIFACTS = ("intent", "prd", "trd", "spec", "plan")
# Tolerant of bold, indentation, numbered lists and table cells. If NO row/requirement matches, the check fails
# loudly below; a single row in an unusual format (e.g. "must (MVP)", "### FR-2") can still be missed.
FEATURE_ROW = re.compile(r"^\s*\|\s*\**(P-\d+)\b", re.M)
MUST_FEATURE = re.compile(r"^\s*\|\s*\**(P-\d+)\**\s*\|.*\|\s*\**must(?:[- ]have)?\**\s*\|", re.M | re.I)
REQUIREMENT = re.compile(r"^\s*(?:[-*+]|\d+[.)]|\|)\s*\**(N?FR-\d+)\b", re.M)


class Report:
    def __init__(self) -> None:
        self.checks = 0
        self.defects: list[str] = []
        self.inconclusive: list[str] = []

    def check(self, ok: bool, message: str) -> None:
        self.checks += 1
        if not ok:
            self.defects.append(message)


def front_matter(path: Path | str) -> dict[str, str] | None:
    """Fields between the opening --- lines; accepts a file path or the text itself."""
    text = path if isinstance(path, str) else path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        kv = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if kv:
            fields[kv.group(1)] = kv.group(2).split("  #")[0].strip()
    return fields


def repo_files(root: Path, report: Report) -> list[str] | None:
    """Tracked plus new, non-ignored files — the same set git would publish."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        report.inconclusive.append(f"git ls-files failed ({error}); file-map and link checks skipped")
        return None
    return sorted(p for p in out.splitlines() if p and (root / p).exists())


def check_skills_and_agents(root: Path, report: Report) -> list[Path]:
    skills = sorted((root / ".claude/skills").glob("*/SKILL.md"))
    report.check(len(skills) == EXPECTED_SKILLS, f"expected {EXPECTED_SKILLS} skills, found {len(skills)}")
    for skill in skills:
        fields = front_matter(skill)
        rel = skill.relative_to(root)
        report.check(fields is not None, f"{rel}: no front matter")
        if fields:
            report.check(fields.get("name") == skill.parent.name, f"{rel}: name != folder name")
            report.check(20 < len(fields.get("description", "")) <= 1536, f"{rel}: description length")
    agents = sorted((root / ".claude/agents").glob("*.md"))
    report.check(len(agents) == EXPECTED_AGENTS, f"expected {EXPECTED_AGENTS} agents, found {len(agents)}")
    for agent in agents:
        fields = front_matter(agent) or {}
        rel = agent.relative_to(root)
        for key in ("name", "description", "tools", "model", "effort"):
            report.check(bool(fields.get(key)), f"{rel}: missing '{key}'")
        report.check(fields.get("model") in AGENT_MODELS, f"{rel}: unexpected model {fields.get('model')}")
        report.check(fields.get("effort") in EFFORTS, f"{rel}: bad effort {fields.get('effort')}")
    return skills


def check_links_and_file_map(root: Path, files: list[str], report: Report) -> None:
    for rel in (f for f in files if f.endswith(".md")):
        page = root / rel
        for target in LINK.findall(page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            report.check((page.parent / target.split("#")[0]).resolve().exists(), f"{rel}: broken link -> {target}")
    file_map = root / "docs/FILES.md"
    if not file_map.exists():
        return
    linked, folders = set(), []
    for target in LINK.findall(file_map.read_text(encoding="utf-8")):
        if not target.startswith(("http", "#", "mailto:")):
            resolved = (file_map.parent / target.split("#")[0]).resolve()
            if resolved.is_relative_to(root):
                rel_target = resolved.relative_to(root).as_posix()
                # a link to a folder (memory/episodic/handoffs/) covers the files that accumulate in it
                (folders.append(rel_target + "/") if resolved.is_dir() else linked.add(rel_target))
    for rel in files:
        report.check(rel in linked or any(rel.startswith(folder) for folder in folders),
                     f"docs/FILES.md does not list {rel}")


def check_settings(root: Path, report: Report) -> None:
    settings_path = root / ".claude/settings.json"
    if not settings_path.exists():
        return
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        report.check(False, f".claude/settings.json is not valid JSON: {error}")
        return
    for groups in settings.get("hooks", {}).values():
        for group in groups:
            for hook in group.get("hooks", []):
                for script in re.findall(r"\$\{?CLAUDE_PROJECT_DIR\}?/([\w./-]+)", hook.get("command", "")):
                    report.check((root / script).exists(), f"settings.json hook script missing: {script}")


def status_of(path: Path) -> str:
    raw = (front_matter(path.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")) or {}).get("status", "")
    return re.sub(r"\s#.*$", "", raw).strip().strip("'\"").lower()


def content_lines(path: Path) -> list[str]:
    """Lines that carry content: template guidance sits in '>' blockquotes and is skipped."""
    return [line for line in path.read_text(encoding="utf-8").splitlines() if not line.lstrip().startswith(">")]


def check_trace(root: Path, source: Path, pattern: re.Pattern, haystack: str, target: str, what: str, report: Report) -> None:
    """Every ID the pattern finds in the source must appear in the target text (spec-kit 'analyze', made deterministic)."""
    for item in sorted(set(pattern.findall("\n".join(content_lines(source))))):
        report.check(re.search(rf"\b{re.escape(item)}\b", haystack) is not None,
                     f"{source.relative_to(root)}: {what} {item} reaches no {target}")


def check_artifacts(root: Path, report: Report) -> None:
    """Approved artifacts carry no open [NEEDS CLARIFICATION] and stay traced down the chain (ADR-0006).

    A trace that finds nothing to check is a defect, never a silent pass.
    """
    folders = [root / "docs", *sorted(p for p in (root / "docs/changes").glob("*") if p.is_dir())]
    for folder in folders:
        docs = {name: folder / f"{name}.md" for name in ARTIFACTS if (folder / f"{name}.md").exists()}
        statuses = {name: status_of(path) for name, path in docs.items()}
        for name, status in statuses.items():
            report.check(status in KNOWN_STATUSES, f"{docs[name].relative_to(root)}: unknown status '{status}' — artifact checks cannot run")
        approved = {name for name, status in statuses.items() if status in DONE_STATUSES}
        for name in sorted(approved):
            lines = docs[name].read_text(encoding="utf-8").splitlines()
            text = "\n".join(l.replace(CLARIFY_PLACEHOLDER, "") if l.lstrip().startswith(">") else l for l in lines)
            report.check(CLARIFY.lower() not in text.lower(),
                         f"{docs[name].relative_to(root)}: approved but still has {CLARIFY}]")
        if "prd" in approved:
            report.check(bool(FEATURE_ROW.search("\n".join(content_lines(docs["prd"])))),
                         f"{docs['prd'].relative_to(root)}: approved but no P-n feature row found — the trace proves nothing")
        if "spec" in approved:
            report.check(bool(REQUIREMENT.search("\n".join(content_lines(docs["spec"])))),
                         f"{docs['spec'].relative_to(root)}: approved but no FR-n/NFR-n requirement found — the trace proves nothing")
        if {"prd", "spec"} <= approved:
            requirement_lines = "\n".join(l for l in content_lines(docs["spec"]) if REQUIREMENT.match(l))
            check_trace(root, docs["prd"], MUST_FEATURE, requirement_lines, "requirement line in spec.md", "must-priority feature", report)
        if {"spec", "plan"} <= approved:
            todo = root / "tasks/todo.md"
            haystack = "\n".join(content_lines(docs["plan"]) + (content_lines(todo) if todo.exists() else []))
            check_trace(root, docs["spec"], REQUIREMENT, haystack, "plan.md / todo.md", "requirement", report)


def run(root: Path) -> int:
    report = Report()
    for rel in REQUIRED_FILES:
        report.check((root / rel).exists(), f"required file missing: {rel}")
    skills = check_skills_and_agents(root, report)
    files = repo_files(root, report)
    if files is not None:
        check_links_and_file_map(root, files, report)
    named = {p for src in [root / "CLAUDE.md", *skills] if src.exists()
             for p in NAMED_PATH.findall(src.read_text(encoding="utf-8"))}
    for rel in sorted(named):
        report.check((root / rel).exists(), f"referenced path missing: {rel}")
    if (root / "CLAUDE.md").exists():
        report.check(len((root / "CLAUDE.md").read_text(encoding="utf-8").splitlines()) < 200, "CLAUDE.md is 200+ lines")
    if (root / "memory/now.md").exists():
        report.check(len((root / "memory/now.md").read_text(encoding="utf-8").splitlines()) <= 120, "memory/now.md exceeds 120 lines")
    check_settings(root, report)
    check_artifacts(root, report)
    source = f"{len(files)} files from git ls-files" if files is not None else "git unavailable"
    print(f"input: {root} ({source}); checks run: {report.checks}")
    for message in report.inconclusive:
        print(f"INCONCLUSIVE: {message}")
    if report.defects:
        print("DEFECTS:", *report.defects, sep="\n  - ")
        return 1
    if report.inconclusive:
        return 2
    print("PASS")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    sys.exit(run(target.resolve()))
