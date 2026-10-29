# Evergrowth Chiropractic preview

Noindex static preview. Not the live client site.

Book Appointment uses the single path in `tools/shell.py` (`book-appointment/`), same tab. The page is `tools/page_book.py`: a visual form that does not submit.
Unbuilt menu items point at `site-map.html` until their pages are added.
Condition pages use `tools/condition.py`. Back Pain is `tools/page_back_pain.py`. Spine batch A is `tools/page_spine_a.py`. Injury batch B is `tools/page_injuries_b.py`. Injury and extremity batch C is `tools/page_injuries_c.py`. Other conditions batch D is `tools/page_other_d.py`. Services batch is `tools/page_services.py`. Follow Up Visit is `tools/page_follow_up.py`. Payment Plans is `tools/page_payment_plans.py`. Testimonials is `tools/page_testimonials.py`. Office Tour is `tools/page_office_tour.py`. Meet the Doctor is `tools/page_meet_the_doctor.py`. Legal batch 1 is `tools/page_legal_a.py`. Legal batch 2 is `tools/page_legal_b.py`. Blog index is `tools/page_blog.py`. Blog posts batch 1 is `tools/page_blog_posts_a.py`. Form confirmation is `tools/page_thank_you.py` at `thank-you-form/`. Rows that add another condition call `render_condition()`.
