#!/usr/bin/env python3
"""Generate 404.html (repo root, "site/docs/"). Run from `site/docs/`:
    python3 scripts/build_404.py

GitHub Pages serves this file's content for any unmatched URL at any depth,
but the browser keeps the original (nonexistent) URL — so unlike every other
page here, this one MUST use absolute paths (prefix="/"), never a relative
"../" prefix, or its own CSS/JS/nav links would resolve against whatever
deep path 404'd instead of against the site root.
"""
from pathlib import Path

from partials import nav_html, footer_html, person_modal_html, head_html, end_scripts_html

ROOT = Path(__file__).resolve().parent.parent

DESCRIPTION = "Tuhle stránku jsme nenašli. Zkuste se vrátit na hlavní stránku nebo si přečíst volební program."


def build():
    prefix = "/"
    main_html = f'''<section class="bg-white py-24 px-14 max-md:py-14 max-md:px-5 text-center">
<div class="mx-auto max-w-[560px]">
<p class="font-name text-green-deep font-black text-[20px] tracking-[0.1em] mb-4">404</p>
<h1 class="font-display text-ink font-black text-[40px] max-md:text-3xl uppercase tracking-tight leading-[1.1] mb-6">Tuhle stránku jsme nenašli</h1>
<p class="text-[17px] leading-[1.6] text-black/70 mb-10">Možná jsme ji přesunuli, nebo je v adrese překlep. Zkuste se vrátit na hlavní stránku, nebo se podívat na náš volební program.</p>
<div class="flex gap-3 justify-center flex-wrap">
<a class="btn btn-green btn-lg" href="{prefix}">Domů</a>
<a class="btn btn-pink btn-lg" href="{prefix}program/">Volební program</a>
</div>
</div>
</section>'''
    html = f'''<!DOCTYPE html>
<html lang="cs">
<head>
{head_html("Stránka nenalezena", DESCRIPTION, prefix, "/404.html")}
</head>
<body class="wp-singular page-template page-404 wp-embed-responsive wp-theme-zeleni-new font-sans bg-paper text-ink antialiased min-h-screen flex flex-col tribe-no-js">
{nav_html(prefix)}
<main class="site-main flex-1" id="site-main">{main_html}
</main><!-- /#site-main -->

{footer_html(prefix)}
{person_modal_html(prefix)}
{end_scripts_html(prefix)}
</body>
</html>
'''
    (ROOT / "404.html").write_text(html, encoding="utf-8")
    print("wrote 404.html")


if __name__ == "__main__":
    build()
