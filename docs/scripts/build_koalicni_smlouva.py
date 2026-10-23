#!/usr/bin/env python3
"""Generate the full text of the Brno coalition agreement (2026–2030).
Run from `docs/`:
    python3 scripts/build_koalicni_smlouva.py
"""
import re
from pathlib import Path

from partials import nav_html, footer_html, person_modal_html, head_html, end_scripts_html, nbsp_single_letters

ROOT = Path(__file__).resolve().parent.parent

SLUG = "koalicni-smlouva"
DATE = "23. 10. 2026"
DATETIME = "2026-10-23T12:00:00+02:00"
TITLE = "Koaliční smlouva"
SUBTITLE = "pro Zastupitelstvo města Brna ve volebním období 2026–2030"
DESCRIPTION = ("Plné znění koaliční smlouvy pro Zastupitelstvo města Brna na období 2026–2030 a její přílohy, "
               "Programového prohlášení Rady města Brna pro roky 2026–2030.")
ANNEX_MD = Path(__file__).resolve().parent / "programove_prohlaseni_2026_2030.md"
ANNEX_ID = "programove-prohlaseni"


def slugify(text):
    import unicodedata
    s = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def annex_html():
    """Render the programme statement (simple Markdown: #, ##, ###, '- ' lists, paragraphs, ---)."""
    out, toc, items = [], [], []

    def flush():
        if items:
            out.append(ul(items))
            items.clear()

    for line in ANNEX_MD.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:])
            continue
        flush()
        if not line or line == "---" or line.startswith("# "):
            continue
        if line.startswith("### "):
            out.append(f"<h4>{line[4:]}</h4>")
        elif line.startswith("## "):
            title = line[3:]
            anchor = f"pp-{slugify(title)}"
            toc.append((anchor, title))
            out.append(f'<h3 id="{anchor}" class="scroll-mt-24">{title}</h3>')
        elif toc:  # the lead sentence before the first chapter is rendered separately
            out.append(p(line))
    flush()
    sep = '<span class="text-black/30 mx-2" aria-hidden="true">·</span>'
    toc_html = sep.join(
        f'<a class="underline underline-offset-2 decoration-black/30 hover:text-green-deep" href="#{a}">{t}</a>'
        for a, t in toc)
    return toc_html, "\n".join(out)


def p(text):
    return f"<p>{nbsp_single_letters(text)}</p>"


def h(text):
    return f"<h3>{text}</h3>"


def ul(items):
    lis = "\n".join(f"<li>{nbsp_single_letters(i)}</li>" for i in items)
    return f"<ul>\n{lis}\n</ul>"


def ol(items):
    lis = "\n".join(f"<li>{nbsp_single_letters(i)}</li>" for i in items)
    return f"<ol>\n{lis}\n</ol>"


def party(name, items):
    return f"<h4>{name}</h4>\n{ul(items)}"


def principle(lead, text):
    return p(f"<b>{lead}</b> {text}")


BODY = [
    h("I. Smluvní strany a účel smlouvy"),
    p("Tuto koaliční smlouvu uzavírají zástupci volebních subjektů Lidovci a Starostové – Brno blíž lidem, ODS, "
      "TOP 09 a nezávislí, Zelené Brno, Piráti a Fakt Brno TU! a Za Lužánky (dále jen „koaliční partneři“), "
      "s cílem vytvořit stabilní většinu v Zastupitelstvu města Brna a společně nést odpovědnost za správu města "
      "ve volebním období 2026–2030."),
    p("Koaliční partneři respektují svobodný mandát členů zastupitelstva, zákonné pravomoci orgánů města a zásadu, "
      "že tato smlouva je politickou dohodou, nikoliv náhradou zákonných rozhodovacích postupů."),

    h("II. Hodnotová východiska a společné principy"),
    principle("Koalice změny.",
              "Naším společným cílem je posunout Brno dopředu. Zavazujeme se přistupovat k řízení města aktivně, "
              "otevřeně komunikovat s obyvateli, novináři i všemi, kteří naše krásné město tvoří. Budeme vyhodnocovat "
              "dosavadní postupy a tam, kde nefungují, prosazovat konkrétní změny ve prospěch obyvatel."),
    principle("Koalice odvážných řešení.",
              "Koalice se hlásí k odvaze přijímat i náročná a dlouhodobá rozhodnutí, která Brno potřebuje. Chceme "
              "upřednostnit promyšlená řešení před odkládáním problémů, dílčím řešením nebo populistickým přístupem. "
              "Každé významné rozhodnutí podložíme věcnými argumenty, odpovědným financováním a otevřenou debatou."),
    principle("Otevřenost jako základ spolupráce.",
              "Koalice je založena na otevřenosti vůči občanům, městským částem, odborné veřejnosti i mezi samotnými "
              "koaličními partnery."),
    principle("Důvěra a partnerské jednání.",
              "Koaliční partneři respektují svou odlišnou politickou identitu. Budeme jednat v dobré víře a hledat "
              "společná řešení."),
    principle("Město blíže lidem.",
              "Rozhodování bude vycházet z každodenních potřeb obyvatel a probíhat co nejblíže těm, kterých se týká. "
              "Koalice posílí spolupráci s městskými částmi a zapojení občanů do přípravy důležitých projektů."),
    principle("Odvaha investovat do budoucnosti.",
              "Skončí výprodej městského majetku. Prioritou bude dostupné bydlení, kvalitní školy a služby, fungující "
              "doprava, bezpečný veřejný prostor a strategická infrastruktura. Koalice bude odpovědně spravovat "
              "městský majetek."),
    principle("Moderní a srozumitelná radnice.",
              "Koalice podpoří digitalizaci, využívání dat, průhledné zadávání veřejných zakázek a účinnou kontrolu "
              "hospodaření. Brno bude předvídatelným partnerem občanů, podnikatelů a městských částí."),
    principle("Soudržné a otevřené Brno.",
              "Rozvoj města má přinášet příležitosti dětem, rodinám, seniorům i lidem se zdravotním postižením. "
              "Koalice bude podporovat vzdělávání, kulturu, sport, sociální služby a respekt k rozmanitosti obyvatel."),
    principle("Zdravé a odolné město.",
              "Koalice připraví Brno na projevy změny klimatu důslednou ochranou životního prostředí, hospodařením "
              "s vodou a energií a adaptačními opatřeními."),

    h("III. Vedení města Brna a rozdělení kompetencí"),
    p("Koaliční partneři se zavazují prosazovat následující obsazení funkcí a rozdělení věcných gescí. Jednotlivé "
      "funkce budou obsazeny nominanty příslušných koaličních subjektů; konkrétní personální nominace jsou v jejich "
      "působnosti. 11 členů Rady města Brna bude rozděleno takto:"),
    party("Lidovci a Starostové", [
        "<b>Primátor</b> – Organizační odbor, vnitřní věci, obrana, rozpočet a financování, interní audit a kontrola, "
        "tiskové středisko, kybernetická bezpečnost, kancelář primátora, strategické projekty města",
        "<b>3. Náměstek/kyně primátora</b> – Školství a mládež, participace",
        "<b>4. Náměstek/kyně primátora</b> – Zdravotnictví, sociální péče, strategie a pronájmy městských bytů",
        "<b>Člen/ka rady</b> – Investice, evropské fondy",
        "<b>Člen/ka rady</b> – Územní plánování a rozvoj, veřejný prostor, městská energetika",
    ]),
    party("ODS a TOP 09", [
        "<b>Náměstek/kyně primátora</b> – Zahraniční vztahy, sport",
        "<b>Člen/ka rady</b> – IT, strategický rozvoj a inovace",
        "<b>Člen/ka rady</b> – Majetek města, správa majetku, bytová výstavba",
    ]),
    party("Zelené Brno", [
        "<b>2. Náměstek/kyně primátora</b> – Životní prostředí a udržitelný rozvoj města",
    ]),
    party("Piráti a Fakt Brno TU!", [
        "<b>Člen/ka rady</b> – Doprava a mobilita",
    ]),
    party("Za Lužánky", [
        "<b>Člen/ka rady</b> – Kultura, památková péče, marketing a cestovní ruch",
    ]),
    party("Další pozice", [
        "Lidovci a Starostové nominují předsedu/kyni koncernového výboru;",
        "ODS a TOP 09 náleží nominace na uvolněného předsedu/kyni bytové komise Rady města Brna;",
        "Zelenému Brnu nominace na uvolněného předsedu/kyni Výboru pro národnostní menšiny;",
        "subjektu Piráti a Fakt Brno TU! nominace na uvolněného předsedu/kyni finančního výboru.",
        "Za Lužánky nominují neuvolněného zastupitele pověřeného řízením strategického projektu výstavby stadionu "
        "Za Lužánkami.",
        "Koaliční partneři se současně zavazují podpořit nominanta hnutí ANO do funkce uvolněného předsedy/kyně "
        "Kontrolního výboru Zastupitelstva města Brna.",
    ]),

    h("IV. Výkon gescí a programové prohlášení"),
    p("Každý člen rady v rámci svěřené gesce koordinuje přípravu návrhů, spolupracuje s příslušnými odbory magistrátu "
      "a odpovídá za politické prosazování programových priorit. Rozdělení gescí mezi koaliční subjekty se nemění "
      "samotnou změnou osoby nominanta."),
    p("Programové prohlášení Rady města Brna pro roky 2026–2030 tvoří nedílnou přílohu č. 1 této smlouvy. Jeho text "
      "není do tohoto vyhotovení smlouvy vložen; koaliční partneři se zavazují společně prosazovat jeho plnění."),

    h("V. Společné rozhodování a koordinace"),
    ol([
        "Koaliční spolupráce je na týdenní bázi organizována na Poradě vedení; Poradu vedení vede primátor. Porada "
        "vedení sestává z členů Rady města Brna. Přístup na ni mají také předsedové klubů.",
        "Koaliční rada je politickým koordinačním orgánem koalice. Členem je primátor a dva zástupci z každého "
        "subjektu; primátor svolává její jednání zpravidla jednou za měsíc a mimo to vždy na žádost kteréhokoliv "
        "partnera.",
        "Koaliční rada předem projedná zejména návrh rozpočtu a jeho zásadní změny, velké investice, strategické "
        "dokumenty, změny organizační struktury, významné majetkové dispozice a nominace do orgánů městských "
        "společností.",
        "Jednotlivé strany koaliční smlouvy se dohodly v hlasování na zastupitelstvu primárně podpořit návrh, který "
        "byl odhlasován v Radě města Brna, a postupovat ve vztahu k ostatním stranám koaliční smlouvy v souladu "
        "se zásadou legitimního očekávání a transparentnosti s cílem naplňovat Programové prohlášení Rady města Brna "
        "pro roky 2026–2030. Pakliže některá ze stran nebo některý ze zastupitelů nemá v úmyslu na zastupitelstvu "
        "podpořit návrh, který byl odhlasován v Radě města Brna, je předseda klubu povinen toto stanovisko předem "
        "projednat na Poradě vedení, případně koaliční radě.",
        "Před zasedáním zastupitelstva či v případě jiných důležitých otázek svolává primátor Poradu předsedů "
        "zastupitelských klubů.",
    ]),

    h("VI. Dohodovací řízení"),
    ol([
        "Má-li některý koaliční partner zásadní výhradu k zamýšlenému rozhodnutí, písemně ji oznámí ostatním "
        "partnerům a požádá o dohodovací řízení. Uvede spornou otázku, důvody a případný návrh řešení.",
        "Prvotně bude sporná otázka řešena na úrovni Porady vedení, případně mezi příslušnými členy rady.",
        "Nedojde-li k dohodě, svolá primátor koaliční radu nejpozději do pěti pracovních dnů. Každý partner má právo "
        "předložit vlastní variantu řešení a vyžádat si podklady.",
        "Po dobu dohodovacího řízení se sporný návrh zpravidla nepředkládá k rozhodnutí, ledaže odklad znemožňuje "
        "splnění zákonné povinnosti, způsobuje bezprostřední škodu nebo s odlišným postupem souhlasí všichni "
        "partneři.",
    ]),

    h("VII. Personální nominace a městské organizace"),
    p("Návrhy do výborů, komisí, představenstev, dozorčích rad a dalších orgánů městských organizací se projednají "
      "koaličně. Koalice se dohodla, že opoziční hnutí ANO bude zastoupeno ve všech výborech a komisích a také "
      "v dozorčích radách všech městem zřizovaných organizací."),

    h("VIII. Vystupování a odpovědnost"),
    p("Partneři budou včas sdílet informace o zásadních rozhodnutích a veřejných sděleních týkajících se společné "
      "politiky. Zachovávají právo na vlastní programové postoje, avšak na veřejnosti vystupují jednotně. Případné "
      "spory se pokusí vyřešit koaličním jednáním. Každý partner odpovídá za své nominanty. Základním pravidlem "
      "nominace do jakékoliv pozice je odbornost."),

    h("IX. Změny smlouvy, trvání a závěrečná ustanovení"),
    p("Smlouva nabývá účinnosti podpisem všech partnerů a uzavírá se pro volební období 2026–2030. Změny a doplňky "
      "se přijímají pouze písemným dodatkem se souhlasem všech partnerů. Podstatné porušení smlouvy je nejprve "
      "předmětem dohodovacího řízení. Partner oznámí ukončení své účasti písemně ostatním partnerům."),
    p("Smlouva bude po podpisu zveřejněna. Programové prohlášení Rady města Brna pro roky 2026–2030 je její "
      "nedílnou přílohou č. 1, která je vedena jako samostatný dokument."),

    h("X. Podpisy"),
    ul([
        "Za KDU-ČSL: Mgr. Petr Hladík, předseda Městského výboru",
        "Za ODS: Mgr. Matyáš Svoboda, pověřený člen OS Brno-město",
        "Za STAN: JUDr. Michal Marek, předseda OS Brno-město",
        "Za TOP 09: Bc. Tomáš Aberl, předseda RO Brno-město",
        "Zelené Brno: Mgr. Matouš Vencálek, spolupředseda KO SZ JMK",
        "Piráti a Fakt Brno TU!: Mgr. Adam Zemek, předseda MS Brno",
        "Za Lužánky: Mgr. et Mgr. Jana Janulíková, pověřená podpisem za hnutí Za Lužánky",
    ]),
    p(f"V Brně dne {DATE}"),
]


def build():
    prefix = "../"
    body_html = "\n".join(BODY)
    toc_html, annex_body = annex_html()
    main_html = f'''<section class="bg-white py-20 px-14 max-md:py-12 max-md:px-5">
<div class="mx-auto max-w-[800px]">
<p class="font-name text-green-deep font-bold text-[15px] uppercase tracking-[0.18em] mb-6">Dokument · {DATE}</p>
<h1 class="font-display text-ink font-black text-[56px] max-md:text-4xl uppercase tracking-tight leading-[1.1] mb-4">{TITLE}</h1>
<p class="text-[20px] max-md:text-[18px] leading-[1.4] text-black/70 mb-6">{nbsp_single_letters(SUBTITLE)}</p>
<p class="mb-10"><a class="btn btn-pink" href="#{ANNEX_ID}">Příloha č. 1: Programové prohlášení ↓</a></p>
<article class="wysiwyg">
{body_html}
</article>
<div class="wysiwyg-meta">
<span class="wysiwyg-meta__item">
<span class="wysiwyg-meta__label">Podepsáno:</span>
<time datetime="{DATETIME}">{DATE}</time>
</span>
</div>
<div id="{ANNEX_ID}" class="scroll-mt-24 mt-16 pt-12 border-t-4 border-green">
<p class="font-name text-green-deep font-bold text-[15px] uppercase tracking-[0.18em] mb-4">Příloha č. 1 koaliční smlouvy</p>
<h2 class="font-display text-ink font-black text-[44px] max-md:text-[30px] uppercase tracking-tight leading-[1.1] mb-6">Programové prohlášení Rady města Brna pro roky 2026–2030</h2>
<p class="font-svgd text-[22px] max-md:text-[19px] leading-[1.45] text-ink mb-8">{nbsp_single_letters("Budeme řídit Brno jako moderní evropské město stojící na důvěře, partnerství a rozhodování co nejblíže lidem.")}</p>
<nav aria-label="Kapitoly programového prohlášení" class="text-[15px] leading-[1.9] text-ink mb-10">
<p class="font-name text-black/50 font-bold text-[12px] uppercase tracking-[0.14em] mb-1">Kapitoly:</p>
<p>{toc_html}</p>
</nav>
<article class="wysiwyg">
{annex_body}
</article>
</div>
<div class="bg-[#f4faf6] p-8 max-md:p-6 mt-10">
<p class="font-name font-black text-[22px] leading-tight text-ink mb-3">Co přesně jsme vyjednali?</p>
<p class="text-[16px] leading-[1.6] text-black/75 mb-5">{nbsp_single_letters("Přehled toho, co se z našeho programu dostalo do programového prohlášení, co bude mít na starosti náš resort a odpovědi na časté otázky najdete na hlavní stránce.")}</p>
<div class="flex gap-3 flex-wrap">
<a class="btn btn-green" href="{prefix}#vyjednali">Co jsme prosadili →</a>
<a class="btn btn-ink" href="{prefix}zeleni-budou-soucasti-vedeni-brna/">Tisková zpráva →</a>
</div>
</div>
</div>
</section>
<section class="bg-ink py-16 px-14 text-center max-md:py-12 max-md:px-5">
<div class="mx-auto max-w-[680px]">
<h2 class="font-display text-white font-black text-[38px] uppercase tracking-tight leading-[1.15] mb-8 max-md:text-[28px]">Teď začíná práce</h2>
<p class="text-white/75 text-[16px] leading-[1.6] mb-8">{nbsp_single_letters("Přidejte se k nám a pomozte prosazovat to, s čím jsme do voleb šli.")}</p>
<div class="flex gap-3 justify-center flex-wrap">
<a class="btn btn-green btn-lg" href="{prefix}zapoj-se/">Zapojte se</a>
<a class="btn btn-pink btn-lg" href="{prefix}darujte/">Darujte</a>
</div>
</div>
</section>'''
    html = f'''<!DOCTYPE html>
<html lang="cs">
<head>
{head_html(f"{TITLE} 2026–2030", DESCRIPTION, prefix, f"/{SLUG}/")}
</head>
<body class="page-template-default page wp-embed-responsive wp-theme-zeleni-new font-sans bg-paper text-ink antialiased min-h-screen flex flex-col tribe-no-js">
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
