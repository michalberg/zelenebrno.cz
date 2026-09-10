#!/usr/bin/env python3
"""Shared HTML fragments (nav, footer, closing CTA, head meta) used by every
generator/patch script in this folder. `prefix` is the relative path back to
the site root: "" at depth 0, "../" at depth 1, "../../" at depth 2, etc.
"""
import re

_NBSP_SINGLE_LETTER = re.compile(r"(?<![\w&])([aiksouvzAIKSOUVZ]) ")


def nbsp_single_letters(text):
    """Czech typographic convention: one-letter words (a, i, k, o/s/u/v/z…)
    must never dangle at the end of a line, so glue them to the next word."""
    return _NBSP_SINGLE_LETTER.sub(r"\1&nbsp;", text)


ICON_READ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5c2.5-1 5.5-1 8 0v13c-2.5-1-5.5-1-8 0z"/><path d="M12 5.5c2.5-1 5.5-1 8 0v13c-2.5-1-5.5-1-8 0z"/></svg>'
ICON_LISTEN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 13v-1a8 8 0 0 1 16 0v1"/><rect x="2" y="13" width="5" height="7" rx="1.5"/><rect x="17" y="13" width="5" height="7" rx="1.5"/></svg>'
ICON_ASK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"/></svg>'

NAV_LINKS = [
    ("program/", "Program"),
    ("kandidatka/", "Kandidátka"),
    ("natalie-vencovska/", "Natálie Vencovská"),
    ("mestske-casti/", "Městské části"),
    ("jak-volit/", "Jak volit"),
    ("prochazky/", "Procházky"),
]


def nav_html(prefix):
    p = prefix
    links = "\n".join(
        f'<a class="py-1.5 hover:text-green transition-colors" href="{p}{href}">{label}</a>'
        for href, label in NAV_LINKS
    )
    overlay_links = "\n".join(
        f'<a class="nav-overlay__link" href="{p}{href}">{label}</a>'
        for href, label in NAV_LINKS
    )
    home = p if p else "."
    return f'''<!-- Nav -->
<nav class="site-nav flex items-center gap-12 px-64 bg-white">
<a class="site-nav__brand flex items-baseline gap-2.5 leading-none" href="{home}">
<span class="font-name text-green font-black text-5xl">ZELENÉ</span>
<span class="font-svgd text-ink font-bold text-5xl">Brno<span class="brand-flower" aria-hidden="true"></span></span>
</a>
<div class="site-nav__links font-svgd flex items-center gap-6 ml-12 text-[40px] font-semibold">
{links}
</div>
<div class="site-nav__cta flex items-center gap-2.5 ml-auto font-name font-normal">
<img alt="Volte číslo 3" class="site-nav__ballot" src="{p}wp-content/uploads/sites/123/2026/09/volte-3-odznak.png"/>
<a class="btn btn-green" href="{p}zapoj-se/">Zapojte se do kampaně</a>
<a class="btn btn-pink" href="{p}darujte/">Darujte</a>
</div>
<button aria-expanded="false" aria-label="Open menu" class="nav-toggle" data-nav-toggle="">
<span></span><span></span><span></span>
</button>
</nav>
<!-- Mobile menu overlay -->
<div aria-hidden="true" class="nav-overlay" data-nav-overlay="">
<div class="nav-overlay__panel">
{overlay_links}
<div class="nav-overlay__cta">
<div class="flex items-center gap-3 mb-1">
<img alt="Volte číslo 3" class="site-nav__ballot" src="{p}wp-content/uploads/sites/123/2026/09/volte-3-odznak.png"/>
<span class="font-svgd font-bold text-[15px]">Volte číslo 3</span>
</div>
<a class="btn btn-green" href="{p}zapoj-se/">Zapojte se do kampaně</a>
<a class="btn btn-pink" href="{p}darujte/">Darujte</a>
</div>
</div>
</div>'''


def footer_html(prefix):
    p = prefix
    return f'''<!-- Footer -->
<footer class="text-white pb-16 max-md:pb-12 bg-[#025B58]">
<div class="max-w-container mx-auto px-14 max-md:px-5 mb-10 pt-8 pb-8 max-md:pt-6 max-md:pb-6 border-b border-white/15 text-center">
<p class="font-svgd text-green text-[22px] max-md:text-[18px] font-bold">Volte Zelené Brno ve volbách 9. a 10. října.</p>
</div>
<div class="max-w-container mx-auto px-14 grid grid-cols-[1fr_1fr_1fr] gap-12 items-start max-md:grid-cols-1 max-md:gap-9 max-md:px-5 max-md:text-left">
<!-- Brand and contacts -->
<div>
<div class="text-white font-black text-[56px] max-md:text-[36px] tracking-wide leading-none mb-10"><span class="font-name">ZELENÉ</span> <span class="font-svgd">Brno<span class="brand-flower" aria-hidden="true"></span></span></div>
<div class="text-[14px] leading-[1.5] mb-5">
<p class="font-bold">Natálie Vencovská</p> <p class="font-bold">lídryně kandidátky</p> <a class="underline underline-offset-2 hover:text-pink transition" href="https://natalievencovska.cz/" rel="noopener" target="_blank">natalievencovska.cz</a><br/> <a class="underline underline-offset-2 hover:text-pink transition" href="mailto:natalie@zeleni.cz">natalie@zeleni.cz</a> </div>
<div class="text-[14px] leading-[1.5] mb-5">
<p class="font-bold">Matouš Vencálek</p> <p class="font-bold">spolupředseda krajské organizace</p> <a class="underline underline-offset-2 hover:text-pink transition" href="mailto:matous.vencalek@zeleni.cz">matous.vencalek@zeleni.cz</a> <p>603 931 205</p> </div>
<div class="text-[14px] leading-[1.5] mb-5">
<p class="font-bold">Adéla Mišove</p> <p class="font-bold">spolupředsedkyně krajské organizace</p> <a class="underline underline-offset-2 hover:text-pink transition" href="mailto:adela.misove@gmail.com">adela.misove@gmail.com</a> </div>
</div>
<!-- Menu -->
<div class="flex flex-col gap-2.5 text-[17px] leading-[1.55] font-bold">
<img alt="Volte číslo 3" class="w-[76px] h-[76px] mb-3 max-md:mx-auto" src="{p}wp-content/uploads/sites/123/2026/09/volte-3-odznak.png"/>
<a class="block underline underline-offset-2 hover:text-pink transition" href="{p}program/">Program</a>
<a class="block underline underline-offset-2 hover:text-pink transition" href="{p}kandidatka/">Kandidátka</a>
<a class="block underline underline-offset-2 hover:text-pink transition" href="{p}natalie-vencovska/">Natálie Vencovská</a>
<a class="block underline underline-offset-2 hover:text-pink transition" href="{p}mestske-casti/">Městské části</a>
<a class="block underline underline-offset-2 hover:text-pink transition" href="{p}jak-volit/">Jak volit</a>
<a class="block underline underline-offset-2 hover:text-pink transition" href="{p}prochazky/">Procházky</a>
<a class="block underline underline-offset-2 hover:text-pink transition" href="{p}zapoj-se/">Zapoj se</a>
<a class="block underline underline-offset-2 hover:text-pink transition" href="{p}aktuality/">Aktuality</a>
</div>
<!-- Party info (fine print) -->
<div class="text-right text-[13px] leading-[1.5] text-white/60 max-md:text-left">
<img alt="Protože Brno má na víc" class="w-full max-w-[280px] ml-auto mb-6 max-md:ml-0" src="{p}wp-content/uploads/sites/123/2026/09/protoze-brno-ma-na-vic.png"/>
<div class="flex gap-3 justify-end max-md:justify-start mb-6">
<a aria-label="Facebook" class="w-[52px] h-[52px] rounded-full bg-white/10 ring-1 ring-white/20 flex items-center justify-center hover:bg-white/20 transition" href="https://www.facebook.com/zelenebrno">
<svg aria-hidden="true" class="w-6 h-6" fill="white" viewbox="0 0 24 24"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"></path></svg>
</a>
<a aria-label="Instagram" class="w-[52px] h-[52px] rounded-full bg-white/10 ring-1 ring-white/20 flex items-center justify-center hover:bg-white/20 transition" href="https://www.instagram.com/zelenebrno/">
<svg aria-hidden="true" class="w-6 h-6" fill="white" viewbox="0 0 24 24"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"></path></svg>
</a>
</div>
<p class="font-bold text-white/80 mb-1">Strana zelených</p>
<p>Řešovská 495/18, 181 00 Praha 8<br/>IČ: 00409740</p>
<a class="inline-block underline underline-offset-2 hover:text-pink transition mt-3" href="https://www.zeleni.cz/ochrana-osobnich-udaju/" rel="noopener" target="_blank">Ochrana osobních údajů</a><br/>
<a class="inline-block underline underline-offset-2 hover:text-pink transition mt-2" href="{p}reklama/">Informace o transparentnosti kampaně</a>
</div>
</div>
</footer>'''


def closing_cta_html(prefix):
    p = prefix
    return f'''<section class="bg-ink py-16 px-14 text-center max-md:py-12 max-md:px-5">
<div class="mx-auto max-w-[680px]">
<h2 class="font-display text-white font-black text-[38px] uppercase tracking-tight leading-[1.15] mb-8 max-md:text-[28px]">Tuhle kampaň táhnou lidé jako vy.</h2>
<div class="flex gap-3 justify-center flex-wrap">
<a class="btn btn-pink btn-lg" href="{p}darujte/">Darujte</a>
<a class="btn btn-green btn-lg" href="{p}zapoj-se/">Zapojte se</a>
</div>
</div>
</section>'''


def person_modal_html(prefix):
    p = prefix
    return f'''<!-- Person modal (used by Naši lidé block) -->
<div aria-hidden="true" aria-modal="true" class="person-modal" data-assets="{p}wp-content/themes/zeleni-new/assets/img" id="personModal" role="dialog">
<div class="person-modal__backdrop"></div>
<div class="person-modal__box">
<button aria-label="Zavřít" class="person-modal__close">
<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewbox="0 0 24 24"><line x1="18" x2="6" y1="6" y2="18"></line><line x1="6" x2="18" y1="6" y2="18"></line></svg>
</button>
<div class="person-modal__img-wrap">
<img alt="" class="person-modal__img" src=""/>
</div>
<div class="person-modal__body">
<p class="person-modal__role"></p>
<h2 class="person-modal__name"></h2>
<div class="person-modal__bio wysiwyg"></div>
<ul aria-label="Sociální sítě" class="person-modal__socials"></ul>
</div>
</div>
</div>'''


def head_html(title, description, prefix, canonical_path, og_image=None, full_title=None):
    p = prefix
    full_title = full_title or f"Zelené Brno – {title}"
    og_image_tag = ""
    if og_image:
        og_image_tag = f'<meta property="og:image" content="{og_image}"/>\n'
    return f'''<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<link href="{p}wp-content/themes/zeleni-new/assets/img/favicon.png" rel="icon" type="image/png"/>
<link href="{p}wp-content/themes/zeleni-new/assets/img/apple-touch-icon.png" rel="apple-touch-icon"/>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,600;1,700;1,800&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
<link href="{p}wp-content/themes/zeleni-new/assets/css/tailwind.css" rel="stylesheet"/>
<title>{full_title}</title>
<meta content="max-image-preview:large" name="robots"/>
<meta name="description" content="{description}"/>
<link rel="canonical" href="https://zelenebrno.cz{canonical_path}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Zelené Brno"/>
<meta property="og:title" content="{full_title}"/>
<meta property="og:description" content="{description}"/>
<meta property="og:url" content="https://zelenebrno.cz{canonical_path}"/>
{og_image_tag}<meta name="twitter:card" content="summary_large_image"/>
<link href="{p}wp-content/themes/zeleni-new/assets/css/styles.css" id="zeleni-main-css" media="all" rel="stylesheet"/>
<link href="{p}wp-content/themes/zeleni-new/assets/css/floating-widget.css" rel="stylesheet"/>
<meta content="WordPress 7.1" name="generator"/>
<script defer src="https://cloud.umami.is/script.js" data-website-id="12e306b8-b908-43ac-8c54-5de37b73809c"></script>'''


def end_scripts_html(prefix, donate=False):
    p = prefix
    extra = f'\n<script src="{p}wp-content/themes/zeleni-new/assets/js/donate-form.js"></script>' if donate else ""
    return f'''<script id="zeleni-main-js" src="{p}wp-content/themes/zeleni-new/assets/js/main.js"></script>
<script src="{p}wp-content/themes/zeleni-new/assets/js/floating-widget.js"></script>{extra}'''


DONATE_LEGAL = (
    'Strana zelených (IČ 00409740) zpracovává osobní údaje dárců na základě zákonné povinnosti evidovat '
    'dárce politických stran v souladu se zákonem č. 424/1991 Sb. Prosím, berte na vědomí, že osobní údaje '
    'v rozsahu jméno, příjmení, datum narození a obec trvalého bydliště budou zveřejněny na webových '
    'stránkách Strany zelených a Úřadu pro dohled nad hospodařením politických stran a hnutí v rámci '
    'výroční zprávy nebo zprávy o volební kampani. E-mailovou adresu a číslo telefonu zpracovává Strana '
    'zelených na základě svého oprávněného zájmu za účelem přímého marketingu a rozvoje vztahu s dárci. '
    'Proti takovému zpracování je možné vznést námitku na '
    '<a href="mailto:soukromi@zeleni.cz">soukromi@zeleni.cz</a>. Více o ochraně osobních údajů ve Straně '
    'zelených najdete na <a href="http://www.zeleni.cz/soukromi" target="_blank" rel="noopener">www.zeleni.cz/soukromi</a>.'
)


NEWSLETTER_CONSENT_DEFAULT = (
    'Souhlasím se zpracováním e-mailu za účelem zasílání informací o kampani Zelené Brno. '
    'Souhlas lze kdykoli odvolat, viz <a href="https://www.zeleni.cz/ochrana-osobnich-udaju/" '
    'target="_blank" rel="noopener" class="underline">zásady zpracování údajů</a>.'
)


def newsletter_widget_html(tag, heading, submit_label="Přihlásit se", variant="light", consent_text=None,
                            an_url=None, autoresponse=False):
    consent_text = consent_text or NEWSLETTER_CONSENT_DEFAULT
    heading_html = f'<p class="zb-newsletter-heading">{heading}</p>' if heading else ""
    an_url_attr = f' data-an-url="{an_url}"' if an_url else ""
    autoresponse_attr = ' data-autoresponse="true"' if autoresponse else ""
    return f'''<div class="zb-newsletter zb-newsletter--{variant}" data-newsletter-form data-tag="{tag}"{an_url_attr}{autoresponse_attr}>
{heading_html}
<form>
<div class="zb-newsletter-hp" aria-hidden="true"><label>Nevyplňujte, pokud jste člověk<input type="text" tabindex="-1" autocomplete="off" data-newsletter-hp></label></div>
<div class="zb-newsletter-row">
<input type="email" placeholder="Váš e-mail" required autocomplete="email" data-newsletter-email>
<button type="submit" class="btn btn-green" data-newsletter-submit>{submit_label}</button>
</div>
<label class="zb-newsletter-consent">
<input type="checkbox" required>
<span>{consent_text}</span>
</label>
<p class="zb-newsletter-error" data-newsletter-error>Zadejte prosím platný e-mail.</p>
</form>
<p class="zb-newsletter-success" data-newsletter-success hidden>Hotovo, budeme vás informovat.</p>
</div>'''


COALITION_LOGOS = [
    ("zeleni.svg", "Strana zelených"),
    ("zit-brno.png", "Žít Brno"),
    ("sen21.svg", "SEN 21"),
    ("les.png", "Liberálně ekologická strana"),
    ("hnuti-kruh.png", "Hnutí Kruh"),
    ("volt.svg", "Volt Česko"),
    ("budoucnost.png", "hnutí Budoucnost"),
]


def coalition_logos_html(prefix):
    items = "\n".join(
        f'<img alt="{name}" title="{name}" class="h-8 md:h-9 w-auto object-contain" '
        f'src="{prefix}wp-content/uploads/sites/123/2026/09/loga-koalice/{file}"/>'
        for file, name in COALITION_LOGOS
    )
    return f'''<div class="flex flex-wrap items-center gap-x-8 gap-y-4">
{items}
</div>'''


def coalition_panel_html(prefix):
    """Compact 'coalition' card: logo row on its own card, sized to sit
    beside the team block without stretching into empty leftover space."""
    items = "\n".join(
        f'<img alt="{name}" title="{name}" class="h-10 w-auto object-contain" '
        f'src="{prefix}wp-content/uploads/sites/123/2026/09/loga-koalice/{file}"/>'
        for file, name in COALITION_LOGOS
    )
    return f'''<div class="bg-white shadow-card p-7">
<p class="font-svgd text-ink text-[16px] mb-5">Koalici Zelené Brno tvoří</p>
<div class="flex flex-wrap items-center gap-x-7 gap-y-6">
{items}
</div>
</div>'''


def donate_teaser_html(prefix, default_amount=1000, button_class="btn btn-pink btn-lg"):
    target = f"{prefix}darujte/"
    return f'''<div class="zb-donate-teaser" data-donate-teaser data-target="{target}">
<div class="zb-donate-amounts">
<button type="button" class="zb-amount-btn" data-amount="300">300 Kč</button>
<button type="button" class="zb-amount-btn" data-amount="500">500 Kč</button>
<button type="button" class="zb-amount-btn is-selected" data-amount="1000">1000 Kč</button>
<button type="button" class="zb-amount-btn" data-amount="2000">2000 Kč</button>
<input type="number" min="1" placeholder="Jiná částka" class="zb-amount-custom" data-amount-custom>
</div>
<a class="{button_class}" data-donate-teaser-link href="{target}?amount={default_amount}">Pokračovat k daru →</a>
</div>'''


def donate_widget_html():
    """Donate form + success state. Same fund/account as natalievencovska.cz."""
    return f'''<div class="zb-donate" data-donate-form>
<form>
<div class="zb-donate-amounts" data-donate-amounts>
<button type="button" class="zb-amount-btn" data-amount="300">300 Kč</button>
<button type="button" class="zb-amount-btn" data-amount="500">500 Kč</button>
<button type="button" class="zb-amount-btn is-selected" data-amount="1000">1000 Kč</button>
<button type="button" class="zb-amount-btn" data-amount="2000">2000 Kč</button>
<input type="number" min="1" placeholder="Jiná částka" class="zb-amount-custom" data-amount-custom>
</div>
<div class="zb-form-row">
<div class="zb-form-field"><label>Jméno</label><input required data-field="firstName" placeholder="Jméno"></div>
<div class="zb-form-field"><label>Příjmení</label><input required data-field="lastName" placeholder="Příjmení"></div>
</div>
<div class="zb-form-row">
<div class="zb-form-field"><label>Datum narození</label><input required data-field="birth" placeholder="DD.MM.RRRR (starší 15 let)" pattern="\\d{{1,2}}\\.\\d{{1,2}}\\.\\d{{4}}"></div>
<div class="zb-form-field"><label>Telefon</label><input type="tel" data-field="phone" placeholder="Nepovinné"></div>
</div>
<div class="zb-form-field zb-mb"><label>E-mail</label><input type="email" required data-field="email" placeholder="E-mail"></div>
<div class="zb-form-field zb-mb"><label>Ulice</label><input required data-field="street" placeholder="Ulice"></div>
<div class="zb-form-row zb-city-row">
<div class="zb-form-field"><label>Město</label><input required data-field="city" placeholder="Město"></div>
<div class="zb-form-field"><label>PSČ</label><input required data-field="zip" placeholder="PSČ" pattern="\\d{{3}} ?\\d{{2}}"></div>
</div>
<div class="zb-submit-row">
<button type="submit" class="btn btn-green btn-lg" data-donate-submit>Darovat <span data-donate-amount-label>1000 Kč</span> →</button>
<p class="zb-submit-note">Po odeslání obdržíte platební údaje a QR kód pro převod.</p>
<p class="zb-submit-note">Jednorázový nebo pravidelný dar na lepší Brno poslalo už 183 lidí.</p>
</div>
<p class="zb-legal">{DONATE_LEGAL}</p>
</form>
<div class="zb-donate-success" data-donate-success hidden>
<h3>Děkujeme za váš dar!</h3>
<p>Pro dokončení převeďte <strong data-success-amount>—</strong> Kč na účet níže. Potvrzení a darovací smlouvu vám posíláme na e-mail <strong data-success-email>—</strong>.</p>
<div class="zb-payment-grid">
<dl class="zb-payment-info">
<div><dt>Číslo účtu</dt><dd data-success-account>2400146729/2010</dd></div>
<div><dt>IBAN</dt><dd data-success-iban>CZ5520100000002400146729</dd></div>
<div><dt>Variabilní symbol</dt><dd data-success-vs>—</dd></div>
<div><dt>Částka</dt><dd><span data-success-amount-2>—</span> Kč</dd></div>
</dl>
<div class="zb-payment-qr">
<img data-success-qr alt="QR kód pro převod" width="220" height="220">
<p>Naskenujte v mobilní bankovní aplikaci</p>
</div>
</div>
<p class="zb-payment-note">Napište prosím do zprávy pro příjemce, že se jedná o <strong>„dar"</strong> — je to požadavek zákona. (QR kód toto vyplňuje automaticky.)</p>
</div>
</div>'''
