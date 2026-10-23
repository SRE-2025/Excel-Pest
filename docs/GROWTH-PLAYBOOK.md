# Excel Pest: qualified-traffic growth plan

Updated 2026-10-23. Owner: Jason / Excel office. Implementation: Codex.

## Scope and success criteria

Work on Excel Pest only, not the separate lawn-care website. Advertise only
services on the current website. Wildlife means raccoons, squirrels and
opossums; rodent work means rats and mice. Do not add other animals from the
legacy Hibu site. Termite content may explain a concern but must not sell a
termite inspection, treatment or letter. Never fabricate jobs, reviews, prices,
guarantees or location-specific experience.

Primary outcome: qualified inquiries and booked work, not raw visits. Analytics
clicks are not completed phone calls. A successful form-backend response is not
proof an email was read or a job booked. No baseline or growth percentage is
available without the account data; leave those fields unknown.

## Six workstreams

| Workstream | First pass | Next evidence / owner action |
| --- | --- | --- |
| Google Business Profile and reviews | Office checklist and unbiased request templates below | Office provides profile access, exact Google review URL, verified hours and categories |
| Pest library | `/pest-library.html`: 10 pest groups, linked services and guides; new fire-ant and cockroach guides | Improve based on actual Search Console queries, not guessed volumes |
| Service conversion | All 12 service pages explain estimate factors, what to tell the office and scope questions; service-selection links; smaller right-hand image layout | Owner confirms any actual warranty or response-time promise before adding it |
| Seasonal content | `/insights/central-texas-pest-calendar.html`: 12-month prevention checklist | Review seasonally; weather-dependent, not a guaranteed infestation forecast |
| Local authority | Four researched outreach opportunities and draft below | Owner approves contacts/membership costs; nothing sent or purchased |
| Measurement | Production-only phone, text, email, estimate-click, form-start, confirmed-form and fallback events | GA4 access to verify event receipt and key-event settings; Search Console baseline |

## 1. Office review and Google profile workflow

First verify the existing profile: business name, address/service-area display,
phone, hours, primary category and current services. Do not create a duplicate
profile or add fake offices to target cities. Use current, owner-approved photos
of people, trucks and real jobs; do not pass generated stock imagery off as work.

Get the review link from the business's own Google profile, not a search-result
guess. Save it in the office's approved template. Ask genuine serviced customers
consistently, without screening for satisfaction, requesting five stars, offering
incentives or diverting unhappy customers to a private-only channel. Use only a
channel the customer has agreed to use. The office handles sending and replies.

Short request (replace the link before use):

> Thank you for choosing Excel Pest. Would you share an honest review of your
> experience? Your feedback helps other local homeowners: [VERIFIED GOOGLE REVIEW
> LINK]. If you need help with your service, please call us at (512) 291-5900.

Optional follow-up, once, only where appropriate:

> Thanks again for working with Excel Pest. If you would like to leave feedback,
> here is our review link: [VERIFIED GOOGLE REVIEW LINK]. We appreciate your time.

Do not publish either placeholder. Use Google's own review QR option once the
correct profile is verified. Ask the office to record request date and response
status in its existing customer system; do not add customer names to this repo.

Profile website link to consider after owner verification:
`https://www.excelpest-lawncontrol.com/?utm_source=google&utm_medium=organic&utm_campaign=business_profile`

Sources: [Google local ranking guidance](https://support.google.com/business/answer/7091),
[Google's review-request guidance](https://support.google.com/business/answer/3474122).
Profile completeness and reviews can help discovery and trust; no position is promised.

## 2–4. Content and conversion next steps

The library routes symptoms to actual services. New articles target useful
questions, not unverified search-volume estimates. The calendar is a practical
maintenance checklist. Existing guides and new service sections link together.

Check the publishing routines before drafting another article: Claude's existing
schedule is documented in CONTENT-AUTOMATION.md, but its execution was not
verified in this pass. Do not duplicate topics or publish for volume alone.

Next topics to assess against Search Console: cricket entry points, flea/tick
visit preparation, and rodent removal versus exclusion. Prefer improving a
relevant existing page over making overlapping pages. Service-by-city pages
require distinct local evidence and demand; do not generate all city/service
combinations. Do not label fictional neighborhood jobs as real examples.

## 5. Local-link and referral preparation

These are researched opportunities, not claimed memberships or acquired links.
Check the directory first so an existing listing is corrected rather than duplicated.

| Opportunity | Verified destination | Proposed action |
| --- | --- | --- |
| Greater Buda Chamber | https://www.budachambertx.com/member-directory | Check for an existing listing; ask about correct category and eligibility |
| Kyle Area Chamber | https://www.kylechamber.org/ | Check directory/membership and genuine local networking opportunities |
| San Marcos Area Chamber, Texas | https://sanmarcostexas.com/ | Check local directory and business-resource opportunities; not the California chamber |
| Research Turf Management | https://researchturfmgmt.com | Confirm a helpful sister-company pest-service referral link with its owner; no automated link swap |

Draft for an approved contact (not sent):

> Hello, I help Austin Excel Pest & Lawn Control in Buda keep its local business
> information accurate. Could you let us know whether we already have a listing
> and the requirements for updating or being included in your directory? Our
> website is https://www.excelpest-lawncontrol.com/ and our phone is
> (512) 291-5900. We would also welcome information about relevant local business
> events. Thank you.

Use the normal business name and accurate destination, not keyword-stuffed anchor
text. Do not buy SEO links. Memberships/sponsorships require owner approval and
should have real business value, not a promised ranking benefit. Outreach log:
organization, existing-listing URL, owner-approved contact date, reply, next step.

## 6. Measurement and weekly scorecard

GA4 measurement ID in the site: `G-LDWMBCL4D9`. The implementation adds no new
analytics vendor. No names, emails, phone numbers, ZIPs or message text are sent
as custom event parameters.

| Event | What it actually means |
| --- | --- |
| `phone_click` / `sms_click` / `email_click` | A contact link was selected, not a completed contact |
| `estimate_cta_click` | A visitor selected a link to the estimate page |
| `estimate_form_start` | First form input on this page visit |
| `generate_lead` | The email service accepted a valid form submission; excludes honeypot fills |
| `estimate_form_fallback` | AJAX did not confirm success; normal POST or email-app fallback attempted |

Parameters are limited to page path, link placement, allowlisted service category,
and method. Service-specific links preserve the requested service if the visitor
keeps its matching form option; otherwise the selected broad group is used.
Never count a fallback as confirmed
delivery. The Google Sheet backup is best effort and is not independently verified.

With account access: test in GA4 Realtime/DebugView, mark the appropriate events
as key events, disable duplicate automatic form events if needed, and confirm
privacy/consent settings with the owner. Do not import click events into Ads as
booked jobs. No ad campaign or budget is authorized by this plan.

| Weekly metric | Baseline | Source |
| --- | --- | --- |
| Organic clicks and impressions by page/query | Unknown | Search Console, last 28 vs previous 28 days |
| Indexed canonical URLs / sitemap errors | Unknown | Search Console Page indexing |
| Organic sessions and landing pages | Unknown | GA4 |
| Phone clicks and accepted forms | Unknown | GA4, separate channels |
| Qualified inquiries / jobs booked | Unknown | Office log, aggregate counts only |
| Review requests / new honest reviews | Unknown | Office log / verified Google profile |

Weekly: check deployment and service accuracy, inspect account data if available,
select the highest-evidence improvement, test it, and log the change. Avoid daily
ranking conclusions. Request reindexing only for meaningful changes, not every
page on every run. Without accounts, report only observable site changes.

## Claude review: second pass

Read-only consultation completed in the existing Excel Pest Claude conversation
on 2026-10-23. Claude could inspect the repo but its live-site requests were blocked.
Its conclusions are leads to verify, not independent evidence of live indexation.

- Done: added links to five existing city pages from all 12 services.
- Verification correction: Claude described rating schema as site-wide, but it
  was only in an unused reviews renderer. Removed that dormant capability and
  the unverified numeric rating/count badges actually visible on the website.
  Google does not award review snippets for self-serving LocalBusiness reviews;
  this pass does not claim the site had a manual action.
  [Google policy](https://developers.google.com/search/docs/appearance/structured-data/review-snippet).
- Done: analytics loading and custom events restricted to the production domain.
- Done: sitemap uses known article revision dates, not a new date for every page
  on every build; other pages omit lastmod until a reliable date is available.
- Done: removed the separate lawn brand from the pest business's sameAs identity
  links. The normal sister-company referral links remain intact.
- Do not copy old Hibu photos: Jason explicitly rejected old-site imagery. Real
  team/truck/job photography requires owner assets; generated images must not
  masquerade as those assets. Image-slot work remains separately tracked.
- Guarantees, financing, same-day response and free return visits remain pending
  owner confirmation, not copywriting opportunities to invent promises.
- Verify live redirects and Search Console indexation; console configuration is
  not proven by a file in the repo.

## Change log

- 2026-10-23: first six workstreams implemented/prepared; termite guide corrected;
  current wildlife scope documented. Checks pass for 81 HTML pages and 57 sitemap
  URLs at both root and preview paths. Nineteen routes checked at desktop and
  mobile widths, including all 12 service pages. Conversion tests use mock
  requests, with no emails or analytics sent. Changes pushed in commit `75ef6c5`;
  the production library, calendar, service estimate section and tracking script
  returned HTTP 200 with the new content. GitHub preview also serves the library
  with correctly prefixed links. Weekly follow-up scheduled for Mondays at
  10:00 a.m. America/Los_Angeles in this chat. Google account connections remain
  outstanding; no ranking or traffic improvement has yet been measured.
