"""Founder of Gonstead page. Copy is the 2026-06-06 archive text.

The only wording change is Henderson, NV to Las Vegas, NV in the closing line
and in the title. Reviews stay word for word.
"""
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1

PARAS = [
    "Dr. Clarence Gonstead, a visionary in the field of chiropractic, redefined the landscape of his profession and erected a chiropractic stronghold in the unassuming town of Wisconsin. He stands as one of the most influential figures in the history of Chiropractic, and the Gonstead System serves as an enduring testament to the pinnacle of chiropractic care.",
    "Born on July 23, 1898, in Willow Lake, South Dakota, Clarence Gonstead's early years saw his family settling on a dairy farm in Primrose, Wisconsin. At the age of 19, he was struck by a debilitating bout of rheumatoid arthritis that rendered him bedridden for weeks. It was during this trying period that his aunt sought the assistance of her chiropractor, Dr. J.B. Olson. After a series of chiropractic adjustments, Gonstead's recovery was nothing short of miraculous, allowing him to walk again.",
    "This transformative encounter propelled Clarence Gonstead on a new path. He enrolled in Palmer College of Chiropractic and completed his studies in 1923. Concurrently, he pursued a career as an automotive engineer, an experience that would profoundly influence his chiropractic journey. His mechanical background instilled in him a unique perspective, prompting him to question prevailing theories about subluxation mechanisms.",
    'At the time, B.J. Palmer\'s theory, which posited that vertebral displacement caused neural foramina encroachment, dominated the chiropractic profession. Dr. Gonstead challenged this paradigm through the application of biomechanical principles and clinical observation in his practice. He introduced the groundbreaking Level Disc Theory, contending that subluxations originated at the disc level, where inflammatory responses from damaged tissue created "nerve pressure," resulting in the neurological complications associated with subluxations.',
    "The assertion that subluxations stemmed from disc involvement marked a revolutionary departure from conventional chiropractic thought. Dr. Gonstead developed an entirely new approach to correcting vertebral subluxations, centered around this principle. His objective was to realign vertebrae on the disc to restore an optimal relationship. To maximize the efficiency of detecting and correcting subluxations, he pioneered several inventions.",
    'The Nervoscope, a device designed by Dr. Gonstead, enabled practitioners to objectively identify the neurological components of a subluxation by measuring bilateral temperature differences along the spine. This innovation effectively allowed chiropractors to "troubleshoot" the nerves at each chord level. Additionally, Dr. Gonstead introduced the cervical chair and knee chest table, enabling chiropractors to leverage gravity and spinal mechanics to gain the necessary "lift" for precise adjustments.',
    "Through unwavering determination and relentless refinement of his craft, Dr. Gonstead achieved international acclaim. He erected a clinic in Mt. Horeb, Wisconsin, which reached its zenith with amenities like an airstrip and a patient hotel, catering to individuals who traveled from all corners of the world to receive his care. It's a little-known fact that during the polio epidemic that swept the United States in the first half of the 20th century, not a single patient under Dr. Gonstead's care succumbed to the disease.",
    "Dr. Gonstead was a revolutionary thinker who reshaped our understanding of subluxation mechanisms. He recognized that subluxation was a complex entity, leading him to expand the chiropractic system to encompass a multifaceted approach to diagnosis. His method involved analyzing a patient's problem through multiple diagnostic criteria and correlating findings to achieve the most accurate diagnosis possible.",
]

LEGACY = "Through his enduring legacy, the Gonstead System continues to stand as the gold standard of excellence in the chiropractic profession, offering hope and healing to all who seek chiropractic care."

REVIEWS = """<section class="tint"><div class="container"><div class="center"><span class="eyebrow">Our testimonial</span><h2>What patients say about Evergrowth Chiropractic</h2></div><div class="t-grid "><figure class="t-card" style="margin:0"><p>Dr Will is a GREAT chiropractor. I used to have lower back pain that was frequent; now I no longer have that pain. With regular adjustments my back stays aligned and free from tension and stiffness. I highly recommend Evergrowth Chiropractic services for individuals and families!</p><cite>DNoria R.</cite></figure><figure class="t-card" style="margin:0"><p>I enjoy my visits to Evergrowth Chiropractic so much! Dr. Will is amazing! I feel so refreshed after my treatments. Wendy is so sweet and friendly as well! I highly recommend their practice; I'm so glad I found them! Relaxing, no stress atmosphere.</p><cite>Emily E.</cite></figure><figure class="t-card" style="margin:0"><p>It was my first time being adjusted and WOW. The Experience from start to finish was Awesome!</p><p>Professional Friendly and Personable staff and Dr Will was kind and was super informative about my visit and what needed to be done. So happy I am now a Patient!!</p><cite>Laurie W.</cite></figure><figure class="t-card" style="margin:0"><p>Very professional and knowledgeable. We brought my 9 year old due to issues with her ears and they explained everything thoroughly and made her comfortable. I highly recommend Evergrowth Chiropractic.</p><cite>Andrea V.</cite></figure></div></div></section>"""


def esc(text):
    return html.escape(text, quote=False)


def build():
    pre = shell.prefix(DEPTH)
    paras = "".join(f"<p>{esc(text)}</p>" for text in PARAS)
    home = shell.href("index", DEPTH)
    close = (
        "Discover the Gonstead System's transformative power for yourself by visiting your "
        f'<a href="{home}">Las Vegas, NV Chiropractor</a> today.'
    )
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Gonstead Technique<span>/</span>Dr. Gonstead</div><h1>Founder Of The Gonstead Technique</h1><p class="sub-h">Unveiling the Legacy of Dr. Clarence Gonstead, D.C.</p></div></section>
<section style="padding-top:40px"><div class="container article-grid"><article class="article"><div class="a-img"><img src="{pre}assets/img/founder-of-gonstead.jpg" alt="Clarence Gonstead" width="2400" height="1600"></div>{paras}<p>In his own words, Dr. Gonstead asserted,</p><h2>Remember Chiropractic always works.</h2><p>{esc(LEGACY)}</p>
<div class="inline-cta"><p>{close}</p><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Gonstead Technique</h3><a href="{shell.href("founder-of-gonstead", DEPTH)}">Dr. Gonstead</a><a href="{shell.href("gonstead-system", DEPTH)}">The 5 Components</a></div></aside></div></section>
{REVIEWS}'''
    page = shell.render_page(
        "Founder Of The Gonstead Technique - Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "Unveiling the Legacy of Dr. Clarence Gonstead, D.C.",
        body,
        DEPTH,
    )
    dest = ROOT / "founder-of-gonstead" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    print(dest)


if __name__ == "__main__":
    build()
