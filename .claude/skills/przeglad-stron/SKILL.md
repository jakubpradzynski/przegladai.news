---
name: przeglad-stron
description: Przegląd stron i blogów śledzonych przez PrzeglądAI (redakcja/strony.json) - zbiera wpisy opublikowane od dnia przed ostatnim wydaniem, sprawdza dostępność każdej strony, robi preselekcję AI (tak / może / nie) według reguł uczonych na decyzjach Kuby i uruchamia narzędzie do szybkiego wyboru wpisów do data.csv. Reaguje na "/przeglad-stron", "przejrzyj strony", "sprawdź blogi". Dodawanie i usuwanie stron: skill strony.
---

Kuba uruchamia to w dniu przygotowania wydania (zwykle czwartek), przed `/zbierz-dane`.
Twoje zadanie: zebrać nowe wpisy, wstępnie je ocenić, dać Kubie narzędzie do wyboru i po jego
decyzjach samodzielnie poprawić reguły preselekcji. **Do `data.csv` trafia tylko to, co Kuba zatwierdzi.**

## Krok 1 — Zbieranie

```bash
python3 narzedzia/strony/zbierz.py
```

Zakres: od dnia przed ostatnim wydaniem (data z `wydania/NNN/meta.json`), żeby złapać też wpisy
z dnia, w którym powstawało poprzednie wydanie. Inna data: `--od RRRR-MM-DD`. Starsze wpisy
nie są brane; wpisy bez ustalonej daty też nie.

Statusy stron: `ok`; `uwaga` (wszystkie pobrane wpisy są nowe — kanał/listing mógł uciąć część tygodnia);
`problem` (brak wpisów albo dat — zmienił się układ strony); `blad` (HTTP 4xx/5xx, timeout);
`przegladarka` (strona blokuje pobieranie).

## Krok 2 — Dopełnienie przez przeglądarkę

Dla każdej strony ze statusem innym niż `ok` otwórz ją w Chrome (skill `claude-in-chrome`)
i odczytaj listę wpisów, np.:

```js
await new Promise(r => setTimeout(r, 2500));
[...document.querySelectorAll('a[href]')].map(a => ({href: a.href, text: a.innerText.replace(/\s+/g, ' ').slice(0, 160)}))
  .filter(x => x.text.length > 25)
```

Weź tylko wpisy z datą ≥ data „od” (datę zwykle widać w tekście linku; jeśli nie — otwórz artykuł).
Dla `uwaga` szukaj wpisów starszych niż te, które skrypt już ma (przewiń albo otwórz drugą stronę listingu).
Zapisz do `.cache/strony/przegladarka.json`:

```json
{"od": "<ta sama data co w .cache/strony/wynik.json>",
 "wpisy": [{"strona": "<nazwa z strony.json>", "tytul": "...", "link": "...", "data": "RRRR-MM-DD", "opis": "..."}],
 "sprawdzone": ["<nazwy stron sprawdzonych w przeglądarce, także te bez nowych wpisów>"]}
```

Gdy strona nie działa także w Chrome — zostaw ją i powiedz o tym Kubie w kroku 5. Gdy znajdziesz
sposób, żeby działała bez przeglądarki (np. kanał RSS), popraw ją przez skill `strony`.

## Krok 3 — Preselekcja AI

```bash
python3 narzedzia/strony/preselekcja.py przygotuj
```

Skrypt najpierw stosuje reguły automatyczne z `redakcja/preselekcja.md` (bez AI, natychmiast): wpisy
bez związku z AI na stronach ogólnych i tytuły pasujące do wzorców odrzucenia dostają „nie”.
Resztę dzieli na paczki po 25 w `.cache/strony/do_oceny/paczka_NN.json`.

Dla **każdej paczki** uruchom subagenta `preselektor` (Agent, `subagent_type: "preselektor"`) —
**wszystkie naraz, w jednej wiadomości**, żeby działały równolegle. Polecenie dla każdego:
„Oceń `.cache/strony/do_oceny/paczka_NN.json`, wynik zapisz do `.cache/strony/oceny/paczka_NN.json`.”
Preselektor ocenia tylko po tytule i opisie (Haiku, bez sieci) — cała preselekcja powinna trwać
około minuty. Potem:

```bash
python3 narzedzia/strony/preselekcja.py sprawdz
```

Scala oceny do `.cache/strony/preselekcja.json`. Gdy brakuje paczki albo ocen, uruchom preselektora
ponownie tylko dla tej paczki. Gdy to się nie uda, idź dalej — wpisy bez oceny trafią do „Do decyzji”.

## Krok 4 — Narzędzie

W tle (`run_in_background: true`):

```bash
touch .cache/strony/przeglad_start
python3 narzedzia/strony/przeglad/server.py
```

Napisz Kubie: **http://localhost:8020** i krótko, ile jest „Proponowanych” (zaznaczonych od razu),
ile „Do decyzji” i ile „Odrzuconych przez AI” (zwiniętych — można rozwinąć i sprawdzić).
Klawisze: ↑/↓ lub J/K — ruch, Spacja — zaznacz/odznacz, O — otwórz artykuł.
„Zapisz wybrane do data.csv” dopisuje zaznaczone linki bez duplikatów, a do
`redakcja/dziennik/strony_wybory.jsonl` trafia każdy pokazany wpis z oceną AI i decyzją Kuby.

Poczekaj (Monitor): `until [ data.csv -nt .cache/strony/przeglad_start ]; do sleep 5; done`,
potem zamknij serwer: `curl -s -X POST http://localhost:8020/api/shutdown`.

## Krok 5 — Nauka i podsumowanie

Od razu, bez pytania Kuby, uruchom skill `ucz-sie` — część 2 „preselekcja wpisów ze stron”.
Poprawia `redakcja/preselekcja.md` na podstawie rozbieżności między AI a Kubą, żeby w kolejnym
tygodniu mniej trzeba było przeklikać.

Podaj Kubie:
- ile linków dodano do `data.csv`,
- zgodność AI (np. „z 14 proponowanych wziąłeś 11; z „Do decyzji” wziąłeś 6 z 40”),
- co zmieniło się w regułach preselekcji,
- które strony nie działają albo zmieniły układ.

Z `redakcja/dziennik/strony.jsonl`, gdy są co najmniej 4 przeglądy: strony, z których Kuba nic nie
wybrał w ostatnich 4+ przeglądach — zaproponuj usunięcie (skill `strony`, decyzja Kuby).
