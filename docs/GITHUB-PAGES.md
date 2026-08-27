# GitHub Pages — live preview link

This repo publishes a live preview of the site to **GitHub Pages** on every push
to the working branch.

**Live URL:** https://sre-2025.github.io/Excel-Pest/

## How it works

- `.github/workflows/pages.yml` runs on each push.
- It rebuilds the site with a base path (`BASE_PATH=/Excel-Pest`) so all links
  work under the `/Excel-Pest/` project sub-directory, then deploys it to Pages.
- The committed `site/` stays root-relative (base `""`) for AWS Amplify / S3 —
  only the CI build for Pages uses the base path. Nothing conflicts.

## One-time enablement

If the very first workflow run fails on a permissions/"Pages not enabled" error:

1. Repo **Settings → Pages**.
2. **Build and deployment → Source: GitHub Actions**.
3. Re-run the failed workflow (Actions tab → the run → "Re-run jobs"), or push again.

After that it deploys automatically and the URL above goes live (first publish
can take a couple of minutes).

## Note

This Pages URL is a **preview/staging** link on `github.io`, not the client's
real domain. The production domain is attached later via AWS Amplify (see
`AMPLIFY.md`). The `pay-invoice` page stays gated regardless of where it's hosted.
