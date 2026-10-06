---
name: sdlc-spec
description: Phase 4 — write docs/spec.md (requirements + design) from the accepted intent and ADRs, with every requirement testable, every success criterion traced to a future check, and every conflict flagged before approval. Use after the harness is approved, or when requirements change.
---
# Phase 4 — Spec

Claude writes the spec; the owner reviews it and resolves the flagged concerns.

## Before you start
Gate: phase 3 `approved`. Read docs/intent.md, the accepted ADRs and any project skills that encode policy. Set phase 4 to `in-progress`.

## Steps
1. Copy sdlc/templates/spec.md → docs/spec.md and write it in one pass from the intent and the ADRs. Every requirement gets an ID (FR-n / NFR-n) and acceptance criteria that a test or an eval can check.
2. Flag concerns explicitly: contradictions between intent and ADRs, open questions still unanswered, privacy or security issues, anything you could not satisfy. Put the concerns first in your summary to the owner.
3. Walk the owner through the concerns one at a time (AskUserQuestion, recommendation first). Record each outcome — resolved or parked — in the spec.
4. Traceability: every success criterion from the intent → at least one requirement → a planned check. Missing links are concerns too.
5. Run the `auditor` (gate: spec): testability, traceability, unverified assumptions.
6. Owner approval → `status: approved`, phase 4 `approved` + a gate-log line, commit `docs(spec): approve`.
7. Next steps: `/sdlc-evaluate` in design mode (choose the gates and evals for this spec), then `/sdlc-plan`.

## Done when
No flagged concern is unresolved, every requirement is testable and traced, the auditor reports no open HIGH finding, and the owner approved.
