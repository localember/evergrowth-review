"""First Visit page. Copy is the 2026-01-21 archive text.

Wording changes, and only these:
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- "Henderson, NV chiropractors" becomes "Las Vegas, NV chiropractors".
- "BEGINNING CHIROPRACTIC CARE IN Henderson" becomes
  "BEGINNING CHIROPRACTIC CARE IN Las Vegas".
The new address and hours come from the shared shell, not from the old footer.
Reviews stay word for word. No images. The five numbered cards reuse the
Home steps layout.
"""
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1

INTRO_BEFORE = (
    "You can expect to spend approximately 45 min. to 1 hour during your first visit. "
    "Prior to your visit, Las Vegas, NV chiropractors ask that you fill out our “"
)
INTRO_LINK = "initial visit forms"
INTRO_AFTER = (
    "” online with details regarding your health history. This saves valuable time "
    "when you have these forms filled out in advance."
)

STEPS = [
    (
        "COURSE OF CARE",
        [
            "We will discuss all your health concerns with you to help determine the best course of care. Next, our Gonstead Chiropractor will perform a skin temperature test using an instrument called a “Temp-o-scope/Nervo-scope”. This instrument records temperature readings on both sides of the spine. They're also looking for asymmetries that show up as specific patterns along the spine demonstrating nerve irritation. The scope pinpoints the particular area/areas that likely indicate where the nerve is being irritated. The instrument is non-invasive and glides gently down the length of your back like two fingers sliding down each side of your spine.",
        ],
    ),
    (
        "BEGINNING CHIROPRACTIC CARE IN Las Vegas",
        [
            "Next, your chiropractor will feel for the presence of swelling, tenderness, and any abnormal texture or tightness in the muscles and other tissues of your back (static palpation). They're also feeling for motion in the spine while moving and bending you (motion palpation) to determine how easily/difficult each segment in your spine is moving in different directions. Your doctor is also visually looking for subtle changes in your posture or gait that may indicate a problem as well.",
        ],
    ),
    (
        "NEXT STEPS",
        [
            "We’ll take an x-ray (if appropriate). The X-rays help Gonstead Chiropractors complete a thorough analysis of your spine.",
        ],
    ),
    (
        "THE X-RAYS IN THE “GONSTEAD SYSTEM”",
        [
            "Aside from pathology, x-rays are used to determine the best way to adjust a segment SPECIFICALLY e.g., which side of the joint to contact and thrust on and which side to stabilize, the best line-of-drive and thrust mechanism to make a specific correction. The goal is to restore FUNCTION, not necessarily straighten misalignments that may be normal for that individual.",
        ],
    ),
    (
        "FIRST ADJUSTMENT",
        [
            "After taking the necessary time to analyze your X-rays, Our team is ready to deliver your first specific spinal adjustment. The Gonstead system was designed to be as specific and precise as possible! Great care is taken to adjust only that which is needed with the most accuracy and finesse possible.",
            "Lastly, we will schedule your second visit to discuss our findings regarding your condition and determine a course of care.",
        ],
    ),
]

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


def build():
    home = shell.href("index", DEPTH)
    pdf = shell.paperwork_href(DEPTH)
    intro = (
        f"<p>{esc(INTRO_BEFORE)}<a href=\"{pdf}\" target=\"_blank\" rel=\"noopener\">{esc(INTRO_LINK)}</a>{esc(INTRO_AFTER)}</p>"
    )
    cards = []
    for i, (heading, paras) in enumerate(STEPS, start=1):
        body = "".join(f"<p>{esc(text)}</p>" for text in paras)
        cards.append(f'<div class="step"><span class="n">{i}</span><h3>{esc(heading)}</h3>{body}</div>')
    steps = '<div class="steps">' + "".join(cards) + "</div>"
    links = "".join(
        f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in PATIENTS
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Patients<span>/</span>First Visit</div><h1>1st Chiropractic Visit</h1><p class="sub-h">On your first visit to our office</p></div></section>
<section class="tint"><div class="container">{intro}{steps}{shell.pay_box()}</div></section>
<section><div class="container article-grid"><article class="article"><h2>Ready To Find Out More Information?</h2><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Patients</h3>{links}</div></aside></div></section>
{REVIEWS}'''
    page = shell.render_page(
        "First Chiropractic Visit - Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "You can expect to spend approximately 45 min. to 1 hour during your first visit.",
        body,
        DEPTH,
    )
    dest = ROOT / "first-visit" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    print(dest)


if __name__ == "__main__":
    build()
