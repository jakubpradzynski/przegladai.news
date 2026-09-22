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

Wynik: tabela + `.cache/newslettery/raport.json` (z przykładami trafień i tematami maili). Kolumny:
- **ZRODLO** — newsy z wydań, do których mail dał bezpośrednio link (także po rozwinięciu trackera),
  albo mail sam był artykułem (newslettery autorskie na Substacku: Addy Osmani, Pragmatic Engineer…),
- **TEMAT / T+PR** — newsy, które nadawca opisał, nawet z innym linkiem („pewne” / z „prawdopodobnymi”, precyzja ok. 2/3),
- **1SZY** — ile newsów ten nadawca podał jako pierwszy, **UNIK** — ile tylko on,
- **DOM%** — udział linków z próbki prowadzących do domen często używanych w wydaniach
  (0% bywa mylące, gdy nadawca linkuje do własnej strony albo trackera, którego nie da się rozwinąć),
- **AI%** — udział treści o AI.

## Krok 3 — Propozycja

Podziel nadawców na grupy i przy każdej wypisz krótkie uzasadnienie liczbami:
1. **Kluczowe źródła** — wysokie ZRODLO lub UNIK.
2. **Duplikaty** — duży wolumen, sporo tematów, ale UNIK≈0 i mało ZRODLO: wszystko to samo przychodzi z lepszych źródeł.
3. **Radar bez linków** — dużo TEMAT, często 1SZY, ale ZRODLO≈0 (linkują do siebie / paywall).
4. **Niewykorzystany potencjał** — mało trafień, ale wysoki DOM% i AI% albo profil pasujący do sekcji „Bliżej technologii”.
5. **Do wypisania** — brak trafień i niski potencjał (reklamy, poza tematem, tekst bez linków).
6. **Decyzja Kuby** — polscy twórcy i autorzy, których Kuba może chcieć zostawić z innych powodów.

Przy wątpliwych przejrzyj `tematy_maili` i `przyklady` z raportu. Pokaż Kubie wynik i szacunek,
ile maili tygodniowo ubędzie. **Nie wypisuj bez wyraźnej zgody Kuby.**

## Krok 4 — Wypisanie (po zgodzie)

Zatwierdzonych nadawców zapisz do `praca/do_wypisania.txt` (jedna linia = nadawca dokładnie jak w raporcie):

```bash
python3 narzedzia/newslettery/wypisz.py --lista praca/do_wypisania.txt            # podgląd
python3 narzedzia/newslettery/wypisz.py --lista praca/do_wypisania.txt --wykonaj
```

Skrypt używa one-click `List-Unsubscribe`, w razie potrzeby wysyła mail przez `gws`, a resztę
wypisuje jako linki do kliknięcia. Wynik zapisuje w `redakcja/zrodla.md`.
