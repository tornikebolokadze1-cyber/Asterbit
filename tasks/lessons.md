# Lessons — გაკვეთილები

> შენი ყოველი შესწორება აქ იწერება: თარიღი · რა მოხდა არასწორად · წესი, რომელიც ამას თავიდან აგვაცილებს.
> გაკვეთილი, რომელიც მეორედ განმეორდება, CLAUDE.md-ში გადადის (playbook-ის წესი: „ერთი შეცდომა ორჯერ → CLAUDE.md").
> If a lesson has a machine check that now prevents it, name the check; if none exists, say so.

| Date | What went wrong | Rule | Check that guards it | In CLAUDE.md? |
|---|---|---|---|---|
| 2026-10-06 | Multi-phase work (research → scaffold → interview) ran without PROGRESS.md, although the owner's global CLAUDE.md requires it, and there was no PROCESS.md either — the owner had to point it out | Create PROGRESS.md at the start of any multi-phase work and append after every phase; keep the working agreement in PROCESS.md | None yet — an existence check for both files is planned with the harness v0 structure gate | Yes — project CLAUDE.md now requires PROGRESS.md entries |
| 2026-10-06 | `git add -A` swept a plugin's runtime file (`.omc/state/idle-notif-cooldown.json`, oh-my-claudecode) into commit 8d4ebae; found while listing files for the owner | Stage explicit paths, not `git add -A`; keep tool state folders in .gitignore | `.omc/` is now in .gitignore (prevents this folder only); no general check yet | Not yet — first occurrence |
