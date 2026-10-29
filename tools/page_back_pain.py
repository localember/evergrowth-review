"""Back Pain page. Copy is the 2026-05-11 archive text.

Allowed swaps only, logged in SWAPS:
- Henderson to Las Vegas (four places in the article, plus the title)
- title suffix "New Patient Experience" to "Evergrowth Chiropractic",
  matching the approved mockup and the other inner pages
- old address and old hours are not on this page; the shared shell
  supplies the Las Vegas address and the new hours

Reviews stay word for word, including "Dr Will" and "Dr. Will".
No FAQ: the archive page and the approved mockup have none.
Hero image is stock Catalog/Conditions/back-pain.webp, not a client photo.
"""
import hashlib
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import condition
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
CATALOG = Path(
    "/Users/johnowens/localember/tools/bd-generator/assets/stock/Catalog/Conditions/back-pain.webp"
)
IMAGE_NAME = "stock-condition-back-pain.webp"

SWAPS = [
    "Subhead: 'Chiropractic Care for Back Pain in Henderson, NV' to 'Chiropractic Care for Back Pain in Las Vegas, NV'",
    "Opening: 'chiropractic care in Henderson' to 'chiropractic care in Las Vegas'",
    "Disc section: 'In Henderson, NV,' to 'In Las Vegas, NV,'",
    "Closing: 'Evergrowth Chiropractic in Henderson, NV' to 'Evergrowth Chiropractic in Las Vegas, NV'",
    "Title: 'Chiropractor Henderson NV | New Patient Experience' to 'Chiropractor Las Vegas NV | Evergrowth Chiropractic'",
    "Chrome: old address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 replaced by 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123",
    "Chrome: old weekday 10am-6pm hours replaced by Mon, Wed, Thu 10am to 1pm and 3pm to 6pm; Tue 3pm to 6pm; Fri appointments only; Sat and Sun closed",
    "No name swap. Reviews keep Dr Will and Dr. Will. New Patient Special omitted.",
]

BLOCKS = [
    (
        "p",
        "Chronic back pain can be a relentless burden, affecting your daily life. Whether your pain is a minor inconvenience or a debilitating condition, finding relief is a top priority. This article is here to shed light on the causes of lower back pain and how chiropractic care in Las Vegas can be your pathway to lasting back health, ensuring you can continue to enjoy life's simple pleasures like leisurely walks in the park.",
    ),
    ("h2", "Understanding Back Pain"),
    (
        "p",
        "The back is a complex structure comprising tendons, ligaments, discs, muscles, and bones. Pinpointing the exact source of pain can be a challenging task without a thorough understanding of these components. Here, we'll delve into some common back issues and their distinctive characteristics, along with how chiropractic treatment can offer solutions. Remember, while this provides a general guideline, it's essential to seek professional advice for a precise diagnosis.",
    ),
    ("h2", "Disc Bulges and Herniations"),
    (
        "p",
        "Disc bulges and herniations occur when the outer edges of the discs, nestled between your vertebrae, become damaged, causing the gel-like center to protrude or rupture. Surprisingly, this condition doesn't always manifest with severe pain; some individuals may not feel it at all. The intensity of pain, for those who do experience it, hinges on the type and location of the herniation. If the affected disc irritates nearby nerves, you may suffer from severe shooting or stabbing pain along with leg weakness.",
    ),
    (
        "p",
        "Prompt and accurate identification of this issue is crucial to prevent further harm. In Las Vegas, NV, chiropractors are adept at assessing your condition comprehensively and determining the appropriate treatment to alleviate pain while minimizing herniation progression.",
    ),
    ("h2", "Subluxations"),
    (
        "p",
        "Subluxation is a term in the medical world that refers to misalignments in the vertebral column. These misalignments can result from various factors, including physical stress, trauma, or toxins. Subluxations are often painful and can disrupt your normal range of motion. Surprisingly, they are one of the most frequently overlooked contributors to back pain. Fortunately, chiropractors are well-trained to identify and address subluxations using non-invasive adjustment techniques.",
    ),
    ("h2", "Muscular Sprains and Tendon or Ligament Strains"),
    (
        "p",
        "Muscular sprains and tendon or ligament strains typically occur when you engage in activities your body isn't accustomed to or experience accidents. Actions like lifting while twisting or stretching beyond your limits can lead to these painful conditions, often accompanied by swelling and bruising in the affected area. Such incidents can also alter the spine's alignment. Fortunately, back strains and sprains tend to respond well to chiropractic care.",
    ),
    ("h2", "Stress and Its Role in Back Pain"),
    (
        "p",
        "Chronic stress can wreak havoc on your body, potentially leading to hypertension and persistent back pain. The physical manifestation of stress often involves tension and muscle spasms, triggered by the release of stress hormones. Tension tends to accumulate in specific areas known as trigger points, causing extreme pain that requires professional attention. Chiropractors possess the expertise and tools to alleviate stress from these trigger points and address underlying nervous system imbalances that might be perpetuating your cycle of stress and pain.",
    ),
]

CLOSING = (
    "If you have questions about how our team at Evergrowth Chiropractic in Las Vegas, NV, "
    "can assist you, don't hesitate to schedule a consultation today. Your journey to a "
    "pain-free back and a more fulfilling life begins here."
)


def place_image():
    dest = ROOT / "assets" / "img" / IMAGE_NAME
    if CATALOG.is_file():
        shutil.copyfile(CATALOG, dest)
        return dest
    if dest.is_file():
        return dest
    raise SystemExit(f"missing stock image {CATALOG}")


def check(page):
    problems = []
    if "Henderson" in page:
        problems.append("Henderson still present")
    if "evergrowthchiro.com/book" in page.lower():
        problems.append("booking link points at the client site")
    if 'href="/' in page or "src=\"/" in page:
        problems.append("root-absolute path")
    if "localhost" in page or "127.0.0.1" in page:
        problems.append("localhost leak")
    if "noindex" not in page:
        problems.append("missing noindex")
    if 'target="' in page:
        problems.append("target attribute on a page with no outside link")
    if "New Patient Special" in page or "$47" in page:
        problems.append("special offer leaked")
    if "Dr. [Last Name]" in page:
        problems.append("placeholder doctor name")
    book = page.count('href="../book-appointment/"')
    if book < 4:
        problems.append(f"expected book links in header, article, sidebar, footer; found {book}")
    if "stock-condition-back-pain.webp" not in page:
        problems.append("missing stock hero")
    for sentence in (
        "chiropractic care in Las Vegas can be your pathway",
        "In Las Vegas, NV, chiropractors are adept",
        "Evergrowth Chiropractic in Las Vegas, NV",
        "Chiropractic Care for Back Pain in Las Vegas, NV",
        "DNoria R.",
        "Emily E.",
        "Laurie W.",
        "Andrea V.",
        "So happy I am now a Patient!!",
    ):
        if sentence not in page:
            problems.append(f"missing copy: {sentence}")
    if problems:
        raise SystemExit("back-pain check failed: " + "; ".join(problems))


def build():
    place_image()
    pre = shell.prefix(DEPTH)
    page = condition.render_condition(
        depth=DEPTH,
        title="Back Pain Relief | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        description="Chiropractic care for back pain in Las Vegas, NV at Evergrowth Chiropractic.",
        crumbs=[
            ("Home", "index"),
            ("What We Do", None),
            ("Spine Related", None),
            ("Back Pain", None),
        ],
        h1="Back Pain Relief",
        sub="Chiropractic Care for Back Pain in Las Vegas, NV",
        image=f"{pre}assets/img/{IMAGE_NAME}",
        image_alt="Person holding their lower back",
        image_w=2400,
        image_h=1600,
        blocks=BLOCKS,
        closing=CLOSING,
        group_title="Spine Related",
        group_links=condition.nav_group("Spine Related"),
    )
    check(page)
    dest = ROOT / "back-pain" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()[:12]
    print(dest)
    print("page-sha", digest)
    for line in SWAPS:
        print("swap:", line)


if __name__ == "__main__":
    build()
