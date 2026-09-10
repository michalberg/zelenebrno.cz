#!/usr/bin/env python3
"""Generate sitemap.xml and llms.txt from the site's actual pages, so both
stay in sync with real URLs and meta descriptions. Run from `site/docs/`:
python3 scripts/generate_sitemap_and_llms.py
"""
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.zelenebrno.cz"


def read_meta(path):
    html = (ROOT / path / "index.html").read_text(encoding="utf-8")
    title_m = re.search(r"<title>(.*?)</title>", html)
    desc_m = re.search(r'name="description" content="([^"]*)"', html)
    title = title_m.group(1) if title_m else ""
    desc = desc_m.group(1) if desc_m else ""
    return title, desc


ALL_PAGES = [
    "",
    "program",
    "program/dostupne-bydleni-a-vystavba",
    "program/bezpecna-doprava",
    "program/verejny-prostor-pro-lidi",
    "program/zelen-voda-a-stin-ve-meste",
    "program/energie-odpady-a-ciste-mesto",
    "program/skoly-deti-rodiny-a-sport",
    "program/pece-o-seniory-a-lidi-v-nouzi",
    "program/zdravi-bezpeci-a-krizova-pripravenost",
    "program/otevrena-radnice-a-dobre-hospodareni",
    "program/mistni-ekonomika-a-zive-centrum",
    "program/kultura-a-komunitni-zivot",
    "kandidatka",
    "kandidatka-brno-stred",
    "natalie-vencovska",
    "mestske-casti",
    "jak-volit",
    "prochazky",
    "zapoj-se",
    "darujte",
    "komise",
    "reklama",
    "prazdniny",
    "aktuality",
    "na-verejna-gymnazia-a-lycea-v-brne-se-dostala-mene-nez-polovina-uchazecu-zeleni-chteji-mestske-lyceum",
    "brno-ma-na-vic-rikaji-zeleni-v-siroke-koalici-spojili-zkusene-osobnosti-z-radnic-i-nove-tvare",
]

CHAPTER_SLUGS = {
    "program/dostupne-bydleni-a-vystavba",
    "program/bezpecna-doprava",
    "program/verejny-prostor-pro-lidi",
    "program/zelen-voda-a-stin-ve-meste",
    "program/energie-odpady-a-ciste-mesto",
    "program/skoly-deti-rodiny-a-sport",
    "program/pece-o-seniory-a-lidi-v-nouzi",
    "program/zdravi-bezpeci-a-krizova-pripravenost",
    "program/otevrena-radnice-a-dobre-hospodareni",
    "program/mistni-ekonomika-a-zive-centrum",
    "program/kultura-a-komunitni-zivot",
}


def build_sitemap():
    today = date.today().isoformat()
    entries = []
    for slug in ALL_PAGES:
        url = f"{BASE}/{slug + '/' if slug else ''}"
        entries.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n  </url>")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"wrote sitemap.xml ({len(ALL_PAGES)} urls)")


def build_llms_txt():
    def line(slug):
        title, desc = read_meta(slug)
        title = title.replace("Zelené Brno – ", "")
        url = f"{BASE}/{slug}/"
        return f"- [{title}]({url}): {desc}"

    chapters = "\n".join(line(s) for s in ALL_PAGES if s in CHAPTER_SLUGS)

    txt = f"""# Zelené Brno

> Koalice Zelené Brno (Strana zelených, Žít Brno, SEN 21, Liberálně ekologická strana, Hnutí Kruh, Volt Česko, hnutí Budoucnost) kandiduje pod číslem 3 do Zastupitelstva města Brna v komunálních volbách 9.–10. října 2026. Lídryní kandidátky je Natálie Vencovská. Tento web nese kompletní volební program „Brno do detailu" (256 konkrétních opatření v 11 kapitolách), kandidátní listinu a informace o zapojení do kampaně.

## Program

Volební program „Brno do detailu" po kapitolách:

{line("program")}
{chapters}

## Kandidátky

{line("kandidatka")}
{line("kandidatka-brno-stred")}
{line("natalie-vencovska")}
{line("mestske-casti")}

## Volby

{line("jak-volit")}
{line("komise")}
{line("reklama")}

## Zapojení a podpora

{line("zapoj-se")}
{line("darujte")}
{line("prochazky")}

## Aktuality

{line("aktuality")}
{line("na-verejna-gymnazia-a-lycea-v-brne-se-dostala-mene-nez-polovina-uchazecu-zeleni-chteji-mestske-lyceum")}
{line("brno-ma-na-vic-rikaji-zeleni-v-siroke-koalici-spojili-zkusene-osobnosti-z-radnic-i-nove-tvare")}
{line("prazdniny")}
"""
    (ROOT / "llms.txt").write_text(txt, encoding="utf-8")
    print("wrote llms.txt")


if __name__ == "__main__":
    build_sitemap()
    build_llms_txt()
