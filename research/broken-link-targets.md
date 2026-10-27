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

---

## 2026-10-27 batch (America/New_York): 20 broken-link pages + 4 resource-fit pages

Research only. **Nothing has been sent.** Every status below came from this box on 2026-10-27, using `curl -sSL` with a Chrome UA.
A broken link counts only if it gives a real 404 or redirects to a 404 page or a homepage. 403s, WAF pages and timeouts don't count.
Outbound port 80 is blocked from the box, so http:// links were tested on their https:// equivalent.
Maine replacement (https://www.maine.gov/sos/corporations-commissions/authentications-and-apostilles) returned 200 earlier today.
Later runs got 403 (rate limit), so re-check it before sending.
Ohio replacement (https://www.ohiosos.gov/records/authentications-and-apostilles/) is behind a bot check: **unverified, don't cite until checked in a browser**.

Risk/effort: **L** = one short email with a clear fix. **M** = a general inbox or a form, or a weaker fix. **H** = unlikely to get a reply, or the fix isn't a U.S. link.

### Broken-link pages

| # | Page | Broken link → status | Official replacement (200 today) | Contact | Risk/effort |
|---|---|---|---|---|---|
| 1 | germany.info Maine page https://www.germany.info/us-en/service/08-documents-certificationsandapostille/apostille-authorities-us-902204/2564804-2564804 | http://www.maine.gov/sos/cec/apostilles/ → 404 | https://www.maine.gov/sos/corporations-commissions/authentications-and-apostilles | Contact form https://www.germany.info/us-en/2510824-2510824 (page 200) | L-M (one form covers #1-5) |
| 2 | germany.info South Dakota …/2564896-2564896 | https://sdsos.gov/generalservices/apostilles → 404 | https://sdsos.gov/general-services/apostilles-authentications.aspx | same form | L-M |
| 3 | germany.info Puerto Rico …/2564878-2564878 | estado.pr.gov/en/certification-of-documents-and-filing-regulations/ → 404 | https://estado.pr.gov/apostillas | same form | L-M |
| 4 | germany.info Pennsylvania …/2564874-2564874 | dos.pa.gov/OtherServices/Certifications_Apostilles/ → redirects to the agency homepage | https://www.pa.gov/agencies/dos/programs/document-certification | same form | L-M (PA is in our data) |
| 5 | germany.info Missouri …/2564820-2564820 | typo "https://www.sos.mo/gov/" (malformed) | https://www.sos.mo.gov/authentication | same form | L-M |
| 6 | Brazil CG Houston https://www.gov.br/mre/pt-br/consulado-houston/informacoes-uteis/apostilamento/apostilamento | AR sos.arkansas.gov/BCS/Pages/apostilleCertification.aspx 404; CO sos.state.co.us/pubs/notary/apostilleHelp.html 404; LA …/AuthenticateSignaturesOfLouisianaOfficials/Pages/default.aspx 404; NM sos.state.nm.us/…/Apostille_Information_Overview.aspx → redirect → 404 | AR https://www.sos.arkansas.gov/business-commercial-services-bcs/for-apostille-certification/ ; CO https://www.coloradosos.gov/pubs/apostilles/home.html ; LA https://www.sos.la.gov/certifications/apostilles-authentications ; NM https://www.sos.nm.gov/notary-and-apostille/apostille-authentications/ | consular.houston@itamaraty.gov.br (on gov.br list) | L (4 fixes, one email) |
| 7 | Brazil CG Washington https://www.gov.br/mre/pt-br/consulado-washington/apostila-da-haia | OH ohio.gov/wps/portal/…/document-authentication-and-certification 404; WV sos.wv.gov/business/Pages/AuthDocs.aspx 404 | WV https://sos.wv.gov/business/apostilles-and-authentications/authentication-documents-international-use ; OH unverified (see note) | atos.cgwashington@itamaraty.gov.br (notarial acts) or cons.cgwashington@itamaraty.gov.br | L |
| 8 | Brazil CG Los Angeles …/consulado-los-angeles/servicos-consulares/servicos-notariais/legalizacao-de-documentos-apostila/legalizacao-de-documentos-estrangeiros-apostila | ID sos.idaho.gov/NOTARY/apostille/index.html 404; CNJ cartorios-autorizados 404 | ID https://sos.idaho.gov/apostille/ | notarial.la@itamaraty.gov.br | L |
| 9 | Brazil CG Chicago https://www.gov.br/mre/pt-br/consulado-chicago/servicos-consulares/legalizacao-de-documentos-apostilamento | MI michigan.gov/sos/0,4670,7-127-1633_95527_95530---,00.html → redirect → michigan.gov/som/404; CNJ FAQ 404 | MI https://www.michigan.gov/sos/all-services/document-authentication-and-apostille | notarial.chicago@itamaraty.gov.br | L |
| 10 | Brazil CG Miami https://www.gov.br/mre/pt-br/consulado-miami/servicos-consulares-e-informacoes-uties/apostilamento | PR estado.pr.gov/es/certificacion-documentos-y-radicacion-de-reglamentos/ → 404 | https://estado.pr.gov/apostillas | consular.miami@itamaraty.gov.br | L |
| 11 | Brazil CG Boston https://www.gov.br/mre/pt-br/consulado-boston/servicos/copy_of_apostila-antiga-legalizacao | ME /sos/cec/apostilles/ 404 | Maine URL above | contato.boston@itamaraty.gov.br | L-M |
| 12 | Argentina CG Chicago https://cchic.cancilleria.gob.ar/en/node/25311 | IN www.in.gov/sos/notary/seal.html 404; SD www.state.sd.us/sos/Notaries/apostilles_and_authentications.htm 404 (also dead legacy domains for OH and WI) | IN https://www.in.gov/sos/business/apostilleauthentication/ ; SD https://sdsos.gov/general-services/apostilles-authentications.aspx | cchic@mrecic.gov.ar (on page) | L |
| 13 | Argentina CG New York https://cnyor.cancilleria.gob.ar/en/hague-apostille-united-states-public-documents (+ ES twin …/es/2-apostilla-en-documentos-emitidos-en-estados-unidos) | ME /sos/cec/apostilles/ 404 | Maine URL above | cnyor@mrecic.gov.ar (on page) | L |
| 14 | Argentina Embassy DC https://eeeuu.cancilleria.gob.ar/es/requisitos-modalidad-y-costos-de-tramitaci%C3%B3n-apostilla | WV form sos.wv.gov/FormSearch/Business/Apostilles/AC-1.pdf 404 | https://sos.wv.gov/media/225/ac-1pdf | consular@embassyofargentina.us (on contacto-sede page) | M |
| 15 | Philippine CG Houston https://pcghouston.org/notarial-services/ | LA sos.la.gov/NotaryAndCertifications/Certifications/Pages/default.aspx 404 | https://www.sos.la.gov/certifications/apostilles-authentications | houstonpcg.legal@dfa.gov.ph (on page) | L |
| 16 | Philippine CG New York https://newyorkpcg.org/pcgny/consular-services/legalization-notarization/authentication-of-a-public-document-through-apostille/ | ME /sos/cec/apostilles/ 404 | Maine URL above | newyorkpcg.notarials@dfa.gov.ph (on page) | L |
| 17 | Czech CG New York https://mzv.gov.cz/consulate.newyork/en/visa_and_consular_information/consular_information/legalization_of_documents/index_1.html | http://hcch.e-vision.nl/…aid=353 → hcch.net 404 (rest of the state table is also badly outdated) | https://www.hcch.net/en/states/authorities/details3/?aid=353 | wwwadmin@mzv.cz (webmaster, on page) | L-M |
| 18 | Brazil CG San Francisco …/consulado-sao-francisco/servicos-consulares-e-informacoes-uteis/apostilamento/informacoes-gerais | CNJ links 404 (+ malformed "http://https://…") | not a U.S. link: no replacement verified | civil.sf@itamaraty.gov.br | H |
| 19 | Brazil CG New York …/consulado-nova-york/servicos-consulares/apostilamento-de-documentos-estrangeiros | Bermuda elections.gov.bm/…/apostille-information.html 404 | not a U.S. state: none verified | legalizacao.novayork@itamaraty.gov.br | H |
| 20 | Italy CG New York https://consnewyork.esteri.it/en/servizi-consolari-e-visti/servizi-per-il-cittadino-italiano/servizi-notarili/apostille/ | Bermuda link 404 (same as above) | none verified | only semplificazione@esteri.it on page (generic) | H |

### Resource-fit pages (no broken links found; a fees page fits their resource list)

| # | Page | Fit | Contact | Risk/effort |
|---|---|---|---|---|
| 21 | UW-Madison Study Abroad, Teaching English Abroad Resources https://studyabroad.wisc.edu/returned-student-resources/teaching-english-abroad-resources/ | Resource list for TEFL grads, who need apostilled degrees | iapweb@studyabroad.wisc.edu (on page) | M |
| 22 | UW-Madison International Internships, Teaching English Abroad Resources https://internships.international.wisc.edu/teaching-english-abroad-resources/ | same | internships@international.wisc.edu (on page) | M |
| 23 | UVA Career Center, Resources for Teaching Abroad https://career.virginia.edu/resources/resources-for-teaching-abroad/ | same | careercenter@virginia.edu (from search, not on page: verify) | M-H |
| 24 | UMass Amherst Registrar, Notarized Documents and Apostille Information https://www.umass.edu/registrar/notarized-documents-and-apostille-information | Sends students to the state apostille office; MA isn't in our data, so it's weak | no email on page (find the registrar contact) | H |

### Top 8 by likelihood of a positive reply

1. **Brazil CG Houston (#6)**: 4 dead state links fixed with one email to a named consular inbox.
2. **German Missions / germany.info (#1-5)**: 5 state pages, one form, and a meticulous webmaster culture. PA is in our data.
3. **Argentina CG Chicago (#12)**: the page publishes its own email, and there are 2 clean fixes (IN, SD).
4. **Brazil CG Washington (#7)**: WV fix verified. OH is in our data, but get the OH URL in a browser first.
5. **Philippine CG Houston (#15)**: a dedicated legal inbox and one clear LA fix.
6. **Brazil CG Chicago (#9)**: Michigan redirects to a 404, with a notarial inbox.
7. **Brazil CG Los Angeles (#8)**: Idaho fix and a notarial inbox.
8. **Czech CG New York (#17)**: a webmaster email, and the HCCH fix is the single most useful link they could have.

The Maine-only pages (#11, #13, #16) are next. Batch them after the Maine URL re-checks as 200.

### Draft (template; not sent; parent must route via DraftExternalMessage after approval)

Subject: Broken state apostille links on your apostille page

Hello,

Your page [PAGE URL] lists the U.S. state apostille offices. A few of those links no longer work, which we checked on 27 October 2026:

- [State]: [old URL] now returns "page not found". The current official page is [replacement URL].

We hope this saves your readers a dead end. If it helps, we also keep a free page listing each state's apostille fee and processing time, with every figure linked to the state's own website: https://apostille-atlas.github.io/apostille-fees-by-state/ . Please keep the official links either way.

Kind regards,
Apostille Atlas

### Five more free awareness ideas (playbook-consistent)

1. **Dataset JSON-LD on the fees page + CSV**, so it qualifies for Google Dataset Search. **Alone** (site change; no outside contact).
2. **Corrections report to the issuing states**: tell state SOS webmasters (e.g. WV, ME, PA) that their old URLs have no redirects. This is goodwill, not a link ask. **Needs approval** (external email).
3. **Offer the CSV to law-library LibGuides / reference librarians** as a citable open dataset (CC-BY attribution, no link swap). **Needs approval**.
4. **Bing Webmaster Tools (import from GSC) + IndexNow ping** after each data update. **Needs account**.
5. **Journalist source platforms (Source of Sources / Qwoted / Featured)**, answering apostille-cost queries as a real, named person and citing the data. **Needs account** (and must be the real user, no personas).
