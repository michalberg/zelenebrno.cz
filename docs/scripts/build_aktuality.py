#!/usr/bin/env python3
"""Generate /aktuality/index.html — index of press releases. Run from `site/`."""
from pathlib import Path

from partials import nav_html, footer_html, closing_cta_html, person_modal_html, head_html, end_scripts_html

ROOT = Path(__file__).resolve().parent.parent

DESCRIPTION = "Tiskové zprávy a aktuality koalice Zelené Brno k volbám do Zastupitelstva města Brna 2026."

# (date, title, slug, image)
ITEMS = [
    ("12.8.2026", "Pojďte pohlídat volby!", "komise/",
     "wp-content/uploads/sites/123/2026/08/komise-1-768x512.png"),
    ("25.6.2026", "Léto, které rodiny v Brně zvládnou", "prazdniny/",
     "wp-content/uploads/sites/123/2026/06/yanapi-senaud-87n4IpQl6c4-unsplash-768x432.jpg"),
    ("9.6.2026", "Brno má na víc, říkají Zelení. V široké koalici spojili zkušené osobnosti z radnic i nové tváře",
     "brno-ma-na-vic-rikaji-zeleni-v-siroke-koalici-spojili-zkusene-osobnosti-z-radnic-i-nove-tvare/",
     "wp-content/uploads/sites/123/2026/06/andreamyska_zeleni090626-12-768x512.jpg"),
    ("26.5.2026", "Na veřejná gymnázia a lycea v Brně se dostala méně než polovina uchazečů. Zelení chtějí městské lyceum",
     "na-verejna-gymnazia-a-lycea-v-brne-se-dostala-mene-nez-polovina-uchazecu-zeleni-chteji-mestske-lyceum/",
     "wp-content/uploads/sites/123/2026/05/f1digitals-omr-3723130-768x512.jpg"),
]


def card_html(prefix, date, title, slug, image):
    return f'''<a class="group block bg-white shadow-card" href="{prefix}{slug}">
<img alt="{title}" class="aspect-[16/10] w-full object-cover" src="{prefix}{image}"/>
<div class="p-6">
<p class="font-name text-green-deep font-bold text-[13px] uppercase tracking-[0.14em] mb-2">{date}</p>
<h2 class="font-name text-[20px] font-extrabold leading-[1.2] text-ink tracking-tight">{title}</h2>
</div>
</a>'''


def build():
    prefix = "../"
    cards = "\n".join(card_html(prefix, *item) for item in ITEMS)
    main_html = f'''<section class="bg-white py-20 px-14 max-md:py-12 max-md:px-5">
<div class="mx-auto max-w-[1040px]">
<h1 class="font-display text-ink font-black text-[56px] max-md:text-4xl uppercase tracking-tight leading-[1.1] mb-12">Aktuality</h1>
<div class="grid grid-cols-2 gap-8 max-md:grid-cols-1">
{cards}
</div>
</div>
</section>
{closing_cta_html(prefix)}'''
    html = f'''<!DOCTYPE html>
<html lang="cs">
<head>
{head_html("Aktuality", DESCRIPTION, prefix, "/aktuality/", og_image="https://www.zelenebrno.cz/wp-content/uploads/sites/123/2026/06/andreamyska_zeleni090626-12-1024x683.jpg")}
</head>
<body class="wp-singular page-template page-aktuality wp-embed-responsive wp-theme-zeleni-new font-sans bg-paper text-ink antialiased min-h-screen flex flex-col tribe-no-js">
{nav_html(prefix)}
<main class="site-main flex-1" id="site-main">{main_html}
</main><!-- /#site-main -->

{footer_html(prefix)}
{person_modal_html(prefix)}
{end_scripts_html(prefix)}
</body>
</html>
'''
    out_dir = ROOT / "aktuality"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print("wrote aktuality/index.html")


if __name__ == "__main__":
    build()
