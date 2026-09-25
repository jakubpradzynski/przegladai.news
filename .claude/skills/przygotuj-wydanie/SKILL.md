---
name: przygotuj-wydanie
description: Po zapisaniu selekcji w admince przygotowuje propozycje tytułu wydania PrzeglądAI, wstęp, opis SEO, slug i napis na okładkę; Kuba poprawia je w zakładce "Wydanie" i generuje wydanie. Uruchamiany automatycznie przez zbierz-dane albo na "przygotuj wydanie".
---

Przygotowujesz drugi etap wydania. Selekcja jest zapisana w `praca/final_prepared_data.csv`,
adminka działa na http://localhost:8000 (jeśli nie działa — uruchom ją w tle:
`python3 narzedzia/adminka/server.py`).

## Krok 1 — Przeczytaj

- `praca/final_prepared_data.csv` — wybrane newsy,
- `redakcja/tytuly.md` (część „Tytuł wydania”), `redakcja/wstep.md`, `redakcja/seo.md`,
  zwłaszcza sekcje „Uwagi Kuby” i „Przykłady poprawek (AI → Kuba)”,
- `meta.json` z 3 ostatnich wydań w `wydania/` — dla ciągłości tonu i żeby nie powtarzać otwarć.

## Krok 2 — Propozycje

Numer wydania: ostatni katalog w `wydania/` + 1. Data: najbliższy piątek (`python3 -c "import sys; sys.path.insert(0,'narzedzia'); from lib import repo; print(repo.next_friday())"`).

Przygotuj:
- 3 propozycje tytułu `Wydanie #<nr>: …`, różniące się doborem tematów (nie tylko szykiem),
- wstęp pasujący do **pierwszej** propozycji (zasady: `redakcja/wstep.md`),
- opis SEO 120–160 znaków do pierwszej propozycji,
- slug: `python3 -c "import sys; sys.path.insert(0,'narzedzia'); from lib import repo; print(repo.issue_slug(<nr>, '<tytuł>'))"`,
- napis na okładkę `#<nr>: …` — sprawdź, że się mieści: `python3 narzedzia/okladka.py "<napis>" --podglad`.
  Gdy skrypt zgłasza, że się nie mieści, skróć napis według `redakcja/seo.md`.

Zapisz do `praca/wydanie_ai.json`:

```json
{"numer": 39, "propozycje_tytulu": ["Wydanie #39: …", "…", "…"], "wstep": "…",
 "opis_seo": "…", "slug": "wydanie-39-…", "data": "2026-09-25", "okladka": "#39: …"}
```

To wersja AI — nie zmieniaj jej potem. Z niej liczymy, co Kuba poprawił.

## Krok 3 — Przekaż Kubie

Napisz krótko: propozycje są w zakładce „Wydanie” w admince (odświeża się sama). Tam Kuba wybiera
tytuł, poprawia wstęp i SEO, podgląda okładkę i klika „Generuj wydanie”. Wypisz też 3 propozycje
tytułu w terminalu.

Poczekaj (Monitor, `until [ -f wydania/<NNN>/substack.html ]; do sleep 5; done`), a gdy wydanie
powstanie, podaj Kubie:
- `wydania/<NNN>/substack.html` — do otwarcia w przeglądarce i skopiowania do Substacka,
- `wydania/<NNN>/okladka.jpeg`,
- dane z bloku metadanych (tytuł, opis SEO, URL, data),
- przypomnienie: po zaplanowaniu posta na Substacku — `/zakoncz-wydanie`.

Kuba może generować wydanie wielokrotnie — każda kolejna wersja nadpisuje pliki w `wydania/<NNN>/`.
