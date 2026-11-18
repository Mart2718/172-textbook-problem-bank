"""FN1 Is a Relation a Function?: templates. Item-type IDs refer to blueprints/ch1.md.

Answer form follows CheckIt: "This ___ defines a function." / "does not define a function."
plus a one-sentence reason that names the specific input (CONVENTIONS: short model answers).
"""
import numpy as np
import sympy as sp

from common import x, m, num, plot_relation, plot_mapping, html_table

y = sp.Symbol("y")


def _pairs_tex(pairs):
    return r"\{" + ", ".join(f"({a}, {b})" for a, b in pairs) + r"\}"


def _relation(rng, is_function, n=6):
    """CheckIt style: 6 inputs from 1..20; if not a function, one input gets a 2nd output."""
    dom = rng.sample(range(1, 21), n)
    cod = rng.sample(range(1, 21), n)
    pairs = [(a, rng.choice(cod)) for a in dom]
    if not is_function:
        dup = rng.choice(dom[1:])
        second = rng.choice([b for b in cod if (dup, b) not in pairs])
        pairs[0] = (dup, second)
        rng.shuffle(pairs)
    return pairs, cod


def _dup_input(pairs):
    seen = {}
    for a, b in pairs:
        seen.setdefault(a, []).append(b)
    dups = {a: bs for a, bs in seen.items() if len(set(bs)) > 1}
    return dups


def _verdict(kind, pairs, noun_input="input"):
    dups = _dup_input(pairs)
    if not dups:
        return f"This {kind} defines a function: each {noun_input} is paired with exactly one output."
    a, bs = next(iter(dups.items()))
    bs = sorted(set(bs))
    return (f"This {kind} does not define a function: the input {m(a)} is paired with two different outputs, "
            f"{m(bs[0])} and {m(bs[1])}.")


# --------------------------------------------------------------------------
# FN1.a/.c (floor): CheckIt part 1: mapping, table, ordered pairs
# --------------------------------------------------------------------------
def relations_trio(rng, fname_tag):
    for _ in range(100):
        flags = [rng.choice([True, False]) for _ in range(3)]
        if len(set(flags)) == 2:  # at least one of each
            break
    map_pairs, map_cod = _relation(rng, flags[0])
    tab_pairs, _ = _relation(rng, flags[1])
    ord_pairs, _ = _relation(rng, flags[2])
    for flag, prs in zip(flags, [map_pairs, tab_pairs, ord_pairs]):
        assert (not _dup_input(prs)) == flag  # verify the construction
    inputs = sorted({a for a, _ in map_pairs}, key=lambda v: rng.random())
    fig = plot_mapping(inputs, map_cod, map_pairs, fname_tag + "-map")
    fig["label"] = "Mapping for part (a)"
    fig["alt"] = ("Mapping diagram with inputs in a left oval and outputs in a right oval. "
                  f"Inputs, top to bottom: {', '.join(map(str, inputs))}. "
                  f"Outputs, top to bottom: {', '.join(map(str, map_cod))}. "
                  "Arrows: " + "; ".join(f"{a} to {b}" for a, b in sorted(map_pairs, key=lambda p: inputs.index(p[0]))) + ".")
    tbl = html_table([r"\(x\)", r"\(y\)"], [(a, b) for a, b in tab_pairs], "Table for part (b)")
    parts = [
        ("The mapping shown above.", _verdict("mapping", map_pairs)),
        (f"This table:{tbl}", _verdict("table", tab_pairs)),
        (f"These ordered pairs: {m(_pairs_tex(ord_pairs))}", _verdict("set of ordered pairs", ord_pairs)),
    ]
    return {"stem": "Explain why each of the following relations does or does not define a function.",
            "parts": parts, "figures": [fig]}


# --------------------------------------------------------------------------
# FN1 (floor): CheckIt part 2: equations, y to an odd vs. even power
# --------------------------------------------------------------------------
def equations_pair(rng):
    for _ in range(500):
        A, B = rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 3, 4, 5]) * rng.choice([1, 2, 4, 8])
        n = rng.choice([3, 5])      # odd power
        k = rng.choice([2, 4])      # even power
        # not-a-function equation:  A x^n = B y^k  -> find x0 > 0 with two real y
        wit = None
        for x0 in range(1, 6):
            rhs = sp.Rational(A * x0 ** n, B)
            r = sp.root(rhs, k)
            if r.is_integer and r > 0:
                wit = (x0, int(r))
                break
        if wit:
            break
    eq_fn = sp.Eq(A * y ** n, B * x ** k)        # y^odd: one real y for each x
    eq_not = sp.Eq(A * x ** n, B * y ** k)
    x0, y0 = wit
    sols = sp.solve(eq_not.subs(x, x0), y)
    real = sorted(s for s in sols if s.is_real)
    assert real == [-y0, y0]
    ysol = sp.solve(eq_fn, y)
    real_fn = [s for s in ysol if s.subs(x, 2).is_real]
    assert len(real_fn) == 1  # exactly one real y for a test input
    fn_ans = (f"This equation defines {m('y')} as a function of {m('x')}: solving gives "
              f"{m('y = \\sqrt[%d]{%s}' % (n, sp.latex(sp.Rational(B, A) * x ** k)))}, and an odd root of a real number has exactly "
              f"one real value, so each {m('x')} gives exactly one {m('y')}.")
    not_ans = (f"This equation does not define {m('y')} as a function of {m('x')}: when {m(f'x = {x0}')}, "
               f"{m('y^{%d} = %s' % (k, sp.latex(sp.Rational(A * x0 ** n, B))))}, so {m(f'y = -{y0}')} or {m(f'y = {y0}')}. "
               f"One input, two outputs.")
    items = [(f"{m(sp.latex(eq_fn.lhs) + ' = ' + sp.latex(eq_fn.rhs))}", fn_ans),
             (f"{m(sp.latex(eq_not.lhs) + ' = ' + sp.latex(eq_not.rhs))}", not_ans)]
    rng.shuffle(items)
    return {"stem": f"Explain why each of the following equations does or does not define {m('y')} as a function of {m('x')}.",
            "parts": items, "figures": []}


# --------------------------------------------------------------------------
# FN1.b (floor): CheckIt part 3: three graphs, vertical line test
# --------------------------------------------------------------------------
def _graph(rng, kind, fname, label):
    W = 5
    xs = np.linspace(-W, W, 801)
    if kind == "line":
        a, b = rng.choice([-2, -1, 1, 2]), rng.choice(range(-3, 4))
        f = lambda t: a * t + b
        curves, dots = [(xs, f(xs))], []
        desc = f"a straight line through (0, {b}) and (1, {a + b}) that continues past the edges of the window"
        pts = [(t, f(t)) for t in range(-W, W + 1) if abs(f(t)) <= W]
        is_fn, wit = True, None
    elif kind == "parabola_up":
        s, h, k = rng.choice([-1, 1]), rng.choice(range(-2, 3)), rng.choice(range(-3, 4))
        f = lambda t: s * (t - h) ** 2 + k
        curves, dots = [(xs, f(xs))], []
        desc = f"a parabola opening {'up' if s > 0 else 'down'} with vertex ({h}, {k}); both branches continue past the edge of the window"
        pts = [(t, f(t)) for t in range(-W, W + 1) if abs(f(t)) <= W]
        is_fn, wit = True, None
    elif kind == "parabola_side":
        s, h, k = rng.choice([-1, 1]), rng.choice(range(-3, 2)), rng.choice(range(-2, 3))
        ys = np.linspace(-W, W, 801)
        g = lambda t: s * (t - k) ** 2 + h      # x = s(y-k)^2 + h
        curves, dots = [(g(ys), ys)], []
        desc = f"a parabola opening to the {'right' if s > 0 else 'left'} with vertex ({h}, {k}); both branches continue past the edge of the window"
        pts = [(g(t), t) for t in range(W, -W - 1, -1) if abs(g(t)) <= W]   # traced top to bottom
        is_fn, wit = False, (h + s, k - 1, k + 1)
    elif kind == "points_fn" or kind == "points_not":
        xv = rng.sample(range(-W, W + 1), 5)
        pts = sorted((t, rng.choice(range(-W, W + 1))) for t in xv)
        if kind == "points_not":
            t0 = pts[2][0]
            other = rng.choice([v for v in range(-W, W + 1) if v != pts[2][1]])
            pts = sorted(pts + [(t0, other)])
        curves, dots = [], pts
        desc = "separate points at " + ", ".join(f"({a}, {b})" for a, b in pts)
        is_fn = kind == "points_fn"
        if not is_fn:
            same = [p for p in pts if p[0] == t0]
            wit = (t0, min(p[1] for p in same), max(p[1] for p in same))
        else:
            wit = None
    elif kind in ("piecewise_fn", "piecewise_not"):
        for _ in range(200):
            cut = rng.choice([-2, -1, 1, 2])
            a, b = rng.choice([-1, 1]), rng.choice([-2, -1, 1, 2])
            c = rng.choice([-3, -2, 2, 3])
            end2 = cut + 1 if kind == "piecewise_fn" else cut - 1
            f1 = lambda t, a=a, b=b: a * t + b
            ok = end2 != 0 and abs(f1(-W)) <= W + 1
            if kind == "piecewise_not":  # overlap on [end2, cut]: pieces clearly apart there
                ok = ok and min(abs(f1(end2) - c), abs(f1(cut) - c)) >= 2
            if ok:
                break
        f2 = lambda t: c + 0 * t
        x1 = np.linspace(-W, cut, 400)
        x2 = np.linspace(end2, W, 400)
        curves = [(x1, f1(x1)), (x2, f2(x2))]
        dots = [(-W, f1(-W)), (cut, f1(cut)), (end2, c), (W, c)]
        desc = (f"two pieces, each with closed dots at both ends. A line segment runs from ({-W}, {f1(-W)}) to ({cut}, {f1(cut)}). "
                f"A horizontal segment at height {c} runs from ({end2}, {c}) to ({W}, {c})")
        # traced piece by piece (not sorted by x), as a sighted student would follow the graph
        pts = [(t, f1(t)) for t in range(-W, cut + 1) if abs(f1(t)) <= W + 1] + [(t, c) for t in range(end2, W + 1)]
        is_fn = kind == "piecewise_fn"
        if not is_fn:
            t0 = end2
            wit = (t0, min(f1(t0), c), max(f1(t0), c))
        else:
            wit = None
    fig = plot_relation(curves, dots, fname, label)
    fig["label"] = label
    fig["alt"] = f"{desc[0].upper() + desc[1:]}. The window shows x and y from -6 to 6 with grid lines 1 unit apart."
    seen, ordered = set(), []
    for p in pts:
        if abs(p[1]) <= W + 1 and p not in seen:
            seen.add(p)
            ordered.append(p)
    pts = ordered
    rows = [(num(a), num(b)) for a, b in pts]
    fig["table"] = rows
    fig["table_headers"] = [r"\(x\)", r"\(y\)"]
    fig["table_caption"] = f"Points on {label}"
    fig["table_toggle"] = f"Table of points for {label}"
    # verify the verdict from the table data itself
    xs_seen = [r[0] for r in rows]
    if kind not in ("line", "parabola_up", "points_fn", "piecewise_fn"):
        assert len(xs_seen) != len(set(xs_seen)) or kind == "parabola_side"
    if is_fn:
        reason = "every vertical line crosses the graph at most once, so each input has at most one output."
        ans = f"{label} represents a function: {reason}"
    else:
        t0, y1, y2 = wit
        ans = (f"{label} does not represent a function: the vertical line {m(f'x = {num(t0)}')} crosses the graph at "
               f"{m(f'({num(t0)}, {num(y1)})')} and {m(f'({num(t0)}, {num(y2)})')}.")
    return fig, ans, is_fn


def graphs_trio(rng, fname_tag):
    fn_kinds = ["line", "parabola_up", "points_fn", "piecewise_fn"]
    not_kinds = ["parabola_side", "points_not", "piecewise_not"]
    for _ in range(100):
        kinds = rng.sample(fn_kinds + not_kinds, 3)
        if any(k in fn_kinds for k in kinds) and any(k in not_kinds for k in kinds):
            break
    figs, parts = [], []
    for i, k in enumerate(kinds):
        label = f"Graph {'ABC'[i]}"
        fig, ans, _ = _graph(rng, k, f"{fname_tag}-{'abc'[i]}", label)
        figs.append(fig)
        parts.append((f"{label}", ans))
    return {"stem": "Explain why each of the following graphs does or does not represent a function.",
            "parts": parts, "figures": figs}


# --------------------------------------------------------------------------
# FN1.a (assessment): repeated outputs are fine; repair a non-function
# --------------------------------------------------------------------------
def repeated_outputs(rng):
    dom = rng.sample(range(-6, 10), 5)
    out_shared = rng.choice(range(-5, 10))
    A = [(dom[0], out_shared), (dom[1], out_shared)] + [(d, rng.choice(range(-5, 10))) for d in dom[2:]]
    rng.shuffle(A)
    assert not _dup_input(A)
    domB = rng.sample(range(-6, 10), 4)
    dupx = domB[1]
    B = [(d, rng.choice(range(-5, 10))) for d in domB]
    other = rng.choice([v for v in range(-5, 10) if v != B[1][1]])
    B.append((dupx, other))
    rng.shuffle(B)
    dups = _dup_input(B)
    assert list(dups) == [dupx]
    culprits = [p for p in B if p[0] == dupx]
    shared_inputs = sorted(a for a, b in A if b == out_shared)
    parts = [
        (f"Does {m('A = ' + _pairs_tex(A))} define a function? Explain.",
         f"Yes. Each input appears exactly once. The inputs {m(shared_inputs[0])} and {m(shared_inputs[1])} share the output "
         f"{m(out_shared)}, and that is allowed: two inputs may have the same output."),
        (f"Does {m('B = ' + _pairs_tex(B))} define a function? Explain.",
         f"No. The input {m(dupx)} is paired with two different outputs, {m(min(c[1] for c in culprits))} and {m(max(c[1] for c in culprits))}."),
        (f"Remove exactly one ordered pair from {m('B')} so that it defines a function. Which pair(s) could you remove?",
         f"Remove either {m(str(culprits[0]))} or {m(str(culprits[1]))}. Either way, the input {m(dupx)} is left with one output."),
    ]
    return {"stem": "Consider the two relations below.", "parts": parts, "figures": []}


# --------------------------------------------------------------------------
# FN1.c (assessment): mapping where an output is shared and an output is unused
# --------------------------------------------------------------------------
def mapping_domain_range(rng, fname_tag):
    inputs = sorted(rng.sample(range(-4, 10), 4))
    outputs = sorted(rng.sample(range(-4, 12), 4))
    shared = rng.choice(outputs)
    unused = rng.choice([o for o in outputs if o != shared])
    rest = [o for o in outputs if o not in (shared, unused)]
    arrows = [(inputs[0], shared), (inputs[1], shared), (inputs[2], rest[0]), (inputs[3], rest[1])]
    rng.shuffle(arrows)
    assert not _dup_input(arrows)
    rng_set = sorted({b for _, b in arrows})
    fig = plot_mapping(inputs, outputs, arrows, fname_tag + "-map")
    fig["label"] = "Mapping"
    fig["alt"] = ("Mapping diagram with inputs in a left oval and outputs in a right oval. "
                  f"Inputs, top to bottom: {', '.join(map(str, inputs))}. Outputs, top to bottom: {', '.join(map(str, outputs))}. "
                  "Arrows: " + "; ".join(f"{a} to {b}" for a, b in sorted(arrows)) + ".")
    parts = [
        ("Does this mapping define a function? Explain.",
         f"Yes. Each input has exactly one arrow. Two inputs sharing the output {m(shared)} is allowed, and an output with no "
         f"arrow ({m(unused)}) doesn't matter."),
        ("List the domain.", m(r"\{" + ", ".join(map(str, inputs)) + r"\}")),
        ("List the range.", m(r"\{" + ", ".join(map(str, rng_set)) + r"\}") + f" (the output {m(unused)} is not used, so it is not in the range)"),
    ]
    return {"stem": "Use the mapping below.", "parts": parts, "figures": [fig]}


def _interval_tex(S):
    if isinstance(S, sp.Union):
        return r" \cup ".join(_interval_tex(a) for a in S.args)
    lo = "-\\infty" if S.start == -sp.oo else sp.latex(S.start)
    hi = "\\infty" if S.end == sp.oo else sp.latex(S.end)
    lb = "(" if (S.left_open or S.start == -sp.oo) else "["
    rb = ")" if (S.right_open or S.end == sp.oo) else "]"
    return f"{lb}{lo}, {hi}{rb}"


# --------------------------------------------------------------------------
# FN1.d (assessment): domain of a radical function in interval notation
# --------------------------------------------------------------------------
def radical_domain(rng):
    a, b = rng.choice([1, 2, 3]), rng.choice([-9, -6, -4, -3, 2, 4, 6, 8])
    c, d = rng.choice([4, 6, 8, 9, 12]), rng.choice([1, 2, 3])
    f = sp.sqrt(a * x + b)
    g = sp.sqrt(c - d * x)
    Df = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)
    Dg = sp.calculus.util.continuous_domain(g, x, sp.S.Reals)
    test = Df.start - 1  # just outside f's domain
    assert test not in Df and not f.subs(x, test).is_real
    parts = [
        (f"Find the domain of {m('f')}. Write it in interval notation.", m(_interval_tex(Df))),
        (f"Find the domain of {m('g')}. Write it in interval notation.", m(_interval_tex(Dg))),
        (f"Is {m(f'f({sp.latex(test)})')} a real number? Explain using part (a).",
         f"No, {m(f'f({sp.latex(test)})')} is undefined: {m(sp.latex(test))} is not in the domain {m(_interval_tex(Df))}. The radicand is {m(sp.latex(a * test + b))}, "
         f"and the square root of a negative number is not real."),
    ]
    return {"stem": f"Let {m('f(x) = ' + sp.latex(f))} and {m('g(x) = ' + sp.latex(g))}.", "parts": parts, "figures": []}


# --------------------------------------------------------------------------
# FN1.d (assessment, extension per FAQ): radical over linear
# --------------------------------------------------------------------------
def radical_rational_domain(rng):
    p = rng.choice([1, 2, 3, 4, 5])
    q = rng.choice([v for v in range(-p + 1, 7) if v != 0])
    f = sp.sqrt(x + p) / (x - q)
    D = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)
    assert D == sp.Union(sp.Interval.Ropen(-p, q), sp.Interval.open(q, sp.oo))
    parts = [
        ("Which inputs make the radicand negative?", m(f"x < {-p}")),
        ("Which input makes the denominator zero?", m(f"x = {q}")),
        ("Write the domain of " + m("f") + " in interval notation.", m(_interval_tex(D))),
    ]
    return {"stem": f"Let {m('f(x) = ' + sp.latex(f))}.", "parts": parts, "figures": []}


# --------------------------------------------------------------------------
# Spot the Slip: "repeated output, so not a function"
# --------------------------------------------------------------------------
def slip_repeated_output(rng):
    dom = rng.sample(range(-5, 10), 4)
    shared = rng.choice(range(-5, 10))
    pairs = [(dom[0], shared), (dom[1], rng.choice(range(-5, 10))), (dom[2], shared), (dom[3], rng.choice(range(-5, 10)))]
    assert not _dup_input(pairs)
    work = ("<div style='border-left: 4px solid #b5651d; padding: 6px 12px; margin: 8px 0; background: #fbf4ec;'>"
            "<p style='margin: 0 0 4px 0;'><em>A student's work:</em></p>"
            f"<p style='margin: 0;'>\"The output {m(shared)} shows up twice, at {m(f'({dom[0]}, {shared})')} and "
            f"{m(f'({dom[2]}, {shared})')}. So this relation is <strong>not</strong> a function.\"</p></div>")
    parts = [
        ("Find the slip in the student's reasoning and explain it in a sentence.",
         "The student checked for repeated <em>outputs</em>. A function only forbids one input having two different outputs; "
         "two inputs sharing an output is allowed."),
        ("Give the correct answer with a reason.",
         f"It is a function: the inputs {m(', '.join(map(str, dom)))} each appear exactly once."),
    ]
    return {"stem": f"A student was asked: <em>Does {m(_pairs_tex(pairs))} define a function? Explain.</em>{work}",
            "parts": parts, "figures": []}


# --------------------------------------------------------------------------
# Bridge (proposed): a circle is not a function, but its halves are
# --------------------------------------------------------------------------
def circle_halves_bridge(rng):
    r, a, b = rng.choice([(5, 3, 4), (5, 4, 3), (10, 6, 8), (13, 5, 12)])
    eq = sp.Eq(x ** 2 + y ** 2, r ** 2)
    sols = sorted(sp.solve(eq.subs(x, a), y))
    assert sols == [-b, b]
    top = sp.sqrt(r ** 2 - x ** 2)
    D = sp.calculus.util.continuous_domain(top, x, sp.S.Reals)
    parts = [
        (f"Show that {m(f'x^2 + y^2 = {r**2}')} does not define {m('y')} as a function of {m('x')} by finding one input with two outputs.",
         f"When {m(f'x = {a}')}, {m(f'y^2 = {b*b}')}, so {m(f'y = -{b}')} or {m(f'y = {b}')}. (Other inputs work too.)"),
        (f"Solve for {m('y')}. You should get two functions. Which one gives the top half of the circle?",
         f"Top half: {m('y = ' + sp.latex(top))}. (The other function, {m('y = -' + sp.latex(top))}, gives the bottom half.)"),
        (f"What is the domain of the top-half function?", m(_interval_tex(D))),
    ]
    return {"stem": f"The graph of {m(f'x^2 + y^2 = {r**2}')} is a circle of radius {m(r)} centered at the origin.",
            "parts": parts, "figures": [],
            "bridge_note": "Calculus works with functions, so curves like circles are split into function pieces (used later for slopes of tangent lines and for areas)"}


TEMPLATES = {
    "relations_trio": relations_trio,
    "equations_pair": equations_pair,
    "graphs_trio": graphs_trio,
    "repeated_outputs": repeated_outputs,
    "mapping_domain_range": mapping_domain_range,
    "radical_domain": radical_domain,
    "radical_rational_domain": radical_rational_domain,
    "slip_repeated_output": slip_repeated_output,
    "circle_halves_bridge": circle_halves_bridge,
}
