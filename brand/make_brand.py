"""ProudAuth brand kit: README banners, social previews, profile cards and the org avatar.

Usage: make_brand.py OUT_DIR   (needs rsvg-convert)
"""
import subprocess
import sys
from pathlib import Path

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"

REPOS = {
    "proudauth": ("Your identity server.", ["OAuth 2.0 &amp; OIDC", "Passkeys &amp; MFA", "Organizations", "One Docker image"]),
    "proudauth-website": ("Website &amp; documentation", ["proudauth.com", "Always the latest release", "Docker quickstart"]),
    "proudauth-sdk-go": ("SDK for Go", ["Verify tokens", "OIDC sign-in", "Admin API"]),
    "proudauth-sdk-node": ("SDK for Node.js", ["TypeScript", "Verify tokens", "OIDC sign-in", "Admin API"]),
    "proudauth-sdk-dart": ("SDK for Dart", ["Verify tokens", "OIDC sign-in", "Admin API"]),
    "proudauth-sdk-php": ("SDK for PHP", ["Verify tokens", "OIDC sign-in", "Admin API"]),
    "proudauth-sdk-dotnet": ("SDK for .NET", ["ASP.NET Core", "Verify tokens", "OIDC sign-in", "Admin API"]),
}

DEFS = """<defs>
  <radialGradient id="g1" cx="78%" cy="50%" r="60%"><stop offset="0" stop-color="#1a5a43"/><stop offset=".55" stop-color="#0a2219"/><stop offset="1" stop-color="#06120e"/></radialGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#3ee6b0" stop-opacity=".55"/><stop offset="1" stop-color="#3ee6b0" stop-opacity="0"/></radialGradient>
  <linearGradient id="mint" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#c8ffec"/><stop offset=".55" stop-color="#3ee6b0"/><stop offset="1" stop-color="#0f9a73"/></linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".55" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".045"/></pattern>
</defs>"""


def mark(x, y, size, fill="url(#mint)", ink="#06120e"):
    s = size / 32
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M6 5h13l7 7v15H6z" fill="{fill}"/>'
            f'<path d="M12 11h6a5 5 0 0 1 0 10h-3v5h-3zm3 3v4h3a2 2 0 0 0 0-4z" fill="{ink}"/></g>')


def art(cx, cy, r):
    """The identity server at the centre, your apps on its orbit."""
    nodes = []
    for i, (dx, dy) in enumerate([(-1.55, -0.95), (1.55, -0.95), (-1.75, 0.55), (1.75, 0.55)]):
        nx, ny = cx + dx * r, cy + dy * r
        nodes.append(f'<path d="M{cx} {cy}L{nx:.0f} {ny:.0f}" stroke="#3ee6b0" stroke-opacity=".55" stroke-width="1.5" stroke-dasharray="5 7"/>')
        nodes.append(f'<rect x="{nx - 30:.0f}" y="{ny - 21:.0f}" width="60" height="42" rx="11" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".16"/>')
        icon = [
            f'<rect x="{nx - 13:.0f}" y="{ny - 9:.0f}" width="26" height="18" rx="3" fill="none" stroke="#c8ffec" stroke-width="1.6"/><path d="M{nx - 13:.0f} {ny - 4:.0f}h26" stroke="#c8ffec" stroke-width="1.6"/>',
            f'<rect x="{nx - 7:.0f}" y="{ny - 12:.0f}" width="14" height="24" rx="3.5" fill="none" stroke="#c8ffec" stroke-width="1.6"/><circle cx="{nx:.0f}" cy="{ny + 7:.0f}" r="1.5" fill="#c8ffec"/>',
            f'<path d="M{nx - 6:.0f} {ny - 8:.0f}l-7 8 7 8M{nx + 6:.0f} {ny - 8:.0f}l7 8-7 8" fill="none" stroke="#c8ffec" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<circle cx="{nx:.0f}" cy="{ny:.0f}" r="6" fill="none" stroke="#c8ffec" stroke-width="1.8"/><path d="M{nx:.0f} {ny - 12:.0f}v4m0 16v4m-12-12h4m16 0h4" stroke="#c8ffec" stroke-width="1.8" stroke-linecap="round"/>',
        ][i]
        nodes.append(icon)
    core = r * 0.52
    return f"""<circle cx="{cx}" cy="{cy}" r="{r * 1.9:.0f}" fill="url(#glow)"/>
  <circle cx="{cx}" cy="{cy}" r="{r * 1.25:.0f}" fill="none" stroke="#3ee6b0" stroke-opacity=".18" stroke-dasharray="2 9"/>
  <circle cx="{cx}" cy="{cy}" r="{r * 0.85:.0f}" fill="none" stroke="#3ee6b0" stroke-opacity=".3"/>
  {''.join(nodes)}
  <circle cx="{cx}" cy="{cy}" r="{core + 14:.0f}" fill="#0a1f18" stroke="#3ee6b0" stroke-opacity=".7"/>
  <circle cx="{cx}" cy="{cy}" r="{core:.0f}" fill="url(#mint)"/>
  {mark(cx - core * 0.62, cy - core * 0.66, core * 1.25, fill="#06120e", ink="url(#mint)")}
  <g transform="translate({cx + core * 0.78:.0f} {cy + core * 0.72:.0f})"><circle r="15" fill="#06120e" stroke="#3ee6b0" stroke-width="1.5"/><rect x="-6" y="-2" width="12" height="9" rx="2" fill="#3ee6b0"/><path d="M-4 -2v-3a4 4 0 0 1 8 0v3" fill="none" stroke="#3ee6b0" stroke-width="1.8"/></g>"""


def chips(x, y, labels, size=15, max_x=10**6):
    parts, cx = [], x
    for label in labels:
        plain = label.replace("&amp;", "&")
        w = int(len(plain) * size * 0.56) + 30
        if cx > x and cx + w > max_x:  # wrap before reaching the artwork
            cx, y = x, y + size + 29
        parts.append(f'<rect x="{cx}" y="{y}" width="{w}" height="{size + 17}" rx="{(size + 17) / 2}" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".14"/>'
                     f'<text x="{cx + 15}" y="{y + size + 4}" font-family="{FONT}" font-size="{size}" fill="#c8ffec">{label}</text>')
        cx += w + 10
    return "".join(parts)


def card(width, height, subtitle, labels):
    tall = height > 500
    pad = 72 if tall else 64
    title_y = height * (0.40 if tall else 0.43)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{DEFS}
<clipPath id="round"><rect width="{width}" height="{height}" rx="28"/></clipPath>
<g clip-path="url(#round)">
  <rect width="{width}" height="{height}" fill="url(#g1)"/>
  <rect width="{width}" height="{height}" fill="url(#grid)"/>
  <rect y="{height - 2}" width="{width}" height="2" fill="url(#fade)"/>
  {art(width * (0.74 if tall else 0.785), height * 0.5, height * (0.2 if tall else 0.26))}
  {mark(pad, title_y - (118 if tall else 104), 54 if tall else 46)}
  <text x="{pad + (66 if tall else 58)}" y="{title_y - (78 if tall else 70)}" font-family="{FONT}" font-weight="700" font-size="{30 if tall else 26}" fill="#ecfff7" letter-spacing="-0.5">ProudAuth</text>
  <text x="{pad}" y="{title_y + 6}" font-family="{FONT}" font-weight="700" font-size="{64 if tall else 54}" fill="#ecfff7" letter-spacing="-2">{subtitle}</text>
  <text x="{pad}" y="{title_y + (70 if tall else 58)}" font-family="{FONT}" font-weight="700" font-size="{40 if tall else 32}" fill="url(#mint)" letter-spacing="-1">Free. Private. Yours.</text>
  {chips(pad, title_y + (112 if tall else 92), labels, 16 if tall else 14, width * (0.52 if tall else 0.61))}
</g>
</svg>"""


def render(svg, name):
    path = out / f"{name}.svg"
    path.write_text(svg)
    subprocess.run(["rsvg-convert", "-z", "2", str(path), "-o", str(out / f"{name}.png")], check=True)


for slug, (subtitle, labels) in REPOS.items():
    render(card(1280, 400, subtitle, labels), f"banner-{slug}")
    render(card(1280, 640, subtitle, labels), f"social-{slug}")

avatar = f"""<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
{DEFS}
<rect width="512" height="512" fill="#06120e"/>
<circle cx="256" cy="256" r="300" fill="url(#glow)"/>
<rect width="512" height="512" fill="url(#grid)"/>
{mark(66, 62, 380)}
</svg>"""
(out / "avatar.svg").write_text(avatar)
subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024", str(out / "avatar.svg"), "-o", str(out / "avatar.png")], check=True)
# Profile cards: the repository grid on github.com/ProudAuth, two per row.
MONO = "SF Mono, Menlo, monospace"
CARDS = {
    # slug: (eyebrow, title, line, tile, path)
    "proudauth": ("IDENTITY SERVER", "proudauth", "Sign-in, organizations and access control in one Docker image.", "mark", "ProudAuth/proudauth"),
    "proudauth-website": ("WEBSITE", "proudauth.com", "The site and documentation, rebuilt from every release.", "web", "ProudAuth/proudauth-website"),
    "proudauth-sdk-go": ("SDK", "Go", "Verify tokens, sign users in, automate administration.", "Go", "ProudAuth/proudauth-sdk-go"),
    "proudauth-sdk-node": ("SDK", "Node.js", "TypeScript-first. Express, Fastify and node:http adapters.", "TS", "ProudAuth/proudauth-sdk-node"),
    "proudauth-sdk-dart": ("SDK", "Dart", "Verify tokens, sign users in, automate administration.", "Dart", "ProudAuth/proudauth-sdk-dart"),
    "proudauth-sdk-php": ("SDK", "PHP", "Verify tokens, sign users in, automate administration.", "PHP", "ProudAuth/proudauth-sdk-php"),
    "proudauth-sdk-dotnet": ("SDK", ".NET", "ASP.NET Core middleware, token verification and admin client.", "C#", "ProudAuth/proudauth-sdk-dotnet"),
    "start": ("START NOW", "Quickstart", "Copy two files from the docs, fill in .env and start.", "term", "$ docker compose up -d"),
}


def wrap(text, limit):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > limit:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line]


def tile(kind, cx, cy, size):
    half = size / 2
    body = (f'<circle cx="{cx}" cy="{cy}" r="{size * 0.95:.0f}" fill="url(#glow)"/>'
            f'<rect x="{cx - half - 14}" y="{cy - half - 14}" width="{size + 28}" height="{size + 28}" rx="{size * 0.3:.0f}" fill="none" stroke="#3ee6b0" stroke-opacity=".28"/>'
            f'<rect x="{cx - half}" y="{cy - half}" width="{size}" height="{size}" rx="{size * 0.24:.0f}" fill="url(#mint)"/>')
    if kind == "mark":
        return body + mark(cx - size * 0.42, cy - size * 0.47, size * 0.84, fill="#06120e", ink="url(#mint)")
    if kind == "web":
        w, h = size * 0.56, size * 0.42
        return body + (f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="8" fill="none" stroke="#06120e" stroke-width="7"/>'
                       f'<path d="M{cx - w / 2:.0f} {cy - h / 2 + 18:.0f}h{w:.0f}" stroke="#06120e" stroke-width="7"/>')
    label = ">_" if kind == "term" else kind
    font = MONO if kind == "term" else FONT
    scale = {1: 0.5, 2: 0.42, 3: 0.33}.get(len(label), 0.27)
    return body + (f'<text x="{cx}" y="{cy + size * scale * 0.36:.0f}" text-anchor="middle" font-family="{font}" font-weight="800" '
                   f'font-size="{size * scale:.0f}" fill="#06120e" letter-spacing="-1">{label}</text>')


def profile_card(eyebrow, title, line, kind, path):
    w, h = 800, 400
    text = "".join(f'<text x="48" y="{226 + i * 31}" font-family="{FONT}" font-size="22" fill="#c8ffec" fill-opacity=".82">{part}</text>'
                   for i, part in enumerate(wrap(line, 38)[:2]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{DEFS}
<clipPath id="round"><rect width="{w}" height="{h}" rx="26"/></clipPath>
<g clip-path="url(#round)">
  <rect width="{w}" height="{h}" fill="url(#g1)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  {tile(kind, 640, 170, 150)}
  {mark(44, 40, 30)}
  <text x="84" y="62" font-family="{FONT}" font-weight="700" font-size="16" fill="#3ee6b0" letter-spacing="3.5">{eyebrow}</text>
  <text x="46" y="170" font-family="{FONT}" font-weight="700" font-size="{62 if len(title) < 11 else 52}" fill="#ecfff7" letter-spacing="-2">{title}</text>
  {text}
  <path d="M48 318H752" stroke="#ffffff" stroke-opacity=".1"/>
  <text x="48" y="358" font-family="{MONO}" font-size="18" fill="#8fdcc0" fill-opacity=".8">{path}</text>
  <g transform="translate(730 352)"><circle r="22" fill="#ffffff" fill-opacity=".05" stroke="#3ee6b0" stroke-opacity=".6"/><path d="M-8 0h15m-6-6 6 6-6 6" fill="none" stroke="#3ee6b0" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g>
</g>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="25.5" fill="none" stroke="#3ee6b0" stroke-opacity=".22" stroke-width="1.5"/>
</svg>"""


for slug, spec in CARDS.items():
    path = out / f"card-{slug}.svg"
    path.write_text(profile_card(*spec))
    subprocess.run(["rsvg-convert", str(path), "-o", str(out / f"card-{slug}.png")], check=True)

# The "Start now" button on the profile page, on a transparent background.
start = f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="168" viewBox="0 0 640 168">
{DEFS}
<defs><filter id="soft" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="14"/></filter></defs>
<rect x="44" y="40" width="552" height="96" rx="48" fill="#3ee6b0" fill-opacity=".45" filter="url(#soft)"/>
<rect x="36" y="28" width="568" height="104" rx="52" fill="url(#mint)"/>
<rect x="37" y="29" width="566" height="102" rx="51" fill="none" stroke="#ffffff" stroke-opacity=".45" stroke-width="2"/>
{mark(84, 54, 52, fill="#06120e", ink="url(#mint)")}
<text x="152" y="98" font-family="{FONT}" font-weight="700" font-size="46" fill="#06120e" letter-spacing="-1">Start now</text>
<g transform="translate(548 80)"><circle r="30" fill="#06120e"/><path d="M-11 0h21m-8-8 8 8-8 8" fill="none" stroke="#3ee6b0" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g>
</svg>"""
(out / "button-start-now.svg").write_text(start)
subprocess.run(["rsvg-convert", str(out / "button-start-now.svg"), "-o", str(out / "button-start-now.png")], check=True)

print("brand kit written to", out)
