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
- Uruchom skrypt w Pythonie (narzędzie `run_shell_command`): `python3 .gemini/skills/prepare-issue-on-articles/scripts/generate_issue_html.py <ostatni_nr> <nowy_nr> "<tytuł>" "<wygenerowany_wstęp>"`, aby automatycznie wygenerować plik w folderze `public/issues/<nowy_nr>.html`. Skrypt ten pobiera odpowiednio poprzednie wydanie, uaktualnia blok z Top 3 informacjami, tytuł w tagu `<title>`, krótki wstęp do newslettera oraz podmienia zawartość sekcji z artykułami.
- Upewnij się po wykonaniu za pomocą narzędzia sprawdzającego (np. `read_file` pobieżnie), że plik faktycznie się wygenerował.

## Krok 3 — Aktualizacja plików konfiguracyjnych
- Ustal datę dla najnowszego wydania jako najbliższy piątek. Użyj do tego skryptu `.gemini/skills/finalize-creating-issue/scripts/next_friday.py` i zamień format na `DD-MM-YYYY`.
- Możesz wykorzystać gotowy skrypt Pythona (o ile taki stworzysz lub istnieje np. `update_configs.py`), bądź dokonać edycji ręcznie za pomocą narzędzia `replace`.
- Zaktualizuj plik `constants.ts`. Dodaj nowy obiekt dla najnowszego wydania NA SAMĄ GÓRĘ tablicy `BLOG_POSTS`. Pola do zaktualizowania: `id`, `slug` (w formacie `wydanie-<nr>-<z-kreskami>`), `title`, `date` (data w formacie `DD-MM-YYYY` z najbliższego piątku), `htmlUrl` (/issues/<nowy_nr>.html).
- Zaktualizuj plik `public/llms.txt`, dodając wpis dla najnowszego wydania w sekcji `## Wydania` NA SAM DOŁ listy. Wpis w postaci: `- **Wydanie #<nr>** ...`.
- Zaktualizuj plik `public/sitemap.xml`, dodając blok `<url>` dla najnowszego wydania na SAM DOŁ pliku, tuż przed zamykającym tagiem `</urlset>`. Pamiętaj, aby data `<lastmod>` była wpisana w poprawnym formacie `YYYY-MM-DD`. Uruchomienie pomocniczego skryptu aktualizującego wszystko naraz jest mocno rekomendowane, zrób to poleceniem `python3 .gemini/skills/prepare-issue-on-articles/scripts/update_configs.py <nowy_nr> "<tytuł>"`

## Krok 4 — Utworzenie pliku z postami na Social Media
- Wygeneruj nowy zestaw wpisów w pliku `public/posts/issue_<nowy_nr>_posts.md`.
- **Zasady ogólne:**
    - Ton: Profesjonalny, analityczny i rzetelny (unikanie stylu czysto marketingowego).
    - Perspektywa: Nie pisz "przygotowałem/liśmy". Pisz o tym, co "można znaleźć w zestawieniu/wydaniu", jakie newsy/artykuły/posty są tam dostępne (np. "Te i inne ciekawe linki znajdziesz w <nr>. wydaniu PrzeglądAI").
    - Zasięgi: **NIE UMIESZCZAJ bezpośrednich linków** do wydania w głównej treści postów premierowych na LinkedIn/Facebook. Zamiast tego używaj sformułowania: "👉 Link do newslettera z najnowszym wydaniem znajdziesz w opisie profilu. Subskrybuj!".
    - Zgodność: Treść musi dokładnie pokrywać się z opisami (`news-desc`) z pliku HTML.
    - Formatowanie: **NIE UŻYWAJ pogrubienia (gwiazdek)** wewnątrz punktów list. Używaj emoji `🔹` na początku punktów.
    - Oznaczenia: Staraj się zamieszczać nazwy firm (np. Anthropic, Google, Meta) oraz autorów (jeśli są dostępni), aby umożliwić późniejsze oznaczenie ich w social mediach.

- **Struktura pliku:**
    1. **LinkedIn / Facebook:** Jeden wspólny, angażujący post promujący całe wydanie. Napisz go tak, aby brzmiał w 100% naturalnie, jak wpis człowieka dzielącego się swoimi obserwacjami. **Pamiętaj, że newsletter jest kuratorem treści (pośrednikiem)** – zbierasz najlepsze linki i krótko je streszczasz. Używaj formy pojedynczej ("zebrałem", "wyselekcjonowałem"). **Konstrukcja posta:**
        - Mocny hook (zacznij post od przyciągającego zdania, ale **absolutnie nie pisz wprost słowa "Hook:"**) i **szerszy, bardzo opisowy wstęp skupiony tylko na jednym, głównym temacie** wydania (narracja o konkretnym trendzie/wydarzeniu). **WAŻNE:** Zachowaj spokojny, analityczny ton. Bezwzględnie unikaj emocjonalnych, dramatycznych i typowych dla AI sformułowań (takich jak "prawdziwe trzęsienie ziemi", "rewolucja", "zmieniają zasady gry", "wstrząsnęło rynkiem"). Pisz konkretami.
        - Płynne przejście do podpunktów bez sztucznych sformułowań typu "Znajdziecie tam linki i omówienia". Użyj czegoś naturalnego, np. "Co jeszcze zebrałem w tym tygodniu?".
        - Ok. 2-3 krótkich punktów (z emoji `🔹`) dotyczących **INNYCH** tematów niż ten opisany we wstępie (absolutnie nie powtarzaj głównego tematu w podpunktach).
        - Krótkie zdanie podsumowujące.
        - Dokładne CTA na końcu: "👉 Link w opisie profilu. Subskrybuj!".
    2. **X (Twitter):** Jeden bardzo krótki, zwięzły post (pojedynczy, bez wątku). **Maksymalnie 280 znaków.** Szybki hook, 2 krótkie punkty oraz na samym końcu obowiązkowo: "👉 Link w Bio". Nie używaj bezpośrednich linków w treści posta na X. Nie generuj żadnych innych postów.

- Zapisz nowo wygenerowaną zawartość za pomocą `write_file`.

## Krok 5 — Przygotowanie grafiki promocyjnej
- Użyj narzędzia `mcp_nanobanana_edit_image`, aby zmodyfikować obraz okładki.
- Jako `file` podaj ŚCIEŻKĘ BAZOWĄ (np. `public/images/issues/wydanie_<ostatni_nr>.jpg`). Sprawdź z jakim rozszerzeniem jest ostatnie zdjęcie (może być .jpg, .jpeg, .png).
- W argumencie `prompt` musisz BYĆ BARDZO PRECYZYJNY i dodać wymóg rozdzielczości: "Zaktualizuj tekst znajdujący się na samym środku obrazka. Zamień tekst '#<ostatni_nr>: ...' na '#<nowy_nr>: <tytuł, który wybraliście bez członu Wydanie>'. Zmień rozmiar / wygeneruj ten obraz w rozdzielczości 4K (5636x3008). Jest to kluczowe: NIE ZMIENIAJ NIC INNEGO poza tekstem i rozdzielczością. Tło, kolory, położenie innych napisów i elementów graficznych pozostaje absolutnie BEZ ZMIAN."
- UWAGA: narzędzie generuje plik u siebie, zapytaj użytkownika lub zapisz go we właściwe miejsce (np. narzędzie może samo zrzucić gdzieś plik tymczasowy, użyj `run_shell_command` żeby przenieść to do `public/images/issues/wydanie_<nowy_nr>.jpg`). Właściwie, `mcp_nanobanana_edit_image` może nie zapisywać na dysk od razu w żądane miejsce, więc podążaj za jego wyjściem i upewnij się, że plik trafia do docelowego folderu `public/images/issues/`.

## Krok 6 — Zakończenie
- Poinformuj użytkownika, że nowa treść (HTML, wpisy na SM, grafika, konfiguracja) jest przygotowana.
- Przypomnij, że jeśli wszystko wygląda dobrze, następnym krokiem będzie użycie polecenia "Ukończ tworzenie wydania" (uruchomi to kolejny skill).
