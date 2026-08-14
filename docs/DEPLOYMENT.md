# Deployment — S3 + CloudFront (alternative path)

> **The active hosting path for this project is AWS Amplify** — see
> [AMPLIFY.md](AMPLIFY.md). This document describes the alternative S3 +
> CloudFront setup, kept for teams that prefer it or move off Amplify later.
> The GitHub Actions workflow for this path is manual-only and will not run
> automatically.

This site deploys to **AWS S3 + CloudFront**. GitHub Actions authenticates to
AWS using **OIDC** — an IAM role is assumed at deploy time, so there are **no
long-lived AWS keys** stored in GitHub.

You do this setup **once**. After that, every push to `main` that touches
`site/**` deploys automatically.

---

## What you need

- An AWS account and permission to create CloudFormation stacks, S3, CloudFront,
  and IAM resources.
- The AWS CLI installed and logged in (`aws configure` / SSO), **or** access to
  the AWS Console.
- Admin access to this GitHub repository (to add secrets/variables).

---

## Step 1 — Deploy the AWS infrastructure

The template `infra/cloudformation-hosting.yml` creates the S3 bucket, the
CloudFront distribution, and the GitHub deploy role.

> CloudFront certificates must live in **us-east-1**, so deploy the stack there.

```bash
aws cloudformation deploy \
  --region us-east-1 \
  --stack-name excel-pest-hosting \
  --template-file infra/cloudformation-hosting.yml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
      GitHubOrg=SRE-2025 \
      GitHubRepo=Excel-Pest \
      GitHubBranch=main
```

**If your AWS account already has a GitHub OIDC provider** (common if you deploy
other repos from GitHub), add `CreateOIDCProvider=false` to the
`--parameter-overrides` so the stack doesn't try to create a second one.

### Get the outputs

```bash
aws cloudformation describe-stacks \
  --region us-east-1 --stack-name excel-pest-hosting \
  --query "Stacks[0].Outputs" --output table
```

You'll get four values:

| Output | Use it for |
|--------|-----------|
| `BucketName` | GitHub **variable** `S3_BUCKET` |
| `DistributionId` | GitHub **secret** `CLOUDFRONT_DISTRIBUTION_ID` |
| `DeployRoleArn` | GitHub **secret** `AWS_DEPLOY_ROLE_ARN` |
| `DistributionDomain` | The live URL (e.g. `d123.cloudfront.net`) |

---

## Step 2 — Add GitHub secrets and variables

Repo → **Settings → Secrets and variables → Actions**.

**Secrets** (Secrets tab):

| Name | Value |
|------|-------|
| `AWS_DEPLOY_ROLE_ARN` | `DeployRoleArn` output |
| `CLOUDFRONT_DISTRIBUTION_ID` | `DistributionId` output |

**Variables** (Variables tab):

| Name | Value |
|------|-------|
| `AWS_REGION` | `us-east-1` |
| `S3_BUCKET` | `BucketName` output |

---

## Step 3 — First deploy

Either merge a change to `main` under `site/**`, or trigger it manually:

Repo → **Actions → "Deploy site to AWS" → Run workflow**.

When it finishes, open the `DistributionDomain` URL. The site is live.

---

## Step 4 — Custom domain (optional, when DNS is ready)

The brief flags that domain ownership must be confirmed before launch (the site
is currently on Hibu). Once you control DNS for `excelpest-lawncontrol.com`:

1. Request an **ACM certificate** in **us-east-1** for `excelpest-lawncontrol.com`
   (and `www.` if wanted) and validate it via DNS.
2. Redeploy the stack adding:
   ```
   DomainName=excelpest-lawncontrol.com
   AcmCertificateArn=arn:aws:acm:us-east-1:<acct>:certificate/<id>
   ```
3. Point the domain's DNS (a CNAME/ALIAS) at the `DistributionDomain`.

---

## How auto-deploy works

```
push to main (site/** changed)
        │
        ▼
GitHub Actions  ──OIDC──▶  assume IAM role (excel-pest-github-deploy)
        │
        ├─ aws s3 sync ./site  → S3 bucket
        └─ aws cloudfront create-invalidation → refresh the CDN
```

Workflow file: `.github/workflows/deploy.yml`.

---

## Coming back to develop later

Everything needed to rebuild this site lives in this repo — nothing is trapped
in a session or a rented platform. To continue development:

1. Clone the repo and edit files under `site/`.
2. Preview locally (`python3 -m http.server` in `site/`).
3. Open a PR; merge to `main`; it deploys automatically.

### Remaining content to add (from the full brief)

- [ ] Paste real page copy from `PAGE-COPY-one-file-per-page` into the page shells
- [ ] Build the 16 service pages (Part 3) and link them from `services.html`
- [ ] Build the location / service-area pages (Part 4)
- [ ] Wire the contact form to real email delivery (Part 1, Section 5)
- [ ] Add JSON-LD schema blocks (Part 1, Section 6)
- [ ] Generate + add images with alt text (Part 1, Section 11)
- [ ] Add 301 redirects from the old site (Part 1, Section 8)
- [ ] Resolve the three launch blockers (duplicate site, phone-number cleanup,
      domain ownership) before going live
- [ ] Enable `pay-invoice.html` **only** after written PayPal confirmation + $1 test
