---
name: zakoncz-wydanie
description: Finalizuje wydanie PrzeglądAI po wrzuceniu go na Substacka - zapisuje poprawki Kuby do dziennika, uczy reguły (ucz-sie), sprząta pliki robocze, commituje na branchu issue-N i tworzy PR zaplanowany na piątek. Reaguje na "/zakoncz-wydanie", "ukończ tworzenie wydania".
---

Finalizujesz wydanie. Przejdź przez wszystkie kroki po kolei.

## Krok 1 — Sprawdzenie

Numer wydania: `numer` z `praca/wydanie.json`. Upewnij się, że istnieją
`wydania/<NNN>/substack.html`, `dane.csv`, `meta.json` i `okladka.jpeg`. Jeśli czegoś brakuje — zatrzymaj się i powiedz Kubie.

## Krok 2 — Dziennik poprawek

```bash
python3 narzedzia/dziennik.py selekcja
python3 narzedzia/dziennik.py wydanie
```

Zapisują do `redakcja/dziennik/poprawki.jsonl` wszystko, co Kuba zmienił względem wersji AI:
tytuły, opisy, tagi, czas, odrzucone i dobrane newsy, tytuł wydania, wstęp, SEO, napis na okładce.
Poprawki zrobione później w edytorze Substacka złapie `/zbierz-dane` przy następnym wydaniu.

## Krok 3 — Nauka

Uruchom skill `ucz-sie`. Działa sam, bez pytania Kuby.

## Krok 4 — Sprzątanie

```bash
curl -s -X POST http://localhost:8000/api/shutdown || true
python3 narzedzia/wyczysc_data.py
rm -rf praca
```

`wyczysc_data.py` usuwa z `data.csv` tylko linie przetworzone w tym wydaniu. Linki dopisane
po `/zbierz-dane` zostają na kolejny tydzień.

## Krok 5 — Git i Pull Request

```bash
git checkout -b issue-<nr>
git add wydania/<NNN> redakcja
git commit -m "Issue #<nr>"
git push -u origin issue-<nr>
```

Jeśli w repo są inne niezacommitowane zmiany, nie dodawaj ich — zapytaj Kubę.

PR z automatycznym scaleniem w piątek rano (workflow `Issue Merge Schedule`):

```bash
gh pr create --title "Issue #<nr>" --body "/schedule $(python3 -c "import sys; sys.path.insert(0,'narzedzia'); from lib import repo; print(repo.next_friday().strftime('%Y-%m-%dT05:00:00.000Z'))")"
```

Podaj Kubie link do PR-a i krótkie podsumowanie z kroku 3: jakie reguły się zmieniły.
