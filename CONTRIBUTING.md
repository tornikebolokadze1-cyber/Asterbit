# CONTRIBUTING — როგორ ვიმუშაოთ ამ პროექტზე

> **ვისთვის:** ყველასთვის, ვინც პროექტს პირველად ჩამოტვირთავს და მასში ცვლილებას შეიტანს.
> **გუნდი:** მფლობელი — Tornike ([@tornikebolokadze1-cyber](https://github.com/tornikebolokadze1-cyber)) · თანამშრომელი — [@lashavamleti](https://github.com/lashavamleti)

## 1. რა არის ეს პროექტი

ამ რეპოზიტორიაში (repository — პროექტის საქაღალდე, რომლის ისტორიასაც git ინახავს) ორი რამ ცხოვრობს. პირველი არის ძრავა: Claude Code-თან მუშაობის ეტაპობრივი სისტემა (SDLC), რომელშიც შედის წესები, ეტაპების ბრძანებები, დამხმარე აგენტები, თარგები და მეხსიერება. მეორე იქნება პროდუქტი, რომელსაც ამ ძრავით ავაშენებთ; ის ჯერ არ არჩეულა. თითქმის ყველა ფაილი ჩვეულებრივი ტექსტია (markdown), ამიტომ ნებისმიერ რედაქტორში იკითხება.

პირველად წაიკითხე ამ თანმიმდევრობით: [README.md](README.md) (რა არის და სად რა დევს) → [PROCESS.md](PROCESS.md) (როგორ ვმუშაობთ და ვინ რას წყვეტს) → [docs/FILES.md](docs/FILES.md) (თითოეული ფაილის ახსნა) → [PROGRESS.md](PROGRESS.md) (სად ვართ ახლა).

## 2. რა გჭირდება

აუცილებელი:

- მოწვევის მიღება: https://github.com/tornikebolokadze1-cyber/Asterbit/invitations (ან ბმული ელფოსტიდან).
- git.
- Claude Code — VS Code-ის გაფართოება ან ტერმინალის ვერსია. Claude-ის ანგარიშზე Opus 5.5 და Sonnet 5.5 უნდა იყოს ხელმისაწვდომი, რადგან პროექტის აგენტები ამ მოდელებს იყენებენ.
- Python 3 (3.9 ან უფრო ახალი), ბრძანებით `python3`. მასზე მუშაობს პროექტის დამცავი hook-ები. macOS-სა და Linux-ს ის უკვე აქვს; Windows-ზე გამოიყენე Git Bash ან WSL, Python-ით. თუ `python3` არ არის, hook-ები ვერ ჩაირთვება: Claude Code hook-ის შეცდომას აჩვენებს და დაცვა შენს კომპიუტერზე გამორთულია — ასეთ შემთხვევაში მფლობელს შეატყობინე.

სურვილისამებრ:

- GitHub CLI (`gh`) — PR-ების (pull request — ცვლილების შემოთავაზება GitHub-ზე) ტერმინალიდან შესაქმნელად.
- Superpowers plugin — მეთოდების ბიბლიოთეკა, რომელსაც ჩვენი ბრძანებები ტექნიკად ასახელებს. მის გარეშეც ყველაფერი მუშაობს. Claude Code-ში: `/plugin install superpowers@claude-plugins-official` (თუ marketplace ვერ იპოვა, ჯერ `/plugin marketplace add anthropics/claude-plugins-official`).
- gitleaks — საიდუმლოებების შემოწმება commit-მდე (იხ. §6).
- Obsidian — `docs/`-ისა და `memory/`-ის ბმულების გრაფად სანახავად; საქაღალდე უკვე Obsidian-ის vault-ია.

## 3. ჩამოტვირთვა და გახსნა

```bash
git clone https://github.com/tornikebolokadze1-cyber/Asterbit.git
cd Asterbit
```

საქაღალდე VS Code-ში გახსენი და ჩართე Claude Code. როცა Claude Code გკითხავს, ენდობი თუ არა ამ საქაღალდეს, უპასუხე „კი". ასე ჩაიტვირთება პროექტის წესები (`CLAUDE.md`), ბრძანებები (`.claude/skills/`) და აგენტები (`.claude/agents/`). შესამოწმებლად ჩაწერე `/sdlc-status` — Claude გეტყვის მიმდინარე ეტაპს და შემდეგ ნაბიჯს.

## 4. როგორ შევიტანოთ ცვლილება

`main` პროექტის მთავარი ვერსიაა. მასში პირდაპირ არავინ წერს — არც მფლობელი და არც Claude. ყოველი ცვლილება ასე მიდის:

```bash
git switch main && git pull          # 1. უახლესი ვერსია
git switch -c docs/my-change         # 2. ახალი branch, ლათინური სახელით (feat/, fix/, docs/, chore/)
# 3. ცვლილება — ხელით ან Claude-ით
git add README.md docs/FILES.md      # 4. ფაილები სახელით, არა `git add -A`
git commit -m "docs: რა შეიცვალა"
git push -u origin docs/my-change    # 5. ატვირთვა
gh pr create --fill                  # 6. PR (ან GitHub-ის საიტიდან)
```

`git add -A`-ს იმიტომ ვერიდებით, რომ ის plugin-ების დროებით ფაილებსაც იჭერს; ერთხელ ასე უკვე მოხდა (იხ. [tasks/lessons.md](tasks/lessons.md)).

PR-ს მფლობელი განიხილავს და `main`-ში თვითონ აერთიანებს. ტექნიკურად გაერთიანება შენც შეგიძლია, რადგან GitHub-ის უფასო გეგმაზე private რეპოში `main`-ის დაცვა (branch protection) არ ირთვება. ამიტომ ეს წესი ჩვენს შეთანხმებაზე დგას და არა ტექნიკურ აკრძალვაზე.

## 5. Claude Code ამ პროექტში

- ეტაპების ბრძანებები: `/sdlc-intent`, `/sdlc-architecture`, `/sdlc-harness`, `/sdlc-spec`, `/sdlc-plan`, `/sdlc-build`, `/sdlc-evaluate`, `/sdlc-secure`, `/sdlc-observe`. ნებისმიერ დროს — `/sdlc-status`, სესიის ბოლოს — `/sdlc-wrap`.
- **კარიბჭეებს (gate — ეტაპის დასრულების დამტკიცება) მხოლოდ მფლობელი ამტკიცებს.** შენთან მუშაობისას Claude ეტაპის შედეგს და PR-ს მოამზადებს, დამტკიცებას კი მფლობელს დაუტოვებს.
- `PROGRESS.md`, `memory/` და `tasks/` საერთო ჟურნალებია. მუშაობის დაწყებამდე `git pull` გაუშვი, რომ ორი ადამიანის ჩანაწერები ერთმანეთს არ შეეჯახოს.
- ფაილის დამატების, გადატანის ან სახელის შეცვლისას იმავე PR-ში განაახლე [docs/FILES.md](docs/FILES.md).
- ძრავის ფაილების შეცვლის შემდეგ გაუშვი `python3 sdlc/checks/check_structure.py` (უნდა თქვას PASS), hook-ის შეცვლის შემდეგ კი `python3 sdlc/checks/drill_hooks.py` (უნდა თქვას ARMED).
- სესიის დასაწყისში Claude-ს პროექტის მდგომარეობა (`memory/now.md`, ბოლო handoff) ავტომატურად მიეწოდება, შეკუმშვისას კი handoff ავტომატურად ინახება `memory/episodic/handoffs/`-ში.
- შენი პირადი ფაილები git-ში არ მოხვდება: `.claude/settings.local.json`, `.claude/handoff-*.md`, `.omc/` და Obsidian-ის ფანჯრების მდგომარეობა `.gitignore`-შია.

## 6. უსაფრთხოება — რა გვაქვს და რა ჯერ არა

პროექტს საკუთარი ავტომატური დაცვა აქვს, რომელიც რეპოსთან ერთად ჩამოდის: `.claude/settings.json` (Claude-ის უფლებები) და `.claude/hooks/` (hook-ები — ავტომატური ჩამრთველები, რომლებიც სახიფათო მოქმედებას ბლოკავს; [ADR-0005](docs/decisions/0005-harness-v0.md)). Claude ფაილებს რეპოში თავისით ასწორებს და სამუშაო branch-ს თავისით ტვირთავს, მაგრამ გკითხავს პროგრამის დაყენებამდე, ინტერნეტიდან ჩამოტვირთვამდე, settings-ის, hook-ების ან CI-ის შეცვლამდე და `main`-ში გაერთიანებამდე. hook-ები ბლოკავს: `rm -rf`-ს, `git reset --hard`-ს, `git clean -f`-ს, force-push-ს, `main`-ში push-ს, `--no-verify`-ს, საიდუმლო ფაილების ჩაწერას და ქსელით გაგზავნას; შეუნახავი სამუშაოს ან branch-ის წამშლელ ბრძანებებზე (`switch -f`, `restore`, `branch -D`, `stash drop`) ჯერ გკითხავს; commit-მდე staged ცვლილებებს საიდუმლოებებზე ამოწმებს. ამიტომ Claude ჯერ `git add`-ს უშვებს და მერე, ცალკე, `git commit`-ს. auditor, verifier და architect ფაილებს ვერ ცვლიან. თუ hook რამეს დაბლოკავს, Claude აგიხსნის, რატომ — hook-ს გვერდს ნუ აუვლი. ყოველ PR-ზე GitHub იგივე შემოწმებებს თავადაც უშვებს (CI) და მწვანე ან წითელ ნიშანს აჩვენებს.

hook-ები Claude-ის მოქმედებებს იცავს. თუ ბრძანებას ხელით უშვებ, სამი წესი შენზეა:

- საიდუმლოება (პაროლი, API გასაღები, `.env`) git-ში არასდროს. `.gitignore` ძირითად შემთხვევებს ფარავს, ხელით commit-მდე კი staged ფაილები ასე შეგიძლია შეამოწმო (gitleaks v8.19 ან უფრო ახალი; exit 0 — სუფთაა, exit 1 — რაღაც იპოვა):

  ```bash
  gitleaks git --pre-commit --staged --redact
  ```

- force-push, უკვე ატვირთული ისტორიის გადაწერა და დესტრუქციული ბრძანებები (`rm -rf`, `git reset --hard`, `git clean -f`) აკრძალულია.
- ფაილს Claude მხოლოდ შენი თანხმობით წაშლის; `main`-ში წაშლა მხოლოდ მფლობელის მიერ დამტკიცებული PR-ით შედის.

## 7. კითხვები

თუ რამე გაუგებარია ან ორი ფაილი ერთმანეთს ეწინააღმდეგება, გახსენი GitHub issue ან პირდაპირ მიწერე მფლობელს.
