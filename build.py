"""Generate the site's pages from one shared template so the button column stays in sync."""
from pathlib import Path

OUT = Path(__file__).parent / "public"
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
<title>{page_title}</title>
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


def write(filename, page_title, body):
    (OUT / filename).write_text(TEMPLATE.format(page_title=page_title, nav=nav_html(), masthead=masthead_html(),
                                                            glyphs=GLYPHS, body=body))
    print("wrote", filename)


write("index.html", "Major Forte Nelson", HOME_BODY)
for filename, title in PAGES.items():
    body = f'<h1 class="title">{title}</h1>\n<div class="content"><p>Coming soon.</p></div>'
    write(filename, f"{title} - Major Forte Nelson", body)
