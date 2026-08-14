#!/usr/bin/env python3
"""
Static-site generator for Austin Excel Pest & Lawn Control.

All pages are generated from the data below so the header, footer, navigation
and schema stay consistent across the whole site. Run:

    python3 tools/build.py

Output is written into ./site (served as-is by AWS Amplify). Everything is
grounded in the Stoneridge Digital discovery brief — no invented prices,
awards, or claims.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

# --------------------------------------------------------------------------
# Business facts (single source of truth — from the discovery brief)
# --------------------------------------------------------------------------
BIZ = {
    "name": "Austin Excel Pest & Lawn Control",
    "legal": "Austin Excel Pest & Lawn Control Inc.",
    "short": "Excel Pest",
    "domain": "https://excelpest-lawncontrol.com",
    "phone": "(737) 201-3059",
    "phone_tel": "+17372013059",
    "text": "(737) 350-8553",
    "text_tel": "+17373508553",
    "email": "office@excelpest-lawncontrol.com",
    "street": "175 Warehouse Drive, Ste A",
    "city": "Buda",
    "state": "TX",
    "zip": "78610",
    "license": "TPCL 0786979",
    "founded": "1998",
    "owner": "Gye Hutson",
    "office_mgr": "Megan Avery",
    "rating": "5.0",
    "reviews": "41",
    "lat": 30.0813,
    "lng": -97.8403,
    "sister_name": "Research Turf Management",
    "sister_url": "https://researchturfmgmt.com",
    "sister_phone": "(512) 233-6300",
    "bbb": "https://www.bbb.org/us/tx/buda/profile/pest-control/excel-pest-lawn-control-0825-90034821",
    "yelp": "https://www.yelp.com/biz/austin-excel-pest-and-lawn-control-buda",
    "facebook": "https://www.facebook.com/ExcelPestandLawnControl/",
    "youtube": "https://www.youtube.com/@excelpestlawncontrol",
}

NAV = [
    ("Home", "/"),
    ("Services", "/services.html"),
    ("Service Area", "/service-area.html"),
    ("Reviews", "/reviews.html"),
    ("Offers", "/offers.html"),
    ("About", "/about.html"),
    ("Contact", "/contact.html"),
]

# All 27 service-area cities (priority ones link to a city page)
ALL_CITIES = [
    "Austin", "Barton Creek", "Bear Creek", "Bee Cave", "Blanco", "Briarcliff",
    "Buda", "Canyon Lake", "Creedmoor", "Del Valle", "Driftwood",
    "Dripping Springs", "Hudson Bend", "Johnson City", "Kyle", "Lakeway",
    "Lost Creek", "Manchaca", "Mustang Ridge", "Niederwald", "Point Venture",
    "Redwood", "San Marcos", "Sunset Valley", "Uhland", "West Lake Hills",
    "Wimberley",
]

# --------------------------------------------------------------------------
# Services (grounded in "What They Actually Sell")
# --------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "pest-control", "nav": "General Pest Control", "icon": "🐜",
        "h1": "General Pest Control in Buda & Central Texas",
        "title": "Pest Control in Buda & Central Texas | Excel Pest since 1998",
        "desc": "Water-based, pet-safe pest control for ants, roaches, crickets, spiders, fleas and ticks across Buda, Kyle and Central Texas. Free estimates — call (737) 201-3059.",
        "lead": "Central Texas homes face a year-round rotation of pests — ants in spring, crickets and scorpions in the late-summer heat, spiders and roaches as it cools. We have treated them here since 1998, with water-based products chosen so your family and four-legged family members stay comfortable.",
        "treats": ["Ants", "Cockroaches", "Crickets", "Fleas", "Spiders", "Ticks", "Silverfish", "Wasps & hornets"],
        "sections": [
            ("Built for Central Texas pests", "<p>Franchise crews run the same program in Ohio as they do in Hays County. We do not. Our recurring treatments are timed to the local calendar — the spring ant push, the summer scorpion and cricket surge, the fall migration indoors — so pests are handled before they become an infestation, not after.</p>"),
            ("How our treatments work", "<p>Every visit covers the interior trouble spots and a full exterior barrier: foundation, eaves, window frames, garage, and the cracks in limestone and slab where Central Texas pests get in. We seal and treat entry points rather than just spraying baseboards. Most homes are on a recurring plan; one-time and emergency service are available too.</p>"),
        ],
        "related": ["scorpion-control", "rodent-control", "lawn-pest-control"],
    },
    {
        "slug": "scorpion-control", "nav": "Scorpion Control", "icon": "🦂",
        "h1": "Scorpion Control in the Central Texas Hill Country",
        "title": "Scorpion Control Buda, Dripping Springs & Wimberley | Excel Pest",
        "desc": "Striped bark scorpions love Hill Country limestone. Excel Pest treats and seals them out across Buda, Dripping Springs and Wimberley. Call (737) 201-3059.",
        "lead": "If you live west of I-35, you know the striped bark scorpion. They thrive in the limestone, cedar and rock that define the Hill Country, and they slip into homes through the smallest gaps. Scorpions are one of the clearest signs you are dealing with Central Texas — and one of the reasons homeowners call us.",
        "treats": ["Striped bark scorpions", "Nesting sites in rock & wood piles", "Entry points around slab & pier-and-beam", "Attic & garage harborage"],
        "sections": [
            ("Why scorpions get inside here", "<p>Scorpions follow moisture and prey. During a Hill Country drought they move toward homes for water; after rain they move to escape it. Limestone foundations, weep holes, and gaps under thresholds give them an easy path indoors, often into bathrooms and closets.</p>"),
            ("Our scorpion approach", "<p>Treating the inside alone never solves a scorpion problem. We treat the perimeter and harborage — rock walls, wood piles, landscaping — reduce the insects scorpions feed on, and seal the entry points that let them in. It is the same exclusion-first method that keeps them out for the long term.</p>"),
        ],
        "related": ["pest-control", "rodent-control", "termite-control"],
    },
    {
        "slug": "termite-control", "nav": "Termite Control", "icon": "🪵",
        "h1": "Termite Control & Inspections in Central Texas",
        "title": "Termite Control & Inspection in Buda, TX | Excel Pest since 1998",
        "desc": "Subterranean termite inspections and treatment for Central Texas homes, backed by our workmanship warranty. Licensed TPCL 0786979. Call (737) 201-3059.",
        "lead": "Subterranean termites are the quiet, expensive threat to a Central Texas home. They work out of sight for years, and clay soils that swell and crack in our droughts give them constant access to a foundation. A licensed inspection is the only way to know where you stand.",
        "treats": ["Subterranean termites", "Mud tubes on the foundation", "Hollow or blistered wood", "Swarms after spring rain"],
        "sections": [
            ("Inspection first, then a plan", "<p>We start with a thorough inspection — interior, exterior, and the crawl or slab line — and show you what we find. If there is active termite pressure, we treat it and set up a barrier to keep the colony from coming back. Our work is backed by a warranty.</p>"),
            ("Buying or selling a home?", "<p>If you need the official paperwork for a real-estate closing, see our <a href=\"/services/termite-letters.html\">termite letters &amp; WDI reports</a> page — we schedule those quickly for lenders and title companies across Hays and Travis County.</p>"),
        ],
        "related": ["termite-letters", "pest-control", "scorpion-control"],
    },
    {
        "slug": "termite-letters", "nav": "Termite Letters (WDI)", "icon": "📄",
        "h1": "Termite Letters & WDI Reports for Home Closings",
        "title": "Termite Letters & WDI Reports for Closings | Buda & Central TX",
        "desc": "Official termite letters (WDI reports) for real-estate closings across Hays and Travis County. Fast scheduling for lenders and title. Licensed TPCL 0786979.",
        "lead": "A home sale in Texas often needs a WDI report — the official \"termite letter\" a lender or title company requires before closing. We are a licensed Texas pest control operator (TPCL 0786979) and we schedule these inspections quickly so your closing stays on track.",
        "treats": ["WDI reports for closings", "Lender & title requirements", "Re-inspections", "Buyer & seller inspections"],
        "sections": [
            ("What the report covers", "<p>A Wood Destroying Insect (WDI) inspection documents any evidence of termites and other wood-destroying insects on the standard state form your lender needs. You get clear results and, if anything is found, straightforward options — including <a href=\"/services/termite-control.html\">termite treatment</a> before the deadline.</p>"),
            ("Booked around your closing date", "<p>Closings do not wait, so we do not make you wait. Tell us your date and property, and we schedule the inspection and turn the paperwork around promptly. Serving Buda, Kyle, San Marcos, Dripping Springs and the surrounding corridor.</p>"),
        ],
        "related": ["termite-control", "pest-control", "rodent-control"],
    },
    {
        "slug": "rodent-control", "nav": "Rodent Control", "icon": "🐀",
        "h1": "Rodent Control & Exclusion in Central Texas",
        "title": "Rodent Control & Exclusion in Buda, TX | Rats & Mice | Excel Pest",
        "desc": "Rats and mice removed and sealed out of Central Texas homes — attics, garages and walls. Exclusion so they don't return. Call (737) 201-3059 for a free estimate.",
        "lead": "Rats and mice do not just leave droppings — they chew wiring, foul insulation, and spread through an attic fast. Getting rid of them for good takes two things: removing the ones inside, and sealing the gaps that let them in. We do both.",
        "treats": ["Roof rats & house mice", "Attic & wall-void activity", "Droppings & gnaw marks", "Entry-point sealing (exclusion)"],
        "sections": [
            ("Removal and exclusion together", "<p>Trapping alone is a treadmill — new rodents simply follow the same trails inside. Our rodent work pairs removal with <strong>exclusion</strong>: we find and seal the entry points around rooflines, pipes, weep holes and the garage, so the problem ends instead of repeating.</p>"),
            ("Protecting the rest of the house", "<p>Rodents rarely travel alone, and they bring other pests with them. Where it helps, we pair rodent work with a <a href=\"/services/pest-control.html\">general pest treatment</a> and check for the wildlife that uses the same gaps — see <a href=\"/services/wildlife-removal.html\">wildlife removal</a>.</p>"),
        ],
        "related": ["wildlife-removal", "pest-control", "scorpion-control"],
    },
    {
        "slug": "wildlife-removal", "nav": "Wildlife Removal", "icon": "🦝",
        "h1": "Humane Wildlife Removal in Central Texas",
        "title": "Wildlife Removal in Buda & Central Texas | Raccoons, Squirrels",
        "desc": "Humane live trapping and removal of raccoons, squirrels and opossums from attics and yards, with entry points sealed. Serving Buda & Central Texas since 1998.",
        "lead": "Raccoons in the attic, squirrels in the soffit, opossums under the deck — Central Texas wildlife treats homes like the hollow trees they replaced. We remove them humanely with live trapping and close off the damage so they cannot move back in.",
        "treats": ["Raccoons", "Squirrels", "Opossums", "Attic, soffit & deck intrusions"],
        "sections": [
            ("Live trapping, done right", "<p>We use humane live-trapping and hands-on removal, then repair and seal the entry points — the vent, gable, or roofline gap that let the animal in. Without that last step, the next animal simply finds the same open door.</p>"),
            ("Acreage and Hill Country lots", "<p>On the larger lots around Driftwood, Dripping Springs and Wimberley, wildlife pressure is constant. We know the local species and the ways they get into a home out here, and we treat the property, not just the symptom.</p>"),
        ],
        "related": ["rodent-control", "pest-control", "mosquito-misting"],
    },
    {
        "slug": "mosquito-misting", "nav": "Mosquito Misting Systems", "icon": "🦟",
        "h1": "Mosquito Control & Misting Systems",
        "title": "Mosquito Control & Misting Systems in Central Texas | Excel Pest",
        "desc": "Take back the backyard — mosquito control and automated misting systems for Central Texas homes. Water-based, family-focused. Call (737) 201-3059.",
        "lead": "Central Texas humidity and standing water turn a backyard into a mosquito nursery from spring through the first cold snap. We control the mosquitoes you have and install misting systems that keep the yard usable all season.",
        "treats": ["Backyard & patio mosquitoes", "Standing-water breeding sites", "Automated misting systems", "Seasonal recurring control"],
        "sections": [
            ("Treat the source, not just the swarm", "<p>Lasting mosquito control starts with the breeding sites — the low spots, drains, and containers that hold water after our heavy Hill Country rains. We treat harborage and, where you want hands-off protection, install a misting system tuned to your landscaping.</p>"),
            ("Made for how Texans live outside", "<p>Patios, pools and outdoor kitchens are the whole point of a Central Texas yard. A misting system runs on a schedule you control, so the space is ready when you are — without you thinking about it.</p>"),
        ],
        "related": ["pest-control", "lawn-pest-control", "wildlife-removal"],
    },
    {
        "slug": "lawn-pest-control", "nav": "Lawn Pest Control", "icon": "🌱",
        "h1": "Lawn Pest, Weed & Disease Control",
        "title": "Lawn Pest Control in Buda & Central Texas | Grubs, Chinch Bugs",
        "desc": "Grubs, chinch bugs and armyworms plus weed and disease control for Central Texas lawns — St. Augustine and Bermuda. Call (737) 201-3059 for a free estimate.",
        "lead": "A brown patch that spreads in the July heat usually is not just the drought — it is chinch bugs, grubs, or armyworms working under the surface. We treat the pests and the weeds and disease that damage Central Texas turf, so the lawn recovers and holds.",
        "treats": ["Chinch bugs", "White grubs", "Armyworms", "Weeds & turf disease (brown patch)"],
        "sections": [
            ("Know what is actually killing the grass", "<p>St. Augustine and Bermuda each fail in their own way here, and the fix depends on the cause. Chinch bugs cook a lawn in full sun; grubs loosen it from below; brown patch spreads in humidity. We diagnose it first, then treat the right problem.</p>"),
            ("Full landscaping and turf renovation", "<p>Excel Pest handles the pests, weeds and disease that damage a lawn. For design, installation, sod, and hardscape, our sister company <a href=\"" + BIZ["sister_url"] + "\" rel=\"noopener\">Research Turf Management</a> handles the build side — many of our customers use both.</p>"),
        ],
        "related": ["pest-control", "mosquito-misting", "scorpion-control"],
    },
]
SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# --------------------------------------------------------------------------
# Priority-corridor city pages
# --------------------------------------------------------------------------
LOCATIONS = [
    {
        "slug": "buda", "city": "Buda", "county": "Hays County",
        "lead": "Buda is home base. Our office and crews work out of 175 Warehouse Drive, and we have treated homes here since long before the subdivisions filled in. As Buda has grown from a small Hays County town into one of the fastest-growing suburbs in Texas, the pest pressure has grown with it.",
        "angle": "New construction on old ranch land pushes scorpions, ants and rodents straight into fresh neighborhoods, while the older homes near downtown and Plum Creek have their own established pest trails. We know both, because this is where we live and work.",
        "nearby": ["kyle", "manchaca", "san-marcos"],
    },
    {
        "slug": "kyle", "city": "Kyle", "county": "Hays County",
        "lead": "Kyle has exploded from a quiet stop on I-35 into one of Central Texas's fastest-growing cities — and rapid new construction is a magnet for pests. Freshly cleared lots displace scorpions, ants and rodents into brand-new homes before the landscaping is even in.",
        "angle": "We treat both the new Plum Creek and Kensington-era subdivisions and the older homes around downtown Kyle, timing recurring service to the local calendar so families are covered through scorpion season and the fall move-indoors.",
        "nearby": ["buda", "san-marcos", "manchaca"],
    },
    {
        "slug": "san-marcos", "city": "San Marcos", "county": "Hays County",
        "lead": "San Marcos pairs a spring-fed river and a major university with heat and humidity — a combination that keeps mosquitoes, roaches and rodents busy. Rental turnover near Texas State and riverside humidity make consistent pest control essential here.",
        "angle": "From family homes on the hills to rentals near the square and the river, we handle the roaches and mosquitoes the humidity feeds, the rodents that follow, and the scorpions that come with the surrounding limestone country.",
        "nearby": ["kyle", "wimberley", "buda"],
    },
    {
        "slug": "dripping-springs", "city": "Dripping Springs", "county": "Hays County",
        "lead": "Dripping Springs is Hill Country proper — limestone, cedar, wells and septic, and homes on acreage well outside town. It is scorpion country, and the rock and brush that make it beautiful also make it a haven for pests and wildlife.",
        "angle": "Out here, exclusion matters more than anywhere. We treat the perimeter, rock walls and wood piles that harbor scorpions, seal the gaps in pier-and-beam and slab foundations, and handle the wildlife that treats a Hill Country home like a hollow tree.",
        "nearby": ["driftwood", "wimberley", "buda"],
    },
    {
        "slug": "wimberley", "city": "Wimberley", "county": "Hays County",
        "lead": "Wimberley sits in the cedar and limestone between the Blanco River and Cypress Creek, full of vacation homes, weekend cabins and full-time Hill Country living. Scorpions and wildlife are simply part of the territory.",
        "angle": "Second homes that sit empty invite rodents and wildlife; riverside lots draw mosquitoes and scorpions. We treat and seal so the home stays protected whether you are there every day or every other weekend.",
        "nearby": ["dripping-springs", "driftwood", "san-marcos"],
    },
    {
        "slug": "driftwood", "city": "Driftwood", "county": "Hays County",
        "lead": "Driftwood is rural Hill Country — acreage, ranchettes, and homes tucked into the cedar off winding county roads. With that much open land around every house, pest and wildlife pressure never really lets up.",
        "angle": "Larger lots mean more perimeter to defend and more wildlife on the move. We build treatments around the whole property — outbuildings, wood piles and foundation alike — to keep scorpions, rodents and wildlife out of the house.",
        "nearby": ["dripping-springs", "wimberley", "buda"],
    },
    {
        "slug": "manchaca", "city": "Manchaca", "county": "Travis County",
        "lead": "Manchaca (Menchaca) sits on the southern edge of Austin in Travis County, a mix of established homes on big lots and newer infill. It is close enough to our Buda office that it has always been core to our service area.",
        "angle": "Mature trees and older foundations give ants, roaches and rodents plenty of ways in, while nearby greenbelt and creek land keeps wildlife and mosquitoes in the picture. We treat the full range, timed to the Central Texas seasons.",
        "nearby": ["buda", "del-valle", "kyle"],
    },
    {
        "slug": "del-valle", "city": "Del Valle", "county": "Travis County",
        "lead": "Del Valle spreads across southeastern Travis County near the airport — rural stretches, established homes and fast new development side by side. Open land and quick growth keep pests and rodents on the move here.",
        "angle": "New builds on former farmland push rodents, ants and scorpions into fresh neighborhoods, while the rural lots bring their own wildlife pressure. We cover both from our nearby Buda base, with recurring plans built for the local calendar.",
        "nearby": ["manchaca", "buda", "kyle"],
    },
]
LOCATION_BY_SLUG = {l["slug"]: l for l in LOCATIONS}
PRIORITY_CITY_SLUG = {l["city"]: l["slug"] for l in LOCATIONS}

# --------------------------------------------------------------------------
# HTML building blocks
# --------------------------------------------------------------------------

def head(title, desc, canonical, schema_blocks, noindex=False, og_type="website"):
    robots = '\n  <meta name="robots" content="noindex, nofollow">' if noindex else ""
    parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        '  <title>' + html.escape(title) + '</title>',
        '  <meta name="description" content="' + html.escape(desc) + '">',
        '  <link rel="canonical" href="' + canonical + '">' + robots,
        '  <meta property="og:type" content="' + og_type + '">',
        '  <meta property="og:site_name" content="' + html.escape(BIZ["name"]) + '">',
        '  <meta property="og:title" content="' + html.escape(title) + '">',
        '  <meta property="og:description" content="' + html.escape(desc) + '">',
        '  <meta property="og:url" content="' + canonical + '">',
        '  <meta name="twitter:card" content="summary">',
        '  <link rel="stylesheet" href="/css/styles.css">',
        '  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">',
    ]
    for block in schema_blocks:
        parts.append('  <script type="application/ld+json">')
        parts.append(json.dumps(block, indent=2))
        parts.append('  </script>')
    parts.append('</head>')
    return "\n".join(parts)


def header():
    links = "\n".join(
        '        <li><a href="%s">%s</a></li>' % (url, html.escape(label))
        for label, url in NAV
    )
    return """<body>
  <header class="site-header">
    <div class="topbar"><div class="container">
      <span>Family-owned in Buda since {founded} · Licensed &amp; insured · {license}</span>
      <span>Call <a href="tel:{ptel}">{phone}</a> · Text <a href="sms:{ttel}">{text}</a></span>
    </div></div>
    <nav class="navbar" aria-label="Primary"><div class="container">
      <a class="brand" href="/">
        <span class="brand__name">{name}</span>
        <span class="brand__tag">Pest · Rodent · Wildlife · Lawn · Since {founded}</span>
      </a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
      <ul class="nav-links">
{links}
        <li class="nav-cta">
          <a class="nav-invoice" href="/pay-invoice.html">Pay Invoice</a>
          <a class="btn btn--primary" href="/contact.html">Free Estimate</a>
        </li>
      </ul>
    </div></nav>
  </header>""".format(
        founded=BIZ["founded"], license=BIZ["license"], ptel=BIZ["phone_tel"],
        phone=BIZ["phone"], ttel=BIZ["text_tel"], text=BIZ["text"],
        name=html.escape(BIZ["name"]), links=links,
    )


def cta_band(heading="Seeing something you shouldn't?", sub="Get a free estimate today — no obligation."):
    return """
  <section class="cta-band">
    <div class="container">
      <div><h2 class="mb-0">{h}</h2><p class="mb-0">{s}</p></div>
      <div class="hero__actions" style="margin:0;">
        <a class="btn btn--ghost" href="tel:{ptel}">Call {phone}</a>
        <a class="btn btn--ghost" href="/contact.html">Request Online</a>
      </div>
    </div>
  </section>""".format(h=html.escape(heading), s=html.escape(sub), ptel=BIZ["phone_tel"], phone=BIZ["phone"])


def footer():
    svc_links = "\n".join(
        '            <li><a href="/services/%s.html">%s</a></li>' % (s["slug"], html.escape(s["nav"]))
        for s in SERVICES
    )
    return """
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h4>{name}</h4>
          <p>Family-owned pest, rodent, wildlife and lawn-pest control for Central Texas since {founded}.</p>
          <p class="mb-0">{street}<br>{city}, {state} {zip}<br>Licensed &amp; insured · {license}</p>
          <p style="margin-top:12px;">
            <a href="{bbb}" rel="noopener">BBB A+</a> ·
            <a href="{yelp}" rel="noopener">Yelp</a> ·
            <a href="{facebook}" rel="noopener">Facebook</a> ·
            <a href="{youtube}" rel="noopener">YouTube</a>
          </p>
        </div>
        <div><h4>Services</h4><ul class="footer-links">
{svc_links}
        </ul></div>
        <div><h4>Company</h4><ul class="footer-links">
          <li><a href="/about.html">About</a></li>
          <li><a href="/reviews.html">Reviews</a></li>
          <li><a href="/offers.html">Offers &amp; Discounts</a></li>
          <li><a href="/pet-family-safety.html">Pet &amp; Family Safety</a></li>
          <li><a href="/faq.html">FAQ</a></li>
          <li><a href="/service-area.html">Service Area</a></li>
          <li><a href="/pay-invoice.html">Pay Invoice</a></li>
        </ul></div>
        <div><h4>Get in touch</h4><ul class="footer-links">
          <li>Call: <a href="tel:{ptel}">{phone}</a></li>
          <li>Text: <a href="sms:{ttel}">{text}</a></li>
          <li>Email: <a href="mailto:{email}">{email}</a></li>
          <li>Hours: Mon–Fri 8–5</li>
          <li>Landscaping? <a href="{sister_url}" rel="noopener">{sister_name}</a></li>
        </ul></div>
      </div>
      <div class="footer-bottom">
        <span>© <span data-year>2026</span> {name}. All rights reserved.</span>
        <span>excelpest-lawncontrol.com</span>
      </div>
    </div>
  </footer>
  <script src="/js/main.js"></script>
</body>
</html>""".format(
        name=html.escape(BIZ["name"]), founded=BIZ["founded"], street=html.escape(BIZ["street"]),
        city=BIZ["city"], state=BIZ["state"], zip=BIZ["zip"], license=BIZ["license"],
        bbb=BIZ["bbb"], yelp=BIZ["yelp"], facebook=BIZ["facebook"], youtube=BIZ["youtube"],
        svc_links=svc_links, ptel=BIZ["phone_tel"], phone=BIZ["phone"], ttel=BIZ["text_tel"],
        text=BIZ["text"], email=BIZ["email"], sister_url=BIZ["sister_url"], sister_name=BIZ["sister_name"],
    )


def page_hero(title, subtitle, crumbs):
    trail = ' / '.join(
        ('<a href="%s">%s</a>' % (u, html.escape(t))) if u else html.escape(t)
        for t, u in crumbs
    )
    return """
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb">{trail}</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
  </section>""".format(trail=trail, title=html.escape(title), subtitle=html.escape(subtitle))


def crosslink_block():
    return """
      <div class="crosslink">
        <span class="eyebrow">Need landscaping, not pest control?</span>
        <p class="mb-0"><strong>{sister}</strong> is our sister company for landscape design, lawn care,
           hardscape and turf across the same Central Texas service area.
           <a href="{url}" rel="noopener">Visit {sister} →</a></p>
      </div>""".format(sister=BIZ["sister_name"], url=BIZ["sister_url"])


# ---------- Schema builders ----------

def business_schema(with_rating=True, with_reviews=False):
    node = {
        "@context": "https://schema.org",
        "@type": "PestControlService",
        "@id": BIZ["domain"] + "/#business",
        "name": BIZ["name"],
        "legalName": BIZ["legal"],
        "url": BIZ["domain"] + "/",
        "telephone": BIZ["phone_tel"],
        "email": BIZ["email"],
        "foundingDate": BIZ["founded"],
        "founder": {"@type": "Person", "name": BIZ["owner"]},
        "image": BIZ["domain"] + "/assets/favicon.svg",
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BIZ["street"],
            "addressLocality": BIZ["city"],
            "addressRegion": BIZ["state"],
            "postalCode": BIZ["zip"],
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "08:00", "closes": "17:00",
        }],
        "areaServed": [{"@type": "City", "name": c} for c in ALL_CITIES],
        "sameAs": [BIZ["bbb"], BIZ["yelp"], BIZ["facebook"], BIZ["youtube"], BIZ["sister_url"]],
    }
    if with_rating:
        node["aggregateRating"] = {
            "@type": "AggregateRating", "ratingValue": BIZ["rating"],
            "reviewCount": BIZ["reviews"], "bestRating": "5",
        }
    if with_reviews:
        node["review"] = [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": "Karla Mathews"},
                "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                "reviewBody": "Been with this company for 30+ years.",
            },
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": "Judy Buck"},
                "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                "reviewBody": "We have used Excel Pest / Research Turf Mgmt for the past 13+ years — pergola, extending patio, masonry work, tree trimming, plus regular lawn care.",
            },
        ]
    return node


def breadcrumb_schema(crumbs):
    items = []
    for i, (name, url) in enumerate(crumbs, start=1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if url:
            item["item"] = BIZ["domain"] + url
        items.append(item)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def service_schema(s):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": s["nav"],
        "name": s["h1"],
        "url": BIZ["domain"] + "/services/" + s["slug"] + ".html",
        "provider": {"@type": "PestControlService", "@id": BIZ["domain"] + "/#business", "name": BIZ["name"]},
        "areaServed": [{"@type": "City", "name": c} for c in ALL_CITIES],
    }


# --------------------------------------------------------------------------
# Page renderers
# --------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def assemble(title, desc, canonical, body, schema_blocks, noindex=False):
    return head(title, desc, canonical, schema_blocks, noindex) + "\n" + header() + "\n" + body + footer() + "\n"


def related_services_grid(slugs, heading="Related services"):
    cards = []
    for slug in slugs:
        s = SERVICE_BY_SLUG[slug]
        cards.append("""        <article class="card card--link">
          <div class="card__icon">{icon}</div>
          <h3>{name}</h3>
          <a class="card__link" href="/services/{slug}.html">Learn more →</a>
        </article>""".format(icon=s["icon"], name=html.escape(s["nav"]), slug=slug))
    return """
  <section class="section section--soft">
    <div class="container">
      <h2>{heading}</h2>
      <div class="grid grid--3">
{cards}
      </div>
    </div>
  </section>""".format(heading=html.escape(heading), cards="\n".join(cards))


def render_service(s):
    canonical = BIZ["domain"] + "/services/" + s["slug"] + ".html"
    crumbs = [("Home", "/"), ("Services", "/services.html"), (s["nav"], None)]
    treats = "".join("<li>%s</li>" % html.escape(t) for t in s["treats"])
    sections = "".join(
        "<h2>%s</h2>%s" % (html.escape(h), body) for h, body in s["sections"]
    )
    body = page_hero(s["h1"], s["desc"].split(". ")[0] + ".", crumbs) + """
  <section class="section">
    <div class="container split">
      <div class="prose">
        <p class="lead">{lead}</p>
        {sections}
        <div class="callout">
          <strong>Safe for your family and pets.</strong> Our products are water-based and chosen with
          family and four-legged family members in mind — see <a href="/pet-family-safety.html">pet &amp; family safety</a>.
        </div>
        <div class="hero__actions">
          <a class="btn btn--primary" href="/contact.html">Get My Free Estimate</a>
          <a class="btn btn--outline" href="tel:{ptel}">Call {phone}</a>
        </div>
      </div>
      <div>
        <div class="card">
          <h3 class="mt-0">What we handle</h3>
          <ul class="info-list" style="margin:0 0 14px;"><li><span class="value" style="font-weight:600;font-size:1rem;">Common issues we treat:</span></li></ul>
          <ul class="prose" style="margin:0;">{treats}</ul>
          <hr style="border:0;border-top:1px solid var(--line);margin:18px 0;">
          <p style="margin:0;"><strong>Serving:</strong> Buda, Kyle, San Marcos, Dripping Springs, Wimberley and
             <a href="/service-area.html">all of Central Texas</a>.</p>
        </div>
        <div class="offer-strip" style="margin-top:18px;">
          <div><h3>Heroes save 10%</h3><p class="mb-0" style="color:#cdd6e6;">Military, veterans, first responders, nurses &amp; teachers.</p></div>
          <a class="btn btn--primary" href="/offers.html">See offer</a>
        </div>
      </div>
    </div>
  </section>""".format(
        lead=s["lead"], sections=sections, treats=treats, ptel=BIZ["phone_tel"], phone=BIZ["phone"],
    )
    body += related_services_grid(s["related"])
    body += cta_band()
    schema = [business_schema(), service_schema(s), breadcrumb_schema(crumbs)]
    return assemble(s["title"], s["desc"], canonical, body, schema)


def render_location(l):
    canonical = BIZ["domain"] + "/locations/" + l["slug"] + ".html"
    crumbs = [("Home", "/"), ("Service Area", "/service-area.html"), (l["city"], None)]
    title = "Pest Control in %s, TX | Excel Pest since %s" % (l["city"], BIZ["founded"])
    desc = "Family-owned pest, rodent, scorpion and lawn-pest control in %s, %s. Trusted across Central Texas since %s. Free estimates — call %s." % (
        l["city"], l["county"], BIZ["founded"], BIZ["phone"])
    svc_cards = "".join(
        """        <article class="card card--link">
          <div class="card__icon">{icon}</div>
          <h3>{name}</h3>
          <a class="card__link" href="/services/{slug}.html">Learn more →</a>
        </article>""".format(icon=s["icon"], name=html.escape(s["nav"]), slug=s["slug"])
        for s in SERVICES
    )
    nearby = "".join(
        '<li><a href="/locations/%s.html">Pest control in %s</a></li>' % (n, html.escape(LOCATION_BY_SLUG[n]["city"]))
        for n in l["nearby"]
    )
    body = page_hero("Pest Control in " + l["city"] + ", Texas", l["county"] + " · Family-owned since " + BIZ["founded"], crumbs) + """
  <section class="section">
    <div class="container split">
      <div class="prose">
        <p class="lead">{lead}</p>
        <p>{angle}</p>
        <h2>Local pest control, done by people who live here</h2>
        <p>{city} sits inside our core Central Texas service area, and we have worked it since {founded}. That
           is the difference between us and the regional franchises: a 5.0-star, family-owned crew that Buda and
           the surrounding towns have trusted for more than 25 years — not a call center. Our office manager
           {mgr} and our technicians are the same familiar faces on every visit.</p>
        <div class="callout">
          <strong>The crew {city} can call by name.</strong> Licensed &amp; insured ({license}), water-based
          products that are safe for family and pets, free estimates, and a workmanship warranty on our work.
        </div>
        <div class="hero__actions">
          <a class="btn btn--primary" href="/contact.html">Get My Free Estimate</a>
          <a class="btn btn--outline" href="tel:{ptel}">Call {phone}</a>
        </div>
      </div>
      <div>
        <div class="card">
          <h3 class="mt-0">Nearby areas we serve</h3>
          <ul class="footer-links" style="list-style:none;padding:0;margin:0 0 14px;">{nearby}</ul>
          <a href="/service-area.html">See all 27 cities →</a>
          <hr style="border:0;border-top:1px solid var(--line);margin:18px 0;">
          <p style="margin:0;"><strong>Landscaping in {city}?</strong> Our sister company
             <a href="{sister_url}" rel="noopener">{sister}</a> covers design, sod and hardscape.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <h2>Pest services we provide in {city}</h2>
      <div class="grid grid--4">
{svc_cards}
      </div>
    </div>
  </section>""".format(
        lead=l["lead"], angle=l["angle"], city=l["city"], founded=BIZ["founded"], mgr=BIZ["office_mgr"],
        license=BIZ["license"], ptel=BIZ["phone_tel"], phone=BIZ["phone"], nearby=nearby,
        sister_url=BIZ["sister_url"], sister=BIZ["sister_name"], svc_cards=svc_cards,
    )
    body += cta_band(heading="Pest problem in " + l["city"] + "?", sub="Talk to the crew that has served the area since " + BIZ["founded"] + ".")
    # Location "Service" schema scoped to the city
    loc_service = {
        "@context": "https://schema.org", "@type": "Service", "serviceType": "Pest Control",
        "name": "Pest Control in " + l["city"] + ", TX",
        "url": canonical,
        "provider": {"@type": "PestControlService", "@id": BIZ["domain"] + "/#business", "name": BIZ["name"]},
        "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"]}},
    }
    schema = [business_schema(), loc_service, breadcrumb_schema(crumbs)]
    return assemble(title, desc, canonical, body, schema)


# --------------------------------------------------------------------------
# Core pages
# --------------------------------------------------------------------------

def services_hub():
    canonical = BIZ["domain"] + "/services.html"
    crumbs = [("Home", "/"), ("Services", None)]
    cards = "".join("""        <article class="card card--link">
          <div class="card__icon">{icon}</div>
          <h3>{name}</h3>
          <p>{blurb}</p>
          <a class="card__link" href="/services/{slug}.html">Learn more →</a>
        </article>""".format(icon=s["icon"], name=html.escape(s["nav"]), slug=s["slug"],
                             blurb=html.escape(s["lead"].split(". ")[0] + "."))
        for s in SERVICES)
    body = page_hero("Our Services", "One local crew for pests, rodents, wildlife and lawn insects across Central Texas.", crumbs) + """
  <section class="section">
    <div class="container">
      <div class="grid grid--3">
{cards}
      </div>
      <div style="margin-top:28px;">{cross}</div>
    </div>
  </section>""".format(cards=cards, cross=crosslink_block())
    body += cta_band()
    schema = [business_schema(), breadcrumb_schema(crumbs)]
    desc = "Pest control, scorpion, termite, rodent, wildlife, mosquito and lawn-pest control across Buda and Central Texas. Family-owned since 1998. Call (737) 201-3059."
    return assemble("Pest Control Services in Buda & Central Texas | Excel Pest", desc, canonical, body, schema)


def service_area_hub():
    canonical = BIZ["domain"] + "/service-area.html"
    crumbs = [("Home", "/"), ("Service Area", None)]
    items = []
    for c in ALL_CITIES:
        if c in PRIORITY_CITY_SLUG:
            items.append('<li><a href="/locations/%s.html">%s</a></li>' % (PRIORITY_CITY_SLUG[c], html.escape(c)))
        else:
            items.append('<li><span>%s</span></li>' % html.escape(c))
    grid = "\n        ".join(items)
    body = page_hero("Service Area — 27 Central Texas Cities", "From South Austin through Hays County and into the Hill Country.", crumbs) + """
  <section class="section">
    <div class="container">
      <p class="lead">Our core corridor runs Buda–Kyle–Plum Creek–Dripping Springs–Wimberley–South Austin, and
         our full service area stretches west into the Hill Country and south to San Marcos. We have covered this
         ground since {founded}.</p>
      <ul class="city-grid">
        {grid}
      </ul>
      <p style="margin-top:16px;color:var(--muted);">Cities shown as links have a dedicated page. Not sure if we
         reach you? <a href="/contact.html">Ask us</a> — if you are in or near {county}, we probably do.</p>
    </div>
  </section>""".format(founded=BIZ["founded"], grid=grid, county="Hays County")
    body += cta_band()
    schema = [business_schema(), breadcrumb_schema(crumbs)]
    desc = "Excel Pest serves 27 Central Texas cities — Buda, Kyle, San Marcos, Dripping Springs, Wimberley and more. Family-owned since 1998. Call (737) 201-3059."
    return assemble("Service Area — Pest Control Across Central Texas | Excel Pest", desc, canonical, body, schema)


def home():
    canonical = BIZ["domain"] + "/"
    svc_cards = "".join("""        <article class="card card--link">
          <div class="card__icon">{icon}</div>
          <h3>{name}</h3>
          <p>{blurb}</p>
          <a class="card__link" href="/services/{slug}.html">Learn more →</a>
        </article>""".format(icon=s["icon"], name=html.escape(s["nav"]), slug=s["slug"],
                             blurb=html.escape(s["lead"].split(". ")[0] + "."))
        for s in SERVICES)
    city_links = " · ".join('<a href="/locations/%s.html">%s</a>' % (l["slug"], html.escape(l["city"])) for l in LOCATIONS)
    body = """
  <section class="hero">
    <div class="container">
      <span class="eyebrow">The crew Buda has trusted since {founded}</span>
      <h1>Family-owned pest control for Central Texas.</h1>
      <p>Pest, rodent, wildlife and lawn-pest control done by the same local crew since {founded} —
         with water-based products chosen for your family and your four-legged family members.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="/contact.html">Get My Free Estimate</a>
        <a class="btn btn--ghost" href="tel:{ptel}">Call {phone}</a>
      </div>
      <div class="badges">
        <span class="badge">★ {rating} rating · {reviews} Google reviews</span>
        <span class="badge">BBB A+ · accredited 2007</span>
        <span class="badge">Licensed &amp; insured · {license}</span>
      </div>
    </div>
  </section>

  <section class="trust-bar"><div class="container">
    <span><span class="star">★★★★★</span> <b>{rating}</b> from {reviews} reviews</span>
    <span><b>Since {founded}</b> · family-owned in Buda</span>
    <span><b>BBB A+</b> accredited</span>
    <span><b>{license}</b> · licensed &amp; insured</span>
  </div></section>

  <section class="section">
    <div class="container">
      <div class="text-center" style="max-width:680px;margin:0 auto 40px;">
        <span class="eyebrow">What we do</span>
        <h2>Everything crawling, gnawing, or buzzing — handled</h2>
        <p class="lead">One local company for the pests inside your walls, the rodents in your attic, the
           wildlife under your deck, and the insects tearing up your lawn.</p>
      </div>
      <div class="grid grid--4">
{svc_cards}
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container split">
      <div>
        <span class="eyebrow">28 years, one owner, named technicians</span>
        <h2>Not a franchise. The crew that actually knows Central Texas.</h2>
        <p>{owner} started Excel Pest in South Austin in {founded} and has run it ever since. We know the local
           pest calendar — when scorpions move indoors, when chinch bugs cook a lawn, when rodents look for a warm
           attic — because we have worked this ground for more than 25 years. Nobody in this market beats our
           5.0 rating; we just do it quietly, one neighbor at a time.</p>
        <ul class="info-list">
          <li><span class="value">✓ &nbsp;Family-owned &amp; locally operated since {founded}</span></li>
          <li><span class="value">✓ &nbsp;Water-based products, safe for family &amp; pets</span></li>
          <li><span class="value">✓ &nbsp;Free estimates · warranties · emergency service</span></li>
        </ul>
        <a class="btn btn--outline" href="/about.html">Read our story</a>
      </div>
      <div>
        <div class="review-card">
          <div class="stars">★★★★★</div>
          <blockquote>"Been with this company for 30+ years."</blockquote>
          <cite>Karla Mathews</cite><div class="meta">Google review · 2026</div>
          <hr style="border:0;border-top:1px solid var(--line);margin:18px 0;">
          <div class="stars">★★★★★</div>
          <blockquote>"We have used Excel Pest / Research Turf for 13+ years — pergola, patio, masonry, tree
             trimming, plus regular lawn care."</blockquote>
          <cite>Judy Buck</cite><div class="meta">Google review · 2026</div>
          <a class="card__link" href="/reviews.html" style="display:inline-block;margin-top:14px;">Read more reviews →</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="offer-strip">
        <div>
          <span class="pct">10% off</span>
          <h3>Military, veterans, first responders, nurses &amp; teachers</h3>
          <p class="mb-0" style="color:#cdd6e6;">Our thanks to the people who serve Central Texas. Mention it when you schedule.</p>
        </div>
        <a class="btn btn--primary" href="/offers.html">See details</a>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container text-center">
      <span class="eyebrow">Local coverage</span>
      <h2>Serving 27 Central Texas cities</h2>
      <p class="lead" style="max-width:720px;margin:0 auto 18px;">From South Austin through Hays County and into
         the Hill Country. Dedicated local pages for:</p>
      <p style="font-size:1.05rem;">{city_links}</p>
      <a class="btn btn--outline" href="/service-area.html">See the full service area →</a>
    </div>
  </section>

  <section class="section">
    <div class="container">{cross}</div>
  </section>""".format(
        founded=BIZ["founded"], ptel=BIZ["phone_tel"], phone=BIZ["phone"], rating=BIZ["rating"],
        reviews=BIZ["reviews"], license=BIZ["license"], svc_cards=svc_cards, owner=BIZ["owner"],
        city_links=city_links, cross=crosslink_block(),
    )
    desc = "Family-owned pest, rodent, wildlife and lawn-pest control in Buda and Central Texas since 1998. 5.0-star, BBB A+, licensed. Free estimates — call (737) 201-3059."
    schema = [business_schema(with_rating=True), {
        "@context": "https://schema.org", "@type": "WebSite", "name": BIZ["name"],
        "url": BIZ["domain"] + "/",
    }]
    return assemble("Austin Excel Pest & Lawn Control — Central Texas Pest Control Since 1998",
                    desc, canonical, body, schema)


def about():
    canonical = BIZ["domain"] + "/about.html"
    crumbs = [("Home", "/"), ("About", None)]
    body = page_hero("About Austin Excel Pest & Lawn Control", "Family-owned in Buda since 1998 — and still run by the same owner.", crumbs) + """
  <section class="section">
    <div class="container split">
      <div class="prose">
        <span class="eyebrow">Our story</span>
        <h2>A local company, started by a local.</h2>
        <p>{owner} is an Austin native. He grew up near Lake Travis, went to Leander High School, then Austin
           Community College and Southwestern University in Georgetown — and he has spent his life in Central
           Texas. That matters in this work: he knows Central Texas soil, Central Texas bugs, and Central Texas
           drought.</p>
        <p>In {founded} he opened <strong>Excel Pest &amp; Lawn Control</strong> in South Austin, pest control
           first with lawn work alongside it. In 2007 the landscaping side grew into its own brand,
           <a href="{sister_url}" rel="noopener">Research Turf Management</a> — the same year the business earned
           its BBB accreditation. Today both brands run from one warehouse at {street} in {city}, with a shared
           office and shared crews. Plenty of customers use both.</p>
        <h2>Family, in the literal sense</h2>
        <p>Both brands describe themselves as family-owned and locally operated, and they mean it —
           {owner} is married with three daughters. His philosophy is the throughline of everything we do: he
           treats <em>every home as if it were his own, and every customer — and their four-legged family
           members — like neighbors.</em> That is why our products are water-based and chosen with pets and kids
           in mind.</p>
        <div class="callout">
          <strong>The people you'll deal with.</strong> {mgr}, our Director of Office Operations, runs the office
          for both brands — customers name-check her in their reviews — and our technicians are the same familiar
          faces on every visit.
        </div>
        <p>Twenty-eight years in, we hold a 5.0 rating across {reviews} Google reviews and an A+ from the BBB.
           We are licensed and insured in Texas ({license}). We are proud of it — and we would rather earn your
           trust one visit at a time than act like a franchise that just moved to town.</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="/contact.html">Get a free estimate</a>
          <a class="btn btn--outline" href="/reviews.html">Read our reviews</a>
        </div>
      </div>
      <div>
        <div class="card">
          <h3 class="mt-0">At a glance</h3>
          <ul class="info-list mt-0">
            <li><span class="label">Founded</span><span class="value">{founded}, South Austin</span></li>
            <li><span class="label">Owner</span><span class="value">{owner}</span></li>
            <li><span class="label">Based in</span><span class="value">{city}, Texas</span></li>
            <li><span class="label">License</span><span class="value">{license}</span></li>
            <li><span class="label">Rating</span><span class="value">★ {rating} · {reviews} reviews</span></li>
            <li><span class="label">BBB</span><span class="value">A+ · accredited 2007</span></li>
          </ul>
          <a class="btn btn--primary" href="/contact.html">Contact us</a>
        </div>
      </div>
    </div>
  </section>""".format(
        owner=BIZ["owner"], founded=BIZ["founded"], sister_url=BIZ["sister_url"], street=BIZ["street"],
        city=BIZ["city"], mgr=BIZ["office_mgr"], reviews=BIZ["reviews"], license=BIZ["license"],
        rating=BIZ["rating"],
    )
    body += cta_band()
    desc = "Family-owned in Buda since 1998, still run by owner Gye Hutson. 5.0-star, BBB A+, licensed Texas pest control (TPCL 0786979). Read the Excel Pest story."
    schema = [business_schema(), breadcrumb_schema(crumbs), {
        "@context": "https://schema.org", "@type": "AboutPage", "url": canonical, "name": "About Excel Pest",
    }]
    return assemble("About — Family-Owned in Buda Since 1998 | Excel Pest", desc, canonical, body, schema)


def reviews():
    canonical = BIZ["domain"] + "/reviews.html"
    crumbs = [("Home", "/"), ("Reviews", None)]
    body = page_hero("Reviews", "A 5.0 rating built one Central Texas neighbor at a time.", crumbs) + """
  <section class="section">
    <div class="container">
      <div class="big-rating" style="margin-bottom:30px;">
        <span class="num">{rating}</span>
        <div>
          <div class="stars">★★★★★</div>
          <p class="mb-0"><strong>{reviews} Google reviews</strong> · BBB A+ accredited since 2007</p>
        </div>
      </div>
      <div class="grid grid--2">
        <div class="review-card">
          <div class="stars">★★★★★</div>
          <blockquote>"Been with this company for 30+ years."</blockquote>
          <cite>Karla Mathews</cite>
          <div class="meta">Google review · 2026 · names Megan in the office, Tim the technician, and Gye by name</div>
        </div>
        <div class="review-card">
          <div class="stars">★★★★★</div>
          <blockquote>"We have used Excel Pest / Research Turf Mgmt for the past 13+ years… pergola, extending
             patio, masonry work on front porch and flower beds, tree trimming, plus regular lawn care."</blockquote>
          <cite>Judy Buck</cite>
          <div class="meta">Google review · 2026</div>
        </div>
      </div>
      <div class="callout" style="margin-top:26px;">
        <strong>Why this matters.</strong> Customers do not experience us as two companies — they hire Gye's
        crew and get pest, turf and hardscape work from the same trusted people. That is exactly how we like it.
      </div>
      <div class="hero__actions">
        <a class="btn btn--primary" href="{bbb}" rel="noopener">See our BBB profile</a>
        <a class="btn btn--outline" href="{yelp}" rel="noopener">Read us on Yelp</a>
      </div>
    </div>
  </section>""".format(rating=BIZ["rating"], reviews=BIZ["reviews"], bbb=BIZ["bbb"], yelp=BIZ["yelp"])
    body += cta_band()
    desc = "Excel Pest holds a 5.0 rating across 41 Google reviews and a BBB A+ — some customers for 13 and 30+ years. Read reviews of our Central Texas pest control."
    schema = [business_schema(with_rating=True, with_reviews=True), breadcrumb_schema(crumbs)]
    return assemble("Reviews — 5.0 Stars Across Central Texas | Excel Pest", desc, canonical, body, schema)


def offers():
    canonical = BIZ["domain"] + "/offers.html"
    crumbs = [("Home", "/"), ("Offers", None)]
    body = page_hero("Offers & Discounts", "Straightforward value — no gimmicks, no hidden prices.", crumbs) + """
  <section class="section">
    <div class="container">
      <div class="offer-strip" style="margin-bottom:26px;">
        <div>
          <span class="pct">10% off</span>
          <h3>For those who serve Central Texas</h3>
          <p class="mb-0" style="color:#cdd6e6;">Military, veterans, first responders, nurses and teachers.</p>
        </div>
        <a class="btn btn--primary" href="/contact.html">Get started</a>
      </div>
      <div class="prose">
        <p class="lead">We keep our offers simple, because trust is the point.</p>
        <ul>
          <li><strong>10% off for heroes &amp; educators.</strong> Military, veterans, first responders, nurses
             and teachers save 10%. Please mention it when you schedule — it is not combinable with other offers.</li>
          <li><strong>Free estimates.</strong> Always. We will assess the problem and give you a clear quote before
             any work begins.</li>
          <li><strong>Warranties on our work.</strong> We stand behind what we do.</li>
          <li><strong>Emergency service.</strong> Some pests cannot wait for next week — call us.</li>
          <li><strong>Licensed &amp; insured.</strong> Texas {license}, with continuous annual technician education.</li>
        </ul>
        <div class="callout">
          We do not publish prices because every property is different — an honest quote beats a fake "starting at"
          number. <a href="/contact.html">Ask for your free estimate</a> and you will know exactly where you stand.
        </div>
      </div>
    </div>
  </section>""".format(license=BIZ["license"])
    body += cta_band()
    desc = "10% off pest control for military, veterans, first responders, nurses and teachers. Free estimates, warranties and emergency service from Excel Pest. Call (737) 201-3059."
    schema = [business_schema(), breadcrumb_schema(crumbs)]
    return assemble("Offers & Discounts — 10% for Heroes & Educators | Excel Pest", desc, canonical, body, schema)


def pet_safety():
    canonical = BIZ["domain"] + "/pet-family-safety.html"
    crumbs = [("Home", "/"), ("Pet & Family Safety", None)]
    body = page_hero("Pet & Family Safety", "The first question every parent and dog owner asks — answered.", crumbs) + """
  <section class="section">
    <div class="container split">
      <div class="prose">
        <p class="lead">When you search for pest control, the real question underneath is usually: <em>is this
           safe for my kids and my pets?</em> It is the right question, and it is the one we built our approach
           around.</p>
        <h2>Water-based products, chosen on purpose</h2>
        <p>Our products are water-based. Owner {owner}'s philosophy has always been to treat every home as if it
           were his own and every customer — and their four-legged family members — like neighbors. That is not a
           slogan on this page; it is why we use what we use.</p>
        <h2>Applied by licensed technicians</h2>
        <p>Products are only as safe as the person applying them. Our technicians are licensed, insured, and
           kept current through continuous annual education, so treatments are applied correctly and exactly
           where they are needed — not blanketed where they are not.</p>
        <div class="callout">
          <strong>Safe when applied as directed.</strong> We will walk you through anything you should know for
          your family and pets at the time of service. Have a question before we come out?
          <a href="/contact.html">Just ask</a> — or call <a href="tel:{ptel}">{phone}</a>.
        </div>
      </div>
      <div>
        <div class="card">
          <h3 class="mt-0">Why families choose us</h3>
          <ul class="prose" style="margin:0;">
            <li>Water-based products</li>
            <li>Licensed &amp; insured ({license})</li>
            <li>Ongoing technician education</li>
            <li>Targeted treatment, not over-spraying</li>
            <li>28 years serving Central Texas families</li>
          </ul>
          <a class="btn btn--primary" href="/contact.html" style="margin-top:16px;">Get a free estimate</a>
        </div>
      </div>
    </div>
  </section>""".format(owner=BIZ["owner"], ptel=BIZ["phone_tel"], phone=BIZ["phone"], license=BIZ["license"])
    body += cta_band()
    desc = "Is pest control safe for kids and pets? Excel Pest uses water-based products applied by licensed technicians. Family-focused pest control in Central Texas since 1998."
    schema = [business_schema(), breadcrumb_schema(crumbs)]
    return assemble("Pet & Family Safety — Water-Based Pest Control | Excel Pest", desc, canonical, body, schema)


FAQS = [
    ("Are your products safe for children and pets?",
     "Yes — our products are water-based and applied by licensed technicians exactly where they are needed. Safety for your family and four-legged family members is the throughline of how we work. See our <a href=\"/pet-family-safety.html\">pet &amp; family safety</a> page."),
    ("Do you offer free estimates?",
     "Always. We assess the problem and give you a clear quote before any work begins."),
    ("Are you licensed and insured?",
     "Yes. We are a licensed Texas pest control operator (TPCL 0786979), insured, and our technicians complete continuous annual education."),
    ("Do you guarantee your work?",
     "We back our work with a warranty and offer emergency service when a pest problem cannot wait."),
    ("What areas do you serve?",
     "27 Central Texas cities from South Austin through Hays County into the Hill Country — Buda, Kyle, San Marcos, Dripping Springs, Wimberley and more. See our <a href=\"/service-area.html\">service area</a>."),
    ("Can you provide a termite letter for a home closing?",
     "Yes. We schedule WDI reports (termite letters) quickly for lenders and title companies. See <a href=\"/services/termite-letters.html\">termite letters &amp; WDI reports</a>."),
    ("Do you offer any discounts?",
     "We offer 10% off for military, veterans, first responders, nurses and teachers — just mention it when you schedule. See <a href=\"/offers.html\">offers</a>."),
    ("Do you handle landscaping and lawn installation?",
     "Excel Pest handles lawn pests, weeds and disease. For landscape design, sod and hardscape, our sister company <a href=\"" + BIZ["sister_url"] + "\" rel=\"noopener\">Research Turf Management</a> handles the build side."),
]


def faq():
    canonical = BIZ["domain"] + "/faq.html"
    crumbs = [("Home", "/"), ("FAQ", None)]
    items = "".join(
        '<h3>%s</h3><p>%s</p>' % (html.escape(q), a) for q, a in FAQS
    )
    body = page_hero("Frequently Asked Questions", "Quick answers about our Central Texas pest control.", crumbs) + """
  <section class="section">
    <div class="container" style="max-width:820px;">
      <div class="prose">
{items}
      </div>
    </div>
  </section>""".format(items=items)
    body += cta_band()
    # FAQ schema needs plain-text answers
    import re as _re
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": _re.sub("<[^>]+>", "", a)},
        } for q, a in FAQS],
    }
    desc = "Answers about Excel Pest — product safety for pets and kids, free estimates, licensing, service area, termite letters and discounts. Central Texas pest control since 1998."
    schema = [faq_schema, business_schema(), breadcrumb_schema(crumbs)]
    return assemble("FAQ — Excel Pest & Lawn Control | Central Texas", desc, canonical, body, schema)


def contact():
    canonical = BIZ["domain"] + "/contact.html"
    crumbs = [("Home", "/"), ("Contact", None)]
    options = "".join("<option>%s</option>" % html.escape(s["nav"]) for s in SERVICES)
    body = page_hero("Get a Free Estimate", "Call, text, or send a message — we'll get right back to you.", crumbs) + """
  <section class="section">
    <div class="container contact-grid">
      <div>
        <span class="eyebrow">Reach us directly</span>
        <ul class="info-list">
          <li><span class="label">Call</span><span class="value"><a href="tel:{ptel}">{phone}</a></span></li>
          <li><span class="label">Text</span><span class="value"><a href="sms:{ttel}">{text}</a></span></li>
          <li><span class="label">Email</span><span class="value"><a href="mailto:{email}">{email}</a></span></li>
          <li><span class="label">Office</span><span class="value">{street}, {city}, {state} {zip}</span></li>
          <li><span class="label">License</span><span class="value">{license}</span></li>
        </ul>
        <h3>Hours</h3>
        <ul class="hours">
          <li><span class="day">Monday – Friday</span><span class="time">8:00 – 5:00</span></li>
          <li><span class="day">Saturday – Sunday</span><span class="time">Closed</span></li>
        </ul>
        <div class="crosslink" style="margin-top:20px;">
          <p class="mb-0"><strong>Landscaping?</strong> Our sister company
             <a href="{sister_url}" rel="noopener">{sister}</a> · {sister_phone}.</p>
        </div>
      </div>
      <div>
        <div class="card">
          <h3 class="mt-0">Request an estimate</h3>
          <form action="mailto:{email}" method="post" data-estimate novalidate>
            <div class="field"><label for="name">Name</label>
              <input id="name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="phone">Phone</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
            <div class="field"><label for="email">Email</label>
              <input id="email" name="email" type="email" autocomplete="email"></div>
            <div class="field"><label for="service">What do you need help with?</label>
              <select id="service" name="service">{options}<option>Not sure / other</option></select></div>
            <div class="field"><label for="message">Tell us what you're seeing</label>
              <textarea id="message" name="message" rows="4"></textarea></div>
            <button class="btn btn--primary" type="submit" style="width:100%;">Send Request</button>
            <p class="hero__note" style="color:var(--muted);" data-form-note>By submitting, you agree to be contacted about your request.</p>
          </form>
        </div>
      </div>
    </div>
  </section>""".format(
        ptel=BIZ["phone_tel"], phone=BIZ["phone"], ttel=BIZ["text_tel"], text=BIZ["text"], email=BIZ["email"],
        street=BIZ["street"], city=BIZ["city"], state=BIZ["state"], zip=BIZ["zip"], license=BIZ["license"],
        sister_url=BIZ["sister_url"], sister=BIZ["sister_name"], sister_phone=BIZ["sister_phone"], options=options,
    )
    desc = "Request a free pest control estimate in Buda and Central Texas. Call (737) 201-3059, text (737) 350-8553, or send a message. Family-owned since 1998."
    schema = [business_schema(), breadcrumb_schema(crumbs), {
        "@context": "https://schema.org", "@type": "ContactPage", "url": canonical,
    }]
    return assemble("Contact & Free Estimate | Austin Excel Pest & Lawn Control", desc, canonical, body, schema)


def not_found():
    body = """
  <section class="page-hero" style="min-height:60vh;display:grid;align-items:center;">
    <div class="container text-center">
      <span class="eyebrow">Error 404</span>
      <h1>We couldn't find that page.</h1>
      <p style="margin:0 auto 24px;">Try one of these instead:</p>
      <div class="hero__actions" style="justify-content:center;">
        <a class="btn btn--primary" href="/">Go Home</a>
        <a class="btn btn--ghost" href="/services.html">Services</a>
        <a class="btn btn--ghost" href="/service-area.html">Service Area</a>
        <a class="btn btn--ghost" href="/contact.html">Contact</a>
      </div>
    </div>
  </section>"""
    return assemble("Page Not Found | Excel Pest", "Page not found.", BIZ["domain"] + "/404.html", body, [], noindex=True)


def pay_invoice():
    canonical = BIZ["domain"] + "/pay-invoice.html"
    body = """
  <main class="pay-wrap">
    <div class="pay-card">
      <div class="gate">
        <strong>Not live yet.</strong> This payment page is disabled until the PayPal button is confirmed in
        writing by the business owner and tested. See the code comment in this file.
      </div>
      <span class="pay-company">{name}</span>
      <h1>Pay Your Invoice</h1>
      <p>Settle your bill securely online, or call us and we'll take payment over the phone.</p>
      <div class="pay-checklist">
        <strong>Have this ready</strong>
        <ul><li>Your invoice number</li><li>The amount due on your invoice</li><li>Your billing name and ZIP code</li></ul>
      </div>
      <div class="paypal-placeholder">Secure PayPal checkout will appear here once the account is confirmed.</div>
      <p class="pay-secure">🔒 Processed by PayPal. We never see or store your card details.</p>
      <div class="pay-phone">Prefer to pay by phone? Call <a href="tel:{ptel}">{phone}</a>.</div>
    </div>
  </main>""".format(name=html.escape(BIZ["name"]), ptel=BIZ["phone_tel"], phone=BIZ["phone"])
    # Special head with page-specific styles + gated warning comment
    gate_comment = """
  <!--
    DO NOT PUBLISH THIS PAGE UNTIL THE PAYPAL BUTTON IS CONFIRMED IN WRITING.
    Payments go to whichever PayPal account owns button ID PBRKNRY4BQUJG.
    Confirm in writing that the button belongs to the business account, then make
    and refund a $1.00 test payment. The complete ready-to-use page is in the
    brief's CODE-copy-paste-these/00_pay-invoice-page-COMPLETE.html. Until then this
    page is noindex with NO live PayPal button. On launch: robots index,follow;
    keep in sitemap; no contact form; no login; WebPage schema only.
  -->"""
    pay_styles = """
  <style>
    .pay-wrap { background: var(--bg-soft); min-height: 70vh; display: grid; place-items: center; padding: 56px 20px; }
    .pay-card { background:#fff; max-width:520px; width:100%; border-radius:14px; box-shadow:var(--shadow-lg); padding:40px; text-align:center; }
    .pay-company { text-transform:uppercase; letter-spacing:.16em; font-size:.78rem; font-weight:800; color:var(--navy); }
    .pay-card h1 { font-size:1.9rem; margin:6px 0 8px; }
    .pay-checklist { text-align:left; background:var(--bg-navy-tint); border-radius:10px; padding:18px 22px; margin:22px 0; }
    .pay-secure { color:var(--muted); font-size:.9rem; margin-top:18px; }
    .pay-phone { margin-top:20px; font-size:1.05rem; } .pay-phone a { font-weight:800; }
    .paypal-placeholder { border:2px dashed var(--line); border-radius:10px; padding:28px; color:var(--muted); background:#fff; margin:8px 0; }
    .gate { background:#fff4e8; border:1px solid var(--orange); color:var(--orange-dark); border-radius:10px; padding:14px 18px; font-size:.9rem; margin-bottom:20px; text-align:left; }
  </style>"""
    h = head("Pay Your Invoice | Austin Excel Pest & Lawn Control",
             "Pay your Excel Pest invoice securely online, or call (737) 201-3059 to pay by phone.",
             canonical, [], noindex=True)
    h = h.replace("</head>", gate_comment + pay_styles + "\n</head>")
    return h + "\n" + header() + "\n" + body + footer() + "\n"


# --------------------------------------------------------------------------
# Sitemap / robots
# --------------------------------------------------------------------------

def build_sitemap(urls):
    rows = "\n".join(
        "  <url><loc>%s</loc><changefreq>%s</changefreq><priority>%s</priority></url>" % (u, cf, pr)
        for u, cf, pr in urls
    )
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '\n</urlset>\n'


def build_robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BIZ["domain"]


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    written = []
    sitemap_urls = []

    def emit(path, contents, sm=True, cf="monthly", pr="0.7"):
        written.append(write(path, contents))
        if sm:
            loc = BIZ["domain"] + "/" if path == "index.html" else BIZ["domain"] + "/" + path
            sitemap_urls.append((loc, cf, pr))

    emit("index.html", home(), cf="weekly", pr="1.0")
    emit("services.html", services_hub(), cf="monthly", pr="0.9")
    emit("service-area.html", service_area_hub(), cf="monthly", pr="0.8")
    emit("about.html", about(), pr="0.7")
    emit("reviews.html", reviews(), pr="0.7")
    emit("offers.html", offers(), pr="0.7")
    emit("pet-family-safety.html", pet_safety(), pr="0.6")
    emit("faq.html", faq(), pr="0.6")
    emit("contact.html", contact(), cf="monthly", pr="0.8")

    for s in SERVICES:
        emit("services/%s.html" % s["slug"], render_service(s), cf="monthly", pr="0.8")
    for l in LOCATIONS:
        emit("locations/%s.html" % l["slug"], render_location(l), cf="monthly", pr="0.7")

    # Non-sitemap pages
    write("404.html", not_found())
    written.append("404.html")
    write("pay-invoice.html", pay_invoice())  # intentionally excluded from sitemap until launch
    written.append("pay-invoice.html")

    write("sitemap.xml", build_sitemap(sitemap_urls)); written.append("sitemap.xml")
    write("robots.txt", build_robots()); written.append("robots.txt")

    print("Generated %d files:" % len(written))
    for p in written:
        print("  " + p)


if __name__ == "__main__":
    main()
