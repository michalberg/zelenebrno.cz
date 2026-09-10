#!/usr/bin/env python3
"""Generate /darujte/index.html. Run from `site/`: python3 scripts/build_darujte.py"""
from pathlib import Path

from partials import nav_html, footer_html, person_modal_html, head_html, end_scripts_html, donate_widget_html

ROOT = Path(__file__).resolve().parent.parent

DESCRIPTION = "Podpořte kampaň Zelené Brno darem. Každá koruna se promění v leták, plakát nebo setkání, které dostane naše návrhy k dalším Brňanům."

INTRO = ("Kampaň stavíme na darech lidí, kterým jde o lepší Brno stejně jako nám. Každý váš dar "
         "znamená další leták do schránky, plakát ve čtvrti nebo setkání v ulici — něco, co náš "
         "program přiblíží dalším Brňanům a Brňankám.")
INTRO_STAT = "Jednorázový nebo pravidelný dar na lepší Brno poslalo už 183 lidí."


def build():
    prefix = "../"
    main_html = f'''<section class="bg-white py-20 px-14 max-md:py-12 max-md:px-5">
<div class="mx-auto max-w-[800px]">
<h1 class="font-display text-ink font-black text-[56px] max-md:text-4xl uppercase tracking-tight leading-[1.1] mb-6">Darujte</h1>
<p class="text-[18px] leading-[1.6] text-black/80 mb-4">{INTRO}</p>
<p class="text-[15px] font-bold text-black/60 mb-12">{INTRO_STAT}</p>
{donate_widget_html()}
</div>
</section>'''
    html = f'''<!DOCTYPE html>
<html lang="cs">
<head>
{head_html("Darujte", DESCRIPTION, prefix, "/darujte/", og_image="https://zelenebrno.cz/wp-content/uploads/sites/123/2026/09/natalie-tym.jpg")}
<link href="{prefix}wp-content/themes/zeleni-new/assets/css/donate-form.css" rel="stylesheet"/>
</head>
<body class="wp-singular page-template page-darujte wp-embed-responsive wp-theme-zeleni-new font-sans bg-paper text-ink antialiased min-h-screen flex flex-col tribe-no-js">
{nav_html(prefix)}
<main class="site-main flex-1" id="site-main">{main_html}
</main><!-- /#site-main -->

{footer_html(prefix)}
{person_modal_html(prefix)}
{end_scripts_html(prefix, donate=True)}
</body>
</html>
'''
    out_dir = ROOT / "darujte"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print("wrote darujte/index.html")


if __name__ == "__main__":
    build()
