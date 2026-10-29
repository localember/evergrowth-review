"""Testimonials page. Copy is the 2026-05-11 archive plus the four Home reviews.

The old testimonials page has eight reviews. Home (2026-03-14) has four
more. This page shows those twelve, old eight first, then the Home four.
No stars, no counts, no images, no special offer.

Wording changes, and only these:
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- The old footer address and hours are not copied. The shared shell
  supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the
  new hours.
Reviews stay word for word, including the archive pairing. "Love their
new facility" belongs to Lorena M. Jose P. is the constant-pain review.
"""
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
OLD = Path("/tmp/evergrowth-src/old/pages/testimonials_20260511.txt")
HOME = Path("/tmp/evergrowth-src/old/pages/home_20260314.txt")

OLD_NAMES = [
    "John S.",
    "Jose P.",
    "Lorena M.",
    "Steve M.",
    "Moe Z.",
    "Britney R.",
    "Vince T.",
    "A. Mendoza",
]
HOME_NAMES = ["DNoria R.", "Emily E.", "Laurie W.", "Andrea V."]

WHO = [
    ("Meet the Doctor", "meet-the-doctor"),
    ("Testimonials", "testimonials"),
    ("Office Tour", "office-tour"),
    ("Blog", "blog"),
]


def esc(text):
    return html.escape(text, quote=False)


def split_named(block, names):
    reviews = []
    rest = block
    for name in names:
        marker = "\n" + name
        if marker not in rest:
            raise SystemExit("review name missing from archive: " + name)
        quote, rest = rest.split(marker, 1)
        quote = quote.strip("\n")
        if not quote:
            raise SystemExit("empty review: " + name)
        reviews.append((quote, name))
        rest = rest.lstrip("\n")
    return reviews


def load_reviews():
    old_raw = OLD.read_text()
    home_raw = HOME.read_text()
    if "Chiropractic Testimonials - Chiropractor Henderson NV | New Patient Experience" not in old_raw:
        raise SystemExit("copy drift against archive text: title")
    old_block = old_raw.split("Chiropractic Patient Testimonials\n", 1)[1]
    old_block = old_block.split("\nNew Patient Special Offer", 1)[0]
    home_block = home_raw.split("What patients say about Evergrowth Chiropractic\n", 1)[1]
    home_block = home_block.split("\nWhy Choose a Chiropractor", 1)[0]
    old = split_named(old_block, OLD_NAMES)
    home = split_named(home_block, HOME_NAMES)
    by_name = {name: quote for quote, name in old}
    if not by_name["Lorena M."].startswith("Love their new facility"):
        raise SystemExit("new facility line is not Lorena M.")
    if "new facility" in by_name["Jose P."].lower():
        raise SystemExit("Jose P. gained a facility line; re-check the archive")
    if not by_name["Jose P."].startswith("Love this place"):
        raise SystemExit("Jose P. review drifted")
    if len(old) + len(home) != 12:
        raise SystemExit("expected 12 reviews")
    return old + home


def cards(reviews):
    out = []
    for text, name in reviews:
        paras = "".join(f"<p>{esc(part)}</p>" for part in text.split("\n") if part.strip())
        out.append(
            f'<figure class="t-card" style="margin:0">{paras}<cite>{esc(name)}</cite></figure>'
        )
    return "".join(out)


def retarget_menu():
    changed = 0
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = path.read_text()
        new = text.replace("../site-map.html#testimonials", "../testimonials/")
        new = new.replace("site-map.html#testimonials", "testimonials/")
        if new != text:
            path.write_text(new)
            changed += 1
    return changed


def build():
    reviews = load_reviews()
    home = shell.href("index", DEPTH)
    links = "".join(
        f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in WHO
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Who We Are<span>/</span>Testimonials</div><h1>Chiropractic Patient Testimonials</h1></div></section>
<section class="tint"><div class="container"><div class="t-grid three">{cards(reviews)}</div></div></section>
<section><div class="container article-grid"><article class="article"><h2>Ready To Find Out More Information?</h2><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Who We Are</h3>{links}</div></aside></div></section>'''
    page = shell.render_page(
        "Chiropractic Testimonials | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "Chiropractic Patient Testimonials",
        body,
        DEPTH,
    )
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording in testimonials page")
    if "1263 E Silverado" in page or "Grow Gonstead" in page:
        raise SystemExit("old footer copied onto testimonials page")
    if 'href="/' in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link in testimonials page")
    if 'target="_blank"' in page or "★" in page or "☆" in page:
        raise SystemExit("outside link or star rating in testimonials page")
    if page.count("<cite>") != 12 or 'class="t-grid three"' not in page:
        raise SystemExit("grid is not 12 cards in three columns")
    if 'href="../book-appointment/"' not in page or 'target=' in page.split("<main", 1)[1].split("</main>", 1)[0]:
        raise SystemExit("booking link is not the internal same-tab path")
    dest = ROOT / "testimonials" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    n = retarget_menu()
    print(dest)
    print(f"menu links retargeted in {n} file(s)")


if __name__ == "__main__":
    build()
