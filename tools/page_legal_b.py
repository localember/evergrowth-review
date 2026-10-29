"""Legal pages batch 2. Copy is the named archive text.

Wording changes, and only these:
- Title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic" on every page.
- HIPAA notice address 1263 E Silverado Ranch Blvd #105A Henderson, NV 89183
  becomes 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123.
- HIPAA "DOCTOR*" becomes "Dr. Willie So". The "D.C." credential stays.
- Terms privacy-policy web address becomes an internal privacy-policy link,
  same tab. The client domain is not shown. The sentence otherwise stays.
- Terms keeps "Grow Gonstead/Evergrowth Chiropractic" as written.

The old footer address and hours are not copied. The shared shell supplies
the new address and the new hours. No hours appear in these three bodies.
Archive &quot; entities are shown as quotation marks.
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
HHS_MAIL = "OCRMail@hhs.gov"
HHS_TEXT = "www.hhs.gov/ocr/privacy/hipaa/complaints/hipcomplaint.pdf"
HHS_HREF = "https://www.hhs.gov/ocr/privacy/hipaa/complaints/hipcomplaint.pdf"
OLD_LINE = "Evergrowth Chiropractic-1263 E Silverado Ranch Blvd #105A Henderson, NV 89183"
NEW_LINE = "Evergrowth Chiropractic-9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123"
NAME_TOKEN = "DOCTOR*"
NAME = "Dr. Willie So"
PRIVACY_PHRASE = "Please review our Privacy Policy at https://www.evergrowthchiro.com/privacy-policy/"
PRIVACY_VISIBLE = "Please review our Privacy Policy"
GROW = "Grow Gonstead/Evergrowth Chiropractic"
CLOSER = "Ready To Find Out More Information?"
REQUEST = "Request An Appointment"
OLD_ADDRESS = "1263 E Silverado Ranch Blvd #105A"
OLD_CITY = "Henderson, NV 89183"
TOC = "TABLE OF CONTENTS"
HIPAA_SECTION = "How This Medical Practice May Use or Disclose Your Health Information"

PRIVACY_HEADINGS = {
    "Privacy Notice",
    "Information Collection, Use, and Sharing",
    "Your Access to and Control Over Information",
    "Security",
    "Cookies",
    "Links",
    "Surveys",
}
HIPAA_HEADINGS = {
    HIPAA_SECTION,
    "When This Medical Practice May Not Use or Disclose Your Health Information",
    "Your Health Information Rights",
    "Changes to this Notice of Privacy Practices",
    "Complaints",
}
LIST_STOP = ("We ", "By ", "If ", "You ", "This ", "All ")

NOTES = {
    "hipaa-privacy-practices": (
        "BUILT from old/pages/hipaa-privacy-practices_20260511.txt. Body copy left as written except the allowed swaps. "
        "Title Henderson and New Patient Experience swapped to Las Vegas and Evergrowth Chiropractic. "
        "Notice address 1263 E Silverado Ranch Blvd #105A Henderson, NV 89183 swapped to "
        "9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123. "
        "DOCTOR* swapped to Dr. Willie So. The D.C. credential stayed. "
        "Old footer address was not copied. Old hours Mon through Fri 10am - 6pm, Sat and Sun Closed, were not copied. "
        "The shared shell supplies the new address and the new hours. "
        "The HHS complaint form opens in a new tab. OCRMail@hhs.gov is a mailto link. "
        "New Patient Special left off. No images."
    ),
    "privacy-policy": (
        "BUILT from old/pages/privacy-policy_20260606.txt. Body copy left as written. "
        "No Henderson, street address, hours, or doctor name in the policy text, so no body swap. "
        "Title Henderson and New Patient Experience swapped to Las Vegas and Evergrowth Chiropractic. "
        "Old footer address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 was not copied. "
        "Old hours Mon through Fri 10am - 6pm, Sat and Sun Closed, were not copied. "
        "The shared shell supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the new hours. "
        "New Patient Special left off. No images."
    ),
    "terms-of-service": (
        "BUILT from old/pages/terms-of-service_20260606.txt. Body copy left as written, including "
        "Grow Gonstead/Evergrowth Chiropractic, which stays and is flagged. "
        "Title Henderson and New Patient Experience swapped to Las Vegas and Evergrowth Chiropractic. "
        "The old privacy-policy web address was replaced with an internal privacy-policy link, same tab. "
        "The client domain is not shown. Old footer address was not copied. "
        "Old hours Mon through Fri 10am - 6pm, Sat and Sun Closed, were not copied. "
        "The shared shell supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the new hours. "
        "No doctor name in the terms text. New Patient Special left off. No images."
    ),
}


def esc(text):
    return html.escape(text, quote=False)


def squash(text):
    return re.sub(r"\s+", " ", text).strip()


def require(raw, text, label):
    if text not in raw:
        raise SystemExit("missing from archive: " + label)


def tel(display):
    digits = re.sub(r"\D", "", display)
    if digits.startswith("1") and len(digits) == 11:
        digits = digits[1:]
    return f'<a href="tel:+1{digits}">{esc(display)}</a>'


def ext(href, label):
    return (
        f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener">{esc(label)}</a>'
    )


def mailto(address):
    return f'<a href="mailto:{address}">{esc(address)}</a>'


def para(text, swaps=()):
    out = esc(text)
    for raw, snippet in swaps:
        token = esc(raw)
        count = out.count(token)
        if count < 1:
            raise SystemExit("swap missing: " + raw)
        out = out.replace(token, snippet)
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


def article_page(h1, description, article):
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


def body_after(raw, heading):
    marker = heading + "\n"
    if marker not in raw:
        raise SystemExit("heading not found: " + heading)
    chunk = raw.split(marker, 1)[1].split("New Patient Special Offer", 1)[0]
    lines = [line.strip() for line in chunk.splitlines()]
    return [line for line in lines if line]


def join_lines(lines, heading):
    out = []
    buf = None
    for line in lines:
        if heading(line):
            if buf:
                out.append(buf)
                buf = None
            out.append(line)
            continue
        if buf is None:
            buf = line
            continue
        if buf[-1:] in ",.:;?" or not line[:1].islower():
            out.append(buf)
            buf = line
            continue
        buf = buf + " " + line
    if buf:
        out.append(buf)
    return out


def terms_heading(line):
    letters = [ch for ch in line if ch.isalpha()]
    return bool(letters) and len(line) <= 40 and all(ch.isupper() for ch in letters)


def swaps_for(line):
    swaps = []
    if PHONE in line:
        swaps.append((PHONE, tel(PHONE)))
    if HHS_MAIL in line:
        swaps.append((HHS_MAIL, mailto(HHS_MAIL)))
    if HHS_TEXT in line:
        swaps.append((HHS_TEXT, ext(HHS_HREF, HHS_TEXT)))
    if PRIVACY_PHRASE in line:
        link = shell.link("privacy-policy", "Privacy Policy", DEPTH)
        swaps.append((PRIVACY_PHRASE, "Please review our " + link))
    return tuple(swaps)


def render_blocks(lines, heading):
    parts = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == TOC:
            first = lines[i + 1]
            again = lines.index(first, i + 2)
            items = lines[i + 1:again]
            parts.append(f"<h2>{esc(TOC)}</h2><ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>")
            i = again
            continue
        if heading(line):
            parts.append(f"<h2>{esc(line)}</h2>")
            i += 1
            continue
        if line.endswith(":") and i + 1 < len(lines) and list_item(lines[i + 1], heading):
            parts.append(para(line, swaps_for(line)))
            i += 1
            items = []
            while i < len(lines) and list_item(lines[i], heading):
                items.append(lines[i])
                i += 1
            parts.append("<ul>" + "".join(f"<li>{para(item, swaps_for(item))[3:-4]}</li>" for item in items) + "</ul>")
            continue
        parts.append(para(line, swaps_for(line)))
        i += 1
    return "".join(parts)


def list_item(line, heading):
    if heading(line) or line == TOC:
        return False
    return not line.startswith(LIST_STOP)


def visible(article):
    text = re.sub(r"<a\b[^>]*>|</a>", "", article)
    text = re.sub(r"<[^>]+>", " ", text)
    return squash(html.unescape(text))


def expect(raw, heading, extra_swaps):
    lines = body_after(raw, heading)
    text = squash(" ".join(lines))
    for old, new in extra_swaps:
        if old not in text:
            raise SystemExit("swap source missing: " + old[:80])
        text = text.replace(old, new)
    return text


def check_same(slug, article, expected):
    got = visible(article)
    if got != expected:
        for i, (a, b) in enumerate(zip(got, expected)):
            if a != b:
                raise SystemExit(
                    slug + " diverges at " + str(i) + ": built [" + got[max(0, i - 40):i + 40]
                    + "] archive [" + expected[max(0, i - 40):i + 40] + "]"
                )
        raise SystemExit(slug + " length built " + str(len(got)) + " archive " + str(len(expected)))


def check_common(raw, title):
    require(raw, title, "old title")
    require(raw, CLOSER, "closer")
    require(raw, REQUEST, "request button")
    require(raw, "New Patient Special Offer", "special, which this page leaves off")
    require(raw, OLD_ADDRESS, "old address")
    require(raw, OLD_CITY, "old city")
    require(raw, "Mon 10am - 6pm", "old Monday hours")
    require(raw, "Fri 10am - 6pm", "old Friday hours")
    require(raw, "Sat Closed", "old Saturday")
    require(raw, "Sun Closed", "old Sunday")


def outside_links(main):
    return re.findall(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>', main)


def check_page(slug, h1, page, outside, name_allowed):
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    if "Henderson" in page or "New Patient Special" in page or "$47" in page:
        raise SystemExit("forbidden wording on " + slug)
    if "1263 E Silverado" in page or "Silverado" in page:
        raise SystemExit("old address copied onto " + slug)
    if 'href="/' in page or "evergrowthchiro.com/" in page or "web.archive.org" in page:
        raise SystemExit("root-absolute or live-site link on " + slug)
    if "placeholder=" in page or "Dr. [Last Name]" in page or "DOCTOR*" in page:
        raise SystemExit("placeholder left on " + slug)
    if name_allowed:
        if page.count(NAME) != 1:
            raise SystemExit("name swap count on " + slug)
    elif "Dr. Willie" in page or "Willie So" in page:
        raise SystemExit("name added to " + slug)
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
    for tag in re.findall(r'<a\b[^>]*href="\.\./privacy-policy/"[^>]*>', page):
        if "target" in tag:
            raise SystemExit("privacy policy link opens in a new tab on " + slug)
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
        raise SystemExit("expected booking links on " + slug)


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
    leftover = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        if old in path.read_text():
            leftover.append(str(path.relative_to(ROOT)))
    if leftover:
        raise SystemExit("anchor still in " + ", ".join(leftover))
    home = (ROOT / "index.html").read_text()
    if f'href="{slug}/"' not in home:
        raise SystemExit("home footer was not rewired: " + slug)
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
    if old_cell in row:
        row = row.replace(old_cell, new_cell, 1)
    elif f'href="{slug}/"' not in row:
        raise SystemExit("status cell missing: " + slug + " " + row[:240])
    note_start = row.rfind("<td>")
    if note_start < 0:
        raise SystemExit("note cell missing: " + slug)
    row = row[:note_start] + f"<td>{html.escape(note)}</td>"
    path.write_text(html_text[:start] + row + html_text[end:])
    print("site-map marked", slug)


def stamp(previous):
    digest = hashlib.sha256()
    digest.update((ROOT / "index.html").read_bytes())
    for slug in NOTES:
        digest.update((ROOT / slug / "index.html").read_bytes())
    build_id = digest.hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build_hipaa(raw):
    check_common(raw, "HIPAA Privacy Practices - Chiropractor Henderson NV | New Patient Experience")
    require(raw, OLD_LINE, "notice address")
    require(raw, "DOCTOR* D.C. - (702) 389-5009", "placeholder name")
    require(raw, HHS_MAIL, "hhs mail")
    require(raw, HHS_TEXT, "hhs form")
    require(raw, TOC, "table of contents")
    lines = join_lines(body_after(raw, "HIPAA Privacy Practices"), HIPAA_HEADINGS.__contains__)
    lines = [NEW_LINE if line == OLD_LINE else line.replace(NAME_TOKEN, NAME) for line in lines]
    article = render_blocks(lines, HIPAA_HEADINGS.__contains__)
    expected = expect(raw, "HIPAA Privacy Practices", ((OLD_LINE, NEW_LINE), (NAME_TOKEN, NAME)))
    check_same("hipaa-privacy-practices", article, expected)
    return article


def build_privacy(raw):
    check_common(raw, "Privacy Policy - Chiropractor Henderson NV | New Patient Experience")
    require(raw, "Privacy Notice", "privacy notice")
    require(raw, "This Privacy Policy was last updated on May 2025.", "updated line")
    body = raw.split("Privacy Policy\n", 1)[1].split("New Patient Special Offer", 1)[0]
    if "Henderson" in body or "1263" in body or "DOCTOR" in body:
        raise SystemExit("privacy body gained a city, address, or name")
    lines = join_lines(body_after(raw, "Privacy Policy"), PRIVACY_HEADINGS.__contains__)
    article = render_blocks(lines, PRIVACY_HEADINGS.__contains__)
    check_same("privacy-policy", article, expect(raw, "Privacy Policy", ()))
    return article


def build_terms(raw):
    check_common(raw, "Terms of Service - Chiropractor Henderson NV | New Patient Experience")
    require(raw, GROW, "grow gonstead phrase")
    require(raw, PRIVACY_PHRASE, "old privacy url")
    require(raw, "&quot;Linked Sites&quot;", "linked sites quotes")
    require(raw, "misrepresents the your identity", "kept typo")
    if raw.count(GROW) != 2:
        raise SystemExit("archive Grow Gonstead phrase count")
    lines = join_lines(body_after(raw, "Terms of Service/Terms and Conditions"), terms_heading)
    lines = [line.replace("&quot;", '"') for line in lines]
    article = render_blocks(lines, terms_heading)
    expected = expect(
        raw,
        "Terms of Service/Terms and Conditions",
        (("&quot;", '"'), (PRIVACY_PHRASE, PRIVACY_VISIBLE)),
    )
    check_same("terms-of-service", article, expected)
    if article.count(GROW) != 2:
        raise SystemExit("terms dropped the Grow Gonstead phrase")
    if 'href="../privacy-policy/"' not in article or "evergrowthchiro.com/" in article:
        raise SystemExit("privacy link was not internalized")
    return article


def build():
    previous = (ROOT / "build-id.txt").read_text().strip()
    specs = (
        (
            "hipaa-privacy-practices",
            "HIPAA Privacy Practices",
            "Notice of privacy practices for Evergrowth Chiropractic in Las Vegas.",
            "hipaa-privacy-practices_20260511.txt",
            build_hipaa,
            [HHS_HREF],
            True,
        ),
        (
            "privacy-policy",
            "Privacy Policy",
            "Privacy notice for this website.",
            "privacy-policy_20260606.txt",
            build_privacy,
            [],
            False,
        ),
        (
            "terms-of-service",
            "Terms of Service/Terms and Conditions",
            "Terms of service for this website.",
            "terms-of-service_20260606.txt",
            build_terms,
            [],
            False,
        ),
    )
    written = []
    for slug, h1, description, filename, builder, outside, name_allowed in specs:
        raw = (OLD / filename).read_text()
        article = builder(raw)
        page = article_page(h1, description, article)
        check_page(slug, h1, page, outside, name_allowed)
        if slug == "terms-of-service":
            if page.count(GROW) != 2:
                raise SystemExit("Grow Gonstead phrase was edited")
            if "Copyright &copy; 2026 Evergrowth Chiropractic" not in page:
                raise SystemExit("footer copyright changed")
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
        if f"site-map.html#{slug}" in home:
            raise SystemExit("home still has the site map anchor: " + slug)
    return stamp(previous)


if __name__ == "__main__":
    build()
