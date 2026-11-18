"""FN2 Function Notation: templates. Item-type IDs refer to blueprints/ch1.md."""
from fractions import Fraction

import sympy as sp

from common import x, a, h, m, num, plot_polyline


def _fname(rng, avoid=()):
    # "h" is reserved for the increment in f(x+h) (CONVENTIONS.md), so the draw keeps
    # its four slots (seeds stay stable) but the name h is shown as p.
    n = rng.choice([n for n in ["f", "g", "h", "k"] if n not in avoid])
    return "p" if n == "h" else n


# --------------------------------------------------------------------------
# FN2.a (floor): CheckIt-style piecewise evaluation, one input at the break
# --------------------------------------------------------------------------
def piecewise_eval(rng):
    F = _fname(rng)
    cut = rng.choice([-2, -1, 0, 1, 2])
    kinds = rng.sample(["polynomial", "radical", "rational"], 2)
    pieces = []
    for k in kinds:
        if k == "polynomial":
            pieces.append(rng.choice([1, 2, 3]) * x ** rng.choice([2, 3]) + rng.choice([-3, -2, -1, 1, 2, 3]) * x ** rng.choice([0, 1]))
        elif k == "radical":
            pieces.append(sp.sqrt(rng.choice([1, 3]) * x ** 2 + rng.choice([1, 5])))
        else:
            pieces.append((rng.choice([1, 4]) * x + rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])) / (rng.choice([1, 2]) * x ** 2 + rng.choice([1, 2, 3, 4, 5])))
    cut_left = rng.choice([True, False])  # is the break point in the LEFT piece?
    left_cond = rf"-5 < x \le {cut}" if cut_left else rf"-5 < x < {cut}"
    right_cond = rf"{cut} < x < 5" if cut_left else rf"{cut} \le x < 5"
    flatex = (r"\begin{cases} " + sp.latex(pieces[0]) + " & " + left_cond + r" \\ "
              + sp.latex(pieces[1]) + " & " + right_cond + r" \end{cases}")

    def f(v):
        if -5 < v < cut or (cut_left and v == cut):
            return sp.nsimplify(pieces[0].subs(x, v))
        if cut < v < 5 or (not cut_left and v == cut):
            return sp.nsimplify(pieces[1].subs(x, v))
        raise ValueError("outside domain")

    x1 = rng.choice(range(-4, cut))
    x2 = rng.choice(range(cut + 1, 5))
    inputs = [x1, x2, cut]
    rng.shuffle(inputs)
    parts = []
    for v in inputs:
        val = sp.simplify(f(v))
        assert val.is_real, "piecewise output must be real"
        # independent check: break point uses the piece that includes it
        piece = pieces[0] if (v < cut or (v == cut and cut_left)) else pieces[1]
        assert sp.simplify(val - piece.subs(x, v)) == 0
        parts.append((f"Find {m(f'{F}({v})')}.", m(f"{F}({v}) = " + sp.latex(val))))
    return {"stem": f"Let {m(f'{F}(x) = ' + flatex)}.", "parts": parts, "figure": None}


# --------------------------------------------------------------------------
# FN2.b + FN2.c (floor): CheckIt-style graph: read a value, solve g(x) = k
# --------------------------------------------------------------------------
def _polyline(rng):
    for _ in range(500):
        n_pts = rng.choice([5, 6])
        xs = sorted(rng.sample([2 * k + rng.choice([0, 1]) for k in range(-4, 4)], n_pts))
        if xs[-1] <= 0 or xs[0] >= 0:
            continue
        ys = [rng.choice(range(-6, 7))]
        slope = rng.choice([-2, -1, 1, 2])
        for i in range(1, n_pts):
            ys.append(ys[-1] + slope * (xs[i] - xs[i - 1]))
            slope = rng.choice([s for s in [-2, -1, 1, 2] if s != slope])
        if max(abs(y) for y in ys) <= 7:
            return list(zip(xs, ys))
    raise RuntimeError("no polyline found")


def _value_at(points, c):
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= c <= x1:
            return Fraction(y0) + Fraction(y1 - y0, x1 - x0) * (c - x0)
    raise ValueError


def _solve_level(points, b):
    sols = set()
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if min(y0, y1) <= b <= max(y0, y1):
            if y0 == y1:
                raise ValueError("flat segment")
            s = Fraction(x0) + Fraction(b - y0) * Fraction(x1 - x0, y1 - y0)
            sols.add(s)
    return sorted(sols)


def graph_read_solve(rng, fname_tag, min_solutions=1):
    G = _fname(rng)
    for _ in range(500):
        pts = _polyline(rng)
        xs = [p[0] for p in pts]
        c = rng.choice([v for v in range(xs[0] + 1, xs[-1]) if v not in xs] or [xs[1]])
        b = rng.choice(range(min(p[1] for p in pts), max(p[1] for p in pts) + 1))
        try:
            sols = _solve_level(pts, b)
        except ValueError:
            continue
        # keep solutions readable: integers or halves
        gc_try = _value_at(pts, c)
        # readable solutions; part (a) must not give away part (b)
        if (len(sols) >= min_solutions and all((2 * s).denominator == 1 for s in sols)
                and c not in sols and gc_try != b and gc_try.denominator == 1):
            break
    else:
        raise RuntimeError("no graph found")
    gc = _value_at(pts, c)
    assert gc.denominator == 1
    for s in sols:  # substitute back
        assert _value_at(pts, s) == b
    fig = plot_polyline(pts, G, fname_tag)
    interval = f"[{xs[0]}, {xs[-1]}]"
    sol_txt = ", ".join(m(f"x = {num(s)}") for s in sols)
    parts = [
        (f"Find {m(f'{G}({c})')}.", m(f"{G}({c}) = {num(gc)}")),
        (f"For which {m('x')}-value(s) in the interval {m(interval)} does {m(f'{G}(x) = {b}')}?",
         f"{m(f'{G}(x) = {b}')} when {sol_txt}"),
    ]
    return {"stem": f"Let {m(f'{G}(x)')} be the function graphed below.", "parts": parts, "figure": fig,
            "params": {"points": pts}}


# --------------------------------------------------------------------------
# FN2.d + FN2.e (assessment): evaluate at a number and an expression; solve
# --------------------------------------------------------------------------
def eval_expression_and_solve(rng):
    F = _fname(rng)
    c = -rng.choice(range(2, 10))
    f = x ** 2 + c
    n = rng.choice([-4, -3, -2, 3, 4])
    k = rng.choice([v for v in range(2, 7) if v != abs(n)])
    target = k ** 2 + c
    sols = sp.solve(sp.Eq(f, target), x)
    assert sorted(sols) == [-k, k]
    shifted = sp.expand(f.subs(x, a + 1))
    parts = [
        (f"Find {m(f'{F}({n})')}.", m(f"{F}({n}) = {f.subs(x, n)}")),
        (f"Find and simplify {m(f'{F}(a+1)')}.", m(f"{F}(a+1) = " + sp.latex(shifted))),
        (f"Find every input {m('x')} for which {m(f'{F}(x) = {target}')}.", m(f"x = -{k}") + " or " + m(f"x = {k}")),
    ]
    return {"stem": f"Let {m(f'{F}(x) = ' + sp.latex(f))}.", "parts": parts, "figure": None}


# --------------------------------------------------------------------------
# FN2.a (assessment): piecewise with a restricted domain; one input is outside it
# --------------------------------------------------------------------------
def piecewise_with_domain(rng):
    F = _fname(rng)
    p = rng.choice([4, 5, 6])          # sqrt(x + p) defined on [-p, cut)
    cut = rng.choice([0, 1, 2])
    right_end = cut + rng.choice([3, 4])
    q = x ** 2 - rng.choice([1, 2, 3]) * x + rng.choice([-2, -1, 1])
    left_piece = sp.sqrt(x + p)
    flatex = (r"\begin{cases} " + sp.latex(left_piece) + rf" & {-p} \le x < {cut} \\ "
              + sp.latex(q) + rf" & {cut} \le x \le {right_end} \end{{cases}}")
    # input on the left with a perfect-square radicand
    left_in = rng.choice([v for v in range(-p, cut) if sp.sqrt(v + p).is_integer and v + p > 0])
    outside = rng.choice([-p - 1, -p - 2, right_end + 1, right_end + 2])
    inputs = [left_in, cut, outside]
    parts = []
    for v in inputs:
        if -p <= v < cut:
            val = left_piece.subs(x, v)
            ans = m(f"{F}({v}) = " + sp.latex(val))
        elif cut <= v <= right_end:
            val = q.subs(x, v)
            ans = m(f"{F}({v}) = " + sp.latex(val)) + f" (the boundary value {m(cut)} belongs to the second piece)"
        else:
            ans = (f"{m(f'{F}({v})')} is undefined: {m(v)} is not in the domain "
                   f"{m(f'[{-p}, {right_end}]')}, so neither piece applies.")
        parts.append((f"Find {m(f'{F}({v})')}, or explain why it is undefined.", ans))
    return {"stem": f"Let {m(f'{F}(x) = ' + flatex)}.", "parts": parts, "figure": None}


# --------------------------------------------------------------------------
# FN2.d + FN2.e (assessment): rational function: evaluate, undefined input, solve
# --------------------------------------------------------------------------
def rational_eval_solve(rng):
    F = _fname(rng)
    for _ in range(200):
        A = rng.choice([2, 3, 4])
        B = rng.choice([-5, -3, -1, 1, 3, 5])
        C = rng.choice([1, 2, 3, -1, -2, -3])
        k = rng.choice([v for v in range(-3, 6) if v != A])
        f = (A * x + B) / (x + C)
        sols = sp.solve(sp.Eq(f, k), x)
        if len(sols) == 1 and sols[0].is_integer and sols[0] != -C and B != A * C:
            break
    s = sols[0]
    assert sp.simplify(f.subs(x, s) - k) == 0
    parts = [
        (f"Find {m(f'{F}(0)')}.", m(f"{F}(0) = " + sp.latex(f.subs(x, 0)))),
        (f"Explain why {m(f'{F}({-C})')} is undefined.",
         f"Substituting {m(-C)} makes the denominator {m(f'x + {C}' if C > 0 else f'x - {-C}')} equal to {m(0)}, and division by zero is undefined."),
        (f"Solve {m(f'{F}(x) = {k}')}.", m(f"x = {s}")),
    ]
    return {"stem": f"Let {m(f'{F}(x) = ' + sp.latex(f))}.", "parts": parts, "figure": None}


# --------------------------------------------------------------------------
# Bridge (proposed): difference quotient -> derivative
# --------------------------------------------------------------------------
def difference_quotient_bridge(rng):
    F = _fname(rng)
    bcoef = rng.choice([-4, -3, -2, 1, 2, 3])
    c0 = rng.choice([1, 2, 3])
    f = x ** 2 + bcoef * x
    dq = sp.simplify((f.subs(x, c0 + h) - f.subs(x, c0)) / h)
    assert sp.expand(dq) == sp.expand(2 * c0 + bcoef + h)
    limit = 2 * c0 + bcoef
    hs = ["0.1", "0.01", "0.001"]
    vals = [sp.nsimplify(dq.subs(h, sp.Rational(v))) for v in hs]
    tbl = ", ".join(f"{m(f'h = {v}')}: {m(sp.latex(sp.Float(val, 6)).rstrip('0'))}" for v, val in zip(hs, vals))
    dq_tex = r"\frac{" + f"{F}({c0}+h) - {F}({c0})" + r"}{h}"
    parts = [
        (f"Find and simplify {m(dq_tex)} for {m(r'h \ne 0')}.", m(sp.latex(sp.expand(dq)))),
        (f"Evaluate your answer for {m('h = 0.1')}, {m('h = 0.01')}, and {m('h = 0.001')}. What number do the values approach as {m('h')} gets closer to {m(0)}?",
         f"{tbl}. The values approach {m(limit)}."),
        (f"The expression in part (a) is the slope of the <em>secant line</em> through two points on the graph of {m(F)}. Which two points?",
         f"{m(f'({c0}, {f.subs(x, c0)})')} and {m(f'({c0}+h, ' + sp.latex(sp.expand(f.subs(x, c0 + h))) + ')')}, that is, {m(f'({c0}, {F}({c0}))')} and {m(f'({c0}+h, {F}({c0}+h))')}. "
         f"As {m('h')} shrinks, the second point slides toward the first, and the secant slopes approach the slope of the tangent line at {m(c0)}, which is {m(limit)}."),
    ]
    return {"stem": f"Let {m(f'{F}(x) = ' + sp.latex(f))}.", "parts": parts, "figure": None,
            "bridge_note": "Difference quotient = secant slope; as h → 0 it approaches the tangent slope (the derivative)"}


# --------------------------------------------------------------------------
# Spot the Slip: missing negative solution
# --------------------------------------------------------------------------
def slip_missing_root(rng):
    F = _fname(rng)
    c = -rng.choice(range(2, 10))
    k = rng.choice(range(3, 7))
    target = k ** 2 + c
    sols = sp.solve(sp.Eq(x ** 2 + c, target), x)
    assert sorted(sols) == [-k, k]
    fl = sp.latex(x ** 2 + c)
    work = ("<div style='border-left: 4px solid #b5651d; padding: 6px 12px; margin: 8px 0; background: #fbf4ec;'>"
            "<p style='margin: 0 0 4px 0;'><em>A student's work:</em></p>"
            f"<p style='margin: 0;'>{m(f'{fl} = {target}')}<br/>{m(f'x^2 = {k*k}')}<br/>{m(f'x = {k}')}<br/>"
            f"\"So the only input is {m(f'x = {k}')}.\"</p></div>")
    parts = [
        ("Find the slip in the student's work and explain it in a sentence.",
         f"Going from {m(f'x^2 = {k*k}')} to {m(f'x = {k}')} misses a solution: both {m(k)} and {m(-k)} square to {m(k*k)}."),
        ("Give the correct answer and check it.",
         m(f"x = -{k}") + " or " + m(f"x = {k}") + f". Check: {m(f'{F}(-{k}) = (-{k})^2 - {-c} = {target}')} and {m(f'{F}({k}) = {k}^2 - {-c} = {target}')}."),
    ]
    return {"stem": f"A student was asked: <em>Let {m(f'{F}(x) = {fl}')}. Find every input {m('x')} for which {m(f'{F}(x) = {target}')}.</em>{work}",
            "parts": parts, "figure": None}


TEMPLATES = {
    "piecewise_eval": piecewise_eval,
    "graph_read_solve": graph_read_solve,
    "eval_expression_and_solve": eval_expression_and_solve,
    "piecewise_with_domain": piecewise_with_domain,
    "rational_eval_solve": rational_eval_solve,
    "difference_quotient_bridge": difference_quotient_bridge,
    "slip_missing_root": slip_missing_root,
}
