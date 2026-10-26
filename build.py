#!/usr/bin/env python3
"""Build the Turiya Trails website.

    python3 build.py

Writes every HTML page, sitemap.xml and robots.txt into this folder, ready to
publish as-is. Needs only Python 3.9+. If Pillow is installed, photos added to
assets/img/photos/ are also resized and converted to WebP for fast loading.
"""
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from src.data import SITE  # noqa: E402
from src.pages import all_pages  # noqa: E402
from src.templates import PHOTO_DIR  # noqa: E402


def optimise_photos():
    """Make 900px and 1800px WebP copies of each photo in assets/img/photos/."""
    if not os.path.isdir(PHOTO_DIR):
        return
    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("  Pillow not installed: photos will be used at their original size.")
        return
    out_dir = os.path.join(PHOTO_DIR, "out")
    os.makedirs(out_dir, exist_ok=True)
    for name in sorted(os.listdir(PHOTO_DIR)):
        stem, ext = os.path.splitext(name)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        src = os.path.join(PHOTO_DIR, name)
        for width in (900, 1800):
            dest = os.path.join(out_dir, f"{stem}-{width}.webp")
            if os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(src):
                continue
            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im).convert("RGB")
                if im.width > width:
                    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
                im.save(dest, "WEBP", quality=80, method=6)
            print(f"  photo  {os.path.relpath(dest, ROOT)}")


def main():
    optimise_photos()
    pages = all_pages()
    for path, html in pages:
        dest = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  page   {path}")

    today = date.today().isoformat()
    skip = {"404.html", "conscious-treks.html"}
    urls = []
    for path, _ in pages:
        if path in skip:
            continue
        loc = SITE["url"] + "/" + ("" if path == "index.html" else path)
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod></url>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /src/\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    print(f"Built {len(pages)} pages, sitemap.xml and robots.txt.")


if __name__ == "__main__":
    main()
