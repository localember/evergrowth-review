"""Contact Us page.

Copy is the 2026-04-17 archive text plus the current contact page.
The current page already uses the Las Vegas address. The archive page
still says Henderson.

Wording changes, and only these:
- Title "Contact Us - Chiropractor Henderson NV | New Patient Experience"
  becomes "Contact Us | Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- Archive address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183
  becomes 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123.
- Current address line lacked the comma before Las Vegas. The page shows
  the specified new address, with that comma.
- Archive hours (Fri 10am - 1pm, Sat 10am - 1 pm, Sun Closed) and the
  current hours (no Sat or Sun line) become the new hours, including
  Sat and Sun closed.
- Current phone "702-389-5009" is shown as (702) 389-5009.
The New Patient Special block and the social links are left off.
No map embed. One Google Maps link opens in a new tab.
Reviews stay word for word, including Dr Will and Dr. Will.
The form is shown and does not submit. It shows the same not-active notice as Book Appointment.
"""
import hashlib
import html
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SLUG = "contact-us"
OLD = Path("/tmp/evergrowth-src/old/pages/contact-us_20260417.txt")
CURRENT = Path("/tmp/evergrowth-src/current/contact.txt")

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

MAP = (
    "https://www.google.com/maps/search/?api=1&amp;query="
    "9555+S+Eastern+Ave,+Ste+240B,+Las+Vegas,+NV+89123"
)

NOTE = (
    "BUILT. Form fields shown: first name, last name, phone, email, message, "
    "SMS opt-in (old wording kept). Submit is not wired to a CRM. The form shows the not-active notice and does not submit. No date of birth field. "
    "No map embed. Google Maps link opens in a new tab. "
    "Swaps: title Henderson and New Patient Experience to Las Vegas and Evergrowth Chiropractic; "
    "1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 to 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123; "
    "current address comma added before Las Vegas; "
    "old hours and current hours replaced with the new hours, including Sat and Sun closed; "
    "phone shown as (702) 389-5009. "
    "New Patient Special and social links left off. No photos. Reviews keep Dr Will and Dr. Will."
)


def esc(text):
    return html.escape(text, quote=False)


def check_copy():
    old = OLD.read_text()
    current = CURRENT.read_text()
    for text, label in (
        ("Contact Us - Chiropractor Henderson NV | New Patient Experience", "old title"),
        ("1263 E Silverado Ranch Blvd #105A", "old address"),
        ("Henderson, NV 89183", "old city"),
        ("Fill out the form below, including all required fields, and we will contact you as soon as possible.", "form intro"),
        ("Opt-in to Text Messages", "sms label"),
        ("By providing a telephone number and checking the box to Opt-in to Text Messages", "sms consent"),
        ("Ready To Find Out More Information?", "close heading"),
        ("Request An Appointment", "request button"),
        ("New Patient Special", "special, which this page leaves off"),
        ("Fri 10am - 1pm", "old Friday hours"),
        ("Sat 10am - 1 pm", "old Saturday hours"),
    ):
        if text not in old:
            raise SystemExit("missing from archive: " + label)
    for text, name in REVIEWS:
        if text not in old or name not in old:
            raise SystemExit("review missing from archive: " + name)
    for text, label in (
        ("Contact Your Local Chiropractor Clinic Today", "current heading"),
        ("We Help You Take The Next Step To Relief", "current subhead"),
        ("Have questions about chiropractic care or the Gonstead Method?", "current intro"),
        ("9555 S Eastern Ave, Ste 240B Las Vegas, NV 89123", "current address line"),
        ("702-389-5009", "current phone"),
        ("Info@evergrowthchiro.com", "email"),
        ("Mon Wed Thur 10am-1pm 3pm-6pm", "current hours"),
        ("Friday : Appointments Only", "current Friday"),
    ):
        if text not in current:
            raise SystemExit("missing from current contact page: " + label)
    if "Henderson" in current:
        raise SystemExit("current contact page changed shape; Henderson check would be wrong")


def review_html():
    cards = []
    for text, name in REVIEWS:
        paras = "".join(f"<p>{esc(part)}</p>" for part in text.split("\n") if part.strip())
        cards.append(f'<figure class="t-card" style="margin:0">{paras}<cite>{esc(name)}</cite></figure>')
    return (
        '<section class="tint"><div class="container"><div class="center">'
        '<span class="eyebrow">Our testimonial</span>'
        "<h2>What patients say about Evergrowth Chiropractic</h2></div>"
        '<div class="t-grid three">' + "".join(cards) + "</div></div></section>"
    )


def hours_html():
    rows = "".join(
        f"<li><span>{esc(day)}</span><span>{esc(when)}</span></li>" for day, when in shell.HOURS
    )
    return f"<ul>{rows}</ul>"


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
    check_copy()
    previous = (ROOT / "build-id.txt").read_text().strip()
    home = shell.href("index", DEPTH)
    hours = hours_html()
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{home}">Home</a><span>/</span>Contact Us</div><h1>Contact Your Local Chiropractor Clinic Today</h1><p class="sub-h">We Help You Take The Next Step To Relief</p><p>Have questions about chiropractic care or the Gonstead Method? Our team is here to help. Reach out to Evergrowth Chiropractic to learn more about our approach or schedule your appointment.</p></div></section>
<section><div class="container nap-grid">
<div class="side-card"><h3>Location</h3><p>{shell.ADDR1}<br>{shell.ADDR2}</p><p style="margin-top:12px"><a href="{MAP}" target="_blank" rel="noopener">Google Maps</a></p></div>
<div class="side-card"><h3>Email</h3><p><a href="mailto:{shell.EMAIL}">{shell.EMAIL}</a></p></div>
<div class="side-card"><h3>Phone</h3><p><a class="phone-link" href="{shell.TEL}">{shell.ICONS["phone"]}{shell.PHONE}</a></p></div>
<div class="side-card"><h3>Open Hours</h3>{hours}</div>
</div></section>
<section><div class="container" style="max-width:800px"><h2>Contact Us</h2><p>Fill out the form below, including all required fields, and we will contact you as soon as possible.</p>
<form class="contact-form" onsubmit="return false">
<p class="full form-notice" role="status">This form is not active in this preview and will not accept a message.</p>
<div><label for="first-name">First Name*</label><input id="first-name" name="first-name" type="text" required></div>
<div><label for="last-name">Last Name*</label><input id="last-name" name="last-name" type="text" required></div>
<div><label for="phone">Phone*</label><input id="phone" name="phone" type="tel" required></div>
<div><label for="email">Email*</label><input id="email" name="email" type="email" required></div>
<div class="full"><label for="message">Message*</label><textarea id="message" name="message" required></textarea></div>
<div class="full"><p style="margin:0 0 8px;font-weight:600;color:var(--ink)">Text Messages</p><label class="check"><input type="checkbox" name="sms-opt-in"> Opt-in to Text Messages</label></div>
<div class="full fine"><p>By providing a telephone number and checking the box to Opt-in to Text Messages, I consent to be contacted by SMS text messages regarding customer care, account notifications, and delivery notifications. Reply STOP to opt out of further messaging. Reply HELP for more information. Message frequency may vary. Message and data rates may apply. I agree with the <a href="../site-map.html#privacy-policy">Privacy Policy</a> and <a href="../site-map.html#terms-of-service">Terms and Conditions</a> for Evergrowth Chiropractic.</p></div>
<div class="full"><button class="btn" type="button" disabled>Submit</button></div>
</form></div></section>
{review_html()}
<section class="cta-band"><div class="container"><div class="box"><h2>Ready To Find Out More Information?</h2><div class="book-actions" style="justify-content:center">{shell.book_btn(DEPTH, "Request An Appointment")}</div></div></div></section>'''
    page = shell.render_page(
        "Contact Us | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "Contact Your Local Chiropractor Clinic Today. We Help You Take The Next Step To Relief.",
        body,
        DEPTH,
    )
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording on contact page")
    if "1263 E Silverado" in page or "Grow Gonstead" in page:
        raise SystemExit("old footer copied onto contact page")
    if 'href="/' in page or "evergrowthchiro.com/" in page:
        raise SystemExit("root-absolute or live-site link on contact page")
    if "<iframe" in page.lower() or "maps/embed" in page:
        raise SystemExit("map embed on contact page")
    extra_blank = shell.unexpected_blank_targets(page, extra_allowed=("google.com/maps",))
    if extra_blank:
        raise SystemExit("Google Maps link missing or an extra outside link")
    if "google.com/maps" not in page:
        raise SystemExit("Google Maps link missing")
    if "placeholder=" in page or "Dr. [Last Name]" in page or "\u2014" in page:
        raise SystemExit("placeholder or em dash on contact page")
    if "date of birth" in page.lower() or "20250814_131251" in page or "20251020_162305" in page:
        raise SystemExit("forbidden field or photo on contact page")
    if "<img" in main:
        raise SystemExit("image on contact page")
    if shell.has_unexpected_social(page):
        raise SystemExit("unexpected social link on contact page")
    before, after_reviews = main.split("Our testimonial", 1)
    written = before + after_reviews.split("</section>", 1)[1]
    for word in ("treat", "treatment", "treating", "treated"):
        if word in written.lower():
            raise SystemExit("written text uses " + word)
    for needed in (
        "Contact Your Local Chiropractor Clinic Today",
        "We Help You Take The Next Step To Relief",
        "Have questions about chiropractic care or the Gonstead Method?",
        "Fill out the form below, including all required fields, and we will contact you as soon as possible.",
        "First Name*",
        "Last Name*",
        "Phone*",
        "Email*",
        "Message*",
        "Text Messages",
        "Opt-in to Text Messages",
        "Reply STOP to opt out of further messaging.",
        "Ready To Find Out More Information?",
        "Request An Appointment",
        "DNoria R.",
        "Emily E.",
        "Laurie W.",
        "Andrea V.",
        "Dr Will is a GREAT chiropractor.",
        "Dr. Will is amazing!",
        "after my treatments.",
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
        'href="../contact-us/"',
    ):
        if needed not in page:
            raise SystemExit("missing from page: " + needed)
    book = page.split('href="../book-appointment/"', 1)[1].split(">", 1)[0]
    if "target" in book:
        raise SystemExit("Request An Appointment opens in a new tab")
    if page.count("<cite>") != 4:
        raise SystemExit("expected four reviews")
    if "onsubmit=\"return false\"" not in page or "This form is not active in this preview and will not accept a message." not in page:
        raise SystemExit("form would submit or is missing the not-active notice")
    if 'type="submit"' in page:
        raise SystemExit("contact form still has a submit button")
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
