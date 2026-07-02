---
name: prepare-issue-on-articles
description: Przygotowuje nowe wydanie newslettera bazując na wyselekcjonowanych artykułach. Reaguje na polecenie takie jak np. "Przygotuj wydanie bazując na artykułach".
metadata:
  pattern: pipeline
  steps: "6"
---

Jesteś asystentem przygotowującym nowe wydanie newslettera PrzeglądAI. Przejdź po kolei przez wszystkie kroki. Nie pomijaj żadnego.

## Krok 1 — Wczytanie danych i zaproponowanie tytułu
- Odczytaj `final_prepared_data.csv`, aby zapoznać się z wyselekcjonowanymi newsami.
- Odczytaj `constants.ts`, aby zobaczyć, jaki był tytuł i id ostatniego wydania oraz jaki był styl tytułów (lekko marketingowe, zwięzłe streszczenie najważniejszych newsów, np. "Wydanie #12: Olaf z Krainy Lodu i AI w Google Maps").
- Oblicz `nowy_nr` wydania (ostatni numer + 1).
- Zaproponuj tytuł w formacie "Wydanie #<nowy_nr>: <treść>".
- ZAPYTAJ UŻYTKOWNIKA O AKCEPTACJĘ LUB WERSJĘ TYTUŁU (możesz np. zaproponować 2 warianty). Nie przechodź dalej, dopóki użytkownik nie zaakceptuje lub nie poda swojego tytułu.

## Krok 2 — Utworzenie pliku HTML
- Wygeneruj krótki tekst (2-3 zdania) jako wstęp do wydania, nawiązujący do najważniejszych newsów lub ogólnego tematu bieżącego zestawienia. Tekst ten zastąpi sekcję między "Cześć!" a "Zapraszam do lektury!".
- Uruchom skrypt w Pythonie (narzędzie `run_shell_command`): `python3 .agents/skills/prepare-issue-on-articles/scripts/generate_issue_html.py <ostatni_nr> <nowy_nr> "<tytuł>" "<wygenerowany_wstęp>"`, aby automatycznie wygenerować plik w folderze `public/issues/<nowy_nr>.html`. Skrypt ten pobiera odpowiednio poprzednie wydanie, uaktualnia blok z Top 3 informacjami, tytuł w tagu `<title>`, krótki wstęp do newslettera oraz podmienia zawartość sekcji z artykułami.
- Upewnij się po wykonaniu za pomocą narzędzia sprawdzającego (np. `read_file` pobieżnie), że plik faktycznie się wygenerował.

## Krok 3 — Aktualizacja plików konfiguracyjnych
- Ustal datę dla najnowszego wydania jako najbliższy piątek. Użyj do tego skryptu `.agents/skills/finalize-creating-issue/scripts/next_friday.py` i zamień format na `DD-MM-YYYY`.
- Możesz wykorzystać gotowy skrypt Pythona (o ile taki stworzysz lub istnieje np. `update_configs.py`), bądź dokonać edycji ręcznie za pomocą narzędzia `replace`.
- Zaktualizuj plik `constants.ts`. Dodaj nowy obiekt dla najnowszego wydania NA SAMĄ GÓRĘ tablicy `BLOG_POSTS`. Pola do zaktualizowania: `id`, `slug` (w formacie `wydanie-<nr>-<z-kreskami>`), `title`, `date` (data w formacie `DD-MM-YYYY` z najbliższego piątku), `htmlUrl` (/issues/<nowy_nr>.html).
- Zaktualizuj plik `public/llms.txt`, dodając wpis dla najnowszego wydania w sekcji `## Wydania` NA SAM DOŁ listy. Wpis w postaci: `- **Wydanie #<nr>** ...`.
- Zaktualizuj plik `public/sitemap.xml`, dodając blok `<url>` dla najnowszego wydania na SAM DOŁ pliku, tuż przed zamykającym tagiem `</urlset>`. Pamiętaj, aby data `<lastmod>` była wpisana w poprawnym formacie `YYYY-MM-DD`. Uruchomienie pomocniczego skryptu aktualizującego wszystko naraz jest mocno rekomendowane, zrób to poleceniem `python3 .agents/skills/prepare-issue-on-articles/scripts/update_configs.py <nowy_nr> "<tytuł>"`

## Krok 4 — Generowanie wersji HTML pod Substack
- Wygeneruj opis SEO dla tego wydania. Powinien być jak najlepiej zoptymalizowany pod SEO, konkretny i zachęcający do kliknięcia. Opisuje zawartość wydania. Długość: blisko 160 znaków (nie mniej niż 120).
- Pobierz `slug` i datę publikacji z danych ustalonych w Kroku 3.
- Uruchom skrypt: `python3 .agents/skills/prepare-issue-on-articles/scripts/generate_substack_html.py <nowy_nr> "<tytuł>" "<opis_seo>" "<slug>" "<data_publikacji_DD-MM-YYYY>"`
- Skrypt wygeneruje plik `public/substack_posts_html/issue_<nowy_nr>_substack.html` zawierający treść wydania w formacie gotowym do wklejenia do Substack, z widoczną sekcją metadanych na dole.

## Krok 5 — Przygotowanie grafiki promocyjnej
- Użyj narzędzia `generate_image` do zmodyfikowania obrazu okładki.
- Jako `ImagePaths` podaj pełną bezwzględną ścieżkę do obrazka z poprzedniego wydania (np. `/Users/jakubpradzynski/Projects/przegladai.news/public/images/issues/wydanie_<ostatni_nr>.jpeg`). Sprawdź z jakim rozszerzeniem jest ostatnie zdjęcie (zazwyczaj `.jpeg` lub `.jpg`).
- Jako `AspectRatio` podaj koniecznie `'16:9'`. To kluczowe, aby obraz zachował format i jakość (np. rozdzielczość taką jak 2752x1536).
- W argumencie `Prompt` musisz być bardzo precyzyjny: "Zaktualizuj tekst znajdujący się na samym środku obrazka. Zamień tekst '#<ostatni_nr>: <tytuł_poprzedniego_wydania_bez_slowa_Wydanie>' na '#<nowy_nr>: <nowy_tytuł_bez_slowa_Wydanie>'. Tło, styl, kolory, położenie innych napisów i elementów graficznych pozostaje absolutnie BEZ ZMIAN."
- Zapisz wygenerowany obraz w folderze `public/images/issues/wydanie_<nowy_nr>.jpeg` (skopiuj go z tymczasowej lokalizacji wyjściowej podanej przez narzędzie `generate_image` przy użyciu polecenia powłoki).

## Krok 6 — Zakończenie
- Poinformuj użytkownika, że nowa treść (HTML, grafika, konfiguracja, wersja Substack) jest przygotowana.
- Przypomnij, że kolejnymi krokami są:
  1. `/generate-social-media` — wygenerowanie postów na Social Media.
  2. `/finalize-issue` — ukończenie tworzenia wydania.
