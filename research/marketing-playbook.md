# Apostille Atlas marketing playbook (SEO, GEO, links, conversion)

Written 2026-10-27. Budget: $0. This is an internal working document. It is not linked from the site and contains no credentials.

Ground rules apply to every tactic below. We disclose affiliate links clearly. We never buy links, swap links, spam, post fake reviews, astroturf, or invent an author or expert. We never invent a fee, a processing time, or a statistic. Nothing in this file has been sent or posted. Anything outbound needs the user's approval first.

Ownership tags used in section 6:
- **[ME]**: I can do it alone (code, content or research in this repo).
- **[APPROVAL]**: I can draft it, but it goes out only after the user approves (emails, submissions).
- **[ACCOUNT]**: needs the user's own account or sign-in (Search Console, Bing, Reddit, Stack Exchange and so on).

---

## 1. How a tiny new site gets indexed and ranks for long-tail queries

### 1.1 What Google actually says
- **Discovery.** Google finds pages through links and sitemaps. The SEO Starter Guide recommends a sitemap and says promotion through "social media, community engagement… word of mouth" helps people discover a site, but don't overdo it: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- **Timing.** "Some changes might take effect in a few hours, others could take several months… wait a few weeks to assess" (same page). Recrawling for AI features can take "several days to several months": https://developers.google.com/search/docs/appearance/ai-features
- **Helpful content.** Google's self-assessment asks whether content gives "original information, reporting, research, or analysis" and "substantial value when compared to other pages in search results": https://developers.google.com/search/docs/fundamentals/creating-helpful-content. Warning signs on the same page apply directly to us:
  - "Are you using extensive automation to produce content on many topics?"
  - "mainly summarizing what others have to say without adding much value?"
  - "Did you decide to enter some niche topic area without any real expertise… mainly because you thought you'd get search traffic?"
  - "Are you changing the date of pages to make them seem fresh when the content has not substantially changed?"
- **Who / How / Why.** Google asks who made the content, how it was made, and why. It expects disclosure of automation or AI use "when it would be reasonably expected" (same page). Trust is the most important part of E-E-A-T, and YMYL topics get more weight. Apostilles touch legal documents, immigration and money, so treat them as YMYL-adjacent.
- **Originality.** Attribution "doesn't replace the need for original effort" (same page). Citing the Secretary of State is necessary, but it is not enough by itself.

### 1.2 Affiliate rules and what thin-affiliate penalties look like
Source: Google spam policies, https://developers.google.com/search/docs/essentials/spam-policies
- **Thin affiliation** means pages that copy merchant descriptions without adding value. Google names what good affiliate pages add: "additional information about price, original product reviews, rigorous testing and ratings, navigation of products or categories, and product comparisons."
- **Scaled content abuse** includes using generative AI to produce many pages without value, and "stitching or combining content from different web pages without adding value."
- **Doorway abuse** includes "substantially similar pages" and "pages targeted at specific regions or cities that funnel users to one page." This is the biggest risk for a site built of 50 state pages.
- **Keyword stuffing** includes "blocks of text that list cities and regions."
- **Link spam** includes buying links, "excessive link exchanges", and "low-quality directory or bookmark site links." Affiliate links marked `rel="sponsored"` or `rel="nofollow"` are fine.
- **Site reputation abuse.** The policy says "using affiliate links throughout a page, with links treated appropriately" is not a violation.
- These spam policies now also apply to Google's generative AI answers (same page).
- **What a penalty looks like.** You either get a manual action in Search Console (for example "Thin content with little or no added value", https://support.google.com/webmasters/answer/9044175) or, more often, an algorithmic drop with no notice. Impressions fall across the site, not on a single page.

### 1.3 How we avoid it (site-specific)
1. **Every state page must carry facts that differ by state.** That means the office name, the fee and its exceptions, mail and walk-in times, payment, addresses, quirks (for example Texas walk-ins are Monday and Friday only), and the official sources. Do not publish a state until it has at least the fee, office, method, time and a source. Never pad pages with template text.
2. **The paid-service box stays secondary and honest.** It already says DIY is cheaper, shows the official fee with its source, and lists partner prices exactly as the partner publishes them. That is the "additional information about price" and "comparison" Google asks for.
3. **Original value only we have:** a cross-state dataset of fees, times and walk-in rules (section 3) and decision helpers (section 4). Each is non-commodity, in the sense of Google's 2026 AI guide: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
4. **Honest dates.** Only bump `last_reviewed` when a page has actually been re-checked against the official source. The old line in traffic-plan.md ("keep every page's last reviewed date current") should be read as "re-check, then update." Never just change the date.
5. **Honest authorship.** The About page should explain how pages are made: AI-assisted drafting, every fact checked against the official page linked on that page, plus a corrections email. No invented human author or credentials. Google says not to fabricate author profiles (creating-helpful-content page).
6. **Pace.** One carefully sourced page a night is fine. Bulk-generating hundreds of variants (state × document × country) is exactly what the scaled-content policy describes. Google's 2026 AI guide also warns against creating "separate content for every possible variation" or fan-out query.

### 1.4 Long-tail reality from data
- Ahrefs (2025) found only **1.74%** of newly published pages reached the top 10 within a year (**6.11%** for non-empty English content). Of the pages that did rank, **40.82%** did so within about a month. Low-volume keywords rank faster, and **72.9%** of top-10 pages are more than 3 years old. Their advice is that if a page isn't ranking after about 6 months, update it. https://ahrefs.com/blog/how-long-does-it-take-to-rank-in-google-and-how-old-are-top-ranking-pages/
- Implication: target the precise questions people ask ("Texas apostille walk-in days", "FBI background check apostille for Korea") rather than "apostille". Expect most pages to need months.

---

## 2. GEO: getting cited by ChatGPT, Gemini / AI Overviews, Perplexity and Claude

### 2.1 Google AI Overviews and AI Mode
- **No special work required.** "You don't need to create new machine readable files, AI text files, or markup". A page must simply be indexed and eligible for a snippet: https://developers.google.com/search/docs/appearance/ai-features
- **Google's GEO guide (May 2026)** says GEO and AEO "is still SEO". It lists "valuable, non-commodity content" as the biggest factor and describes query fan-out. Its mythbusting section says llms.txt is not used by Google Search, chunking or AI rewrites aren't needed, and inauthentic mentions don't help. Structured data isn't required for AI features, but it still powers rich results. https://developers.google.com/search/docs/fundamentals/ai-optimization-guide and https://developers.google.cn/search/blog/2026/05/a-new-resource-for-optimizing
- **Structured data must match visible text** (ai-features page). Google deprecated the **FAQ rich result** on 2026-05-07 (https://developers.google.cn/search/updates), and HowTo rich results were retired earlier. Our FAQPage and HowTo JSON-LD is harmless and may still help machines parse the page. Don't expect rich results from it.
- **Measurement.** Search Console now has a generative AI performance report (ai-optimization-guide).

### 2.2 ChatGPT, Perplexity and Claude: let their search bots in
| Engine | Bot that powers citations/search | Training bot | User-triggered fetcher | Source |
|---|---|---|---|---|
| ChatGPT | OAI-SearchBot (needed to appear in ChatGPT search) | GPTBot | ChatGPT-User | https://developers.openai.com/api/docs/bots |
| Perplexity | PerplexityBot (search surfacing, not training) | n/a | Perplexity-User (generally ignores robots.txt) | https://docs.perplexity.ai/guides/bots |
| Claude | Claude-SearchBot | ClaudeBot | Claude-User | https://support.claude.com/en/articles/8896518 |
| Copilot / Bing | Bingbot | n/a | n/a | https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/ |

Our robots.txt already allows all of these (Claude-User falls under `User-agent: *`). OpenAI says robots.txt changes take about 24 hours to take effect. **Bing Webmaster Tools** has an "AI Performance" report (public preview, 2026) that shows citations in Copilot and Bing AI answers. That is a second free reason to set up Bing.

### 2.3 Which content formats get cited
- **Princeton GEO paper (KDD 2024)**, https://arxiv.org/abs/2311.09735. Adding **cited sources, quotations and statistics** improved visibility in generative answers by about **30–40%** (relative, position-adjusted word count). Fluency and easy-to-understand rewrites gained about **15–30%**. **Keyword stuffing did not help** and did worse on Perplexity. Lower-ranked sources gained most: "Cite Sources" gave **+115%** for a rank-5 source. Statistics helped most for **Law & Government** queries, which is our category.
  - Caveats: the tests used a GPT-3.5-based engine over the top 5 Google results, with only a small Perplexity check. Treat this as direction, not a guarantee.
- **What that means for us.** Open each page with a one-sentence direct answer that contains the number and names the office ("Texas charges $15 per document; send Form 2102 to the Secretary of State's Authentications Unit"). Keep the fee and time table near the top, and link the official source next to each fact. We already do most of this.
- **Freshness.** Ahrefs analysed about 17M citations. AI-cited URLs were on average **25.7% fresher** than organic results. ChatGPT leaned newest, and Google AI Overviews leaned older. https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/
  - Takeaway: re-check pages for real and show the true review date. Don't fake it (see 1.3.4).
- **Third-party mentions.** Ahrefs' 75K-brand study found that branded web mentions correlated with AI Overview visibility at **0.664**, against **0.218** for backlinks. That is correlation, not causation. https://ahrefs.com/blog/ai-overview-brand-correlation/
  - Google says inauthentic mentions don't help (ai-optimization-guide). So earn real mentions: libraries, universities, forums where we actually answered the question.

### 2.4 llms.txt: honest evidence
- **Ahrefs, 137K sites (May 2026).** 97% of llms.txt files got zero requests. Of the few requests, about 19.5% came from named AI bots (mostly GPTBot, then Claude-Code). https://ahrefs.com/blog/llmstxt-study/
- **Google.** Mueller compared it to the keywords meta tag (https://www.searchenginejournal.com/google-says-llms-txt-comparable-to-keywords-meta-tag/544804/). Illyes said Google won't use it (https://searchengineland.com/google-says-normal-seo-works-for-ranking-in-ai-overviews-and-llms-txt-wont-be-used-459422).
- There is one anecdote of OpenAI fetching it: https://www.seroundtable.com/openai-crawling-llms-txt-files-39811.html
- **Verdict:** keep our llms.txt and llms-full.txt, since they're free and already built. Expect no measurable effect, and spend no more time on them.

---

## 3. Legitimate free backlinks and mentions

Ratings: effort = our time. Likelihood = the chance of at least one real link or mention in 90 days. Risk = policy or reputation risk if done properly.

| Tactic | How (honestly) | Effort | Likelihood | Risk | Owner |
|---|---|---|---|---|---|
| **Original data page**: "US state apostille fees, processing times and walk-in rules" with a CSV download | Build it from data/states.json. Every cell links its official source, with a methodology note and a true review date. Add Dataset JSON-LD (https://developers.google.com/search/docs/appearance/structured-data/dataset). It is the kind of page journalists, libraries and AI answers cite (Princeton: statistics plus sources). | Medium | Medium (grows with state coverage) | Low | [ME] |
| **Resource-page outreach**: university study-abroad and international offices, TEFL/Fulbright pages, library LibGuides that already list apostille links | Find existing "apostille resources" pages. Send one short personal email explaining what the page offers (free, cites official sources). No follow-up spam. Backlinko's method: https://backlinko.com/hub/seo/resource-pages. Search Engine Land guide: https://searchengineland.com/guide/resource-pages-for-link-building | Medium | Medium (10 of 15 university emails already sent; watch replies) | Low | [APPROVAL] |
| **Broken-link replacement** on .gov, .edu and library pages | Use a link checker on resource pages. If an apostille link is dead (Secretary of State URLs change often), tell the owner and offer the **official** replacement URL first, and our page second. Backlinko: https://backlinko.com/hub/seo/broken-link-building. Leading with the official fix keeps it genuinely helpful. | Medium | Low–medium | Low | [ME] to research, [APPROVAL] to email |
| **Journalist requests**: HARO (relaunched under Featured), Source of Sources (free), Qwoted (free tier, 2 pitches a month), Featured (free tier) | Answer only queries about apostilles, documents for moving abroad, or teaching abroad. Status and pricing (2026): https://offpageatlas.com/tactics/journalist-requests/ and https://subscribepr.com/blog/best-haro-alternatives-2026/. **Ethics: pitches must come from a real, named person (the user) with real experience.** We must not invent an expert persona. Few requests offer a followed link (BuzzStream figure cited by https://outreachdesk.com/haro-alternatives/). | Medium (daily monitoring) | Low | Medium if done dishonestly, low if honest | [ACCOUNT] |
| **Curlie** (editor-reviewed directory) | One submission in the single best category: https://www.curlie.org/docs/en/add.html | Low | Low (slow editors) | Low | [APPROVAL] |
| **Bulk or paid directories, link exchanges, guest-post farms, PBNs** | **Don't.** Named as link spam in Google's spam policies. | n/a | n/a | High | Never |
| **Helpful community answers** (Stack Exchange, Reddit, Quora, expat forums) | Answer fully in the post and link only when our table adds something. Disclose that it's our site. Never post affiliate links there. Follow each community's rules (see traffic-plan.md section 3). These create the real third-party mentions the AI studies correlate with. | Medium, ongoing | Medium | Medium if spammy, low if genuine | [ACCOUNT] |
| **Corrections to official sources** | When we find an error or broken link on an official page during research, report it to the office. This is a goodwill action, not a link request. | Low | Low | None | [APPROVAL] |

---

## 4. Conversion: honest CTAs, comparisons and decision helpers

### 4.1 Disclosure (legal floor)
- **FTC guidance** (https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking):
  - Disclose "clearly and conspicuously", and "the closer the disclosure is to your recommendation, the better." Suggested wording: "I get commissions for purchases made through links in this post."
  - **"Affiliate link" by itself may not be adequate.** "Consumers might not understand that 'affiliate link' means that the person placing the link is getting paid." A "Buy now" button alone is not adequate, and "commissionable link" is "probably not a clear disclosure".
  - **"Paid link" right next to the link "should be an adequate disclosure."**
- **Our status.** Each box shows "(affiliate link)" next to the link plus an adjacent sentence ("we may earn a commission at no extra cost to you"), so we are likely compliant.
  - Cheap upgrade [ME]: change the inline label to "(paid link)", which is the FTC's own example. Keep the sentence in the same box, and keep it visible on mobile.

### 4.2 Placement and banner blindness
- NN/g: users ignore content that "resembles ads, is close to ads, or appears in locations traditionally dedicated to ads" (top banner, right rail, animation). https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/
  - For us, the paid-service box should look like page content: plain text, a short "when it's worth paying" list, no flashing or banner styling.
  - Put the **answer first**, then the box. We already lead with the official facts.
- **Honest CTA copy** names the trade-off: "Doing it yourself costs $15 at the Secretary of State. A service may make sense if you're abroad, on a deadline, or also need translation." Never say "required", "official" or "fastest" unless the source says so.

### 4.3 Comparison tables and decision helpers
- NN/g: comparison tables suit compensatory decisions among about 5–7 options or fewer. Use columns for options and rows for attributes, with consistent, short values. https://www.nngroup.com/articles/comparison-tables/. State differences explicitly, or users assume options are the same: https://www.nngroup.com/articles/explicit-differences/
- A page-level table that fits us has three columns: **DIY by mail**, **DIY in person**, and **Paid service**. Rows: cost (official fee vs the partner's published price), published time, what you do yourself, and when it makes sense. Every value is sourced. Where an office publishes no time, say "not published".
- A decision helper with no JavaScript: "Is your document federal (FBI check, federal court) → US Department of State; state-issued or notarized in a state → that state." We already have /guides/state-or-federal-which-office/. Link it from every state page's opening section.

### 4.4 Benchmarks
I found no independent, methodologically sound public benchmark for affiliate CTR on informational content sites. The figures in circulation come from vendor blogs with undisclosed samples, so this playbook **does not set a target from them**. We will set our own baseline from GoatCounter: `aff-*` events divided by page views per page, reviewed monthly.

---

## 5. Realistic timeline (only sourced statements)
- **Days to weeks:** crawling and indexing after sitemap submission and IndexNow. Google says changes can take "a few hours" to "several months" and to "wait a few weeks to assess" (SEO Starter Guide).
- **Within about a month:** of the new pages that ever reach the top 10, Ahrefs found 40.82% got there within a month. Most new pages never do (1.74% overall, 6.11% for non-empty English content, within a year).
- **Months:** AI features can take "several days to several months" to reflect changes (ai-features page).
- **About 6 months:** Ahrefs' rule of thumb is to update a page if it still isn't ranking.
- **Years:** 72.9% of top-10 pages are over 3 years old (Ahrefs). Authority compounds slowly.
- **No revenue number is forecast here.** Any figure would be invented.

---

## 6. Prioritized 30/60/90-day action list

### Days 0–30
1. **[ACCOUNT]** Finish Search Console: the meta tag is already on every page. Verify the property and submit /sitemap.xml. Then use "Import from Google Search Console" in **Bing Webmaster Tools** to unlock Bing's AI Performance (Copilot citation) report.
2. **[ME]** Build the **state fee and time dataset page** plus a CSV, with sources per cell, a methodology note and Dataset JSON-LD. Do not add it to the main nav unless the user agrees. Link it from the home page and guides index.
3. **[ME]** Change the inline label "(affiliate link)" to "(paid link)" and keep the adjacent commission sentence, per the FTC FAQ.
4. **[ME]** Expand the About / How we make pages section: AI-assisted drafting, every fact checked against the linked official source, a corrections email, no fake author.
5. **[ME]** Continue nightly pages in buyer-intent order (backlog.md). Each must be unique and sourced (doorway check: the page needs facts that differ by state).
6. **[ME]** The cross-state comparison guide now exists (/guides/apostille-services-compared/, commit df8da18). Next, add a small per-state "DIY by mail vs DIY in person vs paid service" table to each state page and link the comparison guide from it. Build it from existing data only, with no new claims.
7. **[ME]** Change traffic-plan.md wording so dates change only after a real re-check.

### Days 31–60
8. **[ME → APPROVAL]** Broken-link research on .gov, .edu and LibGuides apostille resource pages, then draft emails that offer the official replacement URL first.
9. **[APPROVAL]** Second wave of resource-page outreach (libraries, TEFL/Fulbright pages), once the first 10 university replies are reviewed. One email each, no follow-up chains.
10. **[APPROVAL]** Curlie submission (single category).
11. **[ACCOUNT]** Genuine answers on Stack Exchange or Reddit or Quora where an apostille question is open. I draft, the user posts and discloses. No affiliate links.
12. **[ME]** Monthly re-check of every published fee and time. Update `last_reviewed` only on pages actually re-verified, and log changes in the accuracy-audit file.

### Days 61–90
13. **[ME]** Review Search Console, Bing AI Performance and GoatCounter data. Improve the opening answers and titles on pages with impressions but no clicks. Re-check pages with zero impressions for uniqueness.
14. **[ACCOUNT]** Optional: subscribe to Source of Sources or HARO, and answer only apostille or moving-abroad queries as the user, honestly.
15. **[ME]** Pitch the dataset as a citable resource in outreach drafts (for example "fees in 20+ states, each linked to the official page"), only once coverage justifies it.
16. **[APPROVAL]** Decide whether a ~$10/yr custom domain is worth it. Budget is $0 now, so deferred.

Never: buy links, exchange links, submit to bulk directories, post affiliate links in communities, create fake reviews or personas, mass-generate pages, or change dates without a re-check.
