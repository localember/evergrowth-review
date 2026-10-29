"""New Patient Paperwork page. Copy is the 2026-04-17 archive text.

The only wording change is the title suffix, from
"Chiropractor Henderson NV | New Patient Experience" to
"Chiropractor Las Vegas NV | Evergrowth Chiropractic".
The heading, the sentence, and the button label stay as written.
No images. No date of birth field.

PAPERWORK_URL stays empty until the client sends the intake form link.
When it is set, the button is an outside link: new tab, rel noopener.
It must not point at the client's current website.
"""
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1

# Client intake form. Empty until that link arrives.
PAPERWORK_URL = ""

SENTENCE = (
    "The office of Evergrowth Chiropractic offers our patient forms online "
    "so they can be completed in the convenience of your own home or office."
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


def complete_btn():
    label = "Click to Complete"
    url = PAPERWORK_URL.strip()
    if not url:
        return f'<span class="btn" aria-disabled="true">{label}</span>'
    if "evergrowthchiro.com" in url.lower():
        raise SystemExit("paperwork link must not point at the client's current website")
    href = html.escape(url, quote=True)
    return f'<a class="btn" href="{href}" target="_blank" rel="noopener">{label}</a>'


def build():
    home = shell.href("index", DEPTH)
    links = "".join(
        f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in PATIENTS
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Patients<span>/</span>New Patient Paperwork</div><h1>NEW PATIENT PAPERWORK</h1></div></section>
<section style="padding-top:40px"><div class="container article-grid"><article class="article"><p>{esc(SENTENCE)}</p><h2>Online Patient Paperwork</h2><p>{complete_btn()}</p></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Patients</h3>{links}</div></aside></div></section>'''
    page = shell.render_page(
        "New Patient Paperwork | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        SENTENCE,
        body,
        DEPTH,
    )
    dest = ROOT / "new-patient-paperwork" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    print(dest)


if __name__ == "__main__":
    build()
