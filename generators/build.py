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

TIERS = [
    ("floor", "Practice (CheckIt-style)", "Same kinds of questions, wording, and answer forms as CheckIt."),
    ("assessment", "Quiz &amp; Exam Practice", "The kinds of questions you will see on quizzes and exams."),
    ("bridge", "Looking Ahead to Calculus", "An idea from this section that grows into calculus."),
    ("slip", "Spot the Slip", "Find the error, fix it, and explain your thinking."),
]
H3 = "color: #1b4f5c; border-bottom: 2px solid #1b4f5c; padding-bottom: 4px; margin-top: 28px;"
NOTE = "color: #444; font-style: italic; margin-top: 0;"


def render_problem(n, prob, out, review=False):
    html = []
    tag = ""
    if review:
        it = prob["item_type"]
        it = ", ".join(it) if isinstance(it, list) else it
        tag = (f" <span style='font-size: 0.85em; color: #555;'>[{prob['id']} · {it} · "
               f"{prob['template']} · seed {prob['seed']} · {prob['status']}]</span>")
    if review and prob["status"] == "proposed":
        html.append("<div style='border: 2px dashed #b5651d; padding: 8px 12px; margin: 10px 0;'>"
                    f"<p style='margin: 0 0 6px 0; color: #8a4513;'><strong>PROPOSED: needs your approval.</strong> "
                    f"Calculus idea: {prob.get('bridge_note', '')}</p>")
    html.append(f"<p><strong>{n}.</strong> {out['stem']}{tag}</p>")
    if out.get("figure"):
        f = out["figure"]
        src = f["url"] if not review else "../../figures/" + f["file"]
        html.append(f"<p><img src='{src}' alt='{f['alt']}' style='max-width: 380px; width: 100%;' /></p>")
    parts = out["parts"]
    letters = "abcdefgh"
    if len(parts) == 1:
        html.append(f"<p>{parts[0][0]}</p>")
    else:
        html.append("<ol type='a'>" + "".join(f"<li>{p}</li>" for p, _ in parts) + "</ol>")
    ans = parts[0][1] if len(parts) == 1 else "<br/>".join(f"({letters[i]}) {an}" for i, (_, an) in enumerate(parts))
    html.append(f"<dl><dt>Answer</dt><dd>{ans}</dd></dl>")
    if prob.get("solution"):  # reserved: worked solutions appear only when filled in
        html.append(f"<dl><dt>Solution</dt><dd>{prob['solution']}</dd></dl>")
    if review and prob["status"] == "proposed":
        html.append("</div>")
    return "\n".join(html)


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

    def page(review):
        title = f"{bank['section']} {bank['title']} ({bank['outcome']})"
        body = [f"<h2>Problem Set: {title}</h2>",
                f"<p>Answers are hidden. Try each problem first, then click <strong>Answer</strong> to check. "
                f"For more practice with new numbers every time, use "
                f"<a href='{bank['checkit']}'>CheckIt {bank['outcome']}</a>.</p>"]
        n = 0
        for tier, label, desc in TIERS:
            probs = [p for p in bank["problems"] if p["tier"] == tier and (review or p["status"] != "proposed")]
            if not probs:
                continue
            body.append(f"<h3 style='{H3}'>{label}</h3><p style='{NOTE}'>{desc}</p>")
            for p in probs:
                n += 1
                body.append(render_problem(n, p, outputs[p["id"]], review))
        return "\n".join(body)

    stem = f"{chapter}-{bank['section']}-{outcome}"
    os.makedirs(os.path.join(ROOT, "build", "book"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "build", "review"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "build", "preview"), exist_ok=True)
    book = page(review=False)
    open(os.path.join(ROOT, "build", "book", stem + ".html"), "w").write(book + "\n")
    wrap = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>{t}</title>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js'></script>"
            "</head><body style='max-width: 820px; margin: 24px auto; padding: 0 16px; font-family: Georgia, serif; line-height: 1.5;'>"
            "{b}</body></html>")
    open(os.path.join(ROOT, "build", "preview", stem + ".html"), "w").write(wrap.format(t=stem, b=book))
    open(os.path.join(ROOT, "build", "review", f"{chapter}-{outcome}-review.html"), "w").write(
        wrap.format(t=f"{outcome} review", b=page(review=True)))
    print(f"built {stem}: {sum(p['status'] != 'proposed' for p in bank['problems'])} problems in book, "
          f"{sum(p['status'] == 'proposed' for p in bank['problems'])} proposed")
    return outputs


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
