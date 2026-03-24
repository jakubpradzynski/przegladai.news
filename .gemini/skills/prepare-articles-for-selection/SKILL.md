---
id: prepare-articles-for-selection
name: Prepare articles for selection
description: Odczytuje linki z pliku data.csv, czyści je z parametrów śledzących, a następnie przetwarza i generuje plik CSV gotowy do selekcji do newslettera. Użyj, gdy użytkownik prosi o "przygotowanie artykułów do selekcji" lub podobnie.
metadata:
  pattern: pipeline
  steps: "5"
---

Jesteś twórcą newslettera PrzeglądAI.news, doświadczonym dziennikarzem i inżynierem.
Twoim zadaniem jest przeprowadzić pełen proces, który połączy czyszczenie linków z tworzeniem bazy wiedzy w formacie CSV. Plikiem wejściowym domyślnie jest `data.csv`.

Skorzystaj ze wzorca pipeline i wykonaj poniższe kroki w podanej kolejności. **Nie pomijaj żadnego kroku**.

## Krok 1 — Czyszczenie linków
1. Uruchom dedykowany skrypt w Pythonie (korzystając z `run_shell_command`), aby wyczyścić linki z pliku wejściowego (domyślnie `data.csv`):
   `python3 .gemini/skills/prepare-articles-for-selection/scripts/clear_links.py data.csv`
2. Skrypt zapisze wynik w nowym pliku o nazwie `cleaned_data.csv`.
3. Przeczytaj wygenerowany plik `cleaned_data.csv` i wyodrębnij z niego wszystkie unikalne linki.

## Krok 2 — Analiza treści każdego linku (Context Gathering)
Dla każdego linku na z wyczyszczonej listy zapoznaj się z jego treścią, aby móc zebrać kontekst potrzebny do napisania tytułu, opisu, dobrania tagów i czasu.
- Użyj narzędzia `web_fetch` dla standardowych blogów i artykułów.
- **WAŻNE:** W przypadku portali, które blokują zwykłe zapytania HTTP (np. X/Twitter, LinkedIn, YouTube), musisz "otworzyć przeglądarkę" poprzez narzędzia MCP (np. `mcp_chrome-devtools_new_page`, `mcp_chrome-devtools_take_snapshot` czy `mcp_chrome-devtools_evaluate_script`) i przeanalizować treść, aby dowiedzieć się, kto jest autorem, o czym mówi wpis, lub (dla YT) jak długi jest dany filmik.
Zbierz kluczowe informacje w locie, w razie potrzeby twórz tymczasowe notatki.

## Krok 3 — Generowanie metadanych w formacie JSON
Wygeneruj dla każdego linku metadane: Tytuł, Opis, Tagi oraz Czas. Aby to zrobić poprawnie, musisz ściśle trzymać się wytycznych:
- Załaduj plik `references/title_guidelines.md` w celu wygenerowania Tytułu.
- Załaduj plik `references/description_guidelines.md` w celu wygenerowania Opisu.
- Załaduj plik `references/tag_guidelines.md` w celu wygenerowania Tagów oraz Czasu.

Pamiętaj, że:
- Teksty MUSZĄ być w języku polskim.
- Oryginalne (wyczyszczone) linki muszą pozostać w niezmienionej formie.
Przygotuj zebrane dane jako poprawną tablicę obiektów JSON, gdzie każdy element posiada klucze: `"Link"`, `"Tytuł"`, `"Opis"`, `"Tagi"`, `"Czas"`.
Użyj narzędzia `write_file`, aby zapisać tę tablicę tymczasowo jako `data_temp.json`.

## Krok 4 — Konwersja JSON do bezpiecznego formatu CSV
Musisz wygenerować plik CSV, w którym teksty są zawarte w podwójnych cudzysłowach `""`, co jest niezbędne dla poprawnego formatowania po przecinku. Uruchom dedykowany skrypt w Pythonie:
Wykonaj komendę:
`python3 .gemini/skills/prepare-articles-for-selection/scripts/json_to_csv.py data_temp.json prepared_data.csv`

## Krok 5 — Kontrola Jakości (QA)
Zajrzyj do nowo utworzonego pliku `prepared_data.csv` i upewnij się, że:
- Posiada on dokładnie kolumny: Link, Tytuł, Opis, Tagi, Czas.
- Wartości są poprawne, oddzielone przecinkami i otoczone przez `""`.
- Tagi pochodzą wyłącznie z dozwolonej listy i są alfabetycznie posortowane (zgodnie z `tag_guidelines.md`).
- Pola z "Czasem" zawierają jedynie czas w wymaganym formacie dla wideo.
Gdy upewnisz się, że plik jest zgodny z wytycznymi, powiadom użytkownika o sukcesie i skasuj tymczasowy plik `data_temp.json`.
