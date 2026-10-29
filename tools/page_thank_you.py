"""Form confirmation page (thank-you-form).

Copy is old/pages/thank-you-form_20260511.txt, with only the allowed swaps.
The old page's design5 thank-you graphic is not used. This row has no images.
New Patient Special and New Patient Special Offer are left off.
Request An Appointment used to open /special/, which is dropped. The words
stay, and the button goes to this preview's book-appointment page, same tab.
"""
import hashlib
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SLUG = "thank-you-form"
SRC = Path("/tmp/evergrowth-src/old/pages/thank-you-form_20260511.txt")

HEADING = "THANK YOU FOR YOUR INTEREST IN Evergrowth Chiropractic"
MESSAGE = (
    "We really appreciate your inquiry. We will be contacting you shortly. "
    "If you would like to speak with one of our staff members immediately, you can reach us at:"
)
CALL = "Click To Call (702) 389-5009"
READY = "Ready To Find Out More Information?"
REQUEST = "Request An Appointment"
TITLE = "Thank You | Chiropractor Las Vegas NV | Evergrowth Chiropractic"

NOTE = (
    "BUILT. Heading and inquiry sentence kept. Click To Call is a phone link. "
    "Request An Appointment keeps those words and goes to book-appointment/ in the same tab "
    "(the old button opened /special/, which is dropped). "
    "Title: Thank You - Chiropractor Henderson NV | New Patient Experience became "
    "Thank You | Chiropractor Las Vegas NV | Evergrowth Chiropractic. "
    "Footer address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 became "
    "9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123. "
    "Footer hours Mon through Fri 10am - 6pm, Sat Closed, Sun Closed became the new hours, "
    "including Friday appointments only and Sat and Sun closed. "
    "Footer copyright Grow Gonstead became Evergrowth Chiropractic. "
    "New Patient Special and New Patient Special Offer left off. "
    "No images. D5-Thank-You-Page.webp not used. No name swap."
)

SWAPS = [
    "Title: Thank You - Chiropractor Henderson NV | New Patient Experience -> Thank You | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
    "Address: 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 -> 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123",
    "Hours: Mon through Fri 10am - 6pm, Sat Closed, Sun Closed -> Mon, Wed, Thu 10am to 1pm and 3pm to 6pm; Tue 3pm to 6pm; Fri appointments only; Sat and Sun closed",
    "Copyright: Grow Gonstead -> Evergrowth Chiropractic",
    "Left off: New Patient Special; New Patient Special Offer",
    "Request An Appointment: old target /special/ -> book-appointment/ (same tab, words unchanged)",
    "Name: no swap. Dr. Willie So does not appear in this source.",
    "Images: none. D5-Thank-You-Page.webp not used (design5 graphic, not a client photo).",
]


def esc(text):
    return html.escape(text, quote=False)


def check_copy():
    text = SRC.read_text()
    for needed, label in (
        ("Thank You - Chiropractor Henderson NV | New Patient Experience", "old title"),
        (HEADING, "heading"),
        (MESSAGE, "message"),
        (CALL, "call button"),
        ("New Patient Special Offer", "special offer, which this page leaves off"),
        ("New Patient Special", "special button, which this page leaves off"),
        (READY, "closer heading"),
        (REQUEST, "request button"),
        ("1263 E Silverado Ranch Blvd #105A", "old address"),
        ("Henderson, NV 89183", "old city"),
        ("Mon 10am - 6pm", "old Monday hours"),
        ("Fri 10am - 6pm", "old Friday hours"),
        ("Sat Closed", "old Saturday"),
        ("Sun Closed", "old Sunday"),
        ("Grow Gonstead", "old copyright"),
        ("(702) 389-5009", "phone"),
    ):
        if needed not in text:
            raise SystemExit("missing from archive: " + label)


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
    if old_cell in row:
        row = row.replace(old_cell, new_cell, 1)
    elif new_cell not in row:
        raise SystemExit("status cell missing")
    note_start = row.rfind("<td>")
    if note_start < 0:
        raise SystemExit("note cell missing")
    row = row[:note_start] + "<td>" + html.escape(NOTE) + "</td>"
    path.write_text(html_text[:start] + row + html_text[end:])
    print("site-map marked built")


def check(page):
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "New Patient Experience" in page or "$47" in page:
        raise SystemExit("forbidden wording on thank-you page")
    if "1263 E Silverado" in page or "Grow Gonstead" in page or "/special/" in page:
        raise SystemExit("old address, copyright, or special link on thank-you page")
    if 'href="/' in page or "evergrowthchiro.com/" in page or "web.archive.org" in page or "thegonsteadfoundation.com" in page:
        raise SystemExit("root-absolute or outside site link on thank-you page")
    if "placeholder=" in page or "Dr. [Last Name]" in page or "\u2014" in page:
        raise SystemExit("placeholder or em dash on thank-you page")
    if "date of birth" in page.lower() or "dob" in main.lower():
        raise SystemExit("date of birth field on thank-you page")
    if "20250814_131251" in page or "20251020_162305" in page:
        raise SystemExit("unconfirmed photo on thank-you page")
    if "<img" in main:
        raise SystemExit("image on thank-you page")
    if shell.has_unexpected_social(page):
        raise SystemExit("unexpected social link on thank-you page")
    extra_blank = shell.unexpected_blank_targets(page)
    if extra_blank:
        raise SystemExit("outside link on thank-you page")
    for word in ("treat", "treatment", "treating", "treated"):
        if word in main.lower():
            raise SystemExit("written or client text uses " + word)
    for needed in (
        HEADING,
        MESSAGE,
        CALL,
        READY,
        REQUEST,
        'href="../book-appointment/"',
        f'href="{shell.TEL}"',
        "9555 S Eastern Ave, Ste 240B",
        "Las Vegas, NV 89123",
        "10am to 1pm, 3pm to 6pm",
        "3pm to 6pm",
        "Appointments only",
        ">Sat</span>",
        ">Sun</span>",
        ">Closed</span>",
        "Info@evergrowthchiro.com",
        "(702) 389-5009",
        'content="noindex, nofollow"',
        'href="../assets/style.css"',
        'src="../assets/site.js"',
        'href="../index.html"',
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    book = page.split('href="../book-appointment/"', 1)[1].split(">", 1)[0]
    if "target" in book:
        raise SystemExit("Book Appointment opens in a new tab")
    if page.count('href="../book-appointment/"') < 3:
        raise SystemExit("expected header, closer, and footer booking links")
    if len(page.encode()) <= 10000:
        raise SystemExit("thank-you page is under 10kb")


def stamp():
    digest = hashlib.sha256()
    digest.update((ROOT / SLUG / "index.html").read_bytes())
    digest.update((ROOT / "site-map.html").read_bytes())
    build_id = digest.hexdigest()[:12]
    previous = (ROOT / "build-id.txt").read_text().strip()
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    check_copy()
    home = shell.href("index", DEPTH)
    body = f'''<section class="page-hero"><div class="container center" style="max-width:820px"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Thank You</div><h1>{esc(HEADING)}</h1></div></section>
<section><div class="container center" style="max-width:720px"><p>{esc(MESSAGE)}</p><p><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{esc(CALL)}</a></p></div></section>
<section class="cta-band"><div class="container"><div class="box"><h2>{esc(READY)}</h2><div class="book-actions" style="justify-content:center">{shell.book_btn(DEPTH, REQUEST)}</div></div></div></section>'''
    page = shell.render_page(
        TITLE,
        MESSAGE,
        body,
        DEPTH,
    )
    check(page)
    dest = ROOT / SLUG / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    check(dest.read_text())
    mark_site_map()
    built = dest.read_text()
    if "site-map.html#thank-you-form" in built:
        raise SystemExit("page still points at the site map")
    build_id = stamp()
    for line in SWAPS:
        print("swap:", line)
    print(dest)
    return build_id


if __name__ == "__main__":
    build()
