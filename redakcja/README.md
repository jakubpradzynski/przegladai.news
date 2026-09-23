# Redakcja: reguły, z których korzysta AI

Każdy krok generujący treść czyta pliki z tego katalogu. To jedyne miejsce, gdzie
opisany jest styl newslettera. Prompty w skillach tylko odsyłają tutaj.

| Plik | Co ustala |
|---|---|
| `tytuly.md` | Tytuły newsów i tytuł wydania |
| `opisy.md` | Opisy newsów: długość, budowa, ton, zakazane frazy |
| `tagi.md` | Tagi i pole `Czas` |
| `priorytety.md` | Ocena newsów, podział na sekcje, co trafia do TOP 30, kolejność w wydaniu |
| `wstep.md` | Tekst między „Cześć!” a „Zapraszam do lektury!” |
| `seo.md` | Opis SEO, slug, napis na okładce |
| `preselekcja.md` | Wstępna ocena wpisów ze stron (tak / może / nie) — uczona na decyzjach w `/przeglad-stron` |
| `strony.json` | Strony i blogi przeglądane przy każdym wydaniu (`/przeglad-stron`) |
| `newslettery.json` | Decyzje „wypisz” / „zostaw” dla newsletterów (`/porzadki-newsletterow`) |
| `zrodla.md` | Wiedza techniczna o źródłach: paywalle, strony wymagające przeglądarki, trackery, nadawcy newsletterów |

## Jak te pliki się zmieniają

**Sekcja „Uwagi Kuby”** w każdym pliku należy do Kuby. Wpisuje tam swoimi słowami,
czego oczekuje. Ma najwyższy priorytet: gdy coś w niej przeczy reszcie pliku, wygrywa
„Uwagi Kuby”. AI nigdy jej nie edytuje.

**Pozostałe sekcje uzupełnia AI na podstawie poprawek Kuby:**

1. Każda poprawka wygenerowanej treści (tytuł, opis, tag, usunięty news, wstęp, SEO, tytuł wydania,
   napis na okładce, zmiany zrobione później w Substacku) trafia do `dziennik/poprawki.jsonl`,
   a każda decyzja przy preselekcji wpisów ze stron — do `dziennik/strony_wybory.jsonl`.
   Pliki tylko rosną: wpisów nie usuwa się i nie zmienia.
2. Na końcu każdego wydania skill `ucz-sie` czyta nowe wpisy z dziennika i sam,
   bez pytania, aktualizuje reguły i przykłady w tych plikach.
3. Każda zmiana reguł jest opisana w `zmiany-regul.md` (też tylko dopisywany)
   i trafia do PR-a wydania, więc widać ją w diffie i można ją cofnąć.

Zasada uogólniania: pojedyncza poprawka staje się przykładem „AI → Kuba”,
powtarzający się wzorzec (2+ razy) staje się regułą. Przy konflikcie wygrywa
nowsza reguła, a stara zostaje odnotowana w `zmiany-regul.md`.

Reguły startowe zostały spisane z analizy wydań #29–#38 (wrzesień 2026).
