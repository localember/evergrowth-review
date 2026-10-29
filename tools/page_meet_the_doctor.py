"""Meet the Doctor page.

Copy comes from the 2026-06-06 /us/ archive and the current Meet the Doctor
page. The archive holds the bio and the journey. The current page holds the
newer doctor text.

Allowed wording changes, and only these:
- "Dr. Will So" becomes "Dr. Willie So".
- "Will So, D.C." becomes "Dr. Willie So".
- "Dr Willie So" becomes "Dr. Willie So".
- "Dr. [Last Name]" becomes "Dr. Willie So" and the placeholder is not shown.
- "8+ Years Of Experience" becomes "10+ Years Of Experience".
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- The old "Request An Appointment" and the current "Book an Appointment"
  use the shared Book Appointment button (internal, same tab).
The journey, including its first-person wording, is not edited.
Reviews keep "Dr Will" and "Dr. Will".
The New Patient Special block is left off.
The old Henderson address and the old hours are not copied.
"""
import hashlib
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SLUG = "meet-the-doctor"
OLD = Path("/tmp/evergrowth-src/old/pages/us_20260606.txt")
CURRENT = Path("/tmp/egc-src/meet-the-doctor.txt")

WHO = [
    ("Meet the Doctor", "meet-the-doctor"),
    ("Testimonials", "testimonials"),
    ("Office Tour", "office-tour"),
    ("Blog", "blog"),
]

NOTE = (
    "BUILT. Real headshot from the current site (dr-will-so-portrait.webp, "
    "the current Meet the Doctor photo). Not used: 20250814_131251.jpg, unconfirmed. "
    "Still missing: more doctor photos and a larger headshot. "
    "Name swaps: Will So, D.C. to Dr. Willie So; Dr. Will So to Dr. Willie So "
    "(5 in the two bio paragraphs); Dr Willie So to Dr. Willie So in the current heading; "
    "the placeholder last name on the current page became Dr. Willie So. Reviews keep Dr Will and Dr. Will. "
    "Bio line 8+ Years Of Experience became 10+ Years Of Experience "
    "(Brevin named this; ask the client in the preview email). No other bio edits. "
    "Title suffix Chiropractor Henderson NV | New Patient Experience became "
    "Chiropractor Las Vegas NV | Evergrowth Chiropractic. "
    "Old address, old hours, and the New Patient Special are not copied. "
    "Book buttons say Book Appointment and stay on this preview."
)


def esc(text):
    return html.escape(text, quote=False)


def need(lines, exact):
    for index, line in enumerate(lines):
        if line == exact:
            return index
    raise SystemExit("missing line: " + exact)


def paras(text):
    return "".join(f"<p>{esc(part)}</p>" for part in text.split("\n") if part.strip())


def load():
    old = OLD.read_text().splitlines()
    current = CURRENT.read_text().splitlines()
    start = None
    for index, line in enumerate(old):
        if line == "Gonstead Chiropractor" and old[index + 1] == "Will So, D.C.":
            start = index
            break
    if start is None:
        raise SystemExit("archive doctor block missing")
    bio = [old[start + 2], old[start + 3]]
    if old[start + 4] != "Dr. So's Journey to Chiropractic":
        raise SystemExit("journey heading moved")
    if old[start + 12] != "Our strength" or old[start + 13] != "Why choose us?":
        raise SystemExit("strength block moved")
    journey = old[start + 5:start + 12]
    if len(journey) != 7 or any(not line.strip() for line in journey):
        raise SystemExit("journey paragraph count changed")
    years = old[start + 14]
    if years != "8+ Years Of Experience":
        raise SystemExit("years line changed in the archive")
    if old[start + 15] != "Certified Gonstead" or old[start + 16] != "Affordable pricing":
        raise SystemExit("strength items changed")
    review_at = need(old, "Our testimonial")
    if old[review_at + 1] != "What patients say about Evergrowth Chiropractic":
        raise SystemExit("review heading changed")
    reviews = [
        (old[review_at + 2], old[review_at + 3]),
        (old[review_at + 4], old[review_at + 5]),
        (old[review_at + 6] + "\n" + old[review_at + 7], old[review_at + 8]),
        (old[review_at + 9], old[review_at + 10]),
    ]
    if old[review_at + 11] != "New Patient Special Offer":
        raise SystemExit("archive shape changed around the special")
    if "Who we are - Chiropractor Henderson NV | New Patient Experience" not in OLD.read_text():
        raise SystemExit("old title missing")
    if "1263 E Silverado Ranch Blvd #105A" not in OLD.read_text():
        raise SystemExit("old address missing from archive; swap log would be wrong")
    slogan = need(current, "Chiropractor Near You Dedicated To Lasting Relief")
    expected = [
        "Chiropractor Near You Dedicated To Lasting Relief",
        "Meet Dr Willie So Your Local Chiropractor",
        "Feel And Function Better With Targeted Chiropractic Care",
    ]
    if current[slogan:slogan + 3] != expected:
        raise SystemExit("current heading block changed")
    current_paras = current[slogan + 3:slogan + 6]
    if len(current_paras) != 3 or "Dr. [Last Name]" not in current_paras[0]:
        raise SystemExit("current doctor paragraphs changed")
    care = need(current, "Evergrowth Chiropractic Care Focused On You")
    if current[care + 1] != "Helping You Move, Function & Live Better":
        raise SystemExit("care heading changed")
    cards = [
        (current[care + 2], current[care + 3]),
        (current[care + 4], current[care + 5]),
        (current[care + 6], current[care + 7]),
    ]
    gonstead = need(current, "How The Gonstead Chiropractic Method Helps You")
    if current[gonstead + 1] != "Precise Chiropractic Care Tailored To Your Body":
        raise SystemExit("gonstead heading changed")
    gonstead_para = current[gonstead + 2]
    if current[gonstead + 3] != "Explore the Gonstead Method":
        raise SystemExit("gonstead link label changed")
    training = need(current, "Chiropractic Training And Experience You Can Trust")
    if current[training + 1] != "Ongoing Chiropractic Training That Benefits Your Health":
        raise SystemExit("training heading changed")
    training_para = current[training + 2]
    labels = current[training + 3:training + 6]
    if labels != [
        "Gonstead Chiropractic",
        "Continued Professional Education",
        "Patient-Centered Care",
    ]:
        raise SystemExit("training labels changed")
    ready = need(current, "Ready To Start Chiropractic Care Near You Today")
    ready_para = current[ready + 1]
    if current[ready + 2] != "Book an Appointment":
        raise SystemExit("current book label changed")
    if "\u2014" not in journey[0] or "\u2014" not in training_para:
        raise SystemExit("client em dashes missing; the copy was trimmed")
    if "Dr Will" not in reviews[0][0] or "Dr. Will" not in reviews[1][0] or "Dr Will" not in reviews[2][0]:
        raise SystemExit("review lost Dr Will")
    if "Dr Will" in reviews[3][0] or "Dr. Will" in reviews[3][0]:
        raise SystemExit("Andrea review changed")
    return {
        "bio": bio,
        "journey": journey,
        "years": years,
        "certified": old[start + 15],
        "pricing": old[start + 16],
        "reviews": reviews,
        "slogan": current[slogan],
        "meet": current[slogan + 1],
        "feel": current[slogan + 2],
        "current_paras": current_paras,
        "care_h": current[care],
        "care_sub": current[care + 1],
        "cards": cards,
        "gonstead_h": current[gonstead],
        "gonstead_sub": current[gonstead + 1],
        "gonstead_para": gonstead_para,
        "explore": current[gonstead + 3],
        "training_h": current[training],
        "training_sub": current[training + 1],
        "training_para": training_para,
        "labels": labels,
        "ready_h": current[ready],
        "ready_para": ready_para,
    }


def swap_name(text):
    return (
        text.replace("Dr. Will So", "Dr. Willie So")
        .replace("Will So, D.C.", "Dr. Willie So")
        .replace("Dr Willie So", "Dr. Willie So")
        .replace("Dr. [Last Name]", "Dr. Willie So")
    )


def review_html(reviews):
    cards = []
    for text, name in reviews:
        cards.append(
            f'<figure class="t-card" style="margin:0">{paras(text)}<cite>{esc(name)}</cite></figure>'
        )
    return (
        '<section class="tint"><div class="container"><div class="center">'
        '<span class="eyebrow">Our testimonial</span>'
        "<h2>What patients say about Evergrowth Chiropractic</h2></div>"
        '<div class="t-grid ">' + "".join(cards) + "</div></div></section>"
    )


def rewire_nav():
    old = f'site-map.html#{SLUG}"'
    new = f'{SLUG}/"'
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
    start = html_text.find('<tr id="meet-the-doctor">')
    if start < 0:
        raise SystemExit("site-map row missing")
    end = html_text.find("</tr>", start)
    row = html_text[start:end]
    old_cell = "<td>planned (not built)</td>"
    new_cell = '<td><a href="meet-the-doctor/">meet-the-doctor/</a> (built)</td>'
    if old_cell not in row:
        raise SystemExit("status cell missing")
    row = row.replace(old_cell, new_cell, 1)
    old_tag = '<span class="tag partial">content partial</span>'
    new_tag = '<span class="tag ready">content ready</span>'
    if old_tag not in row:
        raise SystemExit("status tag missing")
    row = row.replace(old_tag, new_tag, 1)
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
    data = load()
    if data["bio"][0].count("Dr. Will So") != 3 or data["bio"][1].count("Dr. Will So") != 2:
        raise SystemExit("bio name count changed")
    bio = [swap_name(part) for part in data["bio"]]
    if any("Dr. Will So" in part or "Will So" in part for part in bio):
        raise SystemExit("bio name swap missed")
    years = data["years"].replace("8+ Years Of Experience", "10+ Years Of Experience")
    if years != "10+ Years Of Experience":
        raise SystemExit("years swap missed")
    meet = swap_name(data["meet"])
    current_paras = [swap_name(part) for part in data["current_paras"]]
    if any("Dr. [Last Name]" in part or "Dr Willie So" in part for part in current_paras):
        raise SystemExit("current name swap missed")
    if meet != "Meet Dr. Willie So Your Local Chiropractor":
        raise SystemExit("current heading swap missed")
    for part in data["journey"]:
        if part != swap_name(part) or "8+ Years" in part:
            raise SystemExit("journey was not left as written")
    previous = (ROOT / "build-id.txt").read_text().strip()
    home = shell.href("index", DEPTH)
    pre = shell.prefix(DEPTH)
    links = "".join(
        f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in WHO
    )
    strength = (
        '<div class="strip">'
        f"<div><b>{esc(years)}</b></div>"
        f"<div><b>{esc(data['certified'])}</b></div>"
        f"<div><b>{esc(data['pricing'])}</b></div>"
        "</div>"
    )
    cards = "".join(
        f'<div class="card"><h3>{esc(title)}</h3><p>{esc(text)}</p></div>'
        for title, text in data["cards"]
    )
    labels = "".join(f"<div><b>{esc(label)}</b></div>" for label in data["labels"])
    gonstead = shell.href("gonstead-system", DEPTH)
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Who We Are<span>/</span>Meet the Doctor</div><span class="eyebrow">{esc(data["slogan"])}</span><h1>Dr. Willie So</h1><p class="sub-h">Gonstead Chiropractor</p></div></section>
<section style="padding-top:40px"><div class="container doc-grid"><div class="doc-img"><img src="{pre}assets/img/dr-will-so-portrait.webp" alt="Dr. Willie So" width="900" height="900"></div>
<div>{"".join(f"<p>{esc(part)}</p>" for part in bio)}</div></div></section>
<section><div class="container article-grid"><article class="article"><h2>Dr. So's Journey to Chiropractic</h2>{"".join(f"<p>{esc(part)}</p>" for part in data["journey"])}
<h2>Our strength</h2><h3>Why choose us?</h3>{strength}
<h2>{esc(meet)}</h2><h3>{esc(data["feel"])}</h3>{"".join(f"<p>{esc(part)}</p>" for part in current_paras)}
<h2>{esc(data["care_h"])}</h2><h3>{esc(data["care_sub"])}</h3><div class="cards">{cards}</div>
<h2>{esc(data["gonstead_h"])}</h2><h3>{esc(data["gonstead_sub"])}</h3><p>{esc(data["gonstead_para"])}</p><p><a href="{gonstead}">{esc(data["explore"])}</a></p>
<h2>{esc(data["training_h"])}</h2><h3>{esc(data["training_sub"])}</h3><p>{esc(data["training_para"])}</p><div class="strip">{labels}</div>
<h2>{esc(data["ready_h"])}</h2><p>{esc(data["ready_para"])}</p>
<div class="inline-cta"><h2>Ready To Find Out More Information?</h2><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Who We Are</h3>{links}</div></aside></div></section>
{review_html(data["reviews"])}'''
    page = shell.render_page(
        "Meet the Doctor | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "Feel And Function Better With Targeted Chiropractic Care",
        body,
        DEPTH,
    )
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    for forbidden in (
        "Henderson",
        "New Patient Special",
        "$47",
        "Dr. [Last Name]",
        "Dr. Will So",
        "Will So, D.C.",
        "Dr Willie So",
        "8+ Years Of Experience",
        "1263 E Silverado",
        "Grow Gonstead",
        "20250814_131251",
        "20251020_162305",
        "evergrowthchiro.com/",
        "linkedin.com",
        "youtube.com",
    ):
        if forbidden in page:
            raise SystemExit("forbidden wording in meet the doctor page: " + forbidden)
    if shell.has_unexpected_social(page):
        raise SystemExit("unexpected social link on meet the doctor page")
    if 'href="/' in page or "target=" in main:
        raise SystemExit("root-absolute or outside link in meet the doctor page")
    if page.count("dr-will-so-portrait.webp") != 1:
        raise SystemExit("headshot missing or duplicated")
    if "stock-" in main:
        raise SystemExit("stock image on the doctor page")
    for needed in (
        "Dr. So's Journey to Chiropractic",
        "10+ Years Of Experience",
        "Certified Gonstead",
        "Affordable pricing",
        "Meet Dr. Willie So Your Local Chiropractor",
        "Dr. Willie So works with each patient",
        "Explore the Gonstead Method",
        "Ready To Find Out More Information?",
        "Ready To Start Chiropractic Care Near You Today",
        "DNoria R.",
        "Emily E.",
        "Laurie W.",
        "Andrea V.",
        "Dr Will is a GREAT chiropractor.",
        "Dr. Will is amazing!",
        'href="../book-appointment/"',
        'href="../meet-the-doctor/"',
        'href="../gonstead-system/"',
        "9555 S Eastern Ave, Ste 240B",
        "Las Vegas, NV 89123",
        "10am to 1pm, 3pm to 6pm",
        "Appointments only",
        "Info@evergrowthchiro.com",
        'content="noindex, nofollow"',
        'href="../assets/style.css"',
        "arteriovenous malformation (AVM)",
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    if page.count("<cite>") != 4:
        raise SystemExit("expected four reviews")
    if main.count("Dr. Willie So") < 8:
        raise SystemExit("name did not land often enough")
    # Journey text must match the archive character for character.
    for part in data["journey"]:
        if esc(part) not in page:
            raise SystemExit("journey paragraph missing or edited")
    dest = ROOT / SLUG / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    rewire_nav()
    mark_site_map()
    build_id = stamp(previous)
    print(dest)
    return build_id


if __name__ == "__main__":
    build()
