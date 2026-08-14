# Austin Excel Pest & Lawn Control — Website

Static marketing website for **Austin Excel Pest & Lawn Control**
(`excelpest-lawncontrol.com`), hosted on AWS (S3 + CloudFront) and deployed
automatically from GitHub via GitHub Actions.

> This is **Website 1** of two separate sites described in the Stoneridge Digital
> brief. The sister company, Research Turf Management (`researchturfmgmt.com`),
> is a **separate** website — do not merge content between the two.

## Company facts (single source of truth)

| Field | Value |
|-------|-------|
| Business | Austin Excel Pest & Lawn Control |
| Domain | excelpest-lawncontrol.com |
| Phone | (737) 201-3059 |
| Text line | (737) 350-8553 |
| Email | office@excelpest-lawncontrol.com |
| Address | 175 Warehouse Drive, Buda, TX |
| Founded | 1998, in South Austin |
| Brand colours | Deep navy blue (`#0a1f44`) + orange (`#f26419`) |
| Sister company | Research Turf Management — (512) 233-6300 |

Do **not** change the phone number, business name, address, or email. Do not
invent prices, awards, guarantees, or staff claims. See the brief's "Start Here"
rules.

## How the site is built

The 27 pages are generated from one script so the header, nav, footer, and SEO
schema stay consistent. **Edit content in `tools/build.py`, then regenerate:**

```bash
python3 tools/build.py      # writes all pages into ./site
```

The generated HTML in `./site` is committed and is what Amplify serves — there's
no build step at deploy time.

## Repository layout

```
tools/build.py            Site generator — single source of content + layout
site/                     Generated website (this is what gets deployed)
  index.html              Home
  services.html           Services hub  +  services/*.html  (8 service pages)
  service-area.html       27-city hub   +  locations/*.html (8 city pages)
  about.html reviews.html offers.html faq.html pet-family-safety.html
  contact.html            Contact + free-estimate form (progressive-enhance)
  pay-invoice.html        Pay Your Invoice (GATED — see below)
  404.html
  css/styles.css          Brand + layout tokens (edit colours here)
  js/main.js              Mobile nav, footer year, contact-form handler
  assets/ robots.txt sitemap.xml
amplify.yml               AWS Amplify build spec (publishes ./site)
infra/cloudformation-hosting.yml   Alternative S3 + CloudFront infrastructure
.github/workflows/deploy.yml       Alternative S3 deploy (manual-only)
docs/AMPLIFY.md docs/DEPLOYMENT.md
```

### Pages

- **Core:** Home, Services, Service Area, Reviews, Offers, About, Pet & Family
  Safety, FAQ, Contact
- **Services (8):** general pest, scorpion, termite control, termite letters
  (WDI), rodent, wildlife, mosquito misting, lawn pest
- **Cities (8):** Buda, Kyle, San Marcos, Dripping Springs, Wimberley,
  Driftwood, Manchaca, Del Valle (+ all 27 listed on the hub)

### SEO built in

Unique title + meta description per page, one H1 per page, JSON-LD
(`PestControlService` with NAP/geo/hours, 5.0★ `AggregateRating`, `Service`,
`FAQPage`, `BreadcrumbList`, city-scoped schema), canonical + Open Graph tags,
internal-link mesh, sitemap, robots, and "family-owned in Buda since 1998" as
the consistent positioning.

## Local preview

```bash
cd site
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploying

**Active path: AWS Amplify.** Connect this repo in the AWS Amplify console and it
builds and hosts on every push, with a free `*.amplifyapp.com` link for testing
and a no-downtime path to attach the real domain later. Step-by-step:
**[docs/AMPLIFY.md](docs/AMPLIFY.md)**.

**Alternative path: S3 + CloudFront.** A CloudFormation stack + a (manual-only)
GitHub Actions workflow are also included if you move off Amplify later. See
**[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)**.

## ⚠️ Pay Your Invoice page

`site/pay-invoice.html` is intentionally **disabled** (`noindex`, no live PayPal
button). Per the brief, real money moves through PayPal button `PBRKNRY4BQUJG`.
Do **not** enable it until the owner confirms **in writing** that the button
belongs to his business account, then make and refund a $1.00 test payment.
The complete ready-to-use page lives in the brief's
`CODE-copy-paste-these/00_pay-invoice-page-COMPLETE.html`.

## Status / what's next

The full site is built with real content from the discovery brief and is ready
to preview and deploy to an Amplify dummy link. Before flipping the real domain
live, the brief's launch blockers still apply:

- [ ] Resolve the duplicate indexed site at `reasonsystems.us`
- [ ] Clean up the four inconsistent phone numbers across Google/Yelp/BBB/FB
- [ ] Confirm domain ownership before DNS cutover
- [ ] Add real photography (crews, trucks, completed jobs — no stock)
- [ ] Wire the contact form to real email delivery (SES/API Gateway or a form service)
- [ ] Enable `pay-invoice.html` **only** after written PayPal confirmation + $1 test
- [ ] (Nice to have) pull a live Google-reviews feed onto `reviews.html`
