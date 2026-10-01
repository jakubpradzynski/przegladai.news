# Priorytety: ocena i wybór newsów

## Uwagi Kuby

_(miejsce na Twoje uwagi — AI tej sekcji nie zmienia)_

## Sekcje i proporcje

Wydanie ma 30 newsów w trzech sekcjach (sekcja wynika z tagu):

| Sekcja | Tag | Cel | Zakres w #29–#38 |
|---|---|---|---|
| Nowości | `Nowości i ogłoszenia` | 10 | 7–11 |
| Technologia | `Bliżej technologii` | 10 | 10–14 |
| Pozostałe | bez żadnego z dwóch powyższych (może mieć `Polska` / `Za paywallem`) | 10 | 4–10 |

Dodatkowo w całym wydaniu:
- `Polska`: 1–4 newsy. Dobry polski news ma pierwszeństwo przed podobnie ocenionym zagranicznym.
- Wideo/podcasty (pole `Czas`): 1–4.
- `Za paywallem`: najwyżej 2.
- Najwyżej 3 newsy z jednej domeny (youtube.com się nie liczy).

## Ocena 1–10

Oceniamy wartość dla czytelnika: osoby z branży IT, managera albo entuzjasty technologii,
który chce w 15 minut wiedzieć, co ważnego wydarzyło się w AI w tym tygodniu.

| Ocena | Co to jest |
|---|---|
| 9–10 | Temat tygodnia: duża premiera (nowy model czołowego laboratorium, nowy produkt Apple/Google/OpenAI), duże przejęcie lub runda, wydarzenie, o którym mówi cała branża. Kandydat do tytułu wydania. |
| 7–8 | Wyraźnie wartościowe: konkretny, dobrze napisany tekst techniczny znanego autora (Addy Osmani, Martin Fowler, Pragmatic Engineer, Dan Luu), istotne ogłoszenie, mocny polski temat, ciekawe dane lub badanie. |
| 5–6 | Poprawne, ale do zastąpienia: mniejsze ogłoszenie, kolejny poradnik o agentach bez nowego wątku, ciekawostka. |
| 3–4 | Słabe: marketing przebrany za artykuł, powtórka tematu, który już był, treść ogólnikowa. |
| 1–2 | Nie brać: reklama, oferta pracy, strona bez treści, news sprzed tygodni. |

Podwyższają ocenę: konkretne liczby, oryginalne dane, case study z firmy, autor-praktyk,
temat, który czytelnik może od razu zastosować, związek z Polską, świeżość (ostatnie 7 dni).
Obniżają: clickbait, brak konkretów, temat opisany już w poprzednich wydaniach,
tekst sponsorowany, paywall bez widocznej treści.

## Rekomendacja

W każdej sekcji 10 najwyżej ocenionych dostaje `TOP`, reszta `rezerwa`.
Gdy sekcja ma mniej niż 10 dobrych kandydatów (ocena ≥ 5), brakujące miejsca
przechodzą do sekcji, która ma najwięcej mocnych newsów w rezerwie.

**Duplikaty tematu:** gdy dwa linki opisują to samo wydarzenie, TOP dostaje tylko jeden —
preferowane źródło pierwotne (blog firmy) albo tekst z lepszą analizą. Drugi dostaje
`rezerwa` i adnotację w `Uzasadnienie`: „duplikat: <tytuł>”.

## Kolejność w wydaniu

1. Nowości i ogłoszenia (najpierw z tagiem `Polska`), dalej alfabetycznie po tytule.
2. Bliżej technologii (najpierw z tagiem `Polska`), dalej alfabetycznie.
3. Tylko `Polska`.
4. Bez tagu, alfabetycznie.

Alfabet polski (ł po l itd.). W obrębie każdej grupy Kuba może zmienić kolejność ręcznie w admince (↑/↓);
takie zmiany trafiają do dziennika (`pole: kolejnosc`) — gdy się powtarzają, ta sekcja powinna opisać
zasadę (np. najważniejszy news na górze grupy).

## Czego się nauczyliśmy z selekcji

_(uzupełnia `ucz-sie`: jakie typy newsów Kuba wyrzuca mimo wysokiej oceny, a jakie zostawia
mimo niskiej)_

- #39: z rezerwy wzięte praktyczne teksty inżynierskie o pracy z agentami (code review w Mecie — ocena 6,
  „Czy trzeba czytać kod, czy RAG umarł…” — 7) i osobista refleksja Martina Fowlera (7) → teksty
  praktyków o codziennej pracy z AI oceniać wyżej (7–8), nawet bez „świeżego newsa”.
- #39: odrzucone z TOP: porównanie cen modeli (Simon Willison, ocena 8) — dubluje główny news premierowy
  w tym samym wydaniu; preprint „ScientistTwo” bez niezależnej weryfikacji (7); esej Marka Seemanna (7).
  Porównania/omówienia premiery, która już jest w wydaniu, traktować jak duplikat tematu.
- #39: 27 z 30 rekomendacji TOP zostało w wydaniu.
- #40: z rezerwy wzięte ElevenLabs Eleven v4 (ocena 7) i wycena ElevenLabs (6) oraz lekkie ciekawostki: Claude na Nokii (5), Google Suncatcher (5), felieton o autonomicznych bolidach F1 (5) → ciekawostki o niskiej ocenie wchodzą jako „oddech” (1–3 na wydanie), zwłaszcza jeśli mają trafić do tytułu.
- #40: odrzucone z TOP: podsumowanie DevDay (7) — dubluje osobne wpisy o dots i GPT-6.1 Sol; CNN o agentach OpenAI w USA (7) — dubluje wątek z BBC; Marktechpost o kosztach agentów kodujących (7), Glyph (6), Gemini Gems (6). Zbiorcze podsumowania wydarzeń oceniać niżej, gdy premiery z nich mają osobne wpisy.
- #40: kolejność w grupie „Nowości”: Kuba zamiast alfabetu ułożył najpierw największą premierę (OpenAI dots, GPT-6.1 Sol), potem pary tej samej firmy obok siebie (ElevenLabs ×2, Meta ×3), potem reszta (Marketplace, AMD, Nvidia). Pojedyncza zmiana — przy powtórce zmienić regułę kolejności (najważniejszy news pierwszy, newsy jednej firmy razem).
- #40: 25 z 30 rekomendacji TOP zostało w wydaniu, 5 dobrano z rezerwy.
