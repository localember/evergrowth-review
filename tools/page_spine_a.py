"""Spine condition batch A: headaches, neck pain, sciatica, scoliosis.

Copy is the archive text named in the row. Allowed swaps only, logged in
SWAPS on each page. Reviews stay word for word, including Dr Will.
Heroes are stock Catalog/Conditions files, not client photos.
"""
import hashlib
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import condition
import shell

ROOT = Path(__file__).resolve().parents[1]
DEPTH = 1
CATALOG = Path(
    "/Users/johnowens/localember/tools/bd-generator/assets/stock/Catalog/Conditions"
)

CHROME_ADDRESS = (
    "Chrome: old address 1263 E Silverado Ranch Blvd #105A, Henderson, NV 89183 "
    "replaced by 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123"
)
CHROME_HOURS_WEEKDAY = (
    "Chrome: old weekday 10am-6pm hours replaced by Mon, Wed, Thu 10am to 1pm and "
    "3pm to 6pm; Tue 3pm to 6pm; Fri appointments only; Sat and Sun closed"
)
CHROME_HOURS_SPLIT = (
    "Chrome: old hours Mon/Wed/Thu 10am-1pm and 3pm-6pm, Tue 3pm-6pm, Fri 10am-1pm, "
    "Sat 10am-1pm, Sun closed replaced by Mon, Wed, Thu 10am to 1pm and 3pm to 6pm; "
    "Tue 3pm to 6pm; Fri appointments only; Sat and Sun closed"
)
NO_NAME = (
    "No name swap. Reviews keep Dr Will and Dr. Will. New Patient Special omitted."
)

PAGES = [
    {
        "slug": "headaches-migraines",
        "source": "headaches-migraines_20260511.txt",
        "catalog": "headaches.webp",
        "image_name": "stock-condition-headaches.webp",
        "image_alt": "Woman sitting on a couch holding both sides of her head",
        "title": "Headache & Migraine Relief - Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "description": "Chiropractic care for headaches and migraines in Las Vegas, NV at Evergrowth Chiropractic.",
        "crumb": "Headaches & Migraines",
        "h1": "Headache & Migraine Relief",
        "sub": "Headaches and Migraines in Las Vegas, NV",
        "blocks": [
            (
                "p",
                "Headaches can be quite the ordeal, and migraines take that ordeal to a whole new level of discomfort. Coping with either of these conditions can leave you feeling irritable, and in severe cases, render you incapable of carrying out your daily tasks. While medication can offer temporary relief, it often falls short when the problem persists or recurs. The root cause of your headache or migraine typically lies in structural issues, making it crucial to seek proper treatment to overcome this debilitating problem. If you're seeking relief from headaches or migraines, our chiropractic clinic in Las Vegas, might hold the solution you've been searching for.",
            ),
            ("h2", "Symptoms of Headaches and Migraines"),
            (
                "p",
                "Whether you're contending with a constant throbbing in your head or experiencing the most severe symptoms associated with migraines—such as sensitivity to light and noise, nausea, vomiting, hallucinations, depression, and irritability—the culprit could be a structural concern. When your spine shifts out of alignment due to developmental factors, trauma, repetitive stress, or other incidents, it exerts pressure on the surrounding nerves. When these nerves become compressed or irritated, they transmit signals to the muscles in your back, neck, and jaw, causing them to tense up.",
            ),
            (
                "p",
                "This muscle tightness can directly trigger acute headaches or migraines. Over time, this tension can also gradually misalign your bones, resulting in more persistent and agonizing headaches and migraines. These headaches and migraines may serve as warning signs of deeper issues emerging within your spinal column. Given that your spinal health affects every other system in your body, it becomes imperative to address these problems at the earliest signs.",
            ),
            ("h2", "Chiropractic Treatment for Headaches and Migraines"),
            (
                "p",
                "Chiropractic care boasts a rich history of effectively treating headaches and migraines. Chiropractors in Las Vegas, NV, possess an in-depth understanding of the subtle intricacies occurring in the spine, which is often a primary source of pain due to its connection with the nervous system. A chiropractic session commences with a comprehensive evaluation to rule out other potential causes of your headache and assess your spine for misalignment issues.",
            ),
            (
                "p",
                "This assessment helps pinpoint the precise treatment required for the underlying source of your pain. Using gentle and non-invasive techniques, chiropractors can perform spinal adjustments that, despite their seemingly subtle nature, can provide almost instantaneous relief and restore your long-term well-being. Unlike medications that merely address surface-level symptoms and offer temporary respite, chiropractic adjustments target the root cause of your headache or migraine, yielding lasting results that enhance your overall quality of life.",
            ),
        ],
        "closing": "If you're grappling with migraines or headaches, don't hesitate to reach out to our team at Evergrowth Chiropractic today for assistance.",
        "must": [
            "our chiropractic clinic in Las Vegas, might hold the solution",
            "Chiropractors in Las Vegas, NV, possess an in-depth understanding",
            "Headaches and Migraines in Las Vegas, NV",
            "migraines—such as sensitivity to light",
        ],
        "swaps": [
            "Subhead: 'Headaches and Migraines in Henderson, NV' to 'Headaches and Migraines in Las Vegas, NV'",
            "Opening: 'our chiropractic clinic in Henderson,' to 'our chiropractic clinic in Las Vegas,' (comma after the city kept)",
            "Chiropractic section: 'Chiropractors in Henderson, NV,' to 'Chiropractors in Las Vegas, NV,'",
            "Title: 'Chiropractor Henderson NV | New Patient Experience' to 'Chiropractor Las Vegas NV | Evergrowth Chiropractic'",
            CHROME_ADDRESS,
            CHROME_HOURS_WEEKDAY,
            NO_NAME,
        ],
    },
    {
        "slug": "neck-pain",
        "source": "neck-pain_20260417.txt",
        "catalog": "neck-pain.webp",
        "image_name": "stock-condition-neck-pain.webp",
        "image_alt": "Man at a desk holding the back of his neck",
        "title": "Neck Pain Relief - Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "description": "Chiropractic care for neck pain in Las Vegas, NV at Evergrowth Chiropractic.",
        "crumb": "Neck Pain",
        "h1": "Neck Pain Relief",
        "sub": "Find Relief from Neck Pain in Las Vegas, NV",
        "blocks": [
            (
                "p",
                "Ever heard the age-old expression, \"It's a real pain in the neck\"? Well, if you've experienced persistent neck discomfort, you understand the importance of seeking out the finest chiropractor in Las Vegas, NV. Neck pain can transform even the simplest neck, head, arm, shoulder, and back movements into excruciating ordeals. Neck issues can lead to headaches, upper body discomfort, and sore muscles. Prolonged neck pain can result in weakened and degenerated muscles due to immobility.",
            ),
            (
                "p",
                "Identifying the root cause of your neck pain is a crucial step toward obtaining effective short and long-term treatment. This article delves into the causes of neck pain and sheds light on how chiropractic care in Las Vegas can offer a valuable alternative to conventional treatments.",
            ),
            ("h2", "Treating Neck Pain"),
            (
                "p",
                "Although the neck constitutes a relatively small part of the body, it houses complex structures that play a vital role in supporting your head. The small vertebrae in the neck allow for significant mobility but also render it more susceptible to injury and pain. Common causes of neck pain include:",
            ),
            (
                "ul",
                [
                    "Trauma, such as whiplash.",
                    "Sleeping position.",
                    "Poor posture.",
                    "Repetitive stress.",
                    "Bone structure abnormalities.",
                    "Joint issues.",
                    "Muscle strains and pulls.",
                ],
            ),
            (
                "p",
                "Most of these issues either result from or affect the alignment of the spine. When neck muscles go into spasms, the spine becomes misaligned. Misalignment irritates the nerves, leading to increased tension and other systemic problems. Since every nerve in the body originates in the spinal column, neck-related issues can have far-reaching consequences throughout the entire system.",
            ),
            (
                "p",
                "Unfortunately, many people in Las Vegas, NV, neglect correcting spinal problems, hoping that the pain will eventually subside. While this may happen in some cases, the underlying misalignment usually persists. Over time, the problem can worsen, leading to a recurrence of pain. If left unaddressed, the issue can escalate to the point where surgery becomes the only viable option.",
            ),
            ("h2", "Conventional vs Holistic Approaches"),
            (
                "p",
                "Typically, individuals attempt to manage their neck pain with prescription or over-the-counter medications. While these may temporarily alleviate symptoms, they often come with side effects, and the root problem remains unaddressed. Over the years, massage therapy has gained popularity, providing relief for muscle tightness. However, if the issue originates in the bones or joints, it remains unresolved.",
            ),
            (
                "p",
                "Chiropractic treatment offers a holistic approach that tackles the structural causes behind most neck pain. Following a comprehensive chiropractic assessment aimed at ruling out other potential issues and pinpointing the exact source of the problem, a personalized recovery plan is devised. Gentle spinal adjustments can provide immediate relief and restore long-term neck and overall body health.",
            ),
        ],
        "closing": "Contact our team at Evergrowth Chiropractic today to schedule a consultation and put an end to that nagging pain in your neck.",
        "must": [
            "finest chiropractor in Las Vegas, NV",
            "chiropractic care in Las Vegas can offer a valuable alternative",
            "many people in Las Vegas, NV, neglect correcting spinal problems",
            "Find Relief from Neck Pain in Las Vegas, NV",
            "Trauma, such as whiplash.",
            "Muscle strains and pulls.",
        ],
        "swaps": [
            "Subhead: 'Find Relief from Neck Pain in Henderson, NV' to 'Find Relief from Neck Pain in Las Vegas, NV'",
            "Opening: 'finest chiropractor in Henderson, NV' to 'finest chiropractor in Las Vegas, NV'",
            "Second paragraph: 'chiropractic care in Henderson can offer' to 'chiropractic care in Las Vegas can offer'",
            "Neglect paragraph: 'many people in Henderson, NV,' to 'many people in Las Vegas, NV,'",
            "Title: 'Chiropractor Henderson NV | New Patient Experience' to 'Chiropractor Las Vegas NV | Evergrowth Chiropractic'",
            CHROME_ADDRESS,
            CHROME_HOURS_SPLIT,
            NO_NAME,
        ],
    },
    {
        "slug": "sciatica",
        "source": "sciatica_20260314.txt",
        "catalog": "sciatica.webp",
        "image_name": "stock-condition-sciatica.webp",
        "image_alt": "Woman at a desk holding her lower back",
        "title": "Sciatica Relief - Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "description": "Chiropractic care for sciatica in Las Vegas, NV at Evergrowth Chiropractic.",
        "crumb": "Sciatica",
        "h1": "Sciatica Relief",
        "sub": "Chiropractic Care for Sciatica in Las Vegas, NV",
        "blocks": [
            (
                "p",
                "Experiencing the relentless agony that travels from your back or buttocks down your legs? You might be grappling with the all-too-familiar ailment known as sciatica. For many folks, the quest for relief leads them to seek out a chiropractor in the Las Vegas area, hoping to escape the clutches of sciatic pain. Unfortunately, for many, a long-lasting remedy remains elusive. Unaddressed, sciatica can relentlessly deteriorate, transforming even the simplest daily tasks into insurmountable challenges. This article endeavors to unravel the mysteries of sciatica and illuminate the ways in which chiropractic care can be a beacon of hope in your journey to conquer it.",
            ),
            ("h2", "Sciatica Remedies"),
            (
                "p",
                "Sciatica, often referred to as sciatic neuralgia, inflicts excruciating pain upon the lower back, coursing its way down the leg and ultimately settling in the foot. This condition can make prolonged sitting and standing agonizing ordeals, and it frequently results in weakness, tingling, and numbness in the leg and foot. Sciatica tends to ebb and flow throughout one's life, bringing forth episodes of varying pain intensity and discomfort. Left untreated, sciatic torment invariably intensifies, potentially causing permanent nerve damage.",
            ),
            (
                "p",
                "The reason for this extensive pain, seemingly radiating up and down the legs and back, lies in the compression of the sciatic nerve, the longest nerve within the human body. Originating in the lumbar spine, this nerve meanders through the buttocks before embarking on its journey down the leg, culminating in the ankle and foot. When the vertebrae in the lower back become compressed, the roots of the sciatic nerve become pinched and irritated, thereby triggering the agonizing pain and potential injury.",
            ),
            ("h2", "The Origins of Sciatica"),
            (
                "p",
                "Sciatica can be triggered by various factors, with disc injuries and bulges ranking as the most common culprits. In these instances, the disc exerts pressure on the nerve root, precipitating the condition. Disc injuries can materialize due to poor posture, repetitive-use injuries, or accidents. Furthermore, sciatica frequently occurs when spinal misalignments, known as subluxations, emerge as a result of postural problems, pregnancy, or traumatic incidents. Some individuals recount merely bending over to retrieve a piece of paper when they were suddenly engulfed in excruciating pain. In reality, the spinal condition was likely developing over a considerable period before the triggering event.",
            ),
            ("h2", "Chiropractic Solutions for Sciatica"),
            (
                "p",
                "Chiropractors in Las Vegas, NV are extensively trained to pinpoint the root causes of sciatica and collaborate with patients to devise a tailored treatment plan. After conducting a comprehensive evaluation of the individual's unique condition, the chiropractor employs gentle adjustments that facilitate the body's natural realignment.",
            ),
            (
                "p",
                "Response times vary from person to person, with some experiencing rapid relief while others require more time to recover. The duration of recovery largely hinges on the condition of the disc or joints that necessitate correction. In most scenarios, the longer the issue persists, the more time it takes to achieve full correction. The encouraging news is that rectifying an issue like this typically takes less time than it did to develop it. Once the spine and discs regain their proper alignment, patients often report an overall improvement in their well-being.",
            ),
        ],
        "closing": "If you find yourself grappling with sciatica symptoms, don't hesitate to reach out to our team at Evergrowth Chiropractic today.",
        "must": [
            "a chiropractor in the Las Vegas area",
            "Chiropractors in Las Vegas, NV are extensively trained",
            "Chiropractic Care for Sciatica in Las Vegas, NV",
            "sciatic neuralgia",
        ],
        "swaps": [
            "Subhead: 'Chiropractic Care for Sciatica in Henderson, NV' to 'Chiropractic Care for Sciatica in Las Vegas, NV'",
            "Opening: 'a chiropractor in the Henderson area' to 'a chiropractor in the Las Vegas area'",
            "Solutions section: 'Chiropractors in Henderson, NV are' to 'Chiropractors in Las Vegas, NV are' (no comma after NV, as written)",
            "Title: 'Chiropractor Henderson NV | New Patient Experience' to 'Chiropractor Las Vegas NV | Evergrowth Chiropractic'",
            CHROME_ADDRESS,
            CHROME_HOURS_SPLIT,
            NO_NAME,
        ],
    },
    {
        "slug": "scoliosis",
        "source": "scoliosis_20260417.txt",
        "catalog": "scoliosis.webp",
        "image_name": "stock-condition-scoliosis.webp",
        "image_alt": "Hands checking a back beside a spine illustration",
        "title": "How To Help Scoliosis - Chiropractor Las Vegas NV | Evergrowth Chiropractic",
        "description": "Chiropractic care for scoliosis in Las Vegas, NV at Evergrowth Chiropractic.",
        "crumb": "Scoliosis",
        "h1": "How To Help Scoliosis",
        "sub": "Struggling With Scoliosis in Las Vegas, NV",
        "blocks": [
            (
                "p",
                "Are you in search of the finest chiropractor in Las Vegas, dedicated to caring for scoliosis? Typically, scoliosis begins as a subtle curvature in the spine that gradually intensifies over time. A scoliosis diagnosis occurs when the spine deviates more than ten degrees to either the right or left when facing a medical examiner. As scoliosis advances to more severe stages, it can bring about significant health consequences.",
            ),
            (
                "p",
                "The reassuring news is that when spinal curvature is detected early and chiropractic care is sought, it can be halted from progressing into a debilitating condition. In this article, we will provide you with a concise overview of scoliosis development and its impact on your well-being. We will also shed light on how to identify scoliosis and how chiropractic care in Las Vegas, NV, can effectively reverse its effects and restore your body to optimal health.",
            ),
            ("h2", "Scoliosis and the Spine"),
            (
                "p",
                "Scoliosis manifests as an abnormal bend or curve in the spine, deviating from the ideal vertical alignment of a healthy spine. The exact origin of this curve can often be elusive. In its early stages, it may begin as a minor bend due to a single vertebra's misalignment. Over time, the body compensates by developing musculature that continues to pull the spine into lateral curves to maintain a level head position.",
            ),
            (
                "p",
                "Misalignments can occur due to various factors, including poor posture, degenerative diseases, or traumatic accidents. While many scoliosis cases initiate during rapid growth phases, especially in youth aged 10-12, this condition can also develop in older adults. In older individuals, scoliosis is frequently linked to degenerative disorders such as osteoporosis.",
            ),
            ("h2", "What are the Consequences of Scoliosis?"),
            (
                "p",
                "Neglected scoliosis and its underlying causes can lead to severe and enduring consequences. Scoliosis is associated with discomfort in the back, neck, shoulders, and buttocks. It can result in recurring injuries and has been connected to sciatica. In severe cases, it can lead to reduced lung and heart capacity, painful menstruation, and physical disability.",
            ),
            ("h2", "How is Scoliosis Identified?"),
            (
                "p",
                "Often, parents or close associates are the first to notice scoliosis, as the shoulders and pelvis no longer appear level. A thorough physical examination assesses gait and utilizes visual and manual evaluations to determine the extent of spinal curvature. An Adams Position Test, involving the patient bending forward as far as possible, can reveal the presence of an issue. If a noticeable curvature is detected, an X-ray will be employed to assess the severity of scoliosis.",
            ),
            ("h2", "Chiropractic Care for Scoliosis"),
            (
                "p",
                "Proficient chiropractors are trained to conduct comprehensive examinations to identify scoliosis. Once diagnosed, the chiropractor conducts a detailed health history assessment to identify any contributing factors. This assessment guides the selection of the most appropriate treatment for the specific case.",
            ),
            (
                "p",
                "Chiropractic care in Las Vegas, NV, represents a gentle and non-invasive approach to managing scoliosis. Chiropractors often perform precise spinal adjustments to rectify the body's compensations and aid in the restorative process.",
            ),
        ],
        "closing": "If you seek a safe and non-invasive method for addressing scoliosis, chiropractic medicine is your reliable ally in this journey toward better health.",
        "must": [
            "finest chiropractor in Las Vegas, dedicated to caring for scoliosis",
            "chiropractic care in Las Vegas, NV, can effectively reverse",
            "Chiropractic care in Las Vegas, NV, represents a gentle",
            "Struggling With Scoliosis in Las Vegas, NV",
            "Adams Position Test",
        ],
        "swaps": [
            "Subhead: 'Struggling With Scoliosis in Henderson, NV' to 'Struggling With Scoliosis in Las Vegas, NV'",
            "Opening: 'finest chiropractor in Henderson, dedicated' to 'finest chiropractor in Las Vegas, dedicated'",
            "Second paragraph: 'chiropractic care in Henderson, NV, can effectively reverse' to 'chiropractic care in Las Vegas, NV, can effectively reverse'",
            "Care section: 'Chiropractic care in Henderson, NV, represents' to 'Chiropractic care in Las Vegas, NV, represents'",
            "Title: 'Chiropractor Henderson NV | New Patient Experience' to 'Chiropractor Las Vegas NV | Evergrowth Chiropractic'",
            CHROME_ADDRESS,
            CHROME_HOURS_SPLIT,
            NO_NAME,
        ],
    },
]


def place_image(spec):
    src = CATALOG / spec["catalog"]
    dest = ROOT / "assets" / "img" / spec["image_name"]
    if src.is_file():
        shutil.copyfile(src, dest)
        return dest
    if dest.is_file():
        return dest
    raise SystemExit(f"missing stock image {src}")


def check(spec, page):
    problems = []
    if "Henderson" in page:
        problems.append("Henderson still present")
    if "evergrowthchiro.com/book" in page.lower() or "https://evergrowthchiro.com" in page.lower():
        problems.append("link points at the client site")
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
    if "1263 E Silverado" in page:
        problems.append("old address leaked")
    book = page.count('href="../book-appointment/"')
    if book < 4:
        problems.append(f"expected book links in header, article, sidebar, footer; found {book}")
    if spec["image_name"] not in page:
        problems.append("missing stock hero")
    for sentence in spec["must"]:
        if sentence not in page:
            problems.append(f"missing copy: {sentence}")
    for name in ("DNoria R.", "Emily E.", "Laurie W.", "Andrea V.", "So happy I am now a Patient!!"):
        if name not in page:
            problems.append(f"missing review: {name}")
    if problems:
        raise SystemExit(spec["slug"] + " check failed: " + "; ".join(problems))


def render(spec):
    place_image(spec)
    pre = shell.prefix(DEPTH)
    page = condition.render_condition(
        depth=DEPTH,
        title=spec["title"],
        description=spec["description"],
        crumbs=[
            ("Home", "index"),
            ("What We Do", None),
            ("Spine Related", None),
            (spec["crumb"], None),
        ],
        h1=spec["h1"],
        sub=spec["sub"],
        image=f"{pre}assets/img/{spec['image_name']}",
        image_alt=spec["image_alt"],
        image_w=2400,
        image_h=1600,
        blocks=spec["blocks"],
        closing=spec["closing"],
        group_title="Spine Related",
        group_links=condition.nav_group("Spine Related"),
    )
    check(spec, page)
    dest = ROOT / spec["slug"] / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()[:12]
    print(dest)
    print("page-sha", digest)
    print("source", spec["source"])
    for line in spec["swaps"]:
        print("swap:", line)
    return dest


def rewire_nav():
    pairs = (
        ("site-map.html#headaches-migraines", "headaches-migraines/"),
        ("site-map.html#neck-pain", "neck-pain/"),
        ("site-map.html#sciatica", "sciatica/"),
        ("site-map.html#scoliosis", "scoliosis/"),
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


def mark_site_map():
    path = ROOT / "site-map.html"
    html = path.read_text()
    notes = {
        "headaches-migraines": ("Headaches &amp; Migraines", "headaches.webp"),
        "neck-pain": ("Neck Pain", "neck-pain.webp"),
        "sciatica": ("Sciatica", "sciatica.webp"),
        "scoliosis": ("Scoliosis", "scoliosis.webp"),
    }
    for slug, (label, stock) in notes.items():
        old_cell = f'<tr id="{slug}"><td><b>{label}</b></td><td>planned (not built)</td>'
        new_cell = (
            f'<tr id="{slug}"><td><b>{label}</b></td>'
            f'<td><a href="{slug}/">{slug}/</a> (built)</td>'
        )
        if old_cell not in html:
            raise SystemExit(f"site-map row missing for {slug}")
        html = html.replace(old_cell, new_cell, 1)
        old_note = (
            f"Hero: stock Catalog/Conditions/{stock}<br>"
            f"<small>Stock image: Catalog/Conditions/{stock}</small>"
        )
        new_note = (
            "BUILT. Hero is stock.<br>"
            f"<small>Stock image: Catalog/Conditions/{stock}</small>"
        )
        if old_note not in html:
            raise SystemExit(f"site-map note missing for {slug}")
        html = html.replace(old_note, new_note, 1)
    path.write_text(html)
    print("site-map marked built")


def build():
    for spec in PAGES:
        render(spec)
    rewire_nav()
    mark_site_map()


if __name__ == "__main__":
    build()
