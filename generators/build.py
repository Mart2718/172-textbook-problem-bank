"""Build LibreTexts pages from the bank.

    python3 generators/build.py ch1 FN2

Writes
  build/book/<chapter>-<section>-<outcome>.html     paste into LibreTexts (no proposed problems)
  build/review/<chapter>-<outcome>-review.html       for review: tags, seeds, and proposed bridges
  build/preview/<chapter>-<section>-<outcome>.html   the book page wrapped with MathJax, to open in a browser
"""
import importlib
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from common import rng_for  # noqa: E402
from packet import check_lock, write_packet  # noqa: E402

TIERS = [
    ("floor", "CheckIt Practice", "Same kinds of questions, wording, and answer forms as CheckIt."),
    ("assessment", "Putting It Together Practice", "The same skills, combined into multi-part problems and new formats."),
    ("slip", "Spot the Slip", "Find the error, fix it, and explain your thinking."),
    ("bridge", "Looking Ahead to Calculus", "An idea from this section that grows into calculus."),
]
# Markup follows Dr. Romero's LibreTexts exercise template (box-exercise sections,
# \PageIndex numbering, <dl> Answer blocks, lower-alpha <ol> for parts).
ANSWER = "<dl>\n    <dt><strong class=\"emphasis bold\">Answer</strong></dt>\n    <dd>\n    {body}\n    </dd>\n</dl>"
SOLUTION = "<dl>\n    <dt><strong class=\"emphasis bold\">Solution</strong></dt>\n    <dd>\n    {body}\n    </dd>\n</dl>"


def render_problem(n, prob, out, review=False):
    html = ['<section class="box-exercise">',
            f'<h5 class="box-legend"><span class="lt-icon-default">Exercise \\(\\PageIndex{{{n}}}\\)</span></h5>', ""]
    if review:
        it = prob["item_type"]
        it = ", ".join(it) if isinstance(it, list) else it
        html.append(f"<p style=\"font-size: 0.85em; color: #555;\">[{prob['id']} · {it} · "
                    f"{prob['template']} · seed {prob['seed']} · {prob['status']}]</p>")
        if prob["status"] == "proposed":
            html.append("<p style=\"border: 2px dashed #b5651d; padding: 6px 10px; color: #8a4513;\">"
                        f"<strong>PROPOSED: needs your approval.</strong> Calculus idea: {prob.get('bridge_note', '')}</p>")
    stem = out["stem"]
    if "<div" in stem:  # block content (e.g., student work) can't sit inside <p> (WCAG 4.1.1)
        i = stem.index("<div")
        html.append(f"<p>{stem[:i]}</p>")
        html.append(stem[i:])
    else:
        html.append(f"<p>{stem}</p>")
    if out.get("figure"):
        f = out["figure"]
        html.append(f"<p><img alt=\"{f['alt']}\" src=\"{f['url']}\" style=\"max-width: 480px; width: 100%;\" /></p>")
        if f.get("table"):
            rows = "\n".join(f"        <tr><td>{xv}</td><td>{yv}</td></tr>" for xv, yv in f["table"])
            nm = f["name"]
            html.append(
                "<dl>\n    <dt><strong class=\"emphasis bold\">Table of values for the graph</strong></dt>\n    <dd>\n"
                f"    <table border=\"1\" cellpadding=\"8\">\n"
                f"        <caption>Values of \\({nm}(x)\\) on the graph, every 0.5 unit</caption>\n"
                f"        <thead><tr><th scope=\"col\">\\(x\\)</th><th scope=\"col\">\\({nm}(x)\\)</th></tr></thead>\n"
                f"        <tbody>\n{rows}\n        </tbody>\n    </table>\n    </dd>\n</dl>")
    parts = out["parts"]
    if len(parts) == 1:
        html.append(f"<p>{parts[0][0]}</p>")
        ans = f"<p>{parts[0][1]}</p>"
    else:
        html.append('<ol start="1" style="list-style-type: lower-alpha;">\n'
                    + "\n".join(f"    <li>{p}</li>" for p, _ in parts) + "\n</ol>")
        ans = "\n    ".join(f"<p>{'abcdefgh'[i]}) {an}</p>" for i, (_, an) in enumerate(parts))
    html.append("")
    html.append(ANSWER.format(body=ans))
    if prob.get("solution"):  # reserved: worked solutions appear only when filled in
        html.append(SOLUTION.format(body=prob["solution"]))
    html.append("</section>")
    return "\n".join(html)


def header(bank):
    return (f"<h4><strong>Student Learning Objective</strong></h4>\n\n"
            f"<p><strong>{bank['outcome']}: {bank['objective']}</strong></p>\n\n"
            "<p><strong>CheckIt Practice</strong> matches the CheckIt problems for this outcome. "
            "<strong>Putting It Together Practice</strong> uses the same skills in multi-part problems and new formats. "
            "<strong>Spot the Slip</strong> asks you to find and fix an error. <strong>Looking Ahead to Calculus</strong> "
            "shows where an idea is headed. Try each problem first, then open <strong>Answer</strong> to check. "
            f"For unlimited practice with new numbers, use <a href=\"{bank['checkit']}\">CheckIt {bank['outcome']}</a>.</p>")


def build(chapter, outcome):
    bank = yaml.safe_load(open(os.path.join(ROOT, "bank", chapter, f"{outcome}.yaml")))
    gen = importlib.import_module(bank["generator"])
    outputs = {}
    for prob in bank["problems"]:
        fn = gen.TEMPLATES[prob["template"]]
        args = dict(prob.get("args") or {})
        if prob["template"] == "graph_read_solve":
            args["fname_tag"] = prob["id"]
        outputs[prob["id"]] = fn(rng_for(prob["seed"]), **args)
    check_lock(ROOT, chapter, bank, outputs)  # stop if audited content would change

    def page(review):
        body = [header(bank)]
        n = 0
        for tier, label, desc in TIERS:
            probs = [p for p in bank["problems"] if p["tier"] == tier and (review or p["status"] != "proposed")]
            if not probs:
                continue
            body.append(f"\n<h4>{label}</h4>\n\n<p><em>{desc}</em></p>\n")
            for p in probs:
                n += 1
                body.append(render_problem(n, p, outputs[p["id"]], review))
        return "\n\n".join(body)

    stem = f"{chapter}-{bank['section']}-{outcome}"
    os.makedirs(os.path.join(ROOT, "build", "book"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "build", "review"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "build", "preview"), exist_ok=True)
    book = page(review=False)
    open(os.path.join(ROOT, "build", "book", stem + ".html"), "w").write(book + "\n")
    wrap = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>{t}</title>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<script>window.MathJax={{tex:{{macros:{{PageIndex:['#1',1]}}}}}};</script><script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js'></script>"
            "<style>section.box-exercise{{border:1px solid #9bb;border-radius:6px;padding:4px 16px;margin:14px 0}}h5.box-legend{{background:#e8f1f2;margin:0 -16px 8px;padding:6px 16px}}</style></head><body style='max-width: 820px; margin: 24px auto; padding: 0 16px; font-family: Georgia, serif; line-height: 1.5;'>"
            "{b}</body></html>")
    open(os.path.join(ROOT, "build", "preview", stem + ".html"), "w").write(wrap.format(t=stem, b=book))
    open(os.path.join(ROOT, "build", "review", f"{chapter}-{outcome}-review.html"), "w").write(
        wrap.format(t=f"{outcome} review", b=page(review=True)))
    pk = write_packet(ROOT, chapter, bank, outputs)
    print(f"audit packet: {os.path.relpath(pk, ROOT)}")
    print(f"built {stem}: {sum(p['status'] != 'proposed' for p in bank['problems'])} problems in book, "
          f"{sum(p['status'] == 'proposed' for p in bank['problems'])} proposed")
    return outputs


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
