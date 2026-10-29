"""New Patient Paperwork page.

The form is a printable PDF. Patients download it, print it, and bring it
to the first visit or email a scan. Nothing on this page may say the form
can be filled out or submitted online.

PAPERWORK_URL is the hosted intake PDF in this repo. The button is a
new-tab link with rel noopener. It must not point at the client's
current website.
"""
import hashlib
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1

# Hosted intake PDF. Depth-1 path from this page.
PAPERWORK_URL = "../assets/evergrowth-new-patient-paperwork.pdf"
EMAIL = "info@evergrowthchiro.com"
HEADING = "Printable Patient Paperwork"
BUTTON = "Download PDF"
NOTE = (
    "Our new patient paperwork is a printable PDF. Please download and print it, "
    "fill it out, then bring it with you to your first visit or scan and email it to "
)

PATIENTS = [
    ("First Visit", "first-visit"),
    ("Second Visit", "second-visit"),
    ("Follow-Up Visits", "follow-up-visit"),
    ("New Patient Paperwork", "new-patient-paperwork"),
    ("Payment Plans", "payment-plans"),
]


def esc(text):
    return html.escape(text, quote=False)


def note_html():
    href = html.escape("mailto:" + EMAIL, quote=True)
    return f'<p>{esc(NOTE)}<a href="{href}">{esc(EMAIL)}</a>.</p>'


def complete_btn():
    url = PAPERWORK_URL.strip()
    if not url:
        return f'<span class="btn" aria-disabled="true">{BUTTON}</span>'
    if "evergrowthchiro.com" in url.lower():
        raise SystemExit("paperwork link must not point at the client's current website")
    href = html.escape(url, quote=True)
    return f'<a class="btn" href="{href}" target="_blank" rel="noopener">{BUTTON}</a>'


def stamp(previous):
    page = ROOT / "new-patient-paperwork" / "index.html"
    build_id = hashlib.sha256(page.read_bytes()).hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    previous = (ROOT / "build-id.txt").read_text().strip()
    home = shell.href("index", DEPTH)
    links = "".join(
        f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in PATIENTS
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Patients<span>/</span>New Patient Paperwork</div><h1>NEW PATIENT PAPERWORK</h1></div></section>
<section style="padding-top:40px"><div class="container article-grid"><article class="article">{note_html()}<h2>{esc(HEADING)}</h2><p>{complete_btn()}</p></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Patients</h3>{links}</div></aside></div></section>'''
    page = shell.render_page(
        "New Patient Paperwork - Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        NOTE + EMAIL + ".",
        body,
        DEPTH,
    )
    page = page.replace('assets/style.css"', 'assets/style.css?v=r41"', 1)
    article = page.split("<article", 1)[1].split("</article>", 1)[0].lower()
    for banned in (
        "online",
        "click to complete",
        "submit",
        "completed in the convenience",
    ):
        if banned in article:
            raise SystemExit("paperwork page still suggests online forms: " + banned)
    for needed in (
        NOTE,
        f'href="mailto:{EMAIL}"',
        ">" + EMAIL + "<",
        PAPERWORK_URL,
        BUTTON,
        HEADING,
        'content="noindex, nofollow"',
        'href="../assets/style.css?v=r41"',
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    dest = ROOT / "new-patient-paperwork" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    build_id = stamp(previous)
    print(dest)
    return build_id


if __name__ == "__main__":
    build()
