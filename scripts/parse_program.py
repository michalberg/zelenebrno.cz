#!/usr/bin/env python3
"""Parse foto/program_final.md into structured chapter data for the /program pages.

Run standalone to dump JSON for inspection:
    python3 scripts/parse_program.py
"""
import json
import re
import unicodedata
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "data" / "program_final.md"


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def inline_md(text):
    text = text.strip()
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def md_to_html(text):
    """Convert a chunk of plain paragraphs + '- ' bullet lists into wysiwyg HTML."""
    text = text.strip("\n")
    if not text.strip():
        return ""
    blocks = re.split(r"\n\s*\n", text)
    html_parts = []
    for block in blocks:
        block = block.strip("\n")
        if not block.strip():
            continue
        lines = [l for l in block.split("\n") if l.strip()]
        if all(l.strip().startswith("- ") for l in lines):
            items = "".join(f"<li>{inline_md(l.strip()[2:])}</li>" for l in lines)
            html_parts.append(f"<ul>{items}</ul>")
        else:
            joined = " ".join(l.strip() for l in lines)
            html_parts.append(f"<p>{inline_md(joined)}</p>")
    return "\n".join(html_parts)


def first_sentences(text, n=2):
    text = text.strip()
    # naive sentence split on ". " / "? " / "! " not inside common abbreviations
    parts = re.split(r"(?<=[.!?]) +", text)
    return " ".join(parts[:n]).strip()


def split_by_heading(text, marker):
    """Split text into (preamble, [(heading, body), ...]) on lines starting with marker (e.g. '## ')."""
    lines = text.split("\n")
    preamble_lines = []
    sections = []
    current_heading = None
    current_body = []
    for line in lines:
        if line.startswith(marker) and not line.startswith(marker + "#"):
            if current_heading is None:
                preamble_lines_done = True
            else:
                sections.append((current_heading, "\n".join(current_body)))
            current_heading = line[len(marker):].strip()
            current_body = []
        else:
            if current_heading is None:
                preamble_lines.append(line)
            else:
                current_body.append(line)
    if current_heading is not None:
        sections.append((current_heading, "\n".join(current_body)))
    return "\n".join(preamble_lines), sections


def parse():
    raw = SOURCE.read_text(encoding="utf-8")

    # --- preamble (before first "# 1") ---
    m = re.search(r"\n(?=# 1 )", raw)
    preamble_raw = raw[: m.start()]
    rest = raw[m.start():]

    # preamble: H1 title, H2 subtitle, paragraphs, then "## Obsah" list
    pre_before_obsah, pre_sections = split_by_heading(preamble_raw, "## ")
    # pre_before_obsah contains "# BRNO DO DETAILU" line only (H2 subtitle got
    # captured as first section since "## " marker also matches H2? No -- H2 in
    # markdown is also "## " prefix, same as our section marker, that's fine:
    # first pre_section heading = subtitle, its body = the paragraphs, second
    # pre_section heading = "Obsah", its body = the numbered list.
    subtitle = pre_sections[0][0] if pre_sections else ""
    intro_body = pre_sections[0][1] if pre_sections else ""
    obsah_body = pre_sections[1][1] if len(pre_sections) > 1 else ""
    chapter_titles = re.findall(r"^\d+\.\s+(.+)$", obsah_body, re.M)

    intro_paragraphs = [b.strip() for b in re.split(r"\n\s*\n", intro_body.strip()) if b.strip()]

    program_intro = {
        "title": pre_before_obsah.strip().lstrip("# ").strip(),
        "subtitle": subtitle,
        "paragraphs_html": md_to_html(intro_body),
        "paragraphs_raw": intro_paragraphs,
    }

    # --- chapters ---
    chapter_blocks = re.split(r"\n(?=# \d+ )", rest)
    chapters = []
    for block in chapter_blocks:
        m2 = re.match(r"# (\d+) (.+?)\n", block)
        if not m2:
            continue
        num = int(m2.group(1))
        title = chapter_titles[num - 1] if num - 1 < len(chapter_titles) else m2.group(2).title()
        body = block[m2.end():]

        chapter_intro, sections = split_by_heading(body, "## ")
        chapter_intro_html = md_to_html(chapter_intro)
        chapter_lede = first_sentences(chapter_intro.strip().split("\n\n")[0]) if chapter_intro.strip() else ""

        kde_jsme_dnes_html = ""
        subsections = []
        zavazky = []
        for heading, sbody in sections:
            if heading.strip().lower() == "kde jsme dnes":
                kde_jsme_dnes_html = md_to_html(sbody)
                continue
            hm = re.match(r"^([\d.]+)\s+(.+)$", heading.strip())
            if not hm:
                continue
            sec_id, sec_title = hm.group(1), hm.group(2)
            if "naše závazky" in sec_title.lower() or "naše závazky" in heading.lower():
                zavazky = re.findall(r"^- (.+)$", sbody, re.M)
                continue
            sec_intro, subsecs = split_by_heading(sbody, "### ")
            sub_list = []
            for sh, sbody2 in subsecs:
                shm = re.match(r"^([\d.]+)\s+(.+)$", sh.strip())
                if not shm:
                    continue
                sub_list.append({
                    "id": shm.group(1),
                    "title": shm.group(2),
                    "html": md_to_html(sbody2),
                })
            subsections.append({
                "id": sec_id,
                "title": sec_title,
                "html": md_to_html(sec_intro),
                "subsections": sub_list,
            })

        chapters.append({
            "num": num,
            "title": title,
            "slug": slugify(title),
            "lede": chapter_lede,
            "intro_html": chapter_intro_html,
            "kde_jsme_dnes_html": kde_jsme_dnes_html,
            "sections": subsections,
            "zavazky": zavazky,
        })

    return program_intro, chapters


if __name__ == "__main__":
    intro, chapters = parse()
    out = {"intro": intro, "chapters": chapters}
    print(json.dumps(out, ensure_ascii=False, indent=2))
