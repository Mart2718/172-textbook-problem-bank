# Math 172 Textbook Problem Bank

End-of-chapter problem sets for **Math 172 (Precalculus & Trigonometry)** at Santa Ana College, written for the LibreTexts book *Building Toward Calculus*.

Every problem is written **once** here and used **twice**:

1. **Textbook:** a paste-ready LibreTexts page per chapter, itemized by section.
2. **Practice site (later):** students pick any set of standards, and problems are drawn at random and interleaved. Optional presets (e.g., "Final = everything") are shortcuts only. Nothing is locked to a quiz, because quiz content varies from class to class.

The **outcome code** (FN1, LF2, PR1, …) is the key tag on every problem. That's what makes any mix of standards possible.

## Tiers (in every section)

| Tier | Source | Purpose |
|---|---|---|
| Floor (students see "CheckIt Practice") | TBIL CheckIt | Match CheckIt wording and answer forms |
| Assessment-shaped (students see "Putting It Together Practice") | Quiz and exam item types | Practice every move the assessments ask for, with new problems (never the real items) |
| Bridge (students see "Looking Ahead to Calculus"; approval required) | FAQ and guided notes | Extensions, multiple representations, calculus connections |
| Spot the Slip | Same pattern as the support pages | Find and fix an error; explain the reasoning |

## Where things are

| Folder | What's in it | Status |
|---|---|---|
| [`blueprints/`](blueprints/) | Per chapter: section → outcome → assessment map, plus the item types each outcome is assessed with | Ch 1 done |
| [`CONVENTIONS.md`](CONVENTIONS.md) | Answer forms and vocabulary (house style) | Draft, needs approval |
| [`AUDIT-PROMPT.md`](AUDIT-PROMPT.md) · [`AUDIT-LOG.md`](AUDIT-LOG.md) | Math audit instructions (blind solve, then compare) and results | In use |
| [`SCHEMA.md`](SCHEMA.md) | The format every problem follows, plus decisions made | Agreed |
| [`bank/`](bank/) | One YAML file per outcome, grouped by chapter | FN1, FN2 |
| [`generators/`](generators/) | Python templates; answers **computed** (SymPy), never typed by hand. Build: `python3 generators/build.py ch1 FN2` | FN1, FN2 |
| [`figures/`](figures/) | Generated graphs (PNG + SVG) with alt text | FN1, FN2 |
| [`build/`](build/) | `book/` paste-ready LibreTexts HTML · `preview/` the same page with MathJax, to open in a browser · `review/` with tags, seeds and proposed bridge problems · `audit/` Markdown packet for reviewers | FN1, FN2 |
| [`site/`](site/) | Interleaved practice site (Netlify) | Later |

## Workflow

1. **Blueprint:** map the chapter's outcomes to their quiz and exam item types.
2. **Write:** add templates and fixed problems to `bank/`.
3. **Generate:** compute the answers, render the figures, build the book page.
4. **Audit:** build and review → separate audit agent → ChatGPT check → Dr. Romero's final review.
5. **Publish:** paste into LibreTexts; mark the problems `published`.

## Accessibility

See [`ACCESSIBILITY.md`](ACCESSIBILITY.md) for what every build guarantees and the audit log.

WCAG 2.1 AA. Every figure ships with alt text. Math uses MathJax `\( … \)`. Tables use header cells. Graph conventions match CheckIt: angle sides are rays with arrowheads.

## License

Includes material adapted from TBIL Precalculus (CC BY-NC-SA 4.0); this repo is shared under the same license.

---
*Built for Santa Ana College · Dr. Martin Romero*
