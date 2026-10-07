# Project Progress — პროექტის პროგრესი

> ახლდება ყოველი ეტაპის, კარიბჭისა და milestone-ის ბოლოს და სესიის დასაწყისში იკითხება, რომ კონტექსტი არ დაიკარგოს.
> ჟურნალი მხოლოდ ივსება: ძველი ჩანაწერები არ იცვლება. ფაილების როლები: [PROCESS.md](PROCESS.md) §4.

## Current State (მიმდინარე მდგომარეობა)
- **Phase:** 0 — Engine setup — IN PROGRESS (ძრავა v1 და v2 `main`-შია — PR #2, #3, #4; `AGENTS.md` და `env.example` — PR #5)
- **Branch:** `main` (`d1b66c7`); `engine/agents-env` — PR #5 · **GitHub:** private repo `tornikebolokadze1-cyber/Asterbit` · **გუნდი:** მფლობელი + თანამშრომელი lashavamleti (წერის უფლება, მოწვევა მიღებულია)
- **Decisions:** ADR-0004 accepted; ADR-0001…0003, ADR-0005 და ADR-0006 proposed
- **Checks (2026-10-07, `engine/v2-runtime` = `main`-ის v2 ნაწილი, `sdlc/checks/`):** სტრუქტურა — 329 შემოწმება, PASS (77 ფაილი); წვრთნა — 131 შემთხვევა, ARMED (50 CAUGHT, 42 WORKS, 32 PASSED, 7 ASKED); „უმოქმედო" hook-ებით — DEAD (exit 1)
- **Not built yet:** ნამდვილი `/compact`-ით hook-ის გამოცდა (მხოლოდ მფლობელს შეუძლია გაშვება); ძრავის საცდელი გაშვება

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

### 2026-10-07 — Phase 0.9: ძრავა v2 — P1 (PRD/TRD) და P2 (Sonnet↔Opus ციკლი), branch `engine/v2`
- მფლობელმა ექვსივე პაკეტი აირჩია; კოდის გრაფი — კოდის გაჩენამდე გადადებულია ([ADR-0006](docs/decisions/0006-engine-v2.md), proposed)
- P1: PRD და TRD თარგები, Phase 2 = PRD → ADR-ები → TRD, „ცივი მკითხველის" ტესტი, `[NEEDS CLARIFICATION]` ნიშანი და მისი შემოწმება დამტკიცებულ დოკუმენტებში, მოთხოვნიდან დავალებამდე კვალის შემოწმება
- P2: ციკლი შემოწმება → გასწორება → შემოწმება → გასწორება → ბოლო შემოწმება → მფლობელი; რაუნდებს `sdlc/checks/review_rounds.py` ითვლის ჟურნალში `tasks/review-log.jsonl`
- ციკლი პირველად თავად ამ ცვლილებაზე გაეშვა (loop `ENG-v2-P1P2`): review 1 — FAIL (1 HIGH, 6 MEDIUM: მაგ., თარგების დამხმარე ტექსტი ახალ შემოწმებას აჩერებდა) → fix 1 `26edffd` → review 2 — 0 HIGH, 1 MEDIUM → fix 2 `e17d4cc` → review 3 — 0 HIGH, 0 MEDIUM, 2 LOW → `status` exit 0. LOW-ები runtime branch-ზე სწორდება
- შემოწმებები (`e17d4cc`): სტრუქტურა PASS (exit 0); წვრთნა 106 შემთხვევა ARMED (exit 0, ზედიზედ რამდენიმე გაშვება); „უმოქმედო" hook-ებით DEAD (exit 1); ხუთი ცალკეული mutant ასლში — თითოეული დაიჭირა (exit 1)
- გზად აღმოჩნდა: ძველი წვრთნის შემთხვევა (`commit_secrets`, gitleaks-ის გასაღები) 4 გაშვებიდან ერთხელ ჩავარდა — გადადებულია `tasks/todo.md`-ში; P3–P5-ის ნახევრად მზა სამუშაო ცალკე branch-ზე `engine/v2-runtime` გადავიდა, რომ ციკლს მხოლოდ გასწორება შეეხედა

### 2026-10-07 — Phase 0.10: ძრავა v2 — P3–P6, branch `engine/v2-runtime`
- P3 (მეხსიერება v2): `context_monitor.py` (PostToolUse) ზომავს კონტექსტს სესიის ჩანაწერიდან და შეკუმშვამდე 100 ათასი token-ით ადრე handoff-ის ჩაწერას ითხოვს; ზღვარს `autoCompactWindow`-იდან კითხულობს. `untrusted.py` მეხსიერებას შემთხვევითი ნიშნით (nonce) ღობავს და „ინსტრუქციის ჩანაცვლების" ნიმუშებს ეძებს; handoff-ი `injection_flags` ველს იღებს. `memory_hygiene.py` (ძველი/გადაბერილი ფაილები, exit 0/3/2); მეხსიერების ფენების ცხრილი `memory/README.md`-ში; `/sdlc-wrap` ნაბიჯები 4 და 7
- P4 (თვითგანვითარება): `tasks/lessons.md`-ს „Kind" სვეტი დაემატა; `lessons_graduate.py` ორ სხვადასხვა დღეს განმეორებულ გაკვეთილს ეძებს და შემოწმების აწყობას სთავაზობს — რეალურ ფაილზე უკვე იპოვა 2026-10-06-ის `git add -A` გაკვეთილი
- P5 (კარიბჭეები და ჟურნალი): `run_gates.py` (`docs/gates.json` Phase 7a-ში შეიქმნება; PASS / FAIL / INCONCLUSIVE ცალ-ცალკე, „0 ტესტი" მწვანე არასდროსაა); `event_log.py` (PostToolUse / PostToolUseFailure → `.claude/logs/`, git-ში არ შედის); `agent_report.py`
- P6 (მეორე ეტაპის ჩანაწერები, არაფერი ჩართულა): OpenAI-ის სწორი ID-ები `gpt-6-astra` / `gpt-6.1-sol`; ღია მოდელი API-ით; GPU — RunPod, სათადარიგოდ Hetzner (`sdlc/design/orchestration-and-loop.md` §7)
- ყველა კარიბჭის skill ახლა საერთო ციკლს მიუთითებს (loop id `gate-<phase>`); წვრთნის ასლები ახალ git საცავს ქმნის, ამიტომ worktree-დანაც ეშვება
- ცოცხალი მტკიცებულება ამ სესიიდან: `event_log` 6 ხაზი ჩაწერა, მათ შორის auditor ქვე-აგენტი; `context_monitor`-მა ნამდვილი ჩანაწერი გაზომა (<55%)
- ENG-v2-P1P2-ის ბოლო ორი LOW აქ გასწორდა: `[NEEDS CLARIFICATION: <question>]` გამონაკლისია მხოლოდ `>` ხაზზე, შემოწმება ასოების ზომას აღარ უყურებს (ორი ახალი წვრთნის შემთხვევა); ADR-0006-ში რიცხვები დაზუსტდა
- შემოწმებები: სტრუქტურა 328, PASS (exit 0); წვრთნა 126 შემთხვევა, ARMED (exit 0); „უმოქმედო" hook-ებით DEAD (exit 1)
- გზად აღმოჩნდა: `commit_secrets.py` სესიის საქაღალდეს ამოწმებს და არა იმას, სადაც ბრძანება `cd`-ით ან `git -C`-ით გადადის — worktree-დან გაკეთებული commit-ები ხელით შემოწმდა (gitleaks, built-in ნიმუშები: არაფერი). გასწორება hook-ს ცვლის, ამიტომ მფლობელის „კი" სჭირდება → `tasks/todo.md`
- აუდიტის ციკლი `ENG-v2-P3P6` PR #4-ზე ეშვება
- ციკლი `ENG-v2-P3P6`: review 1 — 0 HIGH, 6 MEDIUM, 8 LOW (მაგ., კონტექსტის მზომი ქვე-აგენტებზეც ეშვებოდა; ჩატვირთვისას handoff-ში შენახულ „ინექციის ნიშანს" ენდობოდა; ჟურნალი მხოლოდ ცნობილი სერვისების გასაღებებს ფარავდა) → fix 1 `3b077a7` → review 2 — 0 HIGH, 2 MEDIUM, 4 LOW → fix 2 `fc4f48d`. მესამე, ბოლო შემოწმება არ ჩატარებულა — მფლობელმა ციკლი შეაჩერა (ქვემოთ). fix 2 მხოლოდ მანქანური შემოწმებებით დადასტურდა: სტრუქტურა 329 PASS, წვრთნა 131 ARMED, „უმოქმედო" hook-ებით DEAD, 3 mutant დაიჭირა, CI. auditor-ის ერთი შემოწმება 7–12 წუთს გრძელდებოდა
- მფლობელის გადაწყვეტილება (2026-10-07): ძრავი Phase 0-ის კარიბჭემდე მსუბუქად შენდება — აუდიტორის ციკლის, mutant-ებისა და ციკლის ჟურნალის გარეშე; რჩება უსაფრთხოების წესები, `check_structure.py`, hook-ის ცვლილებისას წვრთნა და CI. ძრავით გაშვებული სამუშაო (საცდელი გაშვება, პროდუქტი) სრულ ციკლს იყენებს → CLAUDE.md, PROCESS.md, ADR-0006, `tasks/lessons.md`
- გზად: დისკი გაივსო (117 MB დარჩა) და სესიის დროებითი საქაღალდე გასუფთავდა — worktree და fix 1-ის შეუნახავი ნამუშევარი დაიკარგა. commit-ები GitHub-ზე იყო, ამიტომ worktree თავიდან შეიქმნა `~/Asterbit-runtime`-ში და review 1-ის ჩანაწერი ხელახლა ჩაიწერა. ამ ჩანაწერში სტრუქტურის რიცხვი 328 ერთით ნაკლებია — now.md-ის ბმულის შემდეგ 329-ია

### 2026-10-07 — Phase 0.11: ძრავა v2 `main`-შია; `AGENTS.md` და `env.example` (branch `engine/agents-env`)
- მფლობელის „კი"-ს შემდეგ PR #3 (`a0414c8`) და PR #4 (`d1b66c7`) `main`-ში გაერთიანდა; ორივეზე CI მწვანე იყო, `main`-ზე `check_structure.py` — 330 შემოწმება, PASS. ADR-ები `proposed` რჩება Phase 0-ის კარიბჭემდე
- მფლობელის საქაღალდე `~/Asterbit` `main`-ზე გადავიდა; `settings.json`-ის ორი ცარიელი ხაზი (Claude-ს არ ჩაუწერია) `git stash`-ში გადაიდო და არ წაშლილა. გადასვლისთანავე ახალი hook-ები ამ სესიაში ჩაირთო — `.claude/logs/`-ში მოვლენების ჟურნალი და კონტექსტის მზომის ფაილი გაჩნდა
- მფლობელმა იპოვა ორი ხარვეზი: არც `AGENTS.md` იყო (წესები Codex / GPT, Cursor, Kilo-სთვის — მათ `CLAUDE.md` არ წაუკითხავთ) და არც საიდუმლო პარამეტრების ნიმუში. ორივე დაემატა; `AGENTS.md` `check_structure.py`-ის სავალდებულო ფაილებშია
- ნიმუში `env.example` ჰქვია და არა `.env.example`: პროექტის დაცვის წესი `Read(./.env.*)` Claude-ს `.env.example`-ის ჩაწერასაც უკრძალავს. მფლობელმა სახელის შეცვლა აირჩია, დაცვის წესი უცვლელია

## In Progress (მიმდინარე)
- PR #5 (`AGENTS.md`, `env.example`) მფლობელის გაერთიანებას ელოდება

## Next Steps (შემდეგი ნაბიჯები)
1. მფლობელი: PR #5 `main`-ში; გადაწყვეტილება `commit_secrets`-ის ხარვეზზე (`tasks/todo.md`); ზედმეტი სამუშაო ასლის `~/Asterbit-runtime` წაშლა (მფლობელის თანხმობით)
2. ნამდვილი `/compact`-ით მეხსიერების hook-ის გამოცდა (`memory/episodic/handoffs/`) — მფლობელი უშვებს `/compact`-ს, Claude ამოწმებს შედეგს
3. ძრავის საცდელი გაშვება ახალ სესიაში: ხარჯების კალკულატორი (ვებგვერდი), ეტაპები 1–6, branch `dryrun/expense-calculator` (`main`-ში არ შევა), კარიბჭეები `DRY-RUN` ნიშნით (მფლობელის გადაწყვეტილება 2026-10-07); ნაპოვნი ხარვეზების გასწორება
4. Phase 0-ის კარიბჭე: auditor მთელ ძრავაზე → ADR-0001…0003, ADR-0005, ADR-0006 და PROCESS.md-ის დამტკიცება
5. ნამდვილი პროდუქტი: `/sdlc-intent`
