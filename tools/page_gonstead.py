"""Gonstead System page (the 5 components). Copy is the 2026-06-06 archive text.

The only wording change is Henderson, NV to Las Vegas, NV in the opening
paragraph and in the title. Reviews stay word for word.
"""
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1

INTRO = [
    "Why settle for anything less than comprehensive information when making crucial decisions about someone's health? Every patient deserves the highest level of chiropractic care in Las Vegas, NV, achieved through a thorough analysis that correlates various aspects of their clinical picture. This approach ensures specificity and fosters patient confidence in the doctor's ability to provide effective care.",
    "The Gonstead Technique relies on five essential components: Visualization, Instrumentation, Palpation, X-Ray, and patient symptoms. By integrating these elements, we can pinpoint the precise location that requires adjustment. When all these factors align, we can provide the patient with a specific and effective adjustment. Specificity is the key, as Dr. Gonstead emphasized that three adjustments on the wrong vertebral segment could lead to a Subluxation, highlighting the importance of precision.",
]

COMPONENTS = [
    (
        "x-rays",
        "X-Rays",
        "xrays",
        "X-RAYS",
        [
            'In the Gonstead System, Full Spine X-Rays are crucial, capturing both A-P and Lateral views. These films measure 14" x 36" and include the area from ischia to occiput. Full Spine X-Rays use less radiation compared to sectional films and offer numerous advantages.',
            "They provide an accurate count of vertebrae, offer a comprehensive view of spinal contour for posture analysis with axial weight bearing, and reveal issues beyond the chief complaint. These factors make Full Spine X-Rays indispensable in Gonstead Chiropractic, allowing us to fully analyze and correct a patient's condition.",
        ],
    ),
    (
        "palpation",
        "Palpation",
        "palpation",
        "PALPATION",
        [
            "Gonstead Chiropractic employs both Static and Motion Palpation techniques to precisely identify areas of concern. Static Palpation is a hands-on examination that detects changes in contour, tone, texture, and temperature on the patient. Motion Palpation, on the other hand, is used to identify subluxations and their listings.",
        ],
    ),
    (
        "instrumentation",
        "Instrumentation",
        "instrumentation",
        "INSTRUMENTATION",
        [
            "The use of a dual probe instrument, such as the Nervoscope or Delta-T, plays a pivotal role in the Gonstead Technique. It allows for a bilateral temperature comparison of the spine, helping to locate areas of inflammation. The readings obtained through instrumentation indicate the presence of subluxations, their correction progress, and when correction has been achieved.",
        ],
    ),
    (
        "visualization",
        "Visualization",
        "visualization",
        "VISUALIZATION",
        [
            "Visualization begins the moment a patient enters the clinic in the Gonstead System. We carefully observe the patient, taking note of differences in ear, shoulder, and hip heights, posture, and gait. This visual assessment complements the information gathered through X-Rays and Palpation, aiding in the diagnostic process.",
        ],
    ),
    (
        "case-management",
        "Case Management (Symptomatology)",
        "case-management",
        "CASE MANAGEMENT",
        [
            'Although not applied in a rigid "cook-book" manner, understanding a patient\'s health issues helps us determine the specific area that requires adjustment. Symptoms can also assist in differentiating between the two parts of the Autonomic Nervous System (Sympathetic and Parasympathetic) and guide us in delivering precise adjustments.',
        ],
    ),
]

CLOSING = [
    "In the Gonstead System, we synthesize information from these various analysis modes and correlate our findings to identify the likely cause of the patient's problem. Once Subluxations are pinpointed, we apply the appropriate Gonstead technique to effectively correct the problem areas.",
    'The Gonstead system places a strong emphasis on the dynamics of intervertebral discs as the root cause of subluxations and resulting neurological dysfunction. Therefore, Gonstead doctors are often referred to as "disc doctors," focusing on addressing these underlying issues for the benefit of their patients\' overall health and well-being.',
]

DISC = [
    "Dr. Gonstead proposed that vertebral misalignment disrupts the Parallel Disc alignment, leading to compression at the nucleus pulposus. This compression forces the nucleus to exert pressure on the surrounding annular fibers, causing damage to them.",
    "Such damage triggers an inflammatory response, which causes the disc to swell. This swelling then exerts pressure on the nerves located in the respective intervertebral foramen, leading to neurological dysfunction.",
    "According to the Gonstead methodology, understanding that subluxations originate from the disc is crucial. Recognizing the stages of disc degeneration is essential for determining the appropriate adjustment direction and force needed for effective correction.",
]

LEVEL = [
    "Within the spinal column, the intervertebral discs serve a dual purpose: they act as a protective buffer to enhance flexibility and as a structural link that maintains proper motion between the vertebral bodies.",
    'The Nucleus Pulposus, a dense central core, retains fluids and nutrients and acts as a pivot during vertebral movement, much like a "ball bearing." The Annulus Fibrosis, composed of fibrocartilage and collagen fibers, surrounds this core. It is similar to the concentric rings seen in a tree trunk cross-section, and it is anchored to the cartilaginous end plates of the adjacent vertebral bodies.',
    'Dr. Gonstead\'s Level Disc Theory asserts that "anatomically and physiologically normal discs promote optimum vertebral alignment." This is evidenced when the vertical height of a vertebral couple is uniform around 360 degrees, with the vertebral bodies properly aligned. This alignment, known as "Parallel Discs," ensures even weight distribution, adequate nutrient flow, and optimal joint function and movement within the spine.',
]

REVIEWS = """<section class="tint"><div class="container"><div class="center"><span class="eyebrow">Our testimonial</span><h2>What patients say about Evergrowth Chiropractic</h2></div><div class="t-grid "><figure class="t-card" style="margin:0"><p>Dr Will is a GREAT chiropractor. I used to have lower back pain that was frequent; now I no longer have that pain. With regular adjustments my back stays aligned and free from tension and stiffness. I highly recommend Evergrowth Chiropractic services for individuals and families!</p><cite>DNoria R.</cite></figure><figure class="t-card" style="margin:0"><p>I enjoy my visits to Evergrowth Chiropractic so much! Dr. Will is amazing! I feel so refreshed after my treatments. Wendy is so sweet and friendly as well! I highly recommend their practice; I'm so glad I found them! Relaxing, no stress atmosphere.</p><cite>Emily E.</cite></figure><figure class="t-card" style="margin:0"><p>It was my first time being adjusted and WOW. The Experience from start to finish was Awesome!</p><p>Professional Friendly and Personable staff and Dr Will was kind and was super informative about my visit and what needed to be done. So happy I am now a Patient!!</p><cite>Laurie W.</cite></figure><figure class="t-card" style="margin:0"><p>Very professional and knowledgeable. We brought my 9 year old due to issues with her ears and they explained everything thoroughly and made her comfortable. I highly recommend Evergrowth Chiropractic.</p><cite>Andrea V.</cite></figure></div></div></section>"""


def esc(text):
    return html.escape(text, quote=False)


def paras(items):
    return "".join(f"<p>{esc(text)}</p>" for text in items)


def build():
    pre = shell.prefix(DEPTH)
    home = shell.href("index", DEPTH)
    circles = "".join(
        f'<figure><a href="#{anchor}"><img src="{pre}assets/img/stock-gonstead-{file}.webp" alt="" width="250" height="250"><figcaption>{label}</figcaption></a></figure>'
        for anchor, _heading, file, label, _body in COMPONENTS
    )
    sections = "".join(
        f'<h2 id="{anchor}">{esc(heading)}</h2>{paras(body)}'
        for anchor, heading, _file, _label, body in COMPONENTS
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Gonstead Technique<span>/</span>The 5 Components</div><h1>5 Components of The Gonstead Technique</h1></div></section>
<section style="padding-top:40px"><div class="container article-grid"><article class="article"><div class="a-img"><img src="{pre}assets/img/treatment-room.webp" alt="Adjusting room with a Gonstead style chair and padded benches" width="1200" height="1025"></div>{paras(INTRO)}
<div class="five compact">{circles}</div>
{sections}{paras(CLOSING)}
<h2>Dr. Gonstead's Theory on Disc Subluxation</h2>{paras(DISC)}
<h2>Dr. Gonstead's Level Disc Theory</h2>{paras(LEVEL)}
<div class="inline-cta"><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Gonstead Technique</h3><a href="{shell.href("founder-of-gonstead", DEPTH)}">Dr. Gonstead</a><a href="{shell.href("gonstead-system", DEPTH)}">The 5 Components</a></div></aside></div></section>
{REVIEWS}'''
    page = shell.render_page(
        "5 Components of The Gonstead Technique | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "Why settle for anything less than comprehensive information when making crucial decisions about someone's health?",
        body,
        DEPTH,
    )
    dest = ROOT / "gonstead-system" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    print(dest)


if __name__ == "__main__":
    build()
