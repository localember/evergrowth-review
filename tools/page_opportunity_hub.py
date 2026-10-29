"""Opportunity Hub hiring page. Copy is the 2026-06-06 archive text.

Wording changes, and only these:
- Title "Opportunity Hub - Chiropractor Henderson NV | New Patient Experience"
  becomes "Opportunity Hub | Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- The old footer address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183
  is not copied. The shared shell supplies 9555 S Eastern Ave, Ste 240B,
  Las Vegas, NV 89123.
- The old footer hours (Mon through Fri 10am - 6pm, Sat Closed, Sun Closed)
  are not copied. The shared shell supplies the new hours.
The hiring paragraphs already say Las Vegas. They are left as written.
No doctor name appears in the hiring copy, so there is no name swap.
The New Patient Special block is left off.
The form is shown and does not submit. It shows the same not-active notice as Book Appointment.
No images.
"""
import hashlib
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SLUG = "opportunity-hub"
SRC = Path("/tmp/evergrowth-src/old/pages/opportunity-hub_20260606.txt")

HEADING = "Evergrowth Chiropractic Opportunity Hub"
SUBHEAD = "Now Hiring: Associate Chiropractor \u2013 Join a Thriving Gonstead Practice in Las Vegas, NV"
PARAS = [
    "Evergrowth Chiropractic is expanding! We're a busy, principled Gonstead chiropractic clinic located in the heart of Las Vegas, Nevada, and we\u2019re looking for a dedicated Associate Gonstead Chiropractor to join our mission of delivering life-changing care through the Gonstead System.",
    "We serve a loyal and growing patient base seeking specific, results-driven chiropractic care. If you're passionate about getting to the root cause of patient issues and want to sharpen your skills in a fast-paced, supportive environment, we want to hear from you.",
]
LOOKING_H = "What We\u2019re Looking For:"
LOOKING = [
    "A licensed (or soon-to-be licensed) Gonstead chiropractor in Nevada",
    "A heart for service and a commitment to clinical excellence",
    "Great communication skills and a team-first mindset",
    "Open to mentorship and continual learning",
]
OFFER_H = "What We Offer:"
OFFER = [
    "Structured mentorship from an experienced Gonstead practitioner",
    "Competitive compensation with growth potential",
    "Steady stream of new patients",
    "Supportive team culture in a high-energy office",
    "Opportunity to build a rewarding, long-term career",
]
CLOSING = "Whether you're a recent graduate or a seasoned doc ready for a change, Evergrowth Chiropractic offers a rare opportunity to grow in the art, science, and philosophy of Gonstead chiropractic \u2014 in one of the fastest-growing cities in the country."
READY = "Ready to grow with us?"
FIELDS = ["First Name*", "Last Name*", "Email*", "Phone*", "Year*", "College*"]
CLOSER = "Ready To Find Out More Information?"
REQUEST = "Request An Appointment"

NOTE = (
    "BUILT from old/pages/opportunity-hub_20260606.txt. Kept per Brevin. "
    "Hiring copy left as written, including the Las Vegas lines already in the archive. "
    "Swaps: title Henderson and New Patient Experience to Las Vegas and Evergrowth Chiropractic; "
    "footer address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 replaced by the shared shell address "
    "9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123; "
    "old hours Mon through Fri 10am - 6pm, Sat and Sun Closed, replaced by the shared shell hours. "
    "No doctor name in the hiring copy, so no name swap. "
    "New Patient Special and New Patient Special Offer left off. "
    "Form fields shown: first name, last name, email, phone, year, college. The form shows the not-active notice and does not submit. "
    "No date of birth field. No images."
)


def esc(text):
    return html.escape(text, quote=False)


def check_copy():
    raw = SRC.read_text()
    for text, label in (
        ("Opportunity Hub - Chiropractor Henderson NV | New Patient Experience", "old title"),
        (HEADING, "heading"),
        (SUBHEAD, "subhead"),
        (LOOKING_H, "looking heading"),
        (OFFER_H, "offer heading"),
        (CLOSING, "closing"),
        (READY, "form heading"),
        (CLOSER, "closer"),
        (REQUEST, "request button"),
        ("New Patient Special Offer", "special, which this page leaves off"),
        ("1263 E Silverado Ranch Blvd #105A", "old address"),
        ("Henderson, NV 89183", "old city"),
        ("Mon 10am - 6pm", "old Monday hours"),
        ("Fri 10am - 6pm", "old Friday hours"),
        ("Sat Closed", "old Saturday"),
        ("Sun Closed", "old Sunday"),
        ("Submit", "submit"),
    ):
        if text not in raw:
            raise SystemExit("missing from archive: " + label)
    for text in PARAS + LOOKING + OFFER + FIELDS:
        if text not in raw:
            raise SystemExit("missing from archive: " + text[:48])
    hiring = raw.split(HEADING, 1)[1].split("New Patient Special Offer", 1)[0]
    if "Henderson" in hiring:
        raise SystemExit("hiring copy now says Henderson; log the swap before building")
    if "Dr. Willie" in hiring or "Dr Will" in hiring or "8+ Years" in hiring:
        raise SystemExit("hiring copy gained a name or bio; do not edit it here")


def items(lines):
    return "<ul>" + "".join(f"<li>{esc(line)}</li>" for line in lines) + "</ul>"


def form_html():
    specs = [
        ("first-name", "First Name*", "text"),
        ("last-name", "Last Name*", "text"),
        ("email", "Email*", "email"),
        ("phone", "Phone*", "tel"),
        ("year", "Year*", "text"),
        ("college", "College*", "text"),
    ]
    fields = []
    for field_id, label, kind in specs:
        fields.append(
            f'<div><label for="{field_id}">{esc(label)}</label>'
            f'<input id="{field_id}" name="{field_id}" type="{kind}" required></div>'
        )
    return (
        '<form class="contact-form" onsubmit="return false">'
        + '<p class="full form-notice" role="status">This form is not active in this preview and will not accept a message.</p>'
        + "".join(fields)
        + '<div class="full"><button class="btn" type="button" disabled>Submit</button></div></form>'
    )


def hours_html():
    rows = (
        ("Mon, Wed, Thu", "10am to 1pm, 3pm to 6pm"),
        ("Tuesday", "3pm to 6pm"),
        ("Friday", "Appointments only"),
        ("Sat, Sun", "Closed"),
    )
    return "<ul>" + "".join(f"<li><span>{day}</span><span>{when}</span></li>" for day, when in rows) + "</ul>"


def rewire_nav():
    old = f"site-map.html#{SLUG}"
    new = f"{SLUG}/"
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
    row = row.replace(
        '<span class="tag partial">content partial</span>',
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
    build_id = hashlib.sha256((ROOT / "index.html").read_bytes()).hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    check_copy()
    previous = (ROOT / "build-id.txt").read_text().strip()
    home = shell.href("index", DEPTH)
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Contact<span>/</span>Opportunity Hub</div><h1>{esc(HEADING)}</h1><p class="sub-h">{esc(SUBHEAD)}</p></div></section>
<section><div class="container article-grid"><article class="article">{"".join(f"<p>{esc(para)}</p>" for para in PARAS)}<h2>{esc(LOOKING_H)}</h2>{items(LOOKING)}<h2>{esc(OFFER_H)}</h2>{items(OFFER)}<p>{esc(CLOSING)}</p></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p><p style="margin:8px 0 0;text-align:center"><a href="mailto:{shell.EMAIL}">{shell.EMAIL}</a></p></div>
<div class="side-card"><h3>Hours</h3>{hours_html()}</div></aside></div></section>
<section><div class="container" style="max-width:800px"><h2>{esc(READY)}</h2>{form_html()}</div></section>
<section class="cta-band"><div class="container"><div class="box"><h2>{esc(CLOSER)}</h2><div class="book-actions" style="justify-content:center">{shell.book_btn(DEPTH, REQUEST)}</div></div></div></section>'''
    page = shell.render_page(
        "Opportunity Hub | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        SUBHEAD,
        body,
        DEPTH,
    )
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording on opportunity hub page")
    if "1263 E Silverado" in page or "Grow Gonstead" in page:
        raise SystemExit("old footer copied onto opportunity hub page")
    if 'href="/' in page or "evergrowthchiro.com/" in page or "web.archive.org" in page:
        raise SystemExit("root-absolute or live-site link on opportunity hub page")
    if 'target="_blank"' in page or 'rel="noopener"' in page:
        raise SystemExit("outside link on opportunity hub page")
    if "placeholder=" in page or "Dr. [Last Name]" in page:
        raise SystemExit("placeholder text on opportunity hub page")
    if page.count("\u2014") != 1 or CLOSING not in page:
        raise SystemExit("em dash outside the client closing sentence")
    if "date of birth" in page.lower() or "dob" in page.lower():
        raise SystemExit("date of birth field on opportunity hub page")
    if "20250814_131251" in page or "20251020_162305" in page:
        raise SystemExit("unconfirmed photo on opportunity hub page")
    if "<img" in main:
        raise SystemExit("image on opportunity hub page")
    social = ("facebook", "instagram", "linkedin", "youtube", "twitter")
    if any(word in page.lower() for word in social):
        raise SystemExit("social link on opportunity hub page")
    for word in ("treat", "treatment", "treating", "treated"):
        if word in main.lower():
            raise SystemExit("written or client text uses " + word)
    if 'action="' in main or "onsubmit=\"return false\"" not in main or "This form is not active in this preview and will not accept a message." not in main:
        raise SystemExit("form is wired or missing the not-active notice")
    if 'type="submit"' in main:
        raise SystemExit("hiring form still has a submit button")
    for needed in (
        HEADING,
        SUBHEAD,
        CLOSING,
        READY,
        CLOSER,
        ">Submit</button>",
        'href="../book-appointment/"',
        "9555 S Eastern Ave, Ste 240B",
        "Las Vegas, NV 89123",
        "10am to 1pm, 3pm to 6pm",
        "Appointments only",
        ">Sat, Sun</span>",
        ">Closed</span>",
        "Info@evergrowthchiro.com",
        "(702) 389-5009",
        'content="noindex, nofollow"',
        'href="../assets/style.css"',
        'href="../opportunity-hub/"',
        "Year*",
        "College*",
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    for field in FIELDS:
        if main.count(field) != 1:
            raise SystemExit("form label count for " + field)
    book = page.split('href="../book-appointment/"', 1)[1].split(">", 1)[0]
    if "target" in book:
        raise SystemExit("Book Appointment opens in a new tab")
    if page.count('href="../book-appointment/"') < 2:
        raise SystemExit("expected the header and body booking links")
    dest = ROOT / SLUG / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    rewire_nav()
    mark_site_map()
    built = dest.read_text()
    if f'href="../{SLUG}/"' not in built:
        raise SystemExit("page nav lost its own link")
    if "site-map.html#opportunity-hub" in built:
        raise SystemExit("page still points at the site map")
    build_id = stamp(previous)
    if len(dest.read_bytes()) <= 10000:
        raise SystemExit("opportunity hub page is under 10kb")
    print(dest)
    return build_id


if __name__ == "__main__":
    build()
