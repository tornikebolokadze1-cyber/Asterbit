#!/usr/bin/env python3
"""PreToolUse guard for the Asterbit repo — travels with the repo to every machine.

Blocks (exit 2, stderr starts with ASTERBIT-GUARD): recursive force delete,
git reset --hard, git clean -f, force push, any push that lands on or deletes
main (including `git push origin HEAD` while on main), --no-verify, history
rewriting, credential files sent over the network or encoded, writing secret
files, and — for the auditor / verifier / architect agents — any file change.
Asks first (JSON permissionDecision "ask"): commands that throw away
uncommitted work or delete a branch. Commands hidden in `bash -c` / `eval`
are checked too. Everything else exits 0 and the normal permission rules
decide. If the guard itself fails, it blocks.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from secret_patterns import is_secret_file  # noqa: E402

MARKER = "ASTERBIT-GUARD"
FALLBACK_SPLIT = re.compile(r"\|\||&&|;|\||\n|\$\(|`")
OPERATOR_CHARS = set(";&|()")
CREDENTIAL_PATH = re.compile(
    r"(?:^|[\s'\"/=@<])(?:\.env(?!\.example\b)(?:\.[\w-]+)?|\.ssh/|id_rsa|id_ed25519|\.aws/|\.npmrc|"
    r"\.git-credentials|serviceAccountKey|credentials\.json|[\w-]+\.(?:pem|p12|pfx))(?:$|[\s'\"])"
)
TRANSFER_VERBS = {"curl", "wget", "nc", "ncat", "scp", "rsync", "sftp", "ftp", "base64", "xxd", "openssl"}
GIT_OPTIONS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree"}
PUSH_OPTIONS_WITH_VALUE = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}
SHELLS = {"bash", "sh", "zsh", "dash"}
SHORT_FLAGS = re.compile(r"-[a-zA-Z]+")
Finding = tuple[str, str]  # ("block" | "ask", reason)
REDIRECT_OPERATOR = re.compile(r"\d*(?:>>?|<<?<?|>\||<>)")  # its target is the next token
REDIRECT_WITH_TARGET = re.compile(r"\d*(?:>>?|<<?|>\|)\S+")  # e.g. 2>/dev/null, >push.log


def without_redirects(tokens: list[str]) -> list[str]:
    """`git push origin 2>&1` must not look like a push of a branch called '2>'."""
    kept, skip_next = [], False
    for token in tokens:
        if skip_next:
            skip_next = False
        elif REDIRECT_OPERATOR.fullmatch(token):
            skip_next = True
        elif not REDIRECT_WITH_TARGET.fullmatch(token):
            kept.append(token)
    return kept


def segments_of(command: str) -> list[list[str]]:
    """Split a command line into simple commands, respecting quotes and dropping redirections."""
    lexer = shlex.shlex(command.replace("`", " ; ").replace("\n", " ; "), posix=True, punctuation_chars=";&|()")
    lexer.whitespace_split = True
    try:
        tokens = list(lexer)
    except ValueError:
        return [without_redirects(segment.split()) for segment in FALLBACK_SPLIT.split(command)]
    segments, current = [], []
    for token in tokens:
        if token and set(token) <= OPERATOR_CHARS:
            if current:
                segments.append(current)
            current = []
        else:
            current.append(token)
    return [without_redirects(s) for s in segments + ([current] if current else [])]


def inner_commands(tokens: list[str]) -> list[str]:
    """Command strings hidden inside `bash -c '…'` or `eval …`."""
    inner = []
    for i, token in enumerate(tokens):
        name = os.path.basename(token)
        if name in SHELLS:
            for j in range(i + 1, len(tokens) - 1):
                if re.fullmatch(r"-[a-zA-Z]*c[a-zA-Z]*", tokens[j]):
                    inner.append(tokens[j + 1])
                    break
        elif name == "eval" and i + 1 < len(tokens):
            inner.append(" ".join(tokens[i + 1:]))
    return inner


def git_calls(tokens: list[str]) -> list[tuple[str, list[str]]]:
    """Every `git <subcommand> args` inside one simple command (handles `git -C dir …`)."""
    calls = []
    for i, token in enumerate(tokens):
        if os.path.basename(token) != "git":
            continue
        j = i + 1
        while j < len(tokens) and tokens[j].startswith("-"):
            j += 2 if tokens[j] in GIT_OPTIONS_WITH_VALUE else 1
        if j < len(tokens):
            calls.append((tokens[j], tokens[j + 1:]))
    return calls


def current_branch(cwd: str) -> str:
    try:
        # symbolic-ref also answers on a branch with no commits yet, where rev-parse fails
        return subprocess.run(["git", "-C", cwd, "symbolic-ref", "--short", "-q", "HEAD"],
                              capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def push_destination(ref: str, branch: str) -> str:
    source, colon, destination = ref.lstrip("+").partition(":")
    destination = destination if colon else source
    destination = destination.removeprefix("refs/heads/")
    return branch if destination in ("HEAD", "@", "") else destination


def push_problem(args: list[str], cwd: str) -> Finding | None:
    flags, positional, skip = [], [], False
    for arg in args:
        if skip:
            skip = False
        elif arg.startswith("-"):
            flags.append(arg)
            skip = arg in PUSH_OPTIONS_WITH_VALUE
        else:
            positional.append(arg)
    if any(f.startswith("--force") or (SHORT_FLAGS.fullmatch(f) and "f" in f) for f in flags):
        return "block", "force push rewrites shared history"
    if any(ref.startswith("+") for ref in positional[1:]):
        return "block", "a '+refspec' push is a force push"
    if "--all" in flags or "--mirror" in flags:
        return "block", "--all/--mirror would also push main"
    branch = current_branch(cwd)
    for ref in positional[1:] or ["HEAD"]:  # no refspec = the current branch
        if push_destination(ref, branch) == "main":
            return "block", "this push would land on (or delete) main — push a branch and open a pull request"
    return None


def discard_problem(subcommand: str, args: list[str]) -> Finding | None:
    """Commands that throw away uncommitted work or a branch: ask a person first."""
    forced = any(a in ("--force", "--discard-changes") or (SHORT_FLAGS.fullmatch(a) and "f" in a) for a in args)
    if subcommand in ("switch", "checkout") and forced:
        return "ask", f"git {subcommand} with force throws away uncommitted changes"
    if subcommand == "checkout" and ("--" in args or "." in args):
        return "ask", "git checkout of paths throws away uncommitted changes in those files"
    if subcommand == "restore" and not any(a in ("--staged", "-S") for a in args):
        return "ask", "git restore throws away uncommitted changes in those files"
    if subcommand == "branch" and any(a in ("-D", "--force") or (a == "--delete" and "--force" in args) for a in args):
        return "ask", "git branch -D deletes a branch even if its work is not merged"
    if subcommand == "stash" and args[:1] in (["drop"], ["clear"]):
        return "ask", "git stash drop/clear deletes saved work"
    return None


def git_problem(subcommand: str, args: list[str], cwd: str) -> Finding | None:
    if "--no-verify" in args or (subcommand == "commit" and any(SHORT_FLAGS.fullmatch(a) and "n" in a for a in args)):
        return "block", "--no-verify skips the safety checks"
    if subcommand == "reset" and "--hard" in args:
        return "block", "git reset --hard throws away uncommitted work"
    if subcommand == "clean" and any(a == "--force" or (SHORT_FLAGS.fullmatch(a) and "f" in a) for a in args):
        return "block", "git clean -f deletes untracked files for good"
    if subcommand == "push":
        return push_problem(args, cwd)
    if subcommand in ("filter-branch", "filter-repo"):
        return "block", "rewriting history is not allowed"
    if subcommand == "branch" and any(a in ("-D", "-d", "--delete") for a in args) and "main" in args:
        return "block", "deleting main is not allowed"
    return discard_problem(subcommand, args)


def rm_problem(tokens: list[str]) -> Finding | None:
    for i, token in enumerate(tokens):
        if os.path.basename(token) != "rm":
            continue
        rest = tokens[i + 1:]
        short = "".join(t[1:] for t in rest if SHORT_FLAGS.fullmatch(t))
        recursive = "r" in short.lower() or "--recursive" in rest
        force = "f" in short or "--force" in rest
        if recursive and force:
            return "block", "recursive force delete (rm -rf) — ask a person to delete it"
    return None


def bash_problem(command: str, cwd: str, depth: int = 0) -> Finding | None:
    first_ask = None
    for tokens in segments_of(command):
        findings = [rm_problem(tokens)] + [git_problem(s, a, cwd) for s, a in git_calls(tokens)]
        if depth < 3:
            findings += [bash_problem(inner, cwd, depth + 1) for inner in inner_commands(tokens)]
        for finding in filter(None, findings):
            if finding[0] == "block":
                return finding
            first_ask = first_ask or finding
    words = {os.path.basename(t) for tokens in segments_of(command) for t in tokens}
    if CREDENTIAL_PATH.search(command) and words & TRANSFER_VERBS:
        return "block", "a credential file together with a network/encoding command looks like exfiltration"
    return first_ask


READ_ONLY_AGENTS = {"auditor", "verifier", "architect"}
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
WRITING_COMMANDS = {"rm", "mv", "cp", "mkdir", "touch", "chmod", "chown", "tee", "truncate", "dd", "ln", "rmdir"}
WRITING_GIT = {"add", "commit", "push", "pull", "checkout", "switch", "reset", "restore", "merge", "rebase",
               "stash", "clean", "rm", "mv", "tag", "cherry-pick", "revert", "apply", "am", "worktree", "branch"}
QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")
REDIRECT = re.compile(r"(?<![0-9&])>{1,2}(?!&)\s*(?!/dev/null)\S")


def read_only_problem(tool: str, tool_input: dict, depth: int = 0) -> Finding | None:
    """auditor / verifier / architect report; they never change files."""
    if tool in WRITE_TOOLS:
        return "block", f"{tool} is not allowed for a read-only agent"
    if tool != "Bash":
        return None
    command = tool_input.get("command", "")
    if REDIRECT.search(QUOTED.sub("''", command)):
        return "block", "writing to a file (>) is not allowed for a read-only agent"
    for tokens in segments_of(command):
        words = {os.path.basename(t) for t in tokens}
        if words & WRITING_COMMANDS or (words & {"sed", "perl"} and any(t.startswith("-i") for t in tokens)):
            return "block", "a file-changing command is not allowed for a read-only agent"
        if any(sub in WRITING_GIT for sub, _ in git_calls(tokens)):
            return "block", "a git command that changes the repo is not allowed for a read-only agent"
        if "gh" in words and words & {"create", "merge", "edit", "close", "comment", "delete"}:
            return "block", "a GitHub change is not allowed for a read-only agent"
        for inner in inner_commands(tokens) if depth < 3 else []:
            finding = read_only_problem("Bash", {"command": inner}, depth + 1)
            if finding:
                return finding
    return None


def general_problem(tool: str, tool_input: dict, cwd: str) -> Finding | None:
    if tool == "Bash":
        return bash_problem(tool_input.get("command", ""), cwd)
    if tool in WRITE_TOOLS:
        path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        if is_secret_file(path):
            return "block", f"{os.path.basename(path)} is a secret file — edit it by hand, outside Claude"
    return None


def main() -> int:
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    tool_input = event.get("tool_input", {}) or {}
    cwd = event.get("cwd") or os.getcwd()
    agent = str(event.get("agent_type") or "").split(":")[-1]
    finding = read_only_problem(tool, tool_input) if agent in READ_ONLY_AGENTS else None
    finding = finding or general_problem(tool, tool_input, cwd)
    if finding and finding[0] == "block":
        print(f"{MARKER}: blocked — {finding[1]}.", file=sys.stderr)
        return 2
    if finding:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                                 "permissionDecisionReason": f"{MARKER}: ask first — {finding[1]}."}}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # fail closed: a broken guard must not let things through
        print(f"{MARKER}: blocked — the guard itself failed ({type(error).__name__}: {error}).", file=sys.stderr)
        sys.exit(2)
