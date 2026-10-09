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

## 2026-10-01 — wydanie #40 (preselekcja stron)

- preselekcja.md: partnerstwa technologiczne i umowy chmurowe/infrastrukturalne przechodzą z „Bierzemy” do
  „Zwykle może” (na podstawie: 3× „tak” pominięte — OpenAI + Synopsys, DeepSeek + Huawei, Anthropic–Akamai).
- preselekcja.md: Mam Startup dodany do `strony_ogolne` (1 wzięty na 40, 38 pominiętych; wpisy bez słowa o AI
  dostają „nie”); wiersz w tabeli skuteczności, odświeżone liczby stron.
- preselekcja.md: 7 nowych przykładów decyzji (m.in. „duplikat” dla ElevenLabs wyceny okazał się błędny — wzięty;
  Sonnet 5.5 i Astra „tak” pominięte). 309 ocenionych wpisów (13 tak, 95 może, 201 nie; wzięto 9: 6 tak, 2 może, 1 nie).

## 2026-10-01 — wydanie #39 (poprawki w Substacku)

- tagi.md, opisy.md: przykład — Kuba zamienił tag „Za paywallem” na dopisek „[Za paywallem]” na końcu opisu
  (1× WSJ, AI Force); bez zmiany reguł do czasu powtórzenia.

## 2026-10-01 — wydanie #40

- opisy.md: (1) opis nie powtarza tytułu — pierwsze zdanie zaczyna od szczegółów (7× wycięte otwarcie w #40);
  (2) ostatnie zdanie domyślnie bez komentarza „dlaczego to ważne” — to zmiana poprzedniej reguły z #39
  (8× wycięte w #40, 3× w #39); (3) bez uwag o procesie powstawania opisu; fraza „Opis powstał na podstawie”
  dopisana do listy „Nie używać”; przykłady zamykających zdań zastąpione zasadą „kończ na konkrecie”.
- tytuly.md, wstep.md, seo.md: przykłady z #40 — własny tytuł z lekką ciekawostką (Nokia) zamiast incydentu,
  wstęp spinający tytuł, spójność SEO z wybranym tytułem (po 1×, bez zmiany reguł).
- priorytety.md: nauka z selekcji #40 — ciekawostki z rezerwy jako „oddech”, zbiorcze podsumowania wydarzeń niżej,
  pierwsza obserwacja zmiany kolejności w „Nowościach”.

## 2026-10-08 — przegląd stron (wydanie #41)

- preselekcja.md: Future Tools News nigdy „tak” — premiery i stanowiska z agregatora to „może”
  (na podstawie: 3× „tak” pominięte — GPT-6 duplikat openai.com, Runway Praxis-1, Team Human; 4× „może” wzięte);
  tabela „Skuteczność stron” odświeżona; 5 nowych przykładów decyzji, 5 najstarszych usuniętych.
  Z 317 wpisów Kuba wziął 9. Reguły automatyczne bez zmian: żaden wpis odrzucony regułą nie został wzięty,
  ale też żaden wzorzec nie osiągnął progu 5 pominięć.

## 2026-10-08 — wydanie #40 (poprawki z Substacka)

- Bez zmian w regułach: 2 wpisy (Opis + Czas wideo o Project Suncatcher) to tylko przeniesienie „[2 min]” do treści opisu w Substacku, bez zmiany tekstu — format, nie styl.

## 2026-10-08 — wydanie #41

- opisy.md: (1) docelowa długość skrócona do ~600 znaków (3–4 zdania) — 19 opisów skróconych średnio z ~714 do ~589;
  (2) nowa reguła: bez zdań o wiarygodności źródła („bez niezależnej weryfikacji”, „typowo marketingowy”,
  „estymacja” — 3× Nolla Derm, Bloomberry, TikTok), trzy frazy dopisane do „Nie używać”; (3) nowa reguła: bez dopisków
  o dostępności, instalacji, cenniku i zespole (≥8 newsów: Claude w Workspace, Gemini 4 Argon, Haiku 5.5, Ghost,
  GPT-6, Beam, TikTok, walka z robotami); (4) paywall: nie komentować też tego, co widać/czego nie widać w tekście
  (2× w #41, 1× w #39); 2 nowe przykłady.
- tytuly.md: (1) tytuły badań i raportów bez prefiksu „Badanie:”/„Raport X:” (2× w #41 — zmiana wzorca z tabeli);
  (2) nazwisko autora w tytule tylko dla szefów czołowych firm — zdjęte „Hunter Rice:” i „Acemoglu:” (zaostrzenie reguły);
  (3) tytuł wydania: Kuba w #40 i #41 sam składa tytuł z ciekawostką/produktem „z efektem wow”, więc jedna z trzech
  propozycji ma być ciekawostkowa, a pytajnik jest dozwolony przy niepotwierdzonej obietnicy; 4 nowe przykłady.
- tagi.md: 2 przykłady (EmbeddingGemma 2 → Nowości; Nolla Derm → bez tagu), po 1×, bez zmiany reguł.
- priorytety.md: nauka z selekcji #41 — ciekawostki i produkty konsumenckie z rezerwy (oceny 3–5) wchodzą drugi raz
  z rzędu; komunikaty korporacyjne/regulacyjne (ads, watermarking, SynthID) odrzucane z TOP; 24/30 TOP zostało.
- wstep.md: przykład — wstęp pod własny tytuł z konkretem przy każdym temacie i żartobliwym zakończeniem.
- Bez zmian w seo.md (opis SEO przepisany pod wybrany tytuł, reguła spójności z tytułem już obowiązuje) i w regułach
  kolejności (przesunięcie EmbeddingGemma 2 na koniec grupy wynikało ze zmiany tagu).
