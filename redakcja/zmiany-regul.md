# Zmiany reguł

Dziennik zmian w plikach `redakcja/*.md`. Tylko dopisujemy, najnowsze na dole.
Każdy wpis: data, wydanie, co się zmieniło, na podstawie jakich poprawek z `dziennik/poprawki.jsonl`.

## 2026-09-22 — reguły startowe

Spisane z analizy wydań #29–#38: tytuły, opisy, tagi, priorytety, wstęp, SEO.
Źródło: finalne treści wydań w `wydania/029`–`wydania/038`.

## 2026-09-24 — przegląd stron przed wydaniem #39

- seo.md: dodano przykład poprawki opis_seo z #37 (Kuba zastąpił zwięzły opis SEO osobistym wstępem)
  — pojedynczy przypadek, bez zmiany reguły (na podstawie: 1× zmiana opis_seo w dzienniku).
- preselekcja.md: doprecyzowano, że premiery modeli relacjonowane przez agregator (The Decoder) to
  „może”, nie „tak”, nawet dla czołowych labów — AI błędnie dało „tak” 8 razy, Kuba wziął tylko newsy
  biznesowe (Amazon vs Muse, Anthropic IPO) spośród nich (na podstawie: 6× premiera modelu z The
  Decoder pominięta w #39).
- preselekcja.md: zawężono „tekst inżynierski z uniwersalną lekcją” (GitHub Blog, JetBrains) — nie
  liczy się do tego opis własnego rewrite/case study ani developer diary bez przenośnej lekcji
  (na podstawie: 2× GitHub Blog + 1× JetBrains pominięte mimo „tak” w #39).
- preselekcja.md: nowa funkcja SDK bez premiery modelu (Google for Developers/Antigravity) to „może”
  (na podstawie: 1× pominięty w #39).
- preselekcja.md: zaktualizowano tabelę skuteczności stron i przykłady decyzji Kuby na podstawie
  302 ocenionych wpisów z przeglądu stron przed #39 (16 tak, 47 może, 239 nie; wzięto 6).

## 2026-09-24 — wydanie #39

- tytuly.md: nazwisko autora w tytule tylko dla powszechnie znanych osób (na podstawie: 3× Kuba usunął
  „<Autor>: …” — James Shore, Orestis Ioannou, Paul Iusztin); przykład wyboru tytułu wydania.
- opisy.md: ostatnie zdanie ma być opinią o sprawie, nie recenzją artykułu (na podstawie: 3× usunięte
  zamknięcia typu „Konkretne, klarowne rozprawienie się…”); bez względnego czasu, bez komentowania
  paywalla, bez zastrzeżeń i pobocznych szczegółów, „agentów” zamiast „agenty” (po 1× — jako przykłady).
- priorytety.md: praktyczne teksty inżynierskie o pracy z agentami wyżej; porównania premiery, która
  już jest w wydaniu, jak duplikat (na podstawie: 3× wybrane z rezerwy, 3× odrzucone z TOP).
- wstep.md: przykład — bez szablonowego otwarcia „Ten tydzień to…” (1×).
