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
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

# Optional base path for hosting under a sub-directory (e.g. GitHub Pages
# project site at /Excel-Pest/). Empty for root hosting (Amplify, S3/CloudFront).
BASE = os.environ.get("BASE_PATH", "").rstrip("/")

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
        "related": ["scorpion-control", "rodent-removal", "lawn-pest-control"],
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
        "related": ["pest-control", "rodent-removal", "termite-control"],
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
        "related": ["termite-control", "pest-control", "rodent-removal"],
    },
    {
        "slug": "rodent-removal", "nav": "Rodent Removal", "icon": "🐀",
        "h1": "Rodent Removal in Central Texas",
        "title": "Rodent Removal in Buda, TX | Rats & Mice | Excel Pest",
        "desc": "Fast rat and mouse removal from Central Texas attics, garages and walls — then we seal them out. Water-based, pet-safe. Call (737) 201-3059.",
        "lead": "Scratching in the attic at night, droppings in the pantry, chewed wiring — rats and mice do real damage fast, and they breed even faster. We remove the rodents inside now, then seal the gaps so it doesn't repeat.",
        "treats": ["Roof rats & house mice", "Attic & wall-void activity", "Droppings & gnaw marks", "Chewed wiring (a fire risk)"],
        "sections": [
            ("Removal done right", "<p>We locate the activity, remove the rodents, and clean up the trails they leave. But removal alone is only half the job — new rodents follow the same paths back in. That's why we pair it with <a href=\"/services/rodent-exclusion.html\">rodent exclusion</a> to seal them out for good.</p>"),
            ("Why speed matters", "<p>Rodents breed quickly and gnaw constantly — including on electrical wiring, a genuine fire risk. The sooner we're in, the less damage and the smaller the population to clear. We also check for the wildlife that uses the same gaps — see <a href=\"/services/wildlife-live-trapping.html\">wildlife live trapping</a>.</p>"),
        ],
        "related": ["rodent-exclusion", "wildlife-live-trapping", "pest-control"],
    },
    {
        "slug": "rodent-exclusion", "nav": "Rodent Exclusion", "icon": "🧰",
        "h1": "Rodent Exclusion — Seal Them Out for Good",
        "title": "Rodent Exclusion in Buda, TX | Seal Out Rats & Mice | Excel Pest",
        "desc": "Rodent exclusion that finds and seals every entry point so rats and mice can't get back into your Central Texas home. Call (737) 201-3059.",
        "lead": "Trapping without sealing is a treadmill — new rodents follow the same trails right back inside. Exclusion is the permanent fix: we find every gap and close it with materials rodents can't chew through.",
        "treats": ["Roofline & eave gaps", "Weep holes & pipe penetrations", "Garage & foundation gaps", "Vent & soffit openings"],
        "sections": [
            ("The permanent half of rodent control", "<p>A mouse fits through a gap the size of a dime; a rat, a quarter. We inspect the whole exterior — roofline, weep holes, pipe and cable penetrations, the garage — and seal each entry with steel mesh and sealants rodents can't gnaw.</p>"),
            ("Pairs with removal", "<p>Exclusion works hand-in-hand with <a href=\"/services/rodent-removal.html\">rodent removal</a>: clear the ones inside, then seal so no more get in. Together they end the problem instead of managing it month after month.</p>"),
        ],
        "related": ["rodent-removal", "wildlife-live-trapping", "pest-control"],
    },
    {
        "slug": "wildlife-live-trapping", "nav": "Wildlife Live Trapping", "icon": "🦝",
        "h1": "Wildlife Live Trapping & Removal in Central Texas",
        "title": "Wildlife Live Trapping in Buda, TX | Raccoons, Squirrels, Opossums",
        "desc": "Humane live trapping and removal of raccoons, squirrels and opossums from Central Texas homes, with entry points sealed. Call (737) 201-3059.",
        "lead": "Raccoons in the attic, squirrels in the soffit, opossums under the deck — Central Texas wildlife treats homes like the hollow trees they replaced. We remove them humanely with live trapping and close off the damage so they cannot move back in.",
        "treats": ["Raccoons", "Squirrels", "Opossums", "Attic, soffit & deck intrusions"],
        "sections": [
            ("Humane, and it lasts", "<p>We use humane live-trapping and hands-on removal, then repair and seal the entry points — the vent, gable, or roofline gap that let the animal in. Without that last step, the next animal simply finds the same open door.</p>"),
            ("Acreage and Hill Country lots", "<p>On the larger lots around Driftwood, Dripping Springs and Wimberley, wildlife pressure is constant. We know the local species and the ways they get into a home out here — and we pair trapping with <a href=\"/services/rodent-exclusion.html\">exclusion</a> so it holds.</p>"),
        ],
        "related": ["rodent-removal", "rodent-exclusion", "pest-control"],
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
        "related": ["pest-control", "lawn-pest-control", "wildlife-live-trapping"],
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
    {
        "slug": "ant-control", "nav": "Ant Control", "icon": "🐜",
        "h1": "Ant Control in Buda & Central Texas",
        "title": "Ant Control in Buda, TX | Fire Ants & Household Ants | Excel Pest",
        "desc": "Fire ants, sugar ants and carpenter ants treated at the colony across Buda and Central Texas. Water-based, pet-safe. Call (737) 201-3059.",
        "lead": "From fire-ant mounds in the yard to sugar ants marching across the kitchen counter, ants are the most common call we get in Central Texas. Killing the trail you can see does nothing — the colony just sends more. We treat the source.",
        "treats": ["Fire ants", "Sugar / odorous ants", "Carpenter ants", "Acrobat & pharaoh ants", "Mounds in the yard"],
        "sections": [
            ("Why the ants keep coming back", "<p>Spraying a visible trail kills a few foragers while the colony — often thousands strong and hidden in a wall, slab or yard mound — keeps producing more. We use baits and non-repellent products the ants carry back to the nest, so the colony collapses instead of just relocating.</p>"),
            ("Fire ants and Central Texas yards", "<p>Fire ants are their own problem here — painful, fast-spreading, and a hazard for kids and pets. We treat mounds directly and set up a yard program that keeps them from re-establishing through the warm months.</p>"),
        ],
        "related": ["cockroach-control", "cricket-control", "pest-control"],
    },
    {
        "slug": "cockroach-control", "nav": "Cockroach Control", "icon": "🪳",
        "h1": "Cockroach Control in Central Texas",
        "title": "Cockroach Control in Buda, TX | Roach Extermination | Excel Pest",
        "desc": "German and American cockroaches eliminated from Central Texas homes and kept out. Water-based, pet-safe treatment. Call (737) 201-3059.",
        "lead": "Roaches are more than a gross surprise at 2 a.m. — they contaminate food, trigger allergies, and multiply fast in our warm, humid climate. We find where they breed and shut it down.",
        "treats": ["German cockroaches", "American (palmetto) roaches", "Oriental roaches", "Egg cases & harborage"],
        "sections": [
            ("Treat where they breed, not where you see them", "<p>By the time you spot one roach, dozens are hidden behind appliances, in drains and inside wall voids. We target those harborage points and breeding sites so the population crashes, then set up prevention so it stays gone.</p>"),
            ("Built for Central Texas roaches", "<p>Our heat and humidity let American 'palmetto' roaches thrive outdoors and wander in, while German roaches ride in on boxes and groceries and breed in kitchens. We treat for both, inside and out.</p>"),
        ],
        "related": ["ant-control", "pest-control", "rodent-removal"],
    },
    {
        "slug": "cricket-control", "nav": "Cricket Control", "icon": "🦗",
        "h1": "Cricket Control in Central Texas",
        "title": "Cricket Control in Buda, TX | Fall Field Crickets | Excel Pest",
        "desc": "Central Texas field-cricket swarms controlled at the source for homes and businesses. Water-based, pet-safe. Call (737) 201-3059.",
        "lead": "Every late summer, field crickets swarm Central Texas by the thousands — piling at doorways, under lights and inside garages. They stain surfaces, smell, and draw the scorpions and spiders that feed on them. We break the cycle.",
        "treats": ["Field crickets", "Camel / spider crickets", "Exterior-lighting swarms", "Entry points & harborage"],
        "sections": [
            ("Why crickets matter more than you think", "<p>Beyond the noise and mess, crickets are a food source that pulls <a href=\"/services/scorpion-control.html\">scorpions</a> and <a href=\"/services/spider-control.html\">spiders</a> toward your home. Controlling crickets is one of the most effective ways to reduce those pests too.</p>"),
            ("Timing the treatment to cricket season", "<p>The big swarms hit when the weather turns in late summer and fall. We treat the perimeter and harborage ahead of and through the season, and address the exterior lighting and gaps that concentrate them at your doors.</p>"),
        ],
        "related": ["scorpion-control", "spider-control", "pest-control"],
    },
    {
        "slug": "flea-control", "nav": "Flea Control", "icon": "🐾",
        "h1": "Flea Control for Central Texas Homes & Yards",
        "title": "Flea Control in Buda, TX | Home & Yard Flea Treatment | Excel Pest",
        "desc": "Fleas eliminated from the home and yard with treatment that breaks the life cycle — safe for the pets they bite. Call (737) 201-3059.",
        "lead": "Fleas don't just bite pets — they infest carpet, bedding and yards, and a few can become thousands in weeks. Our mild winters let them thrive nearly year-round here. We treat the whole life cycle, indoors and out.",
        "treats": ["Adult fleas", "Eggs & larvae in carpet / bedding", "Shaded yard harborage", "Re-infestation prevention"],
        "sections": [
            ("Break the life cycle, not just the adults", "<p>Most of a flea problem isn't the adults you see — it's eggs and larvae hidden in carpet, pet bedding and shaded yard soil. We treat all stages so the infestation actually ends instead of bouncing back in two weeks.</p>"),
            ("Coordinated with your vet plan", "<p>Yard and home treatment works best alongside the flea prevention your vet provides. We'll tell you exactly what to do before and after service to protect your four-legged family members.</p>"),
        ],
        "related": ["tick-control", "pest-control", "rodent-removal"],
    },
    {
        "slug": "spider-control", "nav": "Spider Control", "icon": "🕷️",
        "h1": "Spider Control in Central Texas",
        "title": "Spider Control in Buda, TX | Black Widows & Recluse | Excel Pest",
        "desc": "Spider control for Central Texas homes — including black widow and brown recluse hotspots. Web removal + prevention. Call (737) 201-3059.",
        "lead": "A few spiders keep other bugs down; a lot of spiders — or a black widow by the garage — is a different story. We reduce spiders by cutting off their food supply and clearing the corners, eaves and garages they nest in.",
        "treats": ["Common house spiders", "Black widows", "Brown recluse", "Webs in eaves & garages"],
        "sections": [
            ("Fewer bugs means fewer spiders", "<p>Spiders follow prey. Our exterior barrier reduces the insects spiders feed on — the most effective long-term way to bring their numbers down — along with knocking down webs and treating the eaves, garages and crawlspaces they favor.</p>"),
            ("The two to watch for in Central Texas", "<p>Black widows like garages, meter boxes and woodpiles; brown recluse hide in undisturbed storage. We treat those hotspots specifically and advise you on reducing the clutter and harborage they need.</p>"),
        ],
        "related": ["cricket-control", "scorpion-control", "pest-control"],
    },
    {
        "slug": "tick-control", "nav": "Tick Control", "icon": "🕸️",
        "h1": "Tick Control for Central Texas Yards",
        "title": "Tick Control in Buda, TX | Yard Tick Treatment | Excel Pest",
        "desc": "Tick control for Central Texas yards and properties — protecting family and pets from bites. Focused on shaded harborage. Call (737) 201-3059.",
        "lead": "Ticks turn a backyard, greenbelt edge or wooded lot into a health risk for your family and pets. In Central Texas they hide in tall grass, leaf litter and shaded borders. We treat where they wait.",
        "treats": ["Yard & perimeter ticks", "Shaded / leaf-litter harborage", "Pet runs & trails", "Greenbelt & wood-line borders"],
        "sections": [
            ("Treat the edges where ticks wait", "<p>Ticks don't live in the open, mowed lawn — they wait in the shaded, humid borders: leaf litter, tall grass, fence lines and the wood line. We focus treatment there, which is exactly where your family and pets pick them up.</p>"),
            ("Especially important on acreage and greenbelt lots", "<p>Homes backing to greenbelt or on Hill Country acreage see the most tick pressure. A perimeter program keeps the yard usable through the warm months — and pairs well with <a href=\"/services/flea-control.html\">flea control</a>.</p>"),
        ],
        "related": ["flea-control", "lawn-pest-control", "pest-control"],
    },
]
SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# Grouped services for the header mega-menu and the services hub
MENU_GROUPS = [
    ("Insect Control", ["ant-control", "cockroach-control", "cricket-control", "flea-control",
                        "scorpion-control", "spider-control", "termite-control", "tick-control"]),
    ("Rodent & Wildlife", ["rodent-removal", "rodent-exclusion", "wildlife-live-trapping"]),
    ("More Services", ["pest-control", "mosquito-misting", "termite-letters", "lawn-pest-control"]),
]

# Per-service mini-FAQ (adds FAQPage schema + an accordion to each service page)
SERVICE_FAQS = {
    "pest-control": [
        ("How often should I have pest control done?", "Most Central Texas homes do best on a recurring quarterly plan that stays ahead of the seasonal surges. We'll recommend a schedule for your property — and one-time and emergency visits are available too."),
        ("Are the products safe for my kids and pets?", "Yes. Our products are water-based and applied by licensed technicians. See our <a href=\"/pet-family-safety.html\">pet &amp; family safety</a> page."),
        ("Do you treat inside and outside?", "Both. Every visit covers interior trouble spots and a full exterior barrier around the foundation, eaves and entry points."),
    ],
    "scorpion-control": [
        ("Why do I still see scorpions after treating inside?", "Because scorpions live outside — in rock, cedar and wood piles — and wander in. Lasting control treats the perimeter and seals entry points, not just the interior."),
        ("When is scorpion season in Central Texas?", "They're most active in the warm months and move toward homes during drought (for water) and after heavy rain (to escape it). Year-round exclusion keeps them out."),
        ("Are Central Texas scorpions dangerous?", "The striped bark scorpion's sting is painful but rarely medically serious for most people — still not something you want indoors, which is why we focus on keeping them out."),
    ],
    "termite-control": [
        ("How do I know if I have termites?", "Common signs are mud tubes on the foundation, hollow-sounding or blistered wood, and swarms after spring rain. A licensed inspection confirms it."),
        ("Do you offer a warranty?", "Yes — we back our termite work with a warranty. Ask for details during your inspection."),
        ("How often should I have a termite inspection?", "An annual inspection is smart in Central Texas, where soil movement gives termites constant access to foundations."),
    ],
    "termite-letters": [
        ("What is a termite letter / WDI report?", "It's the official Wood Destroying Insect inspection report, on the state form that lenders and title companies require for many closings."),
        ("How fast can you get it done?", "Tell us your closing date and property and we schedule promptly and turn the paperwork around quickly."),
        ("What if the inspection finds termites?", "You'll get clear options, including <a href=\"/services/termite-control.html\">treatment</a> before your deadline."),
    ],
    "rodent-removal": [
        ("What's the difference between removal and exclusion?", "Removal gets rid of the rodents inside; exclusion seals the gaps that let them in. We do both — trapping alone just repeats."),
        ("Where do rodents usually get in?", "Rooflines, weep holes, pipe penetrations and the garage are common entry points in Central Texas homes. We find and seal them."),
        ("Are the treatments safe around pets?", "We choose methods with your family and pets in mind and place them where pets can't reach."),
    ],
    "wildlife-live-trapping": [
        ("Do you remove wildlife humanely?", "Yes — we use humane live-trapping and hands-on removal, then seal the entry points so animals can't return."),
        ("What animals do you handle?", "Common Central Texas intruders like raccoons, squirrels and opossums in attics, soffits and under decks."),
        ("Will they come back?", "Not through the same opening — we repair and seal the entry points as part of the job."),
    ],
    "mosquito-misting": [
        ("How does a misting system work?", "It runs on a schedule you control, releasing a fine treatment around your landscaping to knock down mosquitoes before they gather."),
        ("Do I still need to deal with standing water?", "Reducing standing water helps, and we treat breeding sites as part of control — the misting system handles the rest."),
        ("Is misting safe for my yard and pets?", "We use water-based products and tune the system to your landscaping, and we'll walk you through anything to know for pets."),
    ],
    "lawn-pest-control": [
        ("How do I know if it's bugs or drought killing my lawn?", "Spreading brown patches, spongy turf, or moths lifting off at dusk usually mean chinch bugs, grubs or armyworms — we diagnose the real cause before treating."),
        ("Do you handle weeds and disease too?", "Yes — along with lawn pests we treat weeds and turf disease like brown patch."),
        ("Do you do landscaping and sod installation?", "That's our sister company, <a href=\"" + BIZ["sister_url"] + "\" rel=\"noopener\">Research Turf Management</a>. We handle the pests, weeds and disease."),
    ],
    "rodent-exclusion": [
        ("What do you use to seal the gaps?", "Steel mesh, hardware cloth and sealants rodents can't gnaw through — placed at rooflines, weep holes, pipe penetrations, vents and the garage."),
        ("Do you guarantee the work?", "We back our exclusion work with a warranty. Ask for the details when we inspect."),
        ("Do I need removal too?", "Usually yes — clear the rodents inside first with <a href=\"/services/rodent-removal.html\">rodent removal</a>, then seal so no more get in."),
    ],
    "ant-control": [
        ("Do you treat fire ants in the yard?", "Yes — direct mound treatment plus a broadcast yard program to stop them re-establishing through the warm months."),
        ("Why not just use store-bought ant spray?", "Store sprays kill the foragers you see but rarely reach the colony, so the ants return. We use colony-level baits and non-repellents that collapse the nest."),
        ("Are ant treatments safe for pets?", "Yes — water-based and placed where pets can't reach. We'll walk you through anything to know at the visit."),
    ],
    "cockroach-control": [
        ("How long does it take to get rid of roaches?", "Most homes see a sharp drop within the first couple of weeks as the breeding sites are knocked out; heavy infestations may need a follow-up. We set up prevention so they stay gone."),
        ("Do you treat kitchens and drains?", "Yes — those are prime roach harborage. We target the voids, drains and appliance gaps where they hide and breed."),
        ("Is the treatment safe for kids and pets?", "Yes, water-based and applied where it's needed, not blanketed across living areas."),
    ],
    "cricket-control": [
        ("When is cricket season in Central Texas?", "The big field-cricket swarms hit in late summer and fall when the weather turns. We treat ahead of and through the season."),
        ("Do crickets really attract scorpions?", "Yes — crickets are a favorite food, so cutting cricket numbers is one of the best ways to reduce scorpions and spiders around your home."),
        ("Are the treatments pet-safe?", "Yes — water-based and focused on the exterior perimeter and harborage."),
    ],
    "flea-control": [
        ("Is flea treatment safe for my pets?", "Yes — it's water-based, and we coordinate with the vet-provided prevention your pets are on. We'll tell you how to prep and when it's safe to return."),
        ("Do you treat the yard as well as the house?", "Both — fleas breed in shaded yard soil as well as carpet and bedding, so treating only indoors leaves a source outside."),
        ("How should I prep my home?", "Vacuum thoroughly, wash pet bedding, and clear floors. We'll give you the full short checklist when you book."),
    ],
    "spider-control": [
        ("Do you handle black widows and brown recluse?", "Yes — we treat their hotspots (garages, meter boxes, woodpiles, undisturbed storage) specifically and advise on reducing harborage."),
        ("Are the treatments safe for pets?", "Yes — water-based and applied to eaves, corners and the exterior barrier rather than living surfaces."),
        ("Will the webs just come back?", "Far less, because we reduce the insects spiders feed on. Ongoing service keeps eaves and corners clear."),
    ],
    "tick-control": [
        ("Are ticks dangerous in Central Texas?", "Ticks can transmit disease to people and pets, so keeping them out of the yard matters — especially on greenbelt and acreage lots."),
        ("Is tick treatment safe for pets?", "Yes — water-based and focused on the shaded borders where ticks wait, not the open lawn where pets play."),
        ("How often should the yard be treated?", "Through the warm months a recurring perimeter program keeps pressure down; we'll recommend a cadence for your property."),
    ],
}

# Per-service inline image (ChatGPT generation prompt)
SERVICE_IMAGES = {
    "pest-control": ("🏡", "pest-control-exterior-treatment.webp", "Excel Pest technician treating the exterior of a Central Texas home",
        "A licensed pest control technician in a clean plain uniform spraying a water-based treatment along the exterior foundation of a limestone Central Texas home, live oak trees and Hill Country landscaping behind, warm morning light, photorealistic, no text, no logos, no watermark, no visible brand names."),
    "scorpion-control": ("🦂", "scorpion-hill-country.webp", "Striped bark scorpion on Hill Country limestone",
        "A close, detailed photo of a striped bark scorpion on pale limestone rock at dusk in the Texas Hill Country, cedar and dry grass softly blurred behind, natural light, photorealistic, no text, no logos, no watermark."),
    "termite-control": ("🪵", "termite-mud-tubes.webp", "Termite mud tubes on a home foundation",
        "A macro photo of subterranean termite mud tubes running up the concrete foundation of a Central Texas home, weathered slab and soil visible, natural daylight, photorealistic, no text, no logos, no watermark."),
    "termite-letters": ("📄", "termite-letter-inspection.webp", "Inspector performing a WDI termite inspection on a home",
        "A pest control inspector with a clipboard and flashlight examining the foundation and eaves of a suburban Central Texas home during a real-estate inspection, warm daylight, photorealistic, no text, no logos, no watermark."),
    "rodent-removal": ("🐀", "rodent-removal-attic.webp", "Roof rat at the edge of a home attic",
        "A roof rat peering from the edge of a home attic with insulation visible, dim natural light, photorealistic, no text, no logos, no watermark."),
    "rodent-exclusion": ("🧰", "rodent-exclusion-sealing.webp", "Sealing a rodent entry point along a roofline",
        "A technician's hands sealing a gap along a Central Texas home's roofline with steel mesh and sealant, ladder visible, daylight, photorealistic, no text, no logos, no watermark."),
    "wildlife-live-trapping": ("🦝", "wildlife-attic-raccoon.webp", "Raccoon at an attic vent of a Central Texas home",
        "A raccoon peeking out of an attic gable vent on a suburban Central Texas home at dusk, cedar and oak around the roof, natural light, photorealistic, no text, no logos, no watermark."),
    "mosquito-misting": ("🦟", "mosquito-misting-pergola.webp", "Mosquito misting nozzle on a backyard pergola",
        "A backyard mosquito misting system nozzle mounted on a wooden pergola in a lush Central Texas backyard at golden hour, patio and native plants around, a fine mist visible, photorealistic, no text, no logos, no watermark."),
    "lawn-pest-control": ("🌱", "lawn-chinch-bug-damage.webp", "Chinch bug damage in a St. Augustine lawn",
        "A close view of a St. Augustine lawn in Central Texas with a spreading brown chinch-bug patch, healthy green grass beside damaged turf, bright daylight, photorealistic, no text, no logos, no watermark."),
    "ant-control": ("🐜", "ant-control-fire-ant-mound.webp", "Fire ant mound in a Central Texas lawn",
        "A close photo of a fire ant mound in a Central Texas St. Augustine lawn, a suburban home softly blurred behind, bright daylight, photorealistic, no text, no logos, no watermark."),
    "cockroach-control": ("🪳", "cockroach-control.webp", "American cockroach on a kitchen floor",
        "A single American cockroach on a tiled kitchen floor at night, shallow depth of field, photorealistic, no text, no logos, no watermark."),
    "cricket-control": ("🦗", "cricket-control-doorway.webp", "Field crickets gathered by a doorway at night",
        "Field crickets clustered on limestone and concrete near a doorway at night under a porch light in Central Texas, photorealistic, no text, no logos, no watermark."),
    "flea-control": ("🐾", "flea-control-backyard-dog.webp", "A dog resting in a treated Central Texas backyard",
        "A dog resting on a healthy lawn in a Central Texas backyard at golden hour, photorealistic, no text, no logos, no watermark."),
    "spider-control": ("🕷️", "spider-control-web-eave.webp", "Spider web in the eave of a Central Texas home",
        "A spider web glistening with morning dew in the corner of a limestone home's eave in Central Texas, soft backlight, photorealistic, no text, no logos, no watermark."),
    "tick-control": ("🕸️", "tick-control-property-edge.webp", "Shaded property edge where ticks harbor",
        "A wooded, leaf-littered property edge meeting a mowed Central Texas lawn, dappled shade, photorealistic, no text, no logos, no watermark."),
}

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
    {
        "slug": "austin", "city": "Austin", "county": "Travis County",
        "lead": "Austin is the heart of our region, and we have treated homes across the city — from South Austin, where Excel Pest began in 1998, to the neighborhoods ringing downtown. City living does not mean fewer pests; it means roaches, ants, rodents and scorpions adapting to dense blocks, older foundations and greenbelt edges.",
        "angle": "We work the established bungalows of South and Central Austin and the new builds on the fringe alike, timing recurring service to the city's long, warm pest season.",
        "nearby": ["sunset-valley", "manchaca", "west-lake-hills"],
    },
    {
        "slug": "barton-creek", "city": "Barton Creek", "county": "Travis County",
        "lead": "Barton Creek is greenbelt country — upscale homes tucked against limestone bluffs, live oaks and canyon land on the western edge of Austin. That beautiful setting is also prime scorpion and wildlife habitat.",
        "angle": "Homes backing to the greenbelt see scorpions, spiders and the occasional wildlife visitor. We treat the perimeter and seal entry points so the wild stays outside.",
        "nearby": ["west-lake-hills", "lost-creek", "bee-cave"],
    },
    {
        "slug": "bear-creek", "city": "Bear Creek", "county": "Hays County",
        "lead": "Bear Creek sits just south of Austin in northern Hays County, a quieter community of homes on wooded lots. Cedar, oak and creek bottoms keep pest and wildlife pressure steady year-round.",
        "angle": "Wooded lots invite scorpions, rodents and wildlife toward the house. We build treatments around the whole property, not just the walls.",
        "nearby": ["buda", "manchaca", "driftwood"],
    },
    {
        "slug": "bee-cave", "city": "Bee Cave", "county": "Travis County",
        "lead": "Bee Cave is Hill Country living on the doorstep of Lake Travis — limestone, cedar and upscale homes on rocky terrain. Scorpions and wildlife come with the territory out here.",
        "angle": "Rock landscaping and cedar are exactly what scorpions love. Our exclusion-first approach treats harborage and seals the gaps that let them inside.",
        "nearby": ["lakeway", "west-lake-hills", "barton-creek"],
    },
    {
        "slug": "blanco", "city": "Blanco", "county": "Blanco County",
        "lead": "Blanco sits on its namesake river in the heart of the Hill Country, a small town surrounded by ranch land, limestone and cedar. It is scorpion and rodent country through and through.",
        "angle": "Rural homes and ranchettes face constant pressure from scorpions, rodents and wildlife off the surrounding land. We treat the perimeter and outbuildings, not just the house.",
        "nearby": ["wimberley", "johnson-city", "dripping-springs"],
    },
    {
        "slug": "briarcliff", "city": "Briarcliff", "county": "Travis County",
        "lead": "Briarcliff is a lakeside village on the south shore of Lake Travis, full of hillside homes among cedar and oak. Waterfront and wooded lots keep scorpions, spiders and wildlife in the picture.",
        "angle": "Homes on the slopes above the lake see scorpions and the wildlife the cedar draws. We treat and seal so the view stays yours and the pests stay out.",
        "nearby": ["lakeway", "point-venture", "bee-cave"],
    },
    {
        "slug": "canyon-lake", "city": "Canyon Lake", "county": "Comal County",
        "lead": "Canyon Lake spreads around the Guadalupe River and its reservoir in Comal County — lake homes, weekend places and full-time Hill Country living. Lakeside humidity and cedar mean mosquitoes, scorpions and rodents.",
        "angle": "Vacation homes that sit empty invite rodents and wildlife, while the water feeds mosquitoes. We treat, seal and set a schedule that fits how the home is used.",
        "nearby": ["wimberley", "blanco", "san-marcos"],
    },
    {
        "slug": "creedmoor", "city": "Creedmoor", "county": "Travis County",
        "lead": "Creedmoor is a small rural community in southeastern Travis County, surrounded by farmland and quick new development along the SH-130 corridor. Open land and fresh construction push pests toward homes.",
        "angle": "Cleared lots displace rodents, ants and scorpions into new neighborhoods, and rural acreage brings wildlife. We cover both from our nearby Buda base.",
        "nearby": ["mustang-ridge", "del-valle", "buda"],
    },
    {
        "slug": "hudson-bend", "city": "Hudson Bend", "county": "Travis County",
        "lead": "Hudson Bend reaches out on a peninsula into Lake Travis, all cedar, limestone and lake homes. Waterfront living here comes with scorpions, spiders and wildlife.",
        "angle": "Rock and cedar around lake homes are scorpion habitat, and empty second homes draw rodents. We treat harborage and seal the home tight.",
        "nearby": ["lakeway", "point-venture", "briarcliff"],
    },
    {
        "slug": "johnson-city", "city": "Johnson City", "county": "Blanco County",
        "lead": "Johnson City anchors Blanco County in the Hill Country — ranch land, limestone and small-town homes under big live oaks. Scorpions, rodents and wildlife are simply part of life out here.",
        "angle": "Homes surrounded by ranch land face steady pest and wildlife pressure. We treat the perimeter and outbuildings and seal the house against what the land sends toward it.",
        "nearby": ["blanco", "dripping-springs", "wimberley"],
    },
    {
        "slug": "lakeway", "city": "Lakeway", "county": "Travis County",
        "lead": "Lakeway is the hub of the Lake Travis area — established upscale neighborhoods, golf communities and hillside homes among cedar and limestone. It is prime scorpion and wildlife territory.",
        "angle": "Manicured rock landscaping and cedar greenbelt draw scorpions and wildlife toward the house. Our exclusion-first treatments keep them on the outside.",
        "nearby": ["bee-cave", "hudson-bend", "briarcliff"],
    },
    {
        "slug": "lost-creek", "city": "Lost Creek", "county": "Travis County",
        "lead": "Lost Creek is a wooded, upscale neighborhood on the western edge of Austin, wrapped in greenbelt, live oaks and limestone canyon. That setting brings scorpions, spiders and the occasional wildlife guest.",
        "angle": "Homes against the greenbelt see the pests the wild edge sends their way. We treat the perimeter and seal entry points for lasting control.",
        "nearby": ["west-lake-hills", "barton-creek", "lakeway"],
    },
    {
        "slug": "mustang-ridge", "city": "Mustang Ridge", "county": "Travis County",
        "lead": "Mustang Ridge is a small rural city where Travis, Caldwell and Hays counties meet along the SH-130 corridor, surrounded by farmland and new growth. Open country and fresh building stir pests up.",
        "angle": "Rural acreage brings rodents and wildlife while new development pushes ants and scorpions into fresh homes. We handle the full range from nearby Buda.",
        "nearby": ["creedmoor", "del-valle", "niederwald"],
    },
    {
        "slug": "niederwald", "city": "Niederwald", "county": "Hays County",
        "lead": "Niederwald is a small community spanning the Hays–Caldwell county line east of Kyle, a rural stretch of farmland and scattered homes that is growing with the region. Country living keeps pest and rodent pressure high.",
        "angle": "Farmland and open lots mean rodents, ants and scorpions looking for a way indoors. We treat and seal, timed to the Central Texas seasons.",
        "nearby": ["kyle", "uhland", "buda"],
    },
    {
        "slug": "point-venture", "city": "Point Venture", "county": "Travis County",
        "lead": "Point Venture is a small village on a peninsula in Lake Travis, full of lakeside homes and weekend places among the cedar. Waterfront and second-home living bring scorpions, mosquitoes and rodents.",
        "angle": "Homes that sit empty invite rodents and wildlife, and the lakeside cedar shelters scorpions. We treat, seal and schedule around how you use the place.",
        "nearby": ["briarcliff", "hudson-bend", "lakeway"],
    },
    {
        "slug": "redwood", "city": "Redwood", "county": "Guadalupe County",
        "lead": "Redwood is a community just east of San Marcos in Guadalupe County, a rural-residential stretch along the river bottoms and farmland. Humidity and open land keep mosquitoes, roaches and rodents active.",
        "angle": "River-bottom humidity feeds mosquitoes and roaches while farmland brings rodents. We treat the source and seal the home against them.",
        "nearby": ["san-marcos", "kyle", "uhland"],
    },
    {
        "slug": "sunset-valley", "city": "Sunset Valley", "county": "Travis County",
        "lead": "Sunset Valley is a small city entirely surrounded by South Austin, a leafy enclave of established homes among big trees. Mature landscaping and older foundations give ants, roaches and rodents plenty of ways in.",
        "angle": "Big trees and established homes mean well-worn pest trails. We treat interior and exterior and seal the entry points for lasting results.",
        "nearby": ["austin", "manchaca", "west-lake-hills"],
    },
    {
        "slug": "uhland", "city": "Uhland", "county": "Hays County",
        "lead": "Uhland is a small city on the Hays–Caldwell line between Kyle and San Marcos, a rural community growing along the corridor. Farmland and new lots keep rodents and pests moving toward homes.",
        "angle": "Open country brings rodents and scorpions while new construction stirs up ants. We cover it all from our nearby Buda office.",
        "nearby": ["kyle", "niederwald", "san-marcos"],
    },
    {
        "slug": "west-lake-hills", "city": "West Lake Hills", "county": "Travis County",
        "lead": "West Lake Hills is an upscale community in the hills just west of downtown Austin — limestone, live oaks and established homes on wooded lots. That prized setting is also scorpion and wildlife habitat.",
        "angle": "Rock landscaping, cedar and greenbelt draw scorpions and wildlife toward the house. Our exclusion-first approach treats harborage and seals them out.",
        "nearby": ["lost-creek", "barton-creek", "bee-cave"],
    },
]
LOCATION_BY_SLUG = {l["slug"]: l for l in LOCATIONS}
CITY_SLUG = {l["city"]: l["slug"] for l in LOCATIONS}
PRIORITY_CITY_SLUG = CITY_SLUG  # backwards-compatible alias
# Cities featured on the homepage (the core corridor)
PRIORITY_CITIES = ["buda", "kyle", "san-marcos", "dripping-springs", "wimberley", "driftwood", "manchaca", "del-valle"]

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
        '  <link rel="preconnect" href="https://fonts.googleapis.com">',
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap">',
        '  <link rel="stylesheet" href="/css/styles.css">',
        '  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">',
    ]
    for block in schema_blocks:
        parts.append('  <script type="application/ld+json">')
        parts.append(json.dumps(block, indent=2))
        parts.append('  </script>')
    parts.append('</head>')
    return "\n".join(parts)


def mega_menu():
    cols = ""
    for gname, slugs in MENU_GROUPS:
        items = "".join(
            '<li><a href="/services/%s.html"><span class="mega-emo" aria-hidden="true">%s</span>%s</a></li>'
            % (s, SERVICE_BY_SLUG[s]["icon"], html.escape(SERVICE_BY_SLUG[s]["nav"]))
            for s in slugs
        )
        cols += ('<div class="mega-col"><a class="mega-head" href="/services.html">%s</a><ul>%s</ul></div>'
                 % (html.escape(gname), items))
    return ('<li class="has-mega">'
            '<a href="/services.html" class="mega-toggle" aria-haspopup="true" aria-expanded="false">'
            'Services <span class="caret" aria-hidden="true">▾</span></a>'
            '<div class="mega"><div class="mega-inner">' + cols + '</div></div></li>')


def header():
    parts = []
    for label, url in NAV:
        if label == "Services":
            parts.append("        " + mega_menu())
        else:
            parts.append('        <li><a href="%s">%s</a></li>' % (url, html.escape(label)))
    links = "\n".join(parts)
    return """<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="topbar"><div class="container">
      <span>Family-owned in Buda since {founded} · Licensed &amp; insured · {license}</span>
      <span>Call <a href="tel:{ptel}">{phone}</a> · Text <a href="sms:{ttel}">{text}</a></span>
    </div></div>
    <nav class="navbar" aria-label="Primary"><div class="container">
      <a class="brand" href="/" aria-label="Excel Pest Control — home">
        <span class="brand__mark">EXCEL</span>
        <span class="brand__desc">Pest Control</span>
      </a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
      <ul class="nav-links">
{links}
        <li class="nav-cta">
          <a class="nav-invoice" href="/pay-invoice.html">Pay Invoice</a>
          <a class="btn btn--primary" href="/contact.html">Free estimate</a>
        </li>
      </ul>
    </div></nav>
  </header>
  <div class="mobile-actionbar" aria-label="Quick actions">
    <a class="mab mab--call" href="tel:{ptel}">Call now</a>
    <a class="mab mab--est" href="/contact.html">Free estimate</a>
  </div>""".format(
        founded=BIZ["founded"], license=BIZ["license"], ptel=BIZ["phone_tel"],
        phone=BIZ["phone"], ttel=BIZ["text_tel"], text=BIZ["text"],
        links=links,
    )


def cta_band(heading="Seeing something you shouldn't?", sub="Get a free estimate today — no obligation."):
    return """
  <section class="cta-band">
    <div class="container">
      <div><h2 class="mb-0">{h}</h2><p class="mb-0">{s}</p></div>
      <div class="hero__actions" style="margin:0;">
        <a class="btn btn--primary" href="tel:{ptel}">Call {phone}</a>
        <a class="btn btn--ghost" href="/contact.html">Request Online</a>
      </div>
    </div>
  </section>""".format(h=html.escape(heading), s=html.escape(sub), ptel=BIZ["phone_tel"], phone=BIZ["phone"])


def footer():
    # A curated subset of services in the footer (the full list lives on /services.html)
    footer_service_slugs = ["pest-control", "scorpion-control", "termite-control", "ant-control",
                            "rodent-removal", "wildlife-live-trapping", "mosquito-misting", "lawn-pest-control"]
    svc_links = "\n".join(
        '            <li><a href="/services/%s.html">%s</a></li>'
        % (sl, html.escape(SERVICE_BY_SLUG[sl]["nav"]))
        for sl in footer_service_slugs
    ) + '\n            <li><a href="/services.html"><strong>All services →</strong></a></li>'
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
  <button class="to-top" aria-label="Back to top">↑</button>
  <div class="mobile-bar">
    <a class="mb-call" href="tel:{ptel}">📞 Call Now</a>
    <a class="mb-quote" href="/contact.html">Free Estimate</a>
  </div>
  <script src="/js/main.js"></script>
  <script src="/js/interactive.js"></script>
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


IMG_REGISTRY = []

# Existing business-owned photography used while the full custom photo library is completed.
REMOTE_IMAGES = {
    "services/pest-control-exterior-treatment.webp": "https://le-cdn.hibuwebsites.com/537af7c0228d4470bd70c076341bd233/dms3rep/multi/opt/austin-excel-pest-and-lawn-control-hero-insect-control-1920w.jpg",
    "services/rodent-removal-attic.webp": "https://le-cdn.hibuwebsites.com/537af7c0228d4470bd70c076341bd233/dms3rep/multi/opt/austin-excel-pest-and-lawn-control-hero-rodent-control-1920w.jpg",
    "services/scorpion-hill-country.webp": "https://le-cdn.hibuwebsites.com/537af7c0228d4470bd70c076341bd233/dms3rep/multi/opt/austin-excel-pest-and-lawn-control-hero-scorpion-control-1920w.jpg",
    "services/termite-mud-tubes.webp": "https://le-cdn.hibuwebsites.com/537af7c0228d4470bd70c076341bd233/dms3rep/multi/opt/austin-excel-pest-and-lawn-control-hero-termite-control-1920w.jpg",
    "services/lawn-chinch-bug-damage.webp": "https://le-cdn.hibuwebsites.com/537af7c0228d4470bd70c076341bd233/dms3rep/multi/opt/austin-excel-pest-and-lawn-control-hero-lawn-care-services-1920w.jpg",
}
# Real hero photograph (business-owned) shown behind the home hero scrim.
HOME_HERO_IMG = "https://le-cdn.hibuwebsites.com/537af7c0228d4470bd70c076341bd233/dms3rep/multi/opt/austin-excel-pest-and-lawn-control-hero-home-1920w.jpg"


def scene_svg(alt):
    """A polished, on-brand Central Texas dusk scene used until a real image is dropped in."""
    return (
        '<svg class="slot-art" viewBox="0 0 400 225" preserveAspectRatio="xMidYMid slice" '
        'role="img" aria-label="{alt}" xmlns="http://www.w3.org/2000/svg">'
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#0a1f44"/><stop offset="1" stop-color="#1c3a6e"/></linearGradient></defs>'
        '<rect width="400" height="225" fill="url(#sky)"/>'
        '<circle cx="315" cy="66" r="30" fill="#f26419" opacity="0.92"/>'
        '<path d="M0 165 Q100 128 200 160 T400 150 V225 H0 Z" fill="#12305f"/>'
        '<path d="M0 190 Q120 160 240 185 T400 180 V225 H0 Z" fill="#0c2249"/>'
        '<g fill="#071633"><rect x="72" y="140" width="7" height="42"/>'
        '<circle cx="75" cy="132" r="24"/><circle cx="54" cy="142" r="16"/><circle cx="97" cy="142" r="16"/></g>'
        '<g><rect x="250" y="142" width="66" height="46" fill="#eaf0fa"/>'
        '<path d="M244 144 L283 116 L322 144 Z" fill="#f26419"/>'
        '<rect x="268" y="160" width="15" height="28" fill="#0a1f44"/>'
        '<rect x="293" y="156" width="13" height="13" fill="#0a1f44"/></g>'
        '</svg>'
    ).format(alt=html.escape(alt))


def portrait_svg(alt):
    return (
        '<svg class="slot-art" viewBox="0 0 200 200" role="img" aria-label="{alt}" xmlns="http://www.w3.org/2000/svg">'
        '<rect width="200" height="200" fill="#eef2f9"/>'
        '<circle cx="100" cy="150" r="66" fill="#0a1f44"/>'
        '<circle cx="100" cy="76" r="38" fill="#0a1f44"/>'
        '<circle cx="100" cy="100" r="92" fill="none" stroke="#f26419" stroke-width="6" opacity="0.5"/>'
        '</svg>'
    ).format(alt=html.escape(alt))


# ---------- Hand-built pest silhouette motifs (elegant watermark illustrations) ----------
MOTIFS = {
    "bug": '<g transform="translate(120,66)"><ellipse cx="72" cy="46" rx="48" ry="27"/>'
           '<ellipse cx="26" cy="46" rx="16" ry="13"/><circle cx="5" cy="46" r="10"/>'
           '<g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round">'
           '<path d="M-2 40 q-16 -18 -28 -20"/><path d="M-2 52 q-16 18 -28 20"/>'
           '<path d="M24 32 l-18 -22"/><path d="M42 30 l-8 -28"/><path d="M60 30 l6 -28"/>'
           '<path d="M24 60 l-18 22"/><path d="M42 62 l-8 28"/><path d="M60 62 l6 28"/></g></g>',
    "scorpion": '<g transform="translate(120,52)"><ellipse cx="70" cy="66" rx="40" ry="22"/>'
           '<ellipse cx="26" cy="66" rx="15" ry="11"/>'
           '<path d="M12 60 q-26 -10 -36 2 q12 8 26 6 z"/><path d="M12 72 q-26 10 -36 -2 q12 -8 26 -6 z"/>'
           '<g stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round">'
           '<path d="M46 48 l-12 -20"/><path d="M62 46 l-4 -22"/><path d="M78 46 l6 -22"/>'
           '<path d="M46 84 l-12 20"/><path d="M62 86 l-4 22"/><path d="M78 86 l6 22"/>'
           '<path d="M108 62 q34 -2 46 -28 q6 -18 -8 -30" stroke-width="9"/></g>'
           '<circle cx="146" cy="0" r="8"/></g>',
    "spider": '<g transform="translate(150,52)"><ellipse cx="60" cy="74" rx="30" ry="36"/>'
           '<ellipse cx="60" cy="36" rx="18" ry="16"/>'
           '<g stroke="currentColor" stroke-width="5" fill="none" stroke-linecap="round">'
           '<path d="M46 30 q-40 -16 -62 -36"/><path d="M46 42 q-48 -2 -70 -8"/>'
           '<path d="M46 54 q-48 12 -66 26"/><path d="M46 66 q-42 24 -56 48"/>'
           '<path d="M74 30 q40 -16 62 -36"/><path d="M74 42 q48 -2 70 -8"/>'
           '<path d="M74 54 q48 12 66 26"/><path d="M74 66 q42 24 56 48"/></g></g>',
    "mosquito": '<g transform="translate(110,60)"><ellipse cx="96" cy="72" rx="42" ry="12" transform="rotate(12 96 72)"/>'
           '<circle cx="48" cy="64" r="11"/><path d="M42 64 q-30 -8 -48 -2" stroke="currentColor" stroke-width="3" fill="none"/>'
           '<ellipse cx="100" cy="44" rx="30" ry="11" opacity="0.55" transform="rotate(-18 100 44)"/>'
           '<ellipse cx="112" cy="52" rx="26" ry="9" opacity="0.55" transform="rotate(-6 112 52)"/>'
           '<g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round">'
           '<path d="M74 80 q-6 28 -26 38"/><path d="M92 82 q0 32 -12 46"/><path d="M110 82 q8 30 28 40"/></g></g>',
    "mouse": '<g transform="translate(120,72)"><ellipse cx="86" cy="58" rx="54" ry="34"/>'
           '<circle cx="30" cy="52" r="21"/><circle cx="16" cy="30" r="15"/>'
           '<path d="M138 60 q42 8 62 -18" stroke="currentColor" stroke-width="6" fill="none" stroke-linecap="round"/></g>',
    "raccoon": '<g transform="translate(150,44)"><circle cx="80" cy="82" r="56"/>'
           '<path d="M40 34 q-8 -30 18 -32 q10 12 4 36 z"/><path d="M120 34 q8 -30 -18 -32 q-10 12 -4 36 z"/>'
           '<ellipse cx="80" cy="98" rx="20" ry="15" fill="rgba(0,0,0,.18)"/></g>',
    "leaf": '<g transform="translate(150,44)"><path d="M100 16 C42 38 42 142 100 164 C158 142 158 38 100 16 Z"/>'
           '<path d="M100 28 L100 152" stroke="rgba(0,0,0,.18)" stroke-width="4" fill="none"/>'
           '<path d="M100 60 L74 44 M100 84 L72 70 M100 108 L74 98" stroke="rgba(0,0,0,.14)" stroke-width="3" fill="none"/></g>',
}
SERVICE_MOTIF = {
    "scorpion-control": "scorpion", "spider-control": "spider", "tick-control": "spider",
    "mosquito-misting": "mosquito", "rodent-removal": "mouse", "rodent-exclusion": "mouse",
    "wildlife-live-trapping": "raccoon", "lawn-pest-control": "leaf",
}


def pest_scene(alt, motif="bug", sunx=316, suny=58):
    """A Central Texas dusk scene with a large translucent pest silhouette — one per service."""
    return (
        '<svg class="slot-art" viewBox="0 0 400 225" preserveAspectRatio="xMidYMid slice" '
        'role="img" aria-label="{alt}" xmlns="http://www.w3.org/2000/svg">'
        '<defs><linearGradient id="ps" x1="0" y1="0" x2="0.35" y2="1">'
        '<stop offset="0" stop-color="#0a1f44"/><stop offset="1" stop-color="#1c3a6e"/></linearGradient></defs>'
        '<rect width="400" height="225" fill="url(#ps)"/>'
        '<circle cx="{sx}" cy="{sy}" r="30" fill="#f26419" opacity="0.9"/>'
        '<g fill="rgba(255,255,255,0.16)">{motif}</g>'
        '<path d="M0 176 Q100 140 200 168 T400 158 V225 H0 Z" fill="rgba(255,255,255,0.05)"/>'
        '<path d="M0 196 Q120 168 240 190 T400 184 V225 H0 Z" fill="rgba(0,0,0,0.14)"/>'
        '</svg>'
    ).format(alt=html.escape(alt), sx=sunx, sy=suny, motif=MOTIFS.get(motif, MOTIFS["bug"]))


def img_slot(kind, emo, label, filename, alt, spec, ratio="ratio-wide", page="", art="scene", caption="", svg=None):
    """Render polished placeholder ARTWORK (so pages look finished) and register the slot for the
    image brief. The real filename + spec live in an HTML comment for the dev; kind: 'ai' | 'photo'.
    Pass `svg` to supply custom artwork (e.g. a per-pest illustration)."""
    IMG_REGISTRY.append({"kind": kind, "label": label, "filename": filename, "alt": alt, "spec": spec, "page": page})
    comment = "<!-- IMAGE SLOT ({k}): {fn} — {spec} -->".format(
        k=kind.upper(), fn=filename, spec=spec.replace("--", "—"))
    if svg is not None:
        art_svg = svg
    elif art == "portrait":
        art_svg = portrait_svg(alt)
    else:
        art_svg = scene_svg(alt)
    badge = '' if art == "portrait" else '<span class="slot-badge" aria-hidden="true">%s</span>' % emo
    cap = '<figcaption class="slot-cap">%s</figcaption>' % html.escape(caption) if caption else ''
    real_img = ''
    if filename in REMOTE_IMAGES:
        real_img = '<img src="%s" alt="%s">' % (html.escape(REMOTE_IMAGES[filename], quote=True), html.escape(alt, quote=True))
        art_svg = ''
        badge = ''
    return ('<figure class="img-slot {ratio}" data-filename="{fn}">{comment}{real_img}{art}{badge}{cap}</figure>'
            ).format(ratio=ratio, fn=html.escape(filename), comment=comment, real_img=real_img, art=art_svg, badge=badge, cap=cap)


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

def apply_base(htmltext):
    """Rewrite root-relative URLs and inject window.__BASE__ for a sub-path host.
    A single regex (data-href listed first so it wins over the href substring)
    prefixes each URL exactly once."""
    if not BASE:
        return htmltext
    htmltext = re.sub(r'(data-href|href|src)="/',
                      lambda m: m.group(1) + '="' + BASE + "/", htmltext)
    inject = '<script>window.__BASE__=%s;</script></head>' % json.dumps(BASE)
    return htmltext.replace("</head>", inject, 1)


def write(path, content):
    if path.endswith(".html"):
        content = apply_base(content)
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
    emo, fn, alt, prompt = SERVICE_IMAGES[s["slug"]]
    hero_img = img_slot("ai", emo, alt, "services/" + fn, alt, prompt, ratio="ratio-wide",
                        page="/services/" + s["slug"] + ".html",
                        svg=pest_scene(alt, SERVICE_MOTIF.get(s["slug"], "bug")))
    faqs = SERVICE_FAQS.get(s["slug"], [])
    faq_items = "".join(
        ('<div class="acc-item"><button class="acc-head">{q}<span class="ic" aria-hidden="true">+</span></button>'
         '<div class="acc-body"><div class="acc-body__inner">{a}</div></div></div>').format(q=html.escape(q), a=a)
        for q, a in faqs
    )
    faq_section = ("""
  <section class="section section--soft service-faq">
    <div class="container">
      <div class="section-head text-center" style="margin-bottom:26px;">
        <span class="eyebrow">Good questions</span>
        <h2>{name} — FAQ</h2>
      </div>
      <div class="accordion">{items}</div>
    </div>
  </section>""".format(name=html.escape(s["nav"]), items=faq_items)) if faqs else ""

    body = page_hero(s["h1"], s["desc"].split(". ")[0] + ".", crumbs) + """
  <section class="section" style="padding-bottom:0;">
    <div class="container">{hero_img}</div>
  </section>
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
          <p style="margin:0 0 8px;font-weight:600;">Common issues we treat:</p>
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
  </section>""".format(hero_img=hero_img, lead=s["lead"], sections=sections, treats=treats,
                       ptel=BIZ["phone_tel"], phone=BIZ["phone"])
    body += related_services_grid(s["related"])
    body += faq_section
    body += cta_band()
    schema = [business_schema(), service_schema(s), breadcrumb_schema(crumbs)]
    if faqs:
        import re as _re
        schema.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": _re.sub("<[^>]+>", "", a)}}
                           for q, a in faqs],
        })
    return assemble(s["title"], s["desc"], canonical, body, schema)


def render_location(l):
    canonical = BIZ["domain"] + "/locations/" + l["slug"] + ".html"
    crumbs = [("Home", "/"), ("Service Area", "/service-area.html"), (l["city"], None)]
    title = "Pest Control in %s, TX | Excel Pest since %s" % (l["city"], BIZ["founded"])
    desc = "Family-owned pest, rodent, scorpion and lawn-pest control in %s, %s. Trusted across Central Texas since %s. Free estimates — call %s." % (
        l["city"], l["county"], BIZ["founded"], BIZ["phone"])
    loc_service_slugs = ["pest-control", "scorpion-control", "termite-control", "ant-control",
                         "rodent-removal", "wildlife-live-trapping", "mosquito-misting", "lawn-pest-control"]
    svc_cards = "".join(
        """        <article class="card card--link">
          <div class="card__icon">{icon}</div>
          <h3>{name}</h3>
          <a class="card__link" href="/services/{slug}.html">Learn more →</a>
        </article>""".format(icon=SERVICE_BY_SLUG[sl]["icon"], name=html.escape(SERVICE_BY_SLUG[sl]["nav"]), slug=sl)
        for sl in loc_service_slugs
    )
    loc_alt = "A residential street in " + l["city"] + ", Central Texas"
    loc_img = img_slot("photo", "🏠", loc_alt, "photos/" + l["slug"] + "-local.webp", loc_alt,
                       "Real local photo of a home or street in " + l["city"] + " (client to supply).",
                       ratio="ratio-wide", page="/locations/" + l["slug"] + ".html",
                       svg=scene_svg(loc_alt))
    nearby = "".join(
        '<li><a href="/locations/%s.html">Pest control in %s</a></li>' % (n, html.escape(LOCATION_BY_SLUG[n]["city"]))
        for n in l["nearby"]
    )
    body = page_hero("Pest Control in " + l["city"] + ", Texas", l["county"] + " · Family-owned since " + BIZ["founded"], crumbs) + """
  <section class="section" style="padding-bottom:0;">
    <div class="container">{loc_img}</div>
  </section>
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
        sister_url=BIZ["sister_url"], sister=BIZ["sister_name"], svc_cards=svc_cards, loc_img=loc_img,
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
    def card(s):
        return """        <article class="card card--link">
          <div class="card__icon">{icon}</div>
          <h3>{name}</h3>
          <p>{blurb}</p>
          <a class="card__link" href="/services/{slug}.html">Learn more →</a>
        </article>""".format(icon=s["icon"], name=html.escape(s["nav"]), slug=s["slug"],
                             blurb=html.escape(s["lead"].split(". ")[0] + "."))
    groups_html = ""
    for gname, slugs in MENU_GROUPS:
        cards = "\n".join(card(SERVICE_BY_SLUG[sl]) for sl in slugs)
        groups_html += """
      <div class="section-head" style="margin:36px 0 18px;"><h2>{g}</h2></div>
      <div class="grid grid--4">
{cards}
      </div>""".format(g=html.escape(gname), cards=cards)
    body = page_hero("Our Services", "One local crew for pests, rodents, wildlife and lawn insects across Central Texas.", crumbs) + """
  <section class="section">
    <div class="container">{groups}
      <div style="margin-top:32px;">{cross}</div>
    </div>
  </section>""".format(groups=groups_html, cross=crosslink_block())
    body += cta_band()
    schema = [business_schema(), breadcrumb_schema(crumbs)]
    desc = "Pest control, scorpion, termite, rodent, wildlife, mosquito and lawn-pest control across Buda and Central Texas. Family-owned since 1998. Call (737) 201-3059."
    return assemble("Pest Control Services in Buda & Central Texas | Excel Pest", desc, canonical, body, schema)


def service_area_hub():
    canonical = BIZ["domain"] + "/service-area.html"
    crumbs = [("Home", "/"), ("Service Area", None)]
    items = "\n        ".join(
        '<li><a href="/locations/%s.html">%s</a></li>' % (CITY_SLUG[c], html.escape(c))
        for c in ALL_CITIES
    )
    # Schematic coverage pins (angle/radius around the Buda HQ — stylised, not to scale)
    pins = [
        ("Buda", 0, 0, True), ("Kyle", 200, 62, False), ("San Marcos", 205, 128, False),
        ("Wimberley", 250, 150, False), ("Dripping Springs", 300, 120, False),
        ("Driftwood", 265, 95, False), ("Manchaca", 25, 70, False), ("Austin", 350, 110, False),
        ("West Lake Hills", 330, 150, False), ("Bee Cave", 315, 175, False),
        ("Lakeway", 335, 200, False), ("Del Valle", 60, 120, False), ("Canyon Lake", 225, 205, False),
    ]
    pin_html = ""
    for name, ang, dist, hq in pins:
        if hq:
            pin_html += '\n        <span class="cov-hq">%s<small>HQ</small></span>' % html.escape(name)
        else:
            import math as _m
            x = 50 + (dist / 4.2) * _m.cos(_m.radians(ang))
            y = 50 + (dist / 4.2) * _m.sin(_m.radians(ang))
            slug = CITY_SLUG.get(name, "")
            pin_html += '\n        <a class="cov-pin" style="left:%.1f%%;top:%.1f%%" href="/locations/%s.html"><span class="dot"></span>%s</a>' % (x, y, slug, html.escape(name))
    body = page_hero("Service Area — 27 Central Texas Cities", "From South Austin through Hays County and into the Hill Country.", crumbs) + """
  <section class="section">
    <div class="container">
      <div class="coverage">
        <div class="coverage__map" role="img" aria-label="Coverage centered on our Buda headquarters, reaching across Hays and Travis counties and into the Hill Country">
          <span class="cov-ring r1"></span><span class="cov-ring r2"></span><span class="cov-ring r3"></span>{pins}
          <span class="cov-scale">Schematic · centered on our Buda HQ</span>
        </div>
        <div class="coverage__copy">
          <span class="eyebrow">Do we serve you?</span>
          <h2 class="mt-0">Check your city in one tap</h2>
          <p>We have covered this ground since {founded} — a core corridor of Buda–Kyle–Plum Creek–Dripping
             Springs–Wimberley–South Austin, reaching west into the Hill Country and south to San Marcos.</p>
          <form class="checker" data-checker data-cities='{cities}' style="max-width:none;">
            <div class="checker__row">
              <input type="text" placeholder="e.g. Kyle, Dripping Springs, 78610" aria-label="Your city or ZIP code">
              <button type="submit" class="btn btn--primary" data-checker-go>Check</button>
            </div>
            <div class="checker__result" role="status" aria-live="polite"></div>
          </form>
        </div>
      </div>

      <h2 style="margin-top:56px;">All 27 cities we serve</h2>
      <ul class="city-grid">
        {grid}
      </ul>
      <p style="margin-top:16px;color:var(--muted);">Every city links to its own local page. Not sure if we reach
         you? <a href="/contact.html">Ask us</a> — if you are in or near Hays or Travis County, we probably do.</p>
    </div>
  </section>""".format(founded=BIZ["founded"], grid=items, pins=pin_html,
                       cities=json.dumps([{"name": c, "slug": CITY_SLUG.get(c, "")} for c in ALL_CITIES]))
    body += cta_band()
    schema = [business_schema(), breadcrumb_schema(crumbs)]
    desc = "Excel Pest serves 27 Central Texas cities — Buda, Kyle, San Marcos, Dripping Springs, Wimberley and more. Family-owned since 1998. Call (737) 201-3059."
    return assemble("Service Area — Pest Control Across Central Texas | Excel Pest", desc, canonical, body, schema)


PESTS = [
    {"emo": "🦂", "name": "Scorpions", "href": "/services/scorpion-control.html", "cta": "See scorpion control",
     "signs": "Sightings in bathtubs, closets and along baseboards, especially after rain or drought.",
     "desc": "The striped bark scorpion thrives in Hill Country limestone and slips inside through tiny gaps. We treat harborage and seal them out."},
    {"emo": "🐜", "name": "Ants", "href": "/services/ant-control.html", "cta": "See ant control",
     "signs": "Trails along counters and foundations, mounds in the yard, or ants around pet bowls.",
     "desc": "Central Texas ants range from nuisance trails to fire ants. We treat the colony at the source, inside and out."},
    {"emo": "🪳", "name": "Cockroaches", "href": "/services/cockroach-control.html", "cta": "See cockroach control",
     "signs": "Roaches at night in the kitchen or bath, egg cases, or a musty odor.",
     "desc": "Roaches love our warm, humid stretches. Our treatments target where they hide and breed, not just where you see them."},
    {"emo": "🐀", "name": "Rodents", "href": "/services/rodent-removal.html", "cta": "See rodent control",
     "signs": "Droppings, gnaw marks, scratching in the attic or walls at night.",
     "desc": "Rats and mice chew wiring and foul insulation. We remove them and seal the entry points so they don't return."},
    {"emo": "🪵", "name": "Termites", "href": "/services/termite-control.html", "cta": "See termite control",
     "signs": "Mud tubes on the foundation, hollow-sounding wood, or a swarm after spring rain.",
     "desc": "Subterranean termites work out of sight for years. A licensed inspection tells you where you stand — and we treat and warranty it."},
    {"emo": "🕷️", "name": "Spiders", "href": "/services/spider-control.html", "cta": "See spider control",
     "signs": "Webs in corners, garages and eaves; egg sacs; more sightings in fall.",
     "desc": "Spiders follow other insects indoors. Our exterior barrier reduces the prey that draws them in."},
    {"emo": "🦟", "name": "Mosquitoes", "href": "/services/mosquito-misting.html", "cta": "See mosquito control",
     "signs": "Bites at dusk, swarms near standing water, a backyard you can't use.",
     "desc": "We treat breeding sites and install misting systems that keep the yard usable all season."},
    {"emo": "🦝", "name": "Wildlife", "href": "/services/wildlife-live-trapping.html", "cta": "See wildlife removal",
     "signs": "Noises in the attic, torn soffits or vents, animals under the deck.",
     "desc": "Raccoons, squirrels and opossums treat homes like hollow trees. We remove them humanely and close the entry points."},
    {"emo": "🌱", "name": "Lawn pests", "href": "/services/lawn-pest-control.html", "cta": "See lawn pest control",
     "signs": "Spreading brown patches, spongy turf, or moths lifting off the grass at dusk.",
     "desc": "Chinch bugs, grubs and armyworms damage turf from below. We diagnose the real cause and treat it."},
]


def stat_band():
    # Static proof strip — no count-up animation, no clipping. Figures verified against BIZ.
    return """
  <section class="statband"><div class="container">
    <div><div class="stat__num">Since 1998</div><div class="stat__lbl">Family-owned in Buda</div></div>
    <div><div class="stat__num">5.0<span class="stat__u">&#9733;</span></div><div class="stat__lbl">Google rating, 41 reviews</div></div>
    <div><div class="stat__num">27</div><div class="stat__lbl">Central Texas cities served</div></div>
    <div><div class="stat__num">A+</div><div class="stat__lbl">BBB accredited &middot; insured</div></div>
  </div></section>"""


def pest_identifier():
    buttons = "\n".join(
        '        <button class="pest-btn" aria-pressed="false" data-emo="{emo}" data-name="{name}" '
        'data-signs="{signs}" data-desc="{desc}" data-href="{href}" data-cta="{cta}">'
        '<span class="emo">{emo}</span>{name}</button>'.format(
            emo=p["emo"], name=html.escape(p["name"]), signs=html.escape(p["signs"]),
            desc=html.escape(p["desc"]), href=p["href"], cta=html.escape(p["cta"]))
        for p in PESTS
    )
    return """
  <section class="section">
    <div class="container">
      <div class="section-head text-center" style="max-width:660px;margin:0 auto 34px;">
        <span class="eyebrow">Find your pest</span>
        <h2>What's bugging you?</h2>
        <p class="lead">Tap what you're seeing — we'll show you the signs and the fix.</p>
      </div>
      <div class="identifier">
        <div class="pest-grid" data-pest-grid>
{buttons}
        </div>
        <div class="pest-panel" data-pest-panel aria-live="polite"></div>
      </div>
    </div>
  </section>""".format(buttons=buttons)


def area_checker():
    cities_json = json.dumps([{"name": c, "slug": PRIORITY_CITY_SLUG.get(c, "")} for c in ALL_CITIES])
    return """
  <section class="section section--soft">
    <div class="container text-center">
      <span class="eyebrow">Do we serve you?</span>
      <h2>Check your city in one tap</h2>
      <p class="lead" style="max-width:640px;margin:0 auto 22px;">Type your city or ZIP for an instant answer —
         we cover 27 Central Texas cities.</p>
      <form class="checker" data-checker data-cities='{cities}'>
        <div class="checker__row">
          <input type="text" placeholder="e.g. Kyle, Dripping Springs, 78610" aria-label="Your city or ZIP code">
          <button type="submit" class="btn btn--primary" data-checker-go>Check coverage</button>
        </div>
        <div class="checker__result" role="status" aria-live="polite"></div>
      </form>
    </div>
  </section>""".format(cities=cities_json)


# Restrained monoline icons (no emoji) for the home service cards.
_IC = ('<svg class="svc-ic" viewBox="0 0 32 32" fill="none" stroke="currentColor" '
       'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>')
CORE_ICONS = {
    # General pest — house under a shield
    "pest-control": _IC % '<path d="M16 3l10 4v7c0 6-4 10-10 12C10 24 6 20 6 14V7z"/><path d="M12 15l3 3 5-6"/>',
    # Termites — timber beam with grain
    "termite-control": _IC % '<rect x="5" y="10" width="22" height="12" rx="1.5"/><path d="M9 14h9M9 18h6M22 13v6"/>',
    # Rodents & exclusion — home with a sealed gap
    "rodent-exclusion": _IC % '<path d="M5 15l11-8 11 8"/><path d="M8 14v11h16V14"/><path d="M13 25v-6h6v6"/><circle cx="16" cy="16.5" r="1"/>',
    # Wildlife — humane leaf/paw
    "wildlife-live-trapping": _IC % '<path d="M25 7C15 7 8 13 8 22c0 2 1 3 3 3 9 0 15-7 15-16 0-1-.4-2-1-2z"/><path d="M8 25c3-6 8-10 14-12"/>',
    # Scorpions — pincers/tail motif
    "scorpion-control": _IC % '<path d="M6 10c3 0 4 2 6 4s5 2 8 0 5-6 6-4"/><path d="M26 10l-3-1M26 10l-1 3"/><path d="M9 9L6 10l1 3M17 14l-2 3M20 14l1 4"/>',
    # Mosquitoes — droplet + wings
    "mosquito-misting": _IC % '<path d="M16 6c4 5 6 8 6 11a6 6 0 01-12 0c0-3 2-6 6-11z"/><path d="M13 17c-3-2-6-2-8 0M19 17c3-2 6-2 8 0"/>',
}
CORE_HOME = ["pest-control", "termite-control", "rodent-exclusion",
             "wildlife-live-trapping", "scorpion-control", "mosquito-misting"]
CORE_BLURB = {
    "pest-control": "Recurring, water-based treatment for ants, roaches, spiders and the everyday pests that get inside.",
    "termite-control": "Licensed inspections, targeted treatment and a warranty for the termites working out of sight.",
    "rodent-exclusion": "Trap the rats and mice, then seal the entry points so they can't come back.",
    "wildlife-live-trapping": "Humane removal of raccoons, squirrels and possums — then we close the way in.",
    "scorpion-control": "Harborage treatment and exclusion for the striped bark scorpions that thrive in Hill Country limestone.",
    "mosquito-misting": "Treat the breeding sites and install misting systems that keep the backyard usable all season.",
}


def home():
    canonical = BIZ["domain"] + "/"
    core_names = {
        "pest-control": "General Pest Control", "termite-control": "Termite Control",
        "rodent-exclusion": "Rodents &amp; Exclusion", "wildlife-live-trapping": "Wildlife Removal",
        "scorpion-control": "Scorpion Control", "mosquito-misting": "Mosquito Control",
    }
    svc_cards = "".join("""        <article class="card card--link svc-card">
          <div class="svc-card__ic">{icon}</div>
          <h3>{name}</h3>
          <p>{blurb}</p>
          <a class="card__link" href="/services/{slug}.html">Learn more &rarr;</a>
        </article>""".format(icon=CORE_ICONS[slug], name=core_names[slug], slug=slug,
                             blurb=html.escape(CORE_BLURB[slug]))
        for slug in CORE_HOME)
    city_links = " · ".join('<a href="/locations/%s.html">%s</a>' % (LOCATION_BY_SLUG[s]["slug"], html.escape(LOCATION_BY_SLUG[s]["city"])) for s in PRIORITY_CITIES)
    spotlight = """
        <div class="spotlight" data-spotlight>
          <div class="stars">★★★★★</div>
          <div class="spotlight__slide on">
            <blockquote class="spotlight__q">"Been with this company for 30+ years."</blockquote>
            <cite>— Karla Mathews</cite><div class="meta">Google review · 2026</div>
          </div>
          <div class="spotlight__slide">
            <blockquote class="spotlight__q">"We have used Excel Pest / Research Turf for 13+ years — pergola,
               patio, masonry, tree trimming, plus regular lawn care."</blockquote>
            <cite>— Judy Buck</cite><div class="meta">Google review · 2026</div>
          </div>
          <div class="spotlight__dots" aria-label="Choose a review"></div>
          <a class="card__link" href="/reviews.html" style="display:inline-block;margin-top:16px;">Read more reviews →</a>
        </div>"""
    flow = """
  <section class="section">
    <div class="container">
      <div class="section-head text-center" style="max-width:620px;margin:0 auto 34px;">
        <span class="eyebrow">Simple from the first call</span>
        <h2>How it works</h2>
      </div>
      <div class="flow">
        <div class="step"><div class="step__num">1</div><h3>Free estimate</h3>
          <p class="mb-0">Call or text and we assess the problem and give you a clear quote — no pressure, no surprise pricing.</p></div>
        <div class="step"><div class="step__num">2</div><h3>Targeted treatment</h3>
          <p class="mb-0">A local technician treats the source inside and out with water-based products, safe for family and pets.</p></div>
        <div class="step"><div class="step__num">3</div><h3>Keep them out</h3>
          <p class="mb-0">We seal entry points and set a schedule that fits your home, backed by our warranty.</p></div>
      </div>
    </div>
  </section>"""
    gallery = """
  <section class="section section--soft">
    <div class="container">
      <div class="section-head text-center" style="max-width:660px;margin:0 auto 34px;">
        <span class="eyebrow">Why homeowners choose us</span>
        <h2>Local expertise you can actually trust</h2>
        <p class="lead">Twenty-eight years, one owner, and a 5.0 rating — the things a national franchise can't copy.</p>
      </div>
      <div class="grid grid--3">
        <div class="card"><div class="card__icon">🛡️</div><h3>Licensed &amp; insured</h3>
          <p class="mb-0">Texas {license}, with continuous annual technician education — the same trained techs on every visit, not a rotating call center.</p></div>
        <div class="card"><div class="card__icon">🐾</div><h3>Safe for family &amp; pets</h3>
          <p class="mb-0">Water-based products applied only where needed. See our <a href="/pet-family-safety.html">pet &amp; family safety</a> approach.</p></div>
        <div class="card"><div class="card__icon">📍</div><h3>Local since {founded}</h3>
          <p class="mb-0">Family-owned in Buda, 5.0★ across {reviews} reviews. We know the Central Texas pest calendar because we live it.</p></div>
      </div>
    </div>
  </section>""".format(license=BIZ["license"], founded=BIZ["founded"], reviews=BIZ["reviews"])
    body = """
  <section class="hero">
    <div class="hero-photo" aria-hidden="true" style="background-image:url('{hero_img}')"></div>
    <div class="hero-scrim" aria-hidden="true"></div>
    <div class="container">
      <span class="eyebrow">The crew Buda has trusted since {founded}</span>
      <h1>Family-owned pest control for Central Texas.</h1>
      <p>Pest, rodent, wildlife and mosquito control by the same local crew since {founded} —
         water-based products chosen for your family and your four-legged family members.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="/contact.html">Request a free estimate</a>
        <span class="hero__call">or call <a href="tel:{ptel}">{phone}</a></span>
      </div>
      <div class="badges">
        <span class="badge">5.0&#9733; · {reviews} Google reviews</span>
        <span class="badge">BBB A+ accredited</span>
        <span class="badge">Licensed &amp; insured · {license}</span>
      </div>
    </div>
  </section>
{statband}

  <main id="main">
  <section class="section">
    <div class="container">
      <div class="section-head" style="max-width:640px;margin:0 auto 40px;text-align:center;">
        <span class="eyebrow">What we do</span>
        <h2>Core services for Central Texas homes</h2>
        <p class="lead">The problems we get called for most — handled by a licensed local technician, inside and out.</p>
      </div>
      <div class="grid grid--3">
{svc_cards}
      </div>
      <div class="text-center" style="margin-top:34px;">
        <a class="btn btn--outline" href="/services.html">View all services &rarr;</a>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container split">
      <div>
        <span class="eyebrow">28 years, one owner</span>
        <h2>Not a franchise — the crew that knows Central Texas.</h2>
        <p>{owner} started Excel Pest in {founded} and has run it ever since. We know the local
           pest calendar — when scorpions move indoors, when chinch bugs cook a lawn, when rodents look for a warm
           attic — because we have worked this ground for more than 25 years. Nobody in this market beats our
           5.0 rating; we just earn it quietly, one neighbor at a time.</p>
        <a class="btn btn--outline" href="/about.html">Read our story</a>
      </div>
      <div>
        <div class="why-panel">
          <h3>Why homeowners choose us</h3>
          <ul class="why-list">
            <li><strong>Licensed &amp; insured.</strong> Texas {license}, with the same trained techs on every visit — not a rotating call center.</li>
            <li><strong>Safe for family &amp; pets.</strong> Water-based products applied only where needed. See our <a href="/pet-family-safety.html">safety approach</a>.</li>
            <li><strong>Local since {founded}.</strong> Family-owned in Buda, 5.0&#9733; across {reviews} reviews. We live the Central Texas pest calendar.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
{flow}

  <section class="section">
    <div class="container">
      <div class="section-head" style="max-width:560px;margin:0 auto 30px;text-align:center;">
        <span class="eyebrow">In their words</span>
        <h2>Reviewed 5.0 by Central Texas neighbors</h2>
      </div>
      <div style="max-width:680px;margin:0 auto;">
{spotlight}
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container text-center">
      <span class="eyebrow">Local coverage</span>
      <h2>Serving 27 cities across the corridor</h2>
      <p class="lead" style="max-width:720px;margin:0 auto 18px;">From South Austin through Hays County and into
         the Hill Country:</p>
      <p style="font-size:1.02rem;line-height:2;">{city_links}</p>
      <a class="btn btn--outline" href="/service-area.html">See all 27 cities &rarr;</a>
    </div>
  </section>

  <section class="section">
    <div class="container">{cross}</div>
  </section>
  </main>""".format(
        founded=BIZ["founded"], ptel=BIZ["phone_tel"], phone=BIZ["phone"],
        reviews=BIZ["reviews"], license=BIZ["license"], svc_cards=svc_cards, owner=BIZ["owner"],
        city_links=city_links, cross=crosslink_block(), statband=stat_band(),
        spotlight=spotlight, flow=flow, hero_img=HOME_HERO_IMG,
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
        {owner_photo}
        <p style="text-align:center;font-size:.85rem;color:var(--muted);margin:8px 0 0;">{owner}, owner since {founded}</p>
        <div class="card" style="margin-top:18px;">
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
        <div style="margin-top:18px;">{mgr_photo}
          <p style="text-align:center;font-size:.85rem;color:var(--muted);margin:8px 0 0;">{mgr}, Director of Office Operations</p>
        </div>
      </div>
    </div>
  </section>""".format(
        owner=BIZ["owner"], founded=BIZ["founded"], sister_url=BIZ["sister_url"], street=BIZ["street"],
        city=BIZ["city"], mgr=BIZ["office_mgr"], reviews=BIZ["reviews"], license=BIZ["license"],
        rating=BIZ["rating"],
        owner_photo=img_slot("photo", "🧑‍🔧", "Owner Gye Hutson", "photos/gye-hutson.webp",
                             "Gye Hutson, owner of Excel Pest & Lawn Control",
                             "Real portrait photo of owner Gye Hutson (client to supply).",
                             ratio="ratio-square", page="/about.html", art="portrait"),
        mgr_photo=img_slot("photo", "👩‍💼", "Megan Avery", "photos/megan-avery.webp",
                           "Megan Avery, Director of Office Operations",
                           "Real photo of Megan Avery, Director of Office Operations (client to supply).",
                           ratio="ratio-square", page="/about.html", art="portrait"),
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
        """
        <div class="acc-item">
          <button class="acc-head">{q}<span class="ic" aria-hidden="true">+</span></button>
          <div class="acc-body"><div class="acc-body__inner">{a}</div></div>
        </div>""".format(q=html.escape(q), a=a)
        for q, a in FAQS
    )
    body = page_hero("Frequently Asked Questions", "Quick answers about our Central Texas pest control.", crumbs) + """
  <section class="section">
    <div class="container">
      <div class="accordion">
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
    city_opts = "".join('<option value="%s"></option>' % html.escape(c) for c in ALL_CITIES)
    pest_choices = "".join(
        '<label><input type="radio" name="pest" value="{v}"><span>{e} {v}</span></label>'.format(v=v, e=e)
        for e, v in [("🦂","Scorpions"),("🐜","Ants"),("🪳","Roaches"),("🐀","Rodents"),
                     ("🪵","Termites"),("🦝","Wildlife"),("🦟","Mosquitoes"),("🌱","Lawn pests")]
    )
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
          <form action="mailto:{email}" method="post" class="wizard" data-estimate data-wizard novalidate>
            <div class="wiz-prog"><span data-wiz-fill></span></div>
            <div class="wiz-count" data-wiz-count>Step 1 of 3</div>

            <fieldset class="wiz-step active" data-step="0">
              <div class="field"><label for="service">What do you need help with?</label>
                <select id="service" name="service">{options}<option>Not sure / other</option></select></div>
              <div class="field"><label>Seeing something specific? <span style="font-weight:400;color:var(--muted);">(optional)</span></label>
                <div class="pest-choice">{pest_choices}</div></div>
              <div class="wiz-nav"><span></span><button type="button" class="btn btn--primary" data-wiz-next>Next →</button></div>
            </fieldset>

            <fieldset class="wiz-step" data-step="1">
              <div class="field"><label for="name">Name</label>
                <input id="name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="phone">Phone</label>
                <input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
              <div class="field"><label for="email">Email <span style="font-weight:400;color:var(--muted);">(optional)</span></label>
                <input id="email" name="email" type="email" autocomplete="email"></div>
              <div class="wiz-nav"><button type="button" class="btn btn--outline" data-wiz-back>← Back</button>
                <button type="button" class="btn btn--primary" data-wiz-next>Next →</button></div>
            </fieldset>

            <fieldset class="wiz-step" data-step="2">
              <div class="field"><label for="city">Your city</label>
                <input id="city" name="city" type="text" list="city-list" autocomplete="address-level2" placeholder="e.g. Kyle">
                <datalist id="city-list">{city_opts}</datalist></div>
              <div class="field"><label for="message">Anything else we should know?</label>
                <textarea id="message" name="message" rows="3"></textarea></div>
              <div class="wiz-review" data-wiz-review></div>
              <div class="wiz-nav"><button type="button" class="btn btn--outline" data-wiz-back>← Back</button>
                <button class="btn btn--primary" type="submit">Send Request</button></div>
            </fieldset>

            <p class="hero__note" style="color:var(--muted);" data-form-note>By submitting, you agree to be contacted about your request.</p>
          </form>
        </div>
      </div>
    </div>
  </section>""".format(
        ptel=BIZ["phone_tel"], phone=BIZ["phone"], ttel=BIZ["text_tel"], text=BIZ["text"], email=BIZ["email"],
        street=BIZ["street"], city=BIZ["city"], state=BIZ["state"], zip=BIZ["zip"], license=BIZ["license"],
        sister_url=BIZ["sister_url"], sister=BIZ["sister_name"], sister_phone=BIZ["sister_phone"], options=options,
        pest_choices=pest_choices, city_opts=city_opts,
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

    # Image brief (outside ./site — it's documentation, not a served page)
    write_image_brief()

    print("Generated %d files:" % len(written))
    for p in written:
        print("  " + p)
    print("Image slots registered: %d (see docs/IMAGE-BRIEF.md)" % len(IMG_REGISTRY))


# Real photos to request from the client that aren't tied to a single on-page slot
# (the homepage now uses a trust band instead of empty photo boxes, but the client
# should still gather these for future galleries / social / the About page).
REAL_PHOTO_REQUESTS = [
    {"kind": "photo", "label": "Crew on the job", "filename": "photos/crew-on-site.webp",
     "alt": "The Excel Pest crew working at a Central Texas home",
     "spec": "Real photo of the crew on a job — outdoors at a Buda-area home if possible.", "page": "future gallery"},
    {"kind": "photo", "label": "Branded service truck", "filename": "photos/service-truck.webp",
     "alt": "Excel Pest & Lawn Control service truck",
     "spec": "Real photo of a branded service truck.", "page": "future gallery"},
    {"kind": "photo", "label": "Finished / protected home", "filename": "photos/finished-home.webp",
     "alt": "A Central Texas home Excel Pest protects",
     "spec": "Real photo of a completed job or protected home.", "page": "future gallery"},
    {"kind": "photo", "label": "Technician (e.g. Tim) at work", "filename": "photos/technician.webp",
     "alt": "An Excel Pest technician treating a home",
     "spec": "Real photo of a named technician at work (reviews mention Tim).", "page": "future gallery"},
]


def write_image_brief():
    ai = [i for i in IMG_REGISTRY if i["kind"] == "ai"]
    photo = [i for i in IMG_REGISTRY if i["kind"] == "photo"] + REAL_PHOTO_REQUESTS
    lines = [
        "# Image Brief — Austin Excel Pest & Lawn Control",
        "",
        "Auto-generated by `tools/build.py`. Every image slot on the site is listed here with its",
        "filename, alt text, and either a ChatGPT generation prompt (AI) or a real-photo requirement.",
        "",
        "**Workflow (from the brief):** generate or shoot → save with the exact filename → convert to",
        "WebP and compress → drop into `site/` at the path shown → the styled placeholder is replaced.",
        "Every image must keep its alt text. Never AI-generate real people, trucks, or completed jobs.",
        "",
        "## Real photos to request from the client (%d)" % len(photo),
        "",
        "These must be genuine photographs — do not generate them.",
        "",
    ]
    for i in photo:
        lines += [
            "### %s" % i["label"],
            "- **File:** `site/%s`" % i["filename"],
            "- **Alt text:** %s" % i["alt"],
            "- **Used on:** %s" % (i["page"] or "—"),
            "- **Requirement:** %s" % i["spec"],
            "",
        ]
    lines += ["## AI images to generate in ChatGPT (%d)" % len(ai), "",
              "Paste each prompt as-is. Regenerate if the result shows text, a logo, a watermark, or a",
              "place that does not look like Central Texas.", ""]
    for i in ai:
        lines += [
            "### %s" % i["label"],
            "- **File:** `site/%s`" % i["filename"],
            "- **Alt text:** %s" % i["alt"],
            "- **Used on:** %s" % (i["page"] or "—"),
            "- **Prompt:**",
            "  > %s" % i["spec"],
            "",
        ]
    path = os.path.join(ROOT, "docs", "IMAGE-BRIEF.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
