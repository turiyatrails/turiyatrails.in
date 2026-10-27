"""Shared page pieces: <head>, navigation, footer and image slots."""
import json
import os
from html import escape

from . import art
from .data import NAV, SITE, wa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_DIR = os.path.join(ROOT, "assets", "img", "photos")

# Fonts are self-hosted (assets/fonts) so pages do not wait on a third-party server.
FONT_FACES = open(os.path.join(ROOT, "assets", "css", "fonts.css"), encoding="utf-8").read()

WA_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3a.5.5 0 0 0 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.1.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3Z"/></svg>')


def url(path=""):
    return SITE["url"].rstrip("/") + "/" + path.lstrip("/")


# Widths generated for every photo. The browser picks the smallest that looks sharp.
PHOTO_WIDTHS = (480, 800, 1200, 1600)


def photo_sources(slot):
    """Return the optimised versions of a photo if one has been added for this slot."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        original = os.path.join(PHOTO_DIR, f"{slot}.{ext}")
        if os.path.exists(original):
            return {
                "fallback": f"/assets/img/photos/{slot}.{ext}",
                "webp": [(f"/assets/img/photos/out/{slot}-{w}.webp", w) for w in PHOTO_WIDTHS
                         if os.path.exists(os.path.join(PHOTO_DIR, "out", f"{slot}-{w}.webp"))],
            }
    return None


# Where the subject sits in a photo, so cropping keeps it in view (CSS object-position).
# A pair means (wide screens, phones).
FOCUS = {
    "home-hero": "57% 60%",
    "home-intro": "50% 60%",
    "journey-into-the-quiet": "50% 75%",
    "journey-the-seekers-ridge": "50% 70%",
    "journey-where-the-river-begins": "50% 40%",
    "trek-pandavkholi": "55% 60%",
    "trek-bharatkot": "60% 60%",
    "journeys-hero": "50% 62%",
    "treks-hero": ("0% 70%", "50% 70%"),
    "oakakhi-hero": ("50% 40%", "45% 50%"),
    "experiences-hero": ("0% 65%", "46% 65%"),
    "about-hero": "50% 45%",
    "team-nishant": "50% 70%",
    "team-sachin": "35% 60%",
    "team-naveen": "50% 70%",
    "pandavkholi-1": "60% 60%",
    "bharatkot-1": "50% 55%",
}


def media(slot, scene, alt, cls="", eager=False, sizes="(min-width: 1240px) 560px, (min-width: 900px) 45vw, 92vw"):
    """An image slot. Shows the photo for `slot` if it exists, otherwise an illustration."""
    src = photo_sources(slot) if slot else None
    loading = "eager" if eager else "lazy"
    if src:
        srcset = ", ".join(f"{path} {w}w" for path, w in src["webp"])
        source = f'<source type="image/webp" srcset="{srcset}" sizes="{sizes}">' if srcset else ""
        focus = FOCUS.get(slot)
        if isinstance(focus, tuple):
            pos = f' style="--pos:{focus[0]};--pos-m:{focus[1]}"'
        else:
            pos = f' style="--pos:{focus}"' if focus else ""
        fetch = ' fetchpriority="high"' if eager else ""
        inner = f'<picture>{source}<img src="{src["fallback"]}" alt="{escape(alt)}" loading="{loading}"{fetch} decoding="async" width="1800" height="1200"{pos}></picture>'
    else:
        kind, seed = scene
        inner = art.scene(kind, seed, alt)
    return f'<div class="media {cls}">{inner}</div>'


def gallery(items, note=""):
    """A row of photos. items: (slot, alt, caption or "")."""
    figs = "".join(
        f'<figure class="g-item">{media(slot, ("mist", i), alt, sizes="(min-width: 1240px) 270px, (min-width: 900px) 22vw, 46vw")}'
        + (f"<figcaption>{escape(cap)}</figcaption>" if cap else "") + "</figure>"
        for i, (slot, alt, cap) in enumerate(items) if photo_sources(slot)
    )
    if not figs:
        return ""
    note_html = f'<p class="g-note">{escape(note)}</p>' if note else ""
    return f'<div class="gallery reveal">{figs}</div>{note_html}'


def head(meta):
    title = meta["title"]
    desc = meta["description"]
    canonical = url(meta["path"])
    image = url(meta.get("image", "assets/img/og-default.jpg"))
    og_type = meta.get("og_type", "website")
    ld = meta.get("jsonld") or []
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = '<meta name="robots" content="noindex">' if meta.get("noindex") else ""
    return f"""<!DOCTYPE html>
<html lang="en-IN" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta property="og:site_name" content="Turiya Trails">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{escape(meta.get('og_title', title))}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{image}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#17291f">
<link rel="icon" type="image/png" sizes="48x48" href="/assets/img/favicon-48.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/cormorant-garamond-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/outfit-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{FONT_FACES}</style>
<link rel="stylesheet" href="/assets/css/site.css">
<script>document.documentElement.classList.remove('no-js')</script>
{ld_html}
</head>"""


def header(current, tone="light"):
    here = ' aria-current="page"'
    links = "".join(
        f'<li><a href="/{href}"{here if href == current else ""}>{label}</a></li>'
        for label, href in NAV
    )
    mm = "".join(
        f'<li><a class="mm-link" href="/{href}">{label}<small>{"Here" if href == current else ""}</small></a></li>'
        for label, href in NAV
    )
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" data-tone="{tone}">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Turiya Trails, home">
      <img class="brand-dark" src="/assets/img/logo-mark-forest.png" alt="" width="55" height="30">
      <img class="brand-light" src="/assets/img/logo-mark-ivory.png" alt="" width="55" height="30">
      <span class="brand-name">Turiya Trails</span>
    </a>
    <nav aria-label="Main"><ul class="nav-links">{links}</ul></nav>
    <a class="btn btn--line nav-cta" href="/plan.html">Plan your journey</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu"><span class="label">Menu</span><span class="bars" aria-hidden="true"></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  <nav aria-label="Mobile"><ul>{mm}<li><a class="mm-link" href="/plan.html">Plan your journey<small></small></a></li></ul></nav>
  <div class="mm-foot">
    <a class="btn btn--light" href="{wa('Namaste Turiya Trails, I found you through the website and would like to know more.')}">{WA_ICON} Message us on WhatsApp</a>
    <p>Oakakhi, Ranikhet · Kumaun Himalaya</p>
  </div>
</div>"""


def footer():
    explore = [("Journeys", "journeys.html"), ("Day experiences", "experiences.html"), ("Treks", "treks.html"), ("Journal", "field-notes.html")]
    about = [("About Turiya", "about.html"), ("Our guides", "team.html"), ("Oakakhi, our base", "oakakhi.html"), ("Privacy", "privacy.html")]
    col = lambda items: "".join(f'<li><a href="/{h}">{l}</a></li>' for l, h in items)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="/assets/img/logo-mark-ivory.png" alt="Turiya Trails" width="84" height="46" loading="lazy">
        <p>Small-group journeys, forest walks, birdwatching and stargazing in the Kumaun Himalaya. Rooted in Ranikhet.</p>
      </div>
      <div class="footer-col"><h2>Explore</h2><ul>{col(explore)}</ul></div>
      <div class="footer-col"><h2>Turiya Trails</h2><ul>{col(about)}</ul></div>
      <div class="footer-col"><h2>Get in touch</h2><ul>
        <li><a href="{wa('Namaste Turiya Trails, I have a question.')}">WhatsApp {SITE['phone_display']}</a></li>
        <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        <li><a href="/plan.html">Enquiry form</a></li>
        <li><a href="/international.html">Travelling from abroad</a></li>
        <li><a href="{SITE['maps']}" rel="noopener">Oakakhi Stays, Ranikhet</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>© {SITE['year']} Turiya Trails. Rooted in Ranikhet.</span>
      <span>Walk slowly. Notice deeply.</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa('Namaste Turiya Trails, I found you through the website and would like to know more.')}" aria-label="Message Turiya Trails on WhatsApp">{WA_ICON}<span>Ask us</span></a>
<script src="/assets/js/site.js" defer></script>"""


def page(meta, body, current="", tone="light"):
    return f"""{head(meta)}
<body>
{header(current, tone)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""


def breadcrumbs(items):
    """items: list of (label, href or None). Returns (html, jsonld)."""
    lis = "".join(
        f'<li><a href="/{h}">{escape(l)}</a></li>' if h is not None else f'<li aria-current="page">{escape(l)}</li>'
        for l, h in items
    )
    ld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": l, **({"item": url(h)} if h is not None else {})}
            for i, (l, h) in enumerate(items)
        ],
    }
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>', ld


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "TravelAgency",
    "name": "Turiya Trails",
    "url": SITE["url"] + "/",
    "logo": SITE["url"] + "/assets/img/icon-512.png",
    "image": SITE["url"] + "/assets/img/og-default.jpg",
    "telephone": SITE["phone_display"].replace(" ", ""),
    "email": SITE["email"],
    "description": "Small-group journeys, treks, forest walks, birdwatching and stargazing in the Kumaun Himalaya, based at Oakakhi Stays in Ranikhet.",
    "address": {"@type": "PostalAddress", "addressLocality": "Ranikhet", "addressRegion": "Uttarakhand", "addressCountry": "IN"},
    "areaServed": "Kumaun, Uttarakhand, India",
}
