"""Every page on the site. Each function returns (output path, html)."""
import glob
import os
from datetime import date
from html import escape

from . import markdown
from .data import (FAQ, FEATURED_JOURNEYS, JOURNEYS, PLACES, PRICE_NOTE, SESSION_TERMS, SESSIONS, SITE, TEAM, TREKS,
                   USD_RATE, journey, rupees, trek, usd, wa)
from .templates import ORG_LD, ROOT, WA_ICON, breadcrumbs, gallery, media, page, photo_sources, url

E = escape


# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------
def duration(j):
    return f'{j["nights"]} night{"s" if j["nights"] > 1 else ""}, {j["days"]} days'


def price_label(j):
    if j["status"] == "soon":
        return f'From {rupees(j["price"])}'
    return rupees(j["price"])


def journey_card(j, eager=False):
    tag = '<span class="tag">New</span>' if j["status"] == "new" else ('<span class="tag">Opening soon</span>' if j["status"] == "soon" else "")
    return f"""<a class="feature reveal" href="/journeys/{j['slug']}.html">
  {media(j['photo'], j['art'], f"{j['name']}, {j['route']}", eager=eager, sizes="(min-width: 1240px) 340px, (min-width: 1100px) 30vw, (min-width: 760px) 46vw, 92vw")}
  <span class="f-level">{E(j['kind'])} · {E(j['level'])}{tag}</span>
  <h3>{E(j['name'])}</h3>
  <span class="f-route">{E(j['route'])}</span>
  <span class="f-foot"><span>{duration(j)}</span><span class="f-price">{price_label(j)}</span></span>
</a>"""


def journey_row(j):
    tag = '<span class="tag">New</span>' if j["status"] == "new" else ('<span class="tag">Opening soon</span>' if j["status"] == "soon" else "")
    alt = f'<small>{E(j["price_alt"])}</small>' if j.get("price_alt") else f"<small>{PRICE_NOTE} · ≈ {usd(j['price'])}</small>"
    return f"""<li class="journey-row"><a href="/journeys/{j['slug']}.html">
  <span class="jr-level">{E(j['level'])}</span>
  <span><h3>{E(j['name'])}{tag}</h3><span class="jr-sub">{duration(j)}</span></span>
  <span class="jr-route">{E(j['route'])}<span class="jr-sub">{E(j['summary'])}</span></span>
  <span class="jr-price">{price_label(j)}{alt}</span>
</a></li>"""


def checklist(items):
    return '<ul class="checklist">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"


def faq_pick(*questions):
    return [qa for q in questions for qa in FAQ if qa[0] == q]


def faq_block(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{E(q)}</summary><div class="faq-a"><p>{E(a)}</p></div></details>' for q, a in items
    ) + "</div>"


def cta(title="Let’s plan a quieter kind of journey.", text="Tell us what you are looking for, how many of you there are and roughly when. We will help you find the right walk, sky or forest, and we will be honest if we are not the right fit.", tone="section--dark"):
    return f"""<section class="section {tone} cta">
  <div class="wrap reveal">
    <span class="eyebrow">Begin here</span>
    <h2>{title}</h2>
    <p>{E(text)}</p>
    <div class="btn-row">
      <a class="btn btn--light" href="/plan.html">Plan your journey</a>
      <a class="btn btn--ghost-light" href="{wa('Namaste Turiya Trails, I found you through the website and would like to know more.')}">{WA_ICON} WhatsApp us</a>
    </div>
  </div>
</section>"""


def page_hero(eyebrow, title, lede, scene, slot, crumbs=None, facts=None, split=False):
    """Page header with the photo behind the text. With split, the header fills the screen,
    the headline sits at the top and the description at the bottom-left, leaving the
    middle of the photo clear. With split="corner", all the text sits bottom-right."""
    crumb_html = crumbs or ""
    facts_html = ""
    if facts:
        facts_html = '<dl class="facts">' + "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in facts) + "</dl>"
    if split == "corner":
        return f"""<section class="page-hero page-hero--split page-hero--corner">
  <div class="hero-media">{media(slot, scene, "", eager=True, sizes="(max-aspect-ratio: 1/1) 220vh, 100vw")}</div>
  <div class="wrap page-hero-inner">
    {crumb_html}
    <div class="corner-text">
      <span class="eyebrow">{E(eyebrow)}</span>
      <h1>{title}</h1>
      <p class="lede">{E(lede)}</p>
    </div>
  </div>
</section>"""
    if split:
        return f"""<section class="page-hero page-hero--split">
  <div class="hero-media">{media(slot, scene, "", eager=True, sizes="(max-aspect-ratio: 1/1) 220vh, 100vw")}</div>
  <div class="wrap page-hero-inner">
    <div>
      {crumb_html}
      <span class="eyebrow">{E(eyebrow)}</span>
      <h1>{title}</h1>
    </div>
    <p class="lede">{E(lede)}</p>
  </div>
</section>"""
    return f"""<section class="page-hero">
  <div class="hero-media">{media(slot, scene, "", eager=True, sizes="(max-aspect-ratio: 1/1) 220vh, 100vw")}</div>
  <div class="wrap page-hero-inner">
    {crumb_html}
    <span class="eyebrow">{E(eyebrow)}</span>
    <h1>{title}</h1>
    <p class="lede">{E(lede)}</p>
    {facts_html}
  </div>
</section>"""


def plain_hero(eyebrow, title, lede, crumbs=""):
    return f"""<section class="page-hero page-hero--plain">
  <div class="wrap page-hero-inner">
    {crumbs}
    <span class="eyebrow">{E(eyebrow)}</span>
    <h1>{title}</h1>
    <p class="lede">{E(lede)}</p>
  </div>
</section>"""


def journal_posts():
    posts = []
    for path in sorted(glob.glob(os.path.join(ROOT, "src", "journal", "*.md"))):
        meta, body = markdown.front_matter(open(path, encoding="utf-8").read())
        meta["slug"] = os.path.splitext(os.path.basename(path))[0]
        meta["body"] = body
        if meta.get("draft", "").lower() == "true":
            continue
        posts.append(meta)
    posts.sort(key=lambda p: (p.get("date", ""), p.get("number", "")), reverse=True)
    return posts


def nice_date(s):
    try:
        return date.fromisoformat(s).strftime("%-d %B %Y")
    except ValueError:
        return s


def post_row(p):
    return f"""<li class="post-row"><a href="/journal/{p['slug']}.html">
  <span><span class="pr-cat">Field note {E(p.get('number', ''))}</span><br><time datetime="{E(p['date'])}">{nice_date(p['date'])}</time></span>
  <span><h3>{E(p['title'])}</h3><p>{E(p.get('standfirst', p['description']))}</p></span>
  <span class="pr-cat">{E(p.get('category', ''))}</span>
</a></li>"""


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
def home():
    ways = [
        ("01", "Silent forest walks", "Oak and rhododendron forest, walked slowly enough to notice what rushing past would erase. The first half hour is spent in complete silence.", "Kalika forest, Ranikhet · from ₹1,200", "/forest-walks.html", "forest-walks", ("forest", 2), "Explore forest walks"),
        ("02", "Birdwatching", "Learning to hear the forest before you see it. Mornings at Kalika, Kasar Devi and the lakes of Sattal, with guides who know these birds by their calls.", "Ranikhet, Kasar Devi, Sattal · from ₹1,500", "/birdwatching.html", "birdwatching", ("lake", 4), "Explore birdwatching"),
        ("03", "Stargazing", "Dark mountain skies, the stories different cultures told about the same stars, and the silence after the stories end.", "Ranikhet, Kasar Devi, Kausani · from ₹1,800", "/stargazing.html", "stargazing", ("night", 3), "Explore stargazing"),
        ("04", "Treks and mountain journeys", "From a gentle forest climb to Pandavkholi to the high meadows of Khalia Top and the Pindari Glacier. Every trek is graded honestly.", "Beginner to challenging · from ₹3,500", "/treks.html", "treks", ("snow", 3), "Explore treks"),
    ]
    ways_html = "".join(f"""<a class="way reveal" href="{href}">
  <div class="way-media">{media(slot, scene, title)}</div>
  <div class="way-body">
    <span class="way-num">{num}</span>
    <h3>{title}</h3>
    <p>{E(desc)}</p>
    <p class="meta">{E(meta)}</p>
    <span class="link-arrow">{label}</span>
  </div>
</a>""" for num, title, desc, meta, href, slot, scene, label in ways)

    featured = "".join(journey_card(journey(s)) for s in FEATURED_JOURNEYS)

    principles = [
        ("Less noise, more attention", "Most travel is built around getting somewhere. Ours is built around noticing where you already are: a call in the canopy, the light changing on a ridge, your own breath on a climb."),
        ("Small groups, on purpose", "Four to ten people, often fewer. Silence is easier to hold, the forest opens differently, and everyone is a person rather than a headcount."),
        ("Nature to experience, not just photograph", "Cameras are welcome. But we plan days around what is worth being present for, not what photographs well."),
        ("Time to observe", "Slow pace, unhurried mornings, and no rush to the next viewpoint. Four to six kilometres a day, not fifteen."),
        ("Respect for the hills and the people in them", "Leave No Trace, always. Home-cooked Kumaoni food, local guides, and conversations with people who actually live here."),
        ("An old idea, in plain words", "Turiya is the awareness beneath waking, dreaming and deep sleep. You do not need to believe anything to walk with us. You only need to be willing to slow down."),
    ]
    principles_html = "".join(f'<div class="principle reveal"><h3>{t}</h3><p>{E(d)}</p></div>' for t, d in principles)

    places_html = "".join(f"""<div class="place reveal"><span class="p-alt">{E(p['alt'])}</span><h3>{E(p['name'])}</h3><p>{E(p['desc'])}</p><p class="p-what">{E(p['what'])}</p></div>""" for p in PLACES)

    steps = [
        ("Message us", "On WhatsApp or through the enquiry form. Tell us what you are looking for. No booking engine."),
        ("We talk first", "A real conversation about the right journey for you, not a sales pitch. Then dates and the full plan."),
        ("Arrive at Oakakhi", "Our home in Ranikhet. Chai first. Nothing is discussed until chai is in hand."),
        ("Walk, watch, rest", "Slow days with guides who know this forest and this sky personally. Evenings by the fire."),
    ]
    steps_html = "".join(f"<li><h3>{t}</h3><p>{E(d)}</p></li>" for t, d in steps)

    voices = "".join(f"""<figure class="reveal"><blockquote class="quote" style="font-size:var(--fs-xl);max-width:none">“{E(p['quote'])}”</blockquote><figcaption class="quote-cite" style="opacity:.75">{E(p['name'])}, {E(p['role'])}</figcaption></figure>""" for p in TEAM)

    posts_html = "".join(post_row(p) for p in journal_posts()[:3])

    body = f"""
<section class="hero">
  <div class="hero-media">{media("home-hero", ("dawn", 7), "", eager=True, sizes="(max-aspect-ratio: 1/1) 220vh, 100vw")}</div>
  <div class="wrap hero-inner">
    <span class="eyebrow">Ranikhet · Kumaun Himalaya</span>
    <h1>Walk slowly. <em>Notice</em> everything.</h1>
    <p class="hero-sub">Small-group journeys, treks, birdwatching and stargazing in the Kumaun Himalaya. Every one of them begins with chai at Oakakhi, our home in Ranikhet.</p>
    <div class="btn-row">
      <a class="btn btn--light" href="/journeys.html">Explore journeys</a>
      <a class="btn btn--ghost-light" href="/experiences.html">Day experiences</a>
    </div>
    <div class="hero-foot">
      <span class="hf-list"><span>Forest walks</span><span>Birdwatching</span><span>Stargazing</span><span>Treks</span></span>
      <span>Groups of 4 to 10</span>
    </div>
  </div>
</section>

<section class="section" id="about">
  <div class="wrap">
    <div class="grid-2 grid-2--wide-right">
      <div class="reveal">{media("home-intro", ("forest", 5), "Oak forest near Ranikhet", cls="media--tall")}</div>
      <div class="reveal">
        <span class="eyebrow">Not another adventure company</span>
        <p class="intro-statement">A journey can be one bird you finally see properly, an hour inside an oak forest, or a single long look at the <em>night sky.</em></p>
        <div class="prose" style="margin-top:2.5rem">
          <p>Every trek we found nearby was either too loud, too fast, or trying to sell us an adventure. Kalika forest, Oakakhi, the Kumaun skies, none of it needed dressing up. It needed someone to slow down enough to actually see it.</p>
          <p>So a guide, an astro storyteller, a documentarian and a small homestay in Ranikhet built something plainer: walk slowly, watch closely, ask real questions, and let the mountains do the rest.</p>
        </div>
        <a class="link-arrow" href="/about.html">Our story</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper" id="experiences">
  <div class="wrap">
    <div class="heading-block reveal">
      <span class="eyebrow">Ways in</span>
      <h2 class="display">Four ways to walk slowly</h2>
      <p class="lede">Book a single morning or evening on its own, or let us weave several into a journey of a few days. Every way in starts from Ranikhet.</p>
    </div>
    <div class="ways">{ways_html}</div>
  </div>
</section>

<section class="pause section--stone">
  <div class="wrap reveal">
    <p class="quote">“What is nature trying to teach you right now?”</p>
    <span class="quote-cite">A walking question</span>
  </div>
</section>

<section class="section" id="journeys">
  <div class="wrap">
    <div class="heading-block reveal">
      <span class="eyebrow">Journeys</span>
      <h2 class="display">Days that are designed, not packaged</h2>
      <p class="lede">Each journey blends forest walks, birds, a night sky and sometimes a trek, around a single place or idea. Prices include stays, meals, guiding and transport during the journey.</p>
    </div>
    <div class="feature-grid">{featured}</div>
    <p style="margin-top:3.5rem"><a class="link-arrow" href="/journeys.html">See all ten journeys</a></p>
  </div>
</section>

<section class="section section--dark" id="philosophy">
  <div class="wrap">
    <div class="grid-2" style="align-items:start">
      <div class="reveal">
        <span class="eyebrow">Our philosophy</span>
        <h2 class="display">Freedom is not running away. Freedom is seeing clearly.</h2>
      </div>
      <div class="reveal">
        <p class="lede">The name comes from <em>Turiya</em>, a word from the Mandukya Upanishad for the awareness beneath waking, dreaming and deep sleep. Always present, rarely noticed. It shapes how we plan every day, in very practical ways.</p>
        <p style="margin-top:2rem"><a class="link-arrow" href="/journal/what-does-turiya-mean.html">What Turiya means</a></p>
      </div>
    </div>
    <div class="principles" style="margin-top:clamp(3.5rem,7vw,6rem)">{principles_html}</div>
  </div>
</section>

<section class="section" id="landscapes">
  <div class="wrap">
    <div class="heading-block reveal">
      <span class="eyebrow">Where we walk</span>
      <h2 class="display">The landscapes of Kumaun</h2>
      <p class="lede">Ranikhet is our home and our base. From there we go to the places we know well, and only those.</p>
    </div>
    <div class="places">{places_html}</div>
  </div>
</section>

<section class="section section--stone">
  <div class="wrap">
    <div class="heading-block reveal">
      <span class="eyebrow">How it works</span>
      <h2 class="h2">From message to mountain</h2>
    </div>
    <ol class="steps reveal">{steps_html}</ol>
    <div class="cols-2" style="margin-top:clamp(3.5rem,6vw,5rem)">
      <div class="reveal">
        <h3 class="h3" style="margin-bottom:1.25rem">Small enough to actually mean it</h3>
        {checklist(["Guides who live in these hills, not flown in for the season", "Groups capped at 10, most trips smaller", "You message the founders directly, not a call centre", "Leave No Trace, always, not just on the poster", "Trained in Himalayan terrain and basic first aid", "Nothing planned around what photographs well"])}
      </div>
      <div class="reveal">
        <h3 class="h3" style="margin-bottom:1.25rem">Woven into every journey</h3>
        {checklist(["Home-cooked Kumaoni food at Oakakhi", "Unhurried mornings, chai before conversation", "Conversations with people who actually live here", "Forest walks led by someone born in these hills", "Evenings by the fire, sometimes under a very dark sky"])}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="heading-block reveal">
      <span class="eyebrow">From the people you will walk with</span>
      <h2 class="h2">Not reviews. Just why we are doing this.</h2>
      <p class="lede">We are a young company, and we would rather show you nothing than show you something made up. Guest stories will appear here once guests have shared them with us.</p>
    </div>
    <div class="people">{voices}</div>
    <p style="margin-top:3rem"><a class="link-arrow" href="/team.html">Meet the guides</a></p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="heading-block reveal">
      <span class="eyebrow">Journal</span>
      <h2 class="h2">Field notes</h2>
      <p class="lede">Short, honest writing on the philosophy, the place and the practicalities. Growing slowly, the way everything else here does.</p>
    </div>
    <ul class="posts" style="list-style:none">{posts_html}</ul>
    <p style="margin-top:3rem"><a class="link-arrow" href="/field-notes.html">Read the journal</a></p>
  </div>
</section>

<section class="section section--stone">
  <div class="wrap">
    <div class="grid-2">
      <div class="reveal">
        <span class="eyebrow">Travelling from abroad</span>
        <h2 class="h2">Come from far away. We will handle the last stretch.</h2>
      </div>
      <div class="reveal">
        <p class="lede">Getting from Delhi to Ranikhet, visas and permits, the best seasons, what to pack, and how to pay from abroad. All in one place, with approximate US dollar prices for every journey.</p>
        <p style="margin-top:2rem"><a class="link-arrow" href="/international.html">Guide for international travellers</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    <div class="heading-block reveal">
      <span class="eyebrow">Questions</span>
      <h2 class="h2">Before you message us</h2>
    </div>
    {faq_block(FAQ[:6])}
    <p style="margin-top:2.5rem"><a class="link-arrow" href="/plan.html#faq">All questions</a></p>
  </div>
</section>

{cta("Find your way into the mountains.")}
"""
    meta = {
        "path": "",
        "title": "Turiya Trails | Slow journeys and treks from Ranikhet, Kumaon",
        "description": "Small-group Himalayan journeys from Oakakhi, Ranikhet: silent forest walks, birdwatching at Kalika, Kasar Devi and Sattal, stargazing, and treks to Pandavkholi, Bharatkot, Khalia Top and Pindari.",
        "jsonld": [ORG_LD, {"@context": "https://schema.org", "@type": "WebSite", "name": "Turiya Trails", "url": SITE["url"] + "/"}],
    }
    return "index.html", page(meta, body, current="", tone="light")


# ---------------------------------------------------------------------------
# Journeys
# ---------------------------------------------------------------------------
JOURNEY_GROUPS = [
    ("Slow days from Oakakhi", "Short journeys that stay close to Ranikhet, each ending with a different kind of walk.", ["kalika-weekend", "into-the-quiet", "where-the-clouds-rest", "the-seekers-ridge"]),
    ("Birds and skies", "Journeys built around a single way of looking.", ["first-light", "three-skies"]),
    ("Mountain journeys", "Further north, higher up, and longer on the trail.", ["above-the-treeline", "where-the-river-begins"]),
    ("Spiritual circuits", "The quiet places of Kumaun, travelled slowly.", ["sub-ek", "the-long-quiet"]),
]


def journeys_index():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Journeys", None)])
    groups = "".join(f"""<section class="reveal" style="margin-top:clamp(4rem,7vw,6rem)">
  <div class="heading-block" style="margin-bottom:2rem"><h2 class="h2">{E(title)}</h2><p class="lede" style="margin-top:.75rem">{E(sub)}</p></div>
  <ul class="journey-list" style="list-style:none">{''.join(journey_row(journey(s)) for s in slugs)}</ul>
</section>""" for title, sub, slugs in JOURNEY_GROUPS)
    body = f"""
{page_hero("Journeys", "Journeys that ask nothing of you except <em>attention</em>", "Small groups of 4 to 10. Slow days in the Kumaun Himalaya, based at Oakakhi in Ranikhet. Every journey includes our forest walks, shared meals, and evenings that end under the sky.", ("dawn", 12), "journeys-hero", crumbs)}
<section class="section" style="padding-top:clamp(3rem,6vw,5rem)">
  <div class="wrap">
    <div class="notice reveal"><p>Prices are per person and include stays, meals, guiding and transport during the journey. Dates run in small batches and are shared on WhatsApp. Want something in between? Any <a href="/experiences.html">day experience</a> can be added to a journey, or we can shape one around your group.</p></div>
    {groups}
  </div>
</section>
{cta("Not sure which one fits?", "Tell us how many days you have and how much walking you enjoy. We will suggest one or two journeys, honestly.")}
"""
    meta = {
        "path": "journeys.html",
        "title": "Journeys in the Kumaon Himalaya | Turiya Trails, Ranikhet",
        "description": "Ten small-group journeys from Ranikhet: slow days at Oakakhi, Pandavkholi, Pinnath and Bharatkot treks, birding at Sattal and Pangot, stargazing circuits, Khalia Top and the Pindari Glacier.",
        "jsonld": [crumbs_ld, {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": url(f"journeys/{j['slug']}.html"), "name": j["name"]} for i, j in enumerate(JOURNEYS)]}],
    }
    return "journeys.html", page(meta, body, current="journeys.html")


SEO_TITLES = {
    "kalika-weekend": "nature weekend in Ranikhet",
    "into-the-quiet": "Pandavkholi trek from Ranikhet",
    "where-the-clouds-rest": "Pinnath trek near Kausani",
    "the-seekers-ridge": "Bharatkot trek from Ranikhet",
    "first-light": "Sattal and Pangot birding tour",
    "three-skies": "Kumaon stargazing tour",
    "above-the-treeline": "Khalia Top trek, Munsyari",
    "where-the-river-begins": "Pindari Glacier trek",
    "sub-ek": "Kainchi Dham circuit",
    "the-long-quiet": "a week in Kumaon",
}


def journey_page(j):
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Journeys", "journeys.html"), (j["name"], None)])
    is_soon = j["status"] == "soon"
    ask_text = (f"Namaste, please tell me when {j['name']} opens for booking." if is_soon
                else f"Namaste Turiya Trails, I would like to know the next dates for {j['name']}.")
    itinerary = "".join(f"<li><h3>{E(t)}</h3><p>{E(d)}</p></li>" for t, d in j["itinerary"])
    intro = "".join(f"<p>{E(p)}</p>" for p in j["intro"])
    trek_html = ""
    if j.get("trek"):
        t = trek(j["trek"])
        trek_html = f"""<section><h2>The trek</h2><p class="prose">{E(t['name'])} · {E(t['level'])} · {E(t['where'])}. {E(t['desc'])}</p><a class="link-arrow" href="/treks.html#{t['slug']}">More about {E(t['name'])}</a></section>"""
    alt_price = f'<p class="ac-note">{E(j["price_alt"])}</p>' if j.get("price_alt") else ""
    others = [x for x in JOURNEYS if x["slug"] != j["slug"] and x["status"] != "soon"]
    others = sorted(others, key=lambda x: (x["kind"] != j["kind"], abs(x["price"] - j["price"])))[:3]
    body = f"""
{page_hero(f"{j['kind']} · {j['level']}", E(j['name']), j['summary'], j['art'], j['photo'], crumbs,
           [("Duration", duration(j)), ("Route", j['route']), ("Level", j['level']), ("Price", price_label(j) + " pp")])}
<section class="section">
  <div class="wrap">
    <div class="detail">
      <div class="detail-main">
        <section class="prose reveal">{intro}</section>
        <section class="reveal"><h2>Day by day</h2><ol class="itinerary">{itinerary}</ol></section>
        {f'<section><h2>From the trail</h2>{gallery(j["gallery"], "Photographs from our own walks on this route.")}</section>' if j.get("gallery") else ""}
        {trek_html}
        <section class="cols-2 reveal">
          <div><h2>Who it suits</h2>{checklist(j['for'])}</div>
          <div><h2>How fit you need to be</h2><p class="prose">{E(j['fitness'])}</p></div>
        </section>
        <section class="cols-2 reveal">
          <div><h2>Included</h2>{checklist(j['included'])}</div>
          <div><h2>Not included</h2>{checklist(j['excluded'])}</div>
        </section>
        <section class="reveal"><h2>When to go</h2><p class="prose">{E(j['season'])}</p></section>
        <section class="reveal"><h2>Before you book</h2>{faq_block(faq_pick('Where do journeys start?', 'How do I book?', 'I am travelling from abroad. Can I join?', 'What happens in an emergency?'))}</section>
      </div>
      <aside class="aside-card" aria-label="Price and booking">
        <p class="ac-price">{price_label(j)}</p>
        <p class="ac-note">{PRICE_NOTE}{', ' + duration(j) if not j.get('price_alt') else ''}<br>About {usd(j['price'])} · <a href="/international.html">travelling from abroad?</a></p>
        {alt_price}
        <dl>
          <div><dt>Starts</dt><dd>Ranikhet</dd></div>
          <div><dt>Level</dt><dd>{E(j['level'])}</dd></div>
          <div><dt>Group</dt><dd>4 to 10 people</dd></div>
          <div><dt>Dates</dt><dd>{'Opening soon' if is_soon else 'Shared on WhatsApp'}</dd></div>
        </dl>
        <a class="btn btn--solid" href="{wa(ask_text)}">{WA_ICON} {'Tell me when it opens' if is_soon else 'Ask about dates'}</a>
        <a class="btn btn--line" href="/plan.html?journey={j['slug']}">Send an enquiry</a>
        <p class="ac-fine">No payment is taken on this website. We talk with you first, then confirm dates, the full plan and how to reserve your place.</p>
      </aside>
    </div>
  </div>
</section>
<section class="section section--paper">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">You might also like</span><h2 class="h2">Other journeys</h2></div>
    <div class="feature-grid">{''.join(journey_card(o) for o in others)}</div>
  </div>
</section>
{cta()}
"""
    trip_ld = {
        "@context": "https://schema.org", "@type": "TouristTrip",
        "name": j["name"], "description": j["summary"],
        "url": url(f"journeys/{j['slug']}.html"),
        "touristType": [j["kind"]],
        "itinerary": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {"@type": "Place", "name": p}} for i, p in enumerate(j["places"])]},
        "provider": {"@type": "TravelAgency", "name": "Turiya Trails", "url": SITE["url"] + "/"},
    }
    if not is_soon:
        trip_ld["offers"] = {"@type": "Offer", "price": j["price"], "priceCurrency": "INR", "url": url(f"journeys/{j['slug']}.html")}
    meta = {
        "path": f"journeys/{j['slug']}.html",
        "title": f"{j['name']}: {SEO_TITLES[j['slug']]} | Turiya Trails",
        **({"image": photo_sources(j["photo"])["fallback"]} if photo_sources(j["photo"]) else {}),
        "description": f"{j['summary']} {duration(j).capitalize()} from Ranikhet, {price_label(j)} {PRICE_NOTE}.",
        "jsonld": [crumbs_ld, trip_ld],
    }
    return f"journeys/{j['slug']}.html", page(meta, body, current="journeys.html")


# ---------------------------------------------------------------------------
# Day experiences
# ---------------------------------------------------------------------------
def session_rows(items):
    return "".join(f"""<div class="session reveal">
  <div><h3>{E(s['name'])}</h3><span class="s-where">{E(s['where'])} · {E(s['length'])}</span></div>
  <p class="s-desc">{E(s['desc'])}</p>
  <div class="s-price">{rupees(s['price'])}<small>{PRICE_NOTE} · ≈ {usd(s['price'])}</small><a class="link-arrow" href="{wa(f"Namaste Turiya Trails, I would like to book: {s['name']}. Please share available dates.")}">Ask about dates</a></div>
</div>""" for s in items)


def experiences():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Day experiences", None)])
    groups = "".join(f"""<section style="margin-top:clamp(4rem,7vw,6rem)">
  <div class="reveal" style="display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;margin-bottom:1.5rem">
    <h2 class="h2">{E(g['group'])}</h2>
    <a class="link-arrow" href="/{g['page']}">About {E(g['group'].lower())}</a>
  </div>
  <div class="sessions">{session_rows(g['items'])}</div>
</section>""" for g in SESSIONS)
    body = f"""
{page_hero("Day experiences", "A morning, an evening, or a <em>single</em> day", "Not every visit needs a multi-day journey. Book a forest walk, a birding morning, a night under the sky or a day trek on its own, wherever you are staying.", ("mist", 14), "experiences-hero", crumbs)}
<section class="section" style="padding-top:clamp(3rem,6vw,5rem)">
  <div class="wrap">
    <div class="notice reveal">{''.join(f'<p>{E(t)}</p>' for t in SESSION_TERMS)}</div>
    {groups}
  </div>
</section>
<section class="section section--stone">
  <div class="wrap">
    <div class="grid-2">
      <div class="reveal">
        <span class="eyebrow">Combine them</span>
        <h2 class="h2">Two sessions make a day. Three make a weekend.</h2>
      </div>
      <div class="reveal">
        <p class="lede">If you are staying at Oakakhi for a few nights, we can join a birding morning, a nature class and an astro night into one unhurried stay. The <a href="/journeys/kalika-weekend.html">Kalika Weekend</a> is exactly that, already planned.</p>
        <p style="margin-top:2rem"><a class="link-arrow" href="/journeys.html">See all journeys</a></p>
      </div>
    </div>
  </div>
</section>
{cta()}
"""
    offers = [{"@type": "Offer", "name": s["name"], "price": s["price"], "priceCurrency": "INR"} for g in SESSIONS for s in g["items"]]
    meta = {
        "path": "experiences.html",
        "title": "Birdwatching, stargazing and forest walks in Ranikhet | Turiya Trails",
        "description": "Book a single experience in Kumaun: silent forest walks at Kalika, birdwatching at Ranikhet, Kasar Devi and Sattal, astro nights, nature classes and day treks to Pandavkholi and Pinnath.",
        "jsonld": [crumbs_ld, {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Day experiences", "itemListElement": offers}],
    }
    return "experiences.html", page(meta, body, current="experiences.html")


def experience_page(path, title_tag, desc, eyebrow, h1, lede, scene, slot, intro_title, intro_paras, quote, notice_title, notice_items, howto, facts, group_name, journeys_with, extra=""):
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Day experiences", "experiences.html"), (eyebrow, None)])
    sessions = next(g for g in SESSIONS if g["group"] == group_name)["items"]
    notice_html = "".join(f'<div class="place reveal"><h3 style="font-size:1.5rem">{E(n)}</h3><p>{E(d)}</p></div>' for n, d in notice_items)
    facts_html = "".join(f'<div class="reveal"><span class="eyebrow" style="margin-bottom:.75rem">{E(k)}</span><p class="prose">{E(v)}</p></div>' for k, v in facts)
    jw = "".join(journey_card(journey(s)) for s in journeys_with)
    body = f"""
{page_hero(eyebrow, h1, lede, scene, slot, crumbs)}
<section class="section">
  <div class="wrap">
    <div class="grid-2" style="align-items:start">
      <div class="reveal"><span class="eyebrow">The experience</span><h2 class="h2">{intro_title}</h2></div>
      <div class="prose reveal">{''.join(f'<p>{E(p)}</p>' for p in intro_paras)}</div>
    </div>
  </div>
</section>
<section class="pause section--stone"><div class="wrap reveal"><p class="quote">“{E(quote)}”</p><span class="quote-cite">The Turiya Trails way</span></div></section>
<section class="section">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">{E(notice_title[0])}</span><h2 class="h2">{E(notice_title[1])}</h2></div>
    <div class="places">{notice_html}</div>
    {extra}
  </div>
</section>
<section class="section section--paper">
  <div class="wrap">
    <div class="grid-2" style="align-items:start">
      <div class="reveal"><span class="eyebrow">How it works</span><h2 class="h2">What a session looks like</h2><div style="margin-top:2rem">{checklist(howto)}</div></div>
      <div class="stack">{facts_html}</div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">Book a session</span><h2 class="h2">On its own</h2></div>
    <div class="sessions">{session_rows(sessions)}</div>
    <p class="small muted" style="margin-top:1.5rem">{E(' '.join(SESSION_TERMS))}</p>
  </div>
</section>
<section class="section section--paper">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">Or as part of a journey</span><h2 class="h2">Journeys that include it</h2></div>
    <div class="feature-grid">{jw}</div>
  </div>
</section>
{cta()}
"""
    meta = {"path": path, "title": title_tag, "description": desc, "jsonld": [crumbs_ld]}
    return path, page(meta, body, current="experiences.html")


def forest_walks():
    return experience_page(
        "forest-walks.html",
        "Silent forest walks in Ranikhet, Kalika forest | Turiya Trails",
        "Slow, silent walks through the oak and rhododendron of Kalika forest near Ranikhet. Two to three hours at sunrise or late afternoon, from ₹1,200 per person.",
        "Silent forest walks", "Walking as a practice of <em>presence</em>",
        "In oak and rhododendron forests that have stood for centuries, we walk slowly enough to notice what rushing past would erase.",
        ("forest", 9), "forest-walks-hero",
        "Walking as a practice, not a sport",
        ["We live in a world that has turned walking into exercise and forests into photo opportunities. Our silent forest walks are something different, a deliberate return to presence, where the goal is not a destination but attention.",
         "The oak and rhododendron forests around Ranikhet are among the most intact in the Kumaun Himalaya. Walking through them slowly, you begin to notice the texture of bark, the sound of wind through different trees, and the way light changes through the canopy at different times of day."],
        "The forest does not care how fast you walk. It rewards only those who stop.",
        ("What we notice", "The forest up close"),
        [("Banj oak", "The defining tree of the Kumaun forests. Wide-trunked, covered in moss and ferns, and long valued by local communities as a keeper of water on the hillside."),
         ("Buransh", "The rhododendron is Uttarakhand's state tree. It blooms red in March and April, and locals make a deep red juice from the flowers."),
         ("Moss and ferns", "The floor of a healthy Kumaun forest is carpeted in them. Our guides can name many and explain the part they play."),
         ("Forest light", "Early morning brings shafts through mist, afternoon brings dappled patches. Cameras struggle with it. You have to be there.")],
        ["Starts at sunrise or late afternoon, never midday", "Complete silence for the first 30 minutes", "The guide leads, stops often, and points without speaking", "A walking question at the start, to carry with you", "Slower than feels natural at first", "Chai and conversation after, back at Oakakhi"],
        [("The trail", "The Kalika forest trail, starting from Oakakhi. Gentle gradients on well-kept paths. Suitable for all fitness levels."),
         ("Duration", "Two to three hours. Some walks cover three kilometres in three hours. That is not inefficiency, that is the point."),
         ("Group size", "A maximum of six people. Silence is harder to hold in larger groups.")],
        "Silent forest walks", ["kalika-weekend", "into-the-quiet", "where-the-clouds-rest"])


def birdwatching():
    return experience_page(
        "birdwatching.html",
        "Birdwatching in Kumaon: Ranikhet, Kasar Devi, Sattal | Turiya Trails",
        "Guided birdwatching mornings in the Kumaun Himalaya at Kalika forest (Ranikhet), Kasar Devi and the Sattal hides, plus the First Light birding journey to Pangot. From ₹1,500 per person.",
        "Birdwatching", "Learning to <em>see</em> a forest",
        "The Himalayan forests around Ranikhet and Binsar host over 200 species of birds. Our guides teach you to hear the forest before you see it.",
        ("lake", 8), "birdwatching-hero",
        "A living community, hiding in plain sight",
        ["Most people look at a forest and see trees. A birdwatcher looks at the same forest and sees a living community of hundreds of species, each with a role, a voice and a story. Our birdwatching mornings teach you to slow down enough to notice what has always been there.",
         "The Kumaun Himalaya is one of India's richest birding regions, where the plains meet the mountains. We walk at Kalika near Oakakhi, on the Kasar Devi ridge above Almora, and at the hides by the Sattal lakes."],
        "The forest does not perform for you. You must become quiet enough that it forgets you are there.",
        ("Residents of the Kumaun forests", "Birds you may encounter"),
        [("Great Barbet", "Its loud, mournful call is the unofficial soundtrack of the Kumaun forests. Brightly coloured, usually heard high in tall trees before it is seen."),
         ("Khalij Pheasant", "A forest pheasant often heard before seen. Its calls carry through the understorey at dawn around Ranikhet and Kalika."),
         ("Black Francolin", "Heard in the early mornings around Oakakhi. A ground bird with a sharp, repeating call."),
         ("Verditer Flycatcher", "A flash of blue at the forest edge, and one of the birds on our home list at Kalika."),
         ("Lammergeier", "The bearded vulture rides thermals for hours over the ridges. One of the most dramatic birds of the Himalaya."),
         ("Himalayan Monal", "Uttarakhand's state bird, found higher up between about 2,500 and 4,500 metres. A possibility on our mountain journeys, not at Ranikhet.")],
        ["An early start, 5:30 to 6am, when birds are most active", "Walking in silence unless the guide signals", "Birds identified by call before sight", "Binoculars and a field guide provided", "Two to three hours covering two or three kilometres, slowly", "Tea afterwards and a look back at what was seen", "No target list. Presence over checklist."],
        [("Where we go", "Kalika forest and the oak forests around Oakakhi, the Kasar Devi ridge, and the Sattal lakes. On First Light, also Pangot and Kilbury."),
         ("Best season", "March to June for summer migrants and breeding plumage. October to February for winter species. Each season is a different forest."),
         ("Group size", "A maximum of six people. Smaller groups see more.")],
        "Birdwatching", ["first-light", "kalika-weekend", "into-the-quiet"],
        extra=('<div style="margin-top:clamp(3.5rem,6vw,5rem)"><span class="eyebrow">From our camera rolls</span><h3 class="h2" style="margin-bottom:2rem">Birds we have photographed in Kumaun</h3>'
               + gallery([("bird-magpie", "A red-billed blue magpie perched on a post", "Red-billed blue magpie"),
                          ("bird-verditer", "A verditer flycatcher on a wire", "Verditer flycatcher"),
                          ("bird-whistling-thrush", "A blue whistling thrush on a rock", "Blue whistling thrush"),
                          ("bird-kingfisher", "A white-throated kingfisher on a dead branch above a forested slope", "White-throated kingfisher"),
                          ("bird-flameback", "A flameback woodpecker on a bare trunk", "Flameback woodpecker")])
               + '</div><p class="small muted" style="margin-top:1.5rem">Wild birds keep their own schedule. We never guarantee a particular sighting.</p>'))


def stargazing():
    return experience_page(
        "stargazing.html",
        "Stargazing in Ranikhet and Kasar Devi | Turiya Trails",
        "Guided astro nights under the dark skies of the Kumaun Himalaya at Oakakhi, Ranikhet and Kasar Devi, plus the Three Skies stargazing circuit. From ₹1,800 per person.",
        "Stargazing", "The Himalayan sky as a doorway to <em>wonder</em>",
        "At around 1,800 metres, away from city light, the Kumaun night sky is one of the darkest in north India. Stories written in stars, guided with intention.",
        ("night", 8), "stargazing-hero",
        "The sky as a reminder of scale",
        ["Away from city light pollution, the night sky above Ranikhet is dark enough that on a clear, moonless night the Milky Way is not just visible, it is overwhelming. The kind of overwhelming that makes your problems feel appropriately small.",
         "Our astro nights are not astronomy lectures. They are guided moments of stillness under the sky, where stories from different cultures about the same stars remind us that people have always looked up and wondered."],
        "You are not looking at the stars. You are looking back in time, at light that left its source long ago, arriving at your eye tonight.",
        ("What you will see", "Objects in the Himalayan sky"),
        [("The Milky Way", "A dense band of light across the sky on moonless nights. Our own galaxy, seen edge-on. The sight that stops every conversation."),
         ("Orion Nebula", "A fuzzy star in Orion's sword to the naked eye. A stellar nursery about 1,300 light years away."),
         ("Jupiter and Saturn", "Often visible, depending on season. Through binoculars you can see Jupiter's largest moons, the ones Galileo found in 1610."),
         ("Andromeda Galaxy", "The furthest object visible to the naked eye, about 2.5 million light years away."),
         ("Shooting stars", "Several an hour on any clear night, and many more during showers like the Perseids in August."),
         ("The Pleiades", "Krittika in Indian astronomy, the Seven Sisters in Greek myth. Count how many you can see.")],
        ["Begins after dinner, around 8 to 9pm", "A dark field or rooftop away from artificial light", "Stories from Indian, Greek and other sky traditions", "Binoculars for closer views", "Hot chai under the sky", "No phones. Just eyes and the sky.", "A walking question shared before sleep"],
        [("Where we go", "The Oakakhi rooftop and open meadows near Kalika in Ranikhet, the Kasar Devi ridge, and on our Three Skies circuit, Kausani and Mukteshwar."),
         ("Best season", "October to March for the clearest skies. The monsoon brings clouds, but the clarity after the rain in September can be extraordinary. We plan around new moon."),
         ("Group size", "A maximum of eight people, so everyone can sit in comfortable silence.")],
        "Stargazing", ["three-skies", "kalika-weekend", "the-seekers-ridge"],
        extra='<p class="small muted" style="margin-top:1.5rem">The sky depends on the weather. If clouds roll in, we move the session to another night where we can, or tell you honestly that it is not going to clear.</p>')


def nature_classes():
    return experience_page(
        "nature-classes.html",
        "Nature classes in Ranikhet: reading the forest | Turiya Trails",
        "A small, hands-on nature class at Oakakhi, Ranikhet: the trees of the Kumaun forest, bird calls, and keeping a field notebook. Two hours, ₹1,500 per person.",
        "Nature classes", "Reading the <em>forest</em>",
        "A small, hands-on class for anyone who has ever walked through a forest and wished they knew what they were looking at.",
        ("mist", 16), "nature-classes-hero",
        "Names are the start of noticing",
        ["Once you can tell a banj oak from a chir pine, or a barbet's call from a cuckoo's, a forest stops being a green blur. It becomes a place full of particular things.",
         "Our nature class is two unhurried hours at Oakakhi and in the edge of Kalika forest. You learn a few trees, a few calls, and how to keep a simple field notebook, so the next walk you take, anywhere, is a richer one. It suits curious adults and older children alike."],
        "You cannot protect what you cannot name, and you cannot name what you have never stopped to look at.",
        ("What we cover", "A first field course in two hours"),
        [("Trees of the Kumaun forest", "Banj oak, buransh, chir pine and the plants that grow in their shade. How to tell them apart, and why it matters which grows where."),
         ("Learning by ear", "The calls you heard that morning, and how to start recognising birds before you see them."),
         ("The field notebook", "A simple way to record what you notice: sketches, notes and questions. No drawing skill needed."),
         ("Reading signs", "Tracks, feathers, feeding marks and the small clues that tell you who passed by.")],
        ["Small groups, so everyone can ask questions", "Half indoors at Oakakhi, half at the forest edge", "Notebooks and pencils provided", "Suitable for adults and children aged about ten and up", "Pairs well with a birding morning or astro night"],
        [("Where", "Oakakhi and the edge of Kalika forest, Ranikhet."),
         ("When", "Late morning or afternoon, through most of the year."),
         ("Group size", "Up to eight people.")],
        "Nature classes", ["kalika-weekend", "into-the-quiet", "first-light"])


# ---------------------------------------------------------------------------
# Treks
# ---------------------------------------------------------------------------
def treks():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Treks", None)])
    items = []
    for i, t in enumerate(TREKS):
        facts = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in t["facts"])
        part_of = ", ".join(f'<a href="/journeys/{s}.html">{E(journey(s)["name"])}</a>' for s in t["journeys"])
        alone = (f'<p class="small" style="margin-top:1rem"><strong style="font-weight:500">{E(t["standalone_label"])}:</strong> {rupees(t["standalone"])} {PRICE_NOTE}</p>' if t["standalone"] else "")
        order = ' style="order:2"' if i % 2 else ""
        items.append(f"""<article class="grid-2 reveal" id="{t['slug']}" style="margin-top:clamp(4rem,8vw,7rem)">
  <div{order}>{media("trek-" + t['slug'], t['art'], f"{t['name']}, {t['where']}", cls="media--wide")}</div>
  <div>
    <span class="eyebrow">{E(t['level'])} · {E(t['where'])}</span>
    <h2 class="h2">{E(t['name'])}</h2>
    <p class="prose" style="margin-top:1.25rem">{E(t['desc'])}</p>
    <dl class="trek-facts">{facts}</dl>
    <p class="small" style="margin-top:1rem">Part of: {part_of}</p>
    {alone}
    <a class="link-arrow" href="{wa(f"Namaste Turiya Trails, I would like to know the next dates for the {t['name']} trek.")}">Ask about the next batch</a>
  </div>
</article>""")
    body = f"""
{page_hero("Treks", "Walk to notice, not to <em>conquer</em>", "Five trails, graded honestly. These are the treks we know and lead ourselves, from a gentle forest climb to a glacier at the head of a valley.", ("snow", 9), "treks-hero", crumbs, split=True)}
<section class="section" style="padding-top:clamp(3rem,6vw,5rem)">
  <div class="wrap">
    <div class="notice reveal"><p>Each trek lives inside a longer journey, and the shorter ones can also be walked on their own. Groups of 4 to 10, led by our BMC certified lead guide. Dates are released in small batches. Message us and we will tell you what is opening next.</p></div>
    {''.join(items)}
  </div>
</section>
<section class="section section--dark">
  <div class="wrap">
    <div class="grid-2" style="align-items:start">
      <div class="reveal">
        <span class="eyebrow">How we trek</span>
        <h2 class="display">Trekking as a form of inquiry</h2>
        <p class="lede" style="margin-top:1.5rem">There is a version of Himalayan trekking that is about conquest: summits bagged, kilometres logged, photos taken. That is not us. We use the act of walking through mountains for something slower and harder to name.</p>
      </div>
      <div class="reveal">
        {checklist(["A walking question each morning, with no obligation to answer out loud", "A slow pace: 4 to 6 km a day on most treks, not 15", "Simple, fresh food cooked for each meal", "Guides trained in mindful facilitation, not performance", "No competitive atmosphere. Everyone moves at their own pace.", "Campfire conversations in the evening, never forced", "Digital detox encouraged, not enforced", "An honest conversation about readiness before you book"])}
      </div>
    </div>
  </div>
</section>
{cta("Not sure which trail is yours?", "Tell us what walking you have done before. We will be honest about which trek fits, and which one to save for later.")}
"""
    meta = {
        "path": "treks.html",
        "title": "Treks near Ranikhet: Pandavkholi to Pindari | Turiya Trails",
        "description": "Small-group treks in the Kumaun Himalaya, graded honestly: Pandavkholi (beginner), Pinnath (intermediate), Bharatkot (challenging), Khalia Top in Munsyari and the Pindari Glacier.",
        "jsonld": [crumbs_ld],
    }
    return "treks.html", page(meta, body, current="treks.html")


# ---------------------------------------------------------------------------
# Oakakhi
# ---------------------------------------------------------------------------
def oakakhi():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Oakakhi", None)])
    body = f"""
{page_hero("Our base", "Every journey begins at <em>Oakakhi</em>", "A small homestay in the oak forest above Ranikhet, at around 1,800 metres. Chai first. Nothing is discussed until chai is in hand.", ("mist", 20), "oakakhi-hero", crumbs, split="corner")}
<section class="section">
  <div class="wrap">
    <div class="grid-2 grid-2--wide-right">
      <div class="reveal">{media("oakakhi-house", ("forest", 21), "Oakakhi Stays, Ranikhet", cls="media--tall")}</div>
      <div class="reveal">
        <span class="eyebrow">Oakakhi Stays, Ranikhet</span>
        <h2 class="h2">A home, not a base camp</h2>
        <div class="prose" style="margin-top:1.5rem">
          <p>Oakakhi is run by Nishant, our lead guide, who has hosted people here for years. It is where you arrive, where you eat, and where you come back to after a day on the trail.</p>
          <p>The Kalika forest trail starts close by, and so do most of our forest walks and birding mornings. The sky above it is dark enough for our astro nights to happen right here, on the rooftop or in the meadow nearby.</p>
          <p>We do not sell village life as a separate ticket. It is simply how the days already work: chai with Nishant's family, home-cooked Kumaoni meals, and mornings that start slowly because the mountain is not going anywhere.</p>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section section--stone">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">Getting here</span><h2 class="h2">The road to Ranikhet</h2><p class="lede">Ranikhet is in Almora district, Uttarakhand. Times below are approximate and depend on the roads and the season.</p></div>
    <div class="places">
      <div class="place reveal"><span class="p-alt">By train</span><h3>Kathgodam</h3><p>The nearest railway station, about 80 km away. Roughly three hours by road through the hills.</p></div>
      <div class="place reveal"><span class="p-alt">By air</span><h3>Pantnagar</h3><p>The nearest airport, roughly four hours by road.</p></div>
      <div class="place reveal"><span class="p-alt">By road</span><h3>From Delhi</h3><p>About 350 km, a long day's drive via Moradabad and Haldwani, or an overnight train to Kathgodam.</p></div>
    </div>
    <p style="margin-top:2.5rem" class="reveal">Tell us how you are travelling and we will help you plan the last stretch. <a class="link-arrow" href="{SITE['maps']}" rel="noopener">Find Oakakhi on Google Maps</a></p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="cols-2">
      <div class="reveal"><span class="eyebrow">Good to know</span><h2 class="h2">Before you arrive</h2></div>
      <div class="reveal">{checklist(["Mobile signal is patchy at Oakakhi, by design. Ranikhet town has signal.", "Days are pleasant most of the year. Nights are cool, and from October to February you will want warm layers.", "Meals are home-cooked and Kumaoni. Tell us about dietary needs in advance.", "Bring sturdy shoes, a headlamp and less than you think."])}</div>
    </div>
  </div>
</section>
{cta("Come and have chai with us.")}
"""
    meta = {
        "path": "oakakhi.html",
        "title": "Oakakhi Stays, Ranikhet: our base in the Kumaun Himalaya | Turiya Trails",
        "description": "Oakakhi Stays is the homestay in the oak forest above Ranikhet where every Turiya Trails journey begins. Home-cooked Kumaoni food, dark skies, and how to get here from Kathgodam and Delhi.",
        "jsonld": [crumbs_ld, {"@context": "https://schema.org", "@type": "LodgingBusiness", "name": "Oakakhi Stays", "address": {"@type": "PostalAddress", "addressLocality": "Ranikhet", "addressRegion": "Uttarakhand", "addressCountry": "IN"}, "hasMap": SITE["maps"]}],
    }
    return "oakakhi.html", page(meta, body, current="oakakhi.html")


# ---------------------------------------------------------------------------
# About and team
# ---------------------------------------------------------------------------
def about():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("About", None)])
    oath = ["I will walk with awareness, not just legs.", "I will be kind to animals and to the Earth.", "I will leave nature better than I found it.", "I will stay curious. Ask the harder questions.", "I will respect silence and fellow travellers.", "I will return not just changed, but clear."]
    body = f"""
{page_hero("About Turiya Trails", "Not another <em>adventure</em> company", "A guide, an astro storyteller, a documentarian and a small homestay in Ranikhet, building something plainer.", ("dusk", 30), "about-hero", crumbs)}
<section class="section">
  <div class="wrap">
    <div class="grid-2" style="align-items:start">
      <div class="reveal"><span class="eyebrow">Why we started</span><h2 class="h2">Too loud, too fast, or trying to sell an adventure</h2></div>
      <div class="prose reveal">
        <p>Every trek we found nearby was either too loud, too fast, or trying to sell us an adventure. Kalika forest, Oakakhi, the Kumaun skies, none of it needed dressing up. It needed someone to slow down enough to actually see it.</p>
        <p>So a guide, an astro storyteller, a documentarian and a small homestay in Ranikhet built something plainer: walk slowly, watch closely, ask real questions, and let the mountains do the rest.</p>
        <p>The name comes from Turiya, a state of awareness beneath waking, dreaming and deep sleep. Always present, rarely noticed. That is what these journeys are quietly built around.</p>
        <a class="link-arrow" href="/journal/what-does-turiya-mean.html">What Turiya means</a>
      </div>
    </div>
  </div>
</section>
<section class="pause section--stone"><div class="wrap reveal"><p class="quote">“When do you feel most like yourself?”</p><span class="quote-cite">A walking question</span></div></section>
<section class="section">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">Right people, not more people</span><h2 class="h2">Not for everyone. For the right ones.</h2></div>
    <div class="cols-2">
      <div class="reveal"><h3 class="h3" style="margin-bottom:1.25rem">These journeys are for</h3>{checklist(["Spiritual seekers and meditators", "Solo travellers looking for depth", "Nature lovers and birdwatchers", "Stargazers, beginners and experienced alike", "People new to trekking but looking for meaning", "Travellers from abroad looking for the real hills", "Those quietly drawn, not just excited"])}</div>
      <div class="reveal"><h3 class="h3" style="margin-bottom:1.25rem">We gently redirect</h3>{checklist(["Loud adventure tourism", "Party travel and nightlife", "Corporate luxury retreats", "Cheap mass trekking", "Instagram-first experiences"])}</div>
    </div>
  </div>
</section>
<section class="section section--dark">
  <div class="wrap wrap--narrow center">
    <div class="reveal">
      <span class="eyebrow">The Turiya oath</span>
      <h2 class="display" style="margin-bottom:3rem">Words we walk by</h2>
      {''.join(f'<p class="quote" style="font-size:var(--fs-xl);max-width:none;margin:0 auto 1.25rem">{E(o)}</p>' for o in oath)}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="grid-2">
      <div class="reveal"><span class="eyebrow">The people</span><h2 class="h2">Grounded companions, not entertainers</h2></div>
      <div class="reveal"><p class="lede">Trained in Himalayan terrain, safety and first aid, birdwatching and astro storytelling. They speak when the mountain speaks, and stay silent when silence is needed.</p><p style="margin-top:2rem"><a class="link-arrow" href="/team.html">Meet the guides</a></p></div>
    </div>
  </div>
</section>
{cta()}
"""
    meta = {
        "path": "about.html",
        "title": "About Turiya Trails | Conscious travel in the Kumaun Himalaya",
        "description": "Why Turiya Trails exists, what the name means, and who our slow, small-group journeys in Ranikhet and the Kumaun Himalaya are for.",
        "jsonld": [crumbs_ld, ORG_LD],
    }
    return "about.html", page(meta, body, current="about.html")


def team():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("About", "about.html"), ("Guides", None)])
    people = "".join(f"""<article class="person reveal">
  {media(p['photo'], ('mist', 40), f"{p['name']}, {p['role']}", cls="media--portrait", sizes="(min-width: 1240px) 340px, (min-width: 860px) 30vw, 92vw") if photo_sources(p.get('photo', '')) else f'<div class="initial" aria-hidden="true">{E(p["initial"])}</div>'}
  <h3>{E(p['name'])}</h3><span class="role">{E(p['role'])}</span>
  <p>{E(p['bio'])}</p>
  <ul class="chips">{''.join(f'<li>{E(s)}</li>' for s in p['skills'])}</ul>
  <blockquote>“{E(p['quote'])}”</blockquote>
</article>""" for p in TEAM)
    body = f"""
{plain_hero("The people behind Turiya Trails", "Grounded companions, not <em>entertainers</em>", "People trust people, not brochures. Here is who you will actually be walking, watching birds and sitting under the stars with.", crumbs)}
<section class="section" style="padding-top:0">
  <div class="wrap">
    <p class="muted small reveal" style="margin-bottom:3rem">Real people, real photographs. No stock images on this page.</p>
    <div class="people">{people}</div>
  </div>
</section>
<section class="section section--stone">
  <div class="wrap cols-2">
    <div class="reveal"><span class="eyebrow">What connects them</span><h2 class="h2">From these hills, for these hills</h2></div>
    <div class="reveal">{checklist(["All three live in or near the Kumaun hills, not flown in for the season", "Trained in Himalayan safety and basic first aid", "Speak when the mountain speaks, silent when silence is needed", "None of them perform for a camera, including Naveen's own"])}</div>
  </div>
</section>
{cta("Want to meet them yourself?")}
"""
    meta = {
        "path": "team.html",
        "title": "Meet the guides | Turiya Trails, Ranikhet",
        "description": "Meet Nishant, Sachin and Naveen: the lead guide and host, astro storyteller and field documentarian behind Turiya Trails in Ranikhet.",
        "jsonld": [crumbs_ld],
    }
    return "team.html", page(meta, body, current="about.html", tone="dark")


# ---------------------------------------------------------------------------
# Journal
# ---------------------------------------------------------------------------
def journal_index():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Journal", None)])
    posts = journal_posts()
    body = f"""
{plain_hero("Journal", "Notes from the trail and the <em>forest</em>", "Short, honest writing on the philosophy, the place and the practicalities. Growing slowly, the way everything else here does.", crumbs)}
<section class="section" style="padding-top:0">
  <div class="wrap">
    <ul class="posts" style="list-style:none">{''.join(post_row(p) for p in posts)}</ul>
    <div class="grid-2 reveal" style="margin-top:clamp(4rem,8vw,6rem);align-items:start">
      <div><span class="eyebrow">Coming next</span><h2 class="h2">More field notes are on the way</h2></div>
      <ul class="upcoming-posts">
        <li>Birdwatching in the Kumaun hills, a beginner's guide</li>
        <li>What a night sky actually shows you, once you know where to look</li>
        <li>Notes from our first journeys, once guests have walked them</li>
      </ul>
    </div>
  </div>
</section>
{cta()}
"""
    meta = {
        "path": "field-notes.html",
        "title": "Journal: field notes from the Kumaun Himalaya | Turiya Trails",
        "description": "Field notes from Turiya Trails: the meaning of Turiya, practical advice for your first Himalayan trek, and writing on the forests, birds and skies around Ranikhet.",
        "jsonld": [crumbs_ld, {"@context": "https://schema.org", "@type": "Blog", "name": "Turiya Trails Journal", "url": url("field-notes.html"),
                               "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": url(f"journal/{p['slug']}.html"), "datePublished": p["date"]} for p in posts]}],
    }
    return "field-notes.html", page(meta, body, current="field-notes.html", tone="dark")


def article(p, posts):
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Journal", "field-notes.html"), (p["title"], None)])
    others = [x for x in posts if x["slug"] != p["slug"]][:2]
    body = f"""
<article class="article">
  <div class="wrap">
    <header class="article-head">
      {crumbs}
      <span class="eyebrow">Field note {E(p.get('number', ''))} · {E(p.get('category', ''))}</span>
      <h1>{E(p['title'])}</h1>
      <p class="standfirst">{E(p.get('standfirst', ''))}</p>
      <p class="article-meta"><time datetime="{E(p['date'])}">{nice_date(p['date'])}</time> · Turiya Trails</p>
    </header>
    <div class="article-body">{markdown.to_html(p['body'])}</div>
    <footer class="article-foot">
      <span class="eyebrow">Keep reading</span>
      <ul class="posts" style="list-style:none">{''.join(post_row(o) for o in others)}</ul>
      <p style="margin-top:2rem"><a class="link-arrow" href="/field-notes.html">All field notes</a></p>
    </footer>
  </div>
</article>
{cta()}
"""
    ld = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": p["title"], "description": p["description"], "datePublished": p["date"],
        "dateModified": p.get("updated", p["date"]),
        "author": {"@type": "Organization", "name": "Turiya Trails"},
        "publisher": {"@type": "Organization", "name": "Turiya Trails", "logo": {"@type": "ImageObject", "url": SITE["url"] + "/assets/img/icon-512.png"}},
        "mainEntityOfPage": url(f"journal/{p['slug']}.html"),
        "image": url("assets/img/og-default.jpg"),
    }
    meta = {
        "path": f"journal/{p['slug']}.html",
        "title": f"{p['title']} | Turiya Trails",
        "description": p["description"],
        "og_type": "article",
        "jsonld": [crumbs_ld, ld],
    }
    return f"journal/{p['slug']}.html", page(meta, body, current="field-notes.html", tone="dark")


# ---------------------------------------------------------------------------
# Plan / enquiry
# ---------------------------------------------------------------------------
def plan():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Plan your journey", None)])
    options = ['<option value="">I am not sure yet, help me choose</option>']
    options.append('<optgroup label="Journeys">' + "".join(f'<option value="{E(j["name"])}" data-slug="{j["slug"]}">{E(j["name"])} · {duration(j)}</option>' for j in JOURNEYS) + "</optgroup>")
    for g in SESSIONS:
        options.append(f'<optgroup label="{E(g["group"])}">' + "".join(f'<option value="{E(s["name"])}">{E(s["name"])}</option>' for s in g["items"]) + "</optgroup>")
    steps = [
        ("Send your message", "The form opens WhatsApp with your details already written. You press send."),
        ("We reply personally", "One of the founders, not a call centre."),
        ("We talk it through", "Which journey fits, dates, what to bring, and anything you are unsure about."),
        ("You confirm", "Only once you are happy. We explain how to reserve your place at that point."),
    ]
    body = f"""
{plain_hero("Plan your journey", "Tell us what you are <em>looking for</em>", "A few details are enough. We will reply personally and help you find the right walk, sky or forest, or tell you honestly if we are not the right fit.", crumbs)}
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grid-2" style="align-items:start">
      <form class="form reveal" id="enquiry-form" data-phone="{SITE['phone_wa']}" novalidate>
        <div class="form-row">
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-people">Number of people</label><input id="f-people" name="people" type="number" min="1" max="20" inputmode="numeric" placeholder="2"></div>
        </div>
        <div class="field"><label for="f-interest">What interests you</label><select id="f-interest" name="interest">{''.join(options)}</select></div>
        <div class="field"><label for="f-dates">Approximate dates</label><input id="f-dates" name="dates" type="text" placeholder="For example, a weekend in late November"></div>
        <div class="field"><label for="f-message">Anything else we should know</label><textarea id="f-message" name="message" placeholder="Your walking experience, dietary needs, questions…"></textarea></div>
        <div><button class="btn btn--solid" type="submit">{WA_ICON} Continue on WhatsApp</button></div>
        <p class="form-note">This opens WhatsApp with your message ready to send to {SITE['phone_display']}. Nothing is stored on this website.</p>
      </form>
      <div class="reveal">
        <span class="eyebrow">What happens next</span>
        <ol class="steps" style="grid-template-columns:1fr;gap:0">{''.join(f'<li><h3>{t}</h3><p>{E(d)}</p></li>' for t, d in steps)}</ol>
        <div class="notice" style="margin-top:2rem"><p>Prefer to just talk? Message <a href="{wa('Namaste Turiya Trails, I found you through the website and would like to know more.')}">{SITE['phone_display']}</a> on WhatsApp, or email <a href="mailto:{SITE['email']}?subject=Planning%20a%20journey">{SITE['email']}</a>.</p><p>Travelling from abroad? Start with our <a href="/international.html">guide for international travellers</a>.</p></div>
      </div>
    </div>
  </div>
</section>
<section class="section section--paper" id="faq">
  <div class="wrap wrap--narrow">
    <div class="heading-block reveal"><span class="eyebrow">Questions</span><h2 class="h2">Before you message us</h2></div>
    {faq_block(FAQ)}
  </div>
</section>
"""
    meta = {
        "path": "plan.html",
        "title": "Plan your journey | Turiya Trails, Ranikhet",
        "description": "Enquire about a Turiya Trails journey, trek or day experience in the Kumaun Himalaya. Tell us what you are looking for and we will reply personally on WhatsApp.",
        "jsonld": [crumbs_ld],
    }
    return "plan.html", page(meta, body, current="plan.html", tone="dark")


# ---------------------------------------------------------------------------
# Small pages
# ---------------------------------------------------------------------------
def international():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("International travellers", None)])
    starts = ["into-the-quiet", "sub-ek", "where-the-river-begins"]
    prices = "".join(f"""<div class="session reveal">
  <div><h3>{E(j['name'])}</h3><span class="s-where">{duration(j)} · {E(j['route'])}</span></div>
  <p class="s-desc">{E(j['kind'])} · {E(j['level'])}{' · opening soon' if j['status'] == 'soon' else ''}</p>
  <div class="s-price">{price_label(j)}<small>≈ {usd(j['price'])} {PRICE_NOTE}</small><a class="link-arrow" href="/journeys/{j['slug']}.html">See the journey</a></div>
</div>""" for j in JOURNEYS)
    facts = [("Base", "Ranikhet, about 1,800 m"), ("Nearest railway", "Kathgodam"), ("Nearest airport", "Pantnagar"), ("Time zone", "IST, UTC+5:30")]
    route = [
        ("Fly into Delhi", "Indira Gandhi International Airport (DEL) is the usual way in. Give yourself a night in Delhi to recover from the flight."),
        ("Train to Kathgodam", "Kathgodam is the railhead for the Kumaun hills. The Shatabdi runs by day in about six hours, and the Ranikhet Express overnight. Book early on the Indian Railways website or through an agent."),
        ("Up into the hills", "From Kathgodam it is about three hours by road to Ranikhet. Tell us your train and we will help you arrange the drive."),
        ("Chai at Oakakhi", "You arrive at our home in Ranikhet. Everything else is ours to plan."),
    ]
    route_html = "".join(f"<li><h3>{t}</h3><p>{E(d)}</p></li>" for t, d in route)
    body = f"""
{page_hero("For international travellers", "Welcome to the <em>Kumaun</em> Himalaya", "Everything you need to plan a journey with us from abroad: getting from Delhi to Ranikhet, visas and permits, the best seasons, staying safe and well, and how prices work.", ("snow", 31), "international-hero", crumbs, facts)}

<section class="section">
  <div class="wrap">
    <div class="grid-2" style="align-items:start">
      <div class="reveal"><span class="eyebrow">Why come here</span><h2 class="h2">The quieter side of the Himalaya</h2></div>
      <div class="prose reveal">
        <p>Kumaun is the eastern half of Uttarakhand: oak and rhododendron forest, long views of the high Himalaya, small villages, and far fewer visitors than the better-known trails of Himachal or Nepal.</p>
        <p>We are a small team based in Ranikhet. You stay with us at Oakakhi, a family-run home, and walk with guides who grew up in these hills. Groups are small, the pace is slow, and you can message the founders directly at every step, in English.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">Getting here</span><h2 class="h2">From Delhi to Ranikhet</h2><p class="lede">Most international guests come through Delhi. Allow a full day of travel each way between Delhi and Ranikhet.</p></div>
    <ol class="steps reveal">{route_html}</ol>
    <p class="small muted reveal" style="margin-top:2rem">Other options: fly from Delhi to Pantnagar, then about four hours by road; or drive from Delhi in about nine to ten hours.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">Where to start</span><h2 class="h2">Good first journeys for visitors from abroad</h2></div>
    <div class="feature-grid">{''.join(journey_card(journey(x)) for x in starts)}</div>
  </div>
</section>

<section class="section section--stone">
  <div class="wrap">
    <div class="cols-2">
      <div class="reveal">
        <span class="eyebrow">Visas and permits</span>
        <h2 class="h3" style="margin-bottom:1.25rem">Paperwork, simply</h2>
        <div class="prose">
          <p>Most visitors need a visa for India. Many nationalities can apply online for an e-Visa. Always use the official Government of India website, <a href="https://indianvisaonline.gov.in/" rel="noopener">indianvisaonline.gov.in</a>, and apply well before you travel.</p>
          <p>Some areas near India's northern borders need special permits for foreign nationals. Before you book a mountain journey such as Above the Treeline (Munsyari) or Where the River Begins (Pindari), we check the current rules for your nationality and help with any permit that is needed. Carry your passport and visa on every journey.</p>
        </div>
      </div>
      <div class="reveal">
        <span class="eyebrow">When to come</span>
        <h2 class="h3" style="margin-bottom:1.25rem">The seasons</h2>
        {checklist(["October and November: clear skies, long mountain views, and the best stargazing", "December to February: cold and clear, with snow higher up", "March to May: rhododendrons in flower and the busiest birding months", "June to September: monsoon. Green and beautiful, but we avoid long treks", "Pindari: May to June, and September to October"])}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cols-2">
      <div class="reveal">
        <span class="eyebrow">Health and safety</span>
        <h2 class="h3" style="margin-bottom:1.25rem">Travelling well</h2>
        {checklist(["Ranikhet sits at about 1,800 m, which most people barely notice. Khalia Top and Pindari reach about 3,500 to 3,600 m, so we walk slowly and build in time to adjust.", "We strongly recommend travel insurance that covers trekking at the altitude of your journey and emergency evacuation.", "Our guides carry first aid and are trained in immediate response.", "Solo travellers, including women travelling alone, are very welcome. You stay in a family home, groups are small, and you can reach the founders directly.", "Tell us about dietary needs or allergies before you arrive. Meals are home-cooked and fresh."])}
      </div>
      <div class="reveal">
        <span class="eyebrow">Money and staying in touch</span>
        <h2 class="h3" style="margin-bottom:1.25rem">Practical things</h2>
        {checklist(["Prices are set in Indian rupees. Dollar figures on this site are approximate and for guidance only.", "When we confirm your place, we explain how to pay from abroad.", "Ranikhet town has ATMs. Carry some cash for small purchases in villages.", "Buy an Indian SIM card on arrival, with your passport. We coordinate on WhatsApp and email.", "Mobile signal is patchy on the trails, and that is part of the point."])}
      </div>
    </div>
  </div>
</section>

<section class="pause section--stone"><div class="wrap reveal"><p class="quote">“Dress modestly at temples, take your shoes off at the door, and ask before photographing people. The hills will do the rest.”</p><span class="quote-cite">A few gentle customs</span></div></section>

<section class="section">
  <div class="wrap">
    <div class="heading-block reveal"><span class="eyebrow">Prices</span><h2 class="h2">Every journey, in rupees and dollars</h2><p class="lede">Per person, including stays, meals, guiding and transport during the journey. Dollar prices are approximate, at about ₹{USD_RATE} to the dollar.</p></div>
    <div class="sessions">{prices}</div>
  </div>
</section>

<section class="section section--dark cta">
  <div class="wrap reveal">
    <span class="eyebrow">Write to us</span>
    <h2>Tell us where you are coming from.</h2>
    <p>Write in English, from any time zone. We are in India Standard Time (UTC+5:30), and one of the founders replies personally.</p>
    <div class="btn-row">
      <a class="btn btn--light" href="mailto:{SITE['email']}?subject=Journey%20enquiry%20from%20abroad">Email {SITE['email']}</a>
      <a class="btn btn--ghost-light" href="{wa('Hello Turiya Trails, I am travelling from abroad and would like to know more about your journeys.')}">{WA_ICON} WhatsApp us</a>
    </div>
  </div>
</section>
"""
    meta = {
        "path": "international.html",
        "title": "Himalaya trips for international travellers | Turiya Trails",
        "description": "Planning a Himalayan trek or nature journey in Uttarakhand from abroad? Getting from Delhi to Ranikhet, visas, permits, seasons, safety and prices in US dollars, from Turiya Trails.",
        "jsonld": [crumbs_ld],
    }
    return "international.html", page(meta, body, current="international.html")


def privacy():
    crumbs, crumbs_ld = breadcrumbs([("Home", ""), ("Privacy", None)])
    body = f"""
{plain_hero("Privacy", "Short, honest, and <em>actually true</em>", "No legal boilerplate that does not match what this site actually does.", crumbs)}
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="prose reveal" style="max-width:40rem">
      <p>This website does not have accounts, cookies for tracking, analytics, or a database collecting your information. There is no newsletter signup that stores your email.</p>
      <p>Every “Book”, “Ask” and “Enquire” button opens WhatsApp with a pre-filled message, sent directly to the Turiya Trails number. The enquiry form works the same way: it builds a message in your browser and opens WhatsApp. Nothing you type is sent to or stored by this website.</p>
      <p>If you email us at {SITE['email']}, we use your address only to reply to you.</p>
      <p>If you message us on WhatsApp, that conversation lives on WhatsApp, governed by WhatsApp's own privacy terms, not ours. We do not sell, share, or use your number for anything beyond the conversation you started.</p>
      <p>Our hosting provider may log basic technical information, such as IP address and browser type, as part of standard web hosting. We do not access or use this data ourselves.</p>
      <p>If anything here changes, this page will change with it. If you have a question we have not answered, ask us directly on WhatsApp.</p>
    </div>
  </div>
</section>
{cta("Questions? Just ask.")}
"""
    meta = {"path": "privacy.html", "title": "Privacy | Turiya Trails", "description": "How the Turiya Trails website handles your information: no tracking, no accounts, and enquiries sent directly over WhatsApp.", "jsonld": [crumbs_ld]}
    return "privacy.html", page(meta, body, tone="dark")


def not_found():
    body = f"""
{plain_hero("Lost the trail", "This path does not <em>go anywhere</em>", "The page you were looking for has moved or never existed. The forest is still here, though.")}
<section class="section" style="padding-top:0"><div class="wrap btn-row">
  <a class="btn btn--solid" href="/">Back to the homepage</a>
  <a class="btn btn--line" href="/journeys.html">See all journeys</a>
</div></section>
"""
    meta = {"path": "404.html", "title": "Page not found | Turiya Trails", "description": "This page could not be found.", "noindex": True}
    return "404.html", page(meta, body, tone="dark")


def redirect(old, new, title):
    target = "/" + new
    html = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<title>{E(title)} | Turiya Trails</title>
<link rel="canonical" href="{url(new)}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target}">
</head>
<body>
<p>This page has moved to <a href="{target}">{E(title)}</a>.</p>
</body>
</html>
"""
    return old, html


def all_pages():
    posts = journal_posts()
    out = [home(), journeys_index(), experiences(), forest_walks(), birdwatching(), stargazing(), nature_classes(),
           treks(), oakakhi(), about(), team(), journal_index(), plan(), international(), privacy(), not_found(),
           redirect("conscious-treks.html", "treks.html", "Treks")]
    out += [journey_page(j) for j in JOURNEYS]
    out += [article(p, posts) for p in posts]
    return out
