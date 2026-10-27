# Accuracy audit: 2026-10-26

Every factual claim on the 11 state pages, the 5 guides and the FAQ hub was re-checked against its cited official source, fetched fresh on 2026-10-26 (America/New_York).

**How the pages were fetched.** I used curl first. Where a site blocks bots, I fell back to headless Chrome (AZ, IL), WebFetch (NY), or a regular Chrome window on the box driven over DevTools (Ohio ×5, travel.state.gov, plus a recheck of AZ, IL and NY). By the end of the audit **every cited source had loaded.**

**Totals:** 194 claims checked. 187 matched. 7 differed or could not be confirmed (all 7 are fixed; see "Discrepancies and fixes").

## Cited URL status

| # | URL | Status | Redirect? |
|---|---|---|---|
| 1 | HCCH Apostille Handbook PDF | 200 | no |
| 2 | azsos.gov/business/authentication | 200 (browser; curl 403 bot block) | no |
| 3 | dos.fl.gov …/apostille-notarial-certification/ | 200 | no |
| 4 | dos.ny.gov/obtain-apostillecertificate-authentication | 200 (browser; curl 403) | **YES → dos.ny.gov/apostille-certificate-authentication** (same content) |
| 5 | sosnc.gov …/Obtaining_Auth_Certificate | 200 | no |
| 6 | travel.state.gov …/request-services.html | 200 (browser; curl/WebFetch blocked) | no |
| 7 | gsccca.org …/general-apostille-information | 200 | no |
| 8 | hcch.net status table cid=41 | 200 | no |
| 9 | ilsos.gov …/apostilles.html | 200 (browser) | no |
| 10 | nj.gov/treasury/revenue/apostilles.shtml | 200 | no |
| 11 | nj.gov/treasury/revenue/fees.shtml | 200 | no |
| 12 | ohiosos.gov Form 8003 PDF | 200 (browser) | no |
| 13 | ohiosos.gov/contact-our-office | 200 (browser) | no |
| 14 | ohiosos.gov/records/authentications-and-apostilles | 200 (browser) | no |
| 15 | ohiosos.gov …/frequently-asked-questions | 200 (browser) | no |
| 16 | ohiosos.gov/records/forms-fees | 200 (browser) | no |
| 17 | pa.gov …/get-document-certifications---apostilles | 200 | no |
| 18 | sos.ca.gov/notary/authentication | 200 | **YES → sos.ca.gov/notary/request-apostille** (same content) |
| 19–22 | sos.state.tx.us authfaqs, authinfo, Form 2102 PDF, request.shtml | 200 | no |
| 23 | sos.wa.gov apostille FAQ | 200 | no |
| 24 | sosnc.gov/fees/by_title/_authentications | 200 | no |

## Discrepancies and fixes

| Page | Claim on site | Official source now | Verdict | Fix |
|---|---|---|---|---|
| Texas | Fee must be paid 72 business hours before an appointment | That rule applies only to the Houston pop-up event (Aug 26, 2026). Regular Austin appointments pay at the office. | differs | Removed |
| Arizona | "Business Services operates by appointment only" from Nov 2, 2026 (unscoped) | The notice is titled "Phoenix Business Services – Appointment Only". In-person service will no longer be at 1700 W. Washington; the location is given when you book. | differs (scope) | Scoped to Phoenix |
| New Jersey | Mailing address "PO Box 628, Trenton 08625-0628" | The page says to mail or drop off at the "Customer Service Center". The PO Box appears only as the Division's general footer address. | not confirmable as the apostille mailing address | Reworded: no separate apostille mailing address is published; use the address on your online order confirmation. The footer address is labelled as general. |
| Florida | Accepted: "school documents" | "School Transcripts" | differs (wording) | "school transcripts" |
| Hague guide | "Most state offices issue both apostilles and authentication certificates" | Not confirmable nationally. Of the 11 offices covered, 10 issue for both kinds of destination country (GA is the exception). | not confirmable | "Most of the state offices this site covers…" |
| FAQ hub | Apostille vs authentication answer cites Texas Authentication FAQs | Texas issues a single "universal apostille", so it doesn't support the description. Ohio says authentication certificates may need further U.S. DoS verification. | source doesn't support claim | Reworded to mention possible U.S. DoS step; Texas source replaced with Ohio SOS |
| Federal guide | Payment: "Credit card only in person" | In person: credit or debit card, or contactless (Apple/Google/Samsung Pay); no cash, checks or money orders | imprecise | Reworded |

**Other changes (no wrong claim; a hedge replaced by what the source now publishes):**
- IL: payment no longer says "(confirm on the official page)".
- AZ: payment ("Checks and money orders payable to 'Arizona Secretary of State'; no cash by mail") and the toll-free number.
- GA: walk-in payment (cash, check, money order, credit card).
- TX: phone (512) 463-5705.
- CA and NY: cited URLs updated to their redirect targets.

**Noted, no site change:**
- Ohio's FAQ says FBI checks are "authenticated directly through the FBI". Ohio's own Form 8003 and the U.S. DoS say they go to the U.S. Department of State. The site's Ohio text only says Ohio can't apostille them, which is true either way.
- The NJ page shows "Last Updated 04/23/25".

## Per-page tables
Columns: claim | site says | official source now | verdict.

### California (source: sos.ca.gov/notary/request-apostille, redirected)
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Fee | $20 per apostille | $20 | matches |
| In-person handling fee | $6 per different official's signature | $6 special handling | matches |
| Mail address and payee | check or money order to Secretary of State | same | matches |
| Sacramento counter | 3rd floor; Visa/MC, check, MO, cash | same | matches |
| LA counter | Room 12513, temporarily 1st floor Suite 1215; no cash | same | matches |
| Same-day | Sacramento, LA, Pop-Up Shops | same | matches |
| Mail processing | processed in order received | same | matches |
| Items to mail | 4 items | same 4 | matches |
| Courier address | as listed | same | matches |
| Phone | (916) 653-6814 | same | matches |
| Pop-Up tip | Pop-Ups at county offices | same | matches |
| Deadline tip | office points to in-person | same | matches |

### New York (source: dos.ny.gov, redirected)
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Fee | $10 | $10 | matches |
| Walk-in same day | NYC, Albany, Binghamton, Buffalo, Utica | same | matches |
| Walk-in limit | 10 | 10 | matches |
| Drop-off | Albany/NYC, by receipt date | same | matches |
| Mail time | not published | not published | matches |
| Mail address | PO Box 22001, Albany 12201-2001 | same | matches |
| Albany office | 1 Commerce Plaza, 99 Washington Ave 6th Fl | same | matches |
| NYC office | 123 William St 2nd Fl, 10038-3804 | same | matches |
| Binghamton/Buffalo/Utica | 44 Hawley St Rm 1506; 295 Main St 8th Fl Ste 821; 207 Genesee St | same | matches |
| Phone | 518-474-4429 | same | matches |
| Payment | incl. CVV form | same | matches |
| County Clerk step | local records and notarized docs need County Clerk; NYS DOH exempt | same | matches |
| NYC Letter of Exemplification | yes | yes | matches |
| Return label | prepaid; no bill-sender or bill-card | same | matches |

### Texas (authinfo, request.shtml, Form 2102, authfaqs)
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Fee | $15 per document, not per page | same | matches |
| Adoption | $10, max $100 per child | "per adoption" / "each child" | matches |
| Mail time | up to two weeks | same | matches |
| Same-day max | 10 | 10 | matches |
| Walk-in days | Mon & Fri | same | matches |
| Appointments | Tue–Thu | same | matches |
| Appointment prepay 72 h | yes | Houston pop-up only | **differs → removed** |
| Drop box | >10 docs, about 72 h | same | matches |
| Mail payment | check/MO on U.S. bank, or SOS Client Account | same | matches |
| In-person payment | check, MO, card, exact cash | same | matches |
| Mail address | P.O. Box 13550, Austin 78711-3550 | same | matches |
| Office | 400 W 15th St, 8–5 Mon–Fri | same | matches |
| Form 2102; no bill-sender air bills | yes | same | matches |
| Certified records within 5 years | yes | same | matches |
| Country required; no U.S. use | yes | same | matches |
| Notario Publico rejected | yes | same | matches |
| RON | ledger + certificate; some countries reject | same | matches |
| Mailed requests not pulled for walk-in | yes | same | matches |
| Phone | (blank) | (512) 463-5705 | added |

### Florida
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Fee | $10, or $20 for county Clerk-certified | same | matches |
| Payment | check/MO to FL Dept of State, U.S. funds; no cash/credit | same | matches |
| Walk-in | not described; mail | same | matches |
| Processing time | not published | not published | matches |
| Office | 2415 N. Monroe St Ste 810, Tallahassee 32303 | same | matches |
| Return | SASE or air bill, requestor as sender and recipient | same | matches |
| Request form, originals | yes | yes | matches |
| Accepted types | "school documents" | "School Transcripts" | **differs (wording) → fixed** |
| Federal → U.S. DoS; other states → that state | yes | yes | matches |

### Illinois
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Fee | $2 each, each document needs its own | same | matches |
| Mail time | 7–14 business days | same | matches |
| Chicago | 160 N LaSalle Ste 100, 60601; 312-814-8218 | same | matches |
| Springfield | 2701 S Dirksen Pkwy 62723; 217-782-7017 | same | matches |
| DMV+ locations | Chicago Flagship, Aurora, Champaign, Lake Zurich, Melrose Park | same | matches |
| Docs | originals certified by an official or IL-notarized | same | matches |
| SASE | yes | yes | matches |
| Payment | check/MO to IL SOS ("confirm") | one check/MO to IL SOS for the total | matches (hedge removed) |
| FBI/federal not handled | yes | "No" | matches |
| In person processed while you wait | (added) | "in most cases" | added |

### Pennsylvania
All 11 claims match: $15/document; 5–7 business days; walk-in 8–4:30 Mon–Fri (arrive by 4, entrance closes 3 pm); payment terms; North Office Bldg, 401 North St Rm 201, Harrisburg 17120; 717-787-5280; ra-certifications@pa.gov; cover letter/form; UPS air bill only (no FedEx/DHL); no assistant/deputy clerk signatures; marriage via register of wills/orphans' court clerk; death certificates by state registrar.

### North Carolina
All 13 claims match: $10; duplicates; adoption duplicate $5 at the same time; refund exception; payee "North Carolina Secretary of State"; turnaround page and emergencies; in-person via "Getting Documents To and From Us"; address; 919-814-5400; cover letter, payment, originals, prepaid envelope or bar-coded label; diplomas/transcripts need an NC notary (school seal not accepted); agencies not needing notarization; certified since April 1, 2000; English translation required.

### Georgia (GSCCCA)
All 11 claims match: GSCCCA, not SOS; $3; mail 1–2 business days; walk-in typically <20 min, 9–4 Mon–Fri, no appointment; check/MO to GSCCCA or credit card pre-payment voucher; 1875 Century Blvd Ste 100, Atlanta 30345, Attn Notary Division; 404-327-6023 / 800-304-5175 / notary@gsccca.org; cover letter; prepaid envelope or computer-generated air bill; Great Seal Certification by SOS (404-656-2871) for non-Hague; pre-2000 documents → new copy. Added: walk-in payment = cash, check, MO, credit card.

### New Jersey
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Authority | Treasury DORES | same | matches |
| Fee | $25 per certificate | "All certificates (standings and Apostilles), each $25" | matches |
| Adoption | $5 | $5 per certificate | matches |
| Online service; card/e-check; convenience fee | yes | yes | matches |
| Processing time | shown inside online service | same | matches |
| Drop-off with confirmation page | yes | "mail (or drop-off)" | matches |
| Mail address | PO Box 628, Trenton 08625-0628 | only the Division footer address; the page says "Customer Service Center" | **not confirmable → reworded** |
| Inked signatures | notary + signer | same | matches |
| 1923 split DOH / Archives | yes | yes | matches |
| Translation → two apostilles, two fees; no other states' vital records | yes | yes | matches |

### Arizona
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Fee | $3/document | same | matches |
| Expedite | $25 in person, limit 6 | same | matches |
| PR/territories | $18 notarial capacity certificate | same | matches |
| Mail time | 10–20 business days | same | matches |
| Appointment only from Nov 2, 2026 | "Business Services" (unscoped) | Phoenix Business Services | **differs (scope) → fixed** |
| Mail address | 1700 W Washington Fl 7, 85007-2808, Attn Apostille Dept | same | matches |
| Tucson | 400 W Congress Ste 221, 85701 | same | matches |
| Phone | 602-542-6187 | same (+ 1-800-458-5842) | matches (toll-free added) |
| Originals only, form, $3, return postage | yes | yes | matches |
| No electronic apostilles | yes | yes | matches |
| Other states' docs → that state | yes | yes | matches |
| Payment | "see official page" | checks/MO to "Arizona Secretary of State"; no cash by mail | now stated |

### Ohio (5 sources, all loaded in a browser today)
All 14 claims match: Client Service Center, 180 Civic Center Dr., Columbus 43215-4138; $5/document, exact fee, no cash; 2–3 days of receipt; in person for faster service; office hours 8–5 Mon–Fri; check, MO or card, with Credit Card Authorization Form 100 for mail; no foreign checks/MO; phone 614-728-9200 (Apostilles & Authentications); Form 8003; accepted documents list; out-of-state/foreign notaries rejected; FBI, federal seal/court, citizenship (unless Ohio Clerk of Court) rejected; U.S. destination rejected; transcripts notarized first, translation then notarize; don't remove the certificate.

### Guide: U.S. Department of State (travel.state.gov, loaded in a browser, page "Last Updated: October 01, 2026")
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Fee | $20, non-refundable | same | matches |
| Form | DS-4194 | same | matches |
| Mail | within 5 weeks | same | matches |
| Drop-off | within 7 business days | same | matches |
| Drop-off hours/address | Mon–Thu 7:30–9:00, 600 19th St NW, DC 20006 | same | matches |
| Same-day | life-or-death family emergency, travel ≤2 weeks | same | matches |
| Mail address | 44132 Mercure Circle, PO Box 1206, Sterling VA 20166-1206 | same | matches |
| Mail payment | check or MO | same | matches |
| In-person payment | "credit card only" | credit/debit/contactless; no cash/check/MO | **imprecise → fixed** |

### Guide: FBI background check
All 7 claims match (federal document; IL and NY say states can't; DoS issues; DS-4194; $20; Sterling address and DC drop-off; 5 weeks / 7 business days / emergency same-day).

### Guide: Hague countries
| Claim | Site | Source | Verdict |
|---|---|---|---|
| Contracting parties | 130 as of June 30, 2026 | 130, last update 30-VI-2026 | matches |
| U.S. party since | Oct 15, 1981 | EIF 15-X-1981 | matches |
| China | Nov 7, 2023 | 7-XI-2023 | matches |
| Canada | Jan 11, 2024 | 11-I-2024 | matches |
| Algeria | Jul 9, 2026 | 9-VII-2026 | matches |
| Viet Nam | Sep 11, 2026 | 11-IX-2026 | matches |
| Thailand | Feb 28, 2027 | 28-II-2027 | matches |
| Non-Hague → authentication + legalization | yes | Ohio/NY/DoS | matches |
| "Most state offices issue both" | yes | not confirmable nationally | **reworded** |

### Guide: Birth certificate
All 7 claims match: state of issue (WA); certified copy needed (WA/AZ); NY County Clerk and NYC Letter of Exemplification; TX within 5 years; GA preferably since 2000; NJ 1923 split; PA state registrar for death certificates.

### Guide: State or federal
All 6 claims match: vital/court/notarized documents → issuing state; FBI and federal → DoS; IL says it can't do FBI/federal; FL says federal → DoS; GA GSCCCA; NJ DORES online step; NY County Clerk.

### FAQ hub (16 items, 22 claims)
21 match (HCCH origin-not-content; where to file; WA birth state; IL/NY/WA on FBI; DoS 5 weeks / 7 days / emergency; $2 IL to $25 NJ, DoS $20; TX 2 weeks, IL 7–14, PA 5–7; NY County Clerk; photocopy/WA true copy; WA transcripts, NC notary; 130 parties, China/Canada dates; no expiry per Handbook ¶28; TX/WA not for U.S. use; translator affidavit can be apostilled per Handbook ¶187; TX RON). 1 fixed: apostille vs authentication (source didn't support it; reworded and re-sourced).
