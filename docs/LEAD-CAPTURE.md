# Lead capture — never lose a submission

Every estimate-form submission is sent to **two** independent places, so a lead
survives even if one path fails:

1. **Email → office@excelpest-lawncontrol.com** (via FormSubmit) — the immediate
   notification.
2. **A Google Sheet you own** (via a Google Apps Script Web App) — a permanent
   record you can open any time. If email ever has a sending error, every lead is
   still sitting in the Sheet to follow up on.

The site posts to both in parallel on each submit. The Sheet write is
fire-and-forget, so it never slows down or breaks the visitor's experience.

## Turn on the Sheet (one time, ~3 minutes)

1. Create a Google Sheet, e.g. **"Excel Pest — Website Leads."**
2. In it: **Extensions → Apps Script**. Delete the sample code, paste the entire
   contents of [`infra/lead-capture.gs`](../infra/lead-capture.gs), and **Save**.
3. **Deploy → New deployment → Web app**:
   - **Execute as:** Me
   - **Who has access:** Anyone
   - Click **Deploy**, authorize when Google prompts, and **copy the Web app URL**
     (it ends in `/exec`).
4. **Send that `/exec` URL back** — it gets pasted into `LEAD_SHEET_ENDPOINT` in
   `tools/build.py`, the site rebuilds, and from then on every submission is
   logged to the Sheet automatically.

That's it. No API keys, no monthly cost, and the data lives in your Google account.

## Do I get duplicate emails?

No — by default the Apps Script only **logs** to the Sheet (`NOTIFY_EMAIL` is
blank), and FormSubmit handles the email. If you'd rather this script *also* email
you a copy (or replace FormSubmit entirely), set `NOTIFY_EMAIL` at the top of the
script to `office@excelpest-lawncontrol.com`.

## How to recover leads after an email problem
Open the Sheet. Every row is a lead with a timestamp, name, phone, email, service,
what they were seeing, city and message. Sort by timestamp, work the ones that
came in during the outage. Nothing is lost.

## Redeploying the script later
If you change the `.gs` code, use **Deploy → Manage deployments → Edit → New
version** so the same `/exec` URL keeps working (a brand-new deployment makes a
new URL, which would need to be re-pasted into the site).
