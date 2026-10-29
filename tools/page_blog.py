"""Blog index. Copy is the 2026-05-11 archive of /blog/.

Wording changes, and only these:
- Title "Blog - Chiropractor Henderson NV | New Patient Experience"
  becomes "Blog | Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- Every "Henderson" in a post title or excerpt becomes "Las Vegas".
- The old footer address and hours are not copied. The shared shell
  supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the
  new hours.
- "New Patient Special Offer" is left off.
- The closer button "Request An Appointment" is the shared Book
  Appointment link, same tab, same as the other built pages.
No doctor name appears in the index copy, so there is no name swap.
No images. Post cards are plain until each post is built.
Batch 1 and batch 2 Read more links point at the post. The rest point at the site-map row.
"""
import hashlib
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SLUG = "blog"
SRC = Path("/tmp/evergrowth-src/old/pages/blog_20260511.txt")
OLD_PAGES = Path("/tmp/evergrowth-src/old/pages")

# Archive order on /blog/, newest first. Slugs are the old Las Vegas paths.
SLUGS = [
    "las-vegas-chiropractor-discusses-herniated-discs",
    "headache-tips-from-a-las-vegas-chiropractic-office",
    "las-vegas-chiropractic-clinics-help-joint-inflammation",
    "las-vegas-chiropractor-may-help-tmj",
    "las-vegas-chiropractic-office-helps-whiplash",
    "las-vegas-chiropractors-may-relieve-migraines",
    "las-vegas-chiropractor-describes-stretching",
    "las-vegas-chiropractors-help-range-of-motion",
    "sciatic-leg-pain-in-las-vegas",
    "las-vegas-chiropractor-talks-about-wellness-care",
    "achieve-a-healthier-spine-in-las-vegas",
    "las-vegas-athletes-improve-with-chiropractic-care",
    "chiropractor-in-las-vegas-talks-about-headaches",
    "chiropractors-in-las-vegas-have-extensive-schooling",
    "chiropractic-treatment-for-car-accidents-in-las-vegas",
    "chiropractic-for-pregnancy-in-las-vegas",
    "las-vegas-chiropractor-talks-about-improving-your-health",
    "3-common-conditions-las-vegas-chiropractors-help",
    "car-accident-tips-from-a-las-vegas-chiropractor",
    "the-sitting-epidemic-in-las-vegas",
    "are-you-looking-for-a-top-las-vegas-chiropractor",
    "exercise-smarter-in-las-vegas",
    "back-pain-tips-from-a-las-vegas-chiropractor",
]

BUILT_POSTS = {
    "3-common-conditions-las-vegas-chiropractors-help",
    "achieve-a-healthier-spine-in-las-vegas",
    "are-you-looking-for-a-top-las-vegas-chiropractor",
    "back-pain-tips-from-a-las-vegas-chiropractor",
    "car-accident-tips-from-a-las-vegas-chiropractor",
    "chiropractic-for-pregnancy-in-las-vegas",
    "chiropractic-treatment-for-car-accidents-in-las-vegas",
    "chiropractor-in-las-vegas-talks-about-headaches",
    "chiropractors-in-las-vegas-have-extensive-schooling",
    "exercise-smarter-in-las-vegas",
    "headache-tips-from-a-las-vegas-chiropractic-office",
    "las-vegas-athletes-improve-with-chiropractic-care",
}


def card_href(slug):
    if slug in BUILT_POSTS:
        return f"../{slug}/"
    return f"../site-map.html#blog-{slug}"


NOTE = (
    "BUILT from old/pages/blog_20260511.txt. 23 post cards in archive order. "
    "Henderson swapped to Las Vegas in every title and excerpt that named the city. "
    "No images: post photos are not in the archive, so the cards are plain. "
    "Batch 1 and batch 2 posts link to their pages. The other Read more links go to the site map row until that post is built. "
    "New Patient Special left off. "
    "The old Request An Appointment closer is the shared Book Appointment button."
)

CLOSER = "Ready To Find Out More Information?"


def esc(text):
    return html.escape(text, quote=False)


def parse_posts():
    lines = SRC.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("Henderson NV Chiropractor Discusses Herniated Discs"):
            start = i
            break
    if start is None:
        raise SystemExit("could not find the first blog card in the archive")
    posts = []
    i = start
    while i < len(lines):
        if lines[i].startswith("New Patient Special"):
            break
        if i + 2 >= len(lines):
            raise SystemExit("blog archive ended mid card")
        title, excerpt, more = lines[i], lines[i + 1], lines[i + 2]
        if more != "Read more":
            raise SystemExit("expected Read more, got " + more)
        posts.append((title.rstrip(), excerpt.rstrip()))
        i += 3
    if len(posts) != len(SLUGS):
        raise SystemExit(f"expected {len(SLUGS)} posts, got {len(posts)}")
    return posts


def city_swap(text):
    if "Henderson" not in text:
        return text
    return text.replace("Henderson", "Las Vegas")


def load_cards():
    swaps = []
    cards = []
    for slug, (title, excerpt) in zip(SLUGS, parse_posts()):
        matches = [
            path for path in OLD_PAGES.glob(slug + "_*.txt")
            if not path.name.endswith(".images.txt")
        ]
        if len(matches) != 1:
            raise SystemExit("missing archive file for " + slug)
        url_line = matches[0].read_text().splitlines()[0]
        if f"/{slug}/" not in url_line:
            raise SystemExit("slug does not match archive url: " + slug)
        new_title = city_swap(title)
        new_excerpt = city_swap(excerpt)
        if new_title != title:
            swaps.append((title, new_title))
        if new_excerpt != excerpt:
            swaps.append((excerpt, new_excerpt))
        if "Henderson" in new_title or "Henderson" in new_excerpt:
            raise SystemExit("Henderson remained in " + slug)
        cards.append((slug, new_title, new_excerpt))
    return cards, swaps


def cards_html(cards):
    items = []
    for slug, title, excerpt in cards:
        href = card_href(slug)
        items.append(
            '<article class="post-card">'
            f'<h2><a href="{href}">{esc(title)}</a></h2>'
            f"<p>{esc(excerpt)}</p>"
            f'<a class="more" href="{href}">Read more</a>'
            "</article>"
        )
    return '<div class="post-grid">' + "".join(items) + "</div>"


def rewire_nav():
    old = 'site-map.html#blog"'
    new = 'blog/"'
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
    if 'href="blog/"' not in index:
        raise SystemExit("home nav was not rewired")
    leftover = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        if old in path.read_text():
            leftover.append(str(path.relative_to(ROOT)))
    if leftover:
        raise SystemExit("blog index anchor still in " + ", ".join(leftover))


def mark_site_map():
    path = ROOT / "site-map.html"
    html_text = path.read_text()
    start = html_text.find(f'<tr id="{SLUG}">')
    if start < 0:
        raise SystemExit("site-map row missing")
    end = html_text.find("</tr>", start)
    row = html_text[start:end]
    old_cell = "<td>planned (not built)</td>"
    new_cell = f'<td><a href="{SLUG}/">{SLUG}/</a> (built)</td>'
    if old_cell not in row:
        raise SystemExit("status cell missing")
    row = row.replace(old_cell, new_cell, 1)
    note_start = row.rfind("<td>")
    if note_start < 0:
        raise SystemExit("note cell missing")
    row = row[:note_start] + f"<td>{html.escape(NOTE)}</td>"
    path.write_text(html_text[:start] + row + html_text[end:])
    print("site-map marked built")


def stamp(previous):
    build_id = hashlib.sha256((ROOT / "index.html").read_bytes()).hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    cards, swaps = load_cards()
    previous = (ROOT / "build-id.txt").read_text().strip()
    home = shell.href("index", DEPTH)
    body = (
        f'<section class="page-hero"><div class="container"><div class="crumbs">'
        f'<a href="{home}">Home</a><span>/</span>Who We Are<span>/</span>Blog</div>'
        f"<h1>Blog</h1></div></section>"
        f'<section><div class="container">{cards_html(cards)}</div></section>'
        f'<section><div class="container article-grid"><article class="article">'
        f"<h2>{esc(CLOSER)}</h2>"
        f'<div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}'
        f'<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a>'
        f"</div></article></div></section>"
    )
    page = shell.render_page(
        "Blog | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        cards[0][2],
        body,
        DEPTH,
    )
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording on the blog index")
    if "1263 E Silverado" in page or "89183" in page:
        raise SystemExit("old address on the blog index")
    if 'href="/' in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link on the blog index")
    if "evergrowthchiro.com" not in page.split("mailto:", 1)[1].split('"', 1)[0]:
        raise SystemExit("email missing")
    if 'target="_blank"' in page or 'rel="noopener"' in page:
        raise SystemExit("outside link on the blog index")
    if "placeholder=" in page or "Dr. [Last Name]" in page:
        raise SystemExit("placeholder on the blog index")
    if "date of birth" in page.lower() or "20250814_131251" in page or "20251020_162305" in page:
        raise SystemExit("forbidden field or photo on the blog index")
    if "<img" in main:
        raise SystemExit("image on the blog index")
    social = ("facebook", "instagram", "linkedin", "youtube", "twitter")
    if any(word in page.lower() for word in social):
        raise SystemExit("social link on the blog index")
    authored = "Who We Are" + "Blog" + CLOSER + "Book Appointment" + "Read more"
    for word in ("treat", "treatment", "treating", "treated"):
        if word in authored.lower():
            raise SystemExit("authored text uses " + word)
    client_title = "Chiropractic Treatment for Car Accidents in Las Vegas NV"
    if page.count(client_title) != 1:
        raise SystemExit("client Treatment title missing or repeated")
    if "\u2014" in (CLOSER + "Blog" + "Who We Are"):
        raise SystemExit("em dash in authored text")
    for slug, title, excerpt in cards:
        if title not in page or excerpt not in page:
            raise SystemExit("missing card copy: " + title)
        if f'href="{card_href(slug)}"' not in page:
            raise SystemExit("missing read-more link: " + slug)
    if page.count('class="post-card"') != 23 or page.count(">Read more<") != 23:
        raise SystemExit("expected 23 cards")
    for needed in (
        "<h1>Blog</h1>",
        'href="../book-appointment/"',
        "9555 S Eastern Ave, Ste 240B",
        "Las Vegas, NV 89123",
        "10am to 1pm, 3pm to 6pm",
        "Appointments only",
        ">Sat</span>",
        ">Sun</span>",
        ">Closed</span>",
        "Info@evergrowthchiro.com",
        "(702) 389-5009",
        'content="noindex, nofollow"',
        'href="../assets/style.css"',
        'href="../blog/"',
        CLOSER,
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    book = page.split('href="../book-appointment/"', 1)[1].split(">", 1)[0]
    if "target" in book:
        raise SystemExit("Book Appointment opens in a new tab")
    if "Evergrowth Chiropractic provides personalized chiropractic care" not in page.split("</main>", 1)[1]:
        raise SystemExit("footer about line missing")
    dest = ROOT / SLUG / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    rewire_nav()
    mark_site_map()
    build_id = stamp(previous)
    if len(dest.read_bytes()) <= 10000:
        raise SystemExit("blog index is under 10kb")
    log = Path("/tmp/blog-swap-log.txt")
    lines = [f"{len(swaps)} Henderson to Las Vegas swaps", ""]
    for before, after in swaps:
        lines.append("BEFORE: " + before)
        lines.append("AFTER:  " + after)
        lines.append("")
    log.write_text("\n".join(lines))
    print("swaps", len(swaps))
    print(dest)
    return build_id


if __name__ == "__main__":
    build()
