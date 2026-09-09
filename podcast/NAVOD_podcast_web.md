# Návod: vlastní podcastový feed na statickém webu

Tahle složka obsahuje kompletní podklad pro podcast „Brno do detailu" – stačí ji
zapojit do repozitáře vašeho webu.

## 1. Doplň chybějící údaje

Otevři `episodes.json` a nahraď:

- `podcast.author` – jméno/organizaci, která podcast vydává
- `podcast.owner_email` – kontaktní e-mail (Apple/Spotify ho může chtít ověřit)
- `podcast.base_url` – veřejná adresa, na které bude tahle složka dostupná,
  např. `https://www.brnododetailu.cz/podcast/`
- `podcast.link` – adresa hlavního webu

## 2. Přidej obálku (cover art)

Do této složky přidej `cover.jpg` – čtvercový obrázek, ideálně 3000×3000 px
(minimálně 1400×1400 px), formát JPG nebo PNG, bez průhlednosti. Bez něj feed
projde validací, ale Spotify/Apple ho nepřijmou.

## 3. Nahraj do repozitáře webu

Zkopíruj celý obsah téhle složky (kromě tohoto návodu a `generate_feed.py`,
pokud nechceš) do webu na cestu odpovídající `base_url`, typicky něco jako:

```
web-repo/
  static/podcast/
    feed.xml
    cover.jpg
    episodes/
      kapitola_01_bydleni_finalni.mp3
      kapitola_02_doprava_finalni.mp3
      ...
```

Podle toho, jak je web postavený (Hugo, Jekyll, Next.js apod.), se přesná
cesta pro statické soubory může lišit – hlavní je, aby po nasazení byl
`feed.xml` dostupný přesně na adrese z `podcast.base_url` + `feed.xml`.

## 4. Commit a push

Standardní `git add`, `git commit`, `git push` – jakmile se web nasadí, feed
je živý.

## 5. Ověř feed

Před registrací na Spotify/Apple zkontroluj, že feed je validní, např. přes
https://podba.se/validate/ (vlož adresu feedu).

## 6. Zaregistruj feed

- **Spotify for Podcasters**: podcasters.spotify.com → přihlásit se →
  přidat nový podcast → vložit adresu feedu.
- **Apple Podcasts Connect**: podcastsconnect.apple.com → přidat podcast →
  vložit adresu feedu.

Registrace je jednorázová. Od té chvíle si obě služby feed samy pravidelně
kontrolují (obvykle do pár hodin po změně) a nové epizody se objeví
automaticky – stačí do `episodes.json` přidat nový záznam, nahrát mp3 do
`episodes/` a spustit `python generate_feed.py`.

## 7. Přidání další epizody

1. Finální mp3 zkopíruj do `episodes/`.
2. Do `episodes.json` přidej nový záznam do pole `episodes` (zkopíruj
   strukturu existujícího a uprav `slug`, `title`, `description`, `pub_date`,
   `duration`, `file_size_bytes` – velikost souboru v bajtech zjistíš třeba
   příkazem `ls -la`).
3. Spusť `python generate_feed.py` – přepíše `feed.xml`.
4. Commit, push, nasadit.

## Poznámka k datům publikace

`pub_date` u epizod 2–7 jsou teď jen orientační (týden po sobě od dnešního
dne) – uprav je na skutečné datum, kdy budete jednotlivé kapitoly reálně
zveřejňovat.
