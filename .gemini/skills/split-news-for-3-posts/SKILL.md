---
id: split-news-for-3-posts
name: Split News for 3 Posts
description: Dzieli newsy z ostatniego wydania newslettera na 3 części i przygotowuje konkretne posty
---

# Kroki

1. Wczytaj plik `/public/issues/{latest}.md`, gdzie `{latest}` to najwyższy numer.
2. Wydziel z niego linki, tytuły i opisy wszystkich newsów i podziel na 3 części zgodnie z tagami:
    - Newsy z tagiem "Nowości i ogłoszenia" idą do pierwszej części
    - Newsy z tagiem "Bliżej technologii" idą do drugiej części
    - Pozostałe newsy idą do trzeciej części
3. Dla każdej części przygotuj post na social media.
4. Zapisz wyniki w pliku `/public/posts/issue_{latest}_posts.md`.

# Wymagania

- Nie zmieniaj w żaden sposób tytułów newsów. Mają być dokładnie takie same jak w pliku `/public/issues/{latest}.md`.
- Nie zmieniaj w żaden sposób linków do newsów. Mają być dokładnie takie same jak w pliku `/public/issues/{latest}.md`.

# Posty

Każdy post mam mieć format:

```
1/3 paczek newsów z #{latest} wydania newslettera #PrzeglądAI:

🔹 {Tytuł PL}: {link}

🔹 {Tytuł PL}: {link}

🔹 ...

❓ Który news przykuł Twoją uwagę?

👉 Subskrybuj, aby być na bieżąco z tym co dzieje się w świecie AI: https://przegladai.news
```