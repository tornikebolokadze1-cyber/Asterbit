# Asterbit — AI-native SDLC engine

This repo holds (1) a phase-gated SDLC engine for building software with Claude Code and (2), later, the product built with it. The product is not chosen yet — Phase 1 decides it. Owner's guide (Georgian): README.md. Working agreement (Georgian): PROCESS.md — it must say the same as this file; report any mismatch as a defect. Work log: PROGRESS.md. Collaborator guide: CONTRIBUTING.md. File map: docs/FILES.md.

## People
- Owner (GitHub: tornikebolokadze1-cyber): writes Georgian, does not read code, learns by building. Answer in Georgian prose; keep technical terms but gloss each on first use; explain what and why before how.
- Collaborators (listed in CONTRIBUTING.md) clone the repo and work on their own branches; their changes reach main only through a pull request. Answer every person in the language they write in.
- Only the owner approves gates and merges into main. When you work with a collaborator, prepare the artifact and the pull request and leave the approval to the owner; never record an approval on someone else's behalf. You never approve your own work, and the agent that wrote something never audits it.

## Lifecycle — current state lives in docs/sdlc-state.md
| # | Phase | Artifact | Skill |
|---|---|---|---|
| 0 | Engine setup | sdlc/, .claude/, CLAUDE.md | — |
| 1 | Intent | docs/intent.md | /sdlc-intent |
| 2 | Architecture | docs/decisions/NNNN-*.md | /sdlc-architecture |
| 3 | Harness | .claude/settings.json, .claude/hooks/, ADR | /sdlc-harness |
| 4 | Spec | docs/spec.md | /sdlc-spec |
| 5 | Plan | docs/plan.md, tasks/todo.md | /sdlc-plan |
| 6 | Build | code + tests | /sdlc-build |
| 7 | Evaluate | gates + evals — designed right after Spec, run during Build and before release | /sdlc-evaluate |
| 8 | Secure | threat model, controls, drills | /sdlc-secure |
| 9 | Observe | log schema, telemetry, control bands | /sdlc-observe |

After release, every finding, bug or new idea becomes a new intent in docs/changes/NNNN-<slug>/ and the loop restarts.

Gate rules:
- Read docs/sdlc-state.md before any phase work. Do not start phase N+1 until phase N is `approved`.
- No product code (anything outside docs/, tasks/, memory/, sdlc/, .claude/, .obsidian/ and the root files README.md, CLAUDE.md, PROCESS.md, PROGRESS.md, CONTRIBUTING.md, .gitignore) before docs/plan.md is approved.
- Before asking for approval, run the `auditor` subagent on the artifact and show its verdict.
- Approval = the owner's explicit words. Record who and when in docs/sdlc-state.md, then commit.
- After every phase, gate or milestone, append a dated entry to PROGRESS.md and refresh its Current State / In Progress / Next Steps. Never rewrite old entries.

## Artifacts
- Copy templates from sdlc/templates/; never edit a template in place.
- Headings stay in English (checks parse them; Georgian gloss in parentheses); content is written in Georgian.
- Unknowns go to "Open questions" — never invent an answer to fill a section.

## Decisions (ADRs)
- Every stack/tool/library/hosting/model choice → ADR in docs/decisions/ (template sdlc/templates/adr.md) + update docs/decisions/README.md.
- Present 2–3 verified options with trade-offs and a recommendation; the owner chooses.
- Never rewrite an accepted decision. A changed mind = new ADR with `supersedes:`; the old one becomes `status: superseded` with `superseded_by:`.
- If an owner instruction contradicts an accepted ADR, say so and ask before acting.

## Models — ADR-0003 (proposed; settings not applied yet)
- Coder: main session, Sonnet 5.5, effort high.
- Advisor: Opus 5.5 via the advisor tool — consult before committing to an approach, when an error repeats, and before declaring done. Name the advisor's verdict in your reply; a missing verdict is an audit finding.
- `architect` subagent (Opus 5.5, high, read-only): option analysis for decisions.
- `auditor` subagent (Opus 5.5, high, read-only): every gate and every milestone diff.
- `verifier` subagent (Sonnet 5.5, medium): runs proofs in a fresh context, reports only.

## Methods
If the Superpowers plugin is installed (optional; see CONTRIBUTING.md), use its skills as techniques (brainstorming, writing-plans, test-driven-development, systematic-debugging, verification-before-completion), but always write to the paths this engine defines — never to docs/plans/ or any default location of those skills. Without it, follow the steps written in our own skills and treat a named Superpowers technique as a hint, not a dependency.

## Verification
- "Done" means the check ran and its output is shown. No output, no claim. "Could not run" is inconclusive, never a pass.
- Bug fix: failing test first, then the fix. Never weaken, skip or delete a test to get green.
- Same failing check: max 3 fix attempts, then stop and explain. Auditor findings: max 2 fix rounds, then report UNVERIFIED.
- Adding, moving or renaming a file: update docs/FILES.md in the same change.

## Memory — ADR-0004 (accepted 2026-10-06; hooks not built yet)
- Compaction at 65% (650k tokens; the setting is applied in harness v0 — until then each machine uses its own). The repo is an Obsidian vault: use standard relative Markdown links. Search = grep until the QMD trigger in ADR-0004.
- Markdown in git is the source of truth for memory; any search or graph index is derived and rebuildable.
- Session start: read memory/now.md (hot state, ≤120 lines), docs/sdlc-state.md and PROGRESS.md (Current State, Next Steps).
- Session end: run /sdlc-wrap.
- Corrected twice → the rule goes into this file; log every correction in tasks/lessons.md.
- Never write secrets, tokens, other people's personal data, or verbatim untrusted text (web pages, fetched files) into memory/ — it would reload every session.

## Compact instructions
When compacting, write the summary as a handoff, in this order:
1. SDLC phase and gate status (docs/sdlc-state.md).
2. Task in flight: files touched, exact next action.
3. Decisions this session with rationale and rejected options; link ADRs.
4. Verified facts verbatim: paths, commands, versions, observed results.
5. Open loops and blockers.
6. Owner's instructions and preferences stated this session (verbatim when short).
7. Dead ends, so they are not retried.
End with four Georgian lines: Done / In progress / Next / Blocked.

## Safety — these rules travel with the repo
The owner's personal global rules exist only on the owner's machine; every other machine gets only what is written here.
- Work on a branch; main changes only through a pull request that the owner approves and merges.
- Ask the person you work with before you push or install anything. Changes to permissions, hooks or settings affect everyone, so they need the owner's yes.
- Never force-push, rewrite pushed history, or run rm -rf, git reset --hard or git clean -f.
- Delete a file only after the person you work with agrees; a deletion reaches main only through a pull request the owner approves.
- Secrets never enter git; .env* is ignored.
