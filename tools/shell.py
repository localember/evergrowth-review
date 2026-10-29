"""Shared shell for the Evergrowth preview.

BOOK is the only Book Appointment target. It is an internal folder path,
same tab, no target attribute. Later rows should import render_page() and
book_href() instead of writing their own booking link.
"""
import html
import re

BOOK = "book-appointment/"
PHONE = "(702) 389-5009"
TEL = "tel:+17023895009"
ADDR1 = "9555 S Eastern Ave, Ste 240B"
ADDR2 = "Las Vegas, NV 89123"
EMAIL = "Info@evergrowthchiro.com"

HOURS = [
    ("Mon", "10am to 1pm, 3pm to 6pm"),
    ("Tue", "3pm to 6pm"),
    ("Wed", "10am to 1pm, 3pm to 6pm"),
    ("Thu", "10am to 1pm, 3pm to 6pm"),
    ("Fri", "Appointments only"),
    ("Sat", "Closed"),
    ("Sun", "Closed"),
]

NAV = [
    ("Home", "index", None),
    ("Who We Are", None, [
        ("Meet the Doctor", "meet-the-doctor"),
        ("Testimonials", "testimonials"),
        ("Office Tour", "office-tour"),
        ("Blog", "blog"),
    ]),
    ("Gonstead Technique", None, [
        ("Dr. Gonstead", "founder-of-gonstead"),
        ("The 5 Components", "gonstead-system"),
    ]),
    ("Patients", None, [
        ("First Visit", "first-visit"),
        ("Second Visit", "second-visit"),
        ("Follow-Up Visits", "follow-up-visit"),
        ("New Patient Paperwork", "new-patient-paperwork"),
        ("Payment Plans", "payment-plans"),
    ]),
    ("What We Do", "MEGA", [
        ("Services", [
            ("Athletes & Entertainers", "who-we-help-athletes-entertainers"),
            ("Chiropractic Adjustments", "chiropractic-adjustments"),
            ("CLA Insight Thermography", "cla-insight-thermography"),
            ("Education For Healthy Choices", "education-healthy-choices"),
            ("Pregnant Moms & Newborns", "who-we-help-pregnant-moms-newborns"),
            ("Therapeutic Exercises", "therapeutic-exercises"),
        ]),
        ("Spine Related", [
            ("Back Pain", "back-pain"),
            ("Headaches & Migraines", "headaches-migraines"),
            ("Neck Pain", "neck-pain"),
            ("Sciatica", "sciatica"),
            ("Scoliosis", "scoliosis"),
        ]),
        ("Injuries", [
            ("Accident Injury", "who-we-help-accident-injury-recovery"),
            ("Auto Injury", "car-accident"),
            ("Disc Injury", "disc-injury"),
            ("Personal Injury", "personal-injury"),
            ("Whiplash", "whiplash"),
            ("Work Injury", "work-injury"),
        ]),
        ("Extremities", [
            ("Arm & Leg Pain", "arm-leg-pain"),
            ("Carpal Tunnel", "carpal-tunnel"),
            ("Shoulder Pain", "shoulder-pain"),
        ]),
        ("Other Conditions", [
            ("Chiropractic For Kids", "pediatric-care-kids"),
            ("Pregnancy", "pregnancy"),
            ("Relief From Pain", "who-we-help-people"),
            ("Vertigo", "vertigo"),
            ("Wellness Care", "wellness-care"),
        ]),
    ]),
    ("Contact", None, [
        ("Contact Us", "contact-us"),
        ("FAQs", "faqs"),
        ("Opportunity Hub", "opportunity-hub"),
    ]),
]

LEGAL = [
    ("accessibility-statement", "Accessibility"),
    ("anti-discrimination-disclaimer", "Anti-Discrimination"),
    ("good-faith-estimate", "Good Faith Estimate"),
    ("healthcare-disclaimer", "Healthcare Disclaimer"),
    ("hipaa-privacy-practices", "HIPAA Privacy Practices"),
    ("privacy-policy", "Privacy Policy"),
    ("terms-of-service", "Terms of Service"),
]

QUICK = [
    ("Meet the Doctor", "meet-the-doctor"),
    ("First Visit", "first-visit"),
    ("Payment Plans", "payment-plans"),
    ("Testimonials", "testimonials"),
    ("Contact Us", "contact-us"),
    ("Back Pain", "back-pain"),
]


def prefix(depth):
    return "../" * depth


def book_href(depth=0):
    return prefix(depth) + BOOK


def href(slug, depth=0):
    pre = prefix(depth)
    if slug == "index":
        return pre + "index.html"
    if slug == "book-appointment":
        return book_href(depth)
    if slug == "back-pain":
        return pre + "back-pain/"
    if slug == "headaches-migraines":
        return pre + "headaches-migraines/"
    if slug == "neck-pain":
        return pre + "neck-pain/"
    if slug == "sciatica":
        return pre + "sciatica/"
    if slug == "scoliosis":
        return pre + "scoliosis/"
    if slug == "founder-of-gonstead":
        return pre + "founder-of-gonstead/"
    if slug == "gonstead-system":
        return pre + "gonstead-system/"
    if slug == "new-patient-paperwork":
        return pre + "new-patient-paperwork/"
    if slug == "first-visit":
        return pre + "first-visit/"
    if slug == "second-visit":
        return pre + "second-visit/"
    if slug == "follow-up-visit":
        return pre + "follow-up-visit/"
    if slug == "who-we-help-athletes-entertainers":
        return pre + "who-we-help-athletes-entertainers/"
    if slug == "who-we-help-pregnant-moms-newborns":
        return pre + "who-we-help-pregnant-moms-newborns/"
    if slug == "who-we-help-accident-injury-recovery":
        return pre + "who-we-help-accident-injury-recovery/"
    if slug == "car-accident":
        return pre + "car-accident/"
    if slug == "whiplash":
        return pre + "whiplash/"
    if slug == "work-injury":
        return pre + "work-injury/"
    if slug == "disc-injury":
        return pre + "disc-injury/"
    if slug == "personal-injury":
        return pre + "personal-injury/"
    if slug == "arm-leg-pain":
        return pre + "arm-leg-pain/"
    if slug == "carpal-tunnel":
        return pre + "carpal-tunnel/"
    if slug == "shoulder-pain":
        return pre + "shoulder-pain/"
    if slug == "pediatric-care-kids":
        return pre + "pediatric-care-kids/"
    if slug == "pregnancy":
        return pre + "pregnancy/"
    if slug == "who-we-help-people":
        return pre + "who-we-help-people/"
    if slug == "vertigo":
        return pre + "vertigo/"
    if slug == "wellness-care":
        return pre + "wellness-care/"
    if slug == "chiropractic-adjustments":
        return pre + "chiropractic-adjustments/"
    if slug == "therapeutic-exercises":
        return pre + "therapeutic-exercises/"
    if slug == "education-healthy-choices":
        return pre + "education-healthy-choices/"
    if slug == "cla-insight-thermography":
        return pre + "cla-insight-thermography/"
    if slug == "payment-plans":
        return pre + "payment-plans/"
    if slug == "testimonials":
        return pre + "testimonials/"
    if slug == "office-tour":
        return pre + "office-tour/"
    if slug == "meet-the-doctor":
        return pre + "meet-the-doctor/"
    if slug == "blog":
        return pre + "blog/"
    if slug == "contact-us":
        return pre + "contact-us/"
    if slug == "faqs":
        return pre + "faqs/"
    if slug == "opportunity-hub":
        return pre + "opportunity-hub/"
    if slug == "accessibility-statement":
        return pre + "accessibility-statement/"
    if slug == "anti-discrimination-disclaimer":
        return pre + "anti-discrimination-disclaimer/"
    if slug == "good-faith-estimate":
        return pre + "good-faith-estimate/"
    if slug == "healthcare-disclaimer":
        return pre + "healthcare-disclaimer/"
    if slug == "hipaa-privacy-practices":
        return pre + "hipaa-privacy-practices/"
    if slug == "privacy-policy":
        return pre + "privacy-policy/"
    if slug == "terms-of-service":
        return pre + "terms-of-service/"
    if slug == "site-map":
        return pre + "site-map.html"
    if slug in (
        "3-common-conditions-las-vegas-chiropractors-help",
        "achieve-a-healthier-spine-in-las-vegas",
        "are-you-looking-for-a-top-las-vegas-chiropractor",
        "back-pain-tips-from-a-las-vegas-chiropractor",
        "car-accident-tips-from-a-las-vegas-chiropractor",
        "chiropractic-for-pregnancy-in-las-vegas",
    ):
        return pre + slug + "/"
    return pre + "site-map.html#" + slug


def svg(body, vb="0 0 24 24"):
    return (
        f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


ICONS = {
    "phone": svg('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
    "pin": svg('<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.800 7 11 7 11z"/><circle cx="12" cy="10" r="2.500"/>'),
    "clock": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "mail": svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "chev": '<svg class="chev" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg>',
    "menu": svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "instagram": svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/>'),
    "facebook": svg('<path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h3l1-3h-4v-2c0-.6.4-1 1-1z"/>'),
    "tiktok": svg('<path d="M14.2 3v10.1a3.6 3.6 0 1 1-2.9-3.5V12a5.9 5.9 0 1 0 5.4 5.9V8.5A8 8 0 0 0 21 10.2V7.2A8 8 0 0 1 14.2 5.2V3z"/>'),
}

SOCIAL_LINKS = [
    ("Instagram", "https://www.instagram.com/evergrowthchiro", "instagram"),
    ("Facebook", "https://www.facebook.com/evergrowthchiro", "facebook"),
    ("TikTok", "https://www.tiktok.com/@evergrowthchiro", "tiktok"),
]
ALLOWED_SOCIAL_URLS = tuple(url.lower() for _label, url, _key in SOCIAL_LINKS)
PAPERWORK_HREF = "assets/evergrowth-new-patient-paperwork.pdf"


def paperwork_href(depth=1):
    return prefix(depth) + PAPERWORK_HREF
PAY_COPY = (
    "We work with several patient financing companies such as CareCredit, "
    "Cherry and Pay by HFA."
)


def social_list():
    items = []
    for label, url, key in SOCIAL_LINKS:
        href = html.escape(url, quote=True)
        items.append(
            f'<li><a href="{href}" target="_blank" rel="noopener" aria-label="{label}">{ICONS[key]}</a></li>'
        )
    return '<ul class="foot-social">' + "".join(items) + "</ul>"


def pay_box():
    return (
        '<div class="pay-box"><h2>Payment &amp; Financing</h2>'
        f"<p>{html.escape(PAY_COPY)}</p></div>"
    )


def has_unexpected_social(page):
    hosts = (
        "facebook.com",
        "instagram.com",
        "tiktok.com",
        "linkedin.com",
        "youtube.com",
        "twitter.com",
        "x.com",
    )
    urls = re.findall(r"https?://[^\s\"'<>]+", page.lower())
    for url in urls:
        if any(host in url for host in hosts) and not any(
            allowed in url for allowed in ALLOWED_SOCIAL_URLS
        ):
            return True
    return False


def unexpected_blank_targets(page, extra_allowed=()):
    allowed = ALLOWED_SOCIAL_URLS + tuple(item.lower() for item in extra_allowed)
    found = []
    for match in re.finditer(r'<a\b[^>]*>', page, flags=re.I):
        tag = match.group(0)
        if "target=" not in tag.lower():
            continue
        href_match = re.search(r'href="([^"]+)"', tag, flags=re.I)
        href = (href_match.group(1) if href_match else "").lower()
        if any(item in href for item in allowed):
            continue
        found.append(href or tag)
    return found


def link(slug, text, depth=0, cls=""):
    klass = f' class="{cls}"' if cls else ""
    return f'<a{klass} href="{href(slug, depth)}">{text}</a>'


def book_btn(depth=0, text="Book Appointment", cls=""):
    klass = "btn " + cls if cls else "btn"
    return f'<a class="{klass}" href="{book_href(depth)}">{text}</a>'


def nav_desktop(depth):
    out = []
    for label, slug, sub in NAV:
        if sub is None:
            out.append(f"<li>{link(slug, label, depth, 'nav-link')}</li>")
            continue
        if slug == "MEGA":
            cols = "".join(
                f'<div class="col"><h4>{group}</h4><ul>'
                + "".join(f"<li>{link(item_slug, item_label, depth)}</li>" for item_label, item_slug in items)
                + "</ul></div>"
                for group, items in sub
            )
            out.append(
                f'<li class="has-sub mega"><button class="nav-link" aria-expanded="false" aria-haspopup="true">{label}{ICONS["chev"]}</button><div class="sub">{cols}</div></li>'
            )
        else:
            items = "".join(f"<li>{link(item_slug, item_label, depth)}</li>" for item_label, item_slug in sub)
            out.append(
                f'<li class="has-sub"><button class="nav-link" aria-expanded="false" aria-haspopup="true">{label}{ICONS["chev"]}</button><ul class="sub">{items}</ul></li>'
            )
    return "<ul>" + "".join(out) + "</ul>"


def nav_mobile(depth):
    out = []
    for label, slug, sub in NAV:
        if sub is None:
            out.append(f'<div class="m-item">{link(slug, label, depth)}</div>')
            continue
        if slug == "MEGA":
            body = "".join(
                f"<h4>{group}</h4>" + "".join(link(item_slug, item_label, depth) for item_label, item_slug in items)
                for group, items in sub
            )
        else:
            body = "".join(link(item_slug, item_label, depth) for item_label, item_slug in sub)
        out.append(
            f'<div class="m-item"><button aria-expanded="false">{label}{ICONS["chev"]}</button><div class="m-sub">{body}</div></div>'
        )
    return "".join(out) + f'<div class="m-cta">{book_btn(depth, "Book Appointment", "btn-block")}</div>'


def render_page(title, description, body, depth=0):
    pre = prefix(depth)
    home = href("index", depth)
    hours = "".join(f"<li><span>{day}</span><span>{when}</span></li>" for day, when in HOURS)
    quick = "".join(f"<li>{link(slug, label, depth)}</li>" for label, slug in QUICK)
    legal = "".join(f"<li>{link(slug, label, depth)}</li>" for slug, label in LEGAL)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}">
<link rel="stylesheet" href="{pre}assets/style.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container hdr">
<a class="logo" href="{home}"><img src="{pre}assets/img/logo.png" alt="Evergrowth Chiropractic" width="171" height="58"></a>
<nav class="nav" aria-label="Main">{nav_desktop(depth)}{book_btn(depth, "Book Appointment", "hdr-cta")}</nav>
<button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="mobile-nav">{ICONS["menu"]}</button>
</div><div class="mobile-nav" id="mobile-nav">{nav_mobile(depth)}</div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="container">
<div class="foot-grid">
<div class="foot-logo"><a href="{home}"><img src="{pre}assets/img/logo-white.png" alt="Evergrowth Chiropractic" width="189" height="64"></a>
<p>Evergrowth Chiropractic provides personalized chiropractic care using the Gonstead Method, with a focus on precision, comfort, and patient-centered care. Our goal is to help you move, function, and live with greater confidence.</p>
{social_list()}</div>
<div><h4>Quick Links</h4><ul>{quick}</ul></div>
<div><h4>Hours</h4><ul class="hours-list">{hours}</ul></div>
<div><h4>Contact</h4><ul class="foot-contact">
<li>{ICONS["pin"]}<span>{ADDR1}<br>{ADDR2}</span></li>
<li>{ICONS["phone"]}<a href="{TEL}">{PHONE}</a></li>
<li>{ICONS["mail"]}<a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
<p style="margin-top:18px">{book_btn(depth, "Book Appointment")}</p></div>
</div>
<div class="legal"><div>Copyright &copy; 2026 Evergrowth Chiropractic. All Rights Reserved.</div><ul>{legal}</ul></div>
</div></footer>
<script src="{pre}assets/site.js"></script></body></html>'''


NOTICE = "This form is not active in this preview and will not accept a message."
CONCERNS = (
    "Back Pain",
    "Neck Pain",
    "Headaches",
    "Sciatica",
    "Posture / Spinal Concerns",
    "Wellness Care",
    "Other",
)
PATIENT_CHOICES = ("New Patient", "Existing Patient")


def book_page(depth=1):
    """Visual booking form. No action, no submit, no network request."""
    pre = prefix(depth)
    hours = "".join(
        f"<li><span>{day}</span><span>{when}</span></li>" for day, when in (
            ("Mon, Wed, Thu", "10am to 1pm, 3pm to 6pm"),
            ("Tuesday", "3pm to 6pm"),
            ("Friday", "Appointments only"),
            ("Sat, Sun", "Closed"),
        )
    )
    concern_options = "".join(f"<option>{html.escape(name)}</option>" for name in CONCERNS)
    patient_options = "".join(f"<option>{html.escape(name)}</option>" for name in PATIENT_CHOICES)
    body = f'''<section class="page-hero"><div class="container"><div class="crumbs"><a href="{pre}index.html">Home</a><span>/</span>Book Appointment</div><h1>Book Appointment</h1><p class="sub-h">{ADDR1}, {ADDR2}</p></div></section>
<section><div class="container book-layout"><form class="contact-form book-form" onsubmit="return false">
<p class="full form-notice" role="status">{NOTICE}</p>
<div><label for="first-name">First Name</label><input id="first-name" name="first-name" type="text" autocomplete="given-name"></div>
<div><label for="last-name">Last Name</label><input id="last-name" name="last-name" type="text" autocomplete="family-name"></div>
<div><label for="email">Email Address*</label><input id="email" name="email" type="email" autocomplete="email"></div>
<div><label for="phone">Phone Number</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
<div><label for="preferred-date">Preferred Date</label><input id="preferred-date" name="preferred-date" type="date"></div>
<div><label for="preferred-time">Preferred Time</label><input id="preferred-time" name="preferred-time" type="time"></div>
<div><label for="patient-type">New or Existing Patient</label><select id="patient-type" name="patient-type"><option selected>Select</option>{patient_options}</select></div>
<div><label for="concern">Concern</label><select id="concern" name="concern"><option selected>Select</option>{concern_options}</select></div>
<div class="full"><label for="notes">Additional Information</label><textarea id="notes" name="notes"></textarea></div>
<div class="full"><button class="btn" type="button" disabled>Send Message</button></div>
</form>
<div class="book-side"><div class="side-card"><h3>Contact Info</h3><p><a class="phone-link" href="{TEL}">{ICONS["phone"]}{PHONE}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div class="side-card"><h3>Hours</h3><ul>{hours}</ul></div></div></div></section>'''
    return render_page(
        "Book Appointment | Evergrowth Chiropractic",
        "Book an appointment at Evergrowth Chiropractic, 9555 S Eastern Ave, Ste 240B, Las Vegas, NV 89123.",
        body,
        depth,
    )
