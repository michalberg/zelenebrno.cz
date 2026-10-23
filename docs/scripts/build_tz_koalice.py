#!/usr/bin/env python3
"""Generate the press release about joining the Brno city coalition (2026–2030).
Run from `site/`:
    python3 scripts/build_tz_koalice.py
"""
from pathlib import Path

from partials import nav_html, footer_html, person_modal_html, head_html, end_scripts_html, nbsp_single_letters

ROOT = Path(__file__).resolve().parent.parent

SLUG = "zeleni-budou-soucasti-vedeni-brna"
DATE = "23.10.2026"
DATETIME = "2026-10-23T10:00:00+02:00"
TITLE = "Zelení budou součástí vedení Brna, Natálie Vencovská má vést resort životního prostředí"
DESCRIPTION = ("Zelené Brno podepsalo koaliční smlouvu na období 2026–2030. Do programového prohlášení rady "
               "města se dostaly klíčové priority z volebního programu.")
# Provizorní náhled — po podpisu smlouvy stačí přepsat oba soubory fotkou z podpisu.
IMAGE = "wp-content/uploads/sites/123/2026/10/zeleni-ve-vedeni-brna-1024.jpg"
IMAGE_SMALL = "wp-content/uploads/sites/123/2026/10/zeleni-ve-vedeni-brna-768.jpg"

BODY = [
    "<b>Brno, 23. 10. 2026</b> – Zelené Brno bude součástí vedení Brna pro volební období 2026–2030, jeho "
    "zástupkyně a zástupci podepsali koaliční smlouvu. Do programového prohlášení rady města se dostaly klíčové "
    "priority z volebního programu. Účast v koalici schválila hlasováním členská základna Strany zelených "
    "v Brně jasnou většinou.",

    "„Od voličů jsme dostali nejsilnější mandát za posledních dvacet let a šli jsme vyjednávat, abychom "
    "prosadili co nejvíce z našeho programu. Při jednáních se ukázalo, že mnohá témata, včetně dostupného "
    "bydlení nebo kvalitního veřejného prostoru, jsou důležitá i pro další strany. To se promítlo do finálního "
    "programu. Naše účast v koalici stojí na dohodě, že se bude plnit,“ říká lídryně Zeleného Brna "
    "<b>Natálie Vencovská</b>, která by se měla stát náměstkyní primátora pro životní prostředí a udržitelný "
    "rozvoj města.",

    "Programové prohlášení v oblasti životního prostředí obsahuje zelené priority, jimiž jsou koncepční plán "
    "výsadby zeleně, ochrana stromů při rekonstrukcích i rozvoj obnovitelných zdrojů.",

    "„Dobré město poznáte podle detailů. Resort životního prostředí ovlivňuje to, jak se v Brně bude žít "
    "v horkém létě, a teď máme nástroje, jak ty detaily zařídit. Na proměně ulic budu spolupracovat "
    "s Kateřinou Basel, která povede územní plánování, a s Adamem Zemkem, který povede dopravu. V tom, jak mají "
    "brněnské ulice vypadat, si zatím rozumíme,“ dodává <b>Natálie Vencovská</b>.",

    "Zelení budou ovlivňovat i druhé klíčové téma, kterým je bydlení. Programové prohlášení zavazuje město "
    "ukončit prodej bytů, bytových domů a pozemků vhodných pro výstavbu a z bydlení se stává priorita celého "
    "vedení města.",

    "„Bydlení pro nás bylo během vyjednávání klíčové. Do programu se dostalo to podstatné: město přestane byty "
    "prodávat a začne je stavět. Program řeší také férová pravidla pronajímání bytů, žádosti o městské byty "
    "nebo sociální a krizové bydlení. Získáme navíc možnost výstavbu bytů ovlivňovat, nominujeme totiž "
    "předsedu představenstva Realitní společnosti města Brna, která má výstavbu nových městských bytů "
    "na starosti,“ říká předsedkyně klubu zastupitelů Zeleného Brna <b>Jana Drápalová</b>.",

    "Do programového prohlášení se dostaly i další priority Zelených, jako zlevnění jízdného pro Brňany "
    "a Brňanky, bezplatné jízdné v MHD pro děti do 15 let a seniory od 65 let, konec projektu lanovky "
    "na kampus nebo revitalizace přednádražního prostoru. Ulice Veveří se změní v moderní městský bulvár, "
    "město také omezí reklamu na svých pozemcích a bude odstraňovat nelegální billboardy. Důraz bude kladen "
    "i na vyšší bezpečnost ulic pro chodce a cyklisty.",

    "Programové prohlášení obsahuje opatření pro rovné příležitosti a kvalitní vzdělávání všech dětí, včetně "
    "podpory romských dětí a dětí cizinců. Právnička Kristýna Fuchsová bude uvolněnou předsedkyní výboru "
    "zastupitelstva pro národnostní menšiny.",

    "„O uvolněnou funkci předsedkyně výboru jsme usilovali, protože Brno je dnes rozmanité a multikulturní "
    "město. Podíl cizinců, kteří tu žijí, se za dvacet let zvýšil pětinásobně a vedle podpory tradičních "
    "národnostních menšin potřebujeme řešit i sociální vyloučení, rovné příležitosti ve vzdělávání či integraci "
    "uprchlíků z Ukrajiny a dalších skupin cizinců žijících v Brně,“ říká <b>Kristýna Fuchsová</b>. „Na "
    "konkrétních řešeních budu spolupracovat s náměstkyní pro sociální věci Marií Jílkovou, která má na tato "
    "témata velmi podobný pohled,“ dodává.",
]


def build():
    prefix = "../"
    body_html = "\n".join(f"<p>{nbsp_single_letters(p)}</p>" for p in BODY)
    main_html = f'''<section class="bg-white py-20 px-14 max-md:py-12 max-md:px-5">
<div class="mx-auto max-w-[800px]">
<p class="font-name text-green-deep font-bold text-[15px] uppercase tracking-[0.18em] mb-6">Tisková zpráva · {DATE}</p>
<h1 class="font-display text-ink font-black text-[56px] max-md:text-4xl uppercase tracking-tight leading-[1.1] mb-10">{TITLE}</h1>
<div class="mb-10">
<img alt="Zastupitelky a kandidátky Zeleného Brna" class="w-full h-auto shadow-card" decoding="async" fetchpriority="high" src="{prefix}{IMAGE}" width="1024" height="575"/>
</div>
<article class="wysiwyg">
{body_html}
</article>
<div class="wysiwyg-meta">
<span class="wysiwyg-meta__item">
<span class="wysiwyg-meta__label">Publikováno:</span>
<time datetime="{DATETIME}">{DATE}</time>
</span>
</div>
<div class="bg-[#f4faf6] p-8 max-md:p-6 mt-10">
<p class="font-name font-black text-[22px] leading-tight text-ink mb-3">Co přesně jsme vyjednali?</p>
<p class="text-[16px] leading-[1.6] text-black/75 mb-5">{nbsp_single_letters("Podrobný přehled toho, co se z našeho programu dostalo do programového prohlášení, popis resortu životního prostředí a odpovědi na další otázky, třeba proč jsme v koalici s ODS nebo co když se program nebude plnit, najdete na hlavní stránce.")}</p>
<div class="flex gap-3 flex-wrap">
<a class="btn btn-green" href="{prefix}#vyjednali">Co jsme prosadili →</a>
<a class="btn btn-ink" href="{prefix}#otazky">Časté otázky →</a>
</div>
</div>
</div>
</section>
<section class="bg-ink py-16 px-14 text-center max-md:py-12 max-md:px-5">
<div class="mx-auto max-w-[680px]">
<h2 class="font-display text-white font-black text-[38px] uppercase tracking-tight leading-[1.15] mb-8 max-md:text-[28px]">Teď začíná práce</h2>
<p class="text-white/75 text-[16px] leading-[1.6] mb-8">{nbsp_single_letters("Pomozte nám, aby se program propsal do ulic a čtvrtí.")}</p>
<div class="flex gap-3 justify-center flex-wrap">
<a class="btn btn-green btn-lg" href="{prefix}zapoj-se/">Zapojte se</a>
<a class="btn btn-pink btn-lg" href="{prefix}darujte/">Darujte</a>
</div>
</div>
</section>'''
    og_image = f"https://www.zelenebrno.cz/{IMAGE}"
    html = f'''<!DOCTYPE html>
<html lang="cs">
<head>
{head_html(TITLE, DESCRIPTION, prefix, f"/{SLUG}/", og_image=og_image)}
</head>
<body class="post-template-default single single-post wp-embed-responsive wp-theme-zeleni-new font-sans bg-paper text-ink antialiased min-h-screen flex flex-col tribe-no-js">
{nav_html(prefix)}
<main class="site-main flex-1" id="site-main">{main_html}
</main><!-- /#site-main -->

{footer_html(prefix)}
{person_modal_html(prefix)}
{end_scripts_html(prefix)}
</body>
</html>
'''
    out_dir = ROOT / SLUG
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"wrote {SLUG}/index.html")


if __name__ == "__main__":
    build()
