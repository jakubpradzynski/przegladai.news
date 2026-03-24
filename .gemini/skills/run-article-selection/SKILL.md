---
id: run-article-selection
name: Run Article Selection
description: Uruchamia lokalny interfejs graficzny do selekcji i edycji artykułów z pliku prepared_data.csv. Użyj, gdy użytkownik prosi o "uruchomienie selekcji artykułów".
metadata:
  pattern: tool-wrapper
---

Jesteś asystentem pomagającym w procesie tworzenia newslettera. Gdy użytkownik poprosi o "uruchomienie selekcji artykułów", Twoim zadaniem jest uruchomienie lokalnego serwera z aplikacją dla plików `prepared_data.csv`.

## Wytyczne
1. Uruchom skrypt serwera lokalnego `python3 .gemini/skills/run-article-selection/scripts/server.py` w tle. Pamiętaj o ustawieniu flagi `is_background` na `true` w `run_shell_command`.
2. Poinformuj użytkownika, że aplikacja webowa do selekcji została uruchomiona.
3. Podaj użytkownikowi link do aplikacji: **http://localhost:8000**
4. Wyjaśnij krótko, że w interfejsie może edytować, usuwać artykuły, a po zakończeniu prac - zapisać je do ostatecznego pliku `final_prepared_data.csv`.
