---
name: strony
description: Zarządzanie listą stron i blogów śledzonych przez PrzeglądAI (redakcja/strony.json) - dodawanie (z automatycznym wykryciem kanału RSS i testem, czy wpisy i daty się czytają), usuwanie, lista ze skutecznością, sprawdzenie strony. Reaguje na "dodaj stronę", "usuń stronę", "lista stron", "sprawdź stronę", "/strony".
---

Wszystkie zmiany listy stron idą przez skrypt `narzedzia/strony/zarzadzaj.py` — nie edytuj
`redakcja/strony.json` ręcznie. Skrypt dopisuje stronę tylko wtedy, gdy potwierdzi, że da się
odczytać jej wpisy z datami.

## Dodanie strony

```bash
python3 narzedzia/strony/zarzadzaj.py dodaj <url> --nazwa "<krótka nazwa>"
```

Skrypt szuka kanału RSS/Atom (w HTML i pod typowymi adresami). Gdy kanału nie ma, testuje odczyt listingu
i dat ze stron artykułów. Pokazuje 5 najnowszych wpisów — przeczytaj je i sprawdź, czy to faktycznie
artykuły z tej strony (a nie np. menu czy tagi). Gdy skrypt odmówi dodania (brak dat):
- podaj kanał ręcznie: `--feed <url>` (poszukaj go w Chrome, jeśli trzeba),
- zawęź linki do artykułów: `--filtr "/blog/"`,
- strona blokująca pobieranie: `--przegladarka` (wpisy będą zbierane przez Chrome w `/przeglad-stron`).

Nazwa ma być krótka i czytelna (np. „Anthropic Engineering”), bo widać ją w narzędziu przeglądu.
Na koniec pokaż Kubie, co zostało dodane (tryb: kanał / HTML / przeglądarka, najnowsze wpisy).

## Usunięcie strony

```bash
python3 narzedzia/strony/zarzadzaj.py usun "<nazwa albo url>"
```

Historia decyzji dla tej strony zostaje w `redakcja/dziennik/` — usuń ją też z tabeli
„Skuteczność stron” w `redakcja/preselekcja.md`.

## Lista i sprawdzenie

```bash
python3 narzedzia/strony/zarzadzaj.py lista                 # tryb i skuteczność (wzięte / wszystkie)
python3 narzedzia/strony/zarzadzaj.py sprawdz ["<nazwa>"]   # wpisy z ostatnich 30 dni
```

Po każdej zmianie zaproponuj commit `redakcja/strony.json`.
