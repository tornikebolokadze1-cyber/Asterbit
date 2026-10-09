# QA Chapter — workspace Asterbit-ში

> **როლი:** ცალკე app/workspace ძრავის გვერდით. ძრავა (`sdlc/`, `.claude/skills/sdlc-*`, hooks, root `docs/`) **არ იცვლება** ამ საქაღალდიდან.
> **ვისთვის:** QA Chapter Lead და Chapter-ის წევრები; ცვლილება collaborator branch-ით და PR-ით მიდის, კარიბჭეებს მფლობელი ამტკიცებს.

## რა არის ეს

ხარისხის **გადაწყვეტილების** workspace — არა მანუალური QA პროცესის 1:1 ასლი AI-ში. მიზანი: რისკის სიგნალი, შემოწმებადი კონტრაქტები, ადამიანის კარიბჭეები და სწავლა ინციდენტიდან. პრინციპები: [docs/principles.md](docs/principles.md). ჩანაფიქრის draft: [docs/intent.md](docs/intent.md).

## საზღვრები (apps → platform)

| შეიძლება | არ შეიძლება |
|---|---|
| ძრავის თარგებისა და gate/eval იდეების **გამოყენება** | ძრავის skill-ების, hooks-ის ან `CLAUDE.md`-ის შეცვლა ამ workspace-იდან |
| საკუთარი docs / tasks / memory / knowledge | root `docs/intent.md`-ის ან root `docs/sdlc-state.md`-ის გადაწერა |
| მოგვიანებით დამატებითი `.claude/skills/qa-*` (დამატება, არა `sdlc-*`-ის ჩანაცვლება) | პროდუქტის კოდი, სანამ ამ workspace-ის გეგმა და (საჭიროებისას) მფლობელის promote არ დამტკიცდება |

**ორი „სად ვართ":**

- root [`docs/sdlc-state.md`](../../docs/sdlc-state.md) — **მხოლოდ ძრავა** (Phase 0…).
- [`docs/sdlc-state.md`](docs/sdlc-state.md) — **მხოლოდ ეს QA workspace**.

თუ მფლობელი ერთხელ იტყვის „QA Chapter = Asterbit-ის პროდუქტი", intent აქედან root Phase 1-ზე **ADR-ით** გადმოდის (promote) — არა ჩუმად.

## სტრუქტურა

```text
apps/qa-chapter/
├── README.md                 ← ეს ფაილი
├── docs/
│   ├── principles.md         ← ხარისხის მოდელი
│   ├── intent.md             ← ჩანაფიქრი (draft)
│   └── sdlc-state.md         ← ამ workspace-ის ფაზები
├── tasks/todo.md
├── memory/now.md
└── knowledge/                ← რისკები, ინციდენტები, კონტრაქტები (მოგვიანებით)
```

## შემდეგი ნაბიჯი

1. წაიკითხე [docs/principles.md](docs/principles.md) და შეავსე [docs/intent.md](docs/intent.md)-ის ღია კითხვები Chapter Lead-თან.
2. ინსტრუმენტები (Jira, TestRail…) და არსებული SOP — მხოლოდ მას შემდეგ, რაც პრინციპები დამტკიცდება; მათ SOP-ს არ ვაკოპირებთ 1:1.
3. `qa-*` skill-ები და ცოდნის შევსება — ცალკე PR-ებით, ძრავის უცვლელად.
