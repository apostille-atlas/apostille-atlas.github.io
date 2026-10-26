# Apostille Atlas: boring-niche directory site

A static directory of U.S. apostille offices (state + federal) with fees, addresses, timing and requirements, each fact cited to an official government page. No framework or dependencies; you only need Python 3.

## Layout
- `data/states.json`: one record per state (facts + `sources`)
- `content/guides/*.html`: guide pages (JSON front matter in the first `<!-- -->` comment)
- `build.py`: generates `dist/` (HTML, `sitemap.xml`, `robots.txt`, `404.html`)
- `config.json`: site name, **site_url** (set this to the real domain before deploying), last-verified date
- `scripts/new_page.py`: scaffolds the next backlog item as a draft
- `backlog.md`: page ideas, in order
- `research/`: niche rationale and affiliate program list
- `outreach/`: draft partner emails (NOT sent)

## Build & preview
    python3 build.py
    cd dist && python3 -m http.server 8000   # open http://localhost:8000

## Nightly page checklist (~30–45 min)
1. `python3 scripts/new_page.py`: creates a draft for the next backlog item.
2. Open the **official** source (state SOS or equivalent, travel.state.gov, hcch.net). Do not copy facts from competitor sites.
3. Fill in every `TODO`: fee, mail/in-person options, address, payment, what to send, and pitfalls. If the office doesn't publish a processing time, say so instead of guessing.
4. Add each official URL to `sources`. Delete `"draft": true`. (The build skips drafts and pages with no sources.)
5. Add 2–3 internal links (state ⇄ guide ⇄ directory).
6. Use the `title` pattern "<State> Apostille: Office, $<fee> Fee, Processing Time & Steps"; the description should be at most 155 characters.
7. `python3 build.py` and preview locally.
8. `python3 scripts/new_page.py --done`, then commit and deploy.
9. Monthly: re-check fees and addresses on existing pages, and update `last_verified` in `config.json`.

## Affiliate links
Placeholders are `href="#affiliate-placeholder"` with `data-affiliate="..."` and `rel="sponsored nofollow"`. Once a program approves you, replace them with your tracking link (search for `affiliate-placeholder`) and update `/disclosure/` ("Current status").

## Deploy (needs one free account, chosen by the owner)
- **Cloudflare Pages / Netlify / Vercel**: drag and drop or connect the repo; output folder `dist`, build command `python3 build.py`. `netlify.toml` is included.
- **GitHub Pages**: push to a repo; `.github/workflows/pages.yml` builds and publishes `dist/`.
