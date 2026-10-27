#!/usr/bin/env python3
"""Build the static site into ./dist from data/states.json and content/guides/*.html.
Pages marked "draft": true or without sources are skipped (never publish unsourced pages)."""
import json, re, shutil, html, sys
from pathlib import Path
R = Path(__file__).parent; OUT = R / "dist"
C = json.loads((R / "config.json").read_text())
SITE, NAME, LV = C["site_url"].rstrip("/"), C["site_name"], C["last_verified"]
e = html.escape

GOAT = '<script data-goatcounter="https://apostille-atlas.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
ORG = {"@type": "Organization", "name": NAME, "url": SITE + "/"}
strip = lambda h: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
NICE = lambda d: __import__("datetime").date.fromisoformat(d).strftime("%B %-d, %Y")

def faq_html(faqs):
    if not faqs: return ""
    return '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(
        f'<h3>{e(q)}</h3><p>{a}</p>' for q, a in faqs) + "</section>"

def page(path, title, desc, body, h1=None, sources=None, schema=None, summary=None, faqs=None,
         crumbs=None, article=True, reviewed=None, related=None):
    """Write one page. title must be < 60 chars. summary = 2-3 sentence direct answer (confirmed facts only).
    faqs = [[question, answer_html], ...] from real questions (research/questions.md). crumbs = [(name, path), ...]."""
    assert len(title) < 60, f"title too long ({len(title)}): {title}"
    url = SITE + path; rv = reviewed or LV
    PAGES.append(dict(path=path, title=title, desc=desc, lastmod=rv))
    src = ""
    if sources:
        src = '<section class="sources"><h2>Official sources</h2><ul>' + "".join(
            f'<li><a href="{e(u)}" rel="noopener">{e(t)}</a></li>' for t, u in sources) + \
            f'</ul><p class="meta">Last checked against official sources: {rv}. Fees and procedures change, so confirm with the office before sending anything.</p></section>'
    graph = []
    if schema: graph += schema if isinstance(schema, list) else [schema]
    if article and h1:
        graph.append({"@type": "Article", "headline": h1, "description": desc, "url": url, "mainEntityOfPage": url,
                      "datePublished": C.get("launched", LV), "dateModified": rv, "author": ORG, "publisher": ORG, "inLanguage": "en-US"})
    if crumbs is not None:
        trail = [("Home", "/")] + crumbs + [(h1 or title, path)]
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]})
    if faqs:
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                      "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]})
    for g in graph: g.pop("@context", None)
    ld = f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph})}</script>' if graph else ""
    bc = ""
    if crumbs is not None:
        bc = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>' + "".join(' › ' + f'<a href="{p}">{e(n)}</a>' for n, p in crumbs) + "</nav>"
    top = ""
    if h1:
        top = bc + f'<h1>{e(h1)}</h1>'
        if reviewed is not None or sources: top += f'<p class="meta">Last reviewed: <time datetime="{rv}">{NICE(rv)}</time></p>'
    if summary: top += f'<div class="answer"><strong>Short answer:</strong> {e(summary)}</div>'
    rel = ""
    if related:
        rel = '<section class="related"><h2>Related pages</h2><ul>' + "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in related) + "</ul></section>"
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="{'article' if article and h1 else 'website'}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<link rel="stylesheet" href="/style.css">{ld}</head><body>
<header><div class="wrap"><a class="brand" href="/">{NAME}</a><nav><a href="/directory/">Directory</a><a href="/faq/">FAQ</a><a href="/guides/">Guides</a><a href="/guides/state-or-federal-which-office/">Which office?</a><a href="/guides/hague-apostille-countries/">Hague countries</a><a href="/about/">About</a></nav></div></header>
<main class="wrap">{top}{body}{faq_html(faqs)}{rel}{src}</main>
<footer><div class="wrap">{NAME} is an independent guide, not a government website, and not legal advice. <a href="/disclosure/">Affiliate disclosure</a> · <a href="/about/">About</a> · <a href="/faq/">FAQ</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
{GOAT}
</body></html>"""
    f = OUT / path.lstrip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(doc); URLS.append(path)

def state_body(s, states):
    rows = [("Issuing office", s["authority"]), ("Fee", s["fee_note"]), ("By mail", s["mail_time"]),
            ("In person", s["walkin_time"]), ("Payment", s["payment"]),
            ("Addresses", "<br>".join(e(a) for a in s["addresses"]))] + ([("Phone", s["phone"])] if s["phone"] else [])
    t = "".join(f"<tr><th>{k}</th><td>{v if k=='Addresses' else e(v)}</td></tr>" for k, v in rows)
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    others = " · ".join(f'<a href="/states/{o["slug"]}/">{e(o["name"])}</a>' for o in states if o["slug"] != s["slug"])
    n = e(s["name"])
    return (f'<p class="lede">How to get an apostille on a {n} document: which office issues it, the official fee (${s["fee"]} per document), how long it takes, and what to send. Every fact comes from the official {n} source listed at the bottom.</p>'
            f'<h2>Where do I send a {n} apostille request, what does it cost, and how long does it take?</h2><table class="facts">{t}</table>'
            f'<h2>What do I need to send for a {n} apostille?</h2><ol>{li(s["what_to_send"])}</ol>'
            f'<h2>What trips people up with {n} apostilles?</h2><ul>{li(s["tips"])}</ul>'
            '<h2>Is my document state or federal?</h2><p>If a federal agency signed it, such as an FBI background check, it goes to the <a href="/guides/us-department-of-state/">U.S. Department of State</a>, not the state. Not sure? See <a href="/guides/state-or-federal-which-office/">state or federal: which office?</a> Also check whether the destination country <a href="/guides/hague-apostille-countries/">accepts apostilles</a>.</p>'
            f'<div class="aff"><strong>Don\'t want to do it yourself?</strong> Apostille services can file in {n} for you, for a fee on top of the state fee. One such service: <a href="https://apstl.us/6YBeOr" rel="sponsored nofollow noopener" data-affiliate="apostille-usa-original">Apostille USA</a> (affiliate link), which says it handles apostilles in all 50 states and DC. If you order through this link, we may earn a commission at no extra cost to you. See our <a href="/disclosure/">affiliate disclosure</a>.</div>'
            f'<p class="meta">Document from another state? Each state only apostilles its own documents: {others}, or the full <a href="/directory/">directory</a>.</p>')

def state_faqs(s):
    n = s["name"]
    return [[f"Where do I get an apostille in {n}?", f'From the {e(s["authority"])}. Documents issued or notarized in {e(n)} are apostilled there, no matter where you live now.'],
            [f"How much does a {n} apostille cost?", e(s["fee_note"])],
            [f"How long does a {n} apostille take?", f'By mail: {e(s["mail_time"])} In person: {e(s["walkin_time"])}'],
            [f"Can {n} apostille my FBI background check?", f'No. FBI background checks are federal documents, so the <a href="/guides/us-department-of-state/">U.S. Department of State</a> apostilles them, not {e(n)}.'],
            [f"Can {n} apostille a document from another state?", "No. A state only apostilles documents issued or notarized in that state. Send a document from another state to that state's office (see the <a href=\"/directory/\">directory</a>)."]]

GUIDE_LINKS = [("Apostille FAQ", "/faq/"), ("State or federal: which office?", "/guides/state-or-federal-which-office/"),
               ("Birth certificate apostille", "/guides/birth-certificate-apostille/"), ("FBI background check apostille", "/guides/fbi-background-check-apostille/"),
               ("U.S. Department of State (federal)", "/guides/us-department-of-state/"), ("Which countries accept apostilles?", "/guides/hague-apostille-countries/"),
               ("Apostille directory by state", "/directory/")]

def main():
    global URLS, PAGES; URLS = []; PAGES = []
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(); shutil.copy(R / "static/style.css", OUT / "style.css")
    for k in (R / "static").glob("*.txt"): shutil.copy(k, OUT / k.name)  # IndexNow key file
    states = [s for s in json.loads((R / "data/states.json").read_text()) if not s.get("draft") and s.get("sources")]
    states.sort(key=lambda s: s["name"])
    for s in states:
        title = f'{s["name"]} Apostille: Where to Go, ${s["fee"]} Fee & Steps'
        rel = [(n, p) for n, p in GUIDE_LINKS if p != "/directory/"]
        page(f'/states/{s["slug"]}/', title, f'How to get an apostille in {s["name"]}: {s["authority"]}, ${s["fee"]} per document, mail and walk-in options, what to send. From official sources.',
             state_body(s, states), h1=f'{s["name"]} apostille: where to go, fee and steps', sources=s["sources"],
             summary=s.get("summary"), faqs=state_faqs(s), crumbs=[("States", "/directory/")], reviewed=s.get("last_reviewed", LV), related=rel,
             schema={"@type":"HowTo","name":f'Get an apostille in {s["name"]}',"step":[{"@type":"HowToStep","text":x} for x in s["what_to_send"]]})
    guides = []
    for g in sorted((R / "content/guides").glob("*.html")):
        raw = g.read_text(); m = re.match(r"<!--(.*?)-->\s*", raw, re.S)
        meta = json.loads(m.group(1))
        if meta.get("draft") or not meta.get("sources"):
            print("SKIP (draft or no sources):", g.name, file=sys.stderr); continue
        slug = g.stem; guides.append((slug, meta))
        rel = [(n, p) for n, p in GUIDE_LINKS if p != f"/guides/{slug}/"]
        page(f'/guides/{slug}/', meta["title"], meta["description"], raw[m.end():], h1=meta["h1"], sources=meta["sources"],
             summary=meta.get("summary"), faqs=meta.get("faqs"), crumbs=[("Guides", "/guides/")], reviewed=meta.get("last_reviewed", LV), related=rel)
    gcards = "".join(f'<a class="card" href="/guides/{sl}/"><span class="badge">{e(m["category"])}</span><br><strong>{e(m["h1"])}</strong></a>' for sl, m in guides)
    gcards = '<a class="card" href="/faq/"><span class="badge">FAQ</span><br><strong>Frequently asked apostille questions</strong></a>' + gcards
    # FAQ hub
    fq = json.loads((R / "data/faq.json").read_text())
    fsrc, seen = [], set()
    for q, a, ss in fq["items"]:
        for t, u in ss:
            if u not in seen: seen.add(u); fsrc.append([t, u])
    fitems = [[q, a + " <span class=\"cite\">Source: " + ", ".join(f'<a href="{e(u)}" rel="noopener">{e(t)}</a>' for t, u in ss) + "</span>"] for q, a, ss in fq["items"]]
    toc = "<ol>" + "".join(f'<li><a href="#q{i+1}">{e(q)}</a></li>' for i, (q, a, ss) in enumerate(fq["items"])) + "</ol>"
    fbody = (f'<p class="lede">Answers to {len(fq["items"])} questions people ask most often about U.S. apostilles, collected from forums and official FAQ pages. Each answer cites the official source it comes from; where no official source answers the question, we say so instead of guessing.</p>'
             f'<h2>Questions on this page</h2>{toc}<h2>Answers</h2>' + "".join(f'<h3 id="q{i+1}">{e(q)}</h3><p>{a}</p>' for i, (q, a) in enumerate(fitems)) +
             '<p>Next step: open your state in the <a href="/directory/">apostille directory</a>, or read <a href="/guides/state-or-federal-which-office/">state or federal: which office?</a></p>')
    page("/faq/", fq["title"], fq["description"], fbody, h1="Frequently asked apostille questions", sources=fsrc, summary=fq["summary"],
         crumbs=[("Guides", "/guides/")], related=[(n, p) for n, p in GUIDE_LINKS if p != "/faq/"])
    # FAQPage JSON-LD for the hub (answers as plain text, without inline citations)
    hub = OUT / "faq/index.html"; d = hub.read_text()
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a, ss in fq["items"]]}
    d = d.replace('"@graph": [', '"@graph": [' + json.dumps(ld) + ", ", 1); hub.write_text(d)
    # guides index
    page("/guides/", f"Apostille Guides: Documents, Offices, Countries", "Plain-language apostille guides for U.S. documents: birth certificates, FBI checks, federal documents, Hague countries and which office to use.",
         f'<p class="lede">Guides for specific documents and situations. Each one cites official government sources.</p><div class="cards">{gcards}</div><h2>Looking for a state?</h2><p>Open the <a href="/directory/">apostille directory</a>.</p>',
         h1="Apostille guides", crumbs=[], article=False,
         summary="Start with the office: state and locally issued or notarized documents are apostilled by that state, and federal documents such as FBI checks by the U.S. Department of State. Then check whether your destination country accepts apostilles at all.")
    # directory
    rows = "".join(f'<tr data-name="{e(s["name"].lower())} {s["abbr"].lower()}" data-fee="{s["fee"]}" data-walkin="{int(s["walk_in"])}"><td><a href="/states/{s["slug"]}/">{e(s["name"])}</a></td><td>{e(s["authority"])}</td><td>${s["fee"]}</td><td>{"Yes" if s["walk_in"] else "Not listed"}</td></tr>' for s in states)
    js = """<script>const q=document.getElementById('q'),f=document.getElementById('fee'),w=document.getElementById('walk'),o=document.getElementById('feeval');
function run(){o.textContent='$'+f.value;document.querySelectorAll('#tbl tbody tr').forEach(r=>{const ok=r.dataset.name.includes(q.value.toLowerCase().trim())&&(+r.dataset.fee<=+f.value)&&(!w.checked||r.dataset.walkin==='1');r.style.display=ok?'':'none'})}
[q,f,w].forEach(x=>x.addEventListener('input',run));run();</script>"""
    maxfee = max(s["fee"] for s in states); minfee = min(s["fee"] for s in states)
    dbody = (f'<p class="lede">Apostille offices by state, plus the federal office. {len(states)} states covered so far, with one new page added regularly. Use the filters to narrow the list.</p>'
             f'<div class="filters"><input id="q" type="search" placeholder="Search state…" aria-label="Search state"><label>Max fee <input id="fee" type="range" min="1" max="{maxfee}" value="{maxfee}"> <span id="feeval"></span></label><label><input id="walk" type="checkbox"> Walk-in available</label></div>'
             f'<h2>Which office handles my state\'s apostilles?</h2><table id="tbl"><thead><tr><th>State</th><th>Issuing office</th><th>Fee / doc</th><th>Walk-in</th></tr></thead><tbody>{rows}</tbody></table>'
             f'<h2>Where do federal documents go?</h2><p><a href="/guides/us-department-of-state/">U.S. Department of State Office of Authentications</a>: $20 per document, for FBI checks and other federal records.</p>'
             f'<h2>Guides by category</h2><div class="cards">{gcards}</div>' + js)
    page("/directory/", "Apostille Directory by State: Offices, Fees, Walk-in", "Compare U.S. state apostille offices: issuing office, fee per document and walk-in availability, from official sources.", dbody,
         h1="Apostille directory", crumbs=[], article=False, reviewed=LV,
         summary=f"There is no single national apostille office: each state apostilles its own documents, and the U.S. Department of State handles federal ones for $20. Among the {len(states)} states covered so far, official fees range from ${minfee} to ${maxfee} per document.")
    scards = "".join(f'<a class="card" href="/states/{s["slug"]}/"><strong>{e(s["name"])}</strong><small>${s["fee"]}/doc · {e(s["authority"].split(",")[0])}</small></a>' for s in states)
    home = (f'<h1>Get the apostille right the first time</h1><div class="answer"><strong>Short answer:</strong> A U.S. document is apostilled by the state that issued or notarized it, or by the U.S. Department of State if it is federal (such as an FBI background check). This site lists each office\'s official fee, address, processing time and requirements, with a link to the government source.</div>'
            f'<p class="lede">{e(C["tagline"])} Requests get sent back when a document goes to the wrong office or misses a prep step.</p>'
            '<p><a href="/directory/"><strong>Open the directory →</strong></a> · <a href="/faq/"><strong>Read the apostille FAQ →</strong></a></p>'
            '<h2>Start here</h2><ol><li><a href="/guides/state-or-federal-which-office/">Is your document state or federal?</a></li><li><a href="/guides/hague-apostille-countries/">Does the destination country accept apostilles?</a></li><li>Open your state below.</li></ol>'
            f'<h2>States</h2><div class="cards">{scards}<a class="card" href="/guides/us-department-of-state/"><strong>Federal (U.S. Dept. of State)</strong><small>$20/doc · FBI checks, federal records</small></a></div>'
            f'<h2>Guides</h2><div class="cards">{gcards}</div>')
    page("/", f"{NAME}: U.S. Apostille Offices by State", "Find the right U.S. apostille office for your document, with official fees, addresses, processing times and requirements by state, cited to government sources.", home,
         schema=[{"@type":"WebSite","name":NAME,"url":SITE+"/","description":C["tagline"],"inLanguage":"en-US","publisher":ORG}, ORG], article=False)
    page("/about/", f"About {NAME}", f"What {NAME} is, how pages are researched, and how to report an error.",
         f'<p>{NAME} is an independent, plain-language directory of U.S. apostille offices. It is <strong>not</strong> a government website and does not give legal advice.</p><h2>How are pages made?</h2><ul><li>Every fact (fees, addresses, timing, requirements) comes from the official government page linked under "Official sources".</li><li>Each page shows the date it was last reviewed. Processing times and fees change, so always confirm with the office.</li><li>We don\'t publish estimated prices or processing times that the office itself hasn\'t published.</li><li>Questions answered on the site come from real questions people ask in forums and on official FAQ pages.</li></ul><h2>Privacy</h2><p>This site uses privacy-friendly, cookieless analytics (GoatCounter) to count page views.</p><h2>Corrections</h2><p>Found something out of date? Contact: <a href="mailto:{C["contact_email"]}">{C["contact_email"]}</a>.</p>',
         h1=f"About {NAME}", article=False, crumbs=[])
    page("/disclosure/", f"Affiliate Disclosure | {NAME}", "How Apostille Atlas may earn money and how that affects (and does not affect) our content.",
         f'<p>Some links on {NAME} may be affiliate links. If you use one to buy a service, such as a private apostille, courier, translation or online notary service, we may earn a commission at no extra cost to you. Affiliate links are marked with <code>rel="sponsored"</code> and appear in highlighted boxes.</p><p><strong>Current status:</strong> two affiliate partners are live, each labelled "(affiliate link)" where it appears:</p><ul><li><strong>Fingerprints &amp; Apostilles</strong> (a private service that handles FBI background check apostilles), on our <a href="/guides/fbi-background-check-apostille/">FBI background check guide</a> and <a href="/guides/us-department-of-state/">U.S. Department of State guide</a>.</li><li><strong>Apostille USA</strong> (a private service that files state and federal apostilles), on every state page, our <a href="/guides/birth-certificate-apostille/">birth certificate guide</a>, our FBI background check guide and our U.S. Department of State guide.</li></ul><p>If you order through one of these links, we may earn a referral commission at no extra cost to you. No other affiliate partnerships are active.</p><p>Including a link does not mean we have tested, ranked or endorse a service over others. It is one option alongside doing it yourself directly with the government office.</p><p>Affiliate relationships never change the official facts on a page. You can always get an apostille directly from the government office for the official fee, and every page explains how.</p><p>This disclosure is meant to follow the U.S. FTC\'s guidance on endorsements (16 CFR Part 255).</p>', h1="Affiliate disclosure",
         sources=[["FTC: Endorsement Guides (16 CFR Part 255)","https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255"]], article=False, crumbs=[])
    (OUT / "404.html").write_text(f'<!doctype html><meta charset="utf-8"><title>Not found</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/style.css"><main class="wrap"><h1>Page not found</h1><p><a href="/directory/">Go to the directory</a> · <a href="/faq/">Apostille FAQ</a></p></main>{GOAT}')
    sm = "".join(f"<url><loc>{SITE}{p['path']}</loc><lastmod>{p['lastmod']}</lastmod></url>" for p in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Googlebot", "Bingbot", "Applebot-Extended", "CCBot"]
    (OUT / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    byp = {p["path"]: p for p in PAGES}
    L = lambda p: f"- [{byp[p]['title']}]({SITE}{p}): {byp[p]['desc']}"
    llms = (f"# {NAME}\n\n> Independent, plain-language directory of U.S. apostille offices: which office apostilles a document, the official fee, processing time and what to send, "
            f"cited to official government sources. Not a government site; not legal advice. Last reviewed {LV}.\n\n"
            "Key rule: a U.S. document is apostilled by the state that issued or notarized it; federal documents (such as FBI background checks) are apostilled by the U.S. Department of State ($20 per document, Form DS-4194). "
            "Facts on each page link to the official source; where an office publishes no figure, the page says so.\n\n"
            "## Start here\n" + "\n".join(L(p) for p in ["/faq/", "/directory/", "/guides/state-or-federal-which-office/"]) +
            "\n\n## States\n" + "\n".join(L(f'/states/{s["slug"]}/') for s in states) +
            "\n\n## Guides\n" + "\n".join(L(f"/guides/{sl}/") for sl, m in guides) +
            "\n\n## Optional\n" + "\n".join(L(p) for p in ["/about/", "/disclosure/"]) + "\n")
    (OUT / "llms.txt").write_text(llms)
    print(f"Built {len(URLS)} pages ({len(states)} states, {len(guides)} guides) -> {OUT}")

if __name__ == "__main__": main()
