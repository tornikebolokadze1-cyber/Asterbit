# Project Progress — პროექტის პროგრესი

> ახლდება ყოველი ეტაპის, კარიბჭისა და milestone-ის ბოლოს და სესიის დასაწყისში იკითხება, რომ კონტექსტი არ დაიკარგოს.
> ჟურნალი მხოლოდ ივსება: ძველი ჩანაწერები არ იცვლება. ფაილების როლები: [PROCESS.md](PROCESS.md) §4.

## Current State (მიმდინარე მდგომარეობა)
- **Phase:** 0 — Engine setup — IN PROGRESS (harness v0 `main`-შია — PR #2; ძრავა v2-ის კვლევა დასრულდა, პაკეტები მფლობელის არჩევანს ელოდება)
- **Branch:** `engine/v2` (`main`-ში PR-ებით შევა) · **GitHub:** private repo `tornikebolokadze1-cyber/Asterbit` · **გუნდი:** მფლობელი + თანამშრომელი lashavamleti (წერის უფლება, მოწვევა მიღებულია)
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
- PR #2 (`engine/v1` → `main`): CI მწვანეა — 7 ნაბიჯი, მათ შორის „უმოქმედო" hook-ებით DEAD და gitleaks (https://github.com/tornikebolokadze1-cyber/Asterbit/actions/runs/37601321945). ცოცხალი გამოცდები საბოლოო hook-ზე გამეორდა და გავიდა
- გზად: lashavamleti-მ მოწვევა მიიღო (2026-10-07, GitHub API: role `write`)
- PR #2 `main`-ში გაერთიანდა (merge commit `c934e3b`)

### 2026-10-07 — Phase 0.8: ძრავა v2 — კვლევა (branch `engine/v2`)
- მფლობელმა თავდაპირველი პრომპტი ხელახლა გაგზავნა და სთხოვა, ძრავში ყველაფერი დაემატოს, რაც აკლია. რეპოებიდან აღებული ფრაგმენტები კი ჯერ მასთან უნდა შეთანხმდეს
- მფლობელის გადაწყვეტილებები: შეკუმშვა 65%-ზე რჩება (ADR-0004 უცვლელია, თუმცა პრომპტში 70% ეწერა); PRD და TRD ცალკე ფაილებია; Sonnet↔Opus ციკლი ეტაპის ბოლოს და რისკიან დავალებებზე ტრიალებს
- ცხრა რეპო და AI Pulse კოლექცია კოდის დონეზე შეისწავლა ორმა აგენტმა, ვებ-კვლევა კი მესამემ ჩაატარა → `sdlc/research/repo-study.md` (18 ფრაგმენტი), `sdlc/research/models-gpu-graphs.md`, `sdlc/research/engine-v2-gaps.md` (შედარება და პაკეტები P1–P6) — commit `b6c393c`; `check_structure.py`: 283 შემოწმება, PASS, exit 0
- გზად აღმოჩნდა: ADR-0003 და სხვა ოთხი ფაილი არარსებულ მოდელს წერს („ChatGPT 6.1 Astra"; რეალური ID-ებია `gpt-6-astra` და `gpt-6.1-sol`); ADR-0004-ის Verification ამბობს „None of these exist yet", თუმცა `now.md ≤120` შემოწმება უკვე არსებობს; Graphify კოდისთვის ADR-0004-ის არჩევანს („მხოლოდ Obsidian") ეხება, ამიტომ ცალკე კითხვაა
- მრჩევლის (Opus 5.5) შენიშვნით შეთავაზება შესწორდა: კონტექსტის monitor PostToolUse-ზე მუშაობს და ზღვარს settings-იდან კითხულობს; ჟურნალი `.claude/logs/`-შია; გაკვეთილების ზღვარი 2 რჩება; F2 „ან მფლობელის მკაფიო მოთხოვნას" მოიცავს; პაკეტები ცალკე ეტაპებად აიწყობა, სამი PR-ით

## In Progress (მიმდინარე)
- ძრავა v2: მფლობელი ირჩევს პაკეტებს (`sdlc/research/engine-v2-gaps.md` §2) და კოდის გრაფის საკითხს (§3)

## Next Steps (შემდეგი ნაბიჯები)
1. ძრავა v2-ის არჩეული პაკეტები ცალკე ეტაპებად: P1+P2 (PRD/TRD, ციკლი) → P3+P4 (მეხსიერება, თვითგანვითარება) → P5+P6 (კარიბჭეები და ჟურნალი, მეორე ეტაპის დოკუმენტები); თითოეულს თავისი შემოწმება, აუდიტი და PR
2. ნამდვილი `/compact`-ით მეხსიერების hook-ის გამოცდა (`memory/episodic/handoffs/`) — P3-ის ნაწილი
3. ძრავის საცდელი გაშვება ახალ სესიაში: ხარჯების კალკულატორი (ვებგვერდი), ეტაპები 1–6, branch `dryrun/expense-calculator` (`main`-ში არ შევა), კარიბჭეები `DRY-RUN` ნიშნით (მფლობელის გადაწყვეტილება 2026-10-07); ნაპოვნი ხარვეზების გასწორება
4. Phase 0-ის კარიბჭე: auditor მთელ ძრავაზე → ADR-0001…0003, ADR-0005, ADR-0006 და PROCESS.md-ის დამტკიცება
5. ნამდვილი პროდუქტი: `/sdlc-intent`
