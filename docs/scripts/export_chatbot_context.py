#!/usr/bin/env python3
"""Export kandidátka and městské části as JSON appended to the program text
fed to the /program chatbot (program-chat-worker), so it can answer
questions about candidates and district candidacies. Run from `site/docs/`:
python3 scripts/export_chatbot_context.py

Regenerate this whenever kandidatka/, kandidatka-brno-stred/, or
mestske-casti/ change — it's a snapshot, not read live.

Procházky are handled separately: program-chat-worker/src/index.js imports
prochazky.json directly and filters "upcoming" in code at request time,
rather than embedding the full list here for the model to date-compare
itself (that was unreliable — see the worker's git history).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def extract_candidate_table(html):
    start = html.index("<table")
    end = html.index("</table>", start)
    table_html = html[start:end]
    rows = re.findall(r"<tr>(.*?)</tr>", table_html, re.S)
    candidates = []
    for row in rows:
        poradi_m = re.search(r'class="zb-poradi">([^<]*)<', row)
        if not poradi_m:
            continue
        poradi = poradi_m.group(1).strip().rstrip(".")
        jmeno_td_m = re.search(r'data-popis="Jméno">(.*?)</td>', row, re.S)
        jmeno_html = jmeno_td_m.group(1) if jmeno_td_m else ""
        jmeno_html = re.sub(r'<span class="zb-social">.*?</span>', "", jmeno_html, flags=re.S)
        titul_m = re.search(r'<span class="zb-titul">([^<]*)</span>', jmeno_html)
        titul = titul_m.group(1).strip() if titul_m else ""
        jmeno_no_titul = re.sub(r'<span class="zb-titul">.*?</span>', "", jmeno_html, flags=re.S)
        jmeno = re.sub(r"<[^>]+>", "", jmeno_no_titul).strip()
        vek_m = re.search(r'class="zb-vek"[^>]*>([^<]*)<', row)
        vek = vek_m.group(1).strip() if vek_m else ""
        povolani_m = re.search(r'data-popis="Povolání">([^<]*)<', row)
        povolani = povolani_m.group(1).strip() if povolani_m else ""
        strana_td_m = re.search(r'class="zb-strana"[^>]*>(.*?)</td>', row, re.S)
        strana_html = strana_td_m.group(1) if strana_td_m else ""
        navrhuje_m = re.search(r'<span class="zb-navrhuje">([^<]*)</span>', strana_html)
        navrhuje = navrhuje_m.group(1).strip() if navrhuje_m else ""
        strana = re.sub(r'<span class="zb-navrhuje">.*?</span>', "", strana_html, flags=re.S).strip()
        entry = {
            "poradi": int(poradi),
            "jmeno": jmeno,
            "vek": int(vek) if vek.isdigit() else vek,
            "povolani": povolani,
            "prislusnost": strana,
        }
        if titul:
            entry["titul"] = titul
        if navrhuje:
            entry["navrhuje"] = navrhuje
        candidates.append(entry)
    return candidates


def extract_kandidatka():
    html = (ROOT / "kandidatka/index.html").read_text(encoding="utf-8")
    return extract_candidate_table(html)


def extract_kandidatka_brno_stred():
    html = (ROOT / "kandidatka-brno-stred/index.html").read_text(encoding="utf-8")
    return extract_candidate_table(html)


def extract_mestske_casti():
    html = (ROOT / "mestske-casti/index.html").read_text(encoding="utf-8")

    table_start = html.index("<table>")
    table_end = html.index("</table>", table_start)
    rows = re.findall(r"<tr>(.*?)</tr>", html[table_start:table_end], re.S)
    vedeme_radnici = []
    for row in rows:
        tds = re.findall(r"<td>(.*?)</td>", row, re.S)
        if len(tds) != 3:
            continue
        mc = re.sub(r"<[^>]+>", "", tds[0]).strip()
        url_m = re.search(r'href="([^"]+)"', tds[1])
        vedeme_radnici.append({
            "mestska_cast": mc,
            "kandidatka": re.sub(r"<[^>]+>", "", tds[1]).strip(),
            "lidr": re.sub(r"<[^>]+>", "", tds[2]).strip(),
            "url": url_m.group(1) if url_m else None,
        })

    featured_m = re.search(
        r'<a class="zb-mc-featured" href="([^"]+)">\s*<span><strong>([^<]*)</strong>\s*([^<]*)</span>', html
    )
    brno_stred = None
    if featured_m:
        url = featured_m.group(1)
        if url.startswith(".."):
            url = "https://zelenebrno.cz/" + url.lstrip("./")
        brno_stred = {
            "mestska_cast": featured_m.group(2).rstrip(":"),
            "kandidatka": featured_m.group(3).strip(),
            "url": url,
        }

    cols_start = html.index('<div class="zb-mc-cols">')
    cols_end = html.index("</div>", html.index("</div>", cols_start) + 1)
    cols_html = html[cols_start:cols_end]
    p_entries = re.findall(
        r"<p><strong>([^<]+):</strong>\s*(?:<a[^>]*href=\"([^\"]+)\"[^>]*>([^<]+)</a>|([^<]+))</p>", cols_html
    )
    dalsi = []
    for mc, url, name_linked, name_plain in p_entries:
        dalsi.append({
            "mestska_cast": mc.strip(),
            "kandidatka": (name_linked or name_plain).strip(),
            "url": url or None,
        })

    return {"vedeme_radnici": vedeme_radnici, "brno_stred": brno_stred, "dalsi_kandidatky": dalsi}


def build():
    kandidatka = extract_kandidatka()
    kandidatka_brno_stred = extract_kandidatka_brno_stred()
    mestske_casti = extract_mestske_casti()

    out = f"""## Kandidátka Zelené Brno (kompletní kandidátní listina pro volby do Zastupitelstva města Brna)

```json
{json.dumps(kandidatka, ensure_ascii=False, indent=2)}
```

## Kandidátka Žít Zelené Brno pro městskou část Brno-střed (kompletní listina)

```json
{json.dumps(kandidatka_brno_stred, ensure_ascii=False, indent=2)}
```

## Městské části, kde kandidujeme

```json
{json.dumps(mestske_casti, ensure_ascii=False, indent=2)}
```
"""
    out_path = ROOT / "scripts/data/chatbot_appendix.md"
    out_path.write_text(out, encoding="utf-8")
    # Procházky are NOT embedded here — program-chat-worker/src/index.js
    # imports prochazky.json directly and filters "upcoming" in code at
    # request time (date comparison across 19 entries buried in a huge
    # prompt was unreliable for the model to do itself; see commit message).
    print(f"wrote {out_path} ({len(kandidatka)} kandidátů/kandidátek na hlavní kandidátce, "
          f"{len(kandidatka_brno_stred)} na kandidátce Brno-střed, "
          f"{len(mestske_casti['vedeme_radnici']) + len(mestske_casti['dalsi_kandidatky']) + 1} městských částí)")


if __name__ == "__main__":
    build()
