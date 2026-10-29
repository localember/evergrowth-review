"""Office Tour page. Copy is the 2026-05-11 archive text.

The archive page is the heading "Welcome to The Office" and the four
reviews. It has no other sentences. The photo slider on the old site is
not carried over.

The gallery is the four Las Vegas office photos from 2026-10-29. The
waiting-room panorama is full width. Under it, two hallway views and the
suite 240B door sign sit in a grid. No captions and no new sentences.

Old tour files stay off this page. The 2025 reception panorama and the
adjusting room photo may show the Henderson office. The front desk photo
stays unused until the client confirms who is in it. No stock photo
stands in for the office.

Wording changes, and only these:
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- The old footer address and hours are not copied. The shared shell
  supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the
  new hours.
The New Patient Special block on the old page is left off.
Reviews stay word for word, including Dr Will and Dr. Will.
"""
import hashlib
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SLUG = "office-tour"
SRC = Path("/tmp/evergrowth-src/old/pages/office-tour_20260511.txt")

WHO = [
    ("Meet the Doctor", "meet-the-doctor"),
    ("Testimonials", "testimonials"),
    ("Office Tour", "office-tour"),
    ("Blog", "blog"),
]

REVIEWS = [
    (
        "Dr Will is a GREAT chiropractor. I used to have lower back pain that was frequent; now I no longer have that pain. With regular adjustments my back stays aligned and free from tension and stiffness. I highly recommend Evergrowth Chiropractic services for individuals and families!",
        "DNoria R.",
    ),
    (
        "I enjoy my visits to Evergrowth Chiropractic so much! Dr. Will is amazing! I feel so refreshed after my treatments. Wendy is so sweet and friendly as well! I highly recommend their practice; I'm so glad I found them! Relaxing, no stress atmosphere.",
        "Emily E.",
    ),
    (
        "It was my first time being adjusted and WOW. The Experience from start to finish was Awesome!\nProfessional Friendly and Personable staff and Dr Will was kind and was super informative about my visit and what needed to be done. So happy I am now a Patient!!",
        "Laurie W.",
    ),
    (
        "Very professional and knowledgeable. We brought my 9 year old due to issues with her ears and they explained everything thoroughly and made her comfortable. I highly recommend Evergrowth Chiropractic.",
        "Andrea V.",
    ),
]

NOTE = (
    "BUILT. The old page heading is Welcome to The Office. "
    "The four reviews on that page are shown word for word. Title suffix "
    "Chiropractor Henderson NV | New Patient Experience became Chiropractor Las Vegas NV | Evergrowth Chiropractic. "
    "Old footer address and hours are not copied. The New Patient Special block is left off. "
    "Reviews keep Dr Will and Dr. Will as written. "
    "Gallery is the four 2026-10-29 Las Vegas office photos: waiting room panorama, two hallway views, and the suite 240B door sign. No captions. "
    "The 2025 reception panorama and the adjusting room photo stay off: they may show the old Henderson office. "
    "The front desk photo stays unused until the client confirms who is in it. "
    "Old tour photos are not used."
)


def esc(text):
    return html.escape(text, quote=False)


def check_copy():
    raw = SRC.read_text()
    if "Office Tour - Chiropractor Henderson NV | New Patient Experience" not in raw:
        raise SystemExit("copy drift against archive text: title")
    if "Welcome to The Office" not in raw:
        raise SystemExit("copy drift against archive text: heading")
    for text, name in REVIEWS:
        if text not in raw or name not in raw:
            raise SystemExit("review missing from archive: " + name)
    if "New Patient Special" not in raw:
        raise SystemExit("archive shape changed")
    if "1263 E Silverado Ranch Blvd #105A" not in raw or "Henderson, NV 89183" not in raw:
        raise SystemExit("old address missing from archive; swap log would be wrong")


def gallery_html():
    img = "../assets/img/"
    pano = (
        '<figure class="tour-pano"><img '
        f'src="{img}office-waiting-room-2400.jpg" '
        f'srcset="{img}office-waiting-room-1200.jpg 1200w, {img}office-waiting-room-2400.jpg 2400w" '
        'sizes="(max-width: 1228px) 100vw, 1132px" '
        'alt="Waiting room and front desk at Evergrowth Chiropractic in Las Vegas" '
        'width="2400" height="1144" loading="lazy"></figure>'
    )
    shots = [
        (
            "office-hallway-chart-1200.jpg",
            "office-hallway-chart-2400.jpg",
            "2400",
            "1200",
            "1200",
            "Hallway looking toward the front desk, with teal barn doors and a spinal chart at Evergrowth Chiropractic",
        ),
        (
            "office-hallway-1200.jpg",
            "office-hallway-2400.jpg",
            "2400",
            "1200",
            "1200",
            "Hallway with teal barn doors leading to the front desk at Evergrowth Chiropractic",
        ),
        (
            "office-door-sign-1200.jpg",
            "office-door-sign.jpg",
            "2202",
            "1200",
            "754",
            "Suite 240B door sign for Evergrowth Chiropractic",
        ),
    ]
    cards = []
    for small, large, large_w, width, height, alt in shots:
        cards.append(
            "<figure><img "
            f'src="{img}{small}" '
            f'srcset="{img}{small} 1200w, {img}{large} {large_w}w" '
            'sizes="(max-width: 640px) 100vw, 550px" '
            f'alt="{esc(alt)}" '
            f'width="{width}" height="{height}" loading="lazy"></figure>'
        )
    return (
        '<section><div class="container tour-gallery">'
        + pano
        + '<div class="tour-grid">'
        + "".join(cards)
        + "</div></div></section>"
    )


def review_html():
    cards = []
    for text, name in REVIEWS:
        paras = "".join(f"<p>{esc(part)}</p>" for part in text.split("\n") if part.strip())
        cards.append(f'<figure class="t-card" style="margin:0">{paras}<cite>{esc(name)}</cite></figure>')
    return (
        '<section class="tint"><div class="container"><div class="center">'
        '<span class="eyebrow">Our testimonial</span>'
        "<h2>What patients say about Evergrowth Chiropractic</h2></div>"
        '<div class="t-grid ">' + "".join(cards) + "</div></div></section>"
    )


def rewire_nav():
    old = f'site-map.html#{SLUG}"'
    new = f'{SLUG}/"'
    changed = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = path.read_text()
        if old not in text:
            continue
        path.write_text(text.replace(old, new))
        changed.append(str(path.relative_to(ROOT)))
    print("rewired", len(changed))
    index = (ROOT / "index.html").read_text()
    if f'href="{SLUG}/"' not in index:
        raise SystemExit("home nav was not rewired")
    leftover = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        if f"site-map.html#{SLUG}" in path.read_text():
            leftover.append(str(path.relative_to(ROOT)))
    if leftover:
        raise SystemExit("anchor still in " + ", ".join(leftover))


def mark_site_map():
    path = ROOT / "site-map.html"
    html_text = path.read_text()
    start = html_text.find('<tr id="office-tour">')
    if start < 0:
        raise SystemExit("site-map row missing")
    end = html_text.find("</tr>", start)
    row = html_text[start:end]
    old_cell = "<td>planned (not built)</td>"
    new_cell = '<td><a href="office-tour/">office-tour/</a> (built)</td>'
    if old_cell in row:
        row = row.replace(old_cell, new_cell, 1)
    elif "office-tour/" not in row:
        raise SystemExit("status cell missing")
    row = row.replace(
        '<span class="tag image">image missing</span>',
        '<span class="tag ready">content ready</span>',
        1,
    )
    note_start = row.rfind("<td>")
    if note_start < 0:
        raise SystemExit("note cell missing")
    row = row[:note_start] + f"<td>{html.escape(NOTE)}</td>"
    path.write_text(html_text[:start] + row + html_text[end:])
    print("site-map marked built")


def stamp(previous):
    # This page does not edit the home page. The shared stamp hashes index.html,
    # so an office-tour-only publish would keep the previous id.
    build_id = hashlib.sha256((ROOT / "office-tour" / "index.html").read_bytes()).hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    check_copy()
    previous = (ROOT / "build-id.txt").read_text().strip()
    home = shell.href("index", DEPTH)
    links = "".join(
        f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in WHO
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Who We Are<span>/</span>Office Tour</div><h1>Welcome to The Office</h1></div></section>
{gallery_html()}
{review_html()}
<section><div class="container article-grid"><article class="article"><h2>Ready To Find Out More Information?</h2><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Who We Are</h3>{links}</div></aside></div></section>'''
    page = shell.render_page(
        "Office Tour | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "Welcome to The Office",
        body,
        DEPTH,
    )
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording in office tour page")
    if "1263 E Silverado" in page or "Grow Gonstead" in page:
        raise SystemExit("old footer copied onto office tour page")
    if 'href="/' in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link in office tour page")
    if 'target="_blank"' in page or "target=" in main:
        raise SystemExit("outside link in office tour page")
    allowed = {
        "office-waiting-room-1200.jpg",
        "office-waiting-room-2400.jpg",
        "office-hallway-1200.jpg",
        "office-hallway-2400.jpg",
        "office-hallway-chart-1200.jpg",
        "office-hallway-chart-2400.jpg",
        "office-door-sign-1200.jpg",
        "office-door-sign.jpg",
    }
    if "20251020_162305" in page or "office-tour-3" in page or "20250814_" in page or "20251020_" in page:
        raise SystemExit("old office photo on the page")
    srcs = []
    for chunk in main.split("<img")[1:]:
        src = chunk.split('src="', 1)[1].split('"', 1)[0].rsplit("/", 1)[-1]
        srcs.append(src)
        if src not in allowed:
            raise SystemExit("unexpected image " + src)
    if srcs != [
        "office-waiting-room-2400.jpg",
        "office-hallway-chart-1200.jpg",
        "office-hallway-1200.jpg",
        "office-door-sign-1200.jpg",
    ]:
        raise SystemExit("gallery photos out of order")
    if main.count('loading="lazy"') != 4 or "<figcaption" in main:
        raise SystemExit("gallery must be four lazy images with no captions")
    for name in allowed:
        path = ROOT / "assets" / "img" / name
        if not path.exists() or path.stat().st_size < 1000:
            raise SystemExit("missing photo file " + name)
    if "\u2014" in page or "Dr. [Last Name]" in page:
        raise SystemExit("em dash or placeholder on office tour page")
    before, after_reviews = main.split("Our testimonial", 1)
    written = before + after_reviews.split("</section>", 1)[1]
    for word in ("treat", "treatment", "treating", "treated"):
        if word in written.lower():
            raise SystemExit("written text uses " + word)
    for needed in (
        "Welcome to The Office",
        "Ready To Find Out More Information?",
        "DNoria R.",
        "Emily E.",
        "Laurie W.",
        "Andrea V.",
        "Dr Will is a GREAT chiropractor.",
        "Dr. Will is amazing!",
        'href="../book-appointment/"',
        'href="../office-tour/"',
        'href="../testimonials/"',
        "9555 S Eastern Ave, Ste 240B",
        "Las Vegas, NV 89123",
        "10am to 1pm, 3pm to 6pm",
        "Appointments only",
        "Info@evergrowthchiro.com",
        'content="noindex, nofollow"',
        'href="../assets/style.css"',
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    if page.count("<cite>") != 4:
        raise SystemExit("expected four reviews")
    dest = ROOT / "office-tour" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    rewire_nav()
    mark_site_map()
    build_id = stamp(previous)
    print(dest)
    return build_id


if __name__ == "__main__":
    build()
