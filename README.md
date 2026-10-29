# Evergrowth Chiropractic preview

Noindex static preview. Not the live client site.

Book Appointment uses the single path in `tools/shell.py` (`book-appointment/`), same tab.
Unbuilt menu items point at `site-map.html` until their pages are added.
Condition pages use `tools/condition.py`. Back Pain is `tools/page_back_pain.py`. Spine batch A is `tools/page_spine_a.py`. Injury batch B is `tools/page_injuries_b.py`. Injury and extremity batch C is `tools/page_injuries_c.py`. Rows that add another condition call `render_condition()`.
