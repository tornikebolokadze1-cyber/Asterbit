# Project Progress — პროექტის პროგრესი

> ახლდება ყოველი ეტაპის, კარიბჭისა და milestone-ის ბოლოს და სესიის დასაწყისში იკითხება, რომ კონტექსტი არ დაიკარგოს.
> ჟურნალი მხოლოდ ივსება: ძველი ჩანაწერები არ იცვლება. ფაილების როლები: [PROCESS.md](PROCESS.md) §4.

## Current State (მიმდინარე მდგომარეობა)
- **Phase:** 0 — Engine setup — IN PROGRESS (scaffold მზადაა და შენს დამტკიცებას ელოდება)
- **Branch:** `engine/v0-scaffold` (`main`-ში ჯერ არ გაერთიანებულა) · **GitHub:** private repo `tornikebolokadze1-cyber/Asterbit`, PR #1 განსახილველად
- **Decisions:** ADR-0004 accepted; ADR-0001…0003 proposed
- **Checks:** სტრუქტურული შემოწმება 92/92 გადის; drill-მა ჩადებული 3 შეცდომიდან 3 დაიჭირა; Claude Code-მა 11-ივე `sdlc-*` ბრძანება აღმოაჩინა
- **Not built yet:** `.claude/settings.json`, მეხსიერების hook-ები

## Completed (დასრულებული)

### 2026-10-06 — Phase 0.1: კვლევა
- Anthropic-ის „AI-native SDLC playbook" (2026-08-21) სრულად წავიკითხე → `sdlc/research/playbook-notes.md`
- awesome-ai-pulse-georgia-ს ოთხი სექცია შევაფასე, რეპოების აქტიურობა GitHub API-ით გადავამოწმე (GSD archived-ია) → `sdlc/research/engine-selection.md`
- Claude Code-ის დოკუმენტაციით (VS Code-ში 2.1.289) გადავამოწმე: `autoCompactWindow`, PreCompact/PostCompact, advisor tool, effort, subagent-ებისა და skill-ების front matter
- შენს კომპიუტერზე აღმოვაჩინე: გლობალური handoff hook-ები უკვე მუშაობს; MemPalace-ის hook ჩუმად ვერ სრულდება; სესიების ჩანაწერები 30 დღეში იშლება; ტერმინალის CLI 2.1.92-ია

### 2026-10-06 — Phase 0.2: დირექტორია (scaffold)
- git ჩაირთო; branch `engine/v0-scaffold`; commits `3dc2036`, `095d2da`, `85731b3`
- შეიქმნა: README, CLAUDE.md, 11 skill, 3 აგენტი, 7 თარგი, 5 დიზაინ-დოკუმენტი, ADR-0001…0004, `memory/` ფენები
- შემოწმება: 92/92 გადის; drill-მა 3 ჩადებული შეცდომიდან 3 დაიჭირა

### 2026-10-06 — Phase 0.3: მეხსიერების ინტერვიუ
- ADR-0004 accepted: შეკუმშვა 65% · Obsidian vault · ჯერ grep, QMD ზღვარზე · ADR + git + wrap — commit `62b1008`
- Obsidian-ში ჩაირთო ჩვეულებრივი markdown ბმულები (`.obsidian/app.json`)

### 2026-10-06 — Phase 0.4: PROCESS.md და PROGRESS.md
- სამუშაო შეთანხმება ერთ დოკუმენტში ჩაიწერა ([PROCESS.md](PROCESS.md)), პლუს ეს ჟურნალი
- CLAUDE.md-ში დაემატა წესი: PROGRESS.md ყოველი ეტაპის, კარიბჭისა და milestone-ის ბოლოს ივსება; `/sdlc-wrap`-ს შესაბამისი ნაბიჯი დაემატა
- გაკვეთილი ჩაიწერა `tasks/lessons.md`-ში: ეს ფაილები თავიდანვე უნდა შექმნილიყო

### 2026-10-06 — Phase 0.5: GitHub
- `git add -A`-მა plugin-ის დროებითი ფაილი (`.omc/state/idle-notif-cooldown.json`) commit-ში შეიტანა; თვალყურის დევნება შეწყდა, `.omc/` → .gitignore, გაკვეთილი ჩაიწერა — commit `5e41fad`
- საიდუმლოებების შემოწმება ატვირთვამდე: gitleaks (მთელი git ისტორია) და scan_secrets.py — exit 0; ორივემ ჩადებული ყალბი გასაღები დაიჭირა — exit 1
- შეიქმნა private რეპო https://github.com/tornikebolokadze1-cyber/Asterbit; აიტვირთა `main` და `engine/v0-scaffold`; GitHub-ზე 49 ფაილია
- გაიხსნა PR #1 (`engine/v0-scaffold` → `main`): მისი merge = ძრავის v0-ის დამტკიცება

## In Progress (მიმდინარე)
- l.vamleti@asterbit.io-ს მოწვევა რეპოში — საჭიროა მისი GitHub username (ელფოსტით ანგარიში საჯაროდ არ იძებნება)
- შენი პრინციპები handoff-ისა და შეჯამებისთვის → `memory/README.md`
- scaffold-ის განხილვა → ADR-0001…0003-ისა და PROCESS.md-ის დამტკიცება → `main`-ში გაერთიანება

## Next Steps (შემდეგი ნაბიჯები)
1. harness v0: `.claude/settings.json` (Sonnet 5.5 high, Opus 5.5 advisor, `autoCompactWindow: 650000`, უფლებების საბაზისო სია) + გადაწყვეტილება `cleanupPeriodDays`-ზე
2. მეხსიერების hook-ები (PostCompact → `memory/`, SessionStart → `now.md` + handoff) და მათი drill-ები
3. ძრავის საცდელი გაშვება „სათამაშო" იდეაზე (ეტაპები 1–6)
4. ნამდვილი პროდუქტი: `/sdlc-intent`
