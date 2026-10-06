# SDLC state — ფაზების ჟურნალი

> ერთადერთი ადგილი, სადაც წერია, სად ვართ. Claude ამ ფაილს კითხულობს ნებისმიერი ეტაპის დაწყებამდე და აახლებს ყოველ კარიბჭეზე (gate).
> Status values: `not-started` · `in-progress` · `awaiting-approval` · `approved` · `skipped`

| # | Phase | Status | Artifact | Approved by / date |
|---|---|---|---|---|
| 0 | Engine setup | in-progress | sdlc/, .claude/, CLAUDE.md, PROCESS.md, PROGRESS.md, docs/decisions/0001–0004 | — |
| 1 | Intent | not-started | docs/intent.md | — |
| 2 | Architecture | not-started | docs/decisions/ | — |
| 3 | Harness | not-started | .claude/settings.json, .claude/hooks/, ADR | — |
| 4 | Spec | not-started | docs/spec.md | — |
| 5 | Plan | not-started | docs/plan.md, tasks/todo.md | — |
| 6 | Build | not-started | code + tests | — |
| 7 | Evaluate | not-started | gates + evals | — |
| 8 | Secure | not-started | threat model, controls, drills | — |
| 9 | Observe | not-started | log schema, telemetry, control bands | — |

## Current focus (მიმდინარე ფოკუსი)
ძრავა v0: დირექტორია შექმნილია, მეხსიერების ინტერვიუ ჩატარდა (ADR-0004 `accepted`). შემდეგია მფლობელის პრინციპები და harness v0.

## Gate log (კარიბჭეების ჟურნალი)
- 2026-10-06 — Engine scaffold created on branch `engine/v0-scaffold`. Not approved yet.
- 2026-10-06 — ADR-0004 (context & memory) accepted by the owner through the interview: 65% · Obsidian vault · grep → QMD at trigger · ADR + git + wrap check.
