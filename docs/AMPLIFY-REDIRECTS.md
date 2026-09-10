# Amplify redirect rules (fixes B2, B3, B4)

Some routing fixes from the site audit can only be set in the **AWS Amplify
console**, not in the repo — Amplify reads redirects from the console, not from
`amplify.yml`. This file holds the exact rules to paste.

## What these fix
- **B2** — old Hibu URLs (e.g. `/ant-control`) 301 to their current page instead
  of 404-ing. This is the highest-value SEO item left.
- **B3** — anything that doesn't exist serves a real `/404.html` (with a 404
  status) instead of the homepage.

## How to apply (2 minutes)
1. Amplify console → your app **Excel-Pest** → **Hosting** → **Rewrites and
   redirects**.
2. Click **Manage redirects** → **Open text editor** (JSON view).
3. Paste the contents of [`infra/amplify-redirects.json`](../infra/amplify-redirects.json).
4. **Save**. It takes effect immediately (no rebuild needed).

The catch-all `/<*> → /404.html (404)` rule **must stay last** — Amplify serves a
real file first and only falls through to it when nothing matches.

## Important caveat — the apex (B1 path preservation)
These rules run on the site Amplify serves (`www.`). Requests to the **bare
apex** (`excelpest-lawncontrol.com/...`) are handled by GoDaddy forwarding, which
only reliably forwards the root — a path like `excelpest-lawncontrol.com/about.html`
can still 404. Most of the old Hibu inbound links were on the apex.

To fully preserve the path on apex links you need the apex pointed **at Amplify**
(so it 301s to `www` with the path intact). GoDaddy can't do that at the root
(no ANAME/ALIAS). The clean options, in order of preference:
- **Move DNS to Cloudflare** (keep GoDaddy as registrar; change nameservers).
  Cloudflare supports apex flattening, so the apex can point at Amplify and
  Amplify does the apex→www redirect with the path. Free. **You must re-create
  the 5 Google MX records + SPF/DKIM/DMARC in Cloudflare or email breaks.**
- **Route 53** — same idea, same email caveat.

Until then, the console rules above cover every `www` request, which is where
new links and internal navigation point.

## Keeping it in sync
`infra/amplify-redirects.json` is generated from the `REDIRECTS` map in
`tools/build.py`. If you add a legacy URL there, re-generate the JSON and re-paste.
