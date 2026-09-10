#!/usr/bin/env python3
"""Generate the redesigned homepage (index.html). Run from `site/`:
    python3 scripts/build_homepage.py
"""
import json
from datetime import date
from pathlib import Path

from partials import (
    nav_html, footer_html, person_modal_html, head_html, end_scripts_html,
    donate_teaser_html, newsletter_widget_html, coalition_panel_html,
    ICON_READ, ICON_LISTEN, ICON_ASK, nbsp_single_letters, jsonld_script,
)

ELECTION_JSONLD = {
    "@context": "https://schema.org",
    "@type": "Event",
    "name": "Komunální volby 2026 v Brně",
    "startDate": "2026-10-09",
    "endDate": "2026-10-10",
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {
        "@type": "Place",
        "name": "Brno",
        "address": {"@type": "PostalAddress", "addressLocality": "Brno", "addressCountry": "CZ"},
    },
    "organizer": {"@type": "Organization", "name": "Zelené Brno", "url": "https://www.zelenebrno.cz/"},
}

ROOT = Path(__file__).resolve().parent.parent
PROCHAZKY_JSON = ROOT / "wp-content/themes/zeleni-new/assets/data/prochazky.json"

DESCRIPTION = ("Dobré město nedělají velká gesta, ale péče o tisíc detailů. Brno má skoro všechno, co dobré "
               "město potřebuje — přesto asi všichni cítíme, že Brno má na víc.")

PILLARS = [
    {"title": "Bydlení", "heading": "Aby bydlení nestálo půlku výplaty",
     "photo": "01bydleni.jpg",
     "text": ("Opravíme prázdné městské byty a co nejdřív je pronajmeme lidem. Postavíme nové a zařídíme, "
              "aby se výstavba nevlekla deset let jako ta družstevní. Místo dnešního chaosu bude jedna "
              "srozumitelná žádost o byt. A po developerech budeme chtít část bytů s dostupným nájmem, "
              "jako to má Vídeň.")},
    {"title": "Bezpečná mobilita", "heading": "Aby na brněnských ulicích nikdo neumíral",
     "photo": "04mobilita.jpg",
     "text": ("Zabezpečíme cesty do škol, zklidníme provoz v obytných ulicích a postavíme cyklostezky, po "
              "kterých se dá jet i s dětmi. Přednost dostanou místa, kde lidé sami říkají, že se necítí bezpečně.")},
    {"title": "Veřejný prostor a zeleň", "heading": "Aby se ve městě dalo žít i v létě",
     "photo": "02lavicka.jpg",
     "text": ("Vysadíme stromy do ulic, doplníme stín a vodní prvky a přestaneme kácet vzrostlé stromy jen "
              "proto, že pod zemí mají přednost kabely. A budeme je zalévat, protože bez toho výsadbu "
              "nepřežijí.")},
    {"title": "Doprava zdarma", "heading": "Aby šaliny byly důvodem nejet autem",
     "photo": "12tramvaje.jpg",
     "text": ("Zavedeme jízdné zdarma pro děti do 15 let, studenty a seniory nad 65 let, přidáme spoje "
              "i klimatizované vozy. V centru nebudeme tramvaje omezovat.")},
    {"title": "Školy a děti", "heading": "Aby děti měly dobrou školu i péči",
     "photo": "03vzdelani.jpg",
     "text": ("Každá brněnská škola má být kvalitní, ať dítě bydlí kdekoli. Podpoříme školní psychology "
              "a speciální pedagogy, nabídneme prostory pro pediatry ve čtvrtích, kde chybí, a začneme "
              "řešit nedostatek míst na středních školách.")},
    {"title": "Energie", "heading": "Abyste ušetřili za energie",
     "photo": "08energie.jpg",
     "text": ("Zateplíme městské domy, zastíníme je proti letnímu horku a dáme na střechy fotovoltaiku, "
              "ke které se přes komunitní energetiku dostanou i lidé v nájmu. SVJ a družstvům "
              "pomůžeme od posudku až po dotaci.")},
    {"title": "Prázdniny", "heading": "Aby rodiny zvládly devět týdnů prázdnin",
     "photo_path": "wp-content/uploads/sites/123/2026/06/yanapi-senaud-87n4IpQl6c4-unsplash-768x432.jpg",
     "text": ("Dovolená rodičů pokryje sotva polovinu léta, zbytek je logistický oříšek za nemalé peníze. "
              "Otevřeme družiny na celé léto a zavedeme dotované příměstské tábory za tisícovku týdně po "
              "vzoru Vídně.")},
    {"title": "Kultura a komunita", "heading": "Aby svobodná kultura měla střechu nad hlavou",
     "photo": "05kultura.jpg",
     "text": ("Brno má kulturní scénu, kterou mu jiná města závidí, jenže míst pro tvorbu ubývá, často bez "
              "náhrady. Zachováme a rozšíříme zkušebny na Kraví hoře a okolní prostory otevřeme komunitním "
              "aktivitám.")},
    {"title": "Otevřená radnice", "heading": "Aby se o Brně nerozhodovalo bez vás",
     "photo": "06komunita.jpg",
     "text": ("O změnách ve městě se bude rozhodovat s lidmi, kterých se týkají, a ne až po dokončení. "
              "Zveřejníme všechny záměry a budeme je projednávat s lidmi. A každý rok ukážeme, jak plníme "
              "vlastní závazky, včetně toho, co se nepovedlo.")},
]

# (name, district, photo path relative to prefix, or None)
TEAM = [
    ("Jana Drápalová", "Nový Lískovec", "wp-content/uploads/kandidati/kandidatka/02-jana-drapalova.jpg"),
    ("Petr Kunc", "Židenice", "wp-content/uploads/kandidati/kandidatka/05-petr-kunc.jpg"),
    ("Milada Blatná", "Komín", "wp-content/uploads/kandidati/kandidatka/09-milada-blatna.jpg"),
    ("Ivana Fajnorová", "Jundrov", "wp-content/uploads/kandidati/kandidatka/10-ivana-fajnorova.jpg"),
    ("Ludmila Kutálková", "Maloměřice a Obřany", "wp-content/uploads/sites/123/2026/09/ludmila-kutalkova.jpg"),
]

DARUJTE_TEXT = ("Kampaň stavíme na darech lidí, kterým jde o lepší Brno stejně jako nám. Každý váš dar "
                "znamená další leták do schránky, plakát ve čtvrti nebo setkání v ulici — něco, co náš "
                "program přiblíží dalším Brňanům a Brňankám.")

ARROW_ICON = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 6 15 12 9 18"></polyline></svg>'

PLACEHOLDER_ICON = '''<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-4-4 3-3-2-6 5"/></svg>'''


def pillar_card_html(prefix, p):
    extra = ""
    if p.get("extra_href"):
        extra = f'<a class="mt-3 inline-block text-[13px] font-bold text-green-deep underline underline-offset-2 hover:text-green transition" href="{p["extra_href"]}" rel="noopener" target="_blank">{p["extra_label"]} →</a>'
    if p.get("photo"):
        media = f'''<div class="relative aspect-[4/3] mb-5 -mx-8 -mt-8 max-md:-mx-6 max-md:-mt-6 overflow-hidden">
<img alt="{p['title']}" class="w-full h-full object-cover" src="{prefix}wp-content/uploads/sites/123/2026/09/temata/{p['photo']}"/>
</div>'''
    elif p.get("photo_path"):
        media = f'''<div class="relative aspect-[4/3] mb-5 -mx-8 -mt-8 max-md:-mx-6 max-md:-mt-6 overflow-hidden">
<img alt="{p['title']}" class="w-full h-full object-cover" src="{prefix}{p['photo_path']}"/>
</div>'''
    else:
        media = f'''<div class="pillar-placeholder -mx-8 -mt-8 max-md:-mx-6 max-md:-mt-6">
{PLACEHOLDER_ICON}
<span>{p['title']}</span>
</div>'''
    return f'''<div class="bg-white shadow-card p-8 max-md:p-6 flex flex-col">
{media}
<p class="font-display text-ink font-black text-[18px] uppercase tracking-tight leading-[1.2] mb-2">{p['heading']}</p>
<p class="text-[14px] leading-[1.55] text-black/70">{p['text']}</p>
{extra}
</div>'''


PROGRAM_TEASER = [
    (ICON_ASK, "Zeptejte se na program chatbota",
     "Program má 256 konkrétních opatření. Chatbot vám pomůže najít odpověď na to, co vás zajímá.",
     "Otevřít chat", "btn-pink", "program/#chat"),
    (ICON_LISTEN, "Poslechněte si program jako podcast",
     "Nechce se vám program číst? Poslechněte si o něm podcast.",
     "Poslechnout", "btn-ink", "program/#podcast"),
    (ICON_READ, "Přečtěte si program",
     "Kompletní program k procházení na webu i ke stažení jako PDF nebo eBook.",
     "Přečíst program", "btn-green", "program/"),
]


def program_teaser_html(prefix):
    return "\n".join(
        f'''<div class="bg-white shadow-card p-5">
<div class="flex items-center gap-2.5 mb-2">
<span class="w-5 h-5 block shrink-0 text-green-deep">{icon}</span>
<p class="font-display text-ink font-black text-[17px] uppercase tracking-tight leading-[1.2]">{heading}</p>
</div>
<p class="text-[17px] text-black/60 leading-[1.5] mb-3">{body}</p>
<a class="btn btn-md {btn_class} w-full" href="{prefix}{href}">{label}</a>
</div>'''
        for icon, heading, body, label, btn_class, href in PROGRAM_TEASER
    )


def person_card_html(prefix, name, district, photo):
    img = f'<img class="w-20 h-20 rounded-full object-cover object-[50%_25%] shadow-card" alt="{name}" src="{prefix}{photo}"/>'
    return f'''<li class="flex flex-col items-center text-center gap-2 w-[104px]">
{img}
<div class="leading-tight">
<strong class="block leading-tight">{name}</strong>
<span class="block text-black/60 text-[13px] leading-tight mt-1">{district}</span>
</div>
</li>'''


WEEKDAYS_CZ = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]


def prochazka_card_html(item, index):
    d = date.fromisoformat(item["date"])
    kdy = f"{WEEKDAYS_CZ[d.weekday()]} {d.day}. {d.month}. | {item['time']}"
    badge_class = "bg-pink" if index % 2 == 0 else "bg-green"
    return f'''<a class="group block bg-white shadow-card p-6" href="{item['url']}" rel="noopener" target="_blank">
<span class="inline-block {badge_class} text-ink font-name font-bold uppercase text-[13px] px-3 py-1 mb-3">{kdy}</span>
<h3 class="font-name text-[17px] font-extrabold leading-[1.25] text-ink tracking-tight mb-2">{item['title']}</h3>
<p class="text-[13px] text-black/60 leading-[1.4] mb-3">{item['desc']}</p>
<p class="text-[13px] text-black/50"><strong class="text-green-deep">{item['place']}</strong><br/>{item['people']}</p>
</a>'''


def nearest_prochazky_html(count=3):
    items = json.loads(PROCHAZKY_JSON.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    upcoming = sorted((i for i in items if i["date"] >= today), key=lambda i: i["date"])[:count]
    return "\n".join(prochazka_card_html(item, i) for i, item in enumerate(upcoming))


def build():
    prefix = ""
    pillars_html = "\n".join(pillar_card_html(prefix, p) for p in PILLARS)
    team_html = "\n".join(person_card_html(prefix, *t) for t in TEAM)
    prochazky_html = nearest_prochazky_html()

    main_html = f'''<section class="hero hero-angled relative bg-[#025B58] overflow-hidden pt-20 pb-20 px-14 max-nav:pt-14 max-nav:pb-12 max-nav:px-6 max-md:pt-10 max-md:pb-10 max-md:px-4">
<h1 class="sr-only">Zelené Brno — protože Brno má na víc</h1>
<div class="relative mx-auto max-w-[1100px] min-h-[350px] max-nav:min-h-0">

<div class="max-w-[420px] min-w-0 max-nav:max-w-none max-nav:pt-0 max-nav:text-center">
<img alt="" class="w-full max-w-[420px] mb-6 max-nav:mx-auto" src="{prefix}wp-content/uploads/sites/123/2026/09/protoze-brno-ma-na-vic.png"/>
<p class="font-svgd text-white text-[33px] max-md:text-[23px] leading-[1.3] max-w-[440px] max-nav:mx-auto">{nbsp_single_letters("Dobré město nedělají velká gesta, ale péče o tisíc detailů.")}</p>
<p class="font-svgd text-green text-[18px] max-md:text-[16px] font-bold mt-4 max-nav:mx-auto">Volte Zelené Brno ve volbách 9. a 10. října.</p>
</div>

<!-- Photo is absolutely placed against this same centered wrapper (not the
     raw viewport), so its right edge always lines up with the wrapper's
     edge — no overlap risk at any width. It spans the section's full height
     (negative top/bottom matching the section's own py-20) and is trimmed
     by the section's existing diagonal clip-path — the same cut the section
     already uses, not a new shape. -->
<div class="absolute top-[-80px] right-0 bottom-[-84px] w-[540px] max-nav:relative max-nav:top-0 max-nav:w-full max-nav:h-[440px] max-nav:mt-8">
<div class="absolute inset-0 translate-x-3 translate-y-3 bg-green" aria-hidden="true"></div>
<img alt="Natálie Vencovská" class="relative z-10 w-full h-full object-cover object-top" src="{prefix}wp-content/uploads/sites/123/2026/09/natalie-hlavni-foto.jpg"/>
<div class="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-black/60 to-transparent z-10" aria-hidden="true"></div>
<div class="absolute left-4 bottom-[13%] z-20 leading-none">
<div><p class="inline-block bg-pink text-ink font-name font-black text-[20px] px-4 py-2 mb-2">Natálie Vencovská</p></div>
<div><p class="inline-block bg-[#012f2d] text-white font-bold text-[16px] leading-[1.4] px-4 py-2">Lídryně kandidátky<br/>Designérka, odbornice na veřejný prostor</p></div>
</div>
</div>

</div>
</section>

<section class="bg-white pt-10 pb-10 px-14 max-md:pt-8 max-md:pb-8 max-md:px-5" id="diagnoza">
<div class="mx-auto max-w-[800px] text-center mb-16 max-md:mb-10">
<p class="font-svgd text-[28px] max-md:text-[21px] leading-[1.45] text-ink mb-6">Brno má skoro všechno, co dobré město potřebuje. Univerzity, kulturu, šaliny, přírodu na dosah. A pořád si drží lidské měřítko, díky kterému se tu dá žít sousedsky a&nbsp;normálně. Přesto asi všichni cítíme, že <strong>Brno má na víc</strong>.</p>
<p class="text-[18px] max-md:text-[16px] leading-[1.6] text-black/70">V Brně stojí 1&nbsp;592 městských bytů prázdných. Ulice patří spíš autům než dětem. A v létě je na nich nesnesitelné horko, protože chybí stromy a další zeleň. Radnice mezitím řeší arénu a lanovku.</p>
</div>
<div class="mx-auto max-w-[1040px]">
<h2 class="font-display text-ink font-black text-[26px] max-md:text-[22px] uppercase tracking-tight leading-[1.15] mb-8">Věci, do kterých se pustíme hned po volbách:</h2>
<div class="grid grid-cols-3 gap-6 max-nav:grid-cols-2 max-md:grid-cols-1 mb-10">
{pillars_html}
</div>
<div class="bg-[#f4faf6] p-8 max-md:p-5">
<p class="font-svgd text-black/70 font-bold text-[15px] uppercase tracking-[0.1em] mb-5">Chcete vědět víc?</p>
<div class="grid grid-cols-3 gap-4 max-nav:grid-cols-1">
{program_teaser_html(prefix)}
</div>
</div>
</div>
</section>

<section class="bg-paper pt-10 pb-24 px-14 max-md:pt-8 max-md:pb-14 max-md:px-5">
<div class="mx-auto max-w-[1040px]">
<div class="grid grid-cols-[2fr_1fr] gap-10 mb-10 items-start max-nav:grid-cols-1">
<div>
<h2 class="font-display text-ink font-black text-[40px] max-md:text-[30px] uppercase tracking-tight leading-[1.1] mb-6">Lidé, kteří v&nbsp;Brně už&nbsp;něco dokázali</h2>
<p class="text-[17px] leading-[1.6] text-black/75 mb-8">Na kandidátce ZELENÉ BRNO se spojilo sedm subjektů a lidé, kteří v Brně už něco dokázali. Pět starostů a starostek, kteří vedou radnice svých čtvrtí, právnička z bytové komise, živnostníci, zástupci kultury i lidé z občanské společnosti.</p>
<ul class="flex flex-wrap gap-x-6 gap-y-5 mb-8 list-none p-0">
{team_html}
</ul>
<div class="flex gap-4 flex-wrap">
<a class="btn btn-green btn-lg font-svgd" href="{prefix}kandidatka/">Celá kandidátka →</a>
<a class="btn btn-pink btn-lg font-svgd" href="{prefix}natalie-vencovska/">Více o lídryni →</a>
</div>
</div>
{coalition_panel_html(prefix)}
</div>
<div class="shadow-card-lg">
<img alt="Kandidátky a kandidáti Zeleného Brna" class="w-full h-auto aspect-[2048/724] object-cover block" src="{prefix}wp-content/uploads/sites/123/2026/06/andreamyska_zeleni090626-15-2-e1781014583804.jpg"/>
</div>
<p class="text-black/50 text-[13px] mt-3 text-center">Milada Blatná, Jana Drápalová, Jiří Malenovský, Ivana Fajnorová, Natálie Vencovská, Matouš Vencálek, Kristýna Fuchsová, Jasna Flamiková</p>
</div>
</section>

<section class="bg-ink py-14 px-14 max-md:py-10 max-md:px-5">
<div class="mx-auto max-w-[1040px]">
<div class="grid grid-cols-[1.4fr_1fr] gap-12 max-nav:grid-cols-1">
<div>
<h2 class="font-display text-white font-black text-[32px] max-md:text-[26px] uppercase tracking-tight leading-[1.15] mb-8">Tuhle kampaň táhnou lidé jako vy.</h2>
<p class="text-white/80 text-[15px] leading-[1.55] mb-6">{DARUJTE_TEXT}<br/><span class="text-white/50 text-[13px]">Jednorázový nebo pravidelný dar na lepší Brno poslalo už 183 lidí.</span></p>
{donate_teaser_html(prefix, button_class="btn btn-pink")}
</div>
<div class="flex flex-col justify-start border-l border-white/15 pl-12 max-nav:border-l-0 max-nav:border-t max-nav:pl-0 max-nav:pt-8">
<h2 class="font-display text-white font-black text-[32px] max-md:text-[26px] uppercase tracking-tight leading-[1.15] mb-4">Chcete pomoct i jinak než darem?</h2>
<div class="mb-5 overflow-hidden">
<img alt="Dobrovolník kampaně rozdává letáky" class="w-36 h-28 object-cover shadow-card float-right ml-3 mb-2" src="{prefix}wp-content/uploads/sites/123/2026/09/zapojte-se-akce.jpg"/>
<p class="text-white/70 text-[14px] leading-[1.55]">Hodí se nám hlavně vaše energie a čas — být v ulicích na našich stráncích, mluvit s lidmi, roznášet materiály nebo se přidat na happeningy.</p>
</div>
<a class="btn btn-green btn-lg self-start" href="{prefix}zapoj-se/">Zapojte se do kampaně</a>
<p class="text-white/50 text-[13px] mt-4">Do kampaně se už přidalo přes 70 lidí.</p>
</div>
</div>
</div>
</section>

<section class="bg-white py-24 px-14 max-md:py-14 max-md:px-5">
<div class="mx-auto max-w-[1040px]">
<div class="flex items-center justify-between gap-6 mb-12 max-md:flex-col max-md:items-start max-md:gap-4">
<h2 class="font-display text-ink font-black text-[36px] max-md:text-[28px] uppercase tracking-tight leading-[1.1]">Přijďte se potkat na naše procházky</h2>
<a class="btn-read-more" href="{prefix}prochazky/">Všechny procházky<span class="btn-read-more__icon">{ARROW_ICON}</span></a>
</div>
<div class="grid grid-cols-3 gap-6 max-nav:grid-cols-1" data-prochazky-widget data-prochazky-src="{prefix}wp-content/themes/zeleni-new/assets/data/prochazky.json">
{prochazky_html}
</div>
</div>
</section>

<section class="bg-[#f4faf6] py-10 px-14 max-md:py-8 max-md:px-5">
<div class="mx-auto max-w-[1040px] flex items-center gap-8 flex-wrap justify-between max-md:flex-col max-md:items-stretch">
<div class="shrink-0">
<p class="font-display text-ink font-black text-[20px] uppercase tracking-tight leading-tight mb-1">Nechejte na sebe kontakt</p>
<p class="text-[15px] font-bold text-black/70">Chcete vědět o dalších procházkách a akcích brněnských Zelených?</p>
</div>
{newsletter_widget_html("brno_newsletter", "", submit_label="Přihlásit se", variant="light")}
</div>
</section>'''

    html = f'''<!DOCTYPE html>
<html lang="cs">
<head>
{head_html("Zelené Brno", DESCRIPTION, prefix, "/", full_title="Zelené Brno – protože Brno má na víc!")}
{jsonld_script(ELECTION_JSONLD)}
<link href="{prefix}wp-content/themes/zeleni-new/assets/css/donate-form.css" rel="stylesheet"/>
<link href="{prefix}wp-content/themes/zeleni-new/assets/css/newsletter-form.css" rel="stylesheet"/>
</head>
<body class="home wp-singular page-template page-template-templates page-template-page-flexible page-template-templatespage-flexible-php page wp-embed-responsive wp-theme-zeleni-new font-sans bg-paper text-ink antialiased min-h-screen flex flex-col tribe-no-js">
{nav_html(prefix)}
<main class="site-main flex-1" id="site-main">{main_html}
</main><!-- /#site-main -->

{footer_html(prefix)}
{person_modal_html(prefix)}
{end_scripts_html(prefix)}
<script src="{prefix}wp-content/themes/zeleni-new/assets/js/donate-teaser.js"></script>
<script src="{prefix}wp-content/themes/zeleni-new/assets/js/newsletter-form.js"></script>
<script src="{prefix}wp-content/themes/zeleni-new/assets/js/prochazky-widget.js"></script>
</body>
</html>
'''
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("wrote index.html")


if __name__ == "__main__":
    build()
