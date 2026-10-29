"""FAQs page. Copy is the current site text, word for word.

The current page already uses the Las Vegas address in its chrome.
The ten answers do not name a doctor, do not say Henderson, and do
not state hours or the street address.

Wording changes, and only these:
- None in the questions or answers.
The shared shell supplies 9555 S Eastern Ave, Ste 240B, Las Vegas,
NV 89123, the new hours, and (702) 389-5009.
The footer about line is already in the shell, so it is not repeated
in the body. Social links are left off. No images. No reviews.
"""
import hashlib
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SLUG = "faqs"
SRC = Path("/tmp/evergrowth-src/current/faqs.txt")

FAQ = [
    (
        "What is the Gonstead Method?",
        "The Gonstead Method is a specific approach to chiropractic care that emphasizes detailed analysis of the spine and individualized adjustments based on the patient\u2019s needs.",
    ),
    (
        "What makes the Gonstead Method different?",
        "The Gonstead approach focuses on detailed evaluation and specificity rather than using the same approach for every patient. Care is based on the findings of your individual examination.",
    ),
    (
        "What happens during my first appointment?",
        "Your first visit typically begins with a discussion about your concerns, health history, lifestyle, and goals, followed by a detailed chiropractic evaluation.",
    ),
    (
        "Will I receive an adjustment during my first visit?",
        "This depends on your individual situation and the findings of your evaluation. Your chiropractor will explain the recommended next steps based on your needs.",
    ),
    (
        "Does the Gonstead Method use X-rays?",
        "X-rays may be recommended when clinically appropriate to provide additional information about the structure and alignment of the spine.",
    ),
    (
        "How often will I need chiropractic care?",
        "There is no single schedule for everyone. The frequency of care depends on your individual needs, goals, response to care, and your chiropractor\u2019s recommendations.",
    ),
    (
        "Do I need to be in pain to see a chiropractor?",
        "No. Some people seek chiropractic care because of discomfort, while others are interested in supporting healthy spinal function and maintaining an active lifestyle.",
    ),
    (
        "Is chiropractic care personalized?",
        "Yes. At Evergrowth Chiropractic, we take the time to understand each patient\u2019s concerns and develop an approach based on their individual evaluation and needs.",
    ),
    (
        "How do I know if chiropractic care is right for me?",
        "An evaluation is the best way to determine whether chiropractic care may be appropriate for you. Your chiropractor can discuss your concerns, review your history, and explain your options.",
    ),
    (
        "How do I schedule an appointment?",
        "You can schedule an appointment through our online booking system or contact Evergrowth Chiropractic directly. Our team will be happy to help you find a convenient appointment time.",
    ),
]

NOTE = (
    "BUILT from current/faqs.txt. Ten questions, word for word. "
    "No Henderson, name, address, or hours swaps in the answers. "
    "Address, hours, and phone come from the shared shell. "
    "No images. No reviews. Social links left off. "
    "Footer about line stays in the shared shell and is not repeated in the body. "
    "Homepage FAQ still uses the old 9 questions."
)


def esc(text):
    return html.escape(text, quote=False)


def parse_source():
    lines = SRC.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line == "FAQs" and i + 1 < len(lines) and lines[i + 1] == FAQ[0][0]:
            start = i + 1
    if start is None:
        raise SystemExit("could not find the FAQ heading in the current page")
    found = []
    i = start
    while i < len(lines):
        if lines[i].startswith("Evergrowth Chiropractic provides personalized"):
            break
        if i + 1 >= len(lines):
            raise SystemExit("FAQ source ended mid pair")
        found.append((lines[i], lines[i + 1]))
        i += 2
    return found


def check_copy():
    found = parse_source()
    if found != FAQ:
        raise SystemExit("FAQ copy drifted from current/faqs.txt")
    raw = SRC.read_text()
    if "Henderson" in raw:
        raise SystemExit("current FAQ page now says Henderson; log the swap before building")
    if "Icon-facebook" not in raw:
        raise SystemExit("current FAQ page shape changed")


def faq_html():
    items = []
    for question, answer in FAQ:
        items.append(
            "<details><summary><span>"
            + esc(question)
            + '</span><span class="plus" aria-hidden="true"></span></summary><div class="ans"><p>'
            + esc(answer)
            + "</p></div></details>"
        )
    return '<div class="faq">' + "".join(items) + "</div>"


def rewire_nav():
    old = f"site-map.html#{SLUG}"
    new = f"{SLUG}/"
    changed = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = path.read_text()
        if old not in text:
            continue
        path.write_text(text.replace(old, new))
        changed.append(str(path.relative_to(ROOT)))
    print("rewired", len(changed))
    index = (ROOT / "index.html").read_text()
    if f'href="{SLUG}/"' not in index:
        raise SystemExit("home nav was not rewired")
    leftover = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        if f"site-map.html#{SLUG}" in path.read_text():
            leftover.append(str(path.relative_to(ROOT)))
    if leftover:
        raise SystemExit("anchor still in " + ", ".join(leftover))


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
    if old_cell not in row:
        raise SystemExit("status cell missing")
    row = row.replace(old_cell, new_cell, 1)
    note_start = row.rfind("<td>")
    if note_start < 0:
        raise SystemExit("note cell missing")
    row = row[:note_start] + f"<td>{html.escape(NOTE)}</td>"
    path.write_text(html_text[:start] + row + html_text[end:])
    print("site-map marked built")


def stamp(previous):
    build_id = hashlib.sha256((ROOT / "index.html").read_bytes()).hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    if SRC.exists():
        check_copy()
    previous = (ROOT / "build-id.txt").read_text().strip()
    home = shell.href("index", DEPTH)
    body = (
        f'<section class="page-hero"><div class="container"><div class="crumbs">'
        f'<a href="{home}">Home</a><span>/</span>Contact<span>/</span>FAQs</div>'
        f"<h1>FAQs</h1></div></section>"
        f'<section class="tint"><div class="container"><div class="center">'
        f'<span class="eyebrow">faq</span></div>{faq_html()}{shell.pay_box()}'
        f'<div class="book-actions" style="justify-content:center;margin-top:28px">'
        f'{shell.book_btn(DEPTH, "Book Appointment")}</div></div></section>'
    )
    page = shell.render_page(
        "FAQs | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        FAQ[0][1],
        body,
        DEPTH,
    )
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording on FAQs page")
    if 'href="/' in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link on FAQs page")
    if "evergrowthchiro.com" not in page.split("mailto:", 1)[1].split('"', 1)[0]:
        raise SystemExit("email missing")
    extra_blank = shell.unexpected_blank_targets(page)
    if extra_blank:
        raise SystemExit("unexpected outside link on FAQs page: " + ", ".join(extra_blank))
    if "placeholder=" in page or "Dr. [Last Name]" in page or "\u2014" in page:
        raise SystemExit("placeholder or em dash on FAQs page")
    if "date of birth" in page.lower() or "20250814_131251" in page or "20251020_162305" in page:
        raise SystemExit("forbidden field or photo on FAQs page")
    if "<img" in main:
        raise SystemExit("image on FAQs page")
    if shell.has_unexpected_social(page):
        raise SystemExit("unexpected social link on FAQs page")
    for word in ("treat", "treatment", "treating", "treated"):
        if word in main.lower():
            raise SystemExit("written or client text uses " + word)
    for question, answer in FAQ:
        if question not in page or answer not in page:
            raise SystemExit("missing FAQ copy: " + question)
    if page.count("<details>") != 10:
        raise SystemExit("expected ten questions")
    for needed in (
        "<h1>FAQs</h1>",
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
        'href="../faqs/"',
        "online booking system",
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    book = page.split('href="../book-appointment/"', 1)[1].split(">", 1)[0]
    if "target" in book:
        raise SystemExit("Book Appointment opens in a new tab")
    if "Evergrowth Chiropractic provides personalized chiropractic care" not in page.split("</main>", 1)[1]:
        raise SystemExit("footer about line missing")
    if "Evergrowth Chiropractic provides personalized chiropractic care" in main:
        raise SystemExit("footer about line repeated in the body")
    dest = ROOT / SLUG / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    rewire_nav()
    mark_site_map()
    build_id = stamp(previous)
    if len(dest.read_bytes()) <= 10000:
        raise SystemExit("FAQs page is under 10kb")
    print(dest)
    return build_id


if __name__ == "__main__":
    build()
