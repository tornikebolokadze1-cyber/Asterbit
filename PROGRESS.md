# Project Progress — პროექტის პროგრესი

> ახლდება ყოველი ეტაპის, კარიბჭისა და milestone-ის ბოლოს და სესიის დასაწყისში იკითხება, რომ კონტექსტი არ დაიკარგოს.
> ჟურნალი მხოლოდ ივსება: ძველი ჩანაწერები არ იცვლება. ფაილების როლები: [PROCESS.md](PROCESS.md) §4.

## Current State (მიმდინარე მდგომარეობა)
- **Phase:** 0 — Engine setup — IN PROGRESS (harness v0 აწყობილია branch-ზე `engine/v1`; შემდეგია საცდელი გაშვება და Phase 0-ის კარიბჭე)
- **Branch:** `engine/v1` (`main`-ში PR-ით შევა) · **GitHub:** private repo `tornikebolokadze1-cyber/Asterbit` · **გუნდი:** მფლობელი + თანამშრომელი lashavamleti (წერის უფლება, მოწვევა მიღებულია)
- **Decisions:** ADR-0004 accepted; ADR-0001…0003 და ADR-0005 proposed
- **Checks (2026-10-07, რეპოში — `sdlc/checks/`):** სტრუქტურა — 269 შემოწმება, PASS (61 ფაილი); წვრთნა — 89 შემთხვევა, ARMED (50 ჩადებული დეფექტი დაიჭირა, 25 სუფთა მაგალითი გავიდა, 7 „იკითხე" შემთხვევა, 7 ფაილის/კონტექსტის შემოწმება, მათ შორის სტრუქტურის შემოწმება 3-დეფექტიან ასლზე); „უმოქმედო" hook-ებით — DEAD (exit 1)
- **Not built yet:** ნამდვილი `/compact`-ით hook-ის გამოცდა; ძრავის საცდელი გაშვება

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

### 2026-10-07 — Phase 0.7: harness v0 (branch `engine/v1`)
- მფლობელის გადაწყვეტილებები: დაბალანსებული ავტონომია; სესიების ჩანაწერები 30 დღე (ნაგულისხმევი, პარამეტრი არ იცვლება); handoff-ისა და შეჯამების რვა პრინციპი (Claude-ის შემოთავაზება); CI ყოველ PR-ზე → [ADR-0005](docs/decisions/0005-harness-v0.md) (proposed)
- `.claude/settings.json`: Sonnet 5.5 high, Opus 5.5 advisor, `autoCompactWindow: 650000`, allow / ask / deny უფლებები; ჩაწერისთანავე advisor tool ამ სესიაში გამოჩნდა — ესე იგი, ის ამ ანგარიშზე მუშაობს
- hook-ები `.claude/hooks/`-ში (Python, მხოლოდ სტანდარტული ბიბლიოთეკა): `guard.py`, `commit_secrets.py`, `secret_patterns.py`, `memory_handoff.py`, `memory_context.py`
- შემოწმებები `sdlc/checks/`-ში: `check_structure.py`, `drill_hooks.py`; CI: `.github/workflows/checks.yml` (actions/checkout ზუსტ commit-ზე, gitleaks 8.30.1 checksum-ით)
- ცოცხალი გამოცდა: საიდუმლო ფაილის (`.env.probe`) ჩაწერა პროექტის hook-მა დაბლოკა (ASTERBIT-GUARD); verifier აგენტის `touch` დაიბლოკა „read-only agent" შეტყობინებით და ფაილი არ შეიქმნა
- დოკუმენტები: CLAUDE.md და PROCESS.md (push სამუშაო branch-ზე თავისუფლად, `main`-ში — არასდროს; hook-ები; შემოწმებები), CONTRIBUTING.md (Python 3, დაცვა), docs/FILES.md, README.md, `memory/README.md`-ში რვა პრინციპი, ADR-0002-ში Superpowers-ის შენიშვნა, `/sdlc-status` PROGRESS.md-საც კითხულობს
- auditor-ის პირველმა შემოწმებამ harness ჩააჭრა (FAIL): `main`-ზე ყოფნისას `git push origin HEAD` არ იბლოკებოდა; პლუს რვა საშუალო ხარვეზი (`bash -c`-ში დამალული ბრძანება, commit ფაილის სახელით სკანირებას გვერდს უვლიდა, `switch -f`/`branch -D` უკითხავად, handoff-ის ფაილი CI-ს გააწითლებდა და სხვ.). ყველა გასწორდა და თითოეულს წვრთნის შემთხვევა დაემატა. მეორე რაუნდმა კიდევ ერთი გზა იპოვა (`git push origin 2>&1` — გადამისამართება branch-ის სახელად ითვლებოდა); გასწორდა და წვრთნით შემოწმდა. მესამე აუდიტი არ ჩატარებულა (ორი რაუნდის ლიმიტი), ამიტომ ბოლო გასწორებას მხოლოდ წვრთნა ადასტურებს
- გზად: lashavamleti-მ მოწვევა მიიღო (2026-10-07, GitHub API: role `write`)

## In Progress (მიმდინარე)
- `engine/v1` → PR → `main` (CI მწვანე უნდა იყოს; გაერთიანება — შენი თანხმობით)

## Next Steps (შემდეგი ნაბიჯები)
1. ძრავის საცდელი გაშვება „სათამაშო" იდეაზე (ეტაპები 1–6), ცალკე branch-ზე, რომელიც `main`-ში არ შევა; ნაპოვნი ხარვეზების გასწორება
2. ნამდვილი `/compact`-ით მეხსიერების hook-ის გამოცდა (`memory/episodic/handoffs/`)
3. Phase 0-ის კარიბჭე: auditor მთელ ძრავაზე → ADR-0001…0003, ADR-0005 და PROCESS.md-ის დამტკიცება
4. ნამდვილი პროდუქტი: `/sdlc-intent`
