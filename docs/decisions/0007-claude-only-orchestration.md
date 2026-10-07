---
id: "0007"
title: Claude-only orchestration — roles for Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5
status: proposed
scope: engine
date: 2026-10-08
deciders: owner (Claude-only — 2026-10-07; roles — to choose), Claude (drafted)
supersedes: "0003" and ADR-0006 decision 6 — when this ADR is accepted
superseded_by: —
review_by: after the engine dry run
tags: [models, orchestration, cost]
---
# 0007 — Claude-only orchestration

## Context (კონტექსტი)
მფლობელმა 2026-10-07-ს დაწერა: „პირველი ორკესტრაცია უნდა მოხდეს ამ პროექტის ფარლგებში უშუალოდ claude code ის მოდელებს შორის: claude fable 5.1, opus 5.5, sonnet 5.5, haiku 5.5 (წეღან გამოვიდა). და თავიდნა სხვა მოდელების ჩართულობა სრულად უნდა გამოვრიცხოთ".

ეს ორ ძველ ჩანაწერს ცვლის. ADR-0003-ის „Stage 2" ნაწილი და ADR-0006-ის მე-6 გადაწყვეტილება მეორე ეტაპზე OpenAI-ის მოდელებს (`gpt-6.1-sol`, `gpt-6-astra` Codex plugin-ით) და ღია მოდელებს (DeepSeek V4-Pro, Qwen3-Coder-Next) ითვალისწინებდა. ეს გზა იკეტება. Fable 5.1, რომელიც მეორე ეტაპის გეგმაშიც იყო, Claude-ის მოდელია და რჩება.

ფაქტები 2026-10-07-ის მდგომარეობით. წყაროა [claude-models-2026-10.md](../../sdlc/research/claude-models-2026-10.md); მთავარი რიცხვები ოფიციალურ გვერდებზე ხელახლა გადამოწმდა (models overview, advisor, model-config).

| მოდელი | ID | $ / 1M ტოკენი (input / output) | Anthropic-ის აღწერა |
|---|---|---|---|
| Fable 5.1 | `claude-fable-5-1` | 10 / 50 | რთული მსჯელობა და გრძელი agentic სამუშაო, ან როცა Opus 5.5 მაღალ effort-ზეც არ კმარა |
| Opus 5.5 | `claude-opus-5-5` | 4 / 20 | „start with Claude Opus 5.5 for most workloads"; გრძელი agentic კოდირება |
| Sonnet 5.5 | `claude-sonnet-5-5` | 2 / 10 | სიჩქარისა და ჭკუის საუკეთესო ბალანსი; კარგად შემოსაზღვრული ყოველდღიური ამოცანები |
| Haiku 5.5 | `claude-haiku-5-5` | 0.10 / 0.50 (prompt ≤ 100K) | დიდი მოცულობის სწრაფი ამოცანები; „pairs well with Opus 5.5 and Sonnet 5.5 as a subagent on coding work" |

ოთხივეს 1M კონტექსტი და 128K output აქვს.

- **advisor-ის წყვილები** (მთავარი → დასაშვები მრჩეველი): Sonnet 5.5 → Fable, Opus 5+, Sonnet 5.5; Opus 5.5 → Fable, Opus 5+; Haiku 5.5 → Fable, Opus 4.7+, Sonnet 5+, Haiku 5.5; Fable 5.1 → მხოლოდ Fable 5.1. თუ API წყვილს უარყოფს, advisor უხმაუროდ ითიშება. ქვეაგენტები იმავე advisor-ს იღებენ და წყვილს საკუთარი მოდელით ამოწმებენ.
- **advisor-ის ფასი.** advisor ყოველ გამოძახებაზე მთელ საუბარს თავიდან კითხულობს, ქეშის გარეშე და თავისი ფასით. ამ სესიაში Opus advisor-ის ერთმა ზარმა ≈590K კონტექსტზე ≈ $2.5 დაჯდა (list ფასით); Fable advisor-ით იგივე ზარი ≈ $6.3 იქნებოდა.
- **სარგებლის გაზომვა.** Anthropic-ის გაზომვით, კოდირებაზე Opus 5.5 (`high`) + Fable advisor მარტო Opus-ს მხოლოდ +1.7 პუნქტით სჯობს, ეს ხმაურის ზღვარზეა, ფასი კი ≈2.1-ჯერ მაღალია. მისი რჩევა: ჯერ advisor-ის მოდელი მარტო, დაბალ effort-ზე გაზომე; ეს არის ზღვარი, რომელსაც წყვილმა უნდა აჯობოს.
- **Haiku 5.5-ის ვერსია.** Claude Code v2.1.293 ან უფრო ახალი სჭირდება. ამ Mac-ზე v2.1.292 დგას, ამიტომ `claude update`-მდე `haiku` Haiku 4.5-ს ნიშნავს, `claude-haiku-5-5` კი შეცდომას აბრუნებს.
- **Fable-ზე წვდომა.** Max-ზე და premium seat-ებზე Fable კვირის ლიმიტის 50%-მდე დამატებითი ფასის გარეშე მუშაობს. Pro-ზე და standard seat-ებზე მხოლოდ usage credits-ით იხდება (ცალკე ფული) და ერთჯერად თანხმობას ითხოვს (`/model fable`).
- **ვინ ირჩევს მთავარ მოდელს.** რიგი ასეთია: `/model` (VS Code-ის picker-იც) > `--model` > `ANTHROPIC_MODEL` > settings-ის `model` (პროექტი > მომხმარებელი). `/model` არჩევანს მომხმარებლის ფაილში ინახავს, მაგრამ შემდეგ გაშვებაზე პროექტის ფაილი იმარჯვებს. ნანახია: სესია `e3bc42f4` (`/model`-ის გარეშე) Sonnet 5.5-ზე მუშაობდა; `df3e2417` და `31c2c6fd` Opus 5.5-ზე მუშაობდნენ, `/model`-ის გახსნის შემდეგ.
- **Claude-ის გარეშე გზები ამ Mac-ზე.** Codex plugin (`codex@openai-codex` 1.0.1) ჩართულია, Codex CLI დაყენებული და ავტორიზებულია, ანუ აქტიურია. CodeRabbit plugin ჩართულია, მაგრამ მისი CLI დაყენებული არ არის, ამიტომ უმოქმედოა.

## Options considered (განხილული ვარიანტები)
როლები: მთავარი სესია (არტეფაქტებს და კოდს წერს), advisor (მრჩეველი გადაწყვეტილების მომენტებში), `architect` (ADR-ის ვარიანტები), `auditor` (კარიბჭეები, ეტაპები, `[high-risk]` დავალებები), `verifier` (მტკიცებულების ბრძანებებს უშვებს) და დამხმარე (ძებნა, ფაქტის მოძიება, შეჯამება — ახალი როლი Haiku-სთვის).

| როლი | A — ეკონომიური | B — დამოუკიდებელი მსაჯული (რეკომენდებული) | C — მაქსიმალური |
|---|---|---|---|
| მთავარი სესია | Sonnet 5.5 · high | Sonnet 5.5 · high | Opus 5.5 · medium |
| advisor | Opus 5.5 | Opus 5.5 | Fable 5.1 |
| `architect` | Opus 5.5 · high | Opus 5.5 · high | Fable 5.1 · high |
| `auditor` | Opus 5.5 · high | **Fable 5.1 · high** | Fable 5.1 · high |
| `verifier` | Sonnet 5.5 · medium | Sonnet 5.5 · medium | Sonnet 5.5 · medium |
| დამხმარე | Haiku 5.5 · medium | Haiku 5.5 · medium | Haiku 5.5 · medium |

### A — ეკონომიური (ADR-0003-ის პირველი ეტაპი + Haiku)
- What it is: დღევანდელი პარამეტრები უცვლელად, პლუს Haiku 5.5 დამხმარე სამუშაოსთვის; Fable არ გამოიყენება.
- Pros: ყველაზე იაფია; „Sonnet main + Opus advisor" დოკუმენტირებული წყვილია; Fable-ზე წვდომა არ სჭირდება; მფლობელის გლობალურ პრინციპს ემთხვევა — იაფი მოდელი მუშაობს, ძვირი რჩევას იძლევა.
- Cons: advisor და auditor ერთი მოდელია (Opus 5.5). auditor ამოწმებს ნამუშევარს, რომელსაც მისივე მოდელის რჩევამ მისცა ფორმა, ამიტომ მათი ბრმა წერტილები ემთხვევა. ქვეაგენტები იმავე advisor-ს იღებენ, ამიტომ auditor-ს შეუძლია იმავე Opus advisor-ს მიმართოს, ვისაც ავტორი. დამოუკიდებლობის ნაწილი მაინც რჩება: auditor სუფთა კონტექსტში და სხვა კუთხით მუშაობს (თარგი, ზედა არტეფაქტები, „done"-ის განსაზღვრება).
- Cost (money + learning): ყველაზე დაბალი. advisor-ის ერთი ზარი ≈ $0.5 (100K კონტექსტზე) და ≈ $2.5 (590K-ზე).
- Risk: ყველაზე დაბალი.
- Reversibility: მარტივი — settings და აგენტების `model:` ხაზები.
- Source checked: models overview, advisor, model-config (2026-10-07/08).

### B — დამოუკიდებელი მსაჯული (რეკომენდებული)
- What it is: A, ოღონდ `auditor` Fable 5.1-ზე გადადის.
- Pros: ავტორი (Sonnet), მრჩეველი (Opus) და მსაჯული (Fable) სამი სხვადასხვა მოდელია: ვინც ამოწმებს, იმ მოდელს არ იზიარებს, ვისაც ამოწმებს. Fable-ის auditor Opus advisor-ს ვერ მიიღებს (Fable მხოლოდ Fable-ს იღებს მრჩევლად), ამიტომ მსაჯული ავტორის მრჩეველთანაც გამიჯნულია. ყველაზე ძლიერი მოდელი იქ იხარჯება, სადაც ის პატარა, სუფთა კონტექსტს კითხულობს (არტეფაქტი, ზედა დოკუმენტები, diff), და არა მთელ გაზრდილ საუბარს. მფლობელი კოდს ვერ კითხულობს, ამიტომ მისი მთავარი დაცვა სწორედ auditor-ია.
- Cons: Fable-ზე წვდომა სჭირდება; Pro/standard seat-ზე Fable usage credits-ით იხდება. Anthropic-ის თქმით, Opus 5.5 „performs at the level of Claude Fable 5.1 on most work", ამიტომ ხარისხის მატება შეიძლება მცირე იყოს — მთავარი მოგება დამოუკიდებლობაა.
- Cost (money + learning): A-ზე მეტი მხოლოდ auditor-ის გაშვებებზე. Fable-ის ფასი Opus-ისაზე 2.5-ჯერ მაღალია (10 / 50 და 4 / 20), ქეშიდან წაკითხვა კი შედარებით იაფი აქვს. ამიტომ ერთი შემოწმება დაახლოებით 2–2.5-ჯერ ძვირი გამოვა: თუ Opus-ზე ≈ $1.5 ჯდება, Fable-ზე ≈ $3–3.75. ეს უხეში ვარაუდია; ნამდვილ რიცხვს საცდელი გაშვება გაზომავს.
- Risk: რა ხდება, როცა Fable-ის თანხმობა მიცემული არ არის და ქვეაგენტი Fable-ზეა მიბმული (შეცდომა თუ სხვა მოდელზე გადასვლა), დაუდასტურებელია. საცდელმა გაშვებამ უნდა აჩვენოს `claude-fable-5-1` auditor-ის ტრანსკრიპტში.
- Reversibility: მარტივი — ერთი `model:` ხაზი.
- Source checked: იგივე + optimizing-for-cost-and-intelligence.

### C — მაქსიმალური
- What it is: მთავარი სესია Opus 5.5-ზეა (ყველაზე ახლოს იმასთან, რაც ამ სესიაში ფაქტობრივად მუშაობდა); Fable 5.1 advisor-ია, architect-ი და auditor-ი.
- Pros: Anthropic-ის ნაგულისხმევი რჩევაა („start with Claude Opus 5.5 for most workloads"); Opus 5.5 „delegates to subagents far more effectively and checks its own work"; თითო ნაბიჯის ხარისხი ყველაზე მაღალია.
- Cons: ყველაზე ძვირია: ყოველი ნაბიჯი Opus-ის ფასითაა (Sonnet-ზე ორჯერ ძვირი), Fable advisor-ის ზარი დიდ კონტექსტზე კი ≈ $6 ჯდება. Anthropic-ის გაზომვით, Opus + Fable advisor მარტო Opus-ს მხოლოდ +1.7 პუნქტით სჯობს ≈2.1-ჯერ მეტ ფასად. ეწინააღმდეგება მფლობელის გლობალურ წესს „Opus — ხარჯის მაქს. 20%". advisor და auditor ერთი მოდელია (Fable).
- Cost (money + learning): ყველაზე მაღალი.
- Risk: ხარჯი; Fable-ის თანხმობა.
- Reversibility: მარტივი.

უარყოფილია: Haiku 5.5 მთავარ სესიად — დოკუმენტირებული „Haiku main + Opus advisor" ყველაზე იაფია, მაგრამ მფლობელი კოდს ვერ კითხულობს, ამიტომ მთავარი კოდერი ყველაზე პატარა მოდელი არ უნდა იყოს. Fable 5.1 მთავარ სესიად — ყოველი ნაბიჯი $10 / $50-ად, advisor კი მხოლოდ Fable შეიძლება იყოს.

## Decision (გადაწყვეტილება)
1. **მფლობელმა გადაწყვიტა (2026-10-07):** ძრავის ორკესტრაცია მხოლოდ Claude-ის მოდელებს იყენებს — Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5. OpenAI-ის, ღია და სხვა მომწოდებლის მოდელები გამორიცხულია. ამ ADR-ის დამტკიცებისას ADR-0003 `superseded` ხდება, ADR-0006-ის მე-6 გადაწყვეტილება კი ძალას კარგავს.
2. **როლებს მფლობელი ირჩევს.** რეკომენდაციაა B. სანამ მფლობელი არ აირჩევს, `.claude/settings.json` და `.claude/agents/`-ის `model:` ხაზები არ იცვლება — ანუ დღეს A მოქმედებს, Haiku-ს გარეშე.
3. **Haiku 5.5 — დამხმარე როლი** (ძებნა, ფაქტის მოძიება — ვერსია, ფასი, დოკუმენტაციის გვერდი — და გვერდის ან ჟურნალის შეჯამება): ერთი read-only აგენტი `scout` (`model: claude-haiku-5-5`, `effort: medium`). მისი პასუხი მონაცემია: გადაწყვეტილებამდე მას უფრო ძლიერი მოდელი ამოწმებს. აგენტი `claude update`-ის (≥ v2.1.293) შემდეგ იქმნება; განახლება დაყენებაა და მფლობელის „კი"-ს ითხოვს.
4. **Claude-ის გარეშე გზების ჩაკეტვა ამ რეპოში** (settings-ის ცვლილებაა, მფლობელის „კი" სჭირდება): `.claude/settings.json`-ში `"enabledPlugins": {"codex@openai-codex": false, "coderabbit@claude-plugins-official": false}`. ეს ყველა მონაწილეზე მოქმედებს და მფლობელს ამ plugin-ებს სხვა პროექტებისთვის უნარჩუნებს. ჯობნის თუ არა პროექტის `false` მომხმარებლის `true`-ს, ცოცხლად უნდა შემოწმდეს (დაუდასტურებელია). ალტერნატივაა Codex-ის მთლიანად წაშლა Mac-იდან.

## Rationale (რატომ)
B-ს მთავარი არგუმენტი გამიჯნული მოვალეობებია (separation of duties), რომელზეც ძრავა დგას („the agent that wrote something never audits it"). B-ში ის სამ სხვადასხვა მოდელს ეყრდნობა, ყველაზე ძვირი მოდელი კი ყველაზე იაფ ადგილზე იხარჯება. advisor ყოველ ზარზე მთელ საუბარს ქეშის გარეშე კითხულობს, ამიტომ Fable advisor-ად ყველაზე ძვირი იქნებოდა; auditor კი სუფთა, პატარა კონტექსტში მუშაობს. მეორე არგუმენტი Anthropic-ის გაზომვაა: ძვირი advisor თავისთავად არ ანაზღაურდება. ამიტომ advisor Opus რჩება, CLAUDE.md მას მხოლოდ სამ მომენტში იძახებს, და სანამ რამე გაძვირდება, საცდელი გაშვება ნამდვილ ხარჯს გაზომავს.

## Consequences (შედეგები)
- Positive: ერთი მომწოდებელი — ერთი დოკუმენტაცია, ერთი ფასები და ერთი უსაფრთხოების წესები; კოდი სხვა კომპანიის სერვერზე არ მიდის; თანამშრომლისთვის გამართვა მარტივდება.
- Negative: სხვა მომწოდებლის დამოუკიდებელ თვალს ვკარგავთ — ყველა შემმოწმებელი ერთ ოჯახს ეკუთვნის. ამას ამცირებს მანქანური შემოწმებები (`check_structure.py`, hook-ების წვრთნა, ტესტები), რომლებიც დამოუკიდებლობის ყველაზე ძლიერ ფორმად რჩება.
- What becomes harder: არაფერი შეუქცევადი; სხვა მომწოდებლის მოდელი მომავალში მხოლოდ ახალი ADR-ით დაბრუნდება.
- დამტკიცებისას იმავე ცვლილებაში იცვლება: ADR-0003 → `status: superseded`, `superseded_by: "0007"`; ADR-0006-ის მე-6 პუნქტს შენიშვნა ემატება; PROCESS.md-ის მეორე ეტაპის სტრიქონები და CLAUDE.md-ის „Models" სექცია (ერთნაირად); README.md-ის მომავლის აბზაცი; `tasks/todo.md`-ის Stage-2 სტრიქონი; `sdlc/design/orchestration-and-loop.md` §2 და §7; `memory/now.md`; `sdlc/research/models-gpu-graphs.md`-ს თავში ემატება „ჩაანაცვლა ADR-0007-მა" (ისტორიად რჩება); არჩეული ვარიანტის მიხედვით — `.claude/settings.json`, `.claude/agents/*.md` და `sdlc/checks/check_structure.py`-ის `AGENT_MODELS` სია (დღეს მხოლოდ `claude-opus-5-5`-სა და `claude-sonnet-5-5`-ს უშვებს, ამიტომ Fable-ზე ან Haiku-ზე მიბმული აგენტი მის გარეშე შემოწმებას ჩააგდებს).
- `AGENTS.md` რჩება: ის თანამშრომლების ხელსაწყოებს არეგულირებს და არა ძრავის ორკესტრაციას.

## Verification (როგორ შევამოწმებთ)
საცდელ გაშვებაზე (ახალი სესია, `/model`-ის გარეშე): (1) `/status` არჩეული ვარიანტის მთავარ მოდელს აჩვენებს; (2) გაშვებისას advisor-ის შეტყობინება ჩანს; (3) ტრანსკრიპტის `usage.iterations`-ში `advisor_message` არჩეულ advisor-ს ასახელებს; (4) `auditor`-ისა და `verifier`-ის ტრანსკრიპტები მათ მიბმულ მოდელებს აჩვენებს (`/tasks`); (5) თუ მე-4 პუნქტი ამოქმედდა, ამ რეპოში აგენტების სიაში `codex:codex-rescue` აღარ ჩანს. დღეს არც ერთი მათგანი მანქანური შემოწმება არ არის, ტრანსკრიპტიდან ხელით იკითხება. საცდელი გაშვების შემდეგ `agent_report.py`-ში მოდელის შემოწმების დამატება კანდიდატია.

## Links
- [sdlc/research/claude-models-2026-10.md](../../sdlc/research/claude-models-2026-10.md)
- [sdlc/research/anthropic-guidance-2026-10.md](../../sdlc/research/anthropic-guidance-2026-10.md)
- [ADR-0003](0003-model-orchestration-phase-1.md), [ADR-0006](0006-engine-v2.md)
- https://platform.claude.com/docs/en/models/overview
- https://code.claude.com/docs/en/advisor
- https://code.claude.com/docs/en/model-config
- https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence
