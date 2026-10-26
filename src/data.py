"""All Turiya Trails content that appears in more than one place.

Edit prices, dates, journeys and sessions here, then run `python3 build.py`.
Every page that mentions them updates together.
"""

SITE = {
    "name": "Turiya Trails",
    # Canonical address used in search results and share previews.
    # The CNAME file in this repository uses the bare domain, so this matches it.
    "url": "https://turiyatrails.in",
    "tagline": "Slow journeys in the Kumaun Himalaya",
    "phone_display": "+91 63960 91261",
    "phone_wa": "916396091261",
    "base": "Oakakhi Stays, Ranikhet, Uttarakhand",
    "maps": "https://www.google.com/maps/search/Oakakhi+Stays+Ranikhet+Uttarakhand",
    "year": 2026,
}

NAV = [
    ("Journeys", "journeys.html"),
    ("Day experiences", "experiences.html"),
    ("Treks", "treks.html"),
    ("Oakakhi", "oakakhi.html"),
    ("Journal", "field-notes.html"),
    ("About", "about.html"),
]


def wa(text=None):
    """WhatsApp link with an optional prefilled message."""
    from urllib.parse import quote
    base = f"https://wa.me/{SITE['phone_wa']}"
    return f"{base}?text={quote(text)}" if text else base


def rupees(n):
    return "₹" + _indian(n)


def _indian(n):
    s = str(n)
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


PRICE_NOTE = "per person"

# ---------------------------------------------------------------------------
# Multi-day journeys. Each one gets its own page at journeys/<slug>.html.
# status: "open" (dates on WhatsApp), "new" (newly designed), "soon" (not yet bookable)
# ---------------------------------------------------------------------------
JOURNEYS = [
    {
        "slug": "kalika-weekend",
        "name": "The Kalika Weekend",
        "kind": "Slow days",
        "level": "Easy",
        "nights": 2, "days": 3,
        "route": "Oakakhi, Ranikhet",
        "places": ["Ranikhet", "Kalika forest"],
        "price": 12000,
        "status": "new",
        "art": ("mist", 3),
        "photo": "journey-kalika-weekend",
        "summary": "The gentlest way in. Two nights at Oakakhi with a forest walk, a birding morning, a nature class and a night under the Ranikhet sky. No trek, no long drives.",
        "intro": [
            "This is the weekend we would give a friend who has never done anything like this before. Nothing is far, nothing is steep, and every day starts slowly.",
            "You stay at Oakakhi, walk into the Kalika forest at the hours when it is most alive, learn a little about what you are looking at, and spend one long evening under the sky.",
        ],
        "season": "Through the year, except the heaviest monsoon weeks. Dates are shared on WhatsApp.",
        "for": ["First-timers and families with older children", "Anyone who wants the forest without a trek", "A first weekend with us, before a longer journey"],
        "fitness": "Gentle walking on forest paths, two to three hours at a time.",
        "itinerary": [
            ("Day one, afternoon", "Arrive at Oakakhi. Chai first, then a sunset walk into Kalika forest. A home-cooked dinner and an early night."),
            ("Day two", "Birdwatching at first light in Kalika. A slow breakfast. Late morning, a nature class: the trees around you, the calls you heard at dawn, and how to keep a simple field notebook. In the evening, a village walk, then an astro night with our guide and a fire."),
            ("Day three", "A silent forest walk at sunrise, breakfast on the porch, and leave when you are ready."),
        ],
        "included": ["Two nights at Oakakhi", "All meals, home-cooked", "Guided forest walks and birdwatching session", "Nature class", "Astro night with our guide", "Binoculars on loan"],
        "excluded": ["Travel to Ranikhet and back", "Personal expenses", "Travel insurance"],
        "trek": None,
    },
    {
        "slug": "into-the-quiet",
        "name": "Into the Quiet",
        "kind": "Slow days",
        "level": "Beginner",
        "nights": 2, "days": 3,
        "route": "Ranikhet and Pandavkholi",
        "places": ["Ranikhet", "Pandavkholi"],
        "price": 14000,
        "status": "open",
        "art": ("dawn", 1),
        "photo": "journey-into-the-quiet",
        "summary": "Three slow days in the forest above Ranikhet. Birds in the morning, a fire at night, and on the last day a gentle walk up to the Pandavkholi meadow.",
        "intro": [
            "Three slow days in the forest above Ranikhet. You walk in the morning when the birds are loudest, sit through a sunset, and let a fire ask you a few honest questions at night.",
            "On the last day you walk a little higher, to the meadow at Pandavkholi, a place tied to the years the Pandavas spent in hiding. It is the kind of place people stop talking without being asked.",
        ],
        "season": "Runs in small batches through the year, except deep monsoon. Dates are shared on WhatsApp.",
        "for": ["First-time trekkers who can walk a few hours", "Solo travellers", "Anyone who wants a short trek with real quiet at the top"],
        "fitness": "Comfortable walking for three to four hours with some steady climbing on the last day.",
        "itinerary": [
            ("Day one, evening", "Arrive at Oakakhi. A sunset walk into Kalika forest, then a quiet dinner."),
            ("Day two", "Village trail and birdwatching before breakfast. A slow afternoon. In the evening, a village walk, then stargazing and stories with our astro guide. The night ends at the bonfire, with questions worth sitting with."),
            ("Day three", "Drive to Kukuchina via Dwarahat and walk the forest trail to the Pandavkholi meadow, about 3.5 km each way. Time at the top, an optional visit to the Mahavatar Babaji cave, and a gentle return."),
        ],
        "included": ["Two nights at Oakakhi", "All meals", "All guided walks", "Stargazing and storytelling", "Bonfire evening", "The Pandavkholi trek with a certified guide", "Local transport on the trek day"],
        "excluded": ["Travel to Ranikhet and back", "Personal expenses", "Travel insurance"],
        "trek": "pandavkholi",
        "gallery": [("pandavkholi-1", "The open meadow at Pandavkholi under a cloudy sky", ""),
                    ("pandavkholi-2", "A silhouette against the sunset near Pandavkholi", ""),
                    ("pandavkholi-3", "Dusk on the walk to Pandavkholi", ""),
                    ("pandavkholi-4", "The sun setting over the ridges from Pandavkholi", "")],
    },
    {
        "slug": "where-the-clouds-rest",
        "name": "Where the Clouds Rest",
        "kind": "Slow days",
        "level": "Intermediate",
        "nights": 3, "days": 4,
        "route": "Ranikhet and Kausani",
        "places": ["Ranikhet", "Kausani", "Pinnath"],
        "price": 18000,
        "status": "open",
        "art": ("mist", 7),
        "photo": "journey-where-the-clouds-rest",
        "summary": "The slow days of Ranikhet, then a night near Kausani for the Pinnath trail: five kilometres up to a temple ridge at 2,750 metres.",
        "intro": [
            "The slow days of Ranikhet, and then a night near Kausani for the Pinnath trail.",
            "It is a five kilometre walk through oak and rhododendron to a temple at 2,750 metres, where the clouds usually arrive before you do. On a clear day the high Himalaya stands in a line across the north.",
        ],
        "season": "Best from autumn to early summer. Dates are shared on WhatsApp.",
        "for": ["Walkers with a little trekking behind them", "Anyone who wants a longer climb with big views", "People who like to end a journey high up"],
        "fitness": "You should be comfortable walking uphill for a few hours at altitude. We walk slowly on purpose.",
        "itinerary": [
            ("Days one and two", "The full rhythm of Oakakhi. Kalika forest at dusk, birds at dawn, the village trail, stargazing, and the bonfire."),
            ("Day three", "A slow drive to Kausani, about two and a half hours through the hills. Evening at leisure, facing the high Himalaya."),
            ("Day four", "The Pinnath trail. Five kilometres up to the temple ridge, unhurried, and back down for the journey home."),
        ],
        "included": ["Three nights of stay", "All meals", "All guided walks and sessions", "The Pinnath trek with a certified guide", "Transport between Ranikhet and Kausani"],
        "excluded": ["Travel to Ranikhet and back", "Personal expenses", "Travel insurance"],
        "trek": "pinnath",
    },
    {
        "slug": "the-seekers-ridge",
        "name": "The Seeker's Ridge",
        "kind": "Slow days",
        "level": "Challenging",
        "nights": 3, "days": 4,
        "route": "Ranikhet and Bharatkot",
        "places": ["Ranikhet", "Bharatkot"],
        "price": 19500,
        "status": "open",
        "art": ("dusk", 4),
        "photo": "journey-the-seekers-ridge",
        "summary": "For those who want the silence to cost something. A long, honest walk to Bharatkot with one night in camp on the mountain.",
        "intro": [
            "For those who want the silence to cost something. Bharatkot is the highest peak in its range near Almora, and the walk to it is long and honest.",
            "One night is spent in camp on the mountain. The night in camp includes the sky, the fire, and very little else. That is the point.",
        ],
        "season": "For fit walkers. Batches run outside monsoon and deep winter. Dates are shared on WhatsApp.",
        "for": ["Fit, experienced walkers", "People who want a real physical effort", "Anyone drawn to a night on a mountain"],
        "fitness": "Long distances and real climbs over two days. We talk honestly with you about readiness before confirming.",
        "itinerary": [
            ("Day one", "Arrive at Oakakhi. The sunset forest walk, dinner, and an early night. The briefing happens at the fire."),
            ("Days two and three", "The Bharatkot trek, taken over two days with a camp night on the mountain. Led by our BMC certified lead guide."),
            ("Day four", "Descend, return to Oakakhi for a proper meal, and leave when you are ready."),
        ],
        "included": ["Three nights, including one camp night", "All meals", "Camping equipment", "The full trek with a certified guide", "Local transport"],
        "excluded": ["Travel to Ranikhet and back", "Personal expenses", "Travel insurance"],
        "trek": "bharatkot",
        "gallery": [("bharatkot-1", "Our camp on the Bharatkot summit in the morning", ""),
                    ("bharatkot-2", "Snow peaks of the high Himalaya seen from Bharatkot", ""),
                    ("bharatkot-3", "Tents on the ridge near Bharatkot", ""),
                    ("bharatkot-4", "Walking up through oak forest on the way to Bharatkot", "")],
    },
    {
        "slug": "first-light",
        "name": "First Light",
        "kind": "Birdwatching",
        "level": "Easy",
        "nights": 3, "days": 4,
        "route": "Ranikhet, Sattal, Pangot",
        "places": ["Ranikhet", "Sattal", "Pangot"],
        "price": 19500,
        "status": "open",
        "art": ("lake", 2),
        "photo": "journey-first-light",
        "summary": "The classic Kumaun birding triangle, taken slowly. Kalika at dawn, the hides at Sattal, and the pheasant forests of Pangot.",
        "intro": [
            "The classic Kumaun birding triangle, taken slowly. Over five hundred species live between these forests and lakes. You will not see them all. You will learn to see a few of them properly.",
        ],
        "season": "October to June. December and January bring peak activity, April and May bring breeding plumage. No departures in monsoon.",
        "for": ["Birdwatchers of every level", "Photographers with patience", "Anyone who wants to learn to see a forest properly"],
        "fitness": "Easy walking. Very early mornings.",
        "itinerary": [
            ("Night one, Ranikhet", "Arrive by evening. At dawn, Kalika forest with our lead guide. The Great Barbet, the Khalij Pheasant, the Verditer Flycatcher. The home list."),
            ("Night two, Sattal", "Two hours to the seven lakes. An afternoon and a morning at the famous hides, where the birds come to you if you can hold still long enough."),
            ("Night three, Pangot", "Through Nainital, with stops at Kilbury on the way. Pangot's forests hold the three pheasants every birder comes for. An early night, because the morning matters."),
            ("Day four", "First light at Kilbury and Woodpecker Point. Then a short drive down to Kathgodam, and home."),
        ],
        "included": ["All stays", "All meals", "All transport", "Hide charges", "Guiding throughout", "Binoculars on loan if you do not have your own"],
        "excluded": ["Travel to Ranikhet, and home from Kathgodam", "Personal expenses", "Travel insurance"],
        "trek": None,
    },
    {
        "slug": "three-skies",
        "name": "Three Skies",
        "kind": "Stargazing",
        "level": "Easy",
        "nights": 3, "days": 4,
        "route": "Ranikhet, Kausani, Kasar Devi",
        "places": ["Ranikhet", "Kausani", "Kasar Devi", "Mukteshwar"],
        "price": 18500,
        "status": "open",
        "art": ("night", 1),
        "photo": "journey-three-skies",
        "summary": "Three nights, three different skies. Constellations, the stories behind them, and the silence after the stories end.",
        "intro": [
            "Three nights, three different skies. The light you see left its source before you were born.",
            "Our astro guide walks you through the constellations, the stories behind them, and the silence after the stories end.",
        ],
        "season": "Astro batches run only on new moon windows, October to March, when the Kumaun sky is at its darkest. An optional fourth night at Mukteshwar can be added for ₹5,500.",
        "for": ["Anyone who has never really looked up", "Amateur astronomers and photographers", "Couples and small groups of friends"],
        "fitness": "No trekking. Late nights and some time on cold grass.",
        "itinerary": [
            ("Night one, Ranikhet", "Kalika forest at dusk, then the first sky. A full astro night at our home ground near Oakakhi, with the naked eye and a good story."),
            ("Night two, Kausani", "A drive north through the hills. Kausani sits high and clear. Telescope time, and the mountains at dawn."),
            ("Night three, Kasar Devi", "The ridge above Almora that has drawn seekers for a century. No telescope tonight. Just the raw sky, lying back on the grass, and the oldest light there is."),
            ("Optional night four, Mukteshwar", "At 2,285 metres with almost no light below, Mukteshwar is the deepest sky of the circuit. Exit the next morning via Bhimtal and Kathgodam."),
        ],
        "included": ["All stays", "All meals", "All transport between sites", "Every astro session with our guide", "Observatory entry where used"],
        "excluded": ["Travel to Ranikhet and back", "The optional Mukteshwar night (₹5,500)", "Personal expenses", "Travel insurance"],
        "trek": None,
    },
    {
        "slug": "above-the-treeline",
        "name": "Above the Treeline",
        "kind": "Mountain journey",
        "level": "Moderate",
        "nights": 5, "days": 6,
        "route": "Ranikhet to Munsyari and Khalia Top",
        "places": ["Ranikhet", "Munsyari", "Khalia Top"],
        "price": 26500,
        "status": "new",
        "art": ("snow", 1),
        "photo": "journey-above-the-treeline",
        "summary": "From the oak forests of Ranikhet to the high meadows of Khalia Top above Munsyari. A night in camp, a sunrise facing the Panchachuli peaks on a clear morning, and dark skies all the way.",
        "intro": [
            "This journey starts where all of ours do, with a slow evening at Oakakhi. Then it goes further north than anything else we run, to Munsyari and the meadows of Khalia Top, above the treeline at around 3,500 metres.",
            "The walk up is through oak and rhododendron, then open grassland. We camp one night below the top so that the morning can be spent up there, when the Panchachuli peaks are most likely to be clear. Birds on the way, a sky with almost no light under it, and very few people.",
        ],
        "season": "October to June. In winter the meadows can be under snow, which changes the walk completely. We tell you honestly what the trail will be like before you book.",
        "for": ["Walkers ready for a proper day of climbing", "People who want big mountain views without a week-long expedition", "Anyone who wants a camp night under a dark sky"],
        "fitness": "One long climbing day and a steep descent. You should be able to walk five to six hours with breaks.",
        "itinerary": [
            ("Day one, Oakakhi", "Arrive in Ranikhet. Kalika forest at dusk, dinner, and a first astro session if the sky is clear."),
            ("Day two, the long road north", "Birds at dawn, then a full day's drive north through Bageshwar and the Ramganga valley to Munsyari, with stops along the way. Expect most of the day on the road."),
            ("Day three, Munsyari", "A slow day to adjust to the altitude. A walk around the town and its ridges, and an early night."),
            ("Day four, into the high meadows", "Drive to the trailhead and walk up through forest to our camp below Khalia Top. Dinner, the sky, and the fire."),
            ("Day five, Khalia Top", "Up before dawn to the top, for sunrise facing the Panchachuli range if the weather allows. Descend to Munsyari for a warm meal and a proper bed."),
            ("Day six, homeward", "The drive back south. We drop you at Kathgodam or return you to Ranikhet."),
        ],
        "included": ["One night at Oakakhi, three nights in Munsyari, one camp night", "All meals", "Camping equipment", "The Khalia Top trek with our guide", "All transport from Ranikhet and back to Kathgodam or Ranikhet", "Forest entry fees"],
        "excluded": ["Travel to Ranikhet", "Personal expenses", "Travel insurance"],
        "trek": "khalia-top",
    },
    {
        "slug": "where-the-river-begins",
        "name": "Where the River Begins",
        "kind": "Mountain journey",
        "level": "Challenging",
        "nights": 7, "days": 8,
        "route": "Ranikhet to the Pindari Glacier",
        "places": ["Ranikhet", "Khati", "Dwali", "Phurkia", "Pindari Glacier"],
        "price": 34000,
        "status": "new",
        "art": ("snow", 5),
        "photo": "journey-where-the-river-begins",
        "summary": "Up the Pindar valley, village by village, to the foot of the glacier where the river starts. Our longest walk, and the one that asks the most.",
        "intro": [
            "The Pindari trail follows a river back to the ice it comes from. You walk through the last villages of the valley, then forest, then open moraine, until the glacier stands in front of you at around 3,600 metres.",
            "Stays on the trail are simple: village homestays, rest houses or tents, depending on the season and what is open. We keep the days unhurried so the walking stays a pleasure.",
        ],
        "season": "May and June, and September to October. The upper trail is closed by snow in winter and difficult in monsoon. We confirm the route and stays before each batch.",
        "for": ["Fit walkers with some trekking experience", "Anyone who wants a full week away from roads", "People who like the idea of following a river to its source"],
        "fitness": "Several consecutive days of walking, one of them long. You should be in good health and able to walk six to seven hours.",
        "itinerary": [
            ("Day one, Oakakhi", "Arrive in Ranikhet. A slow evening, the forest at dusk, and a briefing at the fire."),
            ("Day two, to Khati", "Drive north through Bageshwar to the roadhead, then walk to Khati, the last village on the trail."),
            ("Day three, Khati to Dwali", "A long, beautiful day along the Pindar river through forest to Dwali, where two valleys meet."),
            ("Day four, Dwali to Phurkia", "A short day on purpose. The altitude starts to matter, so we give it time."),
            ("Day five, to the glacier", "The big day. Up to Zero Point at the foot of the Pindari Glacier, time there, and back down to Dwali."),
            ("Day six, Dwali to Khati", "Retracing the river, with legs that know the way now."),
            ("Day seven, out of the valley", "Walk out to the road and drive to Kausani for a hot shower and a night facing the Himalaya."),
            ("Day eight, homeward", "Back to Ranikhet or down to Kathgodam."),
        ],
        "included": ["Seven nights: Oakakhi, trail stays and Kausani", "All meals", "Tents where needed", "Our guide and local support staff", "All transport from Ranikhet and back", "Trek permits and forest fees"],
        "excluded": ["Travel to Ranikhet", "Porter or mule for personal bags (can be arranged)", "Personal expenses", "Travel insurance"],
        "trek": "pindari",
        "gallery": [("pindari-1", "Arms open below the snow peaks at the head of the Pindar valley", ""),
                    ("pindari-2", "A trekker and a resting flock high in the Pindar valley", ""),
                    ("pindari-3", "A stream tumbling through forest on the Pindari trail", ""),
                    ("pindari-4", "Slate-roofed houses of a village on the Pindari trail", "")],
    },
    {
        "slug": "sub-ek",
        "name": "Sub Ek",
        "kind": "Spiritual circuit",
        "level": "Easy",
        "nights": 1, "days": 2,
        "route": "Kakrighat, Kainchi Dham, Bhumiadhar, Hanuman Garhi",
        "places": ["Kakrighat", "Kainchi Dham", "Bhumiadhar", "Nainital"],
        "price": 9500,
        "price_alt": "₹14,500 for the three-day circuit",
        "status": "open",
        "art": ("dusk", 9),
        "photo": "journey-sub-ek",
        "summary": "Four small temples in the Kumaon hills, one river, and a name people keep returning to. Nothing to buy, nothing to prove.",
        "intro": [
            "Four small temples in the Kumaon hills, one river, and a name people keep returning to. We travel slowly between the places associated with Neem Karoli Baba, sit where his people sat, and keep the phones away.",
            "Nothing to buy, nothing to prove. Sub ek. All is one.",
        ],
        "season": "Darshan at Kainchi is open through the year. We avoid the June bhandara crowds and plan quieter days.",
        "for": ["Devotees and the curious alike", "Anyone who wants these places without the rush", "Travellers with only a couple of days"],
        "fitness": "No trekking. Short walks and steps at the temples.",
        "itinerary": [
            ("The two-day circuit", "An early start from Ranikhet. First Kakrighat, where Vivekananda sat by the Kosi under a peepal tree. Midday darshan at Kainchi Dham, then Bhumiadhar. Overnight near Bhowali or Nainital. The second morning begins at Hanuman Garhi in Nainital, and the return is unhurried."),
            ("The three-day circuit", "The same four places with room to breathe. Evening aarti at Kainchi, a morning by the river, time in Nainital, and no clock worth watching. Two nights of stay."),
        ],
        "included": ["Stays", "All meals", "All travel between the sites", "A guide who knows when to speak and when not to", "Darshan at these temples is free, and we keep it that way"],
        "excluded": ["Travel to Ranikhet and back", "Offerings and personal expenses"],
        "trek": None,
    },
    {
        "slug": "the-long-quiet",
        "name": "The Long Quiet",
        "kind": "Spiritual week",
        "level": "Easy to moderate",
        "nights": 5, "days": 6,
        "route": "Ranikhet to Kainchi, the long way",
        "places": ["Ranikhet", "Pandavkholi", "Sitlakhet", "Kasar Devi", "Kainchi"],
        "price": 39000,
        "status": "soon",
        "art": ("mist", 11),
        "photo": "journey-the-long-quiet",
        "summary": "Five nights across the quiet places of Kumaun. A week that moves slowly on purpose.",
        "intro": [
            "Five nights across the quiet places of Kumaun. Ranikhet, the Pandavkholi meadows, the oak forests of Sitlakhet, the Kasar Devi ridge, and finally the Kainchi valley.",
            "We are walking this route ourselves before we open it. If you would like to be told when the first batch opens, send us a message.",
        ],
        "season": "Opening soon. Message us to hear first.",
        "for": ["People with a full week to give", "Anyone who wants several of our journeys in one", "Seekers who prefer depth to distance"],
        "fitness": "Gentle to moderate walking most days.",
        "itinerary": [
            ("Nights one and two", "Ranikhet and the Kalika forest, then Kukuchina for the Pandavkholi trail and the Mahavatar Babaji cave."),
            ("Night three", "Sitlakhet. The walk to the Syahi Devi temple through old oak forest, and a Himalayan sunset that asks for nothing."),
            ("Night four", "Kasar Devi. The ridge, the caves, and an evening of sitting still."),
            ("Night five", "The Kainchi valley. Kakrighat, darshan at Kainchi Dham, Bhumiadhar, and an exit the next morning through Nainital and Hanuman Garhi."),
        ],
        "included": ["Five nights across four places", "All meals", "All guiding", "Every drive in between"],
        "excluded": ["Travel to Ranikhet, and home from Nainital", "Personal expenses", "Travel insurance"],
        "trek": "pandavkholi",
    },
]

FEATURED_JOURNEYS = ["kalika-weekend", "into-the-quiet", "first-light", "three-skies", "above-the-treeline", "where-the-river-begins"]

# ---------------------------------------------------------------------------
# Independent sessions: book one on its own, or add to any journey.
# ---------------------------------------------------------------------------
SESSIONS = [
    {
        "group": "Silent forest walks",
        "page": "forest-walks.html",
        "items": [
            {"name": "Silent forest walk", "where": "Kalika forest, from Oakakhi, Ranikhet", "length": "2 to 3 hours", "price": 1200,
             "desc": "At sunrise or late afternoon. The first half hour in complete silence, then chai and conversation back at Oakakhi."},
        ],
    },
    {
        "group": "Birdwatching",
        "page": "birdwatching.html",
        "items": [
            {"name": "Birdwatching at Kalika", "where": "Kalika forest, Ranikhet", "length": "3 hours from first light", "price": 1500,
             "desc": "Our home list. Barbets, pheasants, flycatchers and the forest they live in. Binoculars provided."},
            {"name": "Birdwatching at Kasar Devi", "where": "Kasar Devi ridge, Almora", "length": "3 hours from first light", "price": 1800,
             "desc": "Pine and oak on an open ridge, with long views and a different set of birds."},
            {"name": "Birdwatching at Sattal", "where": "Sattal lakes, near Bhimtal", "length": "Half day", "price": 2500,
             "desc": "The famous hides by the seven lakes, where patience is everything. Hide charges included."},
        ],
    },
    {
        "group": "Stargazing",
        "page": "stargazing.html",
        "items": [
            {"name": "Astro night at Oakakhi", "where": "Oakakhi, Ranikhet", "length": "2 hours after dinner", "price": 1800,
             "desc": "Naked eye and binoculars, stories from Indian and Greek skies, and hot chai under the stars."},
            {"name": "Astro night at Kasar Devi", "where": "Kasar Devi ridge, Almora", "length": "2 hours after dark", "price": 2200,
             "desc": "A darker ridge, a wider horizon, and the oldest light there is."},
        ],
    },
    {
        "group": "Nature classes",
        "page": "nature-classes.html",
        "items": [
            {"name": "Reading the forest", "where": "Oakakhi and Kalika forest, Ranikhet", "length": "2 hours", "price": 1500,
             "desc": "A small, hands-on class: the trees of the Kumaun forest, bird calls, and keeping a simple field notebook."},
        ],
    },
    {
        "group": "Day treks",
        "page": "treks.html",
        "items": [
            {"name": "Pandavkholi day trek", "where": "From Oakakhi, via Dwarahat", "length": "Full day", "price": 3500,
             "desc": "A gentle forest climb to the Pandavkholi meadow. Transport from Ranikhet, guide and packed lunch included."},
            {"name": "Pinnath day trek", "where": "From Kausani", "length": "Full day", "price": 4000,
             "desc": "Five kilometres up through oak and rhododendron to the temple ridge at 2,750 metres."},
            {"name": "Bharatkot overnight trek", "where": "Almora district", "length": "2 days, 1 night", "price": 9500,
             "desc": "The hardest walking we offer, with a night in camp on the mountain. Camping equipment included."},
        ],
    },
]

SESSION_TERMS = [
    "Prices are per person, for a minimum of two people. Solo guests are welcome to join a scheduled session.",
    "Sessions at Kasar Devi and Sattal begin there. We can arrange transport from Ranikhet at cost.",
    "Private sessions for your own group can be arranged on request.",
]

# ---------------------------------------------------------------------------
# Treks
# ---------------------------------------------------------------------------
TREKS = [
    {
        "slug": "pandavkholi", "name": "Pandavkholi", "level": "Beginner", "where": "Kukuchina, near Dwarahat",
        "art": ("dawn", 21),
        "desc": "A gentle forest climb to a high meadow tied to the years the Pandavas spent in hiding. The trail passes near the Mahavatar Babaji cave, and the meadow at the top is the kind of place people stop talking without being asked.",
        "facts": [("Trail", "About 3.5 km each way, a steady forest path from Kukuchina village"), ("Getting there", "About 1.5 hours from Ranikhet via Dwarahat. We arrange the drive."), ("Suits", "First-time trekkers who can walk a few hours")],
        "journeys": ["into-the-quiet", "the-long-quiet"], "standalone": 3500, "standalone_label": "Day trek from Oakakhi",
    },
    {
        "slug": "pinnath", "name": "Pinnath", "level": "Intermediate", "where": "Near Kausani",
        "art": ("mist", 22),
        "desc": "A climb through oak and rhododendron to a temple ridge at 2,750 metres. The clouds usually arrive before you do, and on a clear day the high Himalaya stands in a line across the north.",
        "facts": [("Trail", "About 5 km each way, a sustained climb"), ("Altitude", "2,750 metres. High enough to feel it."), ("Suits", "Walkers comfortable going uphill for a few hours")],
        "journeys": ["where-the-clouds-rest"], "standalone": 4000, "standalone_label": "Day trek from Kausani",
    },
    {
        "slug": "bharatkot", "name": "Bharatkot", "level": "Challenging", "where": "Almora district",
        "art": ("dusk", 23),
        "desc": "The highest peak in its range, and the hardest walking near Ranikhet. Usually taken over two days with a night in camp on the mountain. It asks for fitness and gives back a sky you will not forget.",
        "facts": [("Trail", "A full two-day trek with long distances and real climbs"), ("Camp", "One night on the mountain, equipment included"), ("Suits", "Fit, experienced walkers. We talk about readiness before confirming.")],
        "journeys": ["the-seekers-ridge"], "standalone": 9500, "standalone_label": "Overnight trek",
    },
    {
        "slug": "khalia-top", "name": "Khalia Top", "level": "Moderate", "where": "Munsyari, Pithoragarh district",
        "art": ("snow", 24),
        "desc": "Forest giving way to open high meadows above Munsyari, at around 3,500 metres. On a clear morning the Panchachuli peaks fill the horizon. Under snow in winter, flowering in early summer.",
        "facts": [("Trail", "A long climbing day through forest to the meadows, with a camp night"), ("Altitude", "Around 3,500 metres"), ("Suits", "Walkers ready for five to six hours on the trail")],
        "journeys": ["above-the-treeline"], "standalone": None, "standalone_label": "",
    },
    {
        "slug": "pindari", "name": "Pindari Glacier", "level": "Challenging", "where": "Bageshwar district",
        "art": ("snow", 25),
        "desc": "A multi-day walk up the Pindar valley through the last villages, forest and moraine, to Zero Point at the foot of the glacier at around 3,600 metres.",
        "facts": [("Trail", "Five walking days from the roadhead and back"), ("Altitude", "Around 3,600 metres at Zero Point"), ("Suits", "Fit walkers with some trekking experience")],
        "journeys": ["where-the-river-begins"], "standalone": None, "standalone_label": "",
    },
]

# ---------------------------------------------------------------------------
# Places we work in
# ---------------------------------------------------------------------------
PLACES = [
    {"name": "Ranikhet", "alt": "About 1,800 m", "desc": "Our home. Oak and rhododendron forest around Oakakhi, the Kalika ridge, and a night sky with little light beneath it.", "what": "Forest walks · Birdwatching · Astro nights · Nature classes"},
    {"name": "Pandavkholi", "alt": "Above Dwarahat", "desc": "A forest trail to a quiet meadow tied to the Mahabharata, near the Mahavatar Babaji cave.", "what": "Beginner trek"},
    {"name": "Kasar Devi", "alt": "Ridge above Almora", "desc": "The ridge that has drawn seekers for a century. Pine, open views, and dark skies.", "what": "Birdwatching · Stargazing"},
    {"name": "Sattal and Pangot", "alt": "Near Nainital", "desc": "Lakes, forest hides and pheasant country. Among the best-known birding in Kumaun.", "what": "Birdwatching"},
    {"name": "Kausani and Pinnath", "alt": "Up to 2,750 m", "desc": "A long view of the high Himalaya, and a forest climb to a temple in the clouds.", "what": "Intermediate trek · Stargazing"},
    {"name": "Munsyari and Pindari", "alt": "The far north of Kumaun", "desc": "High meadows at Khalia Top, and the valley walk to the Pindari Glacier.", "what": "Mountain journeys"},
]

# ---------------------------------------------------------------------------
# People (from the existing site)
# ---------------------------------------------------------------------------
TEAM = [
    {"initial": "N", "photo": "team-nishant", "name": "Nishant", "role": "Lead guide and host",
     "bio": "Runs Oakakhi Stays in Ranikhet and leads every trek in person. BMC mountaineering certified. The person you will meet first, chai in hand, before anything else is discussed.",
     "skills": ["Himalayan safety", "Hospitality", "Forest ecology"],
     "quote": "I've hosted people at Oakakhi for years. What I want now is to actually walk them into the forest, not just point at it from the porch."},
    {"initial": "S", "photo": "team-sachin", "name": "Sachin", "role": "Astro guide and storyteller",
     "bio": "Training with a stargazing company near Ramnagar and bringing every technique back to Turiya's astro nights. Believes the best fact is the one wrapped inside a story.",
     "skills": ["Constellation navigation", "Astrophotography", "Campfire storytelling"],
     "quote": "Most people have never really looked up. My job on an astro night isn't to recite facts, it's to get out of the way so the sky can do that."},
    {"initial": "K", "photo": "team-naveen", "name": "Naveen (Kannu)", "role": "Field documentarian",
     "bio": "Born in these hills. Shoots every walk, every dawn, every quiet moment that would otherwise go unrecorded. Also first on the trail when the group needs steady hands.",
     "skills": ["Camera craft", "Birding", "First aid"],
     "quote": "I grew up in these hills. Filming them for Turiya Trails is the first time work has meant showing people my own backyard properly."},
]

FAQ = [
    ("Is this suitable for beginners?", "Yes. The Kalika Weekend and every day experience are built for beginners, and Into the Quiet is a gentle first trek. Our longer treks ask more, and we will be honest with you about which one fits."),
    ("Can solo travellers join?", "Solo travellers are a large part of who we build these journeys for, not an edge case we tolerate. You can join a scheduled batch or a session on your own."),
    ("Where do journeys start?", "Almost every journey starts at Oakakhi Stays, our home in Ranikhet. The nearest railway station is Kathgodam, about three hours away by road. Tell us how you are travelling and we will help you plan the last stretch."),
    ("How do I book?", "Message us on WhatsApp or use the enquiry form. We talk first about what you are looking for, then share dates, the full plan and how to confirm your place. No booking is final until we have spoken."),
    ("What should I pack?", "Layers, sturdy shoes, a headlamp, and less than you think. We send a full list once your dates are confirmed."),
    ("Will there be mobile network?", "Patchy in the forest, by design. Ranikhet town has signal. Oakakhi mostly does not, and that is part of the point."),
    ("What food is provided?", "Home-cooked Kumaoni meals at Oakakhi, and simple, fresh food on the trail. All meals are included in journey prices. Tell us about any dietary needs in advance."),
    ("Can I bring my camera?", "Yes, especially for birdwatching and astro nights. We do protect group silence during forest walks, camera included."),
    ("What happens in an emergency?", "Our guides carry first aid supplies and are trained in immediate response. In a real emergency, getting you to help fast is the only priority."),
    ("How cold does it get?", "Ranikhet sits around 1,800 metres. Days are pleasant most of the year, nights can be cool, and warmer layers matter from October to February. Khalia Top and Pindari are much colder, and we send a specific list for them."),
]


def journey(slug):
    return next(j for j in JOURNEYS if j["slug"] == slug)


def trek(slug):
    return next(t for t in TREKS if t["slug"] == slug)
