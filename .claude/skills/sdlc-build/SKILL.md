---
name: sdlc-build
description: Phase 6 — implement tasks/todo.md with the build loop (test first, check, audit, commit) under the stage-1 orchestration (Sonnet 5.5 coder, Opus 5.5 advisor and auditor). Use when the plan is approved and it is time to write code, or to resume building.
---
# Phase 6 — Build

## Roles (ADR-0003)
- You, the main session (Sonnet 5.5, effort high): the coder. You implement, run checks, fix.
- Advisor (Opus 5.5, advisor tool): consult before choosing the approach for a non-trivial task, when the same error appears twice, and before declaring a milestone done. Name its verdict.
- `verifier` subagent: runs the milestone's proof commands in a fresh context and reports only.
- `auditor` subagent (Opus 5.5, high): reviews the milestone diff against docs/spec.md and docs/plan.md; never fixes.
- Owner: sees a demo at every milestone and approves it.

## Before you start
Gate: phase 5 `approved`. Work on a branch `feat/<milestone>`, never on main. Set phase 6 to `in-progress`.

## The loop — once per task
1. Take the first unchecked task in tasks/todo.md and re-read its proof.
2. RED — write the failing test (or the screenshot check for UI). Run it and confirm it fails for the expected reason. Technique: Superpowers `test-driven-development`.
3. GREEN — write the minimal code that passes.
4. CHECK — run the project's single check command (tests + lint + types). Iterate. After 3 failed fix attempts on the same check: stop, explain in Georgian, ask. Technique for failures: Superpowers `systematic-debugging`.
5. IMPROVE — simplify if needed, then re-run CHECK.
6. RECORD — tick the task with evidence (command + result line). If you deviated from docs/plan.md, add a line to its Deviation log in the same commit.
7. COMMIT — conventional commit on the branch.

## The milestone gate — after the last task of a milestone
1. `verifier` runs the milestone proof in a fresh context.
2. `auditor` reviews the milestone diff (passes: bugs · security · compliance with spec and plan · tests that would really fail). Fix what it locates with evidence; at most 2 fix rounds, then report UNVERIFIED with the open findings.
3. Owner demo — tell the owner where to look, what success looks like and what failure would look like.
4. Owner approval → merge or PR per the harness rules; update the progress note in docs/sdlc-state.md.

## Never
- Edit or delete a test to make it pass during a fix.
- Skip CHECK because "the change is small".
- Grow scope beyond the task — park new ideas in tasks/todo.md under "Parked".

## Done when (phase)
All tasks are ticked with evidence, every milestone is audited and owner-approved, and the phase-7 gates are green.
