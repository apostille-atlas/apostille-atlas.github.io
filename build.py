#!/usr/bin/env python3
"""Build the static site into ./dist from data/states.json and content/guides/*.html.
Pages marked "draft": true or without sources are skipped (never publish unsourced pages)."""
import json, re, shutil, html, sys
from pathlib import Path
R = Path(__file__).parent; OUT = R / "dist"
C = json.loads((R / "config.json").read_text())
SITE, NAME, LV = C["site_url"].rstrip("/"), C["site_name"], C["last_verified"]
e = html.escape

def page(path, title, desc, body, h1=None, sources=None, schema=None):
    url = SITE + path
    src = ""
    if sources:
        src = '<section class="sources"><h2>Sources</h2><ul>' + "".join(
            f'<li><a href="{e(u)}" rel="noopener">{e(t)}</a></li>' for t, u in sources) + \
            f'</ul><p class="meta">Last checked against official sources: {LV}. Fees and procedures change, so confirm with the office before sending anything.</p></section>'
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="article"><meta name="twitter:card" content="summary">
<link rel="stylesheet" href="/style.css">{ld}</head><body>
<header><div class="wrap"><a class="brand" href="/">{NAME}</a><nav><a href="/directory/">Directory</a><a href="/guides/state-or-federal-which-office/">Which office?</a><a href="/guides/hague-apostille-countries/">Hague countries</a><a href="/about/">About</a></nav></div></header>
<main class="wrap">{f'<h1>{e(h1)}</h1>' if h1 else ''}{body}{src}</main>
<footer><div class="wrap">{NAME} is an independent guide, not a government website, and not legal advice. <a href="/disclosure/">Affiliate disclosure</a> · <a href="/about/">About</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
</body></html>"""
    f = OUT / path.lstrip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(doc); URLS.append(path)

def state_body(s):
    rows = [("Issuing office", s["authority"]), ("Fee", s["fee_note"]), ("By mail", s["mail_time"]),
            ("In person", s["walkin_time"]), ("Payment", s["payment"]),
            ("Addresses", "<br>".join(e(a) for a in s["addresses"]))] + ([("Phone", s["phone"])] if s["phone"] else [])
    t = "".join(f"<tr><th>{k}</th><td>{v if k=='Addresses' else e(v)}</td></tr>" for k, v in rows)
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    return (f'<p class="lede">How to get an apostille on a {e(s["name"])} document: which office issues it, the official fee (${s["fee"]} per document), how long it takes, and what to send. Every fact comes from the official {e(s["name"])} source listed at the bottom.</p>'
            f'<table class="facts">{t}</table><h2>What to send</h2><ol>{li(s["what_to_send"])}</ol>'
            f'<h2>Things that commonly trip people up</h2><ul>{li(s["tips"])}</ul>'
            '<p>Is your document federal, such as an FBI background check? Then it goes to the <a href="/guides/us-department-of-state/">U.S. Department of State</a>, not the state. Check whether the destination country <a href="/guides/hague-apostille-countries/">accepts apostilles</a>.</p>'
            f'<div class="aff"><strong>Don\'t want to do it yourself?</strong> Apostille services can file in {e(s["name"])} for you, for a fee on top of the state fee. <a href="#affiliate-placeholder" rel="sponsored nofollow" data-affiliate="apostille-service-{s["abbr"].lower()}">[PLACEHOLDER: affiliate partner not yet active]</a></div>')

def main():
    global URLS; URLS = []
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(); shutil.copy(R / "static/style.css", OUT / "style.css")
    states = [s for s in json.loads((R / "data/states.json").read_text()) if not s.get("draft") and s.get("sources")]
    states.sort(key=lambda s: s["name"])
    for s in states:
        title = f'{s["name"]} Apostille: Office, ${s["fee"]} Fee, Processing Time & Steps'
        page(f'/states/{s["slug"]}/', title, f'How to get an apostille in {s["name"]}: {s["authority"]}, ${s["fee"]} per document, mail and walk-in options, what to send. From official sources.',
             state_body(s), h1=f'{s["name"]} apostille: where to go, fee and steps', sources=s["sources"],
             schema={"@context":"https://schema.org","@type":"HowTo","name":f'Get an apostille in {s["name"]}',"step":[{"@type":"HowToStep","text":x} for x in s["what_to_send"]]})
    guides = []
    for g in sorted((R / "content/guides").glob("*.html")):
        raw = g.read_text(); m = re.match(r"<!--(.*?)-->\s*", raw, re.S)
        meta = json.loads(m.group(1))
        if meta.get("draft") or not meta.get("sources"):
            print("SKIP (draft or no sources):", g.name, file=sys.stderr); continue
        slug = g.stem; guides.append((slug, meta))
        page(f'/guides/{slug}/', meta["title"], meta["description"], raw[m.end():], h1=meta["h1"], sources=meta["sources"])
    # directory
    rows = "".join(f'<tr data-name="{e(s["name"].lower())} {s["abbr"].lower()}" data-fee="{s["fee"]}" data-walkin="{int(s["walk_in"])}"><td><a href="/states/{s["slug"]}/">{e(s["name"])}</a></td><td>{e(s["authority"])}</td><td>${s["fee"]}</td><td>{"Yes" if s["walk_in"] else "Not listed"}</td></tr>' for s in states)
    gcards = "".join(f'<a class="card" href="/guides/{sl}/"><span class="badge">{e(m["category"])}</span><br><strong>{e(m["h1"])}</strong></a>' for sl, m in guides)
    js = """<script>const q=document.getElementById('q'),f=document.getElementById('fee'),w=document.getElementById('walk'),o=document.getElementById('feeval');
function run(){o.textContent='$'+f.value;document.querySelectorAll('#tbl tbody tr').forEach(r=>{const ok=r.dataset.name.includes(q.value.toLowerCase().trim())&&(+r.dataset.fee<=+f.value)&&(!w.checked||r.dataset.walkin==='1');r.style.display=ok?'':'none'})}
[q,f,w].forEach(x=>x.addEventListener('input',run));run();</script>"""
    maxfee = max(s["fee"] for s in states)
    dbody = (f'<p class="lede">Apostille offices by state, plus the federal office. {len(states)} states covered so far, with one new page added regularly. Use the filters to narrow the list.</p>'
             f'<div class="filters"><input id="q" type="search" placeholder="Search state…" aria-label="Search state"><label>Max fee <input id="fee" type="range" min="1" max="{maxfee}" value="{maxfee}"> <span id="feeval"></span></label><label><input id="walk" type="checkbox"> Walk-in available</label></div>'
             f'<h2>States</h2><table id="tbl"><thead><tr><th>State</th><th>Issuing office</th><th>Fee / doc</th><th>Walk-in</th></tr></thead><tbody>{rows}</tbody></table>'
             f'<h2>Federal documents</h2><p><a href="/guides/us-department-of-state/">U.S. Department of State Office of Authentications</a>: $20 per document, for FBI checks and other federal records.</p>'
             f'<h2>Guides by category</h2><div class="cards">{gcards}</div>' + js)
    page("/directory/", f"Apostille Directory by State: Offices, Fees, Walk-in | {NAME}", "Compare U.S. state apostille offices: issuing office, fee per document and walk-in availability, from official sources.", dbody, h1="Apostille directory")
    scards = "".join(f'<a class="card" href="/states/{s["slug"]}/"><strong>{e(s["name"])}</strong><small>${s["fee"]}/doc · {e(s["authority"].split(",")[0])}</small></a>' for s in states)
    home = (f'<h1>Get the apostille right the first time</h1><p class="lede">{e(C["tagline"])} Requests get sent back when a document goes to the wrong office or misses a prep step. Each page here lists the official fee, address and requirements, with a link to the source.</p>'
            '<p><a href="/directory/"><strong>Open the directory →</strong></a></p>'
            '<h2>Start here</h2><ol><li><a href="/guides/state-or-federal-which-office/">Is your document state or federal?</a></li><li><a href="/guides/hague-apostille-countries/">Does the destination country accept apostilles?</a></li><li>Open your state below.</li></ol>'
            f'<h2>States</h2><div class="cards">{scards}<a class="card" href="/guides/us-department-of-state/"><strong>Federal (U.S. Dept. of State)</strong><small>$20/doc · FBI checks, federal records</small></a></div>'
            f'<h2>Guides</h2><div class="cards">{gcards}</div>')
    page("/", f"{NAME}: U.S. Apostille Offices, Fees and Steps by State", "Find the right U.S. apostille office for your document, with official fees, addresses, processing times and requirements by state, cited to government sources.", home,
         schema={"@context":"https://schema.org","@type":"WebSite","name":NAME,"url":SITE+"/"})
    page("/about/", f"About {NAME}", f"What {NAME} is, how pages are researched, and how to report an error.",
         f'<p>{NAME} is an independent, plain-language directory of U.S. apostille offices. It is <strong>not</strong> a government website and does not give legal advice.</p><h2>How pages are made</h2><ul><li>Every fact (fees, addresses, timing, requirements) comes from the official government page linked under "Sources".</li><li>Each page shows the date it was last checked. Processing times and fees change, so always confirm with the office.</li><li>We don\'t publish estimated prices or processing times that the office itself hasn\'t published.</li></ul><h2>Corrections</h2><p>Found something out of date? Contact: <a href="mailto:{C["contact_email"]}">{C["contact_email"]}</a>.</p>', h1=f"About {NAME}")
    page("/disclosure/", f"Affiliate Disclosure | {NAME}", "How Apostille Atlas may earn money and how that affects (and does not affect) our content.",
         f'<p>Some links on {NAME} may be affiliate links. If you use one to buy a service, such as a private apostille, courier, translation or online notary service, we may earn a commission at no extra cost to you. Affiliate links are marked with <code>rel="sponsored"</code> and appear in highlighted boxes.</p><p><strong>Current status:</strong> no affiliate partnerships are active yet. Boxes marked "PLACEHOLDER" are not paid links.</p><p>Affiliate relationships never change the official facts on a page. You can always get an apostille directly from the government office for the official fee, and every page explains how.</p><p>This disclosure is meant to follow the U.S. FTC\'s guidance on endorsements (16 CFR Part 255).</p>', h1="Affiliate disclosure",
         sources=[["FTC: Endorsement Guides (16 CFR Part 255)","https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255"]])
    (OUT / "404.html").write_text(f'<!doctype html><meta charset="utf-8"><title>Not found</title><link rel="stylesheet" href="/style.css"><main class="wrap"><h1>Page not found</h1><p><a href="/directory/">Go to the directory</a></p></main>')
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{LV}</lastmod></url>" for u in URLS)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Built {len(URLS)} pages ({len(states)} states, {len(guides)} guides) -> {OUT}")

if __name__ == "__main__": main()
