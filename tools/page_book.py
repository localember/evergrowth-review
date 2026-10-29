"""Book Appointment page. Visual form only. It does not submit.

Field labels come from current/book-appointment.txt. The notes label on
that page is Additional Information. The button label is Send Message.
Concern options are the ones listed there, including Other.
The source file did not list New or Existing Patient choices, only the
word Select, so the choices are New Patient and Existing Patient.
The source line "First Number Address" is not a field on this page.
No images. No date of birth field. No link to the client's website.
"""
import hashlib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
SLUG = "book-appointment"
DEPTH = 1

NOTE = (
    "BUILT. Visual form only. It does not submit and has no form action. "
    "Notice: This form is not active in this preview and will not accept a message. "
    "Labels from the current page: First Name, Last Name, Email Address, Phone Number, "
    "Preferred Date, Preferred Time, New or Existing Patient, Additional Information, "
    "Send Message. Concern options: Back Pain, Neck Pain, Headaches, Sciatica, "
    "Posture / Spinal Concerns, Wellness Care, Other. "
    "New or Existing Patient choices were not listed in the source file, so the choices "
    "are New Patient and Existing Patient. The source line First Number Address was not used. "
    "No Henderson, name, address, or hours swaps in the form labels. "
    "Address, hours, and phone come from the shared shell. No images. No date of birth field."
)


def mark_site_map():
    path = ROOT / "site-map.html"
    html_text = path.read_text()
    start = html_text.find(f'<tr id="{SLUG}">')
    if start < 0:
        raise SystemExit("site-map row missing")
    end = html_text.find("</tr>", start)
    row = html_text[start:end]
    old_cell = "<td>book-appointment/ (shell)</td>"
    new_cell = f'<td><a href="{SLUG}/">{SLUG}/</a> (built)</td>'
    if old_cell in row:
        row = row.replace(old_cell, new_cell, 1)
    elif new_cell not in row:
        raise SystemExit("status cell missing")
    note_start = row.rfind("<td>")
    if note_start < 0:
        raise SystemExit("note cell missing")
    row = row[:note_start] + "<td>" + NOTE + "</td>"
    path.write_text(html_text[:start] + row + html_text[end:])
    print("site-map marked built")


def check(page):
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording on book page")
    if "1263 E Silverado" in page or "Grow Gonstead" in page:
        raise SystemExit("old address or footer on book page")
    if 'href="/' in page or "https://evergrowthchiro.com" in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link on book page")
    if "placeholder=" in page or "Dr. [Last Name]" in page or "\u2014" in page:
        raise SystemExit("placeholder or em dash on book page")
    if "date of birth" in page.lower() or "dob" in main.lower():
        raise SystemExit("date of birth field on book page")
    if "20250814_131251" in page or "20251020_162305" in page:
        raise SystemExit("unconfirmed photo on book page")
    if "<img" in main:
        raise SystemExit("image on book page")
    if shell.has_unexpected_social(page):
        raise SystemExit("unexpected social link on book page")
    extra_blank = shell.unexpected_blank_targets(page)
    if extra_blank or "action=" in main or "method=" in main:
        raise SystemExit("outside link or form action on book page")
    if "fetch(" in page or "XMLHttpRequest" in page or "navigator.sendBeacon" in page:
        raise SystemExit("network request on book page")
    if 'type="submit"' in main or "type='submit'" in main:
        raise SystemExit("submit button on book page")
    if 'type="button" disabled' not in main:
        raise SystemExit("send button is not disabled")
    if 'onsubmit="return false"' not in main:
        raise SystemExit("form can submit")
    for word in ("treat", "treatment", "treating", "treated"):
        if word in main.lower():
            raise SystemExit("written text uses " + word)
    for needed in (
        shell.NOTICE,
        "First Name",
        "Last Name",
        "Email Address*",
        "Phone Number",
        "Preferred Date",
        "Preferred Time",
        "New or Existing Patient",
        "New Patient",
        "Existing Patient",
        "Concern",
        "Additional Information",
        "Send Message",
        "Contact Info",
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
        'type="date"',
        'type="time"',
        'type="email"',
        'type="tel"',
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    for concern in shell.CONCERNS:
        if f"<option>{concern}</option>" not in page:
            raise SystemExit("missing concern option: " + concern)
    book = page.split('href="../book-appointment/"', 1)[1].split(">", 1)[0]
    if "target" in book:
        raise SystemExit("Book Appointment opens in a new tab")


def stamp():
    digest = hashlib.sha256()
    digest.update((ROOT / SLUG / "index.html").read_bytes())
    digest.update((ROOT / "assets" / "style.css").read_bytes())
    build_id = digest.hexdigest()[:12]
    previous = (ROOT / "build-id.txt").read_text().strip()
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    page = shell.book_page(DEPTH)
    check(page)
    dest = ROOT / SLUG / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    check(dest.read_text())
    mark_site_map()
    build_id = stamp()
    print(dest)
    return build_id


if __name__ == "__main__":
    build()
