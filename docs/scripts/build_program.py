#!/usr/bin/env python3
"""Generate /program/index.html and the 11 /program/<slug>/index.html chapter
pages from foto/program_final.md. Run from the `site/` directory:

    python3 scripts/build_program.py
"""
import re
from pathlib import Path

from parse_program import parse
from partials import (
    nav_html, footer_html, closing_cta_html, person_modal_html,
    head_html, end_scripts_html, ICON_READ, ICON_LISTEN, ICON_ASK,
    newsletter_widget_html, nbsp_single_letters,
)

ROOT = Path(__file__).resolve().parent.parent


def meta_description(text, limit=155):
    text = re.sub(r"<[^>]+>", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut + "…"


def page_shell(*, title, description, prefix, canonical_path, body_class, main_html, extra_body="", extra_scripts="", extra_head="", og_image=None):
    return f'''<!DOCTYPE html>
<html lang="cs">
<head>
{head_html(title, description, prefix, canonical_path, og_image=og_image)}
{extra_head}
</head>
<body class="{body_class} wp-embed-responsive wp-theme-zeleni-new font-sans bg-paper text-ink antialiased min-h-screen flex flex-col tribe-no-js">
{nav_html(prefix)}
<main class="site-main flex-1" id="site-main">{main_html}
</main><!-- /#site-main -->

{footer_html(prefix)}
{person_modal_html(prefix)}
{extra_body}
{end_scripts_html(prefix)}
{extra_scripts}
</body>
</html>
'''


CHAPTER_PHOTOS = {
    "dostupne-bydleni-a-vystavba": "01bydleni.jpg",
    "bezpecna-doprava": "04mobilita.jpg",
    "zelen-voda-a-stin-ve-meste": "02lavicka.jpg",
    "skoly-deti-rodiny-a-sport": "03vzdelani.jpg",
    "kultura-a-komunitni-zivot": "11kulturabalon.jpg",
    "otevrena-radnice-a-dobre-hospodareni": "06komunita.jpg",
    "verejny-prostor-pro-lidi": "07verejnyprostor.jpg",
    "energie-odpady-a-ciste-mesto": "08energie.jpg",
    "pece-o-seniory-a-lidi-v-nouzi": "09seniori.jpg",
    "zdravi-bezpeci-a-krizova-pripravenost": "10nemocnice.jpg",
    "mistni-ekonomika-a-zive-centrum": "11zivecentrum.jpg",
}

PLACEHOLDER_ICON = '''<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-4-4 3-3-2-6 5"/></svg>'''


def chapter_card_html(prefix, ch):
    num = f"{ch['num']:02d}"
    photo = CHAPTER_PHOTOS.get(ch["slug"])
    if photo:
        media = f'''<div class="relative aspect-[4/3] mb-5 -mx-8 -mt-8 max-md:-mx-6 max-md:-mt-6 overflow-hidden">
<img alt="{ch['title']}" class="w-full h-full object-cover" src="{prefix}wp-content/uploads/sites/123/2026/09/temata/{photo}"/>
</div>'''
    else:
        media = f'''<div class="pillar-placeholder -mx-8 -mt-8 max-md:-mx-6 max-md:-mt-6">
{PLACEHOLDER_ICON}
<span>{ch['title']}</span>
</div>'''
    return f'''<a class="group block bg-white shadow-card p-8 max-md:p-6 flex flex-col" href="{prefix}program/{ch['slug']}/">
{media}
<span class="font-name text-green-deep font-black text-[15px] tracking-[0.1em] mb-3">{num}</span>
<h3 class="font-display text-ink font-black text-[24px] uppercase leading-[1.12] tracking-tight">{nbsp_single_letters(ch['title'])}</h3>
</a>'''


def program_formats_html(prefix):
    base = f"{prefix}wp-content/uploads/sites/123/2026/09/program"
    return f'''<section class="bg-[#f4faf6] py-10 px-14 max-md:py-8 max-md:px-5">
<div class="mx-auto max-w-[1040px]">
<div class="grid grid-cols-2 gap-4 max-md:grid-cols-1">
<div class="bg-white shadow-card p-5">
<div class="flex items-center gap-2.5 mb-2">
<span class="w-5 h-5 block shrink-0 text-green-deep">{ICON_ASK}</span>
<p class="font-display text-ink font-black text-[17px] uppercase tracking-tight leading-[1.2]">Chatujte s chatbotem o programu</p>
</div>
<p class="text-[17px] text-black/60 leading-[1.5] mb-3">Program má 256 konkrétních opatření. Chatbot vám pomůže najít odpověď na to, co vás zajímá.</p>
<button type="button" class="btn btn-md btn-pink w-full" data-open-program-chat>Otevřít chat</button>
</div>
<div class="bg-white shadow-card p-5 scroll-mt-32" id="podcast">
<div class="flex items-center gap-2.5 mb-2">
<span class="w-5 h-5 block shrink-0 text-green-deep">{ICON_LISTEN}</span>
<p class="font-display text-ink font-black text-[17px] uppercase tracking-tight leading-[1.2]">Poslechněte si program jako podcast</p>
</div>
<p class="text-[17px] text-black/60 leading-[1.5] mb-3">Nechce se vám program číst? Poslechněte si o něm podcast.</p>
<iframe style="border-radius:0" src="https://open.spotify.com/embed/playlist/2iODjU1CXFGEv87HUgcVIH?utm_source=generator" width="100%" height="152" frameborder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
</div>
</div>
<p class="text-center text-[15px] font-bold mt-4">
<a class="text-green-deep underline underline-offset-2 hover:text-green transition" href="{base}/brno-do-detailu.pdf" download>Stáhnout jako PDF</a>
<span class="mx-2 text-black/30">·</span>
<a class="text-green-deep underline underline-offset-2 hover:text-green transition" href="{base}/brno-do-detailu.epub" download>Stáhnout jako eBook (.epub)</a>
</p>
</div>
</section>'''


PROGRAM_CHAT_QUESTIONS = [
    "Co plánujete s prázdnými byty?",
    "Jak chcete zlepšit dopravu?",
    "Co uděláte pro zeleň ve městě?",
    "Jak podpoříte školy?",
]

CHAPTER_CHAT_QUESTIONS = {
    1: [
        "Co plánujete s prázdnými byty?",
        "Jak chcete zlevnit bydlení?",
        "Jak budou fungovat pravidla pro přidělování bytů?",
    ],
    2: [
        "Jak zajistíte bezpečné cesty do škol?",
        "Bude MHD zdarma?",
        "Co uděláte pro cyklisty?",
    ],
    3: [
        "Jak omezíte reklamu v ulicích?",
        "Co uděláte pro bezpečné ulice?",
        "Jak vzniknou nová místa k posezení?",
    ],
    4: [
        "Kolik stromů plánujete vysadit?",
        "Jak chcete zadržet dešťovou vodu ve městě?",
        "Co uděláte s nejteplejšími místy ve městě?",
    ],
    5: [
        "Jak chcete snížit ceny tepla?",
        "Jak zlepšíte třídění odpadu?",
        "Odkud bude Brno brát energii?",
    ],
    6: [
        "Bude dost míst ve školkách?",
        "Jak pomůžete rodinám o prázdninách?",
        "Co uděláte pro sport?",
    ],
    7: [
        "Jak pomůžete seniorům zůstat doma?",
        "Co uděláte s bytovou nouzí?",
        "Jak pomůžete lidem v exekuci?",
    ],
    8: [
        "Jak zlepšíte dostupnost lékařů?",
        "Co uděláte pro bezpečnost ve městě?",
        "Jak je Brno připravené na krize?",
    ],
    9: [
        "Jak zprůhledníte hospodaření radnice?",
        "Jak budou moct lidé zasahovat do rozhodování?",
        "Co uděláte s financemi města?",
    ],
    10: [
        "Jak oživíte centrum města?",
        "Co uděláte pro místní podnikatele?",
        "Jak řešíte prázdné obchody?",
    ],
    11: [
        "Jak podpoříte nezávislou kulturu?",
        "Co bude s kinem Scala?",
        "Jak podpoříte komunitní centra?",
    ],
}


def program_chat_modal_html(questions=None):
    chips = "\n".join(
        f'<button type="button" class="program-chat-modal__chip" data-chat-question>{q}</button>'
        for q in (questions or PROGRAM_CHAT_QUESTIONS)
    )
    return f'''<div class="program-chat-modal" aria-hidden="true" data-program-chat-modal hidden>
<div class="program-chat-modal__backdrop" data-program-chat-close></div>
<div class="program-chat-modal__box" role="dialog" aria-modal="true" aria-label="Chat o programu">
<button type="button" class="program-chat-modal__close" data-program-chat-close aria-label="Zavřít">
<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewBox="0 0 24 24"><line x1="18" x2="6" y1="6" y2="18"></line><line x1="6" x2="18" y1="6" y2="18"></line></svg>
</button>
<h3 class="font-display text-ink font-black text-[22px] uppercase tracking-tight mb-2">Zeptejte se na program</h3>
<p class="text-black/60 text-[14px] mb-4">Zkuste například:</p>
<div class="flex flex-wrap gap-2 mb-5">
{chips}
</div>
<form data-program-chat-form>
<textarea class="program-chat-modal__input" rows="3" placeholder="Napište svůj dotaz…" data-chat-input></textarea>
<button type="submit" class="btn btn-green mt-3" data-chat-submit>Odeslat</button>
</form>
<div class="program-chat-modal__answer" data-chat-answer hidden></div>
<p class="text-[12px] text-black/40 mt-3">Odpovědi generuje AI na základě volebního programu — může se splést, ověřte si důležité informace přímo v textu programu.</p>
</div>
</div>'''


def build_index(intro, chapters):
    prefix = "../"
    cards = "\n".join(chapter_card_html(prefix, ch) for ch in chapters)
    intro_desc = meta_description(intro["paragraphs_raw"][0])
    main_html = f'''<section class="bg-white pt-20 pb-12 px-14 max-md:pt-12 max-md:pb-8 max-md:px-5">
<div class="mx-auto max-w-[1040px]">
<h1 class="font-display text-ink font-black text-[56px] max-md:text-4xl uppercase tracking-tight leading-[1.1] mb-4">{intro['title']}</h1>
<p class="text-black/70 font-svgd font-bold text-[15px] uppercase tracking-[0.12em] mb-6">Volební program koalice Zelené Brno pro komunální volby 2026</p>
<h2 class="font-svgd text-[24px] max-md:text-xl leading-[1.35] text-ink">{intro['subtitle']}.</h2>
</div>
</section>
{program_formats_html(prefix)}
<section class="bg-white pt-12 pb-20 px-14 max-md:pt-8 max-md:pb-12 max-md:px-5">
<div class="mx-auto max-w-[800px]">
<article class="wysiwyg">
{intro['paragraphs_html']}
</article>
</div>
</section>
<section class="bg-paper py-4 px-14 max-md:px-5 pb-20">
<div class="mx-auto max-w-[1040px] grid grid-cols-3 gap-6 max-nav:grid-cols-2 max-md:grid-cols-1">
{cards}
</div>
</section>
{closing_cta_html(prefix)}'''
    html = page_shell(
        title="Program",
        description=intro_desc,
        prefix=prefix,
        canonical_path="/program/",
        body_class="wp-singular page-template page-program",
        main_html=main_html,
        extra_body=program_chat_modal_html(),
        extra_scripts=f'<script src="{prefix}wp-content/themes/zeleni-new/assets/js/program-chat.js"></script>',
    )
    (ROOT / "program" / "index.html").write_text(html, encoding="utf-8")
    print("wrote program/index.html")


def jump_nav_html(ch):
    items = []
    for s in ch["sections"]:
        items.append(f'<a class="jump-nav__link" href="#sec-{s["id"]}"><span class="jump-nav__num">{s["id"]}</span>{s["title"]}</a>')
    zav_id = zavazky_id(ch)
    items.append(f'<a class="jump-nav__link" href="#sec-{zav_id}"><span class="jump-nav__num">{zav_id}</span>Naše závazky</a>')
    return "\n".join(items)


def zavazky_id(ch):
    # one past the last X.Y section, e.g. chapter 1 with sections up to 1.6 -> 1.7
    last = ch["sections"][-1]["id"] if ch["sections"] else f"{ch['num']}.0"
    major, minor = last.split(".")
    return f"{major}.{int(minor) + 1}"


def zavazky_block_html(ch, heading):
    items = "".join(f"<li>{z}</li>" for z in ch["zavazky"])
    zav_id = zavazky_id(ch)
    return f'''<div id="sec-{zav_id}" class="scroll-mt-32">
<h2 class="font-display text-ink font-black text-[28px] uppercase tracking-tight leading-[1.15] mb-4">{zav_id} {heading}</h2>
<ul class="wysiwyg-list">
{items}
</ul>
</div>'''


def top_commitments_html(ch):
    items = "".join(f"<li>{z}</li>" for z in ch["zavazky"])
    return f'''<div class="bg-green p-8 max-md:p-6 mb-12">
<h2 class="font-display text-ink font-black text-[22px] uppercase tracking-tight leading-[1.15] mb-4">Naše závazky v této kapitole</h2>
<ul class="wysiwyg-list wysiwyg-list--tight">
{items}
</ul>
</div>'''


def section_html(ch, s):
    subs = []
    for sub in s["subsections"]:
        subs.append(f'''<div id="sec-{sub['id']}" class="scroll-mt-32 mt-8">
<h3 class="font-display text-ink font-black text-[20px] uppercase tracking-tight leading-[1.2] mb-3">{sub['id']} {sub['title']}</h3>
<div class="wysiwyg">
{sub['html']}
</div>
</div>''')
    body = s["html"]
    body_block = f'<div class="wysiwyg">\n{body}\n</div>' if body else ""
    return f'''<div id="sec-{s['id']}" class="scroll-mt-32 mt-14">
<h2 class="font-display text-ink font-black text-[28px] uppercase tracking-tight leading-[1.15] mb-4">{s['id']} {s['title']}</h2>
{body_block}
{''.join(subs)}
</div>'''


BYDLENI_GUIDE_CONSENT = (
    'Souhlasím se zpracováním e-mailu za účelem zaslání příručky a informací o kampani Zelené Brno. '
    'Souhlas lze kdykoli odvolat, viz <a href="https://www.zeleni.cz/ochrana-osobnich-udaju/" '
    'target="_blank" rel="noopener" class="underline">zásady zpracování údajů</a>.'
)
BYDLENI_GUIDE_AN_URL = "https://actionnetwork.org/api/v2/forms/da64edd7-46a2-44c0-9b5e-3e9b9a8e3f9d/submissions/"


def prazdne_byty_block(prefix):
    form = newsletter_widget_html(
        "web-bydleni-clanek", "", submit_label="Poslat mi příručku", variant="light",
        consent_text=BYDLENI_GUIDE_CONSENT, an_url=BYDLENI_GUIDE_AN_URL, autoresponse=True,
    )
    return f'''<div class="bg-pink text-ink flex items-stretch gap-8 max-md:flex-col mb-10">
<img alt="Kristýna Fuchsová" class="w-64 max-md:w-full max-md:h-56 object-cover shrink-0" src="{prefix}wp-content/uploads/sites/123/2026/09/kristyna-fuchsova.jpg"/>
<div class="py-8 pr-8 max-md:p-6 max-md:pt-0 flex-1">
<p class="font-svgd text-ink font-black text-[14px] uppercase tracking-[0.12em] mb-2">Zdarma na e-mail</p>
<p class="font-svgd text-ink text-[24px] leading-[1.3] max-md:text-lg mb-2">Jak v Brně žádat o byt, neudělat chybu a zvýšit svoje šance</p>
<p class="text-[14px] text-ink/70 mb-6">Praktická příručka od <strong class="text-ink">Kristýny Fuchsové</strong></p>
{form}
</div>
</div>'''


CHAPTER_EPISODES = {
    1: "3vfIEUMYVxlpUWsmsuSSBv",
    2: "3BpUe7wyZjcF2vKwAybNDe",
    3: "16XeD60Gqqt2LBPYXuDWj3",
    4: "1R7V91CjeTLsjn2yjrJFza",
    5: "0sI9XMpOkkY0GKFfNBuZ0g",
    6: "07qW0iEZn8sGXFdxIlkJQY",
    7: "6HuPB1Nhqy9LgTt0vbQ3JZ",
    8: "5euyiRJd6KewsNrWYhfk5C",
    9: "6IZAg6htnxBm9Ezpc3LMU9",
    10: "60V5hw77kTh3SpbdcAaEw8",
    11: "6cewsfCHAZBtw36RoXrGZi",
}


def chapter_header_html(prefix, ch):
    return f'''<div class="mb-10">
<p class="font-name text-green-deep font-black text-[15px] tracking-[0.1em] mb-3">Kapitola {ch['num']:02d}</p>
<h1 class="font-display text-ink font-black text-[48px] max-md:text-4xl uppercase tracking-tight leading-[1.08] mb-5">{nbsp_single_letters(ch['title'])}</h1>
<p class="font-svgd text-[20px] max-md:text-lg leading-[1.4] text-ink">{ch['lede']}</p>
</div>'''


def chapter_listen_ask_html(ch):
    episode_id = CHAPTER_EPISODES.get(ch["num"])
    embed_src = (
        f"https://open.spotify.com/embed/episode/{episode_id}?utm_source=generator"
        if episode_id else
        "https://open.spotify.com/embed/show/5rgTV0z5hy5AhIdKGmx8VQ?utm_source=generator"
    )
    return f'''<div class="grid grid-cols-[1.3fr_1fr] gap-4 max-md:grid-cols-1 mb-10">
<div class="bg-green p-6 max-md:p-5">
<p class="font-svgd text-ink font-bold text-[15px] uppercase tracking-[0.1em] mb-2">Poslechněte si tuto kapitolu jako podcast</p>
<iframe style="border-radius:0" src="{embed_src}" width="100%" height="152" frameborder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe></div>
<div class="bg-pink p-6 max-md:p-5 flex flex-col justify-start items-start gap-3">
<p class="font-svgd text-ink font-bold text-[15px] uppercase tracking-[0.1em] mb-2">Máte otázku k této kapitole?</p>
<button type="button" class="btn btn-green btn-lg w-full" data-open-program-chat>Zeptat se chatbota na tuto kapitolu</button>
</div>
</div>'''


def prev_next_html(prefix, chapters, i):
    parts = []
    if i > 0:
        prev = chapters[i - 1]
        parts.append(f'''<a class="group flex-1 block bg-white shadow-card p-6" href="{prefix}program/{prev['slug']}/">
<span class="text-[12px] font-bold uppercase tracking-wide text-black/40">← Předchozí kapitola</span>
<h4 class="font-display text-ink font-black text-[18px] uppercase leading-tight mt-2">{prev['title']}</h4>
</a>''')
    if i < len(chapters) - 1:
        nxt = chapters[i + 1]
        parts.append(f'''<a class="group flex-1 block bg-white shadow-card p-6 text-right" href="{prefix}program/{nxt['slug']}/">
<span class="text-[12px] font-bold uppercase tracking-wide text-black/40">Další kapitola →</span>
<h4 class="font-display text-ink font-black text-[18px] uppercase leading-tight mt-2">{nxt['title']}</h4>
</a>''')
    return f'<div class="flex gap-4 mt-14 max-md:flex-col">{"".join(parts)}</div>'


def build_chapter(chapters, i):
    prefix = "../../"
    ch = chapters[i]
    sections_html = "\n".join(section_html(ch, s) for s in ch["sections"])
    zav_id = zavazky_id(ch)
    description = meta_description(ch["zavazky"][0] if ch["zavazky"] else ch["lede"])
    extra_block = prazdne_byty_block(prefix) if ch["num"] == 1 else ""

    main_html = f'''<section class="bg-white py-16 px-14 max-md:py-10 max-md:px-5">
<div class="mx-auto max-w-[800px]">
<nav class="text-[13px] font-bold text-black/45 mb-6" aria-label="Drobečková navigace">
<a class="hover:text-green transition" href="{prefix}">Domů</a> <span class="mx-1">/</span> <a class="hover:text-green transition" href="{prefix}program/">Program</a> <span class="mx-1">/</span> <span class="text-black/70">{ch['title']}</span>
</nav>
{chapter_header_html(prefix, ch)}

{chapter_listen_ask_html(ch)}

{extra_block}

{top_commitments_html(ch)}

<div class="jump-nav mb-14">
<h2 class="font-svgd text-black/70 font-bold text-[15px] uppercase tracking-[0.1em] mb-3">V této kapitole</h2>
<div class="jump-nav__list">
{jump_nav_html(ch)}
</div>
</div>

<div class="wysiwyg">
{ch['intro_html']}
</div>
<div id="sec-kde-jsme-dnes" class="scroll-mt-32 mt-10">
<h2 class="font-display text-ink font-black text-[28px] uppercase tracking-tight leading-[1.15] mb-4">Kde jsme dnes</h2>
<div class="wysiwyg">
{ch['kde_jsme_dnes_html']}
</div>
</div>

{sections_html}

<div class="mt-16 pt-2">
{zavazky_block_html(ch, "Naše závazky")}
</div>

{prev_next_html(prefix, chapters, i)}
</div>
</section>
{closing_cta_html(prefix)}'''

    og_image = f"https://www.zelenebrno.cz/wp-content/themes/zeleni-new/assets/img/og/chapter-{ch['num']:02d}.jpg"

    extra_scripts = f'<script src="{prefix}wp-content/themes/zeleni-new/assets/js/program-chat.js"></script>'
    extra_head = ""
    if ch["num"] == 1:
        extra_head = f'<link href="{prefix}wp-content/themes/zeleni-new/assets/css/newsletter-form.css" rel="stylesheet"/>'
        extra_scripts += f'\n<script src="{prefix}wp-content/themes/zeleni-new/assets/js/newsletter-form.js"></script>'

    html = page_shell(
        title=ch["title"],
        description=description,
        prefix=prefix,
        canonical_path=f"/program/{ch['slug']}/",
        body_class="wp-singular page-template page-program-chapter",
        main_html=main_html,
        extra_body=program_chat_modal_html(CHAPTER_CHAT_QUESTIONS.get(ch["num"])),
        extra_scripts=extra_scripts,
        extra_head=extra_head,
        og_image=og_image,
    )
    out_dir = ROOT / "program" / ch["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"wrote program/{ch['slug']}/index.html")


if __name__ == "__main__":
    intro, chapters = parse()
    build_index(intro, chapters)
    for i in range(len(chapters)):
        build_chapter(chapters, i)
