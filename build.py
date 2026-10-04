"""Generate the site's pages from one shared template so the nav stays in sync."""
from pathlib import Path

OUT = Path(__file__).parent / "public"
INSTAGRAM = "https://www.instagram.com/"  # TODO: replace with your profile URL

NAV = [
    ("Hats", "hats.html"),
    ("Hoodies", "hoodies.html"),
    ("Markers", "markers.html"),
    ("Gallery", "gallery.html"),
    ("Instagram", INSTAGRAM),
    ("Misc", "misc.html"),
]

PAGES = {
    "index.html": ("Major Forte Nelson",
                   '<img src="images/home.jpg" width="410" height="598" alt="">'),
    "hats.html": ("Hats", "<p>Coming soon.</p>"),
    "hoodies.html": ("Hoodies", "<p>Coming soon.</p>"),
    "markers.html": ("Markers", "<p>Coming soon.</p>"),
    "gallery.html": ("Gallery", "<p>Coming soon.</p>"),
    "misc.html": ("Misc", "<p>Coming soon.</p>"),
}

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="page">
<div class="nav">
<a class="mark" href="index.html" aria-label="Home"></a>
<ul>
{nav}
</ul>
</div>
<div class="main">
<h1 class="title">{title}</h1>
{body}
</div>
</div>
</body>
</html>
"""


def nav_html(current):
    items = []
    for label, href in NAV:
        external = href.startswith("http")
        attrs = f'href="{href}"'
        if external:
            attrs += ' target="_blank" rel="noopener"'
        if href == current:
            attrs += ' class="current"'
        items.append(f"<li><a {attrs}>{label}</a></li>")
    return "\n".join(items)


for filename, (title, body) in PAGES.items():
    page_title = title if filename == "index.html" else f"{title} - Major Forte Nelson"
    html = TEMPLATE.format(page_title=page_title, nav=nav_html(filename), title=title, body=body)
    (OUT / filename).write_text(html)
    print("wrote", filename)
