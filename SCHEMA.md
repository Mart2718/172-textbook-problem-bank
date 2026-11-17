# Problem Schema (DRAFT, for review)

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
    answer: generated       # computed by generators/, never typed by hand
    solution: brief         # none | brief | full
    figure: null            # or figures/FN2-A-03.svg
    alt_text: null          # required whenever figure is set
    status: draft           # draft | audited | published
```

## Rules

- **Answers are computed.** Template answers come from code (SymPy). Fixed problems get a verification line in their generator too.
- **Floor problems** match CheckIt's wording and answer form.
- **Assessment-shaped problems** match an item type in the blueprint but never reuse a real quiz or exam item.
- **Figures** carry alt text, and angle sides are rays with arrowheads.
- **In the book**, each template appears as 1–3 fixed instances. **On the practice site**, it regenerates every time.

## Open questions for Dr. Romero

1. Rough target per outcome: 8–12 problems (~4 floor, ~4 assessment, 1–2 bridge, 1 slip)?
2. Answers in the book: short answers for all, and full worked solutions for which problems?
3. The bridge tier: always include a calculus forward-look, or only where it fits naturally?
