# Math Content Audit Log

Process: [`AUDIT-PROMPT.md`](AUDIT-PROMPT.md). The reviewer solves blind, then compares against the key and [`CONVENTIONS.md`](CONVENTIONS.md).
A problem is set to `audited` (and locked) only after **both** reviewers pass it: the in-house agent and ChatGPT.

| Outcome | In-house agent | ChatGPT | Status |
|---|---|---|---|
| FN2 | ✅ Nov 17, 2026: 9 ✅ / 1 ⚠️ / 0 ❌, ⚠️ fixed | ✅ Nov 17, 2026: 7 ✅ / 3 ⚠️ (access) / 0 ❌, ⚠️ fixed | **Audited · locked** |

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

## FN2: ChatGPT audit (Nov 17, 2026)

**Result:** all 10 answer keys mathematically correct; the graph images match their descriptions. 7 ✅ / 3 ⚠️ / 0 ❌.

**⚠️ Problems 2, 4, 8 (access):** students using the description had to work out values between the vertices that sighted students read straight off the graph. **Fixed:** each graph now has a **table of values at every 0.5 unit** in a collapsed toggle below it (a real `<table>` with a caption and column headers). The alt text says the table is there. The build verified that each table reproduces the key's answers. No answer-key changes.

**Status:** all 10 FN2 problems set to `audited` and locked in `bank/ch1/FN2.lock.json`. The lock was tested: a changed seed stops the build.
