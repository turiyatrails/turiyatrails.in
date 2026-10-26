"""Illustrated artwork used wherever a real photograph is not yet available.

Each scene is a small inline SVG built from layered ridgelines, in the same
spirit as the Turiya Trails mark (a sun circle above a mountain line). Scenes
are deterministic: the same name always draws the same picture.
"""
import math
import random
import zlib

W, H = 1600, 1000

PALETTES = {
    # sky top, sky bottom, ridge layers back -> front, accent (sun/moon)
    "dawn":    ("#22392b", "#8f8a63", ["#6d7553", "#55623f", "#3d4c31", "#2a3a26", "#1b2a1e"], "#e3c48a"),
    "mist":    ("#cfd0bf", "#ece6d6", ["#b9bda6", "#9fa68a", "#808a6b", "#5f6c4d", "#3f4c33"], "#f4ecd8"),
    "night":   ("#0b1510", "#1c2f27", ["#1b2b22", "#15231b", "#101b15", "#0c140f", "#080e0a"], "#efe6cf"),
    "dusk":    ("#2f3b37", "#b08a5a", ["#6b5b45", "#54493a", "#3f3a2f", "#2b2a22", "#1b1c17"], "#f0cf92"),
    "forest":  ("#1d3125", "#43573c", ["#2f4330", "#263a29", "#1d2f21", "#16251a", "#0f1a12"], "#d7c89c"),
    "snow":    ("#5d7184", "#c9cfcf", ["#eef0ec", "#c7cdc8", "#8c9890", "#5d6b5e", "#34412f"], "#f6f1e3"),
    "lake":    ("#30443a", "#9aa48a", ["#73805f", "#5a6a4a", "#43543a", "#30402b", "#1f2c1d"], "#efe0b8"),
}


def _ridge(rng, base_y, amp, roughness, peaks=None):
    """Return an SVG path for a ridgeline filled to the bottom of the canvas."""
    n = 18
    xs = [-120 + i * (W + 240) / (n - 1) for i in range(n)]
    ys = []
    phase = rng.random() * math.pi * 2
    for i, x in enumerate(xs):
        y = base_y
        y -= amp * math.sin(i / (n - 1) * math.pi * (1.2 + rng.random() * .6) + phase) * .6
        y -= amp * (rng.random() - .5) * roughness
        if peaks:
            for px, ph, pw in peaks:
                d = (x - px * W) / (pw * W)
                y -= ph * math.exp(-d * d)
        ys.append(y)
    pts = list(zip(xs, ys))
    d = f"M0,{H} L{pts[0][0]:.0f},{pts[0][1]:.0f} "
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        d += f"Q{x0:.0f},{y0:.0f} {mx:.0f},{my:.0f} "
    d += f"L{W + 120},{pts[-1][1]:.0f} L{W + 120},{H} Z"
    return d


def _mountains(rng, base_y, peaks):
    """Sharp, snow-capped peaks: straight facets between summits and cols."""
    pts = [(-120, base_y)]
    for px, ph, pw in sorted(peaks):
        cx = px * W
        left, right = cx - pw * W, cx + pw * W
        pts.append((left, base_y - ph * .25 - rng.random() * 20))
        pts.append((cx - pw * W * .55, base_y - ph * .62))
        pts.append((cx, base_y - ph))
        pts.append((cx + pw * W * .45, base_y - ph * .7))
        pts.append((right, base_y - ph * .3 - rng.random() * 20))
    pts.append((W + 120, base_y))
    pts.sort()
    d = f"M-120,{H} " + " ".join(f"L{x:.0f},{y:.0f}" for x, y in pts) + f" L{W + 120},{H} Z"
    return d, pts


def _stars(rng, count, max_y):
    out = []
    for _ in range(count):
        x, y = rng.random() * W, rng.random() ** 1.4 * max_y
        r = .6 + rng.random() ** 3 * 1.8
        o = .35 + rng.random() * .65
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#f5f1e8" opacity="{o:.2f}"/>')
    return "".join(out)


def _trees(rng, rows):
    """Rows of tapered trunks, far rows paler, with mist between them."""
    out = []
    for color, count, width, opacity in rows:
        for _ in range(count):
            x = rng.random() * W
            w = width * (.6 + rng.random() * .8)
            top = -20
            bottom = H
            out.append(f'<path d="M{x - w / 2:.0f},{bottom} L{x - w * .28:.0f},{top} L{x + w * .28:.0f},{top} L{x + w / 2:.0f},{bottom} Z" fill="{color}" opacity="{opacity}"/>')
        out.append(f'<rect width="{W}" height="{H}" fill="#c9cfb8" opacity=".07"/>')
    return "".join(out)


def scene(name, seed=None, label=""):
    """Render a named scene. `seed` varies the shapes; `label` becomes the accessible title."""
    kind = name if name in PALETTES else "dawn"
    rng = random.Random(f"{name}-{seed}")
    top, bottom, layers, accent = PALETTES[kind]
    gid = "g" + format(zlib.crc32(f"{name}-{seed}".encode()), "x")
    title = f"<title>{label}</title>" if label else ""
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    parts = [
        f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" {aria} focusable="false">{title}',
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="url(#{gid})"/>',
    ]

    if kind == "night":
        parts.append(f'<g class="art-twinkle">{_stars(rng, 260, 720)}</g>')
        # a faint band of the Milky Way
        parts.append('<ellipse cx="900" cy="280" rx="900" ry="120" fill="#f5f1e8" opacity=".05" transform="rotate(-24 900 280)"/>')
        parts.append(f'<circle cx="{1180 + rng.random() * 160:.0f}" cy="210" r="34" fill="none" stroke="{accent}" stroke-width="2" opacity=".55"/>')
    elif kind in ("dawn", "dusk", "lake", "mist"):
        cx = 960 + rng.random() * 300
        cy = 300 + rng.random() * 80
        parts.append(f'<defs><radialGradient id="{gid}r"><stop offset="0" stop-color="{accent}" stop-opacity=".35"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>')
        parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="420" fill="url(#{gid}r)"/>')
        parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="96" fill="none" stroke="{accent}" stroke-width="3" opacity=".7"/>')
        parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="30" fill="{accent}" opacity=".75"/>')
    elif kind == "snow":
        parts.append(f'<circle cx="{1240:.0f}" cy="200" r="48" fill="{accent}" opacity=".45"/>')

    bases = [470, 560, 650, 740, 840]
    amps = [90, 80, 70, 60, 50]
    start = 0
    if kind == "snow":
        # A range of sharp peaks, lit from the left, with forested ridges in front.
        shift = rng.random() * .1 - .05
        peaks = [(.18 + shift, 230, .09), (.38 + shift, 330, .08), (.55 + shift, 290, .07), (.76 + shift, 250, .09)]
        d, pts = _mountains(rng, 640, peaks)
        parts.append(f'<path d="{d}" fill="{layers[0]}"/>')
        for px, ph, pw in peaks:
            cx = px * W
            parts.append(f'<path d="M{cx:.0f},{640 - ph:.0f} L{cx + pw * W * .45:.0f},{640 - ph * .7:.0f} L{cx + pw * W:.0f},{640 - ph * .3:.0f} L{cx + pw * W * .15:.0f},640 Z" fill="{layers[1]}" opacity=".55"/>')
        bases, amps, start = [0, 660, 740, 810, 880], [0, 50, 45, 40, 35], 1
    for i, color in enumerate(layers):
        if i < start:
            continue
        cls = ' class="art-drift"' if i == 1 and kind in ("mist", "dawn") else ""
        parts.append(f'<path{cls} d="{_ridge(rng, bases[i], amps[i], 1.3)}" fill="{color}"/>')
        if kind == "mist" and i in (1, 2):
            parts.append(f'<rect class="art-drift" x="-100" y="{bases[i] - 40}" width="{W + 200}" height="90" fill="#f5f1e8" opacity=".22"/>')

    if kind == "forest":
        parts.append(_trees(rng, [("#3b5240", 34, 16, .5), ("#26392a", 18, 30, .8), ("#0e1810", 8, 52, 1)]))
    if kind == "lake":
        parts.append(f'<rect y="800" width="{W}" height="200" fill="#c5c8b2" opacity=".55"/>')
        for k in range(7):
            y = 830 + k * 22
            parts.append(f'<line x1="{120 + rng.random() * 600:.0f}" y1="{y}" x2="{700 + rng.random() * 700:.0f}" y2="{y}" stroke="#f5f1e8" stroke-width="2" opacity=".35"/>')

    parts.append("</svg>")
    return "".join(parts)
