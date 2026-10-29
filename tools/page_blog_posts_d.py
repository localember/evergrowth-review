"""Blog posts batch 4 of 4.

Copy comes from the archive text files. The saved HTML is used only to keep
the original paragraphs, lists, and links. Wording changes, and only these:
- Henderson becomes Las Vegas, including titles, descriptions, and the
  previous and next post titles.
- The title suffix "Chiropractor Henderson NV | New Patient Experience"
  becomes "Chiropractor Las Vegas NV | Evergrowth Chiropractic".
- The old footer address and hours are not copied. The shared shell
  supplies 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123 and the
  new hours.
- Links to the old evergrowthchiro.com pages become preview links.
  Home links go to this preview's home page. Posts in this batch, and
  posts already built, link to their pages. Posts that are not built yet
  link to the site map row.
- Outside links, if a post has any, open in a new tab.

No doctor name appears in these five posts, so there is no name swap.
New Patient Special is left off. No images: the post photos are not saved
files we can place, so the pages stay plain until the client sends originals.
"""
import hashlib
import html
import re
from html.parser import HTMLParser
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_blog
import shell

ROOT = Path(__file__).resolve().parents[1]
OLD = Path("/tmp/evergrowth-src/old/pages")
DEPTH = 1
CLOSER = "Ready To Find Out More Information?"
REQUEST = "Request An Appointment"
OLD_ADDRESS = "1263 E Silverado Ranch Blvd #105A"
OLD_CITY = "Henderson, NV 89183"
TITLE_SUFFIX = "Chiropractor Henderson NV | New Patient Experience"

SLUGS = [
    "las-vegas-chiropractor-talks-about-wellness-care",
    "las-vegas-chiropractors-help-range-of-motion",
    "las-vegas-chiropractors-may-relieve-migraines",
    "sciatic-leg-pain-in-las-vegas",
    "the-sitting-epidemic-in-las-vegas",
]

STRUCT = {"p", "ol", "ul", "li", "strong", "em", "b", "i", "a", "h2", "h3", "h4", "blockquote"}
TRANSPARENT = {"span", "div"}
VOID = {"br"}
SKIP = {"img"}

NOTES = {
    "las-vegas-chiropractor-talks-about-wellness-care": (
        "BUILT from old/pages/las-vegas-chiropractor-talks-about-wellness-care_20260511.txt. "
        "Henderson swapped to Las Vegas in the title, description, body, and previous and next titles. "
        "The home link on Evergrowth Chiropractic in Henderson now points at this preview. "
        "No name swap. Old footer address and hours were not copied. New Patient Special left off. "
        "No image: wellness-care.webp is not a saved file."
    ),
    "las-vegas-chiropractors-help-range-of-motion": (
        "BUILT from old/pages/las-vegas-chiropractors-help-range-of-motion_20260606.txt. "
        "Henderson swapped to Las Vegas in the title, description, body, and previous and next titles. "
        "The home link on Henderson NV chiropractic experts now points at this preview. "
        "No name swap. Old footer address and hours were not copied. New Patient Special left off. "
        "No image: Range-of-motion.webp is not a saved file."
    ),
    "las-vegas-chiropractors-may-relieve-migraines": (
        "BUILT from old/pages/las-vegas-chiropractors-may-relieve-migraines_20260314.txt. "
        "Henderson swapped to Las Vegas in the title, description, body, and previous and next titles. "
        "The home link on Henderson NV chiropractors now points at this preview. "
        "No name swap. Old footer address and hours were not copied. New Patient Special left off. "
        "No image: Migraines.webp is not a saved file."
    ),
    "sciatic-leg-pain-in-las-vegas": (
        "BUILT from old/pages/sciatic-leg-pain-in-las-vegas_20260606.txt. "
        "Henderson swapped to Las Vegas in the title, description, body, and previous and next titles. "
        "The home link on chiropractic clinic in beautiful Henderson now points at this preview. "
        "No name swap. Old footer address and hours were not copied. New Patient Special left off. "
        "No image: Sciatic-leg-pain.webp is not a saved file."
    ),
    "the-sitting-epidemic-in-las-vegas": (
        "BUILT from old/pages/the-sitting-epidemic-in-las-vegas_20260606.txt. "
        "Henderson swapped to Las Vegas in the title, description, body, and previous and next titles. "
        "The home link on lower back pain in Henderson now points at this preview. "
        "No name swap. Old footer address and hours were not copied. New Patient Special left off. "
        "No image: sitting-back-pain.webp is not a saved file."
    ),
}


def esc(text):
    return html.escape(text, quote=False)


def squash(text):
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def edge_text(text):
    raw = text.replace("\xa0", " ")
    if not raw.strip():
        return ""
    lead = raw[0].isspace()
    trail = raw[-1].isspace()
    core = re.sub(r"\s+", " ", raw).strip()
    return (" " if lead else "") + core + (" " if trail else "")


class RichText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.capture = False
        self.depth = 0
        self.parts = []
        self.unknown = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if not self.capture:
            if tag == "div" and "bde-rich-text" in attrs.get("class", ""):
                self.capture = True
                self.depth = 1
            return
        if tag in VOID or tag in SKIP:
            if tag == "br":
                self.parts.append(("br",))
            return
        self.depth += 1
        if tag in STRUCT:
            self.parts.append(("start", tag, attrs))
        elif tag not in TRANSPARENT:
            self.unknown.add(tag)
            self.parts.append(("start", tag, attrs))

    def handle_startendtag(self, tag, attrs):
        if self.capture and tag == "br":
            self.parts.append(("br",))
        elif not self.capture:
            self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if not self.capture or tag in VOID or tag in SKIP:
            return
        self.depth -= 1
        if self.depth <= 0:
            self.capture = False
            return
        if tag in STRUCT or tag not in TRANSPARENT:
            self.parts.append(("end", tag))

    def handle_data(self, data):
        if self.capture and data:
            self.parts.append(("text", data))


def one_file(slug, suffix):
    matches = list(OLD.glob(slug + "_*" + suffix))
    if suffix == ".txt":
        matches = [
            path for path in matches
            if path.name.endswith(".txt") and not path.name.endswith(".images.txt")
        ]
    if len(matches) != 1:
        raise SystemExit(f"expected one {suffix} for {slug}, got {matches}")
    return matches[0]


def content_images(slug):
    path = one_file(slug, ".images.txt")
    names = []
    for line in path.read_text().splitlines():
        lower = line.lower()
        if any(word in lower for word in ("logo", "favicon", "trusted-badge", "eye.svg")):
            continue
        names.append(line.rstrip().rsplit("/", 1)[-1])
    return names


def city_swap(text, slug, where, log):
    if not re.search(r"henderson", text, re.I):
        return text
    for match in re.finditer(r".{0,48}Henderson.{0,48}", text):
        before = squash(match.group(0))
        log.append(f"{slug} | {where} | {before} => {before.replace('Henderson', 'Las Vegas')}")
    for match in re.finditer(r".{0,48}henderson.{0,48}", text):
        if "Henderson" in match.group(0):
            continue
        before = squash(match.group(0))
        log.append(f"{slug} | {where} | {before} => {before.replace('henderson', 'Las Vegas')}")
    swapped = text.replace("Henderson", "Las Vegas").replace("henderson", "Las Vegas")
    if re.search(r"henderson", swapped, re.I):
        raise SystemExit("Henderson remained in " + slug + " " + where)
    return swapped


def visible(parts):
    chunks = []
    blocks = {"p", "li", "h2", "h3", "h4", "blockquote", "ol", "ul"}
    for part in parts:
        if part[0] == "text":
            chunks.append(edge_text(part[1]))
        elif part[0] == "br" or (part[0] in ("start", "end") and part[1] in blocks):
            chunks.append(" ")
    return squash("".join(chunks))


def txt_body(lines, h1):
    indexes = [i for i, line in enumerate(lines) if line.strip() == h1]
    if not indexes:
        raise SystemExit("h1 missing from archive text: " + h1)
    start = indexes[-1] + 1
    body = []
    for line in lines[start:]:
        if line.startswith("Previous Post") or line.startswith("Next Post") or line.startswith("New Patient Special"):
            break
        if line.strip():
            body.append(line.strip())
    return squash(" ".join(body))


def classify_href(href):
    href = href.strip()
    homes = {
        "/",
        "https://www.evergrowthchiro.com",
        "https://www.evergrowthchiro.com/",
        "https://evergrowthchiro.com",
        "https://evergrowthchiro.com/",
    }
    if href in homes:
        return ("home", "")
    for base in ("https://www.evergrowthchiro.com/", "https://evergrowthchiro.com/", "/"):
        if href.startswith(base):
            rest = href[len(base):].split("?", 1)[0].split("#", 1)[0].strip("/")
            if rest and "/" not in rest:
                return ("slug", rest)
            return ("live", href)
    if href.startswith("tel:") or href.startswith("mailto:"):
        return ("direct", href)
    if href.startswith("http://") or href.startswith("https://"):
        return ("external", href)
    return ("bad", href)


def map_href(href):
    kind, value = classify_href(href)
    if kind == "home":
        return shell.href("index", DEPTH), ""
    if kind == "slug":
        if value in SLUGS or (ROOT / value / "index.html").exists():
            return f"../{value}/", ""
        if value in page_blog.SLUGS:
            return f"../site-map.html#blog-{value}", ""
        target = shell.href(value, DEPTH)
        if target.endswith("#" + value):
            raise SystemExit("unmapped internal link: " + href)
        return target, ""
    if kind == "direct":
        return value, ""
    if kind == "external":
        return value, ' target="_blank" rel="noopener"'
    raise SystemExit("refusing live or unknown link: " + href)


def render_parts(parts, slug, log):
    out = []
    for part in parts:
        if part[0] == "text":
            text = edge_text(part[1])
            if text:
                out.append(esc(city_swap(text, slug, "body", log)))
        elif part[0] == "br":
            out.append("<br>")
        elif part[0] == "start":
            tag, attrs = part[1], part[2]
            if tag == "a":
                href, extra = map_href(attrs.get("href", ""))
                out.append(f'<a href="{html.escape(href, quote=True)}"{extra}>')
            else:
                out.append(f"<{tag}>")
        elif part[0] == "end":
            out.append(f"</{part[1]}>")
    return "".join(out)


def adjacent(chunk):
    found = []
    for match in re.finditer(r'<a\b([^>]*)>(.*?)</a>', chunk, re.S):
        inner = squash(html.unescape(re.sub(r"<[^>]+>", " ", match.group(2))))
        label = None
        if inner.startswith("Previous Post"):
            label = "Previous Post"
        elif inner.startswith("Next Post"):
            label = "Next Post"
        else:
            continue
        href = re.search(r'href="([^"]+)"', match.group(1))
        if not href:
            raise SystemExit("adjacent post has no href")
        title = inner[len(label):].strip()
        found.append((label, href.group(1), title))
    return found


def txt_adjacent(lines):
    found = []
    for line in lines:
        for label in ("Previous Post", "Next Post"):
            if line.startswith(label):
                found.append((label, line[len(label):].strip()))
    return found


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


def post_nav(items):
    if not items:
        raise SystemExit("post has no previous or next link")
    bits = ['<nav class="post-nav" aria-label="More posts">']
    only_next = len(items) == 1 and items[0][0] == "Next Post"
    for label, href, title in items:
        klass = "next"
        if only_next:
            klass = "next only-next"
        class_attr = f' class="{klass}"' if label == "Next Post" else ""
        bits.append(
            f'<a{class_attr} href="{html.escape(href, quote=True)}">'
            f"<span>{esc(label)}</span><strong>{esc(title)}</strong></a>"
        )
    bits.append("</nav>")
    return "".join(bits)


def load(slug, log):
    text_path = one_file(slug, ".txt")
    html_path = one_file(slug, ".html")
    raw_txt = text_path.read_text()
    raw_html = html_path.read_text(errors="replace")
    if TITLE_SUFFIX not in raw_txt:
        raise SystemExit("old title suffix missing: " + slug)
    if OLD_ADDRESS not in raw_txt or OLD_CITY not in raw_txt:
        raise SystemExit("old address missing from archive: " + slug)
    if "New Patient Special Offer" not in raw_txt:
        raise SystemExit("special missing from archive: " + slug)
    if f"/{slug}/" not in raw_txt.splitlines()[0]:
        raise SystemExit("archive url does not match slug: " + slug)

    h1_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", raw_html, re.S)
    if not h1_match:
        raise SystemExit("h1 missing: " + slug)
    h1 = squash(html.unescape(re.sub(r"<[^>]+>", " ", h1_match.group(1))))
    desc_match = re.search(r'<meta name="description" content="(.*?)"', raw_html)
    if not desc_match:
        raise SystemExit("description missing: " + slug)
    description = squash(html.unescape(desc_match.group(1)))

    parser = RichText()
    parser.feed(raw_html)
    if parser.unknown:
        raise SystemExit(f"unknown tags in {slug}: {sorted(parser.unknown)}")
    if not parser.parts:
        raise SystemExit("no article body: " + slug)
    if any(part[0] == "start" and part[1] == "img" for part in parser.parts):
        raise SystemExit("image inside the article: " + slug)

    lines = raw_txt.splitlines()
    archive_body = txt_body(lines, h1)
    parsed_body = visible(parser.parts)
    if parsed_body != archive_body:
        raise SystemExit(
            "archive text and saved article do not match for " + slug
            + "\nTXT: " + archive_body[:500]
            + "\nHTML: " + parsed_body[:500]
        )

    body_html = render_parts(parser.parts, slug, log)
    # The saved HTML starts two posts with an empty break before the first
    # sentence. The archive text has no blank line there, so it is not copy.
    body_html = body_html.replace("<p><br>", "<p>")
    h1 = city_swap(h1, slug, "h1", log)
    description = city_swap(description, slug, "description", log)

    marker = raw_html.find("bde-rich-text")
    special = raw_html.find("New Patient Special Offer", marker)
    if marker < 0 or special < 0:
        raise SystemExit("could not isolate adjacent posts: " + slug)
    html_adj = adjacent(raw_html[marker:special])
    text_adj = txt_adjacent(lines)
    if [(label, title) for label, _href, title in html_adj] != text_adj:
        raise SystemExit("adjacent titles do not match the archive text: " + slug + " " + str(html_adj) + " " + str(text_adj))

    nav_items = []
    for label, href, title in html_adj:
        kind, value = classify_href(href)
        if kind != "slug":
            raise SystemExit("adjacent post is not an internal page: " + href)
        mapped, extra = map_href(href)
        if extra:
            raise SystemExit("adjacent post opened as an outside link: " + href)
        nav_items.append((label, mapped, city_swap(title, slug, label, log)))

    if re.search(r"\bDr\.?\s+(?!Gonstead\b)", archive_body):
        raise SystemExit("unexpected doctor name in " + slug)
    return h1, description, body_html, nav_items, text_path.name


def article_page(h1, description, article):
    home = shell.href("index", DEPTH)
    blog = shell.href("blog", DEPTH)
    body = (
        f'<section class="page-hero"><div class="container"><div class="crumbs">'
        f'<a href="{home}">Home</a><span>/</span><a href="{blog}">Blog</a><span>/</span>{esc(h1)}</div>'
        f"<h1>{esc(h1)}</h1></div></section>"
        f'<section><div class="container article-grid"><article class="article">{article}</article>'
        f"{aside()}</div></section>{closer()}"
    )
    return shell.render_page(
        f"{h1} | Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        description,
        body,
        DEPTH,
    )


def check(page, slug):
    main = page.split("<main", 1)[1].split("</main>", 1)[0]
    outside = page.split("<main", 1)[0] + page.split("</main>", 1)[1]
    if "<h1>" not in main or "</h1>" not in main:
        raise SystemExit("h1 missing on " + slug)
    if re.search(r"henderson", page, re.I):
        raise SystemExit("Henderson remained on " + slug)
    for banned in (
        OLD_ADDRESS,
        "89183",
        "Silverado",
        "New Patient Special",
        "$47",
        "New Patient Experience",
        "evergrowthchiro.com/",
        "www.evergrowthchiro.com",
        'href="/',
        'src="/',
        "20250814_131251",
        "20251020_162305",
        "Dr. [Last Name]",
        "placeholder=",
        "date of birth",
    ):
        if banned.lower() in page.lower():
            raise SystemExit("forbidden on " + slug + ": " + banned)
    if "<img" in main:
        raise SystemExit("image in the article: " + slug)
    social = ("facebook.com", "instagram.com", "linkedin.com", "youtube.com", "twitter.com")
    if any(word in page.lower() for word in social):
        raise SystemExit("social link on " + slug)
    authored = " ".join((
        "Home", "Blog", CLOSER, REQUEST, "Book Appointment", "Hours",
        "Previous Post", "Next Post", "More posts",
        "Mon, Wed, Thu", "Tuesday", "Friday", "Sat, Sun",
    ))
    if "\u2014" in authored or "--" in authored:
        raise SystemExit("em dash in authored text: " + slug)
    # Title and description are the client's heading and summary. "Treatment"
    # stays there. The shell around them must not use those words.
    shell_text = re.sub(r"<title>.*?</title>", " ", outside, count=1)
    shell_text = re.sub(r'<meta name="description" content=".*?">', " ", shell_text, count=1)
    for word in ("treat", "treatment", "treating", "treated"):
        if re.search(r"\b" + word + r"\b", authored, re.I):
            raise SystemExit("authored text uses " + word)
        if re.search(r"\b" + word + r"\b", shell_text, re.I):
            raise SystemExit("shell text uses " + word + " on " + slug)
    for needed in (
        'href="../book-appointment/"',
        "9555 S Eastern Ave, Ste 240B",
        "Las Vegas, NV 89123",
        "10am to 1pm, 3pm to 6pm",
        "Appointments only",
        ">Sat, Sun</span>",
        ">Closed</span>",
        "Info@evergrowthchiro.com",
        "(702) 389-5009",
        'content="noindex, nofollow"',
        'href="../assets/style.css"',
        'src="../assets/site.js"',
        'href="../blog/"',
        'href="../index.html"',
        CLOSER,
    ):
        if needed not in page:
            raise SystemExit("missing from " + slug + ": " + needed)
    if page.count('href="../book-appointment/"') < 4:
        raise SystemExit("expected header, aside, closer, and footer booking links on " + slug)
    for chunk in page.split('href="../book-appointment/"')[1:]:
        tag = chunk.split(">", 1)[0]
        if "target" in tag:
            raise SystemExit("Book Appointment opens in a new tab on " + slug)
    for match in re.finditer(r"<a\b([^>]*)>", page):
        attrs = match.group(1)
        if 'target="_blank"' in attrs and 'rel="noopener"' not in attrs:
            raise SystemExit("outside link missing rel on " + slug)
        if 'target="_blank"' in attrs and "http" not in attrs:
            raise SystemExit("internal link opens in a new tab on " + slug)
    if len(page.encode()) <= 10000:
        raise SystemExit(slug + " is under 10kb")


def rewire(slug):
    old = f"site-map.html#blog-{slug}"
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
        raise SystemExit("blog anchor still in " + ", ".join(leftover))
    blog = (ROOT / "blog" / "index.html").read_text()
    if blog.count(f'href="../{slug}/"') != 2:
        raise SystemExit("blog index should link the title and Read more for " + slug)
    print("rewired", slug, changed)


def mark_site_map(slug):
    path = ROOT / "site-map.html"
    html_text = path.read_text()
    start = html_text.find(f'<tr id="blog-{slug}">')
    if start < 0:
        raise SystemExit("site-map row missing: " + slug)
    end = html_text.find("</tr>", start)
    row = html_text[start:end]
    old = f'<td><code>/{slug}/</code></td><td><span class="tag partial">content partial</span>'
    new = (
        f'<td><code>/{slug}/</code> <a href="{slug}/">(built)</a></td>'
        f'<td><span class="tag ready">content ready</span>'
    )
    if old not in row:
        if f'href="{slug}/">(built)</a>' in row and "content ready" in row:
            print("site-map already marked", slug)
            return
        raise SystemExit("status cell missing: " + slug)
    path.write_text(html_text[:start] + row.replace(old, new, 1) + html_text[end:])
    print("site-map marked", slug)


def mark_blog_note():
    path = ROOT / "site-map.html"
    html_text = path.read_text()
    start = html_text.find('<tr id="blog">')
    end = html_text.find("</tr>", start)
    row = html_text[start:end]
    old = "Batch 1, batch 2, and batch 3 posts link to their pages. The other Read more links go to the site map row until that post is built."
    new = "All 23 posts link to their pages."
    if old not in row:
        if new not in row:
            raise SystemExit("blog index note missing")
        return
    path.write_text(html_text[:start] + row.replace(old, new, 1) + html_text[end:])
    print("blog index note updated")


def stamp(previous):
    digest = hashlib.sha256()
    digest.update((ROOT / "blog" / "index.html").read_bytes())
    digest.update((ROOT / "site-map.html").read_bytes())
    digest.update((ROOT / "assets" / "style.css").read_bytes())
    for slug in SLUGS:
        digest.update((ROOT / slug / "index.html").read_bytes())
    build_id = digest.hexdigest()[:12]
    if build_id == previous:
        raise SystemExit("build-id did not change")
    (ROOT / "build-id.txt").write_text(build_id + "\n")
    print("build-id", build_id)
    return build_id


def build():
    log = []
    previous = (ROOT / "build-id.txt").read_text().strip()
    pages = {}
    for slug in SLUGS:
        h1, description, body_html, nav_items, source_name = load(slug, log)
        article = body_html + post_nav(nav_items)
        page = article_page(h1, description, article)
        check(page, slug)
        if source_name not in NOTES[slug]:
            raise SystemExit("note does not name the source file: " + source_name)
        pages[slug] = page
        print("ready", slug, "images", content_images(slug) or "none")
    for slug, page in pages.items():
        dest = ROOT / slug / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page)
        check(dest.read_text(), slug)
    for slug in SLUGS:
        rewire(slug)
        mark_site_map(slug)
    mark_blog_note()
    # Rewiring can touch pages that were just written. Check them again.
    for slug in SLUGS:
        check((ROOT / slug / "index.html").read_text(), slug)
    blog = (ROOT / "blog" / "index.html").read_text()
    if re.search(r"henderson", blog, re.I):
        raise SystemExit("Henderson returned to the blog index")
    build_id = stamp(previous)
    log_path = Path("/tmp/blog-batch4-swap-log.txt")
    log_path.write_text(str(len(log)) + " Henderson to Las Vegas swaps\n\n" + "\n".join(log) + "\n")
    print("swaps", len(log))
    print(log_path)
    return build_id


if __name__ == "__main__":
    build()
