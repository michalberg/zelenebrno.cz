#!/usr/bin/env python3
"""Generate /aktuality/feed.xml (RSS 2.0) from build_aktuality.py's own ITEMS
list, so the feed can't drift from what's actually on the page. Run from
`site/docs/`: python3 scripts/build_aktuality_feed.py
"""
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from build_aktuality import ITEMS

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.zelenebrno.cz"


def rfc822(date_str):
    dt = datetime.strptime(date_str, "%d.%m.%Y")
    return dt.strftime("%a, %d %b %Y 00:00:00 +0200")


def build():
    items_xml = []
    for date_str, title, slug, image, description in ITEMS:
        url = f"{BASE}/{slug}"
        items_xml.append(f"""    <item>
      <title>{escape(title)}</title>
      <link>{escape(url)}</link>
      <guid isPermaLink="true">{escape(url)}</guid>
      <pubDate>{rfc822(date_str)}</pubDate>
      <description>{escape(description)}</description>
    </item>""")

    build_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Aktuality – Zelené Brno</title>
    <link>{BASE}/aktuality/</link>
    <description>Tiskové zprávy a aktuality koalice Zelené Brno k volbám do Zastupitelstva města Brna 2026.</description>
    <language>cs</language>
    <lastBuildDate>{build_date}</lastBuildDate>
{chr(10).join(items_xml)}
  </channel>
</rss>
"""
    out_dir = ROOT / "aktuality"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "feed.xml").write_text(xml, encoding="utf-8")
    print(f"wrote aktuality/feed.xml ({len(ITEMS)} items)")


if __name__ == "__main__":
    build()
