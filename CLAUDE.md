# PrzeglądAI — repozytorium newslettera

Cotygodniowy newsletter o AI (piątek), publikowany na Substacku (przegladai.substack.com).
Repo służy do przygotowania wydania z Claude Code i archiwum wydań. Autor: Kuba.

## Cotygodniowy proces

1. **Codziennie** Kuba wrzuca linki do `data.csv` (dowolny format, byle URL-e).
   W dniu wydania **`/przeglad-stron`** — nowe wpisy ze śledzonych stron (`redakcja/strony.json`) od dnia
   przed ostatnim wydaniem, preselekcja AI (subagent `preselektor`, reguły `redakcja/preselekcja.md`),
   narzędzie na http://localhost:8020, wybrane linki trafiają do `data.csv`, reguły uczą się na decyzjach.
   Lista stron: skill **`/strony`** (dodaj / usuń / lista) — zawsze przez `narzedzia/strony/zarzadzaj.py`.
2. **`/zbierz-dane`** (czwartek) — skill `zbierz-dane`: czyszczenie linków, opisy przez subagentów
   `opisywacz`, ocena i rekomendacje TOP 30, adminka na http://localhost:8000.
3. **Adminka** — Kuba wybiera newsy i poprawia teksty, potem w zakładce „Wydanie” wybiera tytuł,
   poprawia wstęp i SEO i klika „Generuj wydanie” (skill `przygotuj-wydanie` przygotowuje propozycje).
4. **Substack** — Kuba ręcznie wkleja `wydania/NNN/substack.html`, dodaje okładkę i planuje wysyłkę.
   Nie automatyzujemy publikacji na Substacku w żadnej formie.
5. **`/zakoncz-wydanie`** — dziennik poprawek, `ucz-sie`, sprzątanie, branch `issue-N`, PR z `/schedule` na piątek.
6. **`/posty-social [nr]`** (osobny etap po wydaniu) — post główny ze wstępu + propozycje tematów postów pogłębionych;
   w narzędziu na http://localhost:8030 Kuba wybiera tematy, subagenci `social-autor` piszą posty (LinkedIn — ten sam
   tekst na Facebook i Substack Notes — oraz wątek na X), infografiki (`narzedzia/social/grafika.py`) i prompty do zdjęć,
   a `social-weryfikator` sprawdza każdy fakt w źródle (link do podświetlonego fragmentu).
   Kuba poprawia w narzędziu albo prosi Claude; `dziennik.py social` + `ucz-sie` uczą `redakcja/social*.md` i `o-mnie.md`.
   Publikacja ręczna. Cały przepływ i co się z czego uczy: `narzedzia/social/README.md`.

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
wydania/NNN/      archiwum: substack.html, dane.csv, meta.json, okladka.jpeg, social/ (posty social)
narzedzia/        skrypty Pythona (lib/ — wspólne), adminka/, okladka/ (szablon, font),
                  newslettery/ (analiza skrzynki, kandydaci, przeglad/ — narzędzie do wypisywania),
                  strony/ (zbieranie wpisów ze stron, przeglad/ — wybór do data.csv),
                  social/ (posty social: posty.py, grafika.py, przeglad/ — narzędzie do postów)
strona/           przegladai.news — statyczne przekierowanie na Substacka (GitHub Pages)
.claude/          skille i subagenci (opisywacz, preselektor, social-autor, social-weryfikator)
```

## Uwagi techniczne

- Skrypty uruchamiamy z katalogu głównego: `python3 narzedzia/<skrypt>.py`. Zależności: `requests`, `bs4`, `Pillow`.
- Gmail skrzynki przegladai.news — przez CLI `gws` (`narzedzia/lib/gmail.py`, tylko odczyt). Jedyny wyjątek: wypisywanie z list w `narzedzia/newslettery/wypisz.py`, zawsze po decyzji Kuby.
- Strona `strona/` to tylko przekierowanie; nowe wydania jej nie zmieniają.
- Kolory tagów w `narzedzia/generuj_wydanie.py` są dokładnie takie jak na Substacku — nie zmieniać bez sprawdzenia opublikowanego posta.
