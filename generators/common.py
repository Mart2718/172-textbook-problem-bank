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
    w = (xmax - xmin) * 0.42
    hgt = (ymax - ymin) * 0.42
    fig, ax = plt.subplots(figsize=(w, hgt), dpi=150)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_xticks(range(int(xmin), int(xmax) + 1))
    ax.set_yticks(range(int(ymin), int(ymax) + 1))
    ax.grid(True, color="#c9c9c9", linewidth=0.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.tick_params(labelsize=7)
    # hide the 0 labels that collide at the origin
    ax.set_xticklabels([str(t) if t != 0 else "" for t in range(int(xmin), int(xmax) + 1)])
    ax.set_yticklabels([str(t) if t != 0 else "" for t in range(int(ymin), int(ymax) + 1)])
    ax.plot(xs, ys, color="#1f4fbf", linewidth=2.4, solid_capstyle="round")
    ax.plot([xs[0], xs[-1]], [ys[0], ys[-1]], "o", color="#1f4fbf", markersize=5)
    ax.text(xmax - 0.2, 0.25, "x", fontsize=9, ha="right")
    ax.text(0.25, ymax - 0.3, "y", fontsize=9, va="top")
    ax.set_title(f"Graph of {name}", fontsize=9)
    out = os.path.join(FIG_DIR, chapter)
    os.makedirs(out, exist_ok=True)
    fig.savefig(os.path.join(out, fname + ".png"), bbox_inches="tight")
    fig.savefig(os.path.join(out, fname + ".svg"), bbox_inches="tight")
    plt.close(fig)
    pts = ", ".join(f"({p[0]}, {p[1]})" for p in points)
    alt = (f"Graph of {name}: connected line segments joining the points {pts}, "
           f"with closed dots at both ends. The domain is [{xs[0]}, {xs[-1]}].")
    return {"file": f"{chapter}/{fname}.png", "url": f"{RAW_BASE}/{chapter}/{fname}.png", "alt": alt}
