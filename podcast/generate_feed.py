"""
Vygeneruje podcastový RSS feed (feed.xml) z episodes.json.

Použití:
    python generate_feed.py

Přečte episodes.json ve stejné složce a vytvoří/přepíše feed.xml.
Až přidáš novou epizodu, stačí přidat nový záznam do "episodes" v episodes.json
(mp3 soubor nahraj do episodes/) a skript spustit znovu.
"""

import json
import os
from datetime import datetime, timezone, timedelta
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "episodes.json")
OUT_PATH = os.path.join(HERE, "feed.xml")

PRAGUE_OFFSET = timedelta(hours=2)  # CEST; v zimě (CET) změň na hours=1


def rfc2822(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=8, tzinfo=timezone(PRAGUE_OFFSET)
    )
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")


def build_feed(data: dict) -> str:
    p = data["podcast"]
    base_url = p["base_url"].rstrip("/") + "/"
    cover_url = base_url + p["cover_image"]

    items = []
    for ep in data["episodes"]:
        audio_url = base_url + "episodes/" + ep["slug"]
        image_tag = ""
        if ep.get("cover_image"):
            episode_cover_url = base_url + ep["cover_image"]
            image_tag = f'\n      <itunes:image href="{escape(episode_cover_url)}"/>'
        items.append(f"""
    <item>
      <title>{escape(ep["title"])}</title>
      <description>{escape(ep["description"])}</description>
      <enclosure url="{escape(audio_url)}" length="{ep["file_size_bytes"]}" type="audio/mpeg"/>
      <guid isPermaLink="false">{escape(ep["slug"])}</guid>
      <pubDate>{rfc2822(ep["pub_date"])}</pubDate>
      <itunes:duration>{ep["duration"]}</itunes:duration>
      <itunes:episode>{ep["episode_number"]}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>{"true" if p["explicit"] else "false"}</itunes:explicit>{image_tag}
    </item>""")

    channel = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{escape(p["title"])}</title>
    <link>{escape(p["link"])}</link>
    <language>{p["language"]}</language>
    <description>{escape(p["description"])}</description>
    <itunes:author>{escape(p["author"])}</itunes:author>
    <itunes:explicit>{"true" if p["explicit"] else "false"}</itunes:explicit>
    <itunes:image href="{escape(cover_url)}"/>
    <image>
      <url>{escape(cover_url)}</url>
      <title>{escape(p["title"])}</title>
      <link>{escape(p["link"])}</link>
    </image>
    <itunes:owner>
      <itunes:name>{escape(p["author"])}</itunes:name>
      <itunes:email>{escape(p["owner_email"])}</itunes:email>
    </itunes:owner>
    <itunes:category text="{escape(p["category"])}">
      <itunes:category text="{escape(p["subcategory"])}"/>
    </itunes:category>
{''.join(items)}
  </channel>
</rss>
"""
    return channel


if __name__ == "__main__":
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    xml = build_feed(data)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"Hotovo! Feed vygenerován: {OUT_PATH}")
    print(f"Epizod ve feedu: {len(data['episodes'])}")
