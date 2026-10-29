"""Injury and extremity batch C: disc injury, personal injury, arm and leg pain, carpal tunnel, shoulder pain.

Copy is the archive text named in the row. Allowed swaps only. Reviews stay
word for word, including Dr Will. Heroes are the stock files named in the row.
Personal injury has no matching stock, so that page is left plain.
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
    "Chrome: archive footer hours Mon/Wed/Thu 10am-1pm and 3pm-6pm, Tue 3pm-6pm, "
    "Fri 10am-1pm, Sat 10am-1pm, Sun closed, replaced by Mon, Wed, Thu 10am to 1pm "
    "and 3pm to 6pm; Tue 3pm to 6pm; Fri appointments only; Sat and Sun closed"
)
NO_NAME = "No name swap. Reviews keep Dr Will and Dr. Will. New Patient Special omitted."

H1S = {
    "disc-injury": "Disc Injury Relief",
    "personal-injury": "Chiropractic for Personal Injury",
    "arm-leg-pain": "Arm & Leg Pain Relief",
    "carpal-tunnel": "Carpal Tunnel Relief",
    "shoulder-pain": "Shoulder Pain Relief",
}

PAGES = [
    {
        "slug": "disc-injury",
        "source": "disc-injury_20260417.txt",
        "catalog": CATALOG / "Conditions" / "disc-injury.webp",
        "image_name": "stock-condition-disc-injury.webp",
        "image_alt": "Man in a maroon shirt standing by a blue sofa with both hands on his lower back",
        "crumb": "Disc Injury",
        "label": "Disc Injury",
        "map_label": "Disc Injury",
        "group": "Injuries",
        "description": "Chiropractic care for disc injuries in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Disc Injury Relief - Chiropractor Henderson NV | New Patient Experience",
        "closing": "If you're grappling with a disc injury",
        "old_note": "Hero: stock Catalog/Conditions/disc-injury.webp<br><small>Stock image: Catalog/Conditions/disc-injury.webp</small>",
        "new_note": "BUILT. Hero is stock.<br><small>Stock image: Catalog/Conditions/disc-injury.webp</small>",
    },
    {
        "slug": "personal-injury",
        "source": "personal-injury_20260417.txt",
        "catalog": None,
        "image_name": None,
        "image_alt": "",
        "crumb": "Personal Injury",
        "label": "Personal Injury",
        "map_label": "Personal Injury",
        "group": "Injuries",
        "description": "Chiropractic care for personal injury in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Chiropractic for Personal Injury - Chiropractor Henderson NV | New Patient Experience",
        "closing": "full",
        "old_note": "No matching stock photo. Old image was a lady with an injury (not archived).",
        "new_note": "BUILT. No hero image. No matching stock photo. Old image was a lady with an injury (not archived).",
    },
    {
        "slug": "arm-leg-pain",
        "source": "arm-leg-pain_20260417.txt",
        "catalog": CATALOG / "Conditions" / "extremity-pain.webp",
        "image_name": "stock-condition-extremity-pain.webp",
        "image_alt": "Man in a maroon shirt holding his forearm",
        "crumb": "Arm & Leg Pain",
        "label": "Arm & Leg Pain",
        "map_label": "Arm &amp; Leg Pain",
        "group": "Extremities",
        "description": "Chiropractic care for arm and leg pain in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Arm & Leg Pain Relief - Chiropractor Henderson NV | New Patient Experience",
        "closing": "If you're experiencing arm or leg pain",
        "old_note": "Hero: stock Catalog/Conditions/extremity-pain.webp<br><small>Stock image: Catalog/Conditions/extremity-pain.webp</small>",
        "new_note": "BUILT. Hero is stock.<br><small>Stock image: Catalog/Conditions/extremity-pain.webp</small>",
    },
    {
        "slug": "carpal-tunnel",
        "source": "carpal-tunnel_20260314.txt",
        "catalog": CATALOG / "Conditions" / "carpal-tunnel.webp",
        "image_name": "stock-condition-carpal-tunnel.webp",
        "image_alt": "Person at a laptop holding one wrist",
        "crumb": "Carpal Tunnel",
        "label": "Carpal Tunnel",
        "map_label": "Carpal Tunnel",
        "group": "Extremities",
        "description": "Chiropractic care for carpal tunnel in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Carpal Tunnel Relief - Chiropractor Henderson NV | New Patient Experience",
        "closing": "full",
        "old_note": "Hero: stock Catalog/Conditions/carpal-tunnel.webp<br><small>Stock image: Catalog/Conditions/carpal-tunnel.webp</small>",
        "new_note": "BUILT. Hero is stock.<br><small>Stock image: Catalog/Conditions/carpal-tunnel.webp</small>",
    },
    {
        "slug": "shoulder-pain",
        "source": "shoulder-pain_20260417.txt",
        "catalog": CATALOG / "Conditions" / "shoulder-pain.webp",
        "image_name": "stock-condition-shoulder-pain.webp",
        "image_alt": "Woman holding a blue gel pack on her shoulder",
        "crumb": "Shoulder Pain",
        "label": "Shoulder Pain",
        "map_label": "Shoulder Pain",
        "group": "Extremities",
        "description": "Chiropractic care for shoulder pain in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Shoulder Pain Relief - Chiropractor Henderson NV | New Patient Experience",
        "closing": "full",
        "old_note": "Hero: stock Catalog/Conditions/shoulder-pain.webp<br><small>Stock image: Catalog/Conditions/shoulder-pain.webp</small>",
        "new_note": "BUILT. Hero is stock.<br><small>Stock image: Catalog/Conditions/shoulder-pain.webp</small>",
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
    raw = path.read_text(errors="ignore")
    start = re.search(r"<h1\b[^>]*>", raw, re.I)
    if not start:
        raise SystemExit(f"no h1 in {path}")
    chunk = raw[start.start() :]
    stop = chunk.find("Our testimonial")
    chunk = chunk[:stop]
    kinds = []
    for match in re.finditer(r"<(h1|h3|p|ul|ol)\b[^>]*>(.*?)</\1>", chunk, re.I | re.S):
        kind = match.group(1).lower()
        inner = match.group(2)
        if kind in ("ul", "ol"):
            count = len(re.findall(r"<li\b", inner, re.I))
            kinds.append((kind, count))
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
            raise SystemExit(f"{spec['slug']} ran out of text at {kind} (have {lines[cursor:]})")
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
        elif kind in ("ul", "ol"):
            blocks.append((kind, swapped))
        else:
            raise SystemExit(f"{spec['slug']} unknown kind {kind}")
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
    if not spec["catalog"]:
        return None, None
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
    if shell.has_unexpected_social(page):
        problems.append("social link leaked")
    book = page.count('href="../book-appointment/"')
    if book < 4:
        problems.append(f"expected book links in header, article, sidebar, footer; found {book}")
    if spec["image_name"]:
        if spec["image_name"] not in page:
            problems.append("missing stock hero")
    elif "<div class=\"a-img\">" in page:
        problems.append("plain page rendered a hero")
    for line in lines:
        swapped = line.replace("Henderson, NV", "Las Vegas, NV").replace("Henderson NV", "Las Vegas NV").replace("Henderson", "Las Vegas")
        escaped = html.escape(swapped, quote=False)
        if escaped in page:
            continue
        parts = [html.escape(part.strip(), quote=False) for part in swapped.split(". ") if part.strip()]
        if len(parts) < 2 or any(part not in page for part in parts):
            problems.append(f"missing copy: {swapped[:80]}")
    for name in ("DNoria R.", "Emily E.", "Laurie W.", "Andrea V.", "So happy I am now a Patient!!"):
        if name not in page:
            problems.append(f"missing review: {name}")
    if "—" in spec["description"] or "—" in spec["image_alt"]:
        problems.append("em dash in text we wrote")
    for word in ("treat", "treatment", "treating", "treated"):
        if re.search(rf"\b{word}\b", spec["description"], re.I) or re.search(rf"\b{word}\b", spec["image_alt"], re.I):
            problems.append(f"text we wrote uses {word}")
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
    if spec["catalog"]:
        logs.append(
            f"{spec['slug']}: image stock {spec['catalog'].relative_to(CATALOG)} as assets/img/{spec['image_name']} ({width}x{height}), not a client photo"
        )
    else:
        logs.append(f"{spec['slug']}: no hero image. No matching stock. Left plain.")
    pre = shell.prefix(DEPTH)
    page = condition.render_condition(
        depth=DEPTH,
        title=title,
        description=spec["description"],
        crumbs=[
            ("Home", "index"),
            ("What We Do", None),
            (spec["group"], None),
            (spec["crumb"], None),
        ],
        h1=h1,
        sub=sub,
        image=(f"{pre}assets/img/{spec['image_name']}" if spec["image_name"] else None),
        image_alt=spec["image_alt"],
        image_w=width or 0,
        image_h=height or 0,
        blocks=blocks,
        closing=closing,
        group_title=spec["group"],
        group_links=condition.nav_group(spec["group"]),
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
        ('site-map.html#disc-injury"', 'disc-injury/"'),
        ('site-map.html#personal-injury"', 'personal-injury/"'),
        ('site-map.html#arm-leg-pain"', 'arm-leg-pain/"'),
        ('site-map.html#carpal-tunnel"', 'carpal-tunnel/"'),
        ('site-map.html#shoulder-pain"', 'shoulder-pain/"'),
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
    for slug in ("disc-injury", "personal-injury", "arm-leg-pain", "carpal-tunnel", "shoulder-pain"):
        if f'href="{slug}/"' not in index and f'href="{slug}/"' not in index:
            if f'site-map.html#{slug}"' in index:
                raise SystemExit(f"{slug} anchor still in home")
    if 'href="disc-injury/"' not in index:
        raise SystemExit("home nav was not rewired for disc-injury")


def mark_site_map():
    path = ROOT / "site-map.html"
    html_text = path.read_text()
    for spec in PAGES:
        slug = spec["slug"]
        label = spec["map_label"]
        old_cell = f'<tr id="{slug}"><td><b>{label}</b></td><td>planned (not built)</td>'
        new_cell = f'<tr id="{slug}"><td><b>{label}</b></td><td><a href="{slug}/">{slug}/</a> (built)</td>'
        if old_cell in html_text:
            html_text = html_text.replace(old_cell, new_cell, 1)
        elif new_cell not in html_text:
            raise SystemExit(f"site-map row missing for {slug}")
        if spec["old_note"] in html_text:
            html_text = html_text.replace(spec["old_note"], spec["new_note"], 1)
        elif spec["new_note"] not in html_text:
            raise SystemExit(f"site-map note missing for {slug}")
    path.write_text(html_text)
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
    log_path = Path("/tmp/egc-r06-swaps.txt")
    log_path.write_text("\n".join(logs) + f"\nbuild-id {build_id}\n")
    print("swaps", len(logs))
    for line in logs:
        print("swap:", line)


if __name__ == "__main__":
    build()
