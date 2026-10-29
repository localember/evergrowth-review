"""Legal pages batch 1. Copy is the named archive text.

Wording changes, and only these, on every page:
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- The old footer address and hours are not copied. The shared shell
  supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the
  new hours.

No doctor name appears in these four pages, so there is no name swap.
Body sentences stay as written, including chiropracticmaui.com, the
HHS address in Washington, D.C., and the $400 dispute line.
The New Patient Special block is left off.
Outside links open in a new tab. Book Appointment stays on this preview.
No images.
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
OLD = Path("/tmp/evergrowth-src/old/pages")
PHONE = "(702) 389-5009"
TEL = "tel:+17023895009"
HHS_PORTAL = "https://ocrportal.hhs.gov/ocr/portal/lobby.jsf"
HHS_FORM = "https://eforms.state.gov/Forms/ds4282.PDF"
CMS_TEXT = "www.cms.gov/nosurprises"
CMS_HREF = "https://www.cms.gov/nosurprises"
TOLL_FREE = "1-800-985-3059"
HHS_VOICE = "1-800-368-1019"
HHS_TDD = "800-537-7697"
CLOSER = "Ready To Find Out More Information?"
REQUEST = "Request An Appointment"
OLD_ADDRESS = "1263 E Silverado Ranch Blvd #105A"
OLD_CITY = "Henderson, NV 89183"

ACCESS_UPDATED = "UPDATED: February 2024"
ACCESS_GENERAL_H = "General"
ACCESS_GENERAL = (
    "Evergrowth Chiropractic strives to ensure that its services are accessible to people with disabilities. "
    "Evergrowth Chiropractic has invested a significant amount of resources to help ensure that its website is made easier to use and more accessible for people with disabilities, with the strong belief that every person has the right to live with dignity, equality, comfort, and independence."
)
ACCESS_H = "Accessibility"
ACCESS = (
    "Consistent with this goal, we have taken several steps to enhance our site and increase its usability by those who access the web using assistive technology. "
    "Our efforts are guided by the Web Content Accessibility Guidelines, version 2.1, Level AA (WCAG 2.1 AA). We will continue to enhance our digital properties to deliver accessible experiences."
)
ACCESS_DISC_H = "Disclaimer"
ACCESS_DISC = (
    "Evergrowth Chiropractic continues its efforts to constantly improve the accessibility of its site and services in the belief that it is our collective moral obligation to allow seamless, accessible, and unhindered use also for those of us with disabilities."
)
ACCESS_DISC2 = (
    "Despite our efforts to make all pages and content on chiropracticmaui.com fully accessible, some content may not have yet been fully adapted to the strictest accessibility standards. This may be a result of not having found or identified the most appropriate technological solution."
)
ACCESS_HERE_H = "Here For You"
ACCESS_HERE = (
    "If you are experiencing difficulty with any content on chiropracticmaui.com or require assistance with any part of our site, please contact us during normal business hours at (702) 389-5009, and we will be happy to assist."
)
ACCESS_CONTACT_H = "Contact Us"
ACCESS_CONTACT = (
    "If you wish to report an accessibility issue, have any questions, or need assistance, please contact Evergrowth Chiropractic at (702) 389-5009."
)

ANTI_P1 = (
    "This Evergrowth Chiropractic complies with applicable Federal civil rights laws and does not discriminate on the basis of race, color, national origin, age, disability, or sex. "
    "Evergrowth Chiropractic does not exclude people or treat them differently because of race, color, national origin, age, disability, or sex."
)
ANTI_P2 = (
    "If you believe that Evergrowth Chiropractic has failed to provide these services or discriminated in another way on the basis of race, color, national origin, age, disability, or sex, you can file a grievance with our Team at the address, phone number, or email address provided on this website."
)
ANTI_P3 = (
    "You can file a grievance in person or by mail, fax, or email. If you need help filing a grievance, our Team is available to help you."
)
ANTI_P4 = (
    "You can also file a civil rights complaint with the U.S. Department of Health and Human Services, Office for Civil Rights, electronically through the Office for Civil Rights Complaint Portal, available at https://ocrportal.hhs.gov/ocr/portal/lobby.jsf, or by mail or phone at:"
)
ANTI_ADDR = [
    "U.S. Department of Health and Human Services",
    "200 Independence Avenue, SW",
    "Room 509F, HHH Building",
    "Washington, D.C. 20201",
]
ANTI_PHONE_LINE = "1-800-368-1019, 800-537-7697 (TDD)"
ANTI_P5 = "Complaint forms are available at https://eforms.state.gov/Forms/ds4282.PDF"

GFE = [
    'You have the right to receive a "Good Faith Estimate" explaining how much your medical care will cost. Under the law, health care providers need to give patients who don\'t have insurance or who are not using insurance an estimate of the bill for medical items and services.',
    "You have the right to receive a Good Faith Estimate for the total expected cost of any non-emergency items or services. This includes related costs like medical tests, prescription drugs, equipment, and hospital fees.",
    "Make sure your health care provider gives you a Good Faith Estimate in writing at least 1 business day before your medical service or item. You can also ask your healthcare provider, and any other provider you choose, for a Good Faith Estimate before you schedule an item or service.",
    "If you receive a bill that is at least $400 more than your Good Faith Estimate, you can dispute the bill.",
    "Make sure to save a copy or picture of your Good Faith Estimate.",
    "For questions or more information about your right to a Good Faith Estimate, visit www.cms.gov/nosurprises or call 1-800-985-3059.",
]

HEALTH = (
    "The information, including but not limited to, text, graphics, images and other material contained on this website are for informational purposes only. "
    "The purpose of this website is to promote broad consumer understanding and knowledge of various health topics. "
    "It is not intended to be a substitute for professional medical advice, diagnosis or treatment. "
    "Always seek the advice of your physician or other qualified healthcare provider with any questions you may have regarding a medical condition or treatment and before undertaking a new health care regimen, and never disregard professional medical advice or delay in seeking it because of something you have read on this website."
)

NOTES = {
    "accessibility-statement": (
        "BUILT from old/pages/accessibility-statement_20260417.txt. Body copy left as written, including chiropracticmaui.com. "
        "Title Henderson and New Patient Experience swapped to Las Vegas and Evergrowth Chiropractic. "
        "Old footer address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 was not copied. "
        "Old hours on that capture (Mon, Wed, Thu 10am - 1pm and 3pm - 6pm, Tues 3pm - 6pm, Fri 10am - 1pm, Sat 10am - 1 pm, Sun Closed) were not copied. "
        "The shared shell supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the new hours. "
        "No doctor name, so no name swap. New Patient Special left off. No images."
    ),
    "anti-discrimination-disclaimer": (
        "BUILT from old/pages/anti-discrimination-disclaimer_20260511.txt. Body copy left as written, including the HHS address in Washington, D.C. "
        "Title Henderson and New Patient Experience swapped to Las Vegas and Evergrowth Chiropractic. "
        "Old footer address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 was not copied. "
        "Old hours Mon through Fri 10am - 6pm, Sat and Sun Closed, were not copied. "
        "The shared shell supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the new hours. "
        "No doctor name, so no name swap. The complaint portal and the complaint form open in a new tab. New Patient Special left off. No images."
    ),
    "good-faith-estimate": (
        "BUILT from old/pages/good-faith-estimate_20260511.txt. Body copy left as written, including the $400 dispute line. "
        "Title Henderson and New Patient Experience swapped to Las Vegas and Evergrowth Chiropractic. "
        "Old footer address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 was not copied. "
        "Old hours Mon through Fri 10am - 6pm, Sat and Sun Closed, were not copied. "
        "The shared shell supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the new hours. "
        "No doctor name, so no name swap. www.cms.gov/nosurprises opens in a new tab. New Patient Special left off. No images."
    ),
    "healthcare-disclaimer": (
        "BUILT from old/pages/healthcare-disclaimer_20260511.txt. Body copy left as written. "
        "Title Henderson and New Patient Experience swapped to Las Vegas and Evergrowth Chiropractic. "
        "Old footer address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 was not copied. "
        "Old hours Mon through Fri 10am - 6pm, Sat and Sun Closed, were not copied. "
        "The shared shell supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the new hours. "
        "No doctor name, so no name swap. New Patient Special left off. No images."
    ),
}


def esc(text):
    return html.escape(text, quote=False)


def require(raw, text, label):
    if text not in raw:
        raise SystemExit("missing from archive: " + label)


def tel(display, number):
    return f'<a href="tel:+1{number}">{esc(display)}</a>'


def ext(href, label):
    return (
        f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener">{esc(label)}</a>'
    )


def para(text, swaps=()):
    out = esc(text)
    for raw, snippet in swaps:
        token = esc(raw)
        if out.count(token) != 1:
            raise SystemExit("swap count for " + raw)
        out = out.replace(token, snippet, 1)
    return "<p>" + out + "</p>"


def hours_html():
    rows = (
        ("Mon, Wed, Thu", "10am to 1pm, 3pm to 6pm"),
        ("Tuesday", "3pm to 6pm"),
        ("Friday", "Appointments only"),
        ("Sat, Sun", "Closed"),
    )
    return "<ul>" + "".join(
        f"<li><span>{day}</span><span>{when}</span></li>" for day, when in rows
    ) + "</ul>"


def aside():
    return (
        f'<aside class="aside"><div class="side-card"><h3>Book Appointment</h3>'
        f'<p style="font-size:15px">{shell.ADDR1}<br>{shell.ADDR2}</p>'
        f'{shell.book_btn(DEPTH, "Book Appointment", "btn-block")}'
        f'<p style="margin:14px 0 0;text-align:center"><a class="phone-link" href="{shell.TEL}">'
        f'{shell.ICONS["phone"]}{shell.PHONE}</a></p>'
        f'<p style="margin:8px 0 0;text-align:center"><a href="mailto:{shell.EMAIL}">{shell.EMAIL}</a></p></div>'
        f'<div class="side-card"><h3>Hours</h3>{hours_html()}</div></aside>'
    )


def closer():
    return (
        f'<section class="cta-band"><div class="container"><div class="box"><h2>{esc(CLOSER)}</h2>'
        f'<div class="book-actions" style="justify-content:center">{shell.book_btn(DEPTH, REQUEST)}</div>'
        f"</div></div></section>"
    )


def article_page(slug, h1, description, article):
    home = shell.href("index", DEPTH)
    body = (
        f'<section class="page-hero"><div class="container"><div class="crumbs">'
        f'<a href="{home}">Home</a><span>/</span>{esc(h1)}</div><h1>{esc(h1)}</h1></div></section>'
        f'<section><div class="container article-grid"><article class="article">{article}</article>'
        f"{aside()}</div></section>{closer()}"
    )
    return shell.render_page(
        f"{h1} | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        description,
        body,
        DEPTH,
    )


def check_common(raw, title):
    require(raw, title, "old title")
    require(raw, CLOSER, "closer")
    require(raw, REQUEST, "request button")
    require(raw, "New Patient Special Offer", "special, which this page leaves off")
    require(raw, OLD_ADDRESS, "old address")
    require(raw, OLD_CITY, "old city")


def check_access(raw):
    check_common(raw, "Accessibility Statement - Chiropractor Henderson NV | New Patient Experience")
    for text, label in (
        (ACCESS_UPDATED, "updated line"),
        (ACCESS_GENERAL_H, "general heading"),
        (ACCESS_GENERAL, "general"),
        (ACCESS_H, "accessibility heading"),
        (ACCESS, "accessibility"),
        (ACCESS_DISC_H, "disclaimer heading"),
        (ACCESS_DISC, "disclaimer"),
        (ACCESS_DISC2, "disclaimer maui"),
        (ACCESS_HERE_H, "here heading"),
        (ACCESS_HERE, "here"),
        (ACCESS_CONTACT_H, "contact heading"),
        (ACCESS_CONTACT, "contact"),
        ("Mon 10am - 1pm & 3pm - 6pm", "old Monday hours"),
        ("Tues 3pm - 6pm", "old Tuesday hours"),
        ("Fri 10am - 1pm", "old Friday hours"),
        ("Sat 10am - 1 pm", "old Saturday hours"),
        ("Sun Closed", "old Sunday"),
    ):
        require(raw, text, label)
    body = raw.split("Accessibility Statement\n", 1)[1].split("New Patient Special Offer", 1)[0]
    if "Henderson" in body or "1263" in body:
        raise SystemExit("accessibility body gained a city or address; log it before building")


def check_anti(raw):
    check_common(raw, "Anti-Discrimination Disclaimer - Chiropractor Henderson NV | New Patient Experience")
    for text, label in (
        (ANTI_P1, "opening"),
        (ANTI_P2, "grievance"),
        (ANTI_P3, "help"),
        (ANTI_P4, "portal"),
        (ANTI_PHONE_LINE, "hhs phones"),
        (ANTI_P5, "form"),
        ("Mon 10am - 6pm", "old Monday hours"),
        ("Fri 10am - 6pm", "old Friday hours"),
        ("Sat Closed", "old Saturday"),
        ("Sun Closed", "old Sunday"),
    ):
        require(raw, text, label)
    for line in ANTI_ADDR:
        require(raw, line, line)
    body = raw.split("Anti-Discrimination Disclaimer\n", 1)[1].split("New Patient Special Offer", 1)[0]
    if "Henderson" in body or "1263" in body or "Las Vegas" in body:
        raise SystemExit("anti-discrimination body gained a clinic city or address")


def check_gfe(raw):
    check_common(raw, "Good Faith Estimate - Chiropractor Henderson NV | New Patient Experience")
    for text in GFE:
        require(raw, text, text[:48])
    require(raw, "Mon 10am - 6pm", "old Monday hours")
    require(raw, "Sat Closed", "old Saturday")
    require(raw, "Sun Closed", "old Sunday")
    body = raw.split("Good Faith Estimate\n", 1)[1].split("New Patient Special Offer", 1)[0]
    if "Henderson" in body or "1263" in body:
        raise SystemExit("good faith body gained a city or address")


def check_health(raw):
    check_common(raw, "Healthcare Disclaimer - Chiropractor Henderson NV | New Patient Experience")
    require(raw, HEALTH, "disclaimer")
    require(raw, "Mon 10am - 6pm", "old Monday hours")
    require(raw, "Sat Closed", "old Saturday")
    require(raw, "Sun Closed", "old Sunday")
    body = raw.split("Healthcare Disclaimer\n", 1)[1].split("New Patient Special Offer", 1)[0]
    if body.strip() != HEALTH:
        raise SystemExit("healthcare body is not the single archive paragraph")


def access_article():
    return (
        para(ACCESS_UPDATED)
        + f"<h2>{esc(ACCESS_GENERAL_H)}</h2>"
        + para(ACCESS_GENERAL)
        + f"<h2>{esc(ACCESS_H)}</h2>"
        + para(ACCESS)
        + f"<h2>{esc(ACCESS_DISC_H)}</h2>"
        + para(ACCESS_DISC)
        + para(ACCESS_DISC2)
        + f"<h2>{esc(ACCESS_HERE_H)}</h2>"
        + para(ACCESS_HERE, ((PHONE, tel(PHONE, "7023895009")),))
        + f"<h2>{esc(ACCESS_CONTACT_H)}</h2>"
        + para(ACCESS_CONTACT, ((PHONE, tel(PHONE, "7023895009")),))
    )


def anti_article():
    phones = (
        tel(HHS_VOICE, "8003681019")
        + ", "
        + tel(HHS_TDD, "8005377697")
        + " (TDD)"
    )
    address = "<p>" + "<br>".join(esc(line) for line in ANTI_ADDR) + "<br>" + phones + "</p>"
    return (
        para(ANTI_P1)
        + para(ANTI_P2)
        + para(ANTI_P3)
        + para(ANTI_P4, ((HHS_PORTAL, ext(HHS_PORTAL, HHS_PORTAL)),))
        + address
        + para(ANTI_P5, ((HHS_FORM, ext(HHS_FORM, HHS_FORM)),))
    )


def gfe_article():
    parts = []
    for text in GFE:
        swaps = ()
        if CMS_TEXT in text:
            swaps = (
                (CMS_TEXT, ext(CMS_HREF, CMS_TEXT)),
                (TOLL_FREE, tel(TOLL_FREE, "8009853059")),
            )
        parts.append(para(text, swaps))
    return "".join(parts)


def health_article():
    return para(HEALTH)


PAGES = (
    (
        "accessibility-statement",
        "Accessibility Statement",
        "Evergrowth Chiropractic strives to ensure that its services are accessible to people with disabilities.",
        access_article,
        "accessibility-statement_20260417.txt",
        check_access,
    ),
    (
        "anti-discrimination-disclaimer",
        "Anti-Discrimination Disclaimer",
        "This Evergrowth Chiropractic complies with applicable Federal civil rights laws and does not discriminate on the basis of race, color, national origin, age, disability, or sex.",
        anti_article,
        "anti-discrimination-disclaimer_20260511.txt",
        check_anti,
    ),
    (
        "good-faith-estimate",
        "Good Faith Estimate",
        "You have the right to receive a Good Faith Estimate explaining how much your medical care will cost.",
        gfe_article,
        "good-faith-estimate_20260511.txt",
        check_gfe,
    ),
    (
        "healthcare-disclaimer",
        "Healthcare Disclaimer",
        "The information on this website is for informational purposes only.",
        health_article,
        "healthcare-disclaimer_20260511.txt",
        check_health,
    ),
)


def rewire(slug):
    old = f"site-map.html#{slug}"
    new = f"{slug}/"
    changed = 0
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = path.read_text()
        if old not in text:
            continue
        path.write_text(text.replace(old, new))
        changed += 1
    if changed < 1:
        raise SystemExit("nothing rewired for " + slug)
    leftover = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        if old in path.read_text():
            leftover.append(str(path.relative_to(ROOT)))
    if leftover:
        raise SystemExit("anchor still in " + ", ".join(leftover))
    print("rewired", slug, changed)


def mark_site_map(slug, note):
    path = ROOT / "site-map.html"
    html_text = path.read_text()
    start = html_text.find(f'<tr id="{slug}">')
    if start < 0:
        raise SystemExit("site-map row missing: " + slug)
    end = html_text.find("</tr>", start)
    row = html_text[start:end]
    old_cell = "<td>planned (not built)</td>"
    new_cell = f'<td><a href="{slug}/">{slug}/</a> (built)</td>'
    if old_cell not in row:
        raise SystemExit("status cell missing: " + slug)
    row = row.replace(old_cell, new_cell, 1)
    note_start = row.rfind("<td>")
    if note_start < 0:
        raise SystemExit("note cell missing: " + slug)
    row = row[:note_start] + f"<td>{html.escape(note)}</td>"
    path.write_text(html_text[:start] + row + html_text[end:])
    print("site-map marked", slug)


def outside_links(main):
    return re.findall(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>', main)


def check_page(slug, h1, page, outside):
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording on " + slug)
    if "1263 E Silverado" in page or "Grow Gonstead" in page or "Silverado" in page:
        raise SystemExit("old footer copied onto " + slug)
    if 'href="/' in page or "evergrowthchiro.com/" in page or "web.archive.org" in page:
        raise SystemExit("root-absolute or live-site link on " + slug)
    if "placeholder=" in page or "Dr. [Last Name]" in page or "Dr. Willie" in page:
        raise SystemExit("placeholder or name text on " + slug)
    if "\u2014" in page or "\u2013" in page:
        raise SystemExit("dash in " + slug)
    if "20250814_131251" in page or "20251020_162305" in page:
        raise SystemExit("unconfirmed photo on " + slug)
    if "<img" in main:
        raise SystemExit("image on " + slug)
    social = ("facebook", "instagram", "linkedin", "youtube", "twitter")
    if any(word in page.lower() for word in social):
        raise SystemExit("social link on " + slug)
    if "date of birth" in page.lower():
        raise SystemExit("date of birth on " + slug)
    found = outside_links(main)
    if found != outside:
        raise SystemExit("outside links on " + slug + ": " + ", ".join(found))
    for href in found:
        tag = re.search(r'<a\b[^>]*href="' + re.escape(href) + r'"[^>]*>', main)
        if tag is None or 'target="_blank"' not in tag.group(0) or 'rel="noopener"' not in tag.group(0):
            raise SystemExit("outside link missing new-tab attrs on " + slug)
    for tag in re.findall(r'<a\b[^>]*href="(?:tel:|mailto:)[^"]*"[^>]*>', page):
        if "target" in tag:
            raise SystemExit("phone or email opens in a new tab on " + slug)
    for tag in re.findall(r'<a\b[^>]*href="[^"]*book-appointment/[^"]*"[^>]*>', page):
        if "target" in tag:
            raise SystemExit("Book Appointment opens in a new tab on " + slug)
    for needed in (
        f"<h1>{h1}</h1>",
        CLOSER,
        REQUEST,
        'href="../book-appointment/"',
        "9555 S Eastern Ave, Ste 240B",
        "Las Vegas, NV 89123",
        "10am to 1pm, 3pm to 6pm",
        "Appointments only",
        ">Sat, Sun</span>",
        ">Closed</span>",
        "Info@evergrowthchiro.com",
        PHONE,
        'content="noindex, nofollow"',
        'href="../assets/style.css"',
        f'href="../{slug}/"',
        "Mon, Wed, Thu",
        "Tuesday",
        "Friday",
    ):
        if needed not in page:
            raise SystemExit("missing from " + slug + ": " + needed)
    if page.count('href="../book-appointment/"') < 3:
        raise SystemExit("expected header, aside, and closer booking links on " + slug)


def stamp(previous):
    build_id = hashlib.sha256((ROOT / "index.html").read_bytes()).hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    previous = (ROOT / "build-id.txt").read_text().strip()
    written = []
    specs = (
        (
            PAGES[0],
            (ACCESS_UPDATED, ACCESS_GENERAL, ACCESS, ACCESS_DISC, ACCESS_DISC2, ACCESS_HERE, ACCESS_CONTACT),
            [],
        ),
        (PAGES[1], (ANTI_P1, ANTI_P2, ANTI_P3, ANTI_P4, ANTI_P5, ANTI_PHONE_LINE), [HHS_PORTAL, HHS_FORM]),
        (PAGES[2], tuple(GFE), [CMS_HREF]),
        (PAGES[3], (HEALTH,), []),
    )
    for (slug, h1, description, article, filename, checker), needles, outside in specs:
        raw = (OLD / filename).read_text()
        checker(raw)
        page = article_page(slug, h1, description, article())
        visible = re.sub(r"<[^>]+>", "", page)
        for needle in needles:
            if needle not in visible:
                raise SystemExit("copy dropped from " + slug + ": " + needle[:60])
        check_page(slug, h1, page, outside)
        dest = ROOT / slug / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page)
        written.append(slug)
        print(dest)
    for slug in written:
        rewire(slug)
        mark_site_map(slug, NOTES[slug])
        built = (ROOT / slug / "index.html").read_text()
        if f'href="../{slug}/"' not in built:
            raise SystemExit("page lost its own footer link: " + slug)
        if f"site-map.html#{slug}" in built:
            raise SystemExit("page still points at the site map: " + slug)
    home = (ROOT / "index.html").read_text()
    for slug in written:
        if f'href="{slug}/"' not in home:
            raise SystemExit("home footer was not rewired: " + slug)
        if f"site-map.html#{slug}" in home:
            raise SystemExit("home still has the site map anchor: " + slug)
    access = (ROOT / "accessibility-statement" / "index.html").read_text()
    if access.count("chiropracticmaui.com") != 2:
        raise SystemExit("maui wording was edited")
    main = access.split("<main", 1)[1].split("</main>", 1)[0]
    if "chiropracticmaui.com</a>" in main or 'href="http://chiropracticmaui.com' in main or 'href="https://chiropracticmaui.com' in main:
        raise SystemExit("maui domain was turned into a link")
    anti = (ROOT / "anti-discrimination-disclaimer" / "index.html").read_text()
    if len(re.findall(r"\btreat\b", anti)) != 1:
        raise SystemExit("treat wording changed")
    health = (ROOT / "healthcare-disclaimer" / "index.html").read_text()
    if health.count("treatment") != 2:
        raise SystemExit("client treatment wording changed")
    stamp(previous)


if __name__ == "__main__":
    build()
