#!/usr/bin/env python3
"""Generate the Natálie Vencovská profile page (natalie-vencovska/index.html).
Content ported from natalievencovska.cz so visitors don't have to leave the
campaign site to learn who she is. Run from `site/`:
    python3 scripts/build_natalie.py
"""
from pathlib import Path

from partials import nav_html, footer_html, closing_cta_html, person_modal_html, head_html, end_scripts_html

ROOT = Path(__file__).resolve().parent.parent

DESCRIPTION = ("Natálie Vencovská, lídryně kandidátky koalice Zelené Brno do komunálních voleb 2026 — "
               "designérka a odbornice na veřejný prostor.")

CV = [
    ("2026 – dosud", "Architektonický ateliér Archipop", "Koordinátorka městských intervencí"),
    ("2023 – dosud", "Jihomoravské inovační centrum", "Koordinátorka startupové komunity"),
    ("2024 – 2026", "Zlín Design Week", "Kurátorka a dramaturgyně"),
    ("2025", "Pitch Your Single Friend Brno", "Spoluzakladatelka"),
    ("2023 – 2026", "Design Kantýna", "Moderátorka podcastu"),
    ("2022 – 2023", "Swap Spot, Kolding, Dánsko", "Projektová manažerka"),
    ("2020 – 2022", "Designskolen Kolding", "Design pro planetu"),
    ("2017 – 2020", "Univerzita Tomáše Bati, Zlín", "Fashion design"),
]

SOCIAL_ICON_IG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg>'
SOCIAL_ICON_FB = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg>'


def cv_row_html(period, org, role):
    return f'''<div class="flex gap-6 py-4 border-b border-black/10 max-md:flex-col max-md:gap-1">
<p class="w-[150px] shrink-0 font-bold text-green-deep text-[14px]">{period}</p>
<div>
<p class="font-bold text-ink">{org}</p>
<p class="text-black/60 text-[15px]">{role}</p>
</div>
</div>'''


def build():
    prefix = "../"
    cv_html = "\n".join(cv_row_html(*row) for row in CV)

    main_html = f'''<section class="bg-white pt-16 pb-10 px-14 max-md:pt-10 max-md:pb-6 max-md:px-5">
<div class="mx-auto max-w-[900px] grid grid-cols-[1fr_1.3fr] gap-12 items-start max-nav:grid-cols-1">
<div>
<img alt="Natálie Vencovská" class="w-full aspect-[4/5] object-cover shadow-card-lg" src="{prefix}wp-content/uploads/sites/123/2026/09/natalie-louka.jpg"/>
</div>
<div>
<p class="font-svgd text-green-deep text-[16px] mb-2">Lídryně kandidátky ZELENÉ BRNO</p>
<h1 class="font-display text-ink font-black text-[48px] max-md:text-4xl uppercase tracking-tight leading-[1.05] mb-4">Natálie Vencovská</h1>
<p class="text-[15px] text-black/60 mb-6">Designérka, odbornice na veřejný prostor</p>
<div class="flex gap-3 mb-6">
<a aria-label="Instagram" class="w-10 h-10 bg-[#f4faf6] flex items-center justify-center text-green-deep hover:text-green transition" href="https://www.instagram.com/jmenomejenatalie/" rel="noopener" target="_blank"><span class="w-4 h-4 block">{SOCIAL_ICON_IG}</span></a>
<a aria-label="Facebook" class="w-10 h-10 bg-[#f4faf6] flex items-center justify-center text-green-deep hover:text-green transition" href="https://www.facebook.com/jmenomejenatalie" rel="noopener" target="_blank"><span class="w-4 h-4 block">{SOCIAL_ICON_FB}</span></a>
<a aria-label="E-mail" class="w-10 h-10 bg-[#f4faf6] flex items-center justify-center text-green-deep hover:text-green transition text-[13px] font-bold" href="mailto:natalie@zeleni.cz">@</a>
</div>
<article class="wysiwyg">
<p>Pocházím z malé vesničky u Hustopečí. Od mala jsem zvyklá mít přírodu hned za rohem a chodit všude pěšky.</p>
<p>Tři roky jsem žila v Dánsku, kde jsem vystudovala design a vedla organizaci Swap Spot zaměřenou na udržitelnost.</p>
<p>Do Brna jsem se vrátila, protože si myslím, že čistý vzduch, bezpečné ulice a zeleň na dosah nemusí být ani privilegium cizích zemí, ani výsada malých vesnic.</p>
<p>Profesně se věnuji dočasným zásahům do veřejného prostoru, a tak vím, že dobré změny jde dělat bez velkých investic a zároveň s lidmi, kterých se přímo týkají. Zároveň se věnuji startupové komunitě v Jihomoravském inovačním centru, kde denně řeším, jak nápady rychle převést do praxe.</p>
</article>
</div>
</div>
</section>

<section class="bg-[#f4faf6] py-16 px-14 max-md:py-10 max-md:px-5">
<div class="mx-auto max-w-[900px]">
<h2 class="font-display text-ink font-black text-[28px] max-md:text-[24px] uppercase tracking-tight leading-[1.1] mb-8">Co mám za sebou</h2>
{cv_html}
</div>
</section>

<section class="bg-white py-16 px-14 max-md:py-10 max-md:px-5">
<div class="mx-auto max-w-[900px] grid grid-cols-[1.2fr_1fr] gap-12 items-center max-nav:grid-cols-1">
<div>
<h2 class="font-display text-ink font-black text-[28px] max-md:text-[24px] uppercase tracking-tight leading-[1.1] mb-4">Nejsem sama</h2>
<p class="text-[16px] leading-[1.6] text-black/75 mb-6">Za kampaní Zelené Brno stojí celý tým lidí, kteří v Brně a jižní Moravě dělají zelenou politiku už řadu let. Bez nich by tahle kandidátka nevznikla.</p>
<a class="btn btn-green btn-lg font-svgd" href="{prefix}kandidatka/">Celá kandidátka →</a>
</div>
<img alt="Natálie Vencovská s kolegyněmi" class="w-full aspect-[4/3] object-cover shadow-card-lg" src="{prefix}wp-content/uploads/sites/123/2026/09/natalie-tym.jpg"/>
</div>
</section>'''

    html = f'''<!DOCTYPE html>
<html lang="cs">
<head>
{head_html("Natálie Vencovská", DESCRIPTION, prefix, "/natalie-vencovska/")}
</head>
<body class="wp-singular page-template font-sans bg-paper text-ink antialiased min-h-screen flex flex-col tribe-no-js">
{nav_html(prefix)}
<main class="site-main flex-1" id="site-main">{main_html}
{closing_cta_html(prefix)}
</main><!-- /#site-main -->

{footer_html(prefix)}
{person_modal_html(prefix)}
{end_scripts_html(prefix)}
</body>
</html>
'''
    out = ROOT / "natalie-vencovska"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    print("wrote natalie-vencovska/index.html")


if __name__ == "__main__":
    build()
