---
name: zbierz-dane
description: Zbiera dane do nowego wydania PrzeglądAI - czyści linki z data.csv, opisuje je (tytuł, opis, tagi, czas, ocena), wylicza rekomendacje TOP 30 i uruchamia adminkę do selekcji. Reaguje na "/zbierz-dane", "zbierz dane z linków", "przygotuj artykuły".
---

Prowadzisz pierwszy etap wydania newslettera PrzeglądAI. Przejdź przez wszystkie kroki po kolei.
Pliki robocze lądują w `praca/` (jest w `.gitignore`).

## Krok 0 — Nauka z poprzedniego wydania

Numer ostatniego wydania to najwyższy katalog w `wydania/`. Uruchom:

```bash
python3 narzedzia/dziennik.py substack <numer_ostatniego>
```

Porównuje opublikowany post z tym, co wygenerowaliśmy, i zapisuje poprawki Kuby zrobione już
w Substacku do `redakcja/dziennik/poprawki.jsonl`. Jeśli post nie jest jeszcze opublikowany,
skrypt to zgłosi i nic się nie stanie.

Jeśli w dzienniku są wpisy nieprzetworzone (`python3 narzedzia/dziennik.py nowe`), uruchom najpierw
skill `ucz-sie`, żeby opisy powstały już według poprawionych reguł.

## Krok 1 — Linki

```bash
python3 narzedzia/przygotuj_linki.py
```

Skrypt czyści linki z `data.csv`, rozwija przekierowania, usuwa duplikaty i linki opublikowane
we wcześniejszych wydaniach, a wynik dzieli na paczki w `praca/linki.json`. Pokaż Kubie krótkie
podsumowanie (ile linków, ile odrzuconych i dlaczego).

## Krok 2 — Opisy (subagenci)

Dla każdej paczki z `praca/linki.json` uruchom subagenta `opisywacz` (Agent, `subagent_type: "opisywacz"`),
wszystkie paczki równolegle w jednej wiadomości. W prompcie podaj:
- listę linków z paczki,
- plik wynikowy: `praca/opisy/paczka_<id>.json`.

## Krok 3 — Linki, których subagent nie odczytał

Zbierz z `praca/opisy/*.json` pozycje z `"Przegladarka": true`. Dla każdej:
1. Otwórz stronę w Chrome (skill `claude-in-chrome`), odczytaj treść, autora, a dla wideo — długość.
2. Uzupełnij pola w JSON-ie według `redakcja/*.md` (przeczytaj je, jeśli jeszcze tego nie zrobiłeś) i ustaw `"Przegladarka": false`.
3. Jeśli domena wymagała przeglądarki, a nie ma jej w `redakcja/zrodla.md`, dopisz ją tam (sekcja
   „Strony, które trzeba otwierać w przeglądarce”, z datą). Podobnie nowo odkryte paywalle.

Gdy strony nie da się odczytać nawet w Chrome, ustaw `"Pominac": true` i powiedz o tym Kubie.

## Krok 4 — Duplikaty tematów

Przejrzyj tytuły wszystkich opisanych newsów. Gdy dwa linki opisują to samo wydarzenie, w słabszym
(według `redakcja/priorytety.md`: preferowane źródło pierwotne albo lepsza analiza) ustaw
`"Duplikat": "<tytuł lepszego>"`.

## Krok 5 — Scalenie i walidacja

```bash
python3 narzedzia/scal_opisy.py
```

Skrypt sprawdza też, czy temat nie był już w 2 ostatnich wydaniach — także pod innym linkiem
(`narzedzia/lib/tematy.py`). Taki news trafia do rezerwy z uzasadnieniem „BYŁO W WYDANIU #N: …”,
a podobny (niepewny) dostaje dopisek „podobny news był w #N”. Kuba widzi to w admince.

Gdy skrypt zgłasza problemy (zakazane frazy, długość, tagi, czas), popraw wskazane pozycje
w `praca/opisy/*.json` i uruchom ponownie. Dopiero gdy przejdzie, idź dalej. Skrypt zapisuje
`praca/prepared_data.csv` i nietykalną kopię `praca/wersja_ai.csv` — z niej potem liczymy,
co Kuba poprawił.

## Krok 6 — Adminka

Uruchom w tle (`run_in_background: true`):

```bash
python3 narzedzia/adminka/server.py
```

Napisz Kubie: adminka działa na **http://localhost:8000**. W zakładce „Selekcja” newsy są podzielone
na sekcje, rekomendacje AI są już zaznaczone, a rezerwa jest pod kreską. Po kliknięciu „Zapisz selekcję”
przygotujesz propozycje tytułu, wstęp i opis SEO.

Poczekaj, aż pojawi się `praca/final_prepared_data.csv` (Monitor z pętlą `until [ -f praca/final_prepared_data.csv ]; do sleep 5; done`),
a potem od razu przejdź do skilla `przygotuj-wydanie` — bez pytania Kuby.
