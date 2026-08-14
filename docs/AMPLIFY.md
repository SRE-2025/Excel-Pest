# Deploy on AWS Amplify (active hosting path)

This project is set up for **AWS Amplify Hosting**. Amplify connects directly to
this GitHub repo, builds on every push, and gives you a free live URL like
`https://<branch>.<app-id>.amplifyapp.com` — the "dummy link" for testing. You
attach the real domain later, with no downtime.

The repo is already Amplify-ready:
- `amplify.yml` at the repo root tells Amplify to publish the static `./site`
  folder (no build step).
- Everything servable lives in `./site`.

You do the connection once, in the AWS Console. It takes ~5 minutes.

---

## One-time setup

1. Sign in to the **AWS Console** → open **AWS Amplify**.
2. Click **Create new app** → **Host web app**.
3. Choose **GitHub** as the source and authorize AWS Amplify to access the
   `SRE-2025/Excel-Pest` repository.
4. **Repository:** `SRE-2025/Excel-Pest`.
   **Branch:** `claude/website-github-aws-setup-j7tr24` (this gives you a dummy
   link right now without touching a production branch). You can add/switch to
   `main` later for production.
5. Amplify auto-detects `amplify.yml`. Leave the build settings as detected —
   the output directory is `site`. No build command is needed.
6. Click **Save and deploy**.

When the build finishes (green), Amplify shows your live URL:
`https://claude-website-github-aws-setup-j7tr24.<app-id>.amplifyapp.com`

That's the dummy link. Share it, click through it, test on a phone.

---

## Recommended after the first deploy

**Add a 404 rewrite** so unknown paths show our styled 404 page:
Amplify app → **Hosting → Rewrites and redirects → Manage redirects**:

| Source address | Target address | Type |
|----------------|----------------|------|
| `/<*>`         | `/404.html`    | `404 (Not Found)` |

---

## Attaching the real domain later (no downtime)

When the client's domain is ready to point at the new site:

1. Amplify app → **Hosting → Custom domains → Add domain**.
2. Enter `excelpest-lawncontrol.com`, add the `www` subdomain if wanted.
3. Amplify issues a managed SSL certificate and shows the DNS records to add.
   Add them at the domain's DNS provider (Route 53 is automatic if the domain
   is there).
4. Amplify keeps the old dummy URL working, so there is **no downtime** — the
   domain only starts serving the new site once DNS propagates and the
   certificate validates.

> Do the domain cutover only when: the client's domain ownership is confirmed,
> the duplicate indexed site (`reasonsystems.us`) is handled, and the phone
> numbers are cleaned up — the three launch blockers from the brief.

---

## Auto-deploy

Once connected, **every push to the connected branch redeploys automatically** —
no extra CI to manage. Edit files under `site/`, push, and Amplify rebuilds.

The `.github/workflows/deploy.yml` (S3 + CloudFront) is an **alternative** path
and is manual-only; you can ignore it while on Amplify.
