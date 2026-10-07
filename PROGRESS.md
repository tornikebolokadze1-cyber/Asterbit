# Project Progress — პროექტის პროგრესი

> ახლდება ყოველი ეტაპის, კარიბჭისა და milestone-ის ბოლოს და სესიის დასაწყისში იკითხება, რომ კონტექსტი არ დაიკარგოს.
> ჟურნალი მხოლოდ ივსება: ძველი ჩანაწერები არ იცვლება. ფაილების როლები: [PROCESS.md](PROCESS.md) §4.

## Current State (მიმდინარე მდგომარეობა)
- **Phase:** 0 — Engine setup — IN PROGRESS (ჩონჩხი `main`-შია საერთო საფუძვლად; ADR-0001…0003 და PROCESS.md დამტკიცებას ელოდება)
- **Branch:** `main` (PR #1 გაერთიანდა merge commit-ით) · **GitHub:** private repo `tornikebolokadze1-cyber/Asterbit` · **გუნდი:** მფლობელი + თანამშრომელი lashavamleti (წერის უფლება)
- **Decisions:** ADR-0004 accepted; ADR-0001…0003 proposed
- **Checks (2026-10-07, ლოკალური სკრიპტები — რეპოში ჯერ არ დევს):** სტრუქტურა — 197 შემოწმება, PASS; `docs/FILES.md` 51 ფაილიდან 51-ს მოიცავს; ორივემ ჩადებული დეფექტი დაიჭირა (exit 1). Claude Code-მა 11-ივე `sdlc-*` ბრძანება აღმოაჩინა
- **Not built yet:** `.claude/settings.json`, მეხსიერების hook-ები, სტრუქტურის შემოწმება რეპოში

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

### 2026-10-07 — Phase 0.6: თანამშრომელი და დამოუკიდებელი პროექტი
- მფლობელის მოთხოვნა: პროექტი „ცალკე პროექტი" იყოს, რომ თანამშრომელმა ჩამოტვირთოს და შეცვალოს. შემოწმებამ ოთხი ხარვეზი აჩვენა: `main` ცარიელი იყო; CLAUDE.md მფლობელის კომპიუტერის გლობალურ წესებს ეყრდნობოდა; Claude ყველას მფლობელად ჩათვლიდა; Superpowers plugin სავალდებულოდ ეწერა
- lashavamleti მოწვეულია წერის უფლებით (GitHub invitation, 2026-10-07 07:55 UTC) — მიღებას ელოდება
- ახალი: `CONTRIBUTING.md` (თანამშრომლის გზამკვლევი), `docs/FILES.md` (ყველა ფაილის რუკა)
- CLAUDE.md და PROCESS.md: მფლობელი და თანამშრომლები; კარიბჭეებსა და `main`-ს მხოლოდ მფლობელი ამტკიცებს; უსაფრთხოების წესები რეპოშია და ყველა კომპიუტერზე მოქმედებს; Superpowers სურვილისამებრ; ფაილის დამატებისას `docs/FILES.md` ახლდება
- მფლობელის გადაწყვეტილებით PR #1 `main`-ში merge commit-ით ერთიანდება, როგორც საერთო საფუძველი; ეს ADR-0001…0003-სა და PROCESS.md-ს არ ამტკიცებს — ისინი `proposed` რჩება. merge commit-ი ინარჩუნებს ამ ჟურნალში ნახსენებ ყველა commit-ს
- private რეპოში `main`-ის დაცვა (branch protection) GitHub Pro-ს მოითხოვს (API: HTTP 403), ამიტომ „მხოლოდ PR-ით" ჯერ შეთანხმებაა და არა ტექნიკური აკრძალვა

## In Progress (მიმდინარე)
- lashavamleti-ს მიერ მოწვევის მიღება
- შენი პრინციპები handoff-ისა და შეჯამებისთვის → `memory/README.md`
- ADR-0001…0003-ისა და PROCESS.md-ის განხილვა და დამტკიცება (ADR-0002-ში ჩასამატებელია: თანამშრომლებისთვის Superpowers სურვილისამებრია)

## Next Steps (შემდეგი ნაბიჯები)
1. harness v0 (ახალ branch-ზე): `.claude/settings.json` (Sonnet 5.5 high, Opus 5.5 advisor, `autoCompactWindow: 650000`, უფლებების საბაზისო სია) + გადაწყვეტილება `cleanupPeriodDays`-ზე + სტრუქტურის შემოწმება რეპოში (`sdlc/checks/`: სავალდებულო ფაილები, `docs/FILES.md`-ის სისრულე)
2. მეხსიერების hook-ები (PostCompact → `memory/`, SessionStart → `now.md` + handoff) და მათი drill-ები
3. ძრავის საცდელი გაშვება „სათამაშო" იდეაზე (ეტაპები 1–6)
4. ნამდვილი პროდუქტი: `/sdlc-intent`
