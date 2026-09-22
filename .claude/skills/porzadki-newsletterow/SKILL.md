---
name: porzadki-newsletterow
description: Regularne porządki w subskrypcjach skrzynki przegladai.news - analizuje, które newslettery (etykieta Newsletter) dostarczają newsy do wydań PrzeglądAI, i uruchamia narzędzie, w którym Kuba przegląda kandydatów z dwoma ostatnimi mailami, oznacza "wypisz"/"zostaw" i jednym przyciskiem się wypisuje. Reaguje na "/porzadki-newsletterow", "porządki w newsletterach", "wyczyść subskrypcje".
---

Prowadzisz okresowe porządki w newsletterach. Kuba decyduje o każdym wypisaniu w narzędziu —
Ty przygotowujesz dane, uruchamiasz narzędzie i podsumowujesz wynik. **Nigdy nie wypisuj
nikogo bez decyzji Kuby w narzędziu.**

## Krok 1 — Maile

Uruchom w tle (pierwszy raz kilka minut, potem dociąga tylko brakujące):

```bash
python3 narzedzia/newslettery/pobierz_maile.py
```

Zakres: od 12 dni przed 10. wydaniem od końca do dziś (`--ostatnie-wydania N`, żeby zmienić).

## Krok 2 — Analiza i kandydaci

```bash
python3 narzedzia/newslettery/analizuj.py
python3 narzedzia/newslettery/kandydaci.py
```

`analizuj.py` dopasowuje maile do newsów z 10 ostatnich wydań (link, temat maila = artykuł,
ten sam temat innymi słowami) i ocenia potencjał. `kandydaci.py` wybiera listy mailingowe
o niskiej użyteczności, sortuje od tych, które najbardziej zaśmiecają skrzynkę, i pomija:
- listy oznaczone „zostaw” w ostatnich 90 dniach,
- listy już wypisane — chyba że nadal przysyłają maile (wracają na górę z adnotacją).

Decyzje są w `redakcja/newslettery.json`. Pokaż Kubie krótko: ilu kandydatów, ile maili
tygodniowo generują i 5 pierwszych z listy.

## Krok 3 — Przegląd w narzędziu

Przed startem zapamiętaj stan decyzji, a potem uruchom serwer w tle (`run_in_background: true`):

```bash
touch .cache/newslettery/przeglad_start
python3 narzedzia/newslettery/przeglad/server.py
```

Napisz Kubie: narzędzie działa na **http://localhost:8010**. Dla każdego kandydata widać statystyki,
powód, ostrzeżenia (np. ten sam wydawca co newsletter, który zostaje) i dwa ostatnie maile.
Klawisze: **W** — wypisz, **Z** — zostaw, ↑/↓ — nawigacja. Postęp zapisuje się na bieżąco,
można przerwać i wrócić. Na końcu „Podsumowanie i wypisanie” → „Wypisz zaznaczone”.

Poczekaj na zakończenie (Monitor):
`until [ redakcja/newslettery.json -nt .cache/newslettery/przeglad_start ]; do sleep 5; done`

## Krok 4 — Podsumowanie

Przeczytaj z `redakcja/newslettery.json` wpisy z dzisiejszą datą i podaj Kubie:
- ile list wypisano automatycznie i ile maili tygodniowo ubędzie,
- listy ze statusem `do_recznego` — z linkiem do wypisu (pole `uwagi`), do kliknięcia ręcznie,
- ile list zostawił (wrócą do oceny za 90 dni).

Zamknij serwer: `curl -s -X POST http://localhost:8010/api/shutdown`. Zaproponuj commit
`redakcja/newslettery.json` (to historia decyzji, potrzebna przy kolejnych porządkach).
