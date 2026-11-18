"""Lock file for audited problems + Markdown audit packet.

LOCK: problems with status `audited` or `published` are frozen. Their rendered
text is fingerprinted in bank/<chapter>/<OUTCOME>.lock.json. If a template change
would alter a frozen problem, the build stops. To change one on purpose, set its
status back to `draft` (or delete its lock entry), rebuild, and re-audit.

PACKET: build/audit/<chapter>-<OUTCOME>/
  problems.md  : problems only (the reviewer solves these blind)
  key.md       : answers + item type + tier, compared after solving
  figures/     : graph images the reviewer must see
"""
import hashlib
import html
import json
import os
import re
import shutil

FROZEN = ("audited", "published")


def _text(out):
    return json.dumps({"stem": out["stem"], "parts": out["parts"],
                       "figure": (out.get("figure") or {}).get("alt")}, sort_keys=True)


def check_lock(root, chapter, bank, outputs):
    path = os.path.join(root, "bank", chapter, f"{bank['outcome']}.lock.json")
    lock = json.load(open(path)) if os.path.exists(path) else {}
    changed, added = [], []
    for p in bank["problems"]:
        if p["status"] not in FROZEN:
            continue
        digest = hashlib.sha256(_text(outputs[p["id"]]).encode()).hexdigest()
        if p["id"] in lock:
            if lock[p["id"]]["sha256"] != digest:
                changed.append(p["id"])
        else:
            lock[p["id"]] = {"sha256": digest, "template": p["template"], "seed": p["seed"]}
            added.append(p["id"])
    if changed:
        raise SystemExit(f"LOCKED problems would change: {', '.join(changed)}. "
                         "A template edit altered audited content. Revert it, or set these back to "
                         "`draft`, rebuild and re-audit.")
    if added:
        json.dump(lock, open(path, "w"), indent=2, sort_keys=True)
        print(f"locked: {', '.join(added)}")


def to_md(s):
    """HTML + MathJax \\( \\) -> Markdown with $ $ math."""
    s = s.replace(r"\(", "$").replace(r"\)", "$")
    s = re.sub(r"<div[^>]*>", "\n\n> ", s)
    s = re.sub(r"<br\s*/?>", "  \n> ", s)
    s = re.sub(r"</?(em)>", "*", s)
    s = re.sub(r"</?(strong)>", "**", s)
    s = re.sub(r"<p[^>]*>", "", s)
    s = re.sub(r"</p>", "\n> ", s) if "> " in s else re.sub(r"</p>", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"(\n> )+$", "", s.strip())
    return html.unescape(s).strip()


TIER_NAME = {"floor": "CheckIt Practice", "assessment": "Putting It Together Practice",
             "slip": "Spot the Slip", "bridge": "Looking Ahead to Calculus"}
ORDER = ["floor", "assessment", "slip", "bridge"]


def write_packet(root, chapter, bank, outputs):
    out_dir = os.path.join(root, "build", "audit", f"{chapter}-{bank['outcome']}")
    fig_dir = os.path.join(out_dir, "figures")
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(fig_dir)
    probs = sorted(bank["problems"], key=lambda p: ORDER.index(p["tier"]))
    head = (f"# {bank['outcome']} · {bank['title']} (Section {bank['section']})\n\n"
            f"**Objective:** {bank['objective']}\n\n")
    P = [head + "Solve every problem. Graphs are in `figures/`, named by problem number.\n"]
    K = [head + "Answer key. Compare it with your own solutions only after solving.\n"]
    for n, p in enumerate(probs, 1):
        o = outputs[p["id"]]
        P.append(f"\n---\n\n## Problem {n}\n\n{to_md(o['stem'])}\n")
        if o.get("figure"):
            fname = f"problem-{n:02d}.png"
            shutil.copy(os.path.join(root, "figures", o["figure"]["file"]), os.path.join(fig_dir, fname))
            P.append(f"\n![Graph for Problem {n}](figures/{fname})\n\n*Alt text (what a screen-reader student hears):* {o['figure']['alt']}\n")
            if o["figure"].get("table"):
                nm = o["figure"]["name"]
                P.append(f"\n*Table of values (collapsed toggle on the page):*\n\n| $x$ | ${nm}(x)$ |\n|---|---|\n"
                         + "\n".join(f"| {a} | {b} |" for a, b in o["figure"]["table"]) + "\n")
        letters = "abcdefgh"
        if len(o["parts"]) == 1:
            P.append(f"\n{to_md(o['parts'][0][0])}\n")
        else:
            P.append("\n" + "\n\n".join(f"{letters[i]}. {to_md(q)}" for i, (q, _) in enumerate(o["parts"])) + "\n")
        it = ", ".join(p["item_type"]) if isinstance(p["item_type"], list) else p["item_type"]
        K.append(f"\n---\n\n## Problem {n}  \n`{p['id']}` · {TIER_NAME[p['tier']]} · item type {it}\n")
        if p.get("bridge_note"):
            K.append(f"\n*Calculus idea:* {p['bridge_note']}\n")
        K.append("\n" + "\n\n".join(f"{letters[i]}) {to_md(a)}" for i, (_, a) in enumerate(o["parts"])) + "\n")
    open(os.path.join(out_dir, "problems.md"), "w").write("".join(P))
    open(os.path.join(out_dir, "key.md"), "w").write("".join(K))
    return out_dir
