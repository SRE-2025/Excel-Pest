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

## Repository layout

```
site/                     The website (this is what gets deployed)
  index.html              Home
  about.html              About
  services.html           Services hub
  contact.html            Contact + free-estimate form
  pay-invoice.html        Pay Your Invoice (GATED — see below)
  404.html                Not-found page
  css/styles.css          Brand + layout tokens (edit colours here)
  js/main.js              Mobile nav + small helpers
  assets/                 Favicon and images
  robots.txt, sitemap.xml
infra/
  cloudformation-hosting.yml   AWS infrastructure (S3 + CloudFront + OIDC role)
.github/workflows/
  deploy.yml              Deploy ./site to AWS on push to main
docs/
  DEPLOYMENT.md           Step-by-step AWS + GitHub connection guide
```

## Local preview

No build step — it's plain HTML/CSS/JS. Serve the folder:

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

This is the site **foundation**: brand system, core pages, and the full
GitHub → AWS deploy pipeline. To finish the build you still need the full
Excel Pest brief (Parts 1–4) — specifically the `PAGE-COPY-one-file-per-page`
copy files, the 16 service-page specs, the location pages, schema blocks, and
image prompts. Paste that content into these page shells. See the checklist in
`docs/DEPLOYMENT.md`.
