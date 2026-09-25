# Plan: uproszczenie procesu PrzeglądAI

**Założenia:**
- Całość działa w Claude Code, Antigravity znika.
- Domena `przegladai.news` zostaje i przekierowuje na Substacka tak jak teraz.
- Na Substacka wrzucasz i planujesz ręcznie. Repo kończy pracę na gotowych plikach, potem odpalasz finalizację.
- **Repo uczy się samo na Twoich poprawkach, na każdym etapie.**

---

## Zasada naczelna: samorozwój repo

Każda poprawka czegoś, co wygenerował AI, zostaje zapisana i wpływa na kolejne wydania, bez pytania o zgodę.

### 1. Dziennik poprawek

Plik `redakcja/dziennik/poprawki.jsonl`. Wpisy tylko przybywają, nic nie jest kasowane ani nadpisywane. Każdy wpis zawiera:
- datę i numer wydania,
- etap i pole,
- wersję AI i wersję Kuby,
- link albo kontekst.

Rejestrowane są:

| Etap | Co trafia do dziennika |
|---|---|
| Selekcja w admince | Zmiany tytułów, opisów, tagów i czasu. Usunięte newsy wraz z oceną i sekcją, jaką dał im AI. Dodane albo przywrócone pozycje. |
| Wybór tytułu wydania | Która propozycja wybrana, czy wpisany własny tytuł i jak różni się od propozycji. |
| Wstęp (między „Cześć!” a „Zapraszam do lektury!”) | Wersja AI i wersja Kuby. |
| Opis SEO i slug | Wersja AI i wersja Kuby. |
| Napis na okładce | Jeśli został zmieniony. |
| Po publikacji | Na starcie kolejnego `/zbierz-dane` Claude pobiera opublikowany post z publicznej strony Substacka i porównuje go z wygenerowanym plikiem. Dzięki temu łapie też poprawki zrobione już w edytorze Substacka. |

### 2. Automatyczne uczenie się

Skill `ucz-sie` uruchamia się sam na końcu `/zakoncz-wydanie` i obejmuje każdy wpis w dzienniku, którego jeszcze nie przetworzył:
- **Uogólnia poprawki w reguły.** Aktualizuje `redakcja/*.md` (tytuły, opisy, tagi, priorytety, wstęp, SEO) i dopisuje prawdziwe pary przykładów „AI napisał → Kuba poprawił”.
- **Poprawia walidator:** nowe zakazane frazy i reguły tagów.
- **Koryguje ocenę newsów** na podstawie tego, co jest wyrzucane, a co zostaje: jakie typy treści, źródła i tematy.
- **Zapisuje każdą zmianę reguł** w `redakcja/zmiany-regul.md` (też tylko dopisywany), z informacją, która poprawka ją spowodowała.
- **Wprowadza zmiany bez pytania.** Trafiają do tego samego PR-a co wydanie, więc są widoczne w diffie i można je cofnąć w gicie. Jednorazowa poprawka staje się przykładem, a dopiero powtarzający się wzorzec staje się regułą. Przy konflikcie reguł wygrywa nowsza, a stara zostaje odnotowana.

### 3. Uwagi techniczne

Plik `redakcja/zrodla.md`. Domeny, które wymagają przeglądarki, stale paywallowe serwisy, trackery do rozwijania: Claude dopisuje je sam przy pracy, żeby następnym razem nie tracić czasu.

---

## Krok 1: porządki w repo

**Usuwam:**
- `.agents/`, `.antigravitycli/`, `generate_articles_metadata_prompt.md` i komendy `.claude/commands/*.toml` (format Gemini/Antigravity),
- skill `social-media-generator`, `public/posts/` i `private/`,
- stare skille `prepare-articles-for-selection`, `prepare-issue-on-articles` i `run-article-selection` (zastąpią je nowe),
- React i Vite: `components/`, `App.tsx`, `index.tsx`, `constants.ts`, `types.ts`, `generate-paths.js`, `package.json`, `vite.config.ts`, `tsconfig.json`, `metadata.json`,
- `public/issues/*.html`, `llms.txt`, `sitemap.xml` i `migration_to_substack.html`.

**Przekierowanie:** dwa statyczne pliki `index.html` i `404.html` przekierowują `/` i `/<slug>` na `przegladai.substack.com` i `/p/<slug>` jak dotąd. Upraszczam workflow `pages-deploy`, bo nie ma już builda. `CNAME` zostaje.

**Zostają:** `humanizer-pl` (jego wzorce wejdą do `redakcja/opisy.md`) i `youtube-watcher` (do treści i długości filmów).

**Archiwum:** istniejące wydania przenoszę do `wydania/NNN/` (`substack.html` i `okladka.jpeg`).

**Nowe pliki:** `CLAUDE.md` z opisem cotygodniowego procesu i struktury repo.

**Stash:** biorę z niego sprawdzone elementy: generator okładki z szablonem i fontem, obsługę Gmaila przez `gws`, czyszczenie URL-i i indeks opublikowanych linków. Resztę odrzucam.

Docelowa struktura:
```
redakcja/        reguły: tytuly, opisy, tagi, priorytety, wstep, seo, zrodla + dziennik/ + zmiany-regul.md
wydania/NNN/     substack.html, okladka.jpeg, dane.csv (finalna selekcja), meta.json
narzedzia/       skrypty: czyszczenie, walidacja, adminka, generator, okładka, diff do dziennika
strona/          statyczne przekierowanie
.claude/skills/  zbierz-dane, przygotuj-wydanie, zakoncz-wydanie, ucz-sie, porzadki-newsletterow, humanizer-pl, youtube-watcher
```

## Krok 2: reguły redakcyjne z wydań #29–#38

Analiza 10 ostatnich wydań i spisanie `redakcja/*.md`:

- **Tytuły newsów:** długość, struktura, tłumaczenie nazw, kiedy oryginalny tytuł.
- **Opisy:** średnio ok. 850 znaków. Budowa „co się stało” i „dlaczego to ważne”, ton i opinia, zakazane frazy.
- **Tagi i czas:** kiedy który tag, na podstawie realnych rozstrzygnięć. Proporcje w wydaniu: Nowości 7–11, Bliżej technologii 10–14, bez tagu 4–10.
- **Priorytety:** co trafia do TOP 30, po ok. 10 na sekcję.
- **Tytuł wydania:** „Wydanie #N: A, B i C”, czyli trzy konkretne tematy tygodnia.
- **Wstęp:** jeden akapit na 2–4 zdania. Otwiera go główny temat tygodnia, potem 3–5 konkretów i jedna myśl autora. Musi się nadawać zarówno do newslettera, jak i do posta w social mediach.
- **Opis SEO:** 120–160 znaków.

Każdy plik ma sekcję **„Uwagi Kuby”**, gdzie Kuba pisze swoimi słowami, czego oczekuje. Pozostałe sekcje uzupełnia `ucz-sie`. Reguły są pokazywane do akceptacji, zanim zostaną użyte.

## Krok 3: `/zbierz-dane` jako jedna komenda

1. **Czyszczenie (skrypt):** usuwa `utm` i trackery, rozwija przekierowania i usuwa duplikaty. Odrzuca śmieci (np. link do Gmaila) i linki, które już były w poprzednich wydaniach.
2. **Porównanie z opublikowanym poprzednim wydaniem** i zapis różnic do dziennika.
3. **Uzupełnianie opisów:** subagenci (Sonnet) pracują równolegle w paczkach po 10 i stosują `redakcja/*.md`. Najpierw próbują WebFetch, strony oporne obsługuje Chrome, a filmy `youtube-watcher`.
4. **Walidacja (skrypt):** tagi, wykluczanie się tagów, format czasu, długości, zakazane frazy.
5. **Ocena:** kolumny `Sekcja`, `Ocena`, `Uzasadnienie` i `Rekomendacja` (TOP 10 w każdej sekcji albo rezerwa) plus oznaczenie, gdy dwa linki opisują to samo wydarzenie.
6. **Kopia wersji AI** do porównania po selekcji.
7. **Adminka:** uruchamia się i Claude czeka, aż selekcja zostanie zapisana.

## Krok 4: adminka

- Widok w trzech sekcjach z licznikami, np. `Nowości 10/10 · Bliżej technologii 11/10 · Pozostałe 9/10 · razem 30`.
- Pozycje z rekomendacją TOP zaznaczone od razu, rezerwa pod kreską. Ocena i uzasadnienie widoczne przy każdym newsie.
- Tagi jako klikalne chipy ze sprawdzaniem reguł na bieżąco.
- **Druga zakładka „Wydanie”:** tytuł (propozycje do wyboru albo własny), wstęp, opis SEO, slug i napis na okładce. Tu się je poprawia, a każda zmiana trafia do dziennika.
- Przy zapisie: porównanie z wersją AI, wpis do dziennika i od razu generowanie wydania.

## Krok 5: `przygotuj-wydanie`, uruchamiane automatycznie po zapisie

- Po zapisaniu selekcji Claude generuje 2–3 propozycje tytułu, wstęp, opis SEO i slug według reguł i wstawia je do zakładki „Wydanie”.
- Po jej zatwierdzeniu `substack.html` powstaje wprost z CSV. Kolory tagów zostają, a na dole jest blok metadanych (tytuł, opis SEO, slug i data najbliższego piątku).
- Okładka renderuje się z szablonu, bez AI. Font dostrojony do oryginału.
- Wynik trafia do `wydania/NNN/`. Dalej Kuba sam wrzuca wydanie na Substacka i planuje wysyłkę.

## Krok 6: `/zakoncz-wydanie`

- **Pytanie o poprawki na Substacku:** wtedy można porównać wersję opublikowaną z wygenerowaną. Bez odpowiedzi różnice i tak wyłapie następne `/zbierz-dane`.
- **`ucz-sie`:** aktualizuje reguły i zapisuje zmiany w `zmiany-regul.md`.
- **Sprzątanie:** zamyka serwer i usuwa robocze CSV.
- **Git:** branch `issue-N`, commit wydania razem ze zmianami reguł, push i PR z `/schedule` na piątek.

## Krok 7: rezygnacja ze zbędnych newsletterów (`porzadki-newsletterow`)

1. Indeks newsów z ostatnich 10 wydań wraz z oryginalnymi tytułami stron.
2. Około 2000 maili z etykiety Newsletter przez `gws`.
3. Dopasowanie trójstopniowe: taki sam URL, potem podobieństwo tekstu, a przekierowania rozwijane dopiero dla kandydatów.
4. Mały model klasyfikuje tylko nadawców bez trafień.
5. Raport: trafienia, trafienia unikalne i typ nadawcy.
6. Po akceptacji wypisanie przez one-click `List-Unsubscribe`, a w razie potrzeby przez maila albo Chrome.

Wynik trafia do `redakcja/zrodla.md`, a raport można powtarzać np. co miesiąc.

---

## Docelowy tydzień

1. **Codziennie:** linki trafiają do `data.csv`.
2. **Czwartek:** `/zbierz-dane`, po czym wybór newsów w admince i poprawki tekstu w zakładce „Wydanie”. Wersja na Substacka i okładka generują się same.
3. **Ręcznie:** wrzucenie wydania na Substacka i zaplanowanie wysyłki.
4. **Na koniec:** `/zakoncz-wydanie`. Repo samo uczy się na poprawkach i tworzy PR.

## Kolejność

Kroki 1 → 2 → 3 → 4 → 5 → 6 idą po kolei. Krok 7 jest niezależny i może iść równolegle z krokiem 1.

## Status

- [x] Krok 1: porządki w repo (2026-09-22)
- [x] Krok 2: reguły redakcyjne (2026-09-22) — do przejrzenia przez Kubę
- [x] Krok 3: `/zbierz-dane` (2026-09-22) — do sprawdzenia na pierwszym prawdziwym wydaniu (#39)
- [x] Krok 4: adminka (2026-09-22)
- [x] Krok 5: `przygotuj-wydanie` (2026-09-22)
- [x] Krok 6: `/zakoncz-wydanie` i `ucz-sie` (2026-09-22)
- [ ] Krok 7: porządki w newsletterach — raport gotowy, czeka na akceptację listy do wypisania
