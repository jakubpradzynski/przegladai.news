---
name: porzadki-newsletterow
description: Sprawdza, które newslettery w skrzynce przegladai.news (etykieta Newsletter) faktycznie dostarczają newsy do wydań PrzeglądAI, i po akceptacji Kuby wypisuje z bezużytecznych. Reaguje na "porządki w newsletterach", "z których newsletterów się wypisać".
---

## Krok 1 — Maile

Zakres: od tygodnia przed 10. wydaniem od końca do daty ostatniego wydania (daty w `wydania/*/meta.json`).

```bash
python3 narzedzia/newslettery/pobierz_maile.py --od <RRRR-MM-DD> --do <RRRR-MM-DD>
```

Pobiera tylko brakujące maile do `.cache/newslettery/maile.jsonl` (kilka minut, uruchom w tle).

## Krok 2 — Analiza

```bash
python3 narzedzia/newslettery/analizuj.py --wydania <od>-<do>
```

Dopasowuje newsy z wydań do linków w mailach (URL, a przy trackerach — tekst wokół linku
i rozwinięte przekierowanie). Wynik: tabela + `.cache/newslettery/raport.json`.
Kolumny: MAILE, TRAF (newsy z wydań w mailach), URL (potwierdzone adresem), UNIK (news był
tylko w tym newsletterze), L/MAIL (linki treści na mail).

## Krok 3 — Propozycja

Podziel nadawców:
- **wypisać**: 0 trafień przy ≥3 mailach, albo ≤1 trafienie przy ≥20 mailach i 0 unikalnych;
- **decyzja Kuby**: polscy twórcy, autorzy z nazwiska i newslettery z 1–3 unikalnymi trafieniami przy dużym wolumenie;
- **zostają**: reszta.

Przy „wypisać” i „decyzja Kuby” przejrzyj 1–2 tematy maili z raportu (`tematy_maili`), żeby odróżnić
newsletter bez linków lub reklamowy od tematycznie nietrafionego. Pokaż Kubie tabelę z uzasadnieniem
i szacunkiem, ile maili tygodniowo ubędzie. **Nie wypisuj bez wyraźnej zgody Kuby.**

## Krok 4 — Wypisanie (po zgodzie)

Zatwierdzonych nadawców zapisz do `praca/do_wypisania.txt` (jedna linia = nadawca dokładnie jak w raporcie):

```bash
python3 narzedzia/newslettery/wypisz.py --lista praca/do_wypisania.txt            # podgląd
python3 narzedzia/newslettery/wypisz.py --lista praca/do_wypisania.txt --wykonaj
```

Skrypt używa one-click `List-Unsubscribe`, w razie potrzeby wysyła mail przez `gws`, a resztę
wypisuje jako linki do kliknięcia. Wynik zapisuje w `redakcja/zrodla.md`.
