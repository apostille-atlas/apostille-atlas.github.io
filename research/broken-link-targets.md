# Broken-link replacement targets (research only — nothing sent)

Checked 2026-10-27 (America/New_York) with curl from our build box, across 27 candidate resource pages
(consulate guides, law-library LibGuides, university registrar / study-abroad pages, county clerks).

**Nothing has been emailed.** Any note to these contacts needs Schneur's approval first; drafts go to the parent agent.

## How a link was counted as broken

- Counted: a real **HTTP 404**, or an old URL that now **redirects to a 404 page or to the site's homepage**.
- Not counted: **403 / "Just a moment…" / perfdrive pages** (bot protection — travel.state.gov, ohiosos.gov, sos.mn.gov,
  sos.nh.gov, azsos.gov, dos.ny.gov, sosmt.gov, sos.iowa.gov), and **timeouts / TLS errors** on legacy domains
  (cyberdriveillinois.com, ilsos.gov, sos.state.oh.us, sos.state.wi.us, sec.state.vt.us, sos.ne.gov). Our box can't reach
  those reliably, so they are "unverified", not broken.
- Old URLs that still redirect to the right page (sos.ca.gov/notary/authentication → /notary/request-apostille,
  dos.myflorida.com → dos.fl.gov, soswy.state.wy.us → sos.wyo.gov, ltgov.hawaii.gov, sos.tn.gov) are **not** broken.
- Every replacement link below was fetched on 2026-10-27, returned 200, and is the state office's own apostille page.

## Target 1 — Consulate General of Italy in San Francisco (best target)

- Page: https://conssanfrancisco.esteri.it/wp-content/uploads/2024/01/APOSTILLE-Info-and-State-Websites.pdf
- Contact: **statocivile.sanfrancisco@esteri.it**. The PDF itself says: "If you notice any discrepancies or errors with
  the links, please notify us by sending an email to statocivile.sanfrancisco@esteri.it."

| State | Broken link in the PDF | Result | Official replacement (verified 200) |
|---|---|---|---|
| West Virginia | https://sos.wv.gov/business-licensing/apostilles-authentications/Pages/default.aspx | 404 | https://sos.wv.gov/business/apostilles-and-authentications/authentication-documents-international-use |
| Maine | https://www.maine.gov/sos/cec/apostilles/ | 404 | https://www.maine.gov/sos/corporations-commissions/authentications-and-apostilles |
| South Carolina | https://www.scsos.com/Apostilles | 404 | https://sos.sc.gov/services-and-filings/apostilles |
| Arkansas | https://www.sos.arkansas.gov/business-commercial-services-bcs/apostille-certification | 404 | https://www.sos.arkansas.gov/business-commercial-services-bcs/for-apostille-certification |
| Kentucky | https://www.sos.ky.gov/bus/businessrecords/Pages/Apostilles-and-Authentications.aspx | 404 | https://www.sos.ky.gov/bus/apostilles/Pages/default.aspx |
| Kansas | http://www.kssos.org/business/notary_public/certifications.html | redirects to sos.ks.gov 404 page | https://sos.ks.gov/general-services/apostilles-authentications.html |
| Mississippi | http://www.sos.ms.gov/BusinessServices/Pages/Apostilles-Authentications.aspx | redirects to homepage | https://www.sos.ms.gov/regulation-enforcement/notaries-apostilles/apostilles-authentications |
| Colorado | http://www.sos.state.co.us/pubs/notary/apostilleHelp.html | 404 | https://www.sos.state.co.us/pubs/apostilles/home.html |
| New Mexico | http://www.sos.state.nm.us/Business_Services/Apostille_Information_Overview.aspx | redirects to sos.nm.gov, 404 | https://www.sos.nm.gov/notary-and-apostille/apostille-authentications/ |
| Rhode Island (soft) | http://sos.ri.gov/divisions/Business-Portal/Certifications-Apostille-Goodstanding | redirects to general Business Services page | replacement not yet verified (no dedicated apostille page confirmed) |

Also probably outdated but **unverified** (legacy domains our box can't reach): cyberdriveillinois.com, sos.state.wi.us,
sec.state.vt.us, sos.state.oh.us, sos.ne.gov, sos.nh.gov/certs.aspx (503). The Louisiana link is cut off in the PDF text,
so it isn't counted.

## Target 2 — Consulate General of Italy in Los Angeles

- Page: https://conslosangeles.esteri.it/wp-content/uploads/2024/12/APOSTILLE-INFORMATION-What-is-an-Apostille-v.11.12.2024.pdf (v. 11.12.2024)
- Contact: **losangeles.cittadinanza@esteri.it**. The PDF asks readers to report link errors to this address.

| State | Broken link | Result | Official replacement (verified 200) |
|---|---|---|---|
| West Virginia | https://sos.wv.gov/business/Pages/AuthDocs.aspx | 404 | https://sos.wv.gov/business/apostilles-and-authentications/authentication-documents-international-use |
| Maine | https://www.maine.gov/sos/cec/apostilles/ | 404 | https://www.maine.gov/sos/corporations-commissions/authentications-and-apostilles |

Unverified legacy domains: cyberdriveillinois.com, sos.state.oh.us, sos.ne.gov (see note above).

## Target 3 — Consulate General of Brazil in Atlanta (weaker)

- Page: https://www.gov.br/mre/pt-br/consulado-atlanta/english/consular-services/other-Information/apostille-certified-translation/hague-apostille
- Contact: **legalizacao.atlanta@itamaraty.gov.br** (the legalization address published on the consulate's page). There is no "report broken links" invitation.

| State | Broken link | Result | Official replacement (verified 200) |
|---|---|---|---|
| Mississippi | http://www.sos.ms.gov/BusinessServices/Pages/Notaries-Apostilles.aspx | redirects to homepage | https://www.sos.ms.gov/regulation-enforcement/notaries-apostilles/apostilles-authentications |

Possibly outdated (unverified, 403): https://travel.state.gov/content/travel/en/legal-considerations/judicial/authentication-of-documents/apostille-requirements.html.
The current State Dept path, as linked from NASS, is
https://travel.state.gov/content/travel/en/legal/travel-legal-considerations/internl-judicial-asst/authentications-and-apostilles/apostille-requirements.html.

## Pages checked with no confirmed broken links

fclawlib.libguides.com (apostilles, Introduction), mncourts.libguides.com, courts-state-nh-us.libguides.com,
registrar.uchicago.edu (Illinois links unverifiable from our box), registrar.illinois.edu, registrar.mit.edu, case.edu
(its Ohio link carries a stale Cloudflare `__cf_chl_jschl_tk__` token, cosmetic only), onestop.umn.edu, sf.gov, smcacre.gov,
Ventura and Santa Clara county clerks, sc.edu, unm.edu, gvsu.edu, slu.edu, nyu.edu, the Portugal SF consulate (403), and the
Spanish Ministry visa PDF. Berklee, Loyola and Chapman are **already-contacted outreach targets: don't chase**.

## How to pitch (when approved)

The ask: "here are the fixed official links", with our page offered as an optional extra:
https://apostille-atlas.github.io/apostille-fees-by-state/ (fees and processing times, each value linked to the state
source) or the directory. Don't ask for our link in place of the official one. Consulates should keep official
.gov links, and we only cover 11 states so far.
