---
name: przeglad-stron
description: Przegląd stron i blogów śledzonych przez PrzeglądAI (redakcja/strony.json) - zbiera wpisy opublikowane od dnia przed ostatnim wydaniem, sprawdza, czy każda strona jest dostępna, i uruchamia narzędzie, w którym Kuba szybko zaznacza wpisy do dopisania do data.csv. Reaguje na "/przeglad-stron", "przejrzyj strony", "sprawdź blogi". Także "dodaj stronę <url>" / "usuń stronę".
---

Kuba uruchamia to w dniu przygotowania wydania (zwykle czwartek), przed `/zbierz-dane`.
Twoje zadanie: zebrać nowe wpisy ze wszystkich stron, dopełnić to, czego skrypt nie odczytał,
i dać Kubie narzędzie do szybkiego wyboru. **Do `data.csv` trafia tylko to, co Kuba zaznaczy.**

## Krok 1 — Zbieranie

```bash
python3 narzedzia/strony/zbierz.py
```

Zakres: od dnia przed ostatnim wydaniem (data z `wydania/NNN/meta.json`) — tak, żeby złapać też
wpisy z dnia, w którym powstawało poprzednie wydanie. Inna data: `--od RRRR-MM-DD`.
Starsze wpisy nie są brane; wpisy bez ustalonej daty też nie.

Statusy stron:
- `ok` — strona odczytana (także gdy brak nowych wpisów),
- `uwaga` — wszystkie pobrane wpisy są nowe, więc kanał/listing mógł uciąć część tygodnia,
- `problem` — brak wpisów albo brak dat (zmienił się układ strony),
- `blad` — strona nie odpowiada (HTTP 4xx/5xx, timeout),
- `przegladarka` — strona blokuje zwykłe pobieranie (np. Perplexity).

## Krok 2 — Dopełnienie przez przeglądarkę

Dla każdej strony ze statusem innym niż `ok` otwórz ją w Chrome (skill `claude-in-chrome`)
i odczytaj listę wpisów, np.:

```js
await new Promise(r => setTimeout(r, 2500));
[...document.querySelectorAll('a[href]')].map(a => ({href: a.href, text: a.innerText.replace(/\s+/g, ' ').slice(0, 160)}))
  .filter(x => x.text.length > 25)
```

Weź tylko wpisy z datą ≥ data „od” (datę zwykle widać w tekście linku albo na stronie artykułu —
gdy jej nie ma, otwórz artykuł). Dla `uwaga` szukaj wpisów starszych niż te, które skrypt już ma
(przewiń / druga strona listingu). Zapisz wynik do `.cache/strony/przegladarka.json`:

```json
{"od": "<ta sama data co w wynik.json>",
 "wpisy": [{"strona": "<nazwa z strony.json>", "tytul": "...", "link": "...", "data": "RRRR-MM-DD", "opis": "..."}],
 "sprawdzone": ["<nazwy stron sprawdzonych w przeglądarce, także te bez nowych wpisów>"]}
```

Gdy strona nie działa także w Chrome — zostaw ją, powiesz o tym Kubie w kroku 4.
Gdy dało się ją odczytać zwykłym sposobem inaczej niż skrypt (np. znalazłeś kanał RSS),
popraw jej wpis w `redakcja/strony.json` (`feed`, `filtr`, `przegladarka`), żeby następnym razem
zadziałało samo, i dopisz uwagę do `redakcja/zrodla.md`.

## Krok 3 — Narzędzie

W tle (`run_in_background: true`):

```bash
touch .cache/strony/przeglad_start
python3 narzedzia/strony/przeglad/server.py
```

Napisz Kubie: **http://localhost:8020**. Na górze „Stan stron” (która strona ile nowych, które wymagają
uwagi), niżej nowe wpisy pogrupowane po stronach. Klawisze: ↑/↓ lub J/K — ruch, Spacja — zaznacz,
O — otwórz artykuł. „Zapisz wybrane do data.csv” dopisuje zaznaczone linki (bez duplikatów).
Wpisy, które już są w `data.csv`, są domyślnie ukryte.

Poczekaj (Monitor): `until [ data.csv -nt .cache/strony/przeglad_start ]; do sleep 5; done`,
potem zamknij serwer: `curl -s -X POST http://localhost:8020/api/shutdown`.

## Krok 4 — Podsumowanie i nauka

Podaj Kubie: ile linków dodano do `data.csv`, które strony nie działają albo zmieniły układ.

Z `redakcja/dziennik/strony.jsonl` (historia: ile nowych wpisów i ile wybranych na stronę, tylko dopisywana)
wypisz obserwacje, gdy są co najmniej 4 przeglądy:
- strony, z których Kuba nic nie wybrał w ostatnich 4+ przeglądach — propozycja usunięcia,
- strony, które co tydzień wymagają przeglądarki — propozycja poprawki konfiguracji.
Usunięcie strony to decyzja Kuby — zapytaj, nie usuwaj sam.

## Dodawanie i usuwanie stron

„Dodaj stronę <url>”: sprawdź, czy ma kanał RSS/Atom (`<link rel="alternate">` w HTML albo typowe
adresy: `/feed`, `/rss.xml`, `/atom.xml`, `/index.xml`, Blogger `/feeds/posts/default`, Medium `/feed`).
Dopisz do `redakcja/strony.json` (`nazwa`, `url`, opcjonalnie `feed`) i uruchom
`python3 narzedzia/strony/zbierz.py --strona "<nazwa>"`, żeby potwierdzić, że wpisy i daty się czytają.
„Usuń stronę”: usuń wpis z `redakcja/strony.json`.
