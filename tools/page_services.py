"""Services batch: adjustments, exercises, education, CLA Insight.

Copy is the archive text named in the row. Allowed swaps only. Reviews stay
word for word, including Dr Will. Chiropractic Adjustments reuses the real
adjusting-room photo already on Home. The other two heroes are catalog stock.
CLA Insight has no device photo, so that page has no hero.
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

NEW_HOURS = (
    "Mon, Wed, Thu 10am to 1pm and 3pm to 6pm; Tue 3pm to 6pm; "
    "Fri appointments only; Sat and Sun closed"
)
NEW_ADDRESS = "9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123"
NO_NAME = "No name swap. Reviews keep Dr Will and Dr. Will. New Patient Special omitted."

PAGES = [
    {
        "slug": "chiropractic-adjustments",
        "source": "chiropractic-adjustments_20260417.txt",
        "image_kind": "real",
        "image_name": "office-hallway-1200.jpg",
        "image_alt": "Hallway with teal barn doors leading to the front desk at Evergrowth Chiropractic",
        "crumb": "Chiropractic Adjustments",
        "map_label": "Chiropractic Adjustments",
        "group": "Services",
        "description": "Chiropractic adjustments in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Chiropractic Adjustments - Chiropractor Henderson NV | New Patient Experience",
        "old_row": (
            '<tr id="chiropractic-adjustments"><td><b>Chiropractic Adjustments</b></td>'
            '<td>planned (not built)</td><td><code>/chiropractic-adjustments/</code></td>'
            '<td><span class="tag ready">content ready</span></td>'
            "<td>The adjusting room photo (client) fits here.</td></tr>"
        ),
        "new_row": (
            '<tr id="chiropractic-adjustments"><td><b>Chiropractic Adjustments</b></td>'
            '<td><a href="chiropractic-adjustments/">chiropractic-adjustments/</a> (built)</td>'
            "<td><code>/chiropractic-adjustments/</code></td>"
            '<td><span class="tag ready">content ready</span></td>'
            "<td>BUILT. Hero is the adjusting room (client photo 20250814_130730.jpg, the same file as Home). Confirm it shows the Las Vegas office.</td></tr>"
        ),
    },
    {
        "slug": "therapeutic-exercises",
        "source": "therapeutic-exercises_20260417.txt",
        "image_kind": "stock",
        "catalog": CATALOG / "Services" / "Physical Rehabilitation.webp",
        "image_name": "stock-service-therapeutic-exercises.webp",
        "image_alt": "Person extending one arm while a hand rests on the shoulder",
        "crumb": "Therapeutic Exercises",
        "map_label": "Therapeutic Exercises",
        "group": "Services",
        "description": "Therapeutic exercises in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Therapeutic Exercises - Chiropractor Henderson NV | New Patient Experience",
        "old_row": (
            '<tr id="therapeutic-exercises"><td><b>Therapeutic Exercises</b></td>'
            '<td>planned (not built)</td><td><code>/therapeutic-exercises/</code></td>'
            '<td><span class="tag ready">content ready</span></td><td></td></tr>'
        ),
        "new_row": (
            '<tr id="therapeutic-exercises"><td><b>Therapeutic Exercises</b></td>'
            '<td><a href="therapeutic-exercises/">therapeutic-exercises/</a> (built)</td>'
            "<td><code>/therapeutic-exercises/</code></td>"
            '<td><span class="tag ready">content ready</span></td>'
            "<td>BUILT. Hero is stock.<br><small>Stock image: Catalog/Services/Physical Rehabilitation.webp</small></td></tr>"
        ),
    },
    {
        "slug": "education-healthy-choices",
        "source": "education-healthy-choices_20260417.txt",
        "image_kind": "stock",
        "catalog": CATALOG / "Services" / "nutrition.webp",
        "image_name": "stock-service-nutrition.webp",
        "image_alt": "Salmon, greens, nuts, and other foods arranged on a table",
        "crumb": "Education For Healthy Choices",
        "map_label": "Education For Healthy Choices",
        "group": "Services",
        "description": "Education for healthy choices in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "Education For Healthy Choices - Chiropractor Henderson NV | New Patient Experience",
        "old_row": (
            '<tr id="education-healthy-choices"><td><b>Education For Healthy Choices</b></td>'
            '<td>planned (not built)</td><td><code>/education-healthy-choices/</code></td>'
            '<td><span class="tag ready">content ready</span></td><td></td></tr>'
        ),
        "new_row": (
            '<tr id="education-healthy-choices"><td><b>Education For Healthy Choices</b></td>'
            '<td><a href="education-healthy-choices/">education-healthy-choices/</a> (built)</td>'
            "<td><code>/education-healthy-choices/</code></td>"
            '<td><span class="tag ready">content ready</span></td>'
            "<td>BUILT. Hero is stock.<br><small>Stock image: Catalog/Services/nutrition.webp</small></td></tr>"
        ),
    },
    {
        "slug": "cla-insight-thermography",
        "source": "cla-insight-thermography_20260511.txt",
        "image_kind": "missing",
        "image_name": None,
        "image_alt": "",
        "crumb": "CLA Insight Thermography",
        "map_label": "CLA Insight Thermography",
        "group": "Services",
        "description": "CLA Insight thermography in Las Vegas, NV at Evergrowth Chiropractic.",
        "old_title": "CLA Insight Thermography - Chiropractor Henderson NV | New Patient Experience",
        "old_row": (
            '<tr id="cla-insight-thermography"><td><b>CLA Insight Thermography</b></td>'
            '<td>planned (not built)</td><td><code>/cla-insight-thermography/</code></td>'
            '<td><span class="tag image">image missing</span></td>'
            "<td>Need to confirm the clinic still offers CLA Insight thermography at the new office, and a photo of the device.</td></tr>"
        ),
        "new_row": (
            '<tr id="cla-insight-thermography"><td><b>CLA Insight Thermography</b></td>'
            '<td><a href="cla-insight-thermography/">cla-insight-thermography/</a> (built)</td>'
            "<td><code>/cla-insight-thermography/</code></td>"
            '<td><span class="tag image">image missing</span></td>'
            "<td>BUILT. No hero image. Still missing a photo of the CLA Insight device, and confirmation the clinic offers it at the new office.</td></tr>"
        ),
    },
]


def norm(text):
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def text_of(fragment):
    fragment = re.sub(r"<br\s*/?>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return norm(fragment)


def html_blocks(path):
    raw = path.read_text(errors="ignore")
    start = re.search(r"<h1\b", raw, re.I)
    if not start:
        raise SystemExit(f"no h1 in {path}")
    chunk = raw[start.start():]
    chunk = chunk[: chunk.find("Our testimonial")]
    blocks = []
    for match in re.finditer(r"<(h1|h3|p|ul|ol)\b[^>]*>(.*?)</\1>", chunk, re.I | re.S):
        kind = match.group(1).lower()
        inner = match.group(2)
        if kind in ("ul", "ol"):
            items = [text_of(li) for li in re.findall(r"<li\b[^>]*>(.*?)</li>", inner, re.I | re.S)]
            blocks.append((kind, items))
        else:
            blocks.append((kind, text_of(inner)))
    return blocks


def txt_lines(path):
    lines = [line.strip() for line in path.read_text().splitlines()]
    marks = [i for i, line in enumerate(lines) if line == "New Patient Special"]
    if len(marks) < 2:
        raise SystemExit(f"nav marker missing in {path}")
    start = marks[1] + 1
    while start < len(lines) and not lines[start]:
        start += 1
    body = []
    for line in lines[start:]:
        if line == "Our testimonial":
            break
        if line:
            body.append(line)
    return body


def take_text(lines, cursor, expected, where):
    acc = []
    i = cursor
    while i < len(lines):
        acc.append(lines[i])
        buf = norm(" ".join(acc))
        if buf == expected:
            return acc, i + 1
        if not expected.startswith(buf):
            break
        i += 1
    have = lines[cursor:cursor + 4]
    raise SystemExit(f"{where} could not match {expected[:80]!r} from {have!r}")


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
            ctx = out[max(0, found - 42) : found + len(old) + 42].replace("\n", " ")
            logs.append(f"{where}: '{old}' to '{new}' in \"{ctx}\"")
            out = out[:found] + new + out[found + len(old) :]
            start = found + len(new)
    return out


def assemble(spec, logs):
    lines = txt_lines(SRC / spec["source"])
    blocks_html = html_blocks(SRC / spec["source"].replace(".txt", ".html"))
    cursor = 0
    h1 = None
    sub = None
    blocks = []
    for kind, payload in blocks_html:
        if kind in ("ul", "ol"):
            taken = []
            for item in payload:
                chunk, cursor = take_text(lines, cursor, item, spec["slug"])
                if len(chunk) != 1:
                    raise SystemExit(f"{spec['slug']} list item spanned lines: {chunk}")
                taken.append(swap_text(chunk[0], spec["slug"], logs))
            blocks.append((kind, taken))
            continue
        chunk, cursor = take_text(lines, cursor, payload, spec["slug"])
        swapped = [swap_text(line, spec["slug"], logs) for line in chunk]
        text = swapped[0] if len(swapped) == 1 else " ".join(swapped)
        if kind == "h1":
            h1 = text
        elif kind == "h3" and sub is None:
            sub = text
        elif kind == "h3":
            blocks.append(("h2", text))
        elif kind == "p":
            blocks.append(("p", text))
        else:
            raise SystemExit(f"{spec['slug']} unknown kind {kind}")
    if cursor != len(lines):
        raise SystemExit(f"{spec['slug']} unused text lines: {lines[cursor:]}")
    if h1 is None or not sub:
        raise SystemExit(f"{spec['slug']} missing title")
    if not blocks or blocks[-1][0] != "p":
        raise SystemExit(f"{spec['slug']} last block is not the closing paragraph")
    closing = blocks.pop()[1]
    return h1, sub, blocks, closing, lines


def chrome_log(spec, logs):
    lines = [line.strip() for line in (SRC / spec["source"]).read_text().splitlines() if line.strip()]
    phone_at = lines.index("(702) 389-5009")
    copy_at = next(i for i, line in enumerate(lines) if line.startswith("Copyright"))
    old = lines[phone_at + 1 : copy_at]
    logs.append(f"{spec['slug']}: chrome hours '{' ; '.join(old[:-2])}' replaced by {NEW_HOURS}")
    logs.append(f"{spec['slug']}: chrome address '{' '.join(old[-2:])}' replaced by {NEW_ADDRESS}")
    logs.append(f"{spec['slug']}: {NO_NAME}")


def place_image(spec):
    if spec["image_kind"] == "missing":
        return None
    dest = ROOT / "assets" / "img" / spec["image_name"]
    if spec["image_kind"] == "real":
        if not dest.is_file():
            raise SystemExit(f"missing real photo {dest}")
    else:
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
    if spec["image_kind"] == "missing":
        if 'class="a-img"' in page:
            problems.append("CLA page has a hero image")
    elif spec["image_name"] not in page:
        problems.append("missing hero")
    for line in lines:
        swapped = line.replace("Henderson, NV", "Las Vegas, NV").replace("Henderson NV", "Las Vegas NV").replace("Henderson", "Las Vegas")
        escaped = html.escape(swapped, quote=False)
        if escaped in page:
            continue
        parts = [html.escape(part.strip(), quote=False) for part in swapped.split(". ") if part.strip()]
        if len(parts) < 2 or any(part not in page for part in parts):
            problems.append(f"missing copy: {swapped[:90]}")
    for name in ("DNoria R.", "Emily E.", "Laurie W.", "Andrea V.", "So happy I am now a Patient!!"):
        if name not in page:
            problems.append(f"missing review: {name}")
    written = spec["description"] + " " + spec["image_alt"]
    if "—" in written:
        problems.append("em dash in text we wrote")
    for word in ("treat", "treatment", "treating", "treated"):
        if re.search(rf"\b{word}\b", written, re.I):
            problems.append(f"text we wrote uses {word}")
    if "9555 S Eastern Ave, Ste 240B" not in page or "Las Vegas, NV 89123" not in page:
        problems.append("new address missing")
    if "Appointments only" not in page or "Sat, Sun" not in page:
        problems.append("new hours missing")
    if problems:
        raise SystemExit(spec["slug"] + " check failed: " + "; ".join(problems))


def render(spec, logs):
    size = place_image(spec)
    h1, sub, blocks, closing, lines = assemble(spec, logs)
    title = f"{h1} | Chiropractor Las Vegas NV | Evergrowth Chiropractic"
    logs.append(f"{spec['slug']}: title '{spec['old_title']}' to '{title}'")
    chrome_log(spec, logs)
    if spec["image_kind"] == "missing":
        image = None
        width = height = 0
        logs.append(f"{spec['slug']}: no hero. CLA Insight device photo is still missing, and it is not confirmed at the new office")
    else:
        width, height = size
        image = f"{shell.prefix(DEPTH)}assets/img/{spec['image_name']}"
        if spec["image_kind"] == "real":
            logs.append(
                f"{spec['slug']}: image real client photo 20261029_105156.jpg as assets/img/{spec['image_name']} ({width}x{height}), teal hallway"
            )
        else:
            logs.append(
                f"{spec['slug']}: image stock {spec['catalog'].relative_to(CATALOG)} as assets/img/{spec['image_name']} ({width}x{height}), stock, not a client photo"
            )
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
        image=image,
        image_alt=spec["image_alt"],
        image_w=width,
        image_h=height,
        blocks=blocks,
        closing=closing,
        group_title=spec["group"],
        group_links=condition.nav_group(spec["group"]),
    )
    if spec["image_name"] == "office-hallway-1200.jpg" and image:
        src_2400 = image.replace("office-hallway-1200.jpg", "office-hallway-2400.jpg")
        alt = html.escape(spec["image_alt"], quote=False)
        plain = f'<img src="{image}" alt="{alt}" width="{width}" height="{height}">'
        rich = (
            f'<img src="{image}" srcset="{image} 1200w, {src_2400} 2400w" '
            f'sizes="(max-width: 1060px) 100vw, 740px" alt="{alt}" '
            f'width="{width}" height="{height}">'
        )
        if plain not in page:
            raise SystemExit("adjustments hallway image tag was not the expected shape")
        page = page.replace(plain, rich, 1)
    check(spec, page, lines)
    dest = ROOT / spec["slug"] / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()[:12]
    print(dest)
    print("page-sha", digest)
    return dest


def rewire_nav():
    slugs = [spec["slug"] for spec in PAGES]
    pairs = tuple((f'site-map.html#{slug}"', f'{slug}/"') for slug in slugs)
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
    print("rewired", len(changed))
    index = (ROOT / "index.html").read_text()
    for slug in slugs:
        if f'href="{slug}/"' not in index:
            raise SystemExit(f"home nav was not rewired for {slug}")
        if f"site-map.html#{slug}" in index:
            raise SystemExit(f"{slug} anchor still in home")


def mark_site_map():
    path = ROOT / "site-map.html"
    html_text = path.read_text()
    for spec in PAGES:
        if spec["old_row"] in html_text:
            html_text = html_text.replace(spec["old_row"], spec["new_row"], 1)
        elif spec["new_row"] not in html_text:
            raise SystemExit(f"site-map row missing for {spec['slug']}")
    photo_old = "Home, Why Choose a Chiropractor. Planned: Chiropractic Adjustments, Gonstead pages."
    photo_new = "Home, Why Choose a Chiropractor, and Chiropractic Adjustments. Planned: Gonstead pages."
    if photo_old in html_text:
        html_text = html_text.replace(photo_old, photo_new, 1)
    elif photo_new not in html_text:
        raise SystemExit("adjusting room photo row missing")
    path.write_text(html_text)
    print("site-map marked built")


def stamp(previous):
    index = ROOT / "index.html"
    build_id = hashlib.sha256(index.read_bytes()).hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    previous = (ROOT / "build-id.txt").read_text().strip()
    logs = []
    for spec in PAGES:
        render(spec, logs)
    rewire_nav()
    mark_site_map()
    build_id = stamp(previous)
    log_path = Path("/tmp/egc-r08-swaps.txt")
    log_path.write_text("\n".join(logs) + f"\nbuild-id {build_id}\n")
    print("swaps", len(logs))
    for line in logs:
        print("swap:", line)


if __name__ == "__main__":
    build()
