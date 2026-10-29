"""Condition page template for the Evergrowth preview.

Rows 4 to 7 should call render_condition() instead of copying a page.
Book Appointment always comes from shell.book_btn: internal, same tab.
Pass archive copy with the allowed swaps already applied. Do not invent
reviews. The four reviews below are the real Home and Back Pain reviews.

The approved Back Pain mockup has no FAQ block, and the archive page has
no FAQ copy, so this template does not add one.
"""
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

# Same four reviews as Home. Word for word, names as given. No stars.
REVIEWS = [
    (
        [
            "Dr Will is a GREAT chiropractor. I used to have lower back pain that was frequent; now I no longer have that pain. With regular adjustments my back stays aligned and free from tension and stiffness. I highly recommend Evergrowth Chiropractic services for individuals and families!",
        ],
        "DNoria R.",
    ),
    (
        [
            "I enjoy my visits to Evergrowth Chiropractic so much! Dr. Will is amazing! I feel so refreshed after my treatments. Wendy is so sweet and friendly as well! I highly recommend their practice; I'm so glad I found them! Relaxing, no stress atmosphere.",
        ],
        "Emily E.",
    ),
    (
        [
            "It was my first time being adjusted and WOW. The Experience from start to finish was Awesome!",
            "Professional Friendly and Personable staff and Dr Will was kind and was super informative about my visit and what needed to be done. So happy I am now a Patient!!",
        ],
        "Laurie W.",
    ),
    (
        [
            "Very professional and knowledgeable. We brought my 9 year old due to issues with her ears and they explained everything thoroughly and made her comfortable. I highly recommend Evergrowth Chiropractic.",
        ],
        "Andrea V.",
    ),
]

# Sidebar hours, same facts as shell.HOURS, grouped the way the mockup groups them.
SIDE_HOURS = [
    ("Mon, Wed, Thu", "10am to 1pm, 3pm to 6pm"),
    ("Tuesday", "3pm to 6pm"),
    ("Friday", "Appointments only"),
    ("Sat, Sun", "Closed"),
]


def esc(text):
    return html.escape(text, quote=False)


def nav_group(name):
    for _label, slug, sub in shell.NAV:
        if slug != "MEGA" or not sub:
            continue
        for group, items in sub:
            if group == name:
                return items
    raise KeyError(name)


def crumbs_html(items, depth):
    parts = []
    for label, slug in items:
        parts.append(shell.link(slug, label, depth) if slug else esc(label))
    return '<div class="crumbs">' + "<span>/</span>".join(parts) + "</div>"


def reviews_html():
    cards = []
    for paras, name in REVIEWS:
        body = "".join(f"<p>{esc(p)}</p>" for p in paras)
        cards.append(f'<figure class="t-card" style="margin:0">{body}<cite>{esc(name)}</cite></figure>')
    inner = "".join(cards)
    return (
        '<section class="tint"><div class="container"><div class="center">'
        '<span class="eyebrow">Our testimonial</span>'
        "<h2>What patients say about Evergrowth Chiropractic</h2></div>"
        f'<div class="t-grid">{inner}</div></div></section>'
    )


def render_condition(
    *,
    depth,
    title,
    description,
    crumbs,
    h1,
    sub,
    image,
    image_alt,
    image_w,
    image_h,
    blocks,
    closing,
    group_title,
    group_links,
    include_reviews=True,
):
    """blocks is a list of ('h2', text), ('p', text), or ('ul', [items]).
    crumbs is (label, slug or None)."""
    parts = []
    for kind, text in blocks:
        if kind == "h2":
            parts.append(f"<h2>{esc(text)}</h2>")
        elif kind == "ul":
            items = "".join(f"<li>{esc(item)}</li>" for item in text)
            parts.append(f"<ul>{items}</ul>")
        else:
            parts.append(f"<p>{esc(text)}</p>")
    article = "".join(parts)
    links = "".join(
        f'<a href="{shell.href(slug, depth)}">{label}</a>'
        for label, slug in group_links
    )
    hours = "".join(f"<li><span>{day}</span><span>{when}</span></li>" for day, when in SIDE_HOURS)
    phone = f'<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a>'
    reviews = reviews_html() if include_reviews else ""
    body = f'''<section class="page-hero"><div class="container">{crumbs_html(crumbs, depth)}<h1>{esc(h1)}</h1><p class="sub-h">{esc(sub)}</p></div></section>
<section style="padding-top:40px"><div class="container article-grid"><article class="article"><div class="a-img"><img src="{image}" alt="{esc(image_alt)}" width="{image_w}" height="{image_h}"></div>{article}
<div class="inline-cta"><p>{esc(closing)}</p><div class="book-actions">{shell.book_btn(depth, "Book Appointment")}{phone}</div></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(depth, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center">{phone}</p></div>
<div class="side-card"><h3>Hours</h3><ul>{hours}</ul></div>
<div class="side-card side-links"><h3>{esc(group_title)}</h3>{links}</div></aside></div></section>
{reviews}'''
    return shell.render_page(title, description, body, depth)
