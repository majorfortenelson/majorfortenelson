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

HOME_BODY = f"""<img class="hero" src="images/home.jpg" width="300" height="437" alt="">
<p class="bar new"><b>New:</b> <a href="hats.html">Hats</a> | <a href="hoodies.html">Hoodies</a></p>
<p class="bar cta"><b>Want to see more?</b> Follow along on <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a>.</p>"""

PAGES = {
    "hats.html": "Hats",
    "hoodies.html": "Hoodies",
    "markers.html": "Markers",
    "gallery.html": "Gallery",
    "misc.html": "Misc",
}

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{page_title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="page">
<div class="nav">
{nav}
</div>
<div class="main">
<a class="masthead" href="index.html">MAJOR FORTE NELSON</a>
{body}
<div class="footer">&copy; mmxxvi mfn</div>
</div>
</div>
</body>
</html>
"""


def nav_html():
    items = []
    for label, href in NAV:
        attrs = f'href="{href}"'
        if href.startswith("http"):
            attrs += ' target="_blank" rel="noopener"'
        items.append(f"<a {attrs}>{label}</a>")
    return "\n".join(items)


def write(filename, page_title, body):
    (OUT / filename).write_text(TEMPLATE.format(page_title=page_title, nav=nav_html(), body=body))
    print("wrote", filename)


write("index.html", "Major Forte Nelson", HOME_BODY)
for filename, title in PAGES.items():
    body = f'<h1 class="title">{title}</h1>\n<div class="content"><p>Coming soon.</p></div>'
    write(filename, f"{title} - Major Forte Nelson", body)
