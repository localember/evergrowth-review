"""Second Visit page. Copy is the 2026-06-06 archive text.

Wording changes, and only these:
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- The old footer address and hours are not copied. The shared shell
  supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the
  new hours.
The New Patient Special block on the old page is left off.
Reviews stay word for word. No images. This page has no five-step list
in the source, so it uses the First Visit page frame without step cards.
"""
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SRC = Path("/tmp/evergrowth-src/old/pages/second-visit_20260606.txt")

INTRO = (
    "We will review your x-ray findings, answer any additional questions you may have, "
    "and discuss your current healthcare goals during your second chiropractic visit. "
    "The visit will generally take about 30 minutes. A care plan with follow-up visits "
    "will be determined based on your goals and the outcome you desire."
)
PLANS_H = "Evergrowth Chiropractic OFFERS SEVERAL PRE-PAYMENT PLANS"
PLANS = (
    "They are both cost-effective and convenient to help assist in meeting your healthcare goals. "
    "If you have insurance and seek reimbursement, we will provide you with the necessary "
    "documentation for you to seek reimbursement on your own."
)
UNDERSTANDS_H = "Evergrowth Chiropractic UNDERSTANDS"
UNDERSTANDS = (
    "The financial commitment that is sometimes required to reach the level of health care "
    "that you may desire. So, often times we're willing to go out of our way to help you achieve this."
)

PATIENTS = [
    ("First Visit", "first-visit"),
    ("Second Visit", "second-visit"),
    ("Follow-Up Visits", "follow-up-visit"),
    ("New Patient Paperwork", "new-patient-paperwork"),
    ("Payment Plans", "payment-plans"),
]

REVIEWS = """<section class="tint"><div class="container"><div class="center"><span class="eyebrow">Our testimonial</span><h2>What patients say about Evergrowth Chiropractic</h2></div><div class="t-grid "><figure class="t-card" style="margin:0"><p>Dr Will is a GREAT chiropractor. I used to have lower back pain that was frequent; now I no longer have that pain. With regular adjustments my back stays aligned and free from tension and stiffness. I highly recommend Evergrowth Chiropractic services for individuals and families!</p><cite>DNoria R.</cite></figure><figure class="t-card" style="margin:0"><p>I enjoy my visits to Evergrowth Chiropractic so much! Dr. Will is amazing! I feel so refreshed after my treatments. Wendy is so sweet and friendly as well! I highly recommend their practice; I'm so glad I found them! Relaxing, no stress atmosphere.</p><cite>Emily E.</cite></figure><figure class="t-card" style="margin:0"><p>It was my first time being adjusted and WOW. The Experience from start to finish was Awesome!</p><p>Professional Friendly and Personable staff and Dr Will was kind and was super informative about my visit and what needed to be done. So happy I am now a Patient!!</p><cite>Laurie W.</cite></figure><figure class="t-card" style="margin:0"><p>Very professional and knowledgeable. We brought my 9 year old due to issues with her ears and they explained everything thoroughly and made her comfortable. I highly recommend Evergrowth Chiropractic.</p><cite>Andrea V.</cite></figure></div></div></section>"""


def esc(text):
    return html.escape(text, quote=False)


def check_copy():
    raw = SRC.read_text()
    for chunk in (INTRO, PLANS_H, PLANS, UNDERSTANDS_H, UNDERSTANDS, "2nd Chiropractic Visit", "Upon returning for your second visit"):
        if chunk not in raw:
            raise SystemExit("copy drift against archive text: " + chunk[:60])
    for name in ("DNoria R.", "Emily E.", "Laurie W.", "Andrea V."):
        if name not in raw:
            raise SystemExit("review name missing from archive: " + name)


def build():
    check_copy()
    home = shell.href("index", DEPTH)
    links = "".join(
        f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in PATIENTS
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Patients<span>/</span>Second Visit</div><h1>2nd Chiropractic Visit</h1><p class="sub-h">Upon returning for your second visit</p></div></section>
<section class="tint"><div class="container"><p>{esc(INTRO)}</p><h2>{esc(PLANS_H)}</h2><p>{esc(PLANS)}</p><h2>{esc(UNDERSTANDS_H)}</h2><p>{esc(UNDERSTANDS)}</p></div></section>
<section><div class="container article-grid"><article class="article"><h2>Ready To Find Out More Information?</h2><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Patients</h3>{links}</div></aside></div></section>
{REVIEWS}'''
    page = shell.render_page(
        "Second Chiropractic Visit - Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        INTRO,
        body,
        DEPTH,
    )
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording in second visit page")
    if 'href="/' in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link in second visit page")
    dest = ROOT / "second-visit" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    print(dest)


if __name__ == "__main__":
    build()
