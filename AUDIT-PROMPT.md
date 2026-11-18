# Math Content Audit: Reviewer Instructions

Use these instructions for **every** outcome's audit packet (`build/audit/<chapter>-<OUTCOME>/`). They work for ChatGPT, a separate Claude agent, or a human colleague.

## How to run it (two messages)

**Message 1.** Paste everything in the "Step 1 prompt" below, then paste `problems.md` and attach every image in `figures/`. **Don't send the key yet.**

**Message 2.** After the reviewer has posted its solutions, paste the "Step 2 prompt," then paste `key.md` and `CONVENTIONS.md`.

The two steps matter. A reviewer who sees the answers first tends to agree with them. One who solves first catches real errors.

---

## Step 1 prompt (solve blind)

> You are reviewing end-of-section practice problems for a community college precalculus course (Math 172 at Santa Ana College) that prepares students for calculus. Many students are first-generation, and the problems must be correct, clear and fair.
>
> Below are the problems for one learning outcome, with graphs attached as images (each with the alt text a screen-reader student hears).
>
> **Solve every problem and every part yourself, carefully.** Show brief work for each. For graph problems, read values from the image *and* check them against the alt text. If the image and alt text disagree, say so.
>
> While solving, also note:
> 1. **Ambiguity:** any wording a student could reasonably read two ways.
> 2. **Fairness:** anything that requires knowledge beyond the stated objective, or that a screen-reader student couldn't do from the alt text.
> 3. **Giveaways:** any part whose answer is revealed by another part or by the alt text.
>
> Do not ask for the answer key. I'll send it after you've solved everything.

## Step 2 prompt (compare)

> Here is the answer key and the course's conventions sheet. Compare them with **your own solutions**, problem by problem.
>
> For each problem, report one row:
>
> | # | Verdict | Issue | Suggested fix |
> |---|---|---|---|
>
> Verdicts:
> - ✅ **Correct:** the key matches your solution and the conventions.
> - ⚠️ **Convention or wording:** the math is right, but the answer form, vocabulary or wording breaks `CONVENTIONS.md` or is unclear.
> - ❌ **Math error:** the key is wrong, incomplete (e.g., a missing solution), or the problem has no valid answer.
>
> Rules:
> - If you and the key disagree, **re-solve before deciding who is right**, and show the decisive step.
> - Check every "Spot the Slip" problem has **exactly one** error, and the key names it.
> - Check every "Looking Ahead to Calculus" problem is correct *and* that its calculus connection is stated accurately.
> - End with a one-line summary: counts of ✅ / ⚠️ / ❌.

---

## After the audit

1. Bring the table back to Claude. Each ❌ and ⚠️ is fixed in the generator (not by hand-editing the page), and the page is rebuilt.
2. Problems that pass both reviewers are set to `status: audited`. That **locks** them (see `generators/packet.py`), so later template changes can't silently alter approved content.
3. Record the result in `AUDIT-LOG.md` (math content). Accessibility results go in `ACCESSIBILITY.md`.
