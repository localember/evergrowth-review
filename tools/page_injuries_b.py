"""Injury condition batch B: accident recovery, auto injury, whiplash, work injury.

Copy is the archive text named in the row. Allowed swaps only. Reviews stay
word for word, including Dr Will. Heroes are the stock files named in the row.
"""
import hashlib
import html
import re
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import condition
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
SRC = Path("/tmp/evergrowth-src/old/pages")
CATALOG = Path("/Users/johnowens/localember/tools/bd-generator/assets/stock/Catalog")

CHROME_ADDRESS = (
    "Chrome: old address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 "
    "replaced by 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123"
)
CHROME_HOURS = (
    "Chrome: old weekday hours Mon to Fri 10am-6pm, Sat and Sun closed, replaced by "
    "Mon, Wed, Thu 10am to 1pm and 3pm to 6pm; Tue 3pm to 6pm; Fri appointments only; "
    "Sat and Sun closed"
)
NO_NAME = "No name swap. Reviews keep Dr Will and Dr. Will. New Patient Special omitted."

H1S = {
    "who-we-help-accident-injury-recovery": "Accident Injury Recovery",
    "car-accident": "Auto Injury Relief",
    "whiplash": "Help With Whiplash Injuries",
    "work-injury": "Care For Work Injuries",
}

PAGES = [
    {
        "slug": "who-we-help-accident-injury-recovery",
        "source": "who-we-help-accident-injury-recovery_20260511.txt",
        "catalog": CATALOG / "Services" / "Auto Accident Care.webp",
        "image_name": "stock-auto-accident-care.webp",
        "image_alt": "Woman in a car holding the side of her neck",
        "crumb": "Accident Injury",
        "label": "Accident Injury",
        "description": "Chiropractic care for accident and injury recovery in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Accident Injury Recovery - Chiropractor Henderson NV | New Patient Experience",
        "closing": "full",
        "old_note": "Hero: stock Catalog/Services/Auto Accident Care.webp<br><small>Stock image: Catalog/Services/Auto Accident Care.webp</small>",
        "new_note": "BUILT. Hero is stock.<br><small>Stock image: Catalog/Services/Auto Accident Care.webp</small>",
    },
    {
        "slug": "car-accident",
        "source": "car-accident_20260606.txt",
        "catalog": CATALOG / "Conditions" / "whiplash.webp",
        "image_name": "stock-condition-whiplash.webp",
        "image_alt": "Man holding his neck between two damaged cars",
        "crumb": "Auto Injury",
        "label": "Auto Injury",
        "description": "Chiropractic care for auto injuries in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Auto Injury Relief - Chiropractor Henderson NV | New Patient Experience",
        "closing": "full",
        "old_note": "Hero: stock Catalog/Conditions/whiplash.webp (car scene)<br><small>Stock image: Catalog/Conditions/whiplash.webp</small>",
        "new_note": "BUILT. Hero is stock.<br><small>Stock image: Catalog/Conditions/whiplash.webp (car scene)</small>",
    },
    {
        "slug": "whiplash",
        "source": "whiplash_20260606.txt",
        "catalog": CATALOG / "Conditions" / "whiplash.webp",
        "image_name": "stock-condition-whiplash.webp",
        "image_alt": "Man holding his neck between two damaged cars",
        "crumb": "Whiplash",
        "label": "Whiplash",
        "description": "Chiropractic care for whiplash in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Help With Whiplash Injuries - Chiropractor Henderson NV | New Patient Experience",
        "closing": "Reach out to our team at Evergrowth Chiropractic",
        "old_note": "Hero: stock Catalog/Conditions/whiplash.webp<br><small>Stock image: Catalog/Conditions/whiplash.webp</small>",
        "new_note": "BUILT. Hero is stock.<br><small>Stock image: Catalog/Conditions/whiplash.webp</small>",
    },
    {
        "slug": "work-injury",
        "source": "work-injury_20260606.txt",
        "catalog": CATALOG / "Conditions" / "work-injury.webp",
        "image_name": "stock-condition-work-injury.webp",
        "image_alt": "Warehouse worker in a safety vest holding his lower back",
        "crumb": "Work Injury",
        "label": "Work Injury",
        "description": "Chiropractic care for work injuries in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Care For Work Injuries - Chiropractor Henderson NV | New Patient Experience",
        "closing": "hesitate to reach out to our team at Evergrowth Chiropractic",
        "old_note": "Hero: stock Catalog/Conditions/work-injury.webp<br><small>Stock image: Catalog/Conditions/work-injury.webp</small>",
        "new_note": "BUILT. Hero is stock.<br><small>Stock image: Catalog/Conditions/work-injury.webp</small>",
    },
]


def image_size(path):
    data = path.read_bytes()
    if data[0:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise SystemExit(f"not a webp: {path}")
    kind = data[12:16]
    if kind == b"VP8X":
        return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
    if kind == b"VP8 ":
        sig = data.find(b"\x9d\x01\x2a", 20, 60)
        if sig < 0:
            raise SystemExit(f"no VP8 size in {path}")
        width = int.from_bytes(data[sig + 3 : sig + 5], "little") & 0x3FFF
        height = int.from_bytes(data[sig + 5 : sig + 7], "little") & 0x3FFF
        return width, height
    if kind == b"VP8L":
        b0, b1, b2, b3 = data[21:25]
        width = 1 + (((b1 & 0x3F) << 8) | b0)
        height = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
        return width, height
    raise SystemExit(f"unknown webp {kind!r} in {path}")


def txt_body(path, h1):
    lines = path.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == h1 and i > 40:
            start = i
            break
    if start is None:
        raise SystemExit(f"h1 not found in {path}")
    body = []
    for line in lines[start:]:
        if line.strip() == "Our testimonial":
            break
        if line.strip():
            body.append(line.strip())
    return body


def html_kinds(path):
    html = path.read_text(errors="ignore")
    start = re.search(r"<h1\b[^>]*>", html, re.I)
    if not start:
        raise SystemExit(f"no h1 in {path}")
    chunk = html[start.start() :]
    stop = chunk.find("Our testimonial")
    chunk = chunk[:stop]
    kinds = []
    for match in re.finditer(r"<(h1|h3|p|ul)\b[^>]*>(.*?)</\1>", chunk, re.I | re.S):
        kind = match.group(1).lower()
        inner = match.group(2)
        if kind == "ul":
            count = len(re.findall(r"<li\b", inner, re.I))
            kinds.append(("ul", count))
        elif kind == "h3" and re.search(r"<br\b", inner, re.I):
            parts = [part for part in re.split(r"<br\s*/?>", inner, flags=re.I) if re.sub(r"<[^>]+>", "", part).strip()]
            kinds.append(("h3br", len(parts)))
        else:
            kinds.append((kind, 1))
    return kinds


def assemble(spec, logs):
    txt_path = SRC / spec["source"]
    html_path = SRC / spec["source"].replace(".txt", ".html")
    lines = txt_body(txt_path, H1S[spec["slug"]])
    kinds = html_kinds(html_path)
    cursor = 0
    pieces = []
    for kind, count in kinds:
        chunk = lines[cursor : cursor + count]
        if len(chunk) != count:
            raise SystemExit(f"{spec['slug']} ran out of text at {kind}")
        cursor += count
        pieces.append((kind, chunk))
    if cursor != len(lines):
        raise SystemExit(f"{spec['slug']} unused text lines: {lines[cursor:]}")

    h1 = None
    sub_lines = None
    blocks = []
    for kind, chunk in pieces:
        swapped = [swap_text(line, spec["slug"], logs) for line in chunk]
        if kind == "h1":
            h1 = swapped[0]
        elif kind in ("h3", "h3br") and sub_lines is None:
            sub_lines = swapped
        elif kind in ("h3", "h3br"):
            if len(swapped) != 1:
                raise SystemExit(f"{spec['slug']} extra heading lines {swapped}")
            blocks.append(("h2", swapped[0]))
        elif kind == "p":
            blocks.append(("p", swapped[0]))
        else:
            blocks.append(("ul", swapped))
    if h1 is None or not sub_lines:
        raise SystemExit(f"{spec['slug']} missing title")

    if spec["closing"] == "full":
        if not blocks or blocks[-1][0] != "p":
            raise SystemExit(f"{spec['slug']} last block is not the closing paragraph")
        closing = blocks.pop()[1]
    else:
        if not blocks or blocks[-1][0] != "p":
            raise SystemExit(f"{spec['slug']} last block is not a paragraph")
        paragraph = blocks.pop()[1]
        marker = spec["closing"]
        at = paragraph.find(marker)
        if at < 0:
            raise SystemExit(f"{spec['slug']} closing marker missing: {marker}")
        # Keep the sentence that contains the marker, from the previous period.
        sentence_at = paragraph.rfind(". ", 0, at)
        if sentence_at < 0:
            lead, closing = "", paragraph[at:].strip()
        else:
            lead = paragraph[: sentence_at + 1].strip()
            closing = paragraph[sentence_at + 2 :].strip()
        if lead:
            blocks.append(("p", lead))
        if not closing:
            raise SystemExit(f"{spec['slug']} empty closing")
    return h1, "\n".join(sub_lines), blocks, closing, lines


def swap_text(text, where, logs):
    patterns = [
        ("Henderson, NV", "Las Vegas, NV"),
        ("Henderson NV", "Las Vegas NV"),
        ("Henderson", "Las Vegas"),
    ]
    out = text
    for old, new in patterns:
        start = 0
        while True:
            found = out.find(old, start)
            if found < 0:
                break
            ctx = out[max(0, found - 36) : found + len(old) + 36].replace("\n", " ")
            logs.append(f"{where}: '{old}' to '{new}' in \"{ctx}\"")
            out = out[:found] + new + out[found + len(old) :]
            start = found + len(new)
    return out


def place_image(spec):
    dest = ROOT / "assets" / "img" / spec["image_name"]
    src = spec["catalog"]
    if not src.is_file():
        raise SystemExit(f"missing stock image {src}")
    if not dest.is_file() or dest.read_bytes() != src.read_bytes():
        shutil.copyfile(src, dest)
    return image_size(dest)


def check(spec, page, lines):
    problems = []
    if "Henderson" in page:
        problems.append("Henderson still present")
    if "evergrowthchiro.com/book" in page.lower() or "https://evergrowthchiro.com" in page.lower() or "https://www.evergrowthchiro.com" in page.lower():
        problems.append("link points at the client site")
    for match in re.finditer(r"evergrowthchiro\.com", page, re.I):
        prefix = page[max(0, match.start() - 24) : match.start()]
        if not prefix.endswith("Info@") and not prefix.endswith("mailto:Info@"):
            problems.append("client domain outside the email")
            break
    if 'href="/' in page or 'src="/' in page:
        problems.append("root-absolute path")
    if "localhost" in page or "127.0.0.1" in page:
        problems.append("localhost leak")
    if "noindex" not in page:
        problems.append("missing noindex")
    if 'target="' in page:
        problems.append("target attribute on a page with no outside link")
    if "New Patient Special" in page or "$47" in page:
        problems.append("special offer leaked")
    if "Dr. [Last Name]" in page or "New Patient Experience" in page:
        problems.append("old title or placeholder leaked")
    if "1263 E Silverado" in page or "Grow Gonstead" in page:
        problems.append("old address or old copyright leaked")
    if "20250814_131251" in page or "20251020_162305" in page:
        problems.append("unconfirmed photo referenced")
    if "facebook.com" in page or "instagram.com" in page or "youtube.com" in page:
        problems.append("social link leaked")
    book = page.count('href="../book-appointment/"')
    if book < 4:
        problems.append(f"expected book links in header, article, sidebar, footer; found {book}")
    if spec["image_name"] not in page:
        problems.append("missing stock hero")
    for line in lines:
        swapped = line.replace("Henderson, NV", "Las Vegas, NV").replace("Henderson NV", "Las Vegas NV").replace("Henderson", "Las Vegas")
        # The page stores the same words with HTML escapes (&amp;).
        escaped = html.escape(swapped, quote=False)
        if escaped in page:
            continue
        # The closing sentence is moved into the call-to-action, so a source
        # paragraph can be split across the article and that box.
        parts = [html.escape(part.strip(), quote=False) for part in swapped.split(". ") if part.strip()]
        if len(parts) < 2 or any(part not in page for part in parts):
            problems.append(f"missing copy: {swapped[:80]}")
    for name in ("DNoria R.", "Emily E.", "Laurie W.", "Andrea V.", "So happy I am now a Patient!!"):
        if name not in page:
            problems.append(f"missing review: {name}")
    if "—" in spec["description"] or "—" in spec["image_alt"]:
        problems.append("em dash in text we wrote")
    for word in ("treat", "treatment", "treating", "treated"):
        if re.search(rf"\b{word}\b", spec["description"], re.I):
            problems.append(f"description uses {word}")
    if problems:
        raise SystemExit(spec["slug"] + " check failed: " + "; ".join(problems))


def render(spec, logs):
    width, height = place_image(spec)
    h1, sub, blocks, closing, lines = assemble(spec, logs)
    title = f"{h1} - Chiropractor Las Vegas NV | Evergrowth Chiropractic"
    logs.append(f"{spec['slug']}: title '{spec['old_title']}' to '{title}'")
    logs.append(f"{spec['slug']}: {CHROME_ADDRESS}")
    logs.append(f"{spec['slug']}: {CHROME_HOURS}")
    logs.append(f"{spec['slug']}: {NO_NAME}")
    logs.append(f"{spec['slug']}: image stock {spec['catalog'].relative_to(CATALOG)} as assets/img/{spec['image_name']} ({width}x{height}), not a client photo")
    pre = shell.prefix(DEPTH)
    page = condition.render_condition(
        depth=DEPTH,
        title=title,
        description=spec["description"],
        crumbs=[
            ("Home", "index"),
            ("What We Do", None),
            ("Injuries", None),
            (spec["crumb"], None),
        ],
        h1=h1,
        sub=sub,
        image=f"{pre}assets/img/{spec['image_name']}",
        image_alt=spec["image_alt"],
        image_w=width,
        image_h=height,
        blocks=blocks,
        closing=closing,
        group_title="Injuries",
        group_links=condition.nav_group("Injuries"),
    )
    check(spec, page, lines)
    dest = ROOT / spec["slug"] / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()[:12]
    print(dest)
    print("page-sha", digest)
    return dest


def rewire_nav():
    pairs = (
        ('site-map.html#who-we-help-accident-injury-recovery"', 'who-we-help-accident-injury-recovery/"'),
        ('site-map.html#car-accident"', 'car-accident/"'),
        ('site-map.html#whiplash"', 'whiplash/"'),
        ('site-map.html#work-injury"', 'work-injury/"'),
    )
    changed = []
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = path.read_text()
        new = text
        for old, repl in pairs:
            new = new.replace(old, repl)
        if new != text:
            path.write_text(new)
            changed.append(str(path.relative_to(ROOT)))
    print("rewired", ", ".join(changed) if changed else "none")
    index = (ROOT / "index.html").read_text()
    if 'href="who-we-help-accident-injury-recovery/"' not in index:
        raise SystemExit("home nav was not rewired")
    if 'href="car-accident/"' not in index or 'href="whiplash/"' not in index or 'href="work-injury/"' not in index:
        raise SystemExit("home nav missing an injury link")
    if "site-map.html#car-accident-tips" in index.replace("site-map.html#car-accident\"", ""):
        pass
    if 'site-map.html#car-accident"' in index:
        raise SystemExit("car-accident anchor still in home")


def mark_site_map():
    path = ROOT / "site-map.html"
    html = path.read_text()
    for spec in PAGES:
        slug = spec["slug"]
        label = spec["label"]
        old_cell = f'<tr id="{slug}"><td><b>{label}</b></td><td>planned (not built)</td>'
        new_cell = f'<tr id="{slug}"><td><b>{label}</b></td><td><a href="{slug}/">{slug}/</a> (built)</td>'
        if old_cell in html:
            html = html.replace(old_cell, new_cell, 1)
        elif new_cell not in html:
            raise SystemExit(f"site-map row missing for {slug}")
        if spec["old_note"] in html:
            html = html.replace(spec["old_note"], spec["new_note"], 1)
        elif spec["new_note"] not in html:
            raise SystemExit(f"site-map note missing for {slug}")
    path.write_text(html)
    print("site-map marked built")


def stamp():
    index = ROOT / "index.html"
    build_id = hashlib.sha256(index.read_bytes()).hexdigest()[:12]
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    logs = []
    for spec in PAGES:
        render(spec, logs)
    rewire_nav()
    mark_site_map()
    build_id = stamp()
    log_path = Path("/tmp/egc-r05-swaps.txt")
    log_path.write_text("\n".join(logs) + f"\nbuild-id {build_id}\n")
    print("swaps", len(logs))
    for line in logs:
        print("swap:", line)


if __name__ == "__main__":
    build()
