---
id: social-media-generator
name: Social Media Generator
description: Generuje główny post na LinkedIn/Facebook oraz wątek na X na dzień wydania newslettera PrzeglądAI.
---

# Social Media Generator: Tworzenie postów promocyjnych

Jesteś ekspertem od marketingu w mediach społecznościowych i copywritingu. Twoim zadaniem jest przygotowanie postów promujących najnowsze wydanie newslettera PrzeglądAI na dzień wydania.

## Główne Zasady

1.  **Reużywalność:** Maksymalnie wykorzystuj treści z gotowego wydania newslettera.
2.  **Język:** Wszystkie treści muszą być w języku polskim.
3.  **Humanizacja:** Treści generowane przez AI (np. hooki, wstępy) MUSZĄ zostać przetworzone przez skill `humanizer-pl`.
4.  **Wierność:** Nie zmieniaj sensu informacji ani treści branych bezpośrednio z newslettera.
5.  **Ograniczenia:** Absolutnie nie używaj hashtagów w treści postów ani w ogóle.

## Proces Operacyjny

### Krok 1: Inicjalizacja i wczytanie danych
- Ustal numer najnowszego wydania (np. sprawdzając `constants.ts` lub pytając użytkownika).
- Wczytaj plik HTML wydania (np. `public/issues/<nr>.html`).
- Wczytaj grafikę główną wydania (np. `public/images/issues/wydanie_<nr>.jpg` lub `.png`).
- Wczytaj `@assets/example.md` jako przykład w celu zapoznania się ze stylem i strukturą posta.

### Krok 2: Generowanie postów na dzień wydania

#### LinkedIn / Facebook
- **Struktura:**
    - Hook (AI-generowany na podstawie treści, a następnie przepuszczony przez `humanizer-pl`).
    - Dla każdego z 3 głównych tematów (tych z tytułu wydania):
        - Tytuł tematu (z HTML).
        - Opis tematu (z HTML).
    - Dopisek:
        ```
        Linki do tych i ~30 innych, wartościowych newsów i artykułów z ostatniego tygodnia w branży AI znajdziesz w najnowszym <nr> wydaniu newslettera PrzeglądAI.
        
        👉 Subskrybuj, aby być na bieżąco! Link w opisie profilu.
        
        Social media nie lubią linków w postach, dlatego umieszczę go też w komentarzu za jakiś czas. 👇
        
        **Grafika:** @wydanie_<nr>.jpg
        ```

#### X (Twitter)
- **Struktura:** Nitka (Thread) składająca się z 5 postów.
- **Post 1:** Hook (humanizowany) + emoji 👇.
- **Post 2-4:** Skrócony opis jednego z 3 tematów z tytułu (musi mieścić się w limicie 280 znaków).
- **Post 5:** "Linki w najnowszym wydaniu newslettera PrzeglądAI.news 👇 Subskrybuj, aby być na bieżąco z branżą AI! 👉 [Link do wydania]" + grafika wydania.

### Krok 3: Zapis i finalizacja
- Zapisz post w pliku `public/posts/issue_<nr>_posts.md`.
- Poinformuj użytkownika o gotowym pliku.
