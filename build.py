"""Build the site into public/ (what Cloudflare serves).

While the site is unannounced, every public address shows a "Coming soon" page.
The full site is built at a hidden path, PREVIEW_DIR, for private previewing.
Set LAUNCHED = True to put the full site at the root instead.

Sources live in site/ (stylesheet, color script, images); run `python3 build.py`
after any change and commit public/.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "site"
PUBLIC = ROOT / "public"
LAUNCHED = False
PREVIEW_DIR = "preview-f5e3dd68"
INSTAGRAM = "https://www.instagram.com/majorfortenelson/"

NAV = [
    ("Hats", "hats.html"),
    ("Hoodies", "hoodies.html"),
    ("Markers", "markers.html"),
    ("Gallery", "gallery.html"),
    ("Instagram", INSTAGRAM),
    ("Misc", "misc.html"),
]

HOME_BODY = f"""<img class="hero" src="images/home.jpg" width="250" height="364" alt="">
<p class="bar new"><b>New:</b> <a href="hats.html">Hats</a> | <a href="hoodies.html">Hoodies</a></p>
<p class="bar cta"><b>Want to see more?</b> Follow along on <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a>.</p>"""

PAGES = {
    "hats.html": "Hats",
    "hoodies.html": "Hoodies",
    "markers.html": "Markers",
    "gallery.html": "Gallery",
    "misc.html": "Misc",
}

# Hand-drawn symbols (cut out of a photo of the drawing), one beside each line of the name.
# Shown via CSS masks so colors.js can tint each one.
GLYPHS = "".join(f'<span class="glyph g{i}"></span>' for i in (1, 2, 3))

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<title>{page_title}</title>
<link rel="stylesheet" href="style.css">
<script src="colors.js"></script>
</head>
<body>
<div class="page">
<div class="nav">
<div class="glyphs">{glyphs}</div>
{nav}
</div>
<div class="main">
<a class="masthead" href="index.html" aria-label="Major Forte Nelson">{masthead}</a>
{body}
<div class="footer">&copy; mmxxvi mfn</div>
</div>
</div>
</body>
</html>
"""


def masthead_html():
    # One line per word; each letter is its own item so CSS can spread it edge to edge.
    lines = []
    for word in ["MAJOR", "FORTE", "NELSON"]:
        letters = "".join(f"<i>{c}</i>" for c in word)
        lines.append(f"<span>{letters}</span>")
    return "".join(lines)


def nav_html():
    items = []
    for label, href in NAV:
        attrs = f'href="{href}"'
        if href.startswith("http"):
            attrs += ' target="_blank" rel="noopener"'
        items.append(f"<a {attrs}>{label}</a>")
    return "\n".join(items)


COMING_SOON = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Major Forte Nelson</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="page">
<div class="nav">
<div class="glyphs">{glyphs}</div>
</div>
<div class="main">
<div class="masthead" aria-label="Major Forte Nelson">{masthead}</div>
<p class="soon">Coming soon.</p>
</div>
</div>
</body>
</html>
"""


def copy_assets(dest):
    dest.mkdir(parents=True, exist_ok=True)
    for item in SRC.iterdir():
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def write_full_site(out, hidden):
    copy_assets(out)
    robots = '<meta name="robots" content="noindex, nofollow">\n' if hidden else ""

    def write(filename, page_title, body):
        (out / filename).write_text(TEMPLATE.format(
            page_title=page_title, robots=robots, nav=nav_html(), masthead=masthead_html(),
            glyphs=GLYPHS, body=body))

    write("index.html", "Major Forte Nelson", HOME_BODY)
    for filename, title in PAGES.items():
        body = f'<h1 class="title">{title}</h1>\n<div class="content"><p>Coming soon.</p></div>'
        write(filename, f"{title} - Major Forte Nelson", body)


if PUBLIC.exists():
    shutil.rmtree(PUBLIC)
PUBLIC.mkdir()

if LAUNCHED:
    write_full_site(PUBLIC, hidden=False)
    print("built full site at /")
else:
    # Only what the Coming soon page needs, so the photo isn't public yet.
    (PUBLIC / "images").mkdir()
    shutil.copy2(SRC / "style.css", PUBLIC)
    for i in (1, 2, 3):
        shutil.copy2(SRC / "images" / f"symbol{i}.png", PUBLIC / "images")
    (PUBLIC / "index.html").write_text(COMING_SOON.format(glyphs=GLYPHS, masthead=masthead_html()))
    write_full_site(PUBLIC / PREVIEW_DIR, hidden=True)
    print(f"built Coming soon page at /, full site at /{PREVIEW_DIR}/")
