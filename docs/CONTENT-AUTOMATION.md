# Automated content publishing (SEO + AEO guides)

This site publishes fresh **Pest Guides** on a schedule to grow organic search
(SEO) and answer-engine (AEO) visibility. Each guide is one JSON file that the
generator turns into a fully-optimized page (Article + FAQ schema, meta tags,
canonical, sitemap entry, internal links). Content is added by **scheduled
Claude Code Routines** — no human action required.

- **SEO guides** publish **Wednesday & Friday**.
- **AEO guides** publish **Monday & Thursday**.

Everything auto-deploys on push (AWS Amplify / GitHub Pages).

---

## How to publish one guide (the exact process)

1. **Pick a fresh topic** for Central Texas homeowners that is **not already
   covered**. List existing guides first:
   ```
   ls content/articles/
   ```
   Cover the currently advertised services: scorpions, rats and mice, raccoons,
   squirrels and opossums,
   mosquitoes, ants, roaches, crickets, fleas, ticks, spiders, wasps, lawn
   pests — and tie topics to local places/seasons (Buda, Kyle, San Marcos,
   Dripping Springs, Wimberley, the Hill Country, and the Central Texas pest
   calendar). Never repeat an existing slug or angle. Use the current service
   menu, not old Hibu pages. Do not advertise termite work, bats, snakes,
   armadillos, skunks or feral cats. Jason confirmed this scope on 2026-10-23.
   The existing termite guide is informational only and must not imply Excel
   offers termite inspections or treatment.

2. **Write one file** at `content/articles/<slug>.json` using the schema below.
   - Slug: short, lowercase, hyphenated, keyword-first, unique.

3. **Build and sanity-check:**
   ```
   python3 tools/build.py
   ```
   Confirm it prints `[articles] published N guide(s)` with no traceback and
   that `site/insights/<slug>.html` exists.

4. **Commit and push** to the working branch:
   ```
   git add content/articles/<slug>.json site/
   git commit -m "Add pest guide: <title>"
   git push origin claude/website-github-aws-setup-j7tr24
   ```
   Amplify redeploys automatically. Done.

---

## Article JSON schema

```json
{
  "slug": "keyword-first-hyphenated-slug",   // required, unique
  "title": "Question or clear headline",       // required
  "date": "YYYY-MM-DD",                        // original publication date
  "updated": "YYYY-MM-DD",                     // optional: substantive revision
  "informational_only": false,                 // true suppresses service CTAs
  "kind": "seo",                                // "seo" (Wed/Fri) or "aeo" (Mon/Thu)
  "description": "150-158 char meta description with the target keyword.",
  "summary": "One-sentence dek shown on the index and hero.",
  "keywords": ["primary keyword", "secondary", "local variant"],
  "quick_answer": "AEO only: 1–3 sentence direct answer (may include <strong>).",
  "related_services": ["scorpion-control", "pest-control"],  // valid service slugs
  "body_html": "<h2>…</h2><p>…</p><ul><li>…</li></ul>  (600–900 words)",
  "faqs": [ { "q": "Question?", "a": "<p>Concise answer.</p>" } ]
}
```

Only `slug`, `title`, `date`, and `body_html` are strictly required; a malformed
file is skipped so it can never break the build.

### Valid `related_services` slugs
`pest-control`, `scorpion-control`, `rodent-removal`, `rodent-exclusion`,
`wildlife-live-trapping`, `mosquito-misting`, `ant-control`, `cockroach-control`,
`cricket-control`, `flea-tick-control`, `spider-control`, `lawn-pest-control`.
(Termite control/letters were removed; flea & tick are now one combined service.)

---

## SEO guides (Wednesday & Friday) — `"kind": "seo"`
Goal: rank in Google for what local homeowners search.
- Title is a keyword-rich how-to / guide (e.g. *"How to Keep Scorpions Out of
  Your Central Texas Home"*).
- 600–900 words, `<h2>`/`<h3>` structure, scannable lists.
- Work the primary keyword into title, first paragraph, one H2, and the meta
  `description`. Add local place names naturally.
- Link to 1–2 relevant services via `related_services`, and mention the service
  in-body where it fits (the generator also renders a related-services block).
- Include 2–3 `faqs`.

## AEO guides (Monday & Thursday) — `"kind": "aeo"`
Goal: be the sentence an AI answer engine (ChatGPT, Perplexity, Google AI
Overviews) quotes.
- Title is a **natural question** people ask (e.g. *"When Are Scorpions Most
  Active in Central Texas?"*).
- **Always set `quick_answer`** — a direct, factual, self-contained answer in
  the first 1–3 sentences. Citation by an answer engine is not guaranteed.
- Body expands with clear H2 sections and lists; keep claims accurate and
  specific to Central Texas.
- Include 3+ `faqs` phrased as real questions with concise answers (FAQ schema
  is emitted automatically; it does not guarantee rich results or AI citations).

## Quality rules (both types)
- **Accurate and genuinely useful** — no filler, no invented statistics.
- **Local** — Central Texas / Hays & Travis County framing.
- **Unique** — never duplicate an existing guide's slug, title, or angle.
- Keep the brand voice: quiet, expert, family-owned since 1998. Do not call
  treatments universally safe: use product-specific preparation and re-entry
  instructions from the technician and product label. Phone is **(512) 291-5900**.
- Do not invent prices, guarantees, response times, reviews, job photos or local
  experience. See [GROWTH-PLAYBOOK.md](GROWTH-PLAYBOOK.md) for measurement and scope.
- One guide per run.
