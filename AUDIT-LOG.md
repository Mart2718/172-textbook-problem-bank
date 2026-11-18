# Math Content Audit Log

Process: [`AUDIT-PROMPT.md`](AUDIT-PROMPT.md). The reviewer solves blind, then compares against the key and [`CONVENTIONS.md`](CONVENTIONS.md).
A problem is set to `audited` (and locked) only after **both** reviewers pass it: the in-house agent and ChatGPT.

| Outcome | In-house agent | ChatGPT | Status |
|---|---|---|---|
| FN1 | ✅ Nov 17, 2026: 8 ✅ / 2 ⚠️ / 0 ❌, ⚠️ fixed | Pending | Draft (bridge proposed) |
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

## FN1: in-house audit (Nov 17, 2026)

**Blind solve:** matched the key on all 10 problems, every part. The graphs, alt text and tables agree.

**Fixed after the audit:**
- **Problems 2 and 10:** paired answers are now smallest first ("y = −2 or y = 2"), per CONVENTIONS.md.
- **Problem 7c:** uses the course wording, "f(1) is undefined: 1 is not in the domain …".
- **Problem 10b:** the answer now leads with the top half, which is what the question asks.

**Noted, no change:**
- **Domain (Problems 7–8):** the reviewer noted it goes beyond CheckIt FN1 (the FAQ also calls it an extension). It stays because Midterm 1B assesses it under FN1.
- **Problem 6c** (an output with no arrow is not in the range) is an intentional trap, and the key says so.
