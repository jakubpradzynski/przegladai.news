# Opisy newsów

## Uwagi Kuby

_(miejsce na Twoje uwagi — AI tej sekcji nie zmienia)_

## Długość i budowa

- Jeden akapit, 3–5 zdań, zwykle 600–1000 znaków (średnio ok. 850 w wydaniach #29–#38).
  Krótkie newsy mogą mieć ~450, długie teksty techniczne do ~1100.
- **Zdanie 1–2: co konkretnie.** Kto, co zrobił, z jakimi liczbami. Pierwsze zdanie od razu
  przechodzi do rzeczy — podmiotem jest firma albo autor, nie „artykuł”. **Opis nie powtarza tytułu:**
  gdy tytuł już mówi, kto i co zrobił („OpenAI przedstawia dots…”, „AMD przejmuje World Labs…”),
  opis zaczyna od szczegółów — Kuba wyciął takie otwarcie 7× w #40 („Niezwykle wszechstronni, stale
  aktywni agenci…”, „Startup zajmuje się…”, „Katalog liczy ponad 2000…”, „Niewielki gadżet…”).
  - „Mistral AI zamknął rundę Series D na 3 miliardy euro, prowadzoną przez Samsung Electronics, przy wycenie ponad 21 miliardów euro…”
  - „Addy Osmani przekonuje, że rzucanie agentów AI prosto na stary, zaniedbany kod to prosta droga do jeszcze większego długu technicznego.”
- **Zdanie 2–4: szczegóły, które wyróżniają materiał.** Liczby, nazwy, przykład, case study.
  Szczegół zamiast ogólnika: „zespół Bun przepracował 535 tysięcy linii kodu z Zig na Rust w 11 dni”.
- **Ostatnie zdanie: domyślnie kończymy na konkrecie, bez własnego komentarza.** Zdanie „dlaczego to ważne”
  (ocena, wniosek, „to pierwszy przypadek…”, „dla zespołów, które…”) Kuba wycinał w #39 (3×) i w #40
  aż 8× (Muse, Addy Osmani, enzym CRISPR, BBC, JVM Bloggers, felieton o F1…). Dodajemy je tylko wtedy,
  gdy to fakt z materiału (np. porównanie z konkurencją podane w źródle), nie nasza ocena. Nie kończymy
  też recenzją tekstu („Konkretne, klarowne rozprawienie się z…”, „Lekki, polski felieton…”).
  - Dozwolony przykład faktu z materiału na końcu: „…na razie w becie i tylko po angielsku.”

## Ton

- Autor jest inżynierem i managerem, który przeczytał tekst i ma zdanie. Wolno ocenić:
  „robi wrażenie”, „słusznie zaznacza”, „ciekawy, mniej oczywisty wątek”, „nie zostawia złudzeń”.
- Autor tekstu nazwany z imienia i nazwiska, gdy jest znany: „Domen Kožar bierze na warsztat…”,
  „Michael Spencer dokumentuje…”, „Autorzy z Thoughtworks tłumaczą…”.
- Przy wideo i podcastach: kto rozmawia, 2–3 konkretne wątki, dla kogo warto poświęcić czas.
- Bez uwag o tym, jak powstał opis („Opis powstał na podstawie opisu i rozdziałów filmu…”) i o czasie
  trwania demonstracji w odcinku — Kuba wycina to z opisu (#40); takie uwagi idą do pola `Uwagi`.
- Przy tekstach za paywallem nie udawać, że przeczytało się całość — opisywać to, co widać.
  Samego paywalla nie komentujemy w opisie (od tego jest tag `Za paywallem`).
- Bez słów względnego czasu („dziś”, „wczoraj”, „w tym tygodniu”) — wydanie czyta się później.
- Bez zastrzeżeń typu „choć temat pojawiał się już u innych” i bez pobocznych szczegółów (pseudonimy
  autorów, techniczne detale spoza głównej tezy) — skracają opis bez straty.
- „agenci AI” / „agentów” (odmiana osobowa), nie „agenty”.
- Pisownia: półpauza „–” w dopowiedzeniach, polskie cudzysłowy „…”, liczby z przecinkiem dziesiętnym
  („0,1125 centa”), procenty bez spacji („92,5%”).

## Zakazane i nadużywane

Nie używać (walidator je wyłapuje):
- „Warto zauważyć”, „Nie bez znaczenia jest fakt”, „Co więcej,” na początku zdania, „Ponadto,”
- „kamień milowy”, „kolejny krok w kierunku”, „przełomowy”, „rewolucyjny”, „kompleksowy”,
  „ewoluujący krajobraz”, „w dynamicznie zmieniającym się świecie”, „game changer”
- „Opis powstał na podstawie”, „Artykuł omawia”, „Autor omawia kluczowe aspekty”, „W artykule dowiesz się”
- „odgrywa kluczową rolę”, „podkreśla znaczenie”
- pytania retoryczne do czytelnika w stylu „Czy zastanawiałeś się…?”
- listy i pogrubienia w opisie — opis to zwykły akapit

Oszczędnie (max 2 razy na wydanie, nie w sąsiednich newsach):
- „Obowiązkowa lektura dla każdego, kto…”, „Warto rzucić okiem”, „To pokazuje, że…”,
  „Ciekawy sygnał, że…”
- „stanowi” / „reprezentuje” tam, gdzie wystarczy „jest”
- imiesłowy doklejone na końcu zdania („…, podkreślając…”, „…, co czyni…”)
- struktura „nie tylko…, ale także…” i zasada trzech (zawsze dokładnie trzy przymiotniki)

Pełniejsza lista wzorców AI: skill `humanizer-pl`.

## Przykłady wzorcowe (z wydań)

> Domen Kožar bierze na warsztat klasyczne prawo Conwaya – że oprogramowanie odzwierciedla strukturę komunikacyjną organizacji – i pyta, co się z nim dzieje, gdy agent AI staje się pełnoprawnym uczestnikiem tej struktury, interpretując wymagania, pisząc kod i recenzując zmiany. Autor krytycznie patrzy na projekty, które próbują ułożyć AI sztywnymi regułami proceduralnymi – jak wymuszone pliki z instrukcjami w Ghostty czy obowiązkowe potwierdzenia człowieka w Zed – porównując to do uczenia do testu zamiast do zrozumienia. Zamiast tego proponuje mierzenie realnych wyników: czy poprawka faktycznie rozwiązuje problem, czy testy regresyjne to potwierdzają, czy benchmarki uzasadniają usprawnienie. Ciekawy, mniej oczywisty wątek to ryzyko wykluczenia – wysokie wymagania jakościowe, które są tanie dla agenta, mogą stać się barierą wejścia dla ludzkich kontrybutorów w tych samych projektach.

> Anthropic masowo wylogowuje użytkowników i usuwa zapisane metody płatności po wykryciu kampanii, w której złośliwe oprogramowanie typu infostealer kradnie identyfikatory sesji i ciasteczka przeglądarki, omijając w ten sposób nawet uwierzytelnianie dwuskładnikowe. Skradzione sesje pozwalają przestępcom przejąć konto bez znajomości hasła i wyczerpać limity użytkowania ofiary – użytkownik może nie zauważyć niczego niepokojącego przez długi czas. Ciekawym akcentem artykułu jest opisany przypadek użytkownika, który sam padł ofiarą malware'u pobranego wraz z piracką grą, a następnie wykorzystał Claude CLI, by zdiagnozować i usunąć infekcję z własnego komputera.

## Przykłady poprawek (AI → Kuba)

_(uzupełnia `ucz-sie` na podstawie dziennika)_

- #39 Opis („Czy trzeba czytać kod, czy RAG umarł…”): usunięte zamknięcie „Konkretne, klarowne rozprawienie się z trzema modnymi hasłami zamiast kolejnego artykułu-hype'u.” — recenzja tekstu zamiast wniosku.
- #39 Opis (Meta, code review): usunięte „Konkretne wskazówki od kogoś, kto realnie robi code review na dużą skalę, choć sam koncept… pojawiał się już u innych twórców.” — recenzja + zastrzeżenie.
- #39 Opis (ChatGPT i ciasteczko): usunięte „Nieprzyjemne odkrycie dla firmy, która przedstawia się jako…” oraz „działający pod pseudonimem Buchodi”.
- #39 Opis (AI Force): „…ujawnione; WSJ zasłania resztę tekstu paywallem.” → „…ujawnione.” — paywall tylko w tagu.
- #39 Opis (AI Force, po publikacji): do opisu dopisane „[Za paywallem]” zamiast tagu — oznaczenie paywalla na końcu opisu, nie jako zdanie (1×; zob. tagi.md).
- #40 Opis (Muse, Marketplace, Nvidia, Small Business, Charm, ElevenLabs v4, AMD, dots): wycięte pierwsze zdanie powtarzające tytuł („Meta zaprezentowała Muse Charm, niewielki gadżet…” → „Niewielki gadżet…”) — opis zaczyna od szczegółów.
- #40 Opis (Muse, Addy Osmani, enzym CRISPR, BBC): wycięte zamknięcie „To jeden z pierwszych przypadków, w których… i test dla odpowiedzialności firm” — bez komentarza na końcu.
- #40 Opis (film Less Bitter): usunięte „Opis powstał na podstawie opisu i rozdziałów filmu, bo napisów nie udało się pobrać.” — uwagi o procesie nie należą do opisu.
- #40 Opis (JVM Bloggers): usunięte „Demonstracja kodu trwa mniej więcej od 6. do 18. minuty…” oraz zdanie „Dla polskich programistów to praktyczny przykład…” — opis 770 → 570 znaków.
- #39 Opis (GPT-6 Sol i Luna): usunięte „dziś”; (Matt Pocock): „agenty działające” → „agentów działających”.
