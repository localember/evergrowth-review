"""Payment Plans page. Copy is the 2026-04-17 archive text.

The archive page has the heading and the four reviews, and no plan
details. The pre-payment sentence lives on the Second Visit page, so it
is not copied here.

Wording changes, and only these:
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- The old footer address and hours are not copied. The shared shell
  supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the
  new hours.
The New Patient Special block on the old page is left off.
Reviews stay word for word. No images. No plan text was added.
"""
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SRC = Path("/tmp/evergrowth-src/old/pages/payment-plans_20260417.txt")

PATIENTS = [
    ("First Visit", "first-visit"),
    ("Second Visit", "second-visit"),
    ("Follow-Up Visits", "follow-up-visit"),
    ("New Patient Paperwork", "new-patient-paperwork"),
    ("Payment Plans", "payment-plans"),
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


def esc(text):
    return html.escape(text, quote=False)


def check_copy():
    raw = SRC.read_text()
    if "Payment Plans - Chiropractor Henderson NV | New Patient Experience" not in raw:
        raise SystemExit("copy drift against archive text: title")
    if "offers several pre-payment plans" in raw.lower():
        raise SystemExit("archive gained plan copy; do not keep the empty-body page")
    for text, name in REVIEWS:
        if text not in raw or name not in raw:
            raise SystemExit("review missing from archive: " + name)
    if "New Patient Special" not in raw:
        raise SystemExit("archive shape changed")


def review_html():
    cards = []
    for text, name in REVIEWS:
        paras = "".join(f"<p>{esc(part)}</p>" for part in text.split("\n"))
        cards.append(f'<figure class="t-card" style="margin:0">{paras}<cite>{esc(name)}</cite></figure>')
    return (
        '<section class="tint"><div class="container"><div class="center">'
        '<span class="eyebrow">Our testimonial</span>'
        "<h2>What patients say about Evergrowth Chiropractic</h2></div>"
        '<div class="t-grid ">' + "".join(cards) + "</div></div></section>"
    )


def build():
    if SRC.exists():
        check_copy()
    home = shell.href("index", DEPTH)
    links = "".join(
        f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in PATIENTS
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Patients<span>/</span>Payment Plans</div><h1>Payment Plans</h1></div></section>
<section><div class="container article-grid"><article class="article">{shell.pay_box()}<h2>Ready To Find Out More Information?</h2><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Patients</h3>{links}</div></aside></div></section>
{review_html()}'''
    page = shell.render_page(
        "Payment Plans | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "What patients say about Evergrowth Chiropractic",
        body,
        DEPTH,
    )
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording in payment plans page")
    if 'href="/' in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link in payment plans page")
    if "pre-payment" in page.lower():
        raise SystemExit("invented plan copy in payment plans page")
    if shell.has_unexpected_social(page):
        raise SystemExit("unexpected social link in payment plans page")
    extra_blank = shell.unexpected_blank_targets(page)
    if extra_blank:
        raise SystemExit("unexpected outside link in payment plans page: " + ", ".join(extra_blank))
    dest = ROOT / "payment-plans" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    print(dest)


if __name__ == "__main__":
    build()
