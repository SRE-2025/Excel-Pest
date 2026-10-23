"""Discovery and conversion content using only Excel's current service menu."""
import html

LIBRARY = [
    ("ants", "Ants & fire ants", "ant-control",
     "Trails near food, activity around pet bowls, or mounds in the yard.",
     "Note where the trail starts and whether the problem is indoors or outside. Store food in sealed containers and keep people and pets away from active fire-ant mounds. Identification matters: the right approach depends on the ant, the colony and the site.",
     "fire-ants-central-texas-yard", "Fire ants in a Central Texas yard"),
    ("cockroaches", "Cockroaches", "cockroach-control",
     "Repeated kitchen or bathroom sightings, egg cases, or dark specks near hiding places.",
     "Record the room, time and approximate size of the insect. Address leaks and food residue, and reduce cardboard clutter. A single outdoor visitor and a recurring indoor population need different assessments; a photo can help the technician distinguish them.",
     "cockroaches-central-texas-kitchen", "What to do about kitchen cockroaches"),
    ("crickets", "Crickets", "cricket-control",
     "Chirping indoors or crickets gathering near exterior lights and garage doors.",
     "Check door sweeps, screens and gaps around the garage. Note which entrance has the most activity and whether lights attract insects there. Avoid leaving doors open while investigating. Recurring indoor sightings are useful information for an inspection.", "", ""),
    ("fleas-ticks", "Fleas & ticks", "flea-tick-control",
     "Small jumping insects, repeated pet scratching, or ticks found after time outdoors.",
     "Keep a record of where the problem appears: bedding, carpet, a shaded yard or a fence line. Vacuum and wash washable pet bedding. Coordinate any animal treatment with your veterinarian; Excel's service addresses the home and yard, not veterinary care.", "", ""),
    ("scorpions", "Scorpions", "scorpion-control",
     "A scorpion in a garage, closet, bathroom or near stored materials.",
     "Do not handle it. Note the location and check nearby door gaps, stacked materials and clutter. Reducing shelter around the home and addressing entry points are part of a practical prevention plan. Hill Country homes can have repeated outdoor pressure even after one sighting is resolved.",
     "keep-scorpions-out-central-texas-home", "Keeping scorpions out of the home"),
    ("spiders", "Spiders", "spider-control",
     "Repeated webs, egg sacs or spider sightings around eaves, garages and storage areas.",
     "A web or bite-like mark alone does not establish the species. Photograph from a distance and describe the location. Reduce clutter and check screens. An inspection can consider both the spiders and the other insects that attract them.", "", ""),
    ("rodents", "Rats & mice", "rodent-removal",
     "Gnaw marks, droppings, damaged packaging or repeated movement in an attic or wall.",
     "Keep food and pet feed sealed, and record where activity occurs. Do not handle droppings or climb into an unsafe attic. Removal and entry-point repairs are separate parts of the discussion: ask which openings were found and what follow-up is recommended.",
     "signs-of-rats-in-central-texas-attic", "Signs of rats in an attic"),
    ("mosquitoes", "Mosquitoes", "mosquito-misting",
     "Persistent mosquito activity near seating areas, containers or shaded parts of the yard.",
     "Walk the yard after rain and irrigation to look for standing water. Empty containers, clear drainage and check screens. For a property assessment, note the spaces you use most and any existing misting equipment. Equipment and maintenance needs depend on the yard.",
     "reduce-mosquitoes-central-texas-backyard", "A backyard mosquito checklist"),
    ("wildlife", "Raccoons, squirrels & opossums", "wildlife-live-trapping",
     "An animal entering an attic, soffit or space beneath a deck, or fresh damage at an opening.",
     "These are the wildlife animals listed in Excel's current service offering. Keep your distance, note where the animal enters, and avoid closing an occupied opening yourself. Describe the animal and location when requesting live trapping and an entry-point assessment.", "", ""),
    ("lawn-pests", "Lawn pests", "lawn-pest-control",
     "Expanding brown patches, thinning turf or visible insects in damaged grass.",
     "Brown grass alone does not establish an insect problem. Record when damage appeared, irrigation changes and the grass type if known. Excel's lawn-pest service lists chinch bugs, white grubs and armyworms; an assessment helps distinguish insects from other turf problems.", "", ""),
]

CALENDAR = [
    ("January", "Check stored items and rodent access", "Inspect accessible garage storage and look for fresh gnawing or droppings. Record activity rather than entering an unsafe attic.", "rodent-removal"),
    ("February", "Prepare the home's exterior", "Check worn door sweeps and accessible vent screens. Ask about rodent exclusion if there has been recurring attic activity.", "rodent-exclusion"),
    ("March", "Watch ant trails and outdoor water", "As conditions warm, walk the foundation and yard. Note ant activity and empty containers that collect rain or irrigation water.", "ant-control"),
    ("April", "Check outdoor gathering spaces", "Inspect patio drainage, plant saucers and gutters. Discuss mosquito misting needs before relying on the yard for regular gatherings.", "mosquito-misting"),
    ("May", "Revisit the yard after rain", "Look for active ant mounds and new standing water. Keep children and pets away from mounds; ask about a property-specific treatment plan.", "ant-control"),
    ("June", "Reduce hiding places near the house", "Organize stored materials and check gaps around exterior doors. Note scorpion sightings and the rooms where they occur.", "scorpion-control"),
    ("July", "Look closely at damaged turf", "Photograph expanding brown patches and note watering changes. Ask for diagnosis before assuming heat stress or applying a lawn-pest product.", "lawn-pest-control"),
    ("August", "Check garage and doorway entry points", "Review screens and door sweeps where insects gather. Note cricket activity near lights and entrances for your next service visit.", "cricket-control"),
    ("September", "Review food, moisture and storage", "Check kitchen leaks, food storage and cardboard clutter. Recurring roach sightings warrant identification and inspection, regardless of month.", "cockroach-control"),
    ("October", "Plan for attic and garage prevention", "Walk the exterior from ground level and look for damaged vents or roofline openings. Repeated noises are a reason to request a rodent assessment.", "rodent-exclusion"),
    ("November", "Check decorations before bringing them inside", "Inspect accessible storage containers and keep pet food secured. Report fresh animal activity or entry damage without approaching wildlife.", "wildlife-live-trapping"),
    ("December", "Review the year's recurring problems", "Compare notes on sightings and previous visits. Ask which preventive tasks and service intervals fit your home for the coming year.", "pest-control"),
]

GUIDE_MAP = {
    "pest-control": ["central-texas-pest-calendar", "cockroaches-central-texas-kitchen"],
    "scorpion-control": ["keep-scorpions-out-central-texas-home", "when-are-scorpions-most-active-central-texas"],
    "rodent-removal": ["signs-of-rats-in-central-texas-attic"],
    "rodent-exclusion": ["signs-of-rats-in-central-texas-attic"],
    "mosquito-misting": ["reduce-mosquitoes-central-texas-backyard"],
    "ant-control": ["fire-ants-central-texas-yard"],
    "cockroach-control": ["cockroaches-central-texas-kitchen"],
}


def service_support(service, articles):
    slug = service["slug"]
    if slug in ("rodent-removal", "rodent-exclusion", "wildlife-live-trapping"):
        factors = "The animal involved, access to the affected space, the extent of activity, follow-up visits and any entry-point repairs. Ask whether removal and exclusion are quoted separately."
        prepare = "Describe the animal or sounds, the time of day, and where activity occurs. Share any photos taken safely from a distance. Tell the office about inaccessible areas before the visit."
    elif slug == "mosquito-misting":
        factors = "The size and layout of the outdoor area, existing equipment, installation needs and maintenance. Ask which work is included in the initial quote and which services recur."
        prepare = "Note the outdoor spaces you use, standing-water locations and any existing system. Tell the office whether you need an installation assessment or help with recurring mosquito activity."
    elif slug == "lawn-pest-control":
        factors = "The area of affected turf, the pest identified, access to the lawn and the follow-up recommended after assessment. Similar-looking turf damage may need a different response."
        prepare = "Note when damage appeared, how it has spread and recent watering or treatment changes. Photographs can help document the pattern before a visit."
    else:
        factors = "The pest identified, the size and layout of the property, where activity occurs, and whether a single visit or recurring service is appropriate."
        prepare = "Tell the office which rooms or outdoor areas are affected, how often you see activity and what you have already tried. Mention pets and access needs so preparation instructions fit your household."
    linked = [a for a in articles if a["slug"] in GUIDE_MAP.get(slug, ["central-texas-pest-calendar"])]
    links = "".join('<li><a href="/insights/%s.html">%s</a></li>' % (a["slug"], html.escape(a["title"])) for a in linked)
    return '''<section class="section section--soft"><div class="container">
      <div class="section-head"><span class="eyebrow">Before you book</span><h2>Plan your %s estimate</h2></div>
      <div class="grid grid--3">
        <div class="card"><h3>What affects the price?</h3><p>%s</p><p>Request a free estimate for your property.</p></div>
        <div class="card"><h3>What to tell the office</h3><p>%s</p></div>
        <div class="card"><h3>Questions to ask</h3><p>Confirm the areas covered, preparation and re-entry instructions, follow-up schedule, and any applicable warranty terms before scheduling.</p><a href="/contact.html?service=%s">Request an estimate for this service →</a></div>
      </div>
      <div class="prose" style="margin-top:28px"><h3>Helpful reading</h3><ul>%s<li><a href="/pest-library.html">Central Texas pest identification library</a></li></ul></div>
    </div></section>''' % (html.escape(service["nav"].lower()), factors, prepare, slug, links)


def library_body(page_hero):
    crumbs = [("Home", "/"), ("Pest Library", None)]
    body = page_hero("Central Texas Pest Library", "Recognize common signs, choose a useful next step, and find the right Excel Pest service.", crumbs)
    jump = "".join('<li><a href="#%s">%s</a></li>' % (p[0], html.escape(p[1])) for p in LIBRARY)
    body += '<section class="section"><div class="container"><nav aria-label="Find a pest"><ul class="library-jump">%s</ul></nav><p class="lead">For homes in Buda, Kyle, San Marcos and the surrounding Hill Country. These clues help you describe a problem; a sighting alone may not identify the species.</p><div class="grid grid--2">' % jump
    for anchor, name, service, signs, next_step, guide, guide_name in LIBRARY:
        extra = '<p><a href="/insights/%s.html">%s →</a></p>' % (guide, html.escape(guide_name)) if guide else ""
        body += '''<article class="card library-entry" id="%s"><h2>%s</h2><h3>What you may notice</h3><p>%s</p><h3>Your next step</h3><p>%s</p><a class="card__link" href="/services/%s.html">View %s service →</a>%s</article>''' % (anchor, html.escape(name), signs, next_step, service, html.escape(name.lower()), extra)
    body += '</div><div class="callout" style="margin-top:28px"><h2>Plan ahead through the year</h2><p>Use our <a href="/insights/central-texas-pest-calendar.html">month-by-month prevention calendar</a> to keep track of the yard, entry points and indoor spaces.</p></div></div></section>'
    return body, crumbs


def calendar_html():
    cards = "".join('<section class="calendar-month"><h2>%s: %s</h2><p>%s</p><p><a href="/services/%s.html">Explore the related service →</a></p></section>' % row for row in CALENDAR)
    return '''<p>Use this Central Texas pest calendar as a home-maintenance checklist, not a prediction that a pest will appear in a particular month. Rain, temperature, irrigation and a property's condition can change activity. Indoor problems can persist all year.</p><p>Start with the tasks that match your home in <a href="/locations/buda.html">Buda</a>, <a href="/locations/kyle.html">Kyle</a>, <a href="/locations/san-marcos.html">San Marcos</a>, <a href="/locations/dripping-springs.html">Dripping Springs</a> or <a href="/locations/wimberley.html">Wimberley</a>.</p>''' + cards + '''<h2>Three habits for every month</h2><ul><li>Record the location, timing and frequency of pest activity.</li><li>Check accessible door gaps, screens, leaks and outdoor water containers.</li><li>Review recurring problems with the technician instead of assuming every sighting needs the same treatment.</li></ul><p>Unsure what you saw? Begin with the <a href="/pest-library.html">pest library</a>. For mosquito conditions and prevention guidance, see the <a href="https://www.hayscountytx.gov/493/Mosquito-Surveillance-Program">Hays County mosquito program</a>.</p>'''
