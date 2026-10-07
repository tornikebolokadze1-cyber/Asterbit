---
name: sdlc-architecture
description: Phase 2 — turn the accepted intent into architecture decisions (product form, stack, data, hosting, AI models and frameworks, integrations) that the owner chooses from verified alternatives, each recorded as an ADR in docs/decisions/. Use after the intent is approved, or whenever a stack, tool, library, hosting or model choice comes up.
---
# Phase 2 — Architecture decisions

Goal: every significant choice is made by the owner from real alternatives and recorded as an ADR.

## Before you start
- Gate: phase 1 in docs/sdlc-state.md must be `approved`. Read docs/intent.md fully, and docs/decisions/README.md.
- Set phase 2 to `in-progress`.

## 1. List the decisions
Derive the list from the intent — typically: product form and platform; language and framework; data storage; hosting and deployment; AI model and agent framework (if any); integrations; authentication (if any). Show it in plain Georgian and let the owner add or remove items. Put decisions that constrain others first.

## 2. For each decision
1. Spawn the `architect` subagent with the decision, docs/intent.md and the accepted ADRs. It returns 2–3 verified options with pros, cons, cost, risk, reversibility and a recommendation.
2. Consult the advisor on the recommendation and name its verdict.
3. Present the options with AskUserQuestion: recommended option first with "(Recommended)" in the label, a one-sentence trade-off per option, in Georgian. Use `preview` for stack or code comparisons. Gloss any term the owner may not know.
4. After the owner chooses, write `docs/decisions/NNNN-<slug>.md` from sdlc/templates/adr.md (next free number, `scope: product`, `status: accepted`) and add its row to docs/decisions/README.md.
5. If the choice contradicts an earlier accepted ADR: write a new ADR with `supersedes:` and set the old one to `superseded` with `superseded_by:`.

## 3. Close
1. Write the one-paragraph architecture overview in docs/decisions/README.md (what we build with and why); add a mermaid diagram if it helps the owner see the parts.
2. Run the `auditor` (gate: architecture) on the new ADRs: consistency with the intent, unverified claims, missing decisions.
3. Owner approval → phase 2 `approved` + a gate-log line; commit `docs(adr): accept architecture decisions NNNN–MMMM`.
4. Next step: `/sdlc-harness`.

## Done when
Every decision on the list has an accepted ADR with at least two real options considered, the index is current, and the auditor reports no open HIGH finding.
