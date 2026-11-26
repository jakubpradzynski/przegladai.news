# Preselekcja wpisów ze stron

Reguły, według których AI wstępnie ocenia nowe wpisy ze stron (`/przeglad-stron`), zanim Kuba je przejrzy.
Trzy oceny:
- **tak**: prawie na pewno do wydania. W narzędziu jest od razu zaznaczone, Kuba tylko odznacza.
- **może**: nie wiadomo. Kuba decyduje. **Przy wątpliwości zawsze „może”, nigdy „nie”.**
- **nie**: pewne odrzucenie według reguł poniżej. W narzędziu jest zwinięte, można rozwinąć.

„nie” wolno dać tylko wtedy, gdy wpis pasuje do reguły z sekcji „Odrzucamy”, a strona i temat nie mają
w historii przykładów wziętych. Lepiej pokazać Kubie za dużo niż ukryć dobry news.

## Uwagi Kuby

_(miejsce na Twoje uwagi — AI tej sekcji nie zmienia)_

## Bierzemy (zwykle „tak”)

- Premiery i duże aktualizacje modeli czołowych laboratoriów — **tylko ze źródła pierwotnego**
  (blog/Twitter laboratorium): OpenAI, Google/DeepMind, Anthropic, Meta, xAI, Mistral, DeepSeek, Apple.
  **Nie** liczą się do tego kolejne migawki/wersje poboczne istniejącego modelu (DeepSeek „V4.1-Flash-1017” —
  AI „tak”, Kuba pominął #43) — to „może”.
  Przykłady wziętych: „GPT-6 Astra”, „Introducing ChatGPT Images 2.5”, „Gemini 3.8 Live”,
  „Introducing Grok 4.6”. Ta sama premiera relacjonowana przez agregator (The Decoder i podobne)
  to „może”, nawet gdy laboratorium jest czołowe — zob. „Zwykle może” niżej.
- Duże ruchy biznesowe w AI: przejęcia, rundy od ~100 mln $, zmiany kierownictwa w czołowych firmach,
  zerwane partnerstwa („Our decision on Cursor following its acquisition by SpaceX”, „Lovable raised $400M”),
  starcia konkurencyjne dużych graczy („Amazon blocks Meta's AI agent Muse from online shopping”),
  wieści o IPO czołowych labów („Anthropic is also reportedly postponing its IPO”) — także gdy
  relacjonuje je agregator, bo to news biznesowy, nie premiera produktu. Przejęcie niszowej firmy spoza
  głównego nurtu AI (OpenAI + Orchestra Bio, biofarma — AI „tak”, Kuba pominął #43) to „może”. **Nie** liczą się do tego
  partnerstwa technologiczne i umowy infrastrukturalne (OpenAI + Synopsys, DeepSeek + Huawei,
  Anthropic–Akamai $11,6 mld — wszystkie pominięte #40) — to „może”.
- Stanowiska i eseje liderów branży, które wywołują dyskusję (Amodei o tempie rozwoju AI,
  „Pacing model development…”, „An Alien Mind”).
- Teksty inżynierskie z uniwersalną, przenośną lekcją o pracy z AI i agentami (metodyka, ewaluacja),
  od znanych autorów i dużych zespołów inżynierskich (Netflix „The Lifecycle of LLM-as-a-Judge” — wzięty #42): Addy Osmani (8/10 wpisów trafiło do wydań), Martin Fowler (artykuły, nie
  „Fragments”), GitHub Blog o ewaluacji i code review z AI („How to evaluate LLMs before production”).
  **Nie** liczy się do tego opis własnego wdrożenia/rewrite u vendora bez przenośnej lekcji
  (np. GitHub Blog „Rendering huge pull requests in the Copilot app”, „Migrating the GitHub Copilot
  runtime to Rust” — Kuba pominął oba #39) ani developer diary o budowie własnego narzędzia
  (JetBrains „Building a RAG Pipeline… Developer Diary” — pominięty #39) — to „może”, patrz niżej.
- Nowe kategorie produktów AI albo coś, co przebiło się do mediów (Tavus Phoenix, TypeSafe Jev).

## Zwykle „może”

- Relacje agregatorów (The Decoder, Future Tools, AIOAI.pl, LLM Stats) o premierach modeli — **także
  premierach czołowych laboratoriów**, nie tylko mniejszych graczy. W #39 Kuba pominął 6 z 8 takich
  wpisów The Decoder ocenionych błędnie na „tak” (Google Flash TTS, Xiaomi MiMo, xAI Grok 4.7,
  Alibaba Qwen-Image, Tencent Gander, Qwen3.8-Omni-Flash) — wziął tylko dwa newsy biznesowe
  (Amazon vs Muse, Anthropic IPO), nie premiery modeli. Temat bywa dobry, ale do wydania trafia źródło
  pierwotne. Gdy w tej samej partii jest wpis ze źródła pierwotnego, ocena agregatora = „nie”
  z powodem „duplikat: <tytuł źródła>”. Uwaga: w #43 Kuba wziął wpis Future Tools „OpenAI Brings Frontier Models and Codex
  to Google Cloud's Model Garden” oceniony „nie” jako duplikat openai.com — gdy źródło pierwotne jest tylko „może”
  (partnerstwo dystrybucyjne), duplikat z agregatora też dawaj jako „może”, nie „nie”. **Drugi raz w #45:** Kuba wziął
  Future Tools „OpenAI Launches Images 2.6 With GIF Support, 50% Faster Generation…” (AI: „nie”, duplikat), choć wziął też
  oryginał z openai.com — agregator dopisuje szczegóły (GIF, szybkość, API). Dlatego **duplikat agregatora zawsze „może”,
  z podpowiedzią „duplikat: <tytuł>”**; „nie” tylko przy tym samym linku albo gdy wpis niczego nie dodaje.
- **Future Tools News: nigdy „tak”.** W #41 Kuba pominął wszystkie 3 wpisy ocenione tu na „tak” (GPT-6 — ten sam
  news miał już z openai.com w `data.csv`; Runway Praxis-1; Team Human) i wziął 4 z „może” (plugin ChatGPT do notatek,
  EmbeddingGemma 2, raport a16z, ogłoszenie Trumpa). Premiery i stanowiska relacjonowane przez ten agregator
  to „może”; „tak” tylko gdy brak źródła pierwotnego w partii i `data.csv`. W #47 Kuba wziął tylko 2 z 46 „może” (Gemini 4 Neon, GPT-6.2 Astra and Sol — duplikaty premier
  czołowych modeli, oryginał GPT-6.2 też wziął) i pominął 44. **Duplikat Future Tools = „może” tylko dla premiery modelu czołowego laboratorium albo ruchu
  Big Techu; pozostałe wpisy (drobne launche, wtyczki, benchmarki, ciekawostki) = „nie”, z powodem „agregator, drobne”.** W #48 Kuba wziął 2 z 16 „może”: przejście Thariqa z Anthropic do OpenAI i premierę Claude Ship (produkt czołowego labu) — przejścia kluczowych osób między czołowymi labami i premiery produktów czołowych labów (nie tylko modeli) zostają „może”.
- Partnerstwa technologiczne, umowy chmurowe/infrastrukturalne i narzędzia open source firm
  (The Decoder: OpenAI + Synopsys, DeepSeek + Huawei, Anthropic–Akamai — pominięte #40, mimo wysokiej kwoty).
- Ogłoszenia inicjatyw badawczych/biznesowych bez konkretnego produktu („Anthropic is setting up
  a biology lab…” — pominięty #39) i pojedyncze głośne incydenty relacjonowane przez agregator
  („U.S. military nearly boarded a Chinese ship over a hallucinated AI report” — pominięty #39,
  mimo dużego newsa: prawdopodobnie zbyt pośrednie źródło).
- Nowa funkcja SDK/narzędzia deweloperskiego bez własnej premiery modelu (Google for Developers
  „Introducing Support for Local AI Models in the Antigravity SDK” — pominięty #39, mimo że to
  Antigravity: sama integracja lokalnych modeli to za mało na „tak”).
- Polskie tematy o AI: prawo, administracja, polskie firmy (gov.pl, AIOAI.pl, Nowy Marketing, XYZ).
  Tylko gdy dotyczą AI; sama cyfryzacja czy cyberbezpieczeństwo bez AI to „nie”. W #42 Kuba wziął 4 takie
  wpisy z „może” (Żabka Jush, Trasti + ElevenLabs, Politechnika Lubelska, badanie o wynikach firm z AI) —
  polskie wdrożenia i badania o wpływie AI na firmy zostają „może”, nie „nie”. W #43 Kuba wziął z „może” 8 polskich
  wpisów (XYZ: Wordware/Sauna, AI w dużych polskich firmach, Google–Finlandia vs Polska, Cyberly; Mam Startup: Sauna,
  PKO „Genia”; gov.pl: PLLuM w sądzie; JVM Bloggers: rozpoznawanie LLM-ów), ale pominął ok. 13 innych — wciąż „może”,
  nie „tak”. Wpis o tym samym zdarzeniu z kilku polskich źródeł też zostaje „może” (Kuba bierze jedno z nich).
- Premiera modelu w Antigravity/Google, gdy ten sam model ma już wpis ze źródła pierwotnego w partii
  albo w wydaniu (Antigravity „Gemini 4 Argon in Google Antigravity” — AI „tak”, Kuba pominął w #42).
- Badania i raporty z danymi (Anthropic Economic Index, raporty o rynku pracy).
- Ogłoszenia narzędzi developerskich AI (Cursor, JetBrains AI, Antigravity), gdy to nowa funkcja,
  a nie poprawka.
- Nowe produkty i modele mniejszych firm, nawet z agregatora lub bez opisu (ElevenLabs „Brand Kit”,
  Odyssey-3 w The Decoder, Decisions API w AIOAI.pl, nowa funkcja YouTube w Future Tools) — w #42 Kuba
  wziął po jednym z „może”; zostają „może”.

- OpenAI News poza dużymi premierami i ruchami biznesowymi: w #45 Kuba pominął 16 z 16 wpisów ocenionych „może” (case study
  klientów, wewnętrzny security sprint, Model Spec, lobbing, granty), wziął tylko Images 2.6 („tak”). Case study klienta,
  bezpieczeństwo/programy wewnętrzne i polityka bez nowego produktu = „nie” (w #47 znów 0 z 11 „może” wziętych, w #48 0 z 3 „może” i 0 z 13 „nie” — razem 0 z 30 w trzech przeglądach — wpisy
  poza premierą modelu/produktu i dużym ruchem biznesowym dawaj „nie”); „może” tylko gdy to wyjaśnienie praktyki
  albo stanowisko lidera (jak „What FDE means at OpenAI”).
- Polskie źródła (Mam Startup, Nowy Marketing): w #45 Kuba wziął 4 z 14 „może” — mObywatel z AI, PayU + Visa (agenci AI
  w zakupach), inwestycja Wonderful 200 mln PLN, wyrok za wyłudzanie tantiem przez muzykę z AI. Konkretne polskie wdrożenia,
  inwestycje i incydenty z AI zostają „może”; Mam Startup bez słowa o AI nadal „nie” (52 „nie” bez wziętych).
- Polskie źródła w #46: Kuba wziął 7 z „może” — gov.pl „Polska i Korea Południowa… AI” (i ten sam news z Mam Startup),
  Mam Startup: RTV Euro AGD + Gemini, Canva zwalnia przez koszty AI; Nowy Marketing: spór o AI w reklamie Diora;
  XYZ: Bielik 56 języków. Utwierdza to regułę „polskie wdrożenia, polityka i głośne incydenty z AI = może”.
  Gdy ten sam news jest w gov.pl i Mam Startup, oba zostają „może” (Kuba wziął oba). W #47 z Mam Startup wziął 2 z 8 „może”: Nvidia z prognozami po odejściu
  Huanga i Apple z aplikacją badawczą AI w zdrowiu (duplikat agregatora) — wątki z dużych newsów, o których pisze też świat, zostają „może”; XYZ: LATO 4,7 mln $ (wzięty). W #48 z Mam Startup wziął 2 z 8 „może”: raport o kosztach środowiskowych AI (woda) i scoring kredytowy AI w Krakowskim Banku Spółdzielczym — raporty o wpływie AI i pierwsze wdrożenia AI w polskich instytucjach finansowych zostają „może”; 6 pozostałych pominął, a 42 „nie” (bez AI) — żaden wzięty.
- Narzędzia agentowe dużych vendorów w wersji GA i ogólne lekcje o ewaluacji (JetBrains „IDEs Transformed for the Agentic
  Era – With Air”, LangChain „What Is Eval-Driven Development?” — AI „może”, Kuba wziął #46) zostają „może”; reszta wpisów
  JetBrains i LangChain (9–10 „nie” na stronę) nadal „nie”.
- Wpisy autorów/CEO o budowie produktu z AI (Lovable „How we built Lovable…”, Karpathy HackerTube z Claude — wzięte #45, AI: „może”)
  zostają „może”, nie „nie”.
- Teksty inżynierskie o budowie agentów od dużych zespołów, nawet z bloga vendora (LangChain „The Art of Loop Engineering”,
  „How We Built Our Design Agent” — AI „może”/„nie”, Kuba wziął oba #44) i wyjaśnienia roli/praktyki z laboratorium
  (OpenAI „What FDE means at OpenAI”). Case study klienta nadal „nie”; własny agent/harness z lekcją — „może”.
- Incydenty bezpieczeństwa i głośne wydarzenia w czołowych narzędziach AI (Cursor „An update on our recent security incident” — AI: może, Kuba wziął #47)
  zostają „może”; Cursor poza premierami i incydentami nadal „nie”.
- Polskie teksty o pracy z AI w programowaniu (JVM Bloggers „AI w SDLC: Model nie ma znaczenia” — wzięty #44, 1 z 8 „może”). W #47 Kuba wziął 2 z 2 „może” z JVM Bloggers o pracy z agentami
  (Claude Code Review ze specjalistycznymi agentami, Harness Model v2): praktyczne teksty o agentach w programowaniu to „może”, przy dalszych trafieniach — „tak”;
  reszta JVM Bloggers (Java bez AI, osobiste) nadal „nie”.
- Decoder i inne agregatory — stanowiska i spekulacje o rundach/wycenach (Jack Clark o 2027, Altman o alignmencie,
  OpenAI obniża wycenę, OpenAI podbiera klientów Anthropic — wszystkie AI „tak”, Kuba pominął #44): to „może”.
  „Tak” dla agregatora tylko przy konkretnym, dużym fakcie biznesowym czołowego laboratorium albo Big Techu
  (Meta–Nvidia 3 mld $, emisja akcji Meta 95 mld $ — wzięte #44). Inwestycja w firmę spoza czołówki
  (Saudi Aramco 49% Humain, 2,6 mld $ — AI „tak”, Kuba pominął #45) to „może”. W #45 z 41 wpisów The Decoder Kuba wziął 1
  (przejęcie Pierre przez OpenAI, AI: „może”) i pominął 40 „może”: W #46 powtórka: z 33 wpisów The Decoder ocenionych „może” Kuba wziął 0. **The Decoder bez dużego ruchu biznesowego czołowej firmy
  (badania, nowe modele i funkcje mniejszych firm, drobne zmiany cen i limitów) = „nie”**, z powodem „agregator, drobne”.
  Przejęcia przez OpenAI/Anthropic/Google/Meta zostają „może”. **W #47 trzeci przegląd z rzędu: 0 z 33 „może” wziętych, w #48 czwarty: 0 z 15 „może” (i 0 z 35 „nie”) — ruchy kadrowe, stanowiska i głośne wątki (Riemann) też „nie”** — także duplikaty
  premier, które Decoder relacjonuje po źródle pierwotnym: dla Decodera duplikat = „nie” („agregator, duplikat”), wyjątek reguły o duplikatach agregatora dotyczy tylko Future Tools.
- Przed „tak” dla newsa o IPO Anthropic sprawdź, czy temat jest już w partii/`data.csv` z innego źródła
  (S-1 z anthropic.com i Future Tools — AI „tak”, Kuba pominął #44): drugi i kolejny wpis o tym samym to „nie” (duplikat).

## Odrzucamy (zwykle „nie”)

- Drobne aktualizacje funkcji i wydania wersji: Google Workspace Updates (0/19), wydania IDE i bibliotek
  („IntelliJ IDEA 2026.2.3 Is Out!”, „Ktor 3.6.0”, bug-fix releases), „now available on Android”.
- Case study klientów vendora: „How Grab put Cursor…”, „Toyota Scales Enterprise AI with Deep Agents”,
  „NTT DATA cuts incident analysis with Codex”.
- Poradniki dla początkujących i materiały produktowe vendora: „GitHub Copilot app for Beginners”,
  „MCP 101”, „Using skills with Deep Agents”, „Enterprise features July roundup”.
- Sprawy wewnętrzne firm: raporty dostępności, awarie, programy partnerskie, harmonogramy konferencji,
  granty regionalne („Supporting Thailand’s next generation of AI startups”).
- Komentarze giełdowe i finansowe bez nowej informacji o AI (CNBC: „Cisco stock sinks…”, wywiady
  z analitykami w „Closing Bell”).
- The Information: 0 z 165 wziętych (20 nowych w każdym z 5 ostatnich przeglądów, „może” w #45 i #48 — wszystkie pominięte).
  Domyślnie „nie”; „może” tylko przy wyjątkowym temacie AI o czołowym laboratorium, bez duplikatu w innym źródle.
- Wpisy osobiste i przeglądy linków autorów („Fragments: …”, „Social Media Engagement”).
- Treści spoza AI (ICEYE: satelity, JVM Bloggers: Java bez AI, Datadog bez AI).
- Marketing platform agentowych bez ogólnej lekcji (Stack Overflow Blog: 0/71). LangChain: marketing i case study
  klientów — „nie”, ale posty inżynierskie o budowie agentów — „może” (zob. niżej).

## Reguły automatyczne (bez AI)

Stosowane w kodzie przed oceną AI (`narzedzia/strony/preselekcja.py`), więc są natychmiastowe.
`strony_ogolne` — strony, na których nie wszystko dotyczy AI: wpis bez słowa związanego z AI
w tytule i opisie dostaje „nie”. `wzorce_nie` — wyrażenia regularne (bez rozróżniania wielkości liter)
dla tytułów, które zawsze odrzucamy. Tę sekcję aktualizuje też `ucz-sie` — tylko dla wzorców
potwierdzonych wieloma decyzjami Kuby.

```json
{
  "strony_ogolne": ["CNBC AI", "The Information", "XYZ Technologia", "JetBrains", "JVM Bloggers",
                    "Nowy Marketing AI", "Ministerstwo Cyfryzacji", "ICEYE Blog", "ICEYE Press (PL)",
                    "Datadog AI", "Netflix Tech Blog", "GitHub Blog", "Stack Overflow AI", "LeadDev AI",
                    "Google Workspace Updates", "Mam Startup"],
  "wzorce_nie": [
    {"wzorzec": "^Fragments:", "powod": "przegląd linków autora"},
    {"wzorzec": "for Beginners", "powod": "poradnik dla początkujących"},
    {"wzorzec": "\\b\\d+(\\.\\d+)+ (Is|Are) (Now )?(Out|Available)", "powod": "wydanie wersji narzędzia"},
    {"wzorzec": "Bug-?Fix Releases?", "powod": "wydanie poprawek"},
    {"wzorzec": "availability report", "powod": "raport dostępności usługi"},
    {"wzorzec": "stock (sinks|jumps|falls|rises|surges|slides|soars)|price target", "powod": "komentarz giełdowy"}
  ]
}
```

## Skuteczność stron (historia)

Ile wpisów ze strony trafiło do wydań (link albo ten sam temat), stan z `zarzadzaj.py lista`, 2026-11-26 (po przeglądzie #48):

| Strona | Wzięte / wpisy | Komentarz |
|---|---|---|
| Addy Osmani | 8/10 | prawie wszystko — domyślnie „tak” |
| Martin Fowler | 12/44 | artykuły tak, „Fragments” i osobiste nie |
| OpenAI News | 18/276 | tylko duże premiery i stanowiska; case study, granty, regiony — nie |
| Future Tools News | 81/975 | agregator, największe źródło tematów; brać duże newsy, drobne launche — nie; w przeglądzie 8.10 premiery i stanowiska („tak”) pominięte, a „może” (plugin, raport rynku, polityka) wzięte — wszystko tu „może” |
| Anthropic News | 4/35, Research 1/41 | premiery modeli tak, reszta może |
| Google for Developers | 4/51 | premiery modeli i narzędzi AI; nowa funkcja SDK bez premiery — może |
| Google Antigravity | 4/12 | premiery modeli w Antigravity, o ile ten sam model nie ma już wpisu ze źródła pierwotnego |
| The Decoder | 18/534 | agregator; bierze tylko konkretne duże newsy biznesowe (IPO, Meta–Nvidia, emisja akcji), premiery modeli, stanowiska i spekulacje o rundach — może (4 „tak” pominięte w #44); w #45 wzięty 1 z 41 (przejęcie Pierre), więc bez dużego ruchu czołowej firmy — nie |
| AIOAI.pl | 4/71 | polski agregator; duże tematy |
| GitHub Blog | 3/78 | ewaluacja i code review z AI tak; własne case studies/rewrite bez przenośnej lekcji, Copilot for Beginners, raporty — nie |
| Lovable | 5/38 | przejęcia i rundy tak, partnerstwa bez zmiany biznesowej — nie |
| XYZ Technologia | 9/73 | polskie wywiady, startupy i wdrożenia AI — może; w #43 wzięte 4 z 6 „może” |
| Mam Startup | 16/285 | polski agregator startupów i biznesu, prawie nic o AI — domyślnie „nie” (47 „nie” w #44, żaden nie wzięty), polskie tematy AI „może” (3 z 9 wziętych w #45: mObywatel, PayU + Visa, Wonderful; 1 z 10 w #44) |
| CNBC AI (1/157), Ministerstwo Cyfryzacji (2/55) | 1 | pojedyncze trafienia (koszty obrony przed AI; PLLuM w sądzie); reszta „nie”/„może” |
| Manus, ElevenLabs, ElevenLabs Product, Netflix (LLM-as-a-Judge), Simon Couch, Ashpreet Bedi | 1–2 na stronę | rundy, premiery modeli u nich, teksty techniczne |
| LangChain (4/158), JVM Bloggers (5/92) | 2–3 | posty inżynierskie o budowie agentów (LangChain), polskie teksty o AI w programowaniu (JVM) — „może”; reszta „nie” |
| Stack Overflow AI, JetBrains, Google Workspace Updates, Google Innovation & AI, Cursor (poza premierami modeli), ICEYE, Viktor, Datadog, LeadDev, The Batch, Perplexity, The Information (0/165) | 0 | domyślnie „nie” lub „może” przy wyjątkowym temacie; JetBrains developer diary (bez premiery) — może, nie tak |

## Przykłady decyzji Kuby (AI → Kuba)

_(uzupełnia `ucz-sie` na podstawie `dziennik/strony_wybory.jsonl`)_

- Mam Startup / Ministerstwo Cyfryzacji / Nowy Marketing / XYZ: Polska–Korea (AI), RTV Euro AGD + Gemini, Canva + koszty AI, spór o AI w reklamie Diora, Bielik — AI: może, Kuba: wzięty (#46).
- JetBrains „IDEs Transformed for the Agentic Era – With Air”, LangChain „What Is Eval-Driven Development?” — AI: może, Kuba: wzięty (#46).
- Martin Fowler (2), Lovable „The Radish AI team joins Lovable”, OpenAI „GPT-6 Cyber” — AI: tak, Kuba: wzięty (#46) — wszystkie 4 „tak” trafione.
- OpenAI News: 16 wpisów „może" (case study klientów, wewnętrzny sprint bezpieczeństwa, Model Spec) — Kuba pominął wszystkie; poza premierami to „nie”.
- Future Tools News: „Google Launches Gemini 4 Neon…”, „OpenAI Launches GPT-6.2 Astra and Sol…” (duplikaty) — AI: może, Kuba: wzięty (#47); pozostałe 44 „może” z tego agregatora pominięte — duplikat „może” tylko dla premier czołowych modeli.
- OpenAI News: 11 wpisów „może” — Kuba pominął wszystkie (#47, razem 0/27 z #46) — poza premierą i dużym ruchem biznesowym to „nie”.
- The Decoder: 33 wpisy „może” (w tym duplikaty) — Kuba pominął wszystkie (#47, 3. raz) — dla Decodera duplikat = „nie”.
- Cursor: „An update on our recent security incident” — AI: może, Kuba: wzięty (#47) — incydent w czołowym narzędziu AI.
- JVM Bloggers: „Claude Code Review With Specialist Agents”, „The Harness Model v2” — AI: może, Kuba: wzięty (#47) — praktyczne teksty o agentach.
- Mam Startup / XYZ: Nvidia po odejściu Huanga, Apple Health AI, LATO 4,7 mln $ — AI: może, Kuba: wzięty (#47); pozostałe 6 „może” z Mam Startup pominięte.
- Anthropic News „Anthropic prices initial public offering”, OpenAI „GPT-6.2 Astra and Sol”, Martin Fowler „Generated Glossary” — AI: tak, Kuba: wzięty (#47) — wszystkie 3 „tak” trafione.
- The Decoder: 50 wpisów (15 „może”) — Kuba pominął wszystkie (#48, 4. raz z rzędu) — bez dużego ruchu biznesowego czołowej firmy to „nie”, także stanowiska i ruchy kadrowe.
- Future Tools News: „Anthropic Veteran Thariq Joins OpenAI…”, „Anthropic Launches Claude Ship…” — AI: może, Kuba: wzięty (#48); pozostałe 14 „może” pominięte — przejście kluczowej osoby między czołowymi labami i premiera produktu czołowego labu to „może”.
- Mam Startup: „Sztuczna inteligencja zużywa mniej wody niż mleko migdałowe…”, „Sztuczna inteligencja oceni zdolność kredytową. Krakowski Bank Spółdzielczy…” — AI: może, Kuba: wzięty (#48) — raport o kosztach środowiskowych AI i pierwsze w Europie wdrożenie scoringu AI w banku; 6 pozostałych „może” pominiętych.
- LangChain „How to build a knowledge factory for AI agents” — AI: może, Kuba: wzięty (#48) — własny harness agentów z lekcją zostaje „może”; pozostałych 7 wpisów LangChain „nie” słusznie.
