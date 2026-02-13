---
id: prepare-data-csv
name: Prepare data csv
description: Przygotowuje plik csv do dalszego uzupełniania i utworzenia nowego wydania newslettera
---

# Kroki
1. Wczytaj plik data.csv
2. Użyj skilla clear-links-from-query-params aby oczyścić linki z parametrów
3. Usuń duplikaty z pliku cleaned_data.csv
4. Wczytaj linki z pliku cleaned_data.csv
5. Utwórz nowy plik prepared_data.csv, który będzie zawierał kolumny:
- Wydanie
- Link
- Tytuł
- Tytuł PL
- Tagi
- Czas
- Opis

Wypełnij pole `Wydanie` numerem podanego wydania newslettera.
Wypełnij pole `Link` linkiem z pliku cleaned_data.csv.
Pozostałe pola pozostaw puste.