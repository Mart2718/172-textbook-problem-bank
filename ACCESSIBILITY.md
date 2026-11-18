# Accessibility (WCAG 2.1 AA)

Every page built from this bank targets **WCAG 2.1 Level AA**, the standard in the DOJ ADA Title II web rule and the standard LibreTexts uses.

## Built into the generators (applies to every page automatically)

| Area | What the build does | WCAG |
|---|---|---|
| Alt text | Every graph lists its vertices, endpoints, domain, grid spacing and axis ranges: what a sighted student sees, never a computed answer | 1.1.1 |
| Graph contrast | Line #1f4fbf on white is 7.17:1; grid #767676 is 4.5:1 (it stays above 3:1 after PNG anti-aliasing); labels are black | 1.4.11 |
| Graph data table | Every graph has a collapsed table of values (every 0.5 unit) with a caption and `th scope="col"`, the same data as the image | 1.1.1, 1.3.1 |
| Graph legibility | 10–12 pt labels, 200 dpi, shown up to 480 px wide (SVG copies are kept too) | Recommended |
| Math | MathJax `\( \)`, rendered and spoken by LibreTexts, not images of math | 1.1.1, 1.3.1 |
| Structure | LibreTexts exercise template: `box-exercise` sections, real lists for parts, `<dl>` answers | 1.3.1 |
| Valid markup | Block content is never placed inside `<p>`; `<` and `>` inside math are written `\\lt` and `\\gt` so no bare `<` reaches the editor; nesting is checked | 4.1.1 |
| Unique labels | Data-table toggles and captions name their exercise ("… (Exercise 3)") | Recommended (2.4.6) |
| Mappings | Alt text lists every input, every output and every arrow | 1.1.1 |
| Tables of points | Rows follow the graph in trace order, not sorted, so the table never does the vertical line test for the student | 1.1.1 (equal access) |
| Color | Nothing is conveyed by color alone (the student-work box has a text label) | 1.4.1 |
| Text contrast | Student-work box: black on #fbf4ec is 19.25:1 | 1.4.3 |

## Audit log

### FN2 pilot (Nov 17, 2026): first pass plus an independent second pass
- **Fixed:** a `<div>` was inside a `<p>` in the Spot the Slip problem (4.1.1); the gridlines were 1.66:1 and students read values against them (1.4.11, potential failure); the graph labels were small (recommended practice); the alt text now includes grid spacing and axis ranges.
- **Passed:** text contrast, answer leakage in alt text (both passes: the alt text gives only what's visible, never interpolated values), link text, reading order.
- **Needs testing in LibreTexts with a keyboard and a screen reader:** the Answer toggles (keyboard, focus, expanded state); MathJax speech for piecewise `cases`; whether lettered sub-parts are announced as "a, b" or "1, 2"; reflow at 320 px and 400% zoom; whether images load from GitHub.
- **Equal access (resolved after the ChatGPT audit):** screen-reader students had to work out values between vertices. Every graph now gets a half-unit **table of values** in a collapsed toggle, built from the same data as the graph.

---
This is an AI-assisted code-level review, not a compliance certification and not equivalent to testing with real assistive technology. Final acceptance goes through the institution's designated accessibility review and approval process.

### FN1 (Nov 17, 2026): first pass plus an independent second pass
- **Confirmed failures:** none.
- **Fixed (potential failures and recommended practice):**
  - A bare `<` in math became `\lt`. This was applied at render time, so FN2 benefits too without unlocking it.
  - The grid was darkened to #767676: the PNG anti-aliasing had lowered #949494 to 2.46:1.
  - Toggle and caption labels now name their exercise.
  - Tables of points follow the graph in trace order.
  - Alt text now says when a curve continues past the window.
  - Piecewise segments have closed dots at their outer ends.
  - Alt text no longer repeats the "Graph A" label.
- **Still needs testing in LibreTexts:** keyboard and screen-reader operation of the toggles; MathJax speech.
