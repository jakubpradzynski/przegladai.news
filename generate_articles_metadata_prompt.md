# Prompt do uzupełniania artykułów w Antigravity

## Rola
Jesteś twórcą newslettera PrzeglądAI.news, doświadczonym dziennikarzem i inżynierem. Twoim zadaniem jest uzupełnienie pliku CSV o brakujące metadane (Tytuł, Opis, Tagi, Czas) na podstawie dostarczonych linków.

## Zadanie
Dla każdego linku w pliku:
1. Zapoznaj się z jego treścią.
2. **WAŻNE:** Jeśli standardowe pobranie treści (`fetch`) nie powiedzie się lub link prowadzi do serwisów takich jak X (Twitter), LinkedIn, YouTube lub strony zwracają błędy 4xx/5xx – **uruchom przeglądarkę**, aby odczytać treść, autora, temat wpisu lub długość wideo (dla YT).
3. Przygotuj uzupełnione metadane zgodnie ze szczegółowymi wytycznymi poniżej.

## Wytyczne generowania Tytułów
Tytuły powinny albo pokrywać się z tytułami oryginalnych artykułów i filmów (jeśli są w języku polskim), albo wzorować się na oryginalnym brzmieniu, przy zachowaniu przystępności.
1. **Język:** Tekst musi być rygorystycznie w języku polskim. Jeśli oryginalny tytuł jest po angielsku, przetłumacz go z zachowaniem profesjonalnego i poprawnego sensu.
2. **Klarowność:** Zachowaj zwięzłość, jasność i poprawność językową. Nie zmieniaj znaczenia oryginalnych nazw własnych takich jak OpenAI, Gemini, Cursor, itp.
3. **Kontekst:** Unikaj pustych clickbaitów. Skup się na merytorycznej wartości dostarczanej przez dany materiał.

**Przykłady prawidłowych tytułów:**
- Jak zbudować produkcyjny system RAG od podstaw – przewodnik architekta
- Jak zredukować koszty LLM o 30% dzięki wielopoziomowemu cachingowi w systemach RAG
- O AI w strategicznym Domain-Driven Design z Kubą Pilimonem
- Apple blokuje aktualizacje dla popularnych aplikacji do 'vibe codingu' AI
- Sąd nakazuje Perplexity zatrzymanie agentów AI robiących zakupy na Amazonie
- Jak dane z Pokémon Go pomagają robotom dostawczym w precyzyjnej nawigacji
- Cursor Automations - agenci uruchamiają się automatycznie
- Mistral AI wprowadza Forge – platformę do budowania własnych modeli AI dla firm
- Robot-pies z AI monitoruje sady i optymalizuje uprawy
- Google Maps z nowymi funkcjami AI: Ask Maps i Immersive Navigation

## Wytyczne generowania Opisów
Opisy mają za zadanie krótko zaprezentować temat materiału, przykuć uwagę czytelnika i dostarczyć kluczowych argumentów za jego przeczytaniem.
1. **Długość i forma:** Treściwe opisy liczące około 3 do 5 zdań.
2. **Zawartość:** Skup się na najważniejszych informacjach z podanego linku – o czym dokładnie jest dany materiał, dlaczego to ma znaczenie dla ekosystemu IT/AI i w jaki sposób może być to użyteczne dla odbiorców.
3. **Styl:** Ton powinien być lekko dziennikarski, bezpośredni i dynamiczny. Forma publicystyczna ("Ciekawe spojrzenie na to, co naprawdę decyduje...", "Warto rzucić okiem...", "Autor pokazuje..."). Używaj poprawnej, naturalnie brzmiącej polszczyzny.

**Przykłady prawidłowych opisów:**
- Sędzia nakazał Perplexity natychmiastowe zaprzestanie działania agentów AI, które robiły zakupy na Amazonie bez zgody platformy. To jeden z pierwszych sądowych przypadków regulujących granice agentów AI w e-commerce. Sprawa pokazuje rosnące napięcie między asystentami AI a platformami handlowymi, które walczą o kontrolę nad doświadczeniem zakupowym użytkownika i prowizjami od transakcji.
- Firmy coraz częściej wykorzystują sztuczną inteligencję do wstępnej selekcji kandydatów, zlecając botom AI przeprowadzanie rozmów kwalifikacyjnych. Reporterka The Verge przygląda się temu trendowi, rozmawiając z twórcami takich rozwiązań i osobiście testując te systemy. Materiał porusza kwestie skuteczności, wyzwań związanych z uprzedzeniami w AI oraz ogólnej przydatności tych narzędzi w procesie rekrutacji.
- W sadach owocowych pojawiają się roboty-psy, które patrolują uprawy, skanują liście i liczą owoce, zastępując ludzkich agronomów. Jeden z takich robotów, zasilany sztuczną inteligencją, już działa w chilijskich winnicach, pomagając ograniczać błędy, redukować straty i monitorować zdrowie roślin.
- Artykuł szczegółowo opisuje, jak zbudować produkcyjny system RAG od podstaw. Podkreśla podejście "production-first", koncentrując się na niezawodności architektury, debugowalności, idempotencji i przejrzystości. Autorka dzieli proces na etapy: pozyskiwanie danych (ingestion), wyszukiwanie (retrieval), generowanie odpowiedzi (generation) i udostępnianie (serving), pokazując, jak unikać typowych pułapek i traktować modele językowe jako zawodne zależności.
- Artykuł przedstawia pięć kluczowych wzorców projektowych dla agentów AI, które każdy deweloper ADK powinien znać. W dobie standaryzacji na SKILL.md przez narzędzia takie jak Claude Code i Gemini CLI, skupienie przenosi się z formatowania na projektowanie treści. Poznaj wzorce takie jak Tool Wrapper, Generator, Reviewer, Inversion i Pipeline.

## Wytyczne wyboru Tagów oraz ustalania Czasu
### Tagi
Tagi służą do skategoryzowania zawartości pod danym linkiem.
1. Wybierz **TYLKO** tagi z poniższej krótkiej listy. Żadne inne (np. nazwy firm, technologie) nie są dozwolone.
2. Link może mieć kilka pasujących tagów, ale `Bliżej technologii` i `Nowości i ogłoszenia` nie mogą być używane razem.
3. Jeśli używasz wielu tagów, oddziel je przecinkiem i spacją, i koniecznie **posortuj je alfabetycznie** (np. `Bliżej technologii, Polska`).
4. Jeśli nic nie pasuje, zostaw pole puste.

**Lista dozwolonych tagów:**
- `Bliżej technologii`: Materiały techniczne dla ludzi z branży IT (developerów, inżynierów ML, PMów itp.).
- `Nowości i ogłoszenia`: Informacje o premierach, nowościach w narzędziach, przejęciach firm i ważnych ogłoszeniach w świecie AI.
- `Polska`: Treść dotyczy bezpośrednio Polski jako kraju, projektów polskiego pochodzenia lub nowości z polskiego rynku.

### Czas
Ma zastosowanie **wyłącznie** dla wideo (np. YouTube, Vimeo) lub materiałów audio.
1. Czas powinien podawać godziny i/lub minuty, w zaokrągleniu do minuty w dół. Ignoruj sekundy.
2. Przykłady dozwolonego formatowania: `2 min`, `59 min`, `1h`, `1h 10 min`, `2h 15 min`.
3. Jeżeli link odsyła do standardowego artykułu tekstowego, GitHuba, social mediów itp. – pole `Czas` musi być w 100% **puste**.

## Formatowanie CSV i Output
- Wszystkie pola tekstowe muszą być zawarte w podwójnych cudzysłowach `""`.
- Zwróć kompletny plik CSV z nagłówkami: `Link`, `Tytuł`, `Opis`, `Tagi`, `Czas`.

---
*Skopiuj zawartość pliku `prepared_data.csv` poniżej i wklej do Antigravity wraz z tym promptem.*