#!/usr/bin/env python3
"""Patch the existing (pre-redesign) pages in place:
  - swap nav/footer for the updated shared partials (internal Darujte CTA,
    footer utility row)
  - insert meta description / canonical / OG tags (previously missing)
  - add the floating-widget CSS/JS includes
  - append the shared closing CTA block (Darujte + Zapojte se) where relevant

Run from the `site/` directory: python3 scripts/patch_existing_pages.py
"""
import re
from pathlib import Path

from partials import nav_html, footer_html, closing_cta_html, end_scripts_html

ROOT = Path(__file__).resolve().parent.parent

# path (relative to site/), meta description, whether to append the closing CTA
PAGES = [
    ("jak-volit/index.html",
     "Kdy a jak volit v komunálních volbách 2026 v Brně: termíny, doklady a praktické informace k hlasování.",
     True),
    ("kandidatka/index.html",
     "Kompletní kandidátní listina koalice ZELENÉ BRNO pro komunální volby do Zastupitelstva města Brna 2026.",
     True),
    ("kandidatka-brno-stred/index.html",
     "Kandidátní listina koalice Žít Zelené Brno pro volby do Zastupitelstva městské části Brno-střed 2026.",
     True),
    ("komise/index.html",
     "Staňte se členem nebo členkou okrskové volební komise a pohlídejte průběh voleb v Brně.",
     True),
    ("prazdniny/index.html",
     "Jak chce Zelené Brno pomoct rodinám zvládnout devět týdnů letních prázdnin bez zbytečného stresu a nákladů.",
     True),
    ("prochazky/index.html",
     "Procházky po Brně s kandidátkami a kandidáty koalice ZELENÉ BRNO po místech, o kterých mluvíme v programu.",
     True),
    ("reklama/index.html",
     "Transparentní informace o politické reklamě koalice ZELENÉ BRNO pro komunální volby 2026.",
     False),
    ("zapoj-se/index.html",
     "Zapojte se do kampaně Zelené Brno – jako dobrovolník, dobrovolnice nebo podporovatel v ulicích i online.",
     False),
    ("brno-ma-na-vic-rikaji-zeleni-v-siroke-koalici-spojili-zkusene-osobnosti-z-radnic-i-nove-tvare/index.html",
     "Zelení v Brně představují širokou koalici Zelené Brno se zkušenými starosty a starostkami i novými tvářemi.",
     True),
    ("na-verejna-gymnazia-a-lycea-v-brne-se-dostala-mene-nez-polovina-uchazecu-zeleni-chteji-mestske-lyceum/index.html",
     "Na veřejná gymnázia a lycea v Brně se letos dostalo jen 44 % uchazečů. Zelení navrhují zřídit městské lyceum.",
     True),
    ("mestske-casti/index.html",
     "Přehled městských částí Brna, kde kandiduje koalice Zelené Brno, a odkazy na kandidátky jednotlivých čtvrtí.",
     True),
]


def depth_prefix(rel_path):
    depth = rel_path.count("/")
    return "../" * depth


def patch_file(rel_path, description, add_closing_cta):
    path = ROOT / rel_path
    html = path.read_text(encoding="utf-8")
    prefix = depth_prefix(rel_path)
    canonical_path = "/" + rel_path.rsplit("index.html", 1)[0]

    # 1) nav + mobile overlay
    html, n = re.subn(
        r"<!-- Nav -->.*?(?=<main)",
        lambda m: nav_html(prefix) + "\n",
        html,
        count=1,
        flags=re.S,
    )
    assert n == 1, f"nav not replaced in {rel_path}"

    # 2) footer
    html, n = re.subn(
        r"<!-- Footer -->.*?</footer>",
        lambda m: footer_html(prefix),
        html,
        count=1,
        flags=re.S,
    )
    assert n == 1, f"footer not replaced in {rel_path}"

    # 3) meta description / canonical / OG — insert after the robots meta tag
    if "name=\"description\"" not in html:
        title_match = re.search(r"<title>(.*?)</title>", html)
        full_title = title_match.group(1) if title_match else "Zelené Brno"
        meta_block = (
            f'<meta name="description" content="{description}"/>\n'
            f'<link rel="canonical" href="https://zelenebrno.cz{canonical_path}"/>\n'
            f'<meta property="og:type" content="website"/>\n'
            f'<meta property="og:site_name" content="Zelené Brno"/>\n'
            f'<meta property="og:title" content="{full_title}"/>\n'
            f'<meta property="og:description" content="{description}"/>\n'
            f'<meta property="og:url" content="https://zelenebrno.cz{canonical_path}"/>\n'
            f'<meta name="twitter:card" content="summary_large_image"/>\n'
        )
        html, n = re.subn(
            r'(<meta content="max-image-preview:large" name="robots"/>\n)',
            lambda m: m.group(1) + meta_block,
            html,
            count=1,
        )
        assert n == 1, f"robots meta anchor not found in {rel_path}"

    # 4) floating-widget stylesheet (next to the main stylesheet link)
    if "floating-widget.css" not in html:
        html, n = re.subn(
            r'(<link href="[^"]*assets/css/styles\.css" id="zeleni-main-css"[^>]*/>\n)',
            lambda m: m.group(1) + f'<link href="{prefix}wp-content/themes/zeleni-new/assets/css/floating-widget.css" rel="stylesheet"/>\n',
            html,
            count=1,
        )
        assert n == 1, f"styles.css anchor not found in {rel_path}"

    # 5) floating-widget script (next to the main JS include)
    if "floating-widget.js" not in html:
        html, n = re.subn(
            r'(<script id="zeleni-main-js" src="[^"]*"></script>\n)',
            lambda m: m.group(1) + f'<script src="{prefix}wp-content/themes/zeleni-new/assets/js/floating-widget.js"></script>\n',
            html,
            count=1,
        )
        assert n == 1, f"main.js anchor not found in {rel_path}"

    # 6) closing CTA block, right before </main>
    if add_closing_cta and "Tuhle kampaň táhnou lidé jako vy." not in html:
        html, n = re.subn(
            r"</main>",
            lambda m: closing_cta_html(prefix) + "\n</main>",
            html,
            count=1,
        )
        assert n == 1, f"</main> anchor not found in {rel_path}"

    path.write_text(html, encoding="utf-8")
    print(f"patched {rel_path}")


if __name__ == "__main__":
    for rel_path, description, add_closing_cta in PAGES:
        patch_file(rel_path, description, add_closing_cta)
