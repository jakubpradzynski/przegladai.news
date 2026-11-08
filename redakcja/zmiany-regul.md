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

## 2026-10-15 — przegląd stron przed wydaniem #42

- preselekcja.md: (1) „Zwykle może”: polskie wdrożenia i badania o AI (4 wzięte z „może”: Żabka Jush, Trasti, Politechnika
  Lubelska, badanie o wynikach firm) zostają „może”; (2) nowa pozycja: premiera modelu w Antigravity/Google, gdy ten
  sam model ma już wpis ze źródła pierwotnego — „może”, nie „tak” (1× tak→pominięty, Gemini 4 Argon);
  (3) nowe produkty mniejszych firm z agregatorów (Brand Kit, Odyssey-3, Decisions API) — „może”; (4) Netflix
  LLM-as-a-Judge dopisany do tekstów inżynierskich z przenośną lekcją; tabela skuteczności stron odświeżona;
  5 nowych przykładów decyzji (najstarsze 5 usunięte). Reguły automatyczne bez zmian — żaden wpis „nie” nie został
  wzięty (201 „nie” Kuba zostawił zwiniętych, 3 „tak” wzięte z 4).

## 2026-10-15 — wydanie #42

- opisy.md: (1) rozszerzona reguła zastrzeżeń i pobocznych szczegółów — także zdanie o ograniczeniach badania na końcu,
  poboczne wątki z tego samego newslettera, miejsce publikacji pracy naukowej (na podstawie: Fowler 2× w #39/#42, Pragmatic
  Engineer, sciencesays); (2) zapowiedzi „bez podania terminów” do dopisków o dostępności; (3) nowa reguła: osobny fakt
  doklejony po przecinku rozbijamy na dwa zdania (2×: Gemini w Workspace, Scion); 5 nowych przykładów (najstarsze 5 usunięte).
- tagi.md: (1) premiera modelu/API/produktu omawiana przez agregator lub polski serwis = „Nowości i ogłoszenia”, nawet
  techniczna (2× w #41/#42: EmbeddingGemma 2, Decisions API) — zmiana wcześniejszej reguły; (2) „Polska” nie wystarczy
  samym językiem materiału — zdjęte z Decisions API i badania EY (2×); 3 nowe przykłady.
- priorytety.md: nauka z selekcji #42 (ciekawostki z rezerwy trzeci raz z rzędu, odrzucone Gemini 4 Argon ×2 jako temat z #41,
  21/30 TOP zostało); reguła kolejności — powiązane tematycznie newsy obok siebie (2× #40/#42).
- tytuly.md: Kuba trzeci raz z rzędu sam złożył tytuł (z tematów dwóch propozycji, bez ciekawostki) — propozycje mają mieć
  rozłączne tematy; Getty bez „rozdziału 11” w przykładach.
- wstep.md: przykład — usunięta puenta AI na końcu wstępu.
- Bez zmian w seo.md (opis SEO i okładka przyjęte bez poprawek).

## 2026-10-22 — przegląd stron #43

- preselekcja.md: (1) „Bierzemy”: migawki/wersje poboczne modelu (DeepSeek V4.1-Flash-1017) i przejęcia niszowych firm spoza
  głównego nurtu AI (Orchestra Bio) to „może”, nie „tak” (na podstawie: 2× AI „tak”, Kuba pominął); (2) „Zwykle może”: polskie
  tematy AI — 8 z ok. 21 „może” wziętych (XYZ, Mam Startup, gov.pl, JVM Bloggers), więc zostają „może”, bez awansu na „tak”;
  (3) duplikat z agregatora też „może”, gdy oryginał jest „może” (Future Tools + OpenAI/Google Cloud, wzięty mimo „nie”);
  (4) tabela skuteczności stron odświeżona, 6 nowych przykładów decyzji (najstarsze 6 usunięte). Reguły automatyczne bez zmian
  (jedyne „nie”→wzięty nie pochodziło z reguły automatycznej).

## 2026-10-22 — wydanie #42 (porównanie z Substackiem)

- wstep.md: tylko jeden przykład (apostrof typograficzny „merge’y”; reszta różnicy to artefakt przycisku Substacka). Bez nowych reguł.

## 2026-10-22 — wydanie #43

- opisy.md: nowa reguła — bez zamykających zdań o braku informacji („nie ujawniono”, „nie wskazuje”), oceny tekstu i pobocznych
  wątków trzecich osób (na podstawie: ok. 10 wyciętych zdań w Cyberly, Iowa, Vals, Verna, Amazon memo, CNBC/Musk, Stripe,
  Godin, GitHub); 4 nowe przykłady (4 najstarsze usunięte).
- tagi.md: 2 przykłady — przejęcie polskiego startupu bez premiery = tylko „Polska” (Cyberly); eksperyment z agentami jako
  ciekawostka bez tagu (Vals, 1×).
- priorytety.md: limit „Polska” 1–4 nie obowiązuje, gdy w tygodniu jest 5+ mocnych polskich newsów; nauka z selekcji #43
  (polskie newsy i teksty dla EM z rezerwy, wąsko techniczne analizy i trzeci wpis o IPO odrzucone, 24/30 TOP zostało).
- tytuly.md: czwarty z rzędu własny tytuł Kuby (#40–#43) — przy 4+ polskich newsach jedna propozycja ma być „polska”.
- wstep.md, seo.md: wstęp i SEO przepisane pod „polski” tytuł; reguła: SEO piszemy od nowa pod wybrany tytuł (2× — #40, #43).

## 2026-10-29 — przegląd stron przed wydaniem #44

- preselekcja.md: nowe wpisy w „Zwykle może” — posty inżynierskie o budowie agentów (LangChain 2× wzięte: Loop Engineering, Design Agent),
  wyjaśnienia praktyk z laboratoriów (OpenAI FDE), polskie teksty o AI w programowaniu (JVM Bloggers); The Decoder: stanowiska
  i spekulacje o rundach/wycenach nie są „tak” (4× pominięte), „tak” tylko przy konkretnym dużym fakcie (Meta–Nvidia, emisja akcji Meta, wzięte);
  sprawdzanie duplikatu tematu IPO Anthropic przed „tak” (2× pominięty S-1). „Odrzucamy”: LangChain już nie „0/96” — tylko marketing i case study.
  Tabela skuteczności stron odświeżona; 6 nowych przykładów decyzji (5 najstarszych usunięte). Reguły automatyczne bez zmian
  (żaden wpis odrzucony regułą automatyczną nie został wzięty). (Na podstawie: 9 wziętych z 339 pokazanych; 6× „tak”→pominięty, 2× „nie”→wzięty, 4× „może”→wzięty.)

## 2026-10-29 — wydanie #44

- opisy.md: reguła zamykających zdań wzmocniona (9 wyciętych w #44: ograniczenia modelu, brak ceny akcji, terminy, przyznanie autora, kolejny projekt); nowy przykład (najstarszy usunięty) (na podstawie: Genie 4, S-1, Microsoft, FDE, YC, Latent Space, Verna).
- tytuly.md: 2 przykłady — krótsze tytuły newsów bez doprecyzowań i dopowiedzeń po półpauzie (Netflix, Pocock); piąty z rzędu własny tytuł wydania, tym razem „pieniądze i rynek pracy” bez premier.
- priorytety.md: kolejność w „Nowości” — największa premiera pierwsza i newsy jednej firmy obok siebie (2× #40, #44); nauka z selekcji #44 (25/30 TOP zostało, duplikaty: wybór bogatszej wersji + dopisanie faktów z drugiej).
- seo.md: SEO pisane od nowa pod własny tytuł Kuby (3× — #40, #43, #44).

## 2026-10-31 — nowy styl opisów (po #44)

- opisy.md: przebudowany. Opis pisany z perspektywy czytelnika (inżynier, EM, PM/UX, finanse/biznes): co się stało →
  konkrety z porównaniem → co to znaczy dla czytelnika. Zastępuje regułę „kończymy na konkrecie, bez komentarza”
  z #39–#44 – wycinane były ogólne komentarze i uwagi o braku danych, te zakazy zostają; konsekwencja dla czytelnika
  jest teraz wymagana (na podstawie: uwagi Kuby do opisów z #44).
- opisy.md: gołe wyniki benchmarków wyłącznie jako porównanie (skok, próg, cena na tle konkurencji); ocena skali
  w newsach finansowych; bez szczegółów struktury (klasy akcji); nazwisko autora tylko gdy podnosi wagę (zwykle rola + firma).
- opisy.md: prostszy język, krótkie zdania, bez niejasnych sformułowań z artykułu; anglicyzmy zostają, ale nie kilka
  obok siebie; dozwolone jedno konkretne pytanie do czytelnika (max 2–3 na wydanie); pytanie o polski kontekst przy newsach z USA.
- opisy.md + agent opisywacz: możliwość WebSearch po brakujący kontekst (źródło w `Uwagi`).
- tytuly.md: w tytule firma zamiast nazwiska, gdy autor jest istotny tylko jako przedstawiciel firmy.

## 2026-11-02 — wydanie #44 (posty social, uwagi Kuby w czacie)

- social.md: budowa posta pogłębionego haczyk → wstęp (o artykule, wyjaśnienie pojęć) → rozwinięcie → zakończenie;
  pełne zdania zamiast serii krótkich „statementów”; bez mocnych tez; wnioski dla managerów bez pouczania;
  nowe frazy w „Nie używać”; infografiki w nowych stylach `notatka` / `minimal` (na podstawie: uwagi Kuby do t1, t4,
  w-e6z0d i ogólna uwaga o infografikach „wyglądają AI-owo”)
- social-platformy.md: hashtagi domyślnie brak (było 0–3); walidator ostrzega o hashtagach

## 2026-11-05 — przegląd stron przed wydaniem #45

- preselekcja.md: duplikat agregatora zawsze „może” z podpowiedzią „duplikat: …”, „nie” tylko przy tym samym linku (drugi raz — Future Tools „Images 2.6”, wcześniej Model Garden #43) (na podstawie: nie→wziety 1×).
- preselekcja.md: The Decoder bez dużego ruchu biznesowego czołowej firmy = „nie” (wzięty 1 z 41, 40 „może” pominiętych); inwestycja w firmę spoza czołówki (Aramco–Humain) = „może”, nie „tak” (na podstawie: tak→pominiety 1×, 40× może→pominiety).
- preselekcja.md: OpenAI News poza premierami = „nie” (16/16 „może” pominiętych); The Information domyślnie „nie” (0/144); polskie wdrożenia, inwestycje i incydenty z AI oraz teksty twórców o budowie z AI zostają „może” (na podstawie: 7× może→wziety).
- preselekcja.md: tabela skuteczności stron odświeżona, przykłady decyzji (15 najnowszych).
- social.md: sekcja „Wybór tematów” — wnioski z wyboru tematów w #44 (własny temat z prospektu IPO, 2 z 3 poleconych).

## 2026-11-05 — wydanie #45

- opisy.md: nowa reguła w „Długość i budowa” — zdanie z perspektywą czytelnika zostaje, gdy daje konkretne działanie lub wniosek; puste rady, „to znak, że…” i oceny wydarzenia wycinamy lub kończymy opis na fakcie; 3 nowe przykłady (najstarsze usunięte) (na podstawie: 4× wycięte zakończenia — Reddit, Pierre, Proton, PayU; żargon i poboczne detale w Netflix, ChatGPT search, MIT; nazwisko zamiast „Autor” w Hacker Tube).
- tagi.md: przykład — zestaw narzędzi dla agentów (Product Compass) to „Bliżej technologii”, nie „Nowości” (1×).
- tytuly.md: szósty z rzędu własny tytuł wydania — tym razem „inżynierski” (e2e, HackerTube, Lovable); jedna z propozycji ma być pod wątek inżynierski.
- priorytety.md: obniżenie oceny wąsko technicznych poradników o ewaluacji, RAG i inferencji (3× poza wydaniem: #43, #45); lekkie ciekawostki z oceną 4–5 wchodzą z rezerwy po raz szósty; kolejność „Nowości” — największa premiera pierwsza (4× — #40, #42, #44, #45).
- wstep.md, seo.md: przykłady — wstęp i SEO przygotowane pod własny tytuł przyjęte bez zmian.

## 2026-11-05 — posty social #45 (uwaga Kuby w czacie)

- social.md, social-platformy.md: prompty do zdjęć w formacie 3:4 zamiast 4:5 (Google Flow nie obsługuje 4:5), motyw na środku kadru do przycięcia do 4:5; infografiki ze skryptu zostają w 4:5 (na podstawie: komunikat Flow zgłoszony przez Kubę).

## 2026-11-06 — posty social #45 (uwaga Kuby w czacie)

- social.md: posty pogłębione budowane jako news → opinia: haczyk z faktem (4 typy), źródło i kontekst z nazwami, rozwinięcie, ostrożne stanowisko z ustępstwem, wniosek dla czytelnika, konkretne pytanie na końcu; długość 1000–1700 znaków; zasady tonu (konkrety z nazwy, punktory „–”) i obrazków (zdjęcie człowieka zamiast grafiki, gdy pasuje) (na podstawie: uwaga Kuby w czacie).
- social-platformy.md: LinkedIn — praktyczna długość 1000–1700 znaków.

## 2026-11-08 — posty social #45 (poprawki Kuby w czacie)

- social.md: posty pogłębione dłuższe (1500–2200 znaków, 5–7 akapitów) i bardziej profesjonalne; nie piszemy niezrozumiałych sformułowań bez konkretnego przykładu ze źródła (sprawdzamy w artykule) ani idiomów bez tłumaczenia; post jest tekstem Kuby, więc nie piszemy w treści, kto opisał artykuł (źródło w komentarzu); zamiast etykiety „wniosek dla managerów” — „na czym warto się zastanowić”; pytanie końcowe dotyczy głównej tezy; stanowisko rozważa inne przyczyny; nie tłumaczymy podstaw (tokeny); infografika pokazuje sedno, a nie ciekawostkę ze źródła (na podstawie: uwagi Kuby do t2, t3, t4, t6 — w tym 4× „wniosek/coś wartego uwagi dla menedżerów”, 3× niezrozumiałe sformułowanie z artykułu, 3× odesłanie do autora/redakcji w treści).
- social.md, lista „Nie używać”: „Ważny wniosek dla managerów”, „Coś wartego uwagi dla managerów”, „zamienia narzędzie w mandat”, „Autor przypomina”.

## 2026-11-08 — nauka z postów social #45 (poprawki Kuby w tekstach i uwagi o obrazkach)

- social.md, „Stanowisko Kuby”: zastrzeżenia („pewnie”, „chyba”, „może być lepiej”) tylko przy naprawdę niepewnych tezach; uzasadnione twierdzenia wprost (na podstawie: 3 poprawki w t4 i t3, np. „Teraz może być lepiej…” → „Teraz łatwiej jest…”).
- social.md, krok 5: wniosek dla czytelnika bez żadnej etykiety, także bez „Na czym warto się zastanowić:” (na podstawie: usunięta etykieta w t3).
- social.md, „Ton i język”: nie odmieniamy nazw produktów (OpenClaw), cytaty i idiomy w cudzysłowie, tryb przypuszczający dla skutków hipotetycznych, przecinki przy „po pierwsze, …”, konkret zamiast ogólnika, autoironia z emoji (max 1 na post), formy neutralne płciowo w pytaniach (na podstawie: poprawki w t2, t3, t4, t6 i pytaniu w poście głównym).
- social.md, post główny: końcowe pytanie konkretne, o doświadczenie z narzędziem z wydania (na podstawie: pytanie o e2e zamiast ogólnego pytania o agentów).
- social.md, „Obrazki”: obraz nie musi być realistycznym zdjęciem (minimalistyczne ilustracje, grafiki pod temat), ilustruje konkretną tezę (np. dziewięć kubków = podział pracy), bez garażu, motoryzacji i remontów; nowa opcja `mem` (szablon z imgflip + gotowy tekst) obok infografiki i promptu (na podstawie: uwagi Kuby o zdjęciach w t3, t4, t6).
- social.md, „Wybór tematów”: z 7 propozycji Kuba wziął 4 o organizacji pracy z agentami i kosztach, wyłączył polecany esej o zaufaniu do agentów (t1).
- o-mnie.md: bez nawiązań i obrazów motoryzacyjnych.
- Narzędzia: pole `obrazek.mem` w narzędziu posty social, walidatorze, eksporcie i dzienniku; host `lspace.beehiiv.com` w walidatorze czasu.

## 2026-11-08 — zamknięcie postów social #45 (decyzje Kuby)

- social.md, „Obrazki”: obrazek tylko gdy naprawdę dobry — Kuba odrzucił wszystkie wygenerowane zdjęcia i infografiki z #45, zostawił jeden mem („Gru's Plan” przy prawie Brooksa); proponujemy 1–2 mocne pomysły zamiast kompletu, mem najwyżej raz na tydzień, a gotowy plik mema trafia do `obrazki/<id>_mem.jpg` (na podstawie: 3 posty bez obrazka, 1 mem wybrany).
- social-platformy.md: Kuba publikuje ok. trzech postów tygodniowo i zostawia wybór wariantu; terminy to propozycje.
- Weryfikacja faktów (agent `social-weryfikator`, skill `posty-social`): drugie niezależne źródło dla kluczowych liczb i tez oraz osobna kontrola spójności całego tekstu (podmioty, okresy, parafrazy, opinie vs fakty, zgodność LinkedIn z X) (na podstawie: prośba Kuby o jeszcze dokładniejszą weryfikację).
- narzędzia: eksport `posty.md` z tekstem LinkedIn i komentarzem w blokach kodu (kopiowanie zachowuje puste linie między akapitami); `obrazek.mem.plik` obsługiwany w narzędziu i eksporcie.- social.md, przykłady: definicje pojęć krótko, bez „to program, który…” (na podstawie: poprawka w t4, 1×).

