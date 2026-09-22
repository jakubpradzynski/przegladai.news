# PrzeglądAI — repozytorium newslettera

Cotygodniowy newsletter o AI (piątek), publikowany na Substacku (przegladai.substack.com).
Repo służy do przygotowania wydania z Claude Code i archiwum wydań. Autor: Kuba.

## Cotygodniowy proces

1. **Codziennie** Kuba wrzuca linki do `data.csv` (dowolny format, byle URL-e).
2. **`/zbierz-dane`** (czwartek) — skill `zbierz-dane`: czyszczenie linków, opisy przez subagentów
   `opisywacz`, ocena i rekomendacje TOP 30, adminka na http://localhost:8000.
3. **Adminka** — Kuba wybiera newsy i poprawia teksty, potem w zakładce „Wydanie” wybiera tytuł,
   poprawia wstęp i SEO i klika „Generuj wydanie” (skill `przygotuj-wydanie` przygotowuje propozycje).
4. **Substack** — Kuba ręcznie wkleja `wydania/NNN/substack.html`, dodaje okładkę i planuje wysyłkę.
   Nie automatyzujemy publikacji na Substacku w żadnej formie.
5. **`/zakoncz-wydanie`** — dziennik poprawek, `ucz-sie`, sprzątanie, branch `issue-N`, PR z `/schedule` na piątek.

Co jakiś czas: **`/porzadki-newsletterow`** — analiza, które newslettery dostarczają newsy, i narzędzie
do przeglądu kandydatów (dwa ostatnie maile, „wypisz” / „zostaw”) z automatycznym wypisaniem.

## Samorozwój — najważniejsza zasada

Każda poprawka Kuby względem wersji AI trafia do `redakcja/dziennik/poprawki.jsonl` (tylko dopisujemy,
nigdy nie usuwamy) i jest automatycznie zamieniana na reguły w `redakcja/*.md` przez skill `ucz-sie`.
Bez pytania o zgodę — zmiany reguł idą do PR-a wydania i są opisane w `redakcja/zmiany-regul.md`.

Budując nowy krok albo zmieniając istniejący: jeśli AI coś generuje, a Kuba może to poprawić,
zapisz wersję AI, porównaj z finalną (`narzedzia/dziennik.py`) i podepnij pod `ucz-sie`.
Sekcji „Uwagi Kuby” w plikach `redakcja/` nie edytuje nikt poza Kubą.

## Struktura

```
data.csv          linki zbierane w tygodniu (gitignore)
praca/            pliki robocze bieżącego wydania (gitignore)
redakcja/         reguły stylu i wyboru newsów + dziennik poprawek — jedyne źródło prawdy o stylu
wydania/NNN/      archiwum: substack.html, dane.csv, meta.json, okladka.jpeg
narzedzia/        skrypty Pythona (lib/ — wspólne), adminka/, okladka/ (szablon, font),
                  newslettery/ (analiza skrzynki, kandydaci, przeglad/ — narzędzie do wypisywania)
strona/           przegladai.news — statyczne przekierowanie na Substacka (GitHub Pages)
.claude/          skille i subagent opisywacz
```

## Uwagi techniczne

- Skrypty uruchamiamy z katalogu głównego: `python3 narzedzia/<skrypt>.py`. Zależności: `requests`, `bs4`, `Pillow`.
- Gmail skrzynki przegladai.news — przez CLI `gws` (`narzedzia/lib/gmail.py`, tylko odczyt).
- Strona `strona/` to tylko przekierowanie; nowe wydania jej nie zmieniają.
- Kolory tagów w `narzedzia/generuj_wydanie.py` są dokładnie takie jak na Substacku — nie zmieniać bez sprawdzenia opublikowanego posta.
