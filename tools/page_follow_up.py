"""Follow Up Visit page. Copy is the 2026-05-11 archive text.

Wording changes, and only these:
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- "your Henderson, NV Chiropractor" becomes "your Las Vegas, NV Chiropractor".
- "SCHEDULE A CHIROPRACTIC APPOINTMENT IN Henderson NV" becomes
  "SCHEDULE A CHIROPRACTIC APPOINTMENT IN Las Vegas NV".
The new address and hours come from the shared shell, not from the old footer.
The New Patient Special block on the old page is left off.
Reviews stay word for word. No images.
Schedule, Time, Consistency, and Stay Well use the Home steps cards.
The old page has four sections, so no fifth card was added.
"""
import hashlib
import html
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SRC = Path("/tmp/evergrowth-src/old/pages/follow-up-visit_20260511.txt")
SLUG = "follow-up-visit"

NOTE = (
    "BUILT. No images. Old Follow Up Visit copy kept as written. "
    "Title Henderson NV became Las Vegas NV. "
    "Henderson, NV Chiropractor became Las Vegas, NV Chiropractor. "
    "SCHEDULE A CHIROPRACTIC APPOINTMENT IN Henderson NV became Las Vegas NV. "
    "Old footer address and hours replaced by the Las Vegas address and the new hours. "
    "The New Patient Special block on the old page is left off. "
    "The four reviews are included word for word. "
    "Schedule, Time, Consistency, and Stay Well use the Home steps cards. "
    "The old page has four sections, so no fifth card was added."
)


def esc(text):
    return html.escape(text, quote=False)


def grab(lines, number):
    text = lines[number - 1]
    if not text.strip():
        raise SystemExit(f"empty archive line {number}")
    return text


def load_copy():
    raw = SRC.read_text()
    lines = raw.splitlines()
    intro_old = grab(lines, 60)
    schedule_old = grab(lines, 61)
    if intro_old.count("Henderson, NV") != 1 or "Henderson" in intro_old.replace("Henderson, NV", "", 1):
        raise SystemExit("unexpected Henderson in the intro")
    if schedule_old.count("Henderson NV") != 1 or "Henderson" in schedule_old.replace("Henderson NV", "", 1):
        raise SystemExit("unexpected Henderson in the schedule heading")
    intro = intro_old.replace("Henderson, NV", "Las Vegas, NV", 1)
    schedule_h = schedule_old.replace("Henderson NV", "Las Vegas NV", 1)
    copy = {
        "h1": grab(lines, 58),
        "sub": grab(lines, 59),
        "intro": intro,
        "schedule_h": schedule_h,
        "schedule_p": grab(lines, 62),
        "time_h": grab(lines, 63),
        "time_lead": grab(lines, 64),
        "factors": [grab(lines, 65), grab(lines, 66), grab(lines, 67)],
        "consistency_h": grab(lines, 68),
        "consistency_p": grab(lines, 69),
        "stay_h": grab(lines, 70),
        "stay": [grab(lines, 71), grab(lines, 72)],
        "reviews": [
            ([grab(lines, 75)], grab(lines, 76)),
            ([grab(lines, 77)], grab(lines, 78)),
            ([grab(lines, 79), grab(lines, 80)], grab(lines, 81)),
            ([grab(lines, 82)], grab(lines, 83)),
        ],
    }
    for chunk in (
        intro_old,
        schedule_old,
        copy["schedule_p"],
        copy["time_lead"],
        copy["consistency_p"],
        copy["stay"][0],
        copy["stay"][1],
        "New Patient Special Offer",
    ):
        if chunk not in raw:
            raise SystemExit("copy drift against archive text: " + chunk[:70])
    for paras, name in copy["reviews"]:
        if name not in raw:
            raise SystemExit("review name missing from archive: " + name)
        for para in paras:
            if para not in raw:
                raise SystemExit("review text missing from archive: " + para[:70])
    if "Henderson" in intro or "Henderson" in schedule_h:
        raise SystemExit("swap missed Henderson")
    swaps = [
        'Title: "Chiropractor Henderson NV | New Patient Experience" -> "Chiropractor Las Vegas NV | Evergrowth Chiropractic"',
        'Intro: "Henderson, NV" -> "Las Vegas, NV" in "your Henderson, NV Chiropractor"',
        'Heading: "SCHEDULE A CHIROPRACTIC APPOINTMENT IN Henderson NV" -> "SCHEDULE A CHIROPRACTIC APPOINTMENT IN Las Vegas NV"',
        "Name swap: none",
    ]
    return copy, swaps


def steps_html(copy):
    blocks = [
        (copy["schedule_h"], [copy["schedule_p"]]),
        (copy["time_h"], [copy["time_lead"], *copy["factors"]]),
        (copy["consistency_h"], [copy["consistency_p"]]),
        (copy["stay_h"], copy["stay"]),
    ]
    cards = []
    for i, (heading, paras) in enumerate(blocks, start=1):
        body = "".join(f"<p>{esc(text)}</p>" for text in paras)
        cards.append(f'<div class="step"><span class="n">{i}</span><h3>{esc(heading)}</h3>{body}</div>')
    return '<div class="steps n4">' + "".join(cards) + "</div>"


def reviews_html(copy):
    cards = []
    for paras, name in copy["reviews"]:
        body = "".join(f"<p>{esc(text)}</p>" for text in paras)
        cards.append(f'<figure class="t-card" style="margin:0">{body}<cite>{esc(name)}</cite></figure>')
    inner = "".join(cards)
    return (
        '<section class="tint"><div class="container"><div class="center">'
        '<span class="eyebrow">Our testimonial</span>'
        "<h2>What patients say about Evergrowth Chiropractic</h2></div>"
        f'<div class="t-grid ">{inner}</div></div></section>'
    )


def build_page(copy):
    home = shell.href("index", DEPTH)
    patients = [
        ("First Visit", "first-visit"),
        ("Second Visit", "second-visit"),
        ("Follow-Up Visits", "follow-up-visit"),
        ("New Patient Paperwork", "new-patient-paperwork"),
        ("Payment Plans", "payment-plans"),
    ]
    links = "".join(f'<a href="{shell.href(slug, DEPTH)}">{label}</a>' for label, slug in patients)
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Patients<span>/</span>Follow-Up Visits</div><h1>{esc(copy["h1"])}</h1><p class="sub-h">{esc(copy["sub"])}</p></div></section>
<section class="tint"><div class="container"><p>{esc(copy["intro"])}</p>{steps_html(copy)}</div></section>
<section><div class="container article-grid"><article class="article"><h2>Ready To Find Out More Information?</h2><div class="book-actions">{shell.book_btn(DEPTH, "Book Appointment")}<a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></div></article>
<aside class="aside"><div class="side-card"><h3>Book Appointment</h3><p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul><li><span>Mon, Wed, Thu</span><span>10am to 1pm, 3pm to 6pm</span></li><li><span>Tuesday</span><span>3pm to 6pm</span></li><li><span>Friday</span><span>Appointments only</span></li><li><span>Sat, Sun</span><span>Closed</span></li></ul></div>
<div class="side-card side-links"><h3>Patients</h3>{links}</div></aside></div></section>
{reviews_html(copy)}'''
    return shell.render_page(
        "Chiropractic Follow Up Visit | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        copy["intro"],
        body,
        DEPTH,
    )


def check_page(page):
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording in follow up visit page")
    if 'href="/' in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link in follow up visit page")
    extra_blank = shell.unexpected_blank_targets(page)
    if extra_blank:
        raise SystemExit("follow up visit page has an outside-link target")
    if "noindex, nofollow" not in page:
        raise SystemExit("missing noindex")
    for src in ("logo.png", "logo-white.png"):
        if src not in page:
            raise SystemExit("missing logo " + src)
    allowed = {"../assets/img/logo.png", "../assets/img/logo-white.png"}
    found = set(re.findall(r'<img[^>]+src="([^"]+)"', page))
    if found != allowed:
        raise SystemExit("unexpected images: " + ", ".join(sorted(found)))
    if page.count('class="step"') != 4:
        raise SystemExit("expected four step cards")
    if "\u2014" in page:
        raise SystemExit("em dash in follow up visit page")
    if "Dr. [Last Name]" in page or "8+ Years" in page:
        raise SystemExit("placeholder or bio text on follow up visit page")
    without_reviews = page.split("Our testimonial", 1)[0]
    for word in ("treat", "treatment", "treating", "treated"):
        if word in without_reviews.lower():
            raise SystemExit("written text uses " + word)
    for needed in (
        "Las Vegas, NV Chiropractor",
        "SCHEDULE A CHIROPRACTIC APPOINTMENT IN Las Vegas NV",
        "stay consistent",
        "DNoria R.",
        "Emily E.",
        "Laurie W.",
        "Andrea V.",
        'href="../book-appointment/"',
        'href="../follow-up-visit/"',
        "10am to 1pm, 3pm to 6pm",
        "Appointments only",
        "Info@evergrowthchiro.com",
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)


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
    if f"site-map.html#{SLUG}" in index:
        raise SystemExit("follow-up anchor still in home")
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
    start = html_text.find('<tr id="follow-up-visit">')
    if start < 0:
        raise SystemExit("site-map row missing")
    end = html_text.find("</tr>", start)
    row = html_text[start:end]
    old_cell = "<td>planned (not built)</td>"
    new_cell = '<td><a href="follow-up-visit/">follow-up-visit/</a> (built)</td>'
    if old_cell not in row:
        raise SystemExit("status cell missing: " + row[:400])
    row = row.replace(old_cell, new_cell, 1)
    empty = "<td></td>"
    if not row.endswith(empty):
        raise SystemExit("note cell not empty: " + row[-240:])
    row = row[: -len(empty)] + f"<td>{html.escape(NOTE)}</td>"
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
    previous = (ROOT / "build-id.txt").read_text().strip()
    copy, swaps = load_copy()
    page = build_page(copy)
    check_page(page)
    dest = ROOT / SLUG / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    print(dest)
    rewire_nav()
    mark_site_map()
    check_page((ROOT / SLUG / "index.html").read_text())
    build_id = stamp(previous)
    log_path = Path("/tmp/egc-r14-swaps.txt")
    log_path.write_text("\n".join(swaps) + f"\nbuild-id {build_id}\n")
    for line in swaps:
        print("swap:", line)


if __name__ == "__main__":
    build()
