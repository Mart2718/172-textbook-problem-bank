# Math Content Audit Log

Process: [`AUDIT-PROMPT.md`](AUDIT-PROMPT.md). The reviewer solves blind, then compares against the key and [`CONVENTIONS.md`](CONVENTIONS.md).
A problem is set to `audited` (and locked) only after **both** reviewers pass it: the in-house agent and ChatGPT.

| Outcome | In-house agent | ChatGPT | Status |
|---|---|---|---|
| FN2 | ✅ Nov 17, 2026: 9 ✅ / 1 ⚠️ / 0 ❌, ⚠️ fixed | Pending | Draft |

## FN2: in-house audit (Nov 17, 2026)

**Blind solve:** matched the key on all 10 problems, every part.

**Fixed after the audit:**
- **Problem 10 (bridge):** the calculus note said the difference quotient was the "slope of the tangent line." It is the slope of a **secant** line, and its *limit* is the tangent slope. The note, part (c) wording and key are corrected, and the key now gives numeric points, (3, 15) and (3 + h, h² + 8h + 15).
- **Function named *h*:** used in Problems 3, 5 and 7 while Problem 10 uses *h* as the increment. *h* is now never a function name (shown as *p*); CONVENTIONS.md updated.
- **Problem 9b:** the check now verifies both solutions.

**Noted, no change:**
- Interpolating between vertices is more work for screen-reader students than for sighted students (also in ACCESSIBILITY.md). One option: give segment slopes in the alt text.
- "…or explain why it is undefined" on every part of Problem 6 hints that one part is undefined. That's acceptable scaffolding.
- Problems 1 and 3 both test the boundary value, deliberately on opposite sides.
