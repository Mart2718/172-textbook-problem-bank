"""Shared helpers for problem templates.

Every template is a function  template(rng) -> dict  with keys:
    stem    : HTML (MathJax \\( \\) math) shown before the parts, or ""
    parts   : list of (prompt_html, answer_html); a single-part problem has one entry
    figure  : None or {"file": name, "alt": text}  (created via plot_* helpers)
Templates must ASSERT their own answers (substitute back, recompute) so a
bad parameter draw fails loudly instead of printing a wrong answer.
"""
from fractions import Fraction
import os
import random

import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x, a, h = sp.symbols("x a h")

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
RAW_BASE = "https://raw.githubusercontent.com/Mart2718/172-textbook-problem-bank/main/figures"


def m(expr_or_str):
    """Inline MathJax."""
    s = expr_or_str if isinstance(expr_or_str, str) else sp.latex(expr_or_str)
    return r"\(" + s + r"\)"


def num(q):
    """Format a rational as an integer, a fraction, or a terminating decimal (CheckIt style)."""
    q = Fraction(q)
    if q.denominator == 1:
        return str(q.numerator)
    d = q.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d == 1:  # terminating decimal
        return f"{float(q):g}"
    return sp.latex(sp.Rational(q.numerator, q.denominator))


def rng_for(seed):
    return random.Random(seed)


def plot_polyline(points, name, fname, chapter="ch1"):
    """CheckIt-style graph: connected line segments, integer grid, closed endpoints.
    Writes PNG + SVG; returns {"file", "url", "alt"}."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    xmin, xmax = min(xs) - 1, max(xs) + 1
    ymin, ymax = min(min(ys), 0) - 1, max(max(ys), 0) + 1
    w = (xmax - xmin) * 0.5
    hgt = (ymax - ymin) * 0.5
    fig, ax = plt.subplots(figsize=(w, hgt), dpi=200)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_xticks(range(int(xmin), int(xmax) + 1))
    ax.set_yticks(range(int(ymin), int(ymax) + 1))
    ax.grid(True, color="#767676", linewidth=0.6)  # 4.5:1 on white; stays >= 3:1 after PNG anti-aliasing (WCAG 1.4.11)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.tick_params(labelsize=10)
    # hide the 0 labels that collide at the origin
    ax.set_xticklabels([str(t) if t != 0 else "" for t in range(int(xmin), int(xmax) + 1)])
    ax.set_yticklabels([str(t) if t != 0 else "" for t in range(int(ymin), int(ymax) + 1)])
    ax.plot(xs, ys, color="#1f4fbf", linewidth=2.4, solid_capstyle="round")
    ax.plot([xs[0], xs[-1]], [ys[0], ys[-1]], "o", color="#1f4fbf", markersize=5)
    ax.text(xmax - 0.2, 0.25, "x", fontsize=12, ha="right")
    ax.text(0.25, ymax - 0.3, "y", fontsize=12, va="top")
    ax.set_title(f"Graph of {name}", fontsize=12)
    out = os.path.join(FIG_DIR, chapter)
    os.makedirs(out, exist_ok=True)
    fig.savefig(os.path.join(out, fname + ".png"), bbox_inches="tight")
    fig.savefig(os.path.join(out, fname + ".svg"), bbox_inches="tight")
    plt.close(fig)
    pts = ", ".join(f"({p[0]}, {p[1]})" for p in points)
    alt = (f"Graph of {name}: connected line segments joining the points {pts}, "
           f"with closed dots at both ends. The domain is [{xs[0]}, {xs[-1]}]. "
           f"Grid lines are 1 unit apart; the x-axis is shown from {int(xmin)} to {int(xmax)} "
           f"and the y-axis from {int(ymin)} to {int(ymax)}. "
           f"A table of values for this graph is available below it.")
    # Equal-access table: every half-unit x on the domain (WCAG 1.1.1 / FN2 audit).
    # Values are exact because slopes are integers; templates keep answers on half-units.
    table = []
    t = Fraction(xs[0])
    while t <= xs[-1]:
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            if x0 <= t <= x1:
                table.append((t, Fraction(y0) + Fraction(y1 - y0, x1 - x0) * (t - x0)))
                break
        t += Fraction(1, 2)
    return {"file": f"{chapter}/{fname}.png", "url": f"{RAW_BASE}/{chapter}/{fname}.png", "alt": alt,
            "name": name, "table": [(num(a), num(b)) for a, b in table]}


# ---------------------------------------------------------------------------
# General graph + mapping figures (added for FN1). Same accessibility styling.
# ---------------------------------------------------------------------------
def _save(fig, fname, chapter):
    out = os.path.join(FIG_DIR, chapter)
    os.makedirs(out, exist_ok=True)
    fig.savefig(os.path.join(out, fname + ".png"), bbox_inches="tight")
    fig.savefig(os.path.join(out, fname + ".svg"), bbox_inches="tight")
    plt.close(fig)
    return {"file": f"{chapter}/{fname}.png", "url": f"{RAW_BASE}/{chapter}/{fname}.png"}


def plot_relation(curves, dots, fname, title, window=5, chapter="ch1"):
    """curves: list of (xs, ys) sequences; dots: list of (x, y) closed points."""
    lo, hi = -window - 1, window + 1
    fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=200)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal")
    ticks = list(range(lo, hi + 1))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.grid(True, color="#767676", linewidth=0.6)  # 4.5:1 on white; stays >= 3:1 after PNG anti-aliasing (WCAG 1.4.11)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.tick_params(labelsize=10)
    ax.set_xticklabels([str(t) if t not in (0, lo, hi) else "" for t in ticks])
    ax.set_yticklabels([str(t) if t not in (0, lo, hi) else "" for t in ticks])
    for xs, ys in curves:
        ax.plot(xs, ys, color="#1f4fbf", linewidth=2.4)
    if dots:
        ax.plot([d[0] for d in dots], [d[1] for d in dots], "o", color="#1f4fbf", markersize=6)
    ax.text(hi - 0.2, 0.25, "x", fontsize=12, ha="right")
    ax.text(0.25, hi - 0.3, "y", fontsize=12, va="top")
    ax.set_title(title, fontsize=12)
    return _save(fig, fname, chapter)


def plot_mapping(inputs, outputs, arrows, fname, chapter="ch1"):
    """Arrow diagram: inputs (left oval) -> outputs (right oval)."""
    from matplotlib.patches import Ellipse, FancyArrowPatch
    n = max(len(inputs), len(outputs))
    fig, ax = plt.subplots(figsize=(4.6, 0.55 * n + 1.2), dpi=200)
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-0.6 * n / 2 - 0.9, 0.6 * n / 2 + 0.9)
    ax.axis("off")
    for cx in (-2, 2):
        ax.add_patch(Ellipse((cx, 0), 1.6, 0.62 * n + 0.8, fill=True, facecolor="#e8f1f2", edgecolor="#1b4f5c", linewidth=1.5))
    ypos = lambda i, k: 0.6 * (k - 1) / 2 - 0.6 * i
    yin = {v: ypos(i, len(inputs)) for i, v in enumerate(inputs)}
    yout = {v: ypos(i, len(outputs)) for i, v in enumerate(outputs)}
    for v, y in yin.items():
        ax.text(-2, y, str(v), fontsize=13, ha="center", va="center")
    for v, y in yout.items():
        ax.text(2, y, str(v), fontsize=13, ha="center", va="center")
    for a, b in arrows:
        ax.add_patch(FancyArrowPatch((-1.55, yin[a]), (1.55, yout[b]), arrowstyle="-|>", mutation_scale=14,
                                     color="#1f4fbf", linewidth=1.6))
    ax.text(-2, ax.get_ylim()[1] - 0.25, "Inputs", fontsize=11, ha="center")
    ax.text(2, ax.get_ylim()[1] - 0.25, "Outputs", fontsize=11, ha="center")
    return _save(fig, fname, chapter)


def html_table(headers, rows, caption):
    """Accessible data table (LibreTexts style)."""
    th = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f"<table border=\"1\" cellpadding=\"8\"><caption>{caption}</caption>"
            f"<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>")
