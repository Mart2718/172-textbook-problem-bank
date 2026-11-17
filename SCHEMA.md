# Problem Schema

One YAML file per outcome: `bank/ch1/FN2.yaml`.

```yaml
outcome: FN2
title: Function Notation
chapter: 1
section: "1.2"
checkit: https://tbil.org/preview/precalculus/exercises/#/bank/FN2/

problems:
  - id: FN2-A-03            # outcome - tier letter - number
    tier: assessment        # floor | assessment | bridge | slip
    item_type: FN2.a        # from blueprints/ch1.md
    kind: template          # template (randomizable) | fixed
    prompt: |
      Let \(f(x) = \begin{cases} {p1} & {a} < x < {b} \\ {p2} & {b} \le x < {c} \end{cases}\).
      Find \(f({x1})\), \(f({x2})\), and \(f({x3})\).
    params:                 # templates only: ranges + constraints
      constraints:
        - "every requested input is in the domain"
        - "one input sits exactly on the boundary b"
        - "every output is a real number"
    answer: generated       # short answer, computed by generators/, never typed by hand
    solution: null          # RESERVED. Left empty for now (see "Worked solutions" below)
    figure: null            # or figures/FN2-A-03.svg
    alt_text: null          # required whenever figure is set
    status: draft           # proposed | draft | audited | published
```

## Decisions (Nov 17, 2026)

| Decision | Choice |
|---|---|
| Problems per outcome | 8–12 (≈4 floor, ≈4 assessment-shaped, 0–2 bridge, 1 Spot the Slip) |
| Answers in the book | **Short answers only**, hidden until clicked |
| Worked solutions | **Not now, but kept open** (see below) |
| Bridge tier | **Only where it fits. Dr. Romero approves each one** (see below) |

### Worked solutions: kept open for later

- Every problem has a `solution` field, and it's empty for now.
- The book builder shows a solution **only if that field is filled**. Nothing changes on the page until one is added.
- Because template answers are computed in code, the generators can later write step-by-step solutions too. Adding them would mean filling the field and rebuilding, with no restructuring.
- They could be added selectively, e.g., one worked example per item type, or only for Spot the Slip.

### Bridge problems: approval gate

- Bridge problems start as `status: proposed`, with a one-line `bridge_note` naming the calculus idea.
- They are **left out of the book build and the practice site** until Dr. Romero changes the status to `draft` (keep) or deletes them (cut).
- Each chapter's audit includes a short "Bridge proposals" list to review: keep, revise or cut.

```yaml
  - id: LF1-B-01
    tier: bridge
    status: proposed
    bridge_note: "Average rate of change on shrinking intervals → the derivative"
```

## Rules

- **Answers are computed.** Template answers come from code (SymPy). Fixed problems get a verification line in their generator too.
- **Floor problems** match CheckIt's wording and answer form.
- **Assessment-shaped problems** match an item type in the blueprint but never reuse a real quiz or exam item.
- **Figures** carry alt text, and angle sides are rays with arrowheads.
- **In the book**, each template appears as 1–3 fixed instances. **On the practice site**, it regenerates every time.

