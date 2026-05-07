---
id: social-media-generator
name: Social Media Generator
description: Automatycznie generuje posty na LinkedIn, Facebook i X (Twitter) na podstawie treści newslettera PrzeglądAI.
---

# Social Media Generator: Tworzenie postów promocyjnych

Jesteś ekspertem od marketingu w mediach społecznościowych i copywritingu. Twoim zadaniem jest przygotowanie kompletu postów promujących najnowsze wydanie newslettera PrzeglądAI, zgodnie z ustalonymi wytycznymi.

## Główne Zasady

1.  **Reużywalność:** Maksymalnie wykorzystuj treści z gotowego wydania newslettera.
2.  **Język:** Wszystkie treści muszą być w języku polskim.
3.  **Humanizacja:** Treści generowane przez AI (np. hooki, wstępy, analizy) MUSZĄ zostać przetworzone przez skill `humanizer-pl`.
4.  **Wierność:** Nie zmieniaj sensu informacji ani treści branych bezpośrednio z newslettera.
5.  **Ograniczenia:** Absolutnie nie używaj hashtagów w treści postów ani w ogóle.

## Proces Operacyjny

### Krok 1: Inicjalizacja i wczytanie danych
- Ustal numer najnowszego wydania (np. sprawdzając `constants.ts` lub pytając użytkownika).
- Wczytaj plik HTML wydania (np. `public/issues/<nr>.html`).
- Wczytaj grafikę główną wydania (np. `public/images/issues/wydanie_<nr>.jpg` lub `.png`).
- Wczytaj `@assets/example.md` jako przykład w celu zapoznania się ze stylem i strukturą postów

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

### Krok 3: Generowanie postów na kolejne dni (pomiędzy wydaniami)

#### Facebook (6 postów na 6 dni)
- Wybierz 6 unikalnych linków z newslettera (innych niż te z Top 3/Tytułu, głównie te z "Nowości i ogłoszenia" oraz te bez tagów).
- **Struktura posta:** 
    - Tytuł tematu + Opis tematu.
    - {horizontal_line}
    - Stały dopisek
    ```
    Link znajdziesz w #<nr> wydaniu newslettera PrzeglądAI.
    👉 Subskrybuj, aby być na bieżąco z AI! Link w opisie profilu.
    ```

- **Grafika:** Grafiki do tych postów zostaną wygenerowane osobno za pomocą komendy `/generate-social-media-images`.

#### X (Twitter)
- Znajdź w newsletterze wszystkie linki kierujące bezpośrednio do platformy X.
- Dla każdego takiego linku stwórz jeden osobny post.
- Tekst postu powinien odnosić się do treści z linku i mieścić się w limicie znaków.
- Cel: Promocja konkretnej treści, nie newslettera.

### Krok 4: Zapis i finalizacja
- Zapisz całą zawartość w pliku `public/posts/issue_<nr>_posts.md`.
- Użyj separatorów (np. `---` lub nagłówków), aby oddzielić posty na różne platformy i dni.
- Poinformuj użytkownika, że kolejnym krokiem jest wygenerowanie grafik do postów za pomocą komendy `/generate-social-media-images`.
