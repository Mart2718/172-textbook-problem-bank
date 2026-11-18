# Roadmap

Everything below draws on the same bank: templates that compute their own answers, tagged by outcome and item type.

## Architecture: one pool, several front ends

```
bank/ + generators/  ──build──►  pool/  (many pre-generated, pre-checked versions per template, as JSON)
                                   │
        ┌──────────────┬───────────┼──────────────┬────────────────┐
        ▼              ▼           ▼              ▼                ▼
   LibreTexts     Practice site  Instructor     Canvas QTI      MyOpenMath
   pages (now)    (students)     generator      (import)        (translated code)
                                 → Word / Google Doc
```

**Why a pre-generated pool:** the sites stay static (Netlify, no server, fast on phones), and every version has already passed the generator's own checks before anyone sees it. Templates can produce hundreds of versions each.

## Planned

| # | Item | What it is | Status |
|---|---|---|---|
| 1 | **Finish Chapter 1 bank** | FN3, LF1–LF5, PR1–PR2, FN4–FN6 | In progress (FN1, FN2 done) |
| 2 | **Problem pool export** | `build.py --pool`: N fresh versions per template → `pool/<outcome>.json`, never reusing book seeds | Next after Ch 1 |
| 3 | **Instructor problem/test generator** | Website: choose chapter → section → outcome → item type, how many problems, how many versions (A/B/C), answer key yes/no, work space. Preview, swap any problem for a fresh version, then **download an editable Word file** (opens as a Google Doc when uploaded to Drive). For faculty and Dr. Romero. | Planned |
| 4 | **Student practice site** | Students pick any outcomes (not locked to a quiz). Problems are drawn at random and interleaved; check an answer, reveal it, try another version. Linked from the SAC Math Academy hub. | Planned |
| 5 | **Canvas quizzes (QTI)** | Question groups (10–20 versions, pick 1) that auto-grade numeric, choice and dropdown answers; "explain" parts are manually graded | Planned |
| 6 | **Assessment builder (private)** | A private repo (`172-assessments`) for real quizzes, exams and retakes: its own seeds, a seed register, keys never public | Planned |
| 7 | **MyOpenMath** | Translate templates into MOM's randomized question code (MOM math notation, inline styles only); confirm the import route first | Later |
| 8 | **Worksheets & Playlab bot** | 1–2 page section worksheets from the pool; blueprint + conventions + samples as the bot's knowledge base | Later |

## Technical risks to settle early

- **Editable math in Word.** Equations must be real Word equations (OMML), not images, so faculty can edit them. Plan: build each version's OMML ahead of time (pandoc, which already works in this project) and store it in the pool, so the website only assembles a document. Pilot with one outcome before scaling.
- **Google Docs:** generate .docx and convert on upload to Drive (Docs imports Word equations). A direct Google Doc export would need the Google Drive connector, so it's a later option.
- **Exam security:** the generator stores nothing secret. Each download draws fresh versions, so a public generator can't leak a real exam. Real exams and their keys live only in the private repo (item 6).
- **Accessibility:** both sites follow ACCESSIBILITY.md (WCAG 2.1 AA): keyboard-operable controls, live-region feedback, alt text and data tables for graphs. Word exports keep heading structure and alt text.
