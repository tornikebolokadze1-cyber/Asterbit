#!/usr/bin/env python3
"""PreToolUse hook: scan staged changes for secrets before Claude runs `git commit`.

Two scanners: the built-in patterns (always run, no dependencies) and gitleaks
when it is installed. The output names the scanners that actually ran.
Exit 2 (stderr starts with ASTERBIT-SECRETS) blocks the commit; exit 0 lets the
normal permission rules decide. A scan that cannot run blocks — no evidence is
not a pass. A commit that would include anything not yet staged (`git add …
&& git commit`, `-a`, `-i`, `-o`, `-p`, file names) is blocked too, because
the scan only sees what is already staged.
The scan runs in the repository the commit really lands in: `git -C dir`, a
`cd dir &&` before it and a `bash -c '…'` string are followed. A folder that
cannot be known without running the shell (`$VAR`, `--git-dir`, `GIT_DIR=`)
blocks the commit — no evidence is not a pass.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guard import GIT_OPTIONS_WITH_VALUE, inner_commands, segments_of  # noqa: E402
from secret_patterns import find_secrets, is_secret_file  # noqa: E402

MARKER = "ASTERBIT-SECRETS"
GIT_ENV = re.compile(r"\bGIT_(?:DIR|WORK_TREE|INDEX_FILE|COMMON_DIR|NAMESPACE)=")
DIRECTORY_OPTIONS = ("--git-dir", "--work-tree")
DYNAMIC_PATH = re.compile(r"[$`*?\[{\\]")
FANCY_SHELL = re.compile(r"[(){}|]")  # a `cd` next to these may not reach the next command
STAGING_SUBCOMMANDS = {"add", "rm", "mv", "stage"}
BYPASS_LONG = {"--all", "--include", "--only", "--interactive", "--patch", "--pathspec-from-file"}
VALUE_LONG = {"--message", "--file", "--author", "--date", "--template", "--reuse-message", "--reedit-message",
              "--fixup", "--squash", "--trailer", "--cleanup"}
VALUE_SHORT = set("mFCct")
BYPASS_SHORT = set("aiop")


def commit_bypasses_index(args: list[str]) -> str | None:
    """Why this commit would include changes that are not staged yet, or None."""
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--":
            return "it names files to commit" if i + 1 < len(args) else None
        if arg.startswith("--"):
            name = arg.split("=", 1)[0]
            if name in BYPASS_LONG:
                return f"{name} commits changes that are not staged"
            i += 2 if name in VALUE_LONG and "=" not in arg else 1
            continue
        if arg.startswith("-") and len(arg) > 1:
            for k, letter in enumerate(arg[1:]):
                if letter in BYPASS_SHORT:
                    return f"-{letter} commits changes that are not staged"
                if letter in VALUE_SHORT:
                    i += 1 if k == len(arg) - 2 else 0  # value is the next token only if the letter ends the cluster
                    break
            i += 1
            continue
        return "it names files to commit"
    return None


def step(base: str | None, path: str) -> str | None:
    """Where `cd path` / `git -C path` leads from base; None when only running the shell would tell."""
    if not path or path == "-" or DYNAMIC_PATH.search(path):
        return None
    path = os.path.expanduser(path)
    if os.path.isabs(path):
        return os.path.normpath(path)
    return os.path.normpath(os.path.join(base, path)) if base else None


def git_invocations(tokens: list[str]):
    """`git [options] sub args` → (sub, args, `-C` paths, whether --git-dir/--work-tree redirect it)."""
    for i, token in enumerate(tokens):
        if os.path.basename(token) != "git":
            continue
        j, c_paths, redirected = i + 1, [], False
        while j < len(tokens) and tokens[j].startswith("-"):
            if tokens[j] == "-C" and j + 1 < len(tokens):
                c_paths.append(tokens[j + 1])
            redirected = redirected or tokens[j].startswith(DIRECTORY_OPTIONS)
            j += 2 if tokens[j] in GIT_OPTIONS_WITH_VALUE else 1
        if j < len(tokens):
            yield tokens[j], tokens[j + 1:], c_paths, redirected


def git_runs(command: str, cwd: str, depth: int = 0, seen: list[str | None] | None = None):
    """Every git call as (subcommand, args, folders it may run in); None among the folders = unknown."""
    seen = list(seen or [cwd])
    runs = []
    for tokens in segments_of(command):
        name = os.path.basename(tokens[0]) if tokens else ""
        if name in ("cd", "pushd", "popd"):
            args = [t for t in tokens[1:] if t == "-" or not t.startswith("-")]
            seen.append(None if name == "popd" else step(seen[-1], args[0] if args else "~"))
            continue
        # a plain `cd X && git commit` lands in X; around ( ) { } | the cd may not reach it, so every folder is scanned
        bases = seen if len(seen) > 1 and FANCY_SHELL.search(command) else seen[-1:]
        for sub, args, c_paths, redirected in git_invocations(tokens):
            places = []
            for base in bases:
                for c_path in c_paths:
                    base = step(base, c_path)
                places.append(base)
            runs.append((sub, args, [None] if redirected else places))
        if depth < 3:
            for inner in inner_commands(tokens):
                runs += git_runs(inner, seen[-1], depth + 1, seen)
    return runs


def work_tree_roots(places: list[str | None]) -> list[str]:
    """The repositories a commit can land in; raises when that cannot be known or there is none."""
    if None in places:
        raise RuntimeError("cannot tell which folder this commit runs in (a variable, --git-dir or similar) — "
                           "use `git -C /full/path commit …` or `cd /full/path` first")
    roots = []
    for place in dict.fromkeys(places):
        probe = subprocess.run(["git", "-C", place, "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if probe.returncode == 0:
            roots.append(probe.stdout.strip())
    if not roots:
        raise RuntimeError(f"no git repository at {', '.join(dict.fromkeys(places))}")
    return list(dict.fromkeys(roots))


def git(cwd: str, *args: str) -> str:
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, check=True, timeout=30).stdout


def builtin_scan(cwd: str) -> list[str]:
    findings = [f"{name}: secret file is staged" for name in git(cwd, "diff", "--cached", "--name-only").splitlines()
                if is_secret_file(name)]
    added = "\n".join(line[1:] for line in git(cwd, "diff", "--cached", "-U0", "--no-color").splitlines()
                      if line.startswith("+") and not line.startswith("+++"))
    return findings + [f"staged change, {item}" for item in find_secrets(added)]


def gitleaks_scan(cwd: str) -> tuple[str, list[str]]:
    if shutil.which("gitleaks") is None:
        return "gitleaks not installed", []
    result = subprocess.run(["gitleaks", "git", "--pre-commit", "--staged", "--redact", "--no-banner", cwd],
                            capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        return "gitleaks", []
    if result.returncode == 1:
        return "gitleaks", ["gitleaks found a leak in the staged changes (run it yourself to see where)"]
    raise RuntimeError(f"gitleaks exited {result.returncode}")


def main() -> int:
    event = json.load(sys.stdin)
    command = (event.get("tool_input") or {}).get("command", "")
    calls = git_runs(command, event.get("cwd") or os.getcwd()) if event.get("tool_name") == "Bash" else []
    commits = [(args, places) for sub, args, places in calls if sub == "commit"]
    if not commits:
        return 0
    reason = next(filter(None, (commit_bypasses_index(args) for args, _ in commits)), None)
    if reason or any(sub in STAGING_SUBCOMMANDS for sub, _, _ in calls):
        why = reason or "files are staged in the same command"
        print(f"{MARKER}: blocked — {why}, so the secret scan cannot see them. Stage with `git add <files>` "
              "first, then run `git commit -m …` (or `-F file`) as a separate command.", file=sys.stderr)
        return 2
    if GIT_ENV.search(command):
        raise RuntimeError("GIT_DIR / GIT_WORK_TREE / GIT_INDEX_FILE point git somewhere the scan cannot follow")
    roots = work_tree_roots([place for _, places in commits for place in places])
    findings, labels = [], set()
    for root in roots:
        findings += builtin_scan(root)
        label, leaks = gitleaks_scan(root)
        labels.add(label)
        findings += leaks
    scanners = f"built-in patterns + {' / '.join(sorted(labels))}; repository: {', '.join(roots)}"
    if findings:
        print(f"{MARKER}: blocked — possible secret in the commit ({scanners}):", *findings, sep="\n  ", file=sys.stderr)
        return 2
    print(f"{MARKER}: staged changes are clean ({scanners}).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # the scan could not run: block, do not pass silently
        print(f"{MARKER}: blocked — the secret scan could not run ({type(error).__name__}: {error}).", file=sys.stderr)
        sys.exit(2)
