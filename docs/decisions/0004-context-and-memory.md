---
id: "0004"
title: Context and memory layers
status: proposed
scope: engine
date: 2026-10-06
deciders: owner (interview pending), Claude (drafted)
supersedes: —
superseded_by: —
review_by: after the interview
tags: [memory, context, harness]
---
# 0004 — Context and memory layers

## Context (კონტექსტი)
Owner's requirements (2026-10-06): compaction at 60–70%; an automatic handoff before every compaction, following agreed principles; the 4–5 handoffs of a long session merged instead of piling up; a session summary at the end of every session, saved; long-term protection against context overflow through memory layers (graph — e.g. Obsidian; RAG; episodic) that also reveal decisions the owner changed over time. Design and measurements: `sdlc/design/memory-and-context.md`.

## Fixed by design (follows from the requirements and the docs)
1. Markdown in git is the source of truth; every index (search, graph, vectors) is derived and can be rebuilt from the files.
2. Rolling handoff: each compaction summary already contains the previous one, so a session keeps one current handoff; older versions move to the archive.
3. Session summary through `/sdlc-wrap`; if a session ends without one, the next session start asks for it.
4. One injector at session start, with a budget: memory/now.md (≤120 lines) + the current handoff when resuming.

## Options — to be chosen in the interview
- Compaction threshold: 60% / 65% / 70% of the 1M-token window.
- Graph layer: Obsidian vault / Obsidian + Graphify / none yet.
- Retrieval (RAG): grep now + QMD at a measured trigger / QMD now / MemPalace / claude-mem.
- Changed-decision detection: ADR + git + wrap-time check / the same + Graphiti later / MemPalace knowledge graph.

## Decision (გადაწყვეტილება)
_Pending the owner's answers._

## Verification (როგორ შევამოწმებთ)
Defined together with the decision — for example: a manual `/compact` drill shows the summary in the agreed shape and the PostCompact hook writes it into memory/; a budget check fails when memory/now.md exceeds 120 lines.

## Links
- sdlc/design/memory-and-context.md
- memory/README.md
