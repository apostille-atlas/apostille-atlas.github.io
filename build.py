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
# Outbound affiliate click events: any <a data-aff="partner-slug"> sends a cookieless GoatCounter event "aff-partner-slug".
# Guarded: does nothing if count.js has not loaded (blocked or slow); count.js sends with sendBeacon, so navigation is not delayed.
AFF_JS = ("<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-aff]');if(!a)return;"
          "try{if(window.goatcounter&&typeof goatcounter.count==='function')goatcounter.count({path:'aff-'+a.getAttribute('data-aff'),"
          "title:'Affiliate click: '+a.textContent.trim()+' ('+location.pathname+')',event:true})}catch(x){}});</script>")
# Partner facts below are quoted from each partner's own public pages (re-verified 2026-10-27); never add prices/speeds they don't publish.
AUSA_SRC = "https://apostille-usa.com/partner-registration/"
FA_SRC = "https://fingerprintsandapostilles.com/"
AUSA_ORIG = "https://apstl.us/6YBeOr"; AUSA_FED = "https://apstl.us/8jTbZ5"; FA_URL = "https://fingerprintsandapostilles.com?fpr=apostille-f818cb"
DISC = 'Disclosure: if you order through a link marked "(paid link)", we may earn a commission at no extra cost to you. See our <a href="/disclosure/">affiliate disclosure</a>.'
def alink(url, partner, slug, label):
    return f'<a href="{url}" rel="sponsored nofollow noopener" data-aff="{partner}-{slug}">{label}</a> (paid link)'
def aff_box(slug, office, fee, src, federal=False):
    """'Don't want to do it yourself?' box: DIY with the official office is cheaper; a service is optional."""
    why = "A paid service can be worth it if you are mailing from abroad, are up against a deadline, also need a translation, or don't have time to handle it."
    diy = (f'You don\'t need one: doing it yourself directly with the {e(office)} is cheaper, at the official ${fee} per document '
           f'(<a href="{src}" rel="noopener">official source</a>).')
    if federal:
        opts = (f'<li>{alink(FA_URL, "fingerprints-apostilles", slug, "Fingerprints &amp; Apostilles")}: handles FBI background check and other federal apostilles; '
                f'its site lists $120 for the first document and $95 for each additional, with U.S. return shipping included (<a href="{FA_SRC}" rel="noopener">its pricing</a>).</li>'
                f'<li>{alink(AUSA_FED, "apostille-usa", slug, "Apostille USA")}: lists its federal apostille service at $199 + shipping &amp; handling '
                f'(<a href="{AUSA_SRC}" rel="noopener">its pricing</a>).</li>')
    else:
        opts = (f'<li>{alink(AUSA_ORIG, "apostille-usa", slug, "Apostille USA")}: lists $199 + shipping &amp; handling for its 72-hour service and '
                f'$299 + shipping &amp; handling for its 24-hour service (<a href="{AUSA_SRC}" rel="noopener">its pricing</a>).</li>')
    return (f'<div class="aff aff-top"><strong>Don\'t want to do it yourself?</strong> {why} {diy}<ul>{opts}</ul>'
            f'<p class="meta">Compare options: <a href="/guides/apostille-services-compared/">DIY vs paid apostille services</a>. {DISC}</p></div>')
AFF_URLS = {"apostille-usa-orig": AUSA_ORIG, "apostille-usa-fed": AUSA_FED, "fingerprints-apostilles": FA_URL}
LOWEST_SERVICE = 120  # Federal Apostille, $120 per apostille incl. government fee (federalapostille.org/apostille-pricing/, checked 2026-10-27)
def diy_table(states):
    """DIY official fee (from data/states.json) vs the lowest published service price."""
    rows = "".join(f'<tr><td><a href="/states/{s["slug"]}/">{e(s["name"])}</a></td><td>{e(s["authority"].split(",")[0])}</td><td>${s["fee"]}</td>'
                   f'<td>{"Yes" if s["walk_in"] else "Not listed"}</td><td>${LOWEST_SERVICE - s["fee"]}</td></tr>' for s in states)
    rows += (f'<tr><td><a href="/guides/us-department-of-state/">Federal documents</a></td><td>U.S. Department of State</td><td>$20</td>'
             f'<td>Drop-off in Washington, DC</td><td>${LOWEST_SERVICE - 20}</td></tr>')
    return ('<table><thead><tr><th>Where the document is from</th><th>Office</th><th>Official fee per document (DIY)</th><th>In person</th>'
            f'<th>Extra paid with a ${LOWEST_SERVICE} service</th></tr></thead><tbody>{rows}</tbody></table>'
            '<p class="meta">Official fees from each state page (each cites its official source). Some states add fees, for example California charges a $6 in-person handling fee for each different official\'s signature, and Florida charges $20 for documents certified by a county Clerk of the Court. Your own postage is not included.</p>')
def cost_table(states):
    """Official government apostille fee per document, cheapest first, with each office's own fee details, straight from data/states.json (cited)."""
    cite = lambda s, f: " ".join(f'<a href="{e(u)}" rel="noopener" title="{e(t)}">[source]</a>' for t, u in srcs(s, f))
    order = sorted(states, key=lambda s: (s["fee"], s["name"]))
    rows = "".join(f'<tr><td><a href="/states/{s["slug"]}/">{e(s["name"])}</a></td><td><strong>${s["fee"]}</strong></td><td>${s["fee"] * 3}</td>'
                   f'<td>{e(s["fee_note"])} {cite(s, "fee")}</td></tr>' for s in order)
    rows += ('<tr><td><a href="/guides/us-department-of-state/">Federal documents</a> (U.S. Department of State)</td><td><strong>$20</strong></td><td>$60</td>'
             '<td>$20 per document, for federal documents such as FBI background checks. '
             '<a href="https://travel.state.gov/en/replace-certify/authenticate-documents/request-services.html" rel="noopener">[source]</a></td></tr>')
    return ('<div style="overflow-x:auto"><table class="data"><thead><tr><th>Where the document is from</th><th>Official fee per document</th>'
            '<th>Fee for 3 documents</th><th>Fee details from the official page</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
            '<p class="meta">Government fees only, sorted from lowest to highest. "Fee for 3 documents" is simply three times the per-document fee, before any extra fees listed in the details. '
            'Your postage, and the cost of getting a certified copy or a notarization first, are not included. The [source] link opens the official page each fee was copied from.</p>')
def walkin_table(states):
    """In-person / same-day options per covered state, straight from data/states.json (walk_in, walkin_time, addresses), each cited."""
    cite = lambda s, f: " ".join(f'<a href="{e(u)}" rel="noopener" title="{e(t)}">[source]</a>' for t, u in srcs(s, f))
    order = sorted(states, key=lambda s: (not s["walk_in"], s["name"]))
    rows = "".join(f'<tr><td><a href="/states/{s["slug"]}/">{e(s["name"])}</a></td><td>{"Yes" if s["walk_in"] else "Not listed"}</td>'
                   f'<td>{e(s["walkin_time"])} {cite(s, "walk")}</td><td>${s["fee"]}</td></tr>' for s in order)
    rows += ('<tr><td><a href="/guides/us-department-of-state/">Federal documents</a> (U.S. Department of State)</td><td>Drop-off only</td>'
             '<td>Walk-in drop-off in Washington, DC, Monday to Thursday, 7:30 to 9:00 a.m., processed within 7 business days. Same-day service only by appointment '
             'for a life-or-death family emergency abroad with travel within 2 weeks. <a href="https://travel.state.gov/en/replace-certify/authenticate-documents/request-services.html" rel="noopener">[source]</a></td><td>$20</td></tr>')
    return ('<div style="overflow-x:auto"><table class="data"><thead><tr><th>Where the document is from</th><th>In person?</th><th>What the official page says about in-person and same-day service</th>'
            f'<th>Official fee per document</th></tr></thead><tbody>{rows}</tbody></table></div>'
            '<p class="meta">Copied from each office\'s official page (the [source] link opens it). Addresses and hours are on each state page. Offices change hours and rules, so check the official page the day before you go.</p>')
ORG_ID = SITE + "/#org"
ORG_FULL = {"@type": "Organization", "@id": ORG_ID, "name": NAME, "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/apple-touch-icon.png", "width": 180, "height": 180},
            "email": C["contact_email"], "description": C["tagline"]}
ORG = {"@id": ORG_ID}
OG_IMG = SITE + "/og.png"
CSS = (R / "static/style.css").read_text().replace("\n", "")  # inlined: no render-blocking stylesheet request
# U.S. state adjacency (land borders), used for "nearby states" links between covered state pages.
NEIGHBORS = {"alabama": "florida georgia mississippi tennessee", "alaska": "", "arizona": "california colorado nevada new-mexico utah",
 "arkansas": "louisiana mississippi missouri oklahoma tennessee texas", "california": "arizona nevada oregon",
 "colorado": "arizona kansas nebraska new-mexico oklahoma utah wyoming", "connecticut": "massachusetts new-york rhode-island",
 "delaware": "maryland new-jersey pennsylvania", "district-of-columbia": "maryland virginia", "florida": "alabama georgia",
 "georgia": "alabama florida north-carolina south-carolina tennessee", "hawaii": "", "idaho": "montana nevada oregon utah washington wyoming",
 "illinois": "indiana iowa kentucky missouri wisconsin", "indiana": "illinois kentucky michigan ohio", "iowa": "illinois minnesota missouri nebraska south-dakota wisconsin",
 "kansas": "colorado missouri nebraska oklahoma", "kentucky": "illinois indiana missouri ohio tennessee virginia west-virginia",
 "louisiana": "arkansas mississippi texas", "maine": "new-hampshire", "maryland": "delaware district-of-columbia pennsylvania virginia west-virginia",
 "massachusetts": "connecticut new-hampshire new-york rhode-island vermont", "michigan": "indiana ohio wisconsin",
 "minnesota": "iowa north-dakota south-dakota wisconsin", "mississippi": "alabama arkansas louisiana tennessee",
 "missouri": "arkansas illinois iowa kansas kentucky nebraska oklahoma tennessee", "montana": "idaho north-dakota south-dakota wyoming",
 "nebraska": "colorado iowa kansas missouri south-dakota wyoming", "nevada": "arizona california idaho oregon utah",
 "new-hampshire": "maine massachusetts vermont", "new-jersey": "delaware new-york pennsylvania", "new-mexico": "arizona colorado oklahoma texas utah",
 "new-york": "connecticut massachusetts new-jersey pennsylvania vermont", "north-carolina": "georgia south-carolina tennessee virginia",
 "north-dakota": "minnesota montana south-dakota", "ohio": "indiana kentucky michigan pennsylvania west-virginia",
 "oklahoma": "arkansas colorado kansas missouri new-mexico texas", "oregon": "california idaho nevada washington",
 "pennsylvania": "delaware maryland new-jersey new-york ohio west-virginia", "rhode-island": "connecticut massachusetts",
 "south-carolina": "georgia north-carolina", "south-dakota": "iowa minnesota montana nebraska north-dakota wyoming",
 "tennessee": "alabama arkansas georgia kentucky mississippi missouri north-carolina virginia", "texas": "arkansas louisiana new-mexico oklahoma",
 "utah": "arizona colorado idaho nevada new-mexico wyoming", "vermont": "massachusetts new-hampshire new-york",
 "virginia": "district-of-columbia kentucky maryland north-carolina tennessee west-virginia", "washington": "idaho oregon",
 "west-virginia": "kentucky maryland ohio pennsylvania virginia", "wisconsin": "illinois iowa michigan minnesota", "wyoming": "colorado idaho montana nebraska south-dakota utah"}
HIGH_DEMAND = ["california", "new-york", "texas", "florida", "illinois"]  # most-asked states in research/questions.md
strip = lambda h: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
AN = lambda n: ("an " if n[:1] in "AEIO" else "a ") + n  # "an Ohio", "a Utah"
NICE = lambda d: __import__("datetime").date.fromisoformat(d).strftime("%B %-d, %Y")

def faq_html(faqs):
    if not faqs: return ""
    return '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(
        f'<h3>{e(q)}</h3><p>{a}</p>' for q, a in faqs) + "</section>"

def page(path, title, desc, body, h1=None, sources=None, schema=None, summary=None, faqs=None,
         crumbs=None, article=True, reviewed=None, related=None, noindex=False):
    """Write one page. title must be < 60 chars. summary = 2-3 sentence direct answer (confirmed facts only).
    faqs = [[question, answer_html], ...] from real questions (research/questions.md). crumbs = [(name, path), ...]."""
    assert len(title) < 60, f"title too long ({len(title)}): {title}"
    assert len(desc) <= 155, f"description too long ({len(desc)}): {desc}"
    url = SITE + path; rv = reviewed or LV
    if not noindex: PAGES.append(dict(path=path, title=title, desc=desc, lastmod=rv, summary=summary, faqs=faqs))
    src = ""
    if sources:
        src = '<section class="sources"><h2>Official sources</h2><ul>' + "".join(
            f'<li><a href="{e(u)}" rel="noopener">{e(t)}</a></li>' for t, u in sources) + \
            f'</ul><p class="meta">Last checked against official sources: {rv}. Fees and procedures change, so confirm with the office before sending anything.</p></section>'
    graph = []
    if schema: graph += schema if isinstance(schema, list) else [schema]
    if article and h1:
        graph.append({"@type": "Article", "headline": h1, "description": desc, "url": url, "mainEntityOfPage": url,
                      "datePublished": C.get("launched", LV), "dateModified": rv, "author": ORG, "publisher": ORG, "inLanguage": "en-US",
                      "image": OG_IMG, "isPartOf": {"@id": SITE + "/#website"}})
    if (not article or not h1) and not noindex:
        graph.append({"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-US",
                      "isPartOf": {"@id": SITE + "/#website"}, "dateModified": rv, "publisher": ORG})
    if crumbs is not None:
        trail = [("Home", "/")] + crumbs + [(h1 or title, path)]
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]})
    if faqs:
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                      "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]})
    if graph and not noindex:
        site = {"@type": "WebSite", "@id": SITE + "/#website", "name": NAME, "url": SITE + "/", "description": C["tagline"], "inLanguage": "en-US", "publisher": ORG}
        ids = {g.get("@id") for g in graph}
        graph += [n for n in (site, ORG_FULL) if n["@id"] not in ids]
    for g in graph: g.pop("@context", None)
    ld = f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph})}</script>' if graph else ""
    bc = ""
    if crumbs is not None:
        bc = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>' + "".join(' › ' + f'<a href="{p}">{e(n)}</a>' for n, p in crumbs) + "</nav>"
    top = ""
    if h1:
        top = bc + f'<h1>{e(h1)}</h1>'
        if (reviewed is not None or sources or summary) and not noindex: top += f'<p class="meta">Last reviewed: <time datetime="{rv}">{NICE(rv)}</time></p>'
    if summary: top += f'<div class="answer"><strong>Short answer:</strong> {e(summary)}</div>'
    rel = ""
    if related:
        rel = '<section class="related"><h2>Related pages</h2><ul>' + "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in related) + "</ul></section>"
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google-site-verification" content="YmyOw7HPo4pJcKqyHGGfO-omSdR1MkXOuEQz_9bi9z4" />
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta name="robots" content="{'noindex' if noindex else 'index,follow,max-snippet:-1,max-image-preview:large'}">{'' if noindex else f'<link rel="canonical" href="{url}">'}
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="{'article' if article and h1 else 'website'}"><meta property="og:image" content="{OG_IMG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{NAME}: U.S. apostille offices by state"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{OG_IMG}">{f'<meta property="article:modified_time" content="{rv}">' if article and h1 else ''}
<style>{CSS}</style>{ld}</head><body>
<header><div class="wrap"><a class="brand" href="/">{NAME}</a><nav><a href="/directory/">Directory</a><a href="/apostille-fees-by-state/">Fees &amp; times</a><a href="/faq/">FAQ</a><a href="/guides/">Guides</a><a href="/guides/state-or-federal-which-office/">Which office?</a><a href="/guides/hague-apostille-countries/">Hague countries</a><a href="/guides/apostille-services-compared/">DIY vs service</a><a href="/about/">About</a></nav></div></header>
<main class="wrap">{top}{body}{faq_html(faqs)}{rel}{src}</main>
<footer><div class="wrap">{NAME} is an independent guide, not a government website, and not legal advice. <a href="/disclosure/">Affiliate disclosure</a> · <a href="/about/">About</a> · <a href="/faq/">FAQ</a> · <a href="/sitemap.xml">Sitemap</a></div></footer>
{GOAT}{AFF_JS if 'data-aff=' in body else ''}
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
    have = {o["slug"]: o for o in states}
    near = [have[x] for x in NEIGHBORS.get(s["slug"], "").split() if x in have]
    pop = [have[x] for x in HIGH_DEMAND if x in have and x != s["slug"] and have[x] not in near]
    card = lambda o: f'<a class="card" href="/states/{o["slug"]}/"><strong>{e(o["name"])} apostille</strong><small>${o["fee"]}/doc · {e(o["authority"].split(",")[0])}</small></a>'
    nearby = ""
    if near: nearby += f'<h2>Apostilles in states near {e(s["name"])}</h2><div class="cards">' + "".join(card(o) for o in near) + "</div>"
    if pop: nearby += '<h2>Most-requested state apostille offices</h2><div class="cards">' + "".join(card(o) for o in pop) + "</div>"
    n = e(s["name"])
    return (f'<p class="lede">How to get an apostille on {AN(n)} document: which office issues it, the official fee (${s["fee"]} per document), how long it takes, and what to send. Every fact comes from the official {n} source listed at the bottom.</p>'
            + aff_box(s["slug"], s["authority"], s["fee"], s["sources"][0][1]) +
            f'<h2>Where do I send {AN(n)} apostille request, what does it cost, and how long does it take?</h2><table class="facts">{t}</table>'
            f'<h2>What do I need to send for {AN(n)} apostille?</h2><ol>{li(s["what_to_send"])}</ol>'
            f'<h2>What trips people up with {n} apostilles?</h2><ul>{li(s["tips"])}</ul>'
            '<h2>Is my document state or federal?</h2><p>If a federal agency signed it, such as an FBI background check, it goes to the <a href="/guides/us-department-of-state/">U.S. Department of State</a>, not the state. Not sure? See <a href="/guides/state-or-federal-which-office/">state or federal: which office?</a> Also check whether the destination country <a href="/guides/hague-apostille-countries/">accepts apostilles</a>.</p>'
            + nearby +
            f'<p class="meta">Document from another state? Each state only apostilles its own documents: {others}, or the full <a href="/directory/">directory</a>.</p>')

def state_faqs(s):
    n = s["name"]
    return [[f"Where do I get an apostille in {n}?", f'From the {e(s["authority"])}. Documents issued or notarized in {e(n)} are apostilled there, no matter where you live now.'],
            [f"How much does {AN(n)} apostille cost?", e(s["fee_note"])],
            [f"How long does {AN(n)} apostille take?", f'By mail: {e(s["mail_time"])} In person: {e(s["walkin_time"])}'],
            [f"Can I get {AN(n)} apostille in person or same day?", e(s["walkin_time"]) if s["walk_in"] else f'The official {e(n)} page does not describe walk-in service: {e(s["walkin_time"])}'],
            [f"Can {n} apostille my FBI background check?", f'No. FBI background checks are federal documents, so the <a href="/guides/us-department-of-state/">U.S. Department of State</a> apostilles them, not {e(n)}.'],
            [f"Can {n} apostille a document from another state?", "No. A state only apostilles documents issued or notarized in that state. Send a document from another state to that state's office (see the <a href=\"/directory/\">directory</a>)."]]

# Which listed official source backs each value on the fees & times data page, for states that list more than one source.
# Index into that state's "sources" list (checked against the official pages on 2026-10-27). States not listed here have
# a single source, which backs every value. A list of indexes means the value is backed by those sources together.
SRC_FOR = {"texas": {"fee": [3], "mail": [1], "walk": [1]},          # fee: Authentication FAQs; times/walk-in: Request a Universal Apostille
           "north-carolina": {"fee": [0], "mail": [1], "walk": [1]},  # fee: Authentications fees; process page links Turn Around Times
           "new-jersey": {"fee": [1], "mail": [0], "walk": [0]},      # fee: Registry Fee Schedules; online service + drop-off: apostilles page
           "ohio": {"fee": [0, 1, 3], "mail": [0, 1], "walk": [2]}}   # walk-in: Form 8003 (per data note); others: listed Ohio pages
DATA_PATH = "/apostille-fees-by-state/"; CSV_NAME = "apostille-fees-by-state.csv"
def srcs(s, field):
    idx = SRC_FOR.get(s["slug"], {}).get(field) or list(range(len(s["sources"])))
    return [s["sources"][i] for i in idx]
def data_page(states):
    """Original cross-state dataset: every value comes from data/states.json and links to the official source it came from."""
    import csv, io
    cite = lambda s, f: " ".join(f'<a href="{e(u)}" rel="noopener" title="{e(t)}">[source]</a>' for t, u in srcs(s, f))
    rows = "".join(
        f'<tr><td><a href="/states/{s["slug"]}/">{e(s["name"])}</a></td><td>{e(s["authority"])}</td>'
        f'<td><strong>${s["fee"]}</strong> {cite(s, "fee")}<br><small>{e(s["fee_note"])}</small></td>'
        f'<td>{e(s["mail_time"])} {cite(s, "mail")}</td>'
        f'<td>{"Yes" if s["walk_in"] else "Not listed"}: {e(s["walkin_time"])} {cite(s, "walk")}</td>'
        f'<td><time datetime="{s["last_reviewed"]}">{s["last_reviewed"]}</time></td></tr>' for s in states)
    buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n")
    w.writerow(["state", "abbr", "issuing_office", "fee_usd_per_document", "fee_details", "fee_source_url", "mail_available",
                "mail_processing_time", "mail_time_source_url", "in_person_available", "in_person_details", "in_person_source_url",
                "last_reviewed", "state_page_url"])
    for s in states:
        j = lambda f: " | ".join(u for t, u in srcs(s, f))
        w.writerow([s["name"], s["abbr"], s["authority"], s["fee"], s["fee_note"], j("fee"), "yes" if s["mail"] else "not listed",
                    s["mail_time"], j("mail"), "yes" if s["walk_in"] else "not listed", s["walkin_time"], j("walk"),
                    s["last_reviewed"], f'{SITE}/states/{s["slug"]}/'])
    (OUT / CSV_NAME).write_text(buf.getvalue())
    fees = sorted(states, key=lambda s: s["fee"]); lo, hi = fees[0], fees[-1]
    newest = max(s["last_reviewed"] for s in states); oldest = min(s["last_reviewed"] for s in states)
    walk = sum(1 for s in states if s["walk_in"])
    body = (f'<p class="lede">Official apostille fees, mail processing times and in-person options for the {len(states)} U.S. states we cover so far, '
            'side by side. Every value is copied from the state\'s own official page, and the [source] link next to it opens that page.</p>'
            f'<p><a href="/{CSV_NAME}" download><strong>Download the data (CSV) →</strong></a> · Free to reuse; please link to this page as the source.</p>'
            '<h2>Apostille fee, processing time and in-person service by state</h2>'
            '<div style="overflow-x:auto"><table class="data"><thead><tr><th>State</th><th>Issuing office</th><th>Official fee per document</th>'
            f'<th>By mail: processing time</th><th>In person</th><th>Last checked</th></tr></thead><tbody>{rows}</tbody></table></div>'
            '<h2>How was this data collected?</h2><ul>'
            '<li>Each value comes from the state\'s official apostille page, fee schedule, FAQ or request form, linked next to the value and on the state\'s own page.</li>'
            '<li>Where an office does not publish a figure, such as a mail processing time, the table says so instead of estimating one.</li>'
            '<li>"Last checked" is the date the state\'s values were last compared with the official source. Fees and times change, so confirm with the office before sending anything.</li>'
            '<li>Fees are per document, in U.S. dollars, and exclude your own postage. Extra fees (adoption rates, in-person handling or expedite fees) are in the fee details.</li>'
            '<li>Only states we have fully checked are included. More are added over time.</li></ul>'
            '<p>Federal documents, such as FBI background checks, are not apostilled by any state: see the <a href="/guides/us-department-of-state/">U.S. Department of State guide</a>. '
            'To filter offices by fee or walk-in, use the <a href="/directory/">directory</a>. To compare doing it yourself with a paid service, see <a href="/guides/apostille-services-compared/">DIY vs paid apostille services</a>.</p>'
            '<p class="meta">Found a value that no longer matches the official page? See <a href="/about/#corrections">how to report a correction</a>.</p>')
    summary = (f"Among the {len(states)} states covered, official apostille fees range from ${lo['fee']} per document ({lo['name']}) to ${hi['fee']} ({hi['name']}). "
               f"{walk} of the {len(states)} offices describe an in-person option on their official pages. Each value links to its official source, and the full table is downloadable as CSV.")
    allsrc, seen = [], set()
    for s in states:
        for t, u in s["sources"]:
            if u not in seen: seen.add(u); allsrc.append([t, u])
    schema = {"@type": "Dataset", "name": "U.S. state apostille fees and processing times", "description":
              f"Official apostille fee per document, fee details, mail processing time and in-person options for {len(states)} U.S. states, each value with the URL of the official government source it was taken from.",
              "url": SITE + DATA_PATH, "creator": ORG, "publisher": ORG, "isAccessibleForFree": True, "inLanguage": "en-US",
              "license": "https://creativecommons.org/licenses/by/4.0/", "dateModified": newest, "temporalCoverage": f"{oldest}/{newest}",
              "spatialCoverage": {"@type": "Place", "name": "United States"},
              "keywords": ["apostille", "apostille fees", "Secretary of State", "processing times", "United States"],
              "isBasedOn": [u for t, u in allsrc],
              "variableMeasured": ["Official fee per document (USD)", "Mail processing time", "In-person service"],
              "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": SITE + "/" + CSV_NAME}]}
    page(DATA_PATH, "Apostille Fees & Processing Times by State (Data)",
         f"Official apostille fees, mail processing times and in-person options for {len(states)} U.S. states, each value linked to its source. Free CSV download.",
         body, h1="Apostille fees and processing times by state", sources=allsrc, summary=summary, crumbs=[("Directory", "/directory/")],
         reviewed=newest, schema=schema,
         related=[(n, p) for n, p in GUIDE_LINKS] + [(f'{s["name"]} apostille', f'/states/{s["slug"]}/') for s in states])

GUIDE_LINKS = [("Apostille FAQ", "/faq/"), ("State or federal: which office?", "/guides/state-or-federal-which-office/"),
               ("Birth certificate apostille", "/guides/birth-certificate-apostille/"), ("FBI background check apostille", "/guides/fbi-background-check-apostille/"), ("Fastest way to apostille an FBI check", "/guides/fastest-fbi-background-check-apostille/"),
               ("U.S. Department of State (federal)", "/guides/us-department-of-state/"), ("Which countries accept apostilles?", "/guides/hague-apostille-countries/"),
               ("Apostille services compared: DIY vs paid", "/guides/apostille-services-compared/"), ("Apostille for Spain", "/guides/apostille-for-spain/"), ("Same-day and walk-in apostille offices", "/guides/same-day-and-walk-in-apostille-offices/"), ("How much does an apostille cost?", "/guides/apostille-cost-by-state/"),
               ("Apostille fees and processing times by state (data)", "/apostille-fees-by-state/"),
               ("Apostille directory by state", "/directory/")]

def main():
    global URLS, PAGES; URLS = []; PAGES = []
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(); shutil.copy(R / "static/style.css", OUT / "style.css")
    for k in (R / "static").iterdir():
        if k.suffix in (".txt", ".png", ".ico", ".svg"): shutil.copy(k, OUT / k.name)  # IndexNow key, favicons, OG image
    states = [s for s in json.loads((R / "data/states.json").read_text()) if not s.get("draft") and s.get("sources")]
    states.sort(key=lambda s: s["name"])
    for s in states:
        title = f'{s["name"]} Apostille: Where to Go, ${s["fee"]} Fee & Steps'
        rel = [(n, p) for n, p in GUIDE_LINKS if p != "/directory/"]
        auth = s["authority"].split(",")[0]
        desc = f'How to get {AN(s["name"])} apostille: {auth}, ${s["fee"]} per document, mail{" and walk-in" if s["walk_in"] else ""} options and what to send. Official sources.'
        if len(desc) > 155: desc = f'{s["name"]} apostille: {auth}, ${s["fee"]} per document, how to apply and what to send. Official sources.'
        page(f'/states/{s["slug"]}/', title, desc,
             state_body(s, states), h1=f'{s["name"]} apostille: where to go, fee and steps', sources=s["sources"],
             summary=s.get("summary"), faqs=state_faqs(s), crumbs=[("States", "/directory/")], reviewed=s.get("last_reviewed", LV), related=rel,
             schema={"@type":"HowTo","name":f'Get an apostille in {s["name"]}',"step":[{"@type":"HowToStep","text":x} for x in s["what_to_send"]]})
    data_page(states)
    guides = []
    for g in sorted((R / "content/guides").glob("*.html")):
        raw = g.read_text(); m = re.match(r"<!--(.*?)-->\s*", raw, re.S)
        meta = json.loads(m.group(1))
        if meta.get("draft") or not meta.get("sources"):
            print("SKIP (draft or no sources):", g.name, file=sys.stderr); continue
        slug = g.stem; guides.append((slug, meta))
        rel = [(n, p) for n, p in GUIDE_LINKS if p != f"/guides/{slug}/"] + [(f'{s["name"]} apostille', f'/states/{s["slug"]}/') for s in states]
        gbody = raw[m.end():].replace("<!--AFF_BOX_FEDERAL-->", aff_box(slug, "U.S. Department of State Office of Authentications", 20,
                "https://travel.state.gov/en/replace-certify/authenticate-documents/request-services.html", federal=True))
        gbody = gbody.replace("<!--DIY_TABLE-->", diy_table(states)).replace("<!--WALKIN_TABLE-->", walkin_table(states)).replace("<!--COST_TABLE-->", cost_table(states))
        gbody = re.sub(r"<!--AFF:([a-z-]+):(.*?)-->", lambda mm: alink(AFF_URLS[mm.group(1)], mm.group(1).replace("-orig", ""), slug, mm.group(2)), gbody)
        page(f'/guides/{slug}/', meta["title"], meta["description"], gbody, h1=meta["h1"], sources=meta["sources"],
             summary=meta.get("summary"), faqs=meta.get("faqs"), crumbs=[("Guides", "/guides/")], reviewed=meta.get("last_reviewed", LV), related=rel)
    gcards = "".join(f'<a class="card" href="/guides/{sl}/"><span class="badge">{e(m["category"])}</span><br><strong>{e(m["h1"])}</strong></a>' for sl, m in guides)
    scards = "".join(f'<a class="card" href="/states/{s["slug"]}/"><strong>{e(s["name"])}</strong><small>${s["fee"]}/doc · {e(s["authority"].split(",")[0])}</small></a>' for s in states)
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
         crumbs=[("Guides", "/guides/")], related=[(n, p) for n, p in GUIDE_LINKS if p != "/faq/"] + [(f'{s["name"]} apostille', f'/states/{s["slug"]}/') for s in states])
    # FAQPage JSON-LD for the hub (answers as plain text, without inline citations)
    hub = OUT / "faq/index.html"; d = hub.read_text()
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a, ss in fq["items"]]}
    d = d.replace('"@graph": [', '"@graph": [' + json.dumps(ld) + ", ", 1); hub.write_text(d)
    # guides index
    page("/guides/", f"Apostille Guides: Documents, Offices, Countries", "Plain-language apostille guides for U.S. documents: birth certificates, FBI checks, federal documents, Hague countries and which office to use.",
         f'<p class="lede">Guides for specific documents and situations. Each one cites official government sources.</p><div class="cards">{gcards}</div><h2>Looking for a state?</h2><div class="cards">{scards}</div><p>Or open the full <a href="/directory/">apostille directory</a>, or compare every state\'s <a href="/apostille-fees-by-state/">fees and processing times</a> (with CSV download).</p>',
         h1="Apostille guides", crumbs=[], article=False, reviewed=LV,
         summary="Start with the office: state and locally issued or notarized documents are apostilled by that state, and federal documents such as FBI checks by the U.S. Department of State. Then check whether your destination country accepts apostilles at all.")
    # directory
    rows = "".join(f'<tr data-name="{e(s["name"].lower())} {s["abbr"].lower()}" data-fee="{s["fee"]}" data-walkin="{int(s["walk_in"])}"><td><a href="/states/{s["slug"]}/">{e(s["name"])}</a></td><td>{e(s["authority"])}</td><td>${s["fee"]}</td><td>{"Yes" if s["walk_in"] else "Not listed"}</td></tr>' for s in states)
    js = """<script>const q=document.getElementById('q'),f=document.getElementById('fee'),w=document.getElementById('walk'),o=document.getElementById('feeval');
function run(){o.textContent='$'+f.value;document.querySelectorAll('#tbl tbody tr').forEach(r=>{const ok=r.dataset.name.includes(q.value.toLowerCase().trim())&&(+r.dataset.fee<=+f.value)&&(!w.checked||r.dataset.walkin==='1');r.style.display=ok?'':'none'})}
[q,f,w].forEach(x=>x.addEventListener('input',run));run();</script>"""
    maxfee = max(s["fee"] for s in states); minfee = min(s["fee"] for s in states)
    dbody = (f'<p class="lede">Apostille offices by state, plus the federal office. {len(states)} states covered so far, with one new page added regularly. Use the filters to narrow the list, or compare <a href="/apostille-fees-by-state/">fees and processing times side by side</a> (CSV download).</p>'
             f'<div class="filters"><input id="q" type="search" placeholder="Search state…" aria-label="Search state"><label>Max fee <input id="fee" type="range" min="1" max="{maxfee}" value="{maxfee}"> <span id="feeval"></span></label><label><input id="walk" type="checkbox"> Walk-in available</label></div>'
             f'<h2>Which office handles my state\'s apostilles?</h2><table id="tbl"><thead><tr><th>State</th><th>Issuing office</th><th>Fee / doc</th><th>Walk-in</th></tr></thead><tbody>{rows}</tbody></table>'
             f'<h2>Where do federal documents go?</h2><p><a href="/guides/us-department-of-state/">U.S. Department of State Office of Authentications</a>: $20 per document, for FBI checks and other federal records.</p>'
             f'<h2>Guides by category</h2><div class="cards">{gcards}</div>' + js)
    page("/directory/", "Apostille Directory by State: Offices, Fees, Walk-in", "Compare U.S. state apostille offices: issuing office, fee per document and walk-in availability, from official sources.", dbody,
         h1="Apostille directory", crumbs=[], article=False, reviewed=LV,
         schema={"@type": "ItemList", "name": "U.S. apostille offices by state", "numberOfItems": len(states), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": f'{s["name"]} apostille', "url": f'{SITE}/states/{s["slug"]}/'} for i, s in enumerate(states)]},
         summary=f"There is no single national apostille office: each state apostilles its own documents, and the U.S. Department of State handles federal ones for $20. Among the {len(states)} states covered so far, official fees range from ${minfee} to ${maxfee} per document.")
    home = (f'<p class="lede">{e(C["tagline"])} Requests get sent back when a document goes to the wrong office or misses a prep step.</p>'
            '<p><a href="/directory/"><strong>Open the directory →</strong></a> · <a href="/apostille-fees-by-state/"><strong>Compare fees and processing times →</strong></a> · <a href="/faq/"><strong>Read the apostille FAQ →</strong></a></p>'
            '<h2>Start here</h2><ol><li><a href="/guides/state-or-federal-which-office/">Is your document state or federal?</a></li><li><a href="/guides/hague-apostille-countries/">Does the destination country accept apostilles?</a></li><li>Open your state below.</li></ol>'
            f'<h2>States</h2><div class="cards">{scards}<a class="card" href="/guides/us-department-of-state/"><strong>Federal (U.S. Dept. of State)</strong><small>$20/doc · FBI checks, federal records</small></a></div>'
            f'<h2>Guides</h2><div class="cards">{gcards}</div>')
    page("/", f"{NAME}: U.S. Apostille Offices by State", "Find the right U.S. apostille office for your document: official fees, addresses, processing times and requirements by state, cited to government sources.", home,
         article=False, reviewed=LV,
         h1="Get the apostille right the first time",
         summary="A U.S. document is apostilled by the state that issued or notarized it, or by the U.S. Department of State if it is federal (such as an FBI background check). This site lists each office's official fee, address, processing time and requirements, with a link to the government source.")
    page("/about/", f"About {NAME}: How Pages Are Made", f"Who runs {NAME}, how pages are drafted and fact-checked, how the site earns money, and how to report a correction.",
         f'<p>{NAME} is an independent, plain-language directory of U.S. apostille offices. It is <strong>not</strong> a government website, is not affiliated with any government office, and does not give legal advice.</p>'
         '<h2 id="how">How are pages made?</h2><ul>'
         '<li><strong>Drafted with AI assistance.</strong> Pages are drafted with the help of AI tools. We say so because you should know how the content is produced.</li>'
         '<li><strong>Every fact is checked against the official page.</strong> Before a page is published, each fee, address, processing time and requirement is checked against the official government page linked under "Official sources" on that same page. A page without an official source is not published.</li>'
         '<li><strong>No guessing.</strong> We don\'t publish estimated prices or processing times. Where an office doesn\'t publish a figure, the page says so.</li>'
         '<li><strong>Honest dates.</strong> "Last reviewed" shows when a page was last compared with its official sources. We change it only after a real re-check, not to make a page look fresh.</li>'
         '<li><strong>Real questions.</strong> The questions answered on the site come from questions people ask in forums and on official FAQ pages.</li>'
         '<li><strong>No invented experts.</strong> The site is not written by a lawyer or a former government official, and we don\'t claim credentials we don\'t have. Its value is that it puts the official facts in one place, with the source next to each one.</li></ul>'
         '<p>You can see the facts side by side, with a source link next to each value, on the <a href="/apostille-fees-by-state/">fees and processing times by state</a> page (also downloadable as CSV).</p>'
         '<h2 id="money">How does the site make money?</h2><p>Only through affiliate commissions. Some pages link to private apostille services; those links are labelled "(paid link)" and marked <code>rel="sponsored"</code>. If you order through one, we may earn a commission at no extra cost to you. There are no ads, and nobody pays to be listed. Every page explains how to do it yourself directly with the government office for the official fee, which is usually the cheapest option. Commissions never change the official facts on a page. Details: <a href="/disclosure/">affiliate disclosure</a>.</p>'
         '<h2>Privacy</h2><p>This site uses privacy-friendly, cookieless analytics (GoatCounter) to count page views, plus anonymous counts of clicks on paid links (which partner, from which page). No cookies, no personal data, no cross-site tracking.</p>'
         f'<h2 id="corrections">How do I report a correction?</h2><p>Offices change fees, addresses and procedures, and links break. If something on a page no longer matches the official source, email <a href="mailto:{C["contact_email"]}">{C["contact_email"]}</a> with:</p><ol><li>the page on this site (its URL),</li><li>what is wrong or out of date, and</li><li>a link to the official government page that shows the current information, if you have one.</li></ol><p>We check the report against the official source and, if it is right, fix the page and update its "Last reviewed" date. We don\'t change a fact based on a report alone without confirming it on the official page.</p>',
         h1=f"About {NAME}", article=False, crumbs=[], reviewed=LV,
         summary=f"{NAME} is an independent, plain-language directory of U.S. apostille offices, not a government website. Pages are drafted with AI assistance, and every fee, address, processing time and requirement is checked against the official government page linked on that page. The site earns money only from affiliate commissions on clearly labelled paid links.")
    page("/disclosure/", f"Affiliate Disclosure | {NAME}", "How Apostille Atlas may earn money and how that affects (and does not affect) our content.",
         f'<p>Some links on {NAME} may be affiliate links. If you use one to buy a service, such as a private apostille, courier, translation or online notary service, we may earn a commission at no extra cost to you. Affiliate links are marked with <code>rel="sponsored"</code> and appear in highlighted boxes. We count clicks on them anonymously with cookieless GoatCounter (only which partner and which page, never who clicked) to see which pages are useful.</p><p><strong>Current status:</strong> two affiliate partners are live, each labelled "(paid link)" where it appears:</p><ul><li><strong>Fingerprints &amp; Apostilles</strong> (a private service that handles FBI background check apostilles), on our <a href="/guides/fbi-background-check-apostille/">FBI background check guide</a>, <a href="/guides/fastest-fbi-background-check-apostille/">fastest FBI check apostille guide</a>, <a href="/guides/us-department-of-state/">U.S. Department of State guide</a>, <a href="/guides/apostille-for-spain/">Spain guide</a> and <a href="/guides/apostille-services-compared/">apostille services comparison</a>.</li><li><strong>Apostille USA</strong> (a private service that files state and federal apostilles), on every state page, our <a href="/guides/birth-certificate-apostille/">birth certificate guide</a>, our FBI background check guides, our U.S. Department of State guide, our Spain guide and our apostille services comparison.</li></ul><p>If you order through one of these links, we may earn a referral commission at no extra cost to you. No other affiliate partnerships are active. Our services comparison also lists services we have no relationship with, because they publish clear prices; we earn nothing from them.</p><p>Including a link does not mean we have tested, ranked or endorse a service over others. It is one option alongside doing it yourself directly with the government office.</p><p>Affiliate relationships never change the official facts on a page. You can always get an apostille directly from the government office for the official fee, and every page explains how.</p><p>This disclosure is meant to follow the U.S. FTC\'s guidance on endorsements (16 CFR Part 255).</p>', h1="Affiliate disclosure", reviewed=LV,
         summary="Some links on this site are affiliate links, labelled \"(paid link)\", for two partners: Fingerprints & Apostilles and Apostille USA. If you order through one, we may earn a commission at no extra cost to you. It never changes the official facts on a page.",
         sources=[["FTC: Endorsement Guides (16 CFR Part 255)","https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255"]], article=False, crumbs=[])
    page("/404.html", f"Page not found | {NAME}", "This page does not exist. Find your state's apostille office in the directory or read the apostille FAQ.",
         f'<p class="lede">That page doesn\'t exist or has moved.</p><h2>Find what you need</h2><ul><li><a href="/directory/">Apostille directory by state</a></li><li><a href="/faq/">Apostille FAQ</a></li><li><a href="/guides/">All guides</a></li><li><a href="/guides/state-or-federal-which-office/">State or federal: which office?</a></li></ul><div class="cards">{scards}</div>',
         h1="Page not found", article=False, noindex=True)
    sm = "".join(f"<url><loc>{SITE}{p['path']}</loc><lastmod>{p['lastmod']}</lastmod></url>" for p in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended", "CCBot", "Perplexity-User", "Amazonbot", "DuckAssistBot", "Meta-ExternalAgent", "MistralAI-User", "YouBot"]
    (OUT / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    byp = {p["path"]: p for p in PAGES}
    L = lambda p: f"- [{byp[p]['title']}]({SITE}{p}): {byp[p]['desc']}"
    llms = (f"# {NAME}\n\n> Independent, plain-language directory of U.S. apostille offices: which office apostilles a document, the official fee, processing time and what to send, "
            f"cited to official government sources. Not a government site; not legal advice. Last reviewed {LV}.\n\n"
            "Key rule: a U.S. document is apostilled by the state that issued or notarized it; federal documents (such as FBI background checks) are apostilled by the U.S. Department of State ($20 per document, Form DS-4194). "
            "Facts on each page link to the official source; where an office publishes no figure, the page says so.\n\n"
            "## Start here\n" + "\n".join(L(p) for p in ["/faq/", "/directory/", "/apostille-fees-by-state/", "/guides/state-or-federal-which-office/", "/guides/apostille-services-compared/"]) +
            "\n\n## States\n" + "\n".join(L(f'/states/{s["slug"]}/') for s in states) +
            "\n\n## Guides\n" + "\n".join(L(f"/guides/{sl}/") for sl, m in guides) +
            "\n\n## Optional\n" + "\n".join(L(p) for p in ["/about/", "/disclosure/"]) + f"\n- [Fees and processing times data (CSV)]({SITE}/{CSV_NAME}): fees, processing times and in-person options by state, with source URLs per value\n")
    llms = llms.replace("\n\n## Optional\n", "\n\n## Key facts by state (official fee per document)\n" + "\n".join(
        f'- {s["name"]}: {s["authority"]}; ${s["fee"]} per document; {"walk-in available" if s["walk_in"] else "by mail"}. Details: {SITE}/states/{s["slug"]}/' for s in states) +
        f"\n- Federal documents (FBI checks etc.): U.S. Department of State Office of Authentications; $20 per document; Form DS-4194. Details: {SITE}/guides/us-department-of-state/" +
        f"\n\n## Full text\n- [llms-full.txt]({SITE}/llms-full.txt): every page's short answer and FAQ answers in plain text\n\n## Optional\n", 1)
    (OUT / "llms.txt").write_text(llms)
    full = [f"# {NAME}: full text of short answers and FAQs\n\nIndependent guide, not a government site, not legal advice. Every fact is cited on its page to an official source. Last reviewed {LV}.\n"]
    for pg in PAGES:
        if not (pg["summary"] or pg["faqs"]): continue
        full.append(f"\n## {pg['title']}\nURL: {SITE}{pg['path']}\nLast reviewed: {pg['lastmod']}\n")
        if pg["summary"]: full.append(f"Short answer: {pg['summary']}\n")
        for q, a in (pg["faqs"] or []): full.append(f"\nQ: {q}\nA: {strip(a)}\n")
    full.append("\n## Apostille FAQ (hub)\nURL: " + SITE + "/faq/\n" + "".join(f"\nQ: {q}\nA: {strip(a)}\n" for q, a, ss in fq["items"]))
    (OUT / "llms-full.txt").write_text("".join(full))
    print(f"Built {len(URLS)} pages ({len(states)} states, {len(guides)} guides) -> {OUT}")

if __name__ == "__main__": main()
