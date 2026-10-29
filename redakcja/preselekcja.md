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
  (partnerstwo dystrybucyjne), duplikat z agregatora też dawaj jako „może”, nie „nie”.
- **Future Tools News: nigdy „tak”.** W #41 Kuba pominął wszystkie 3 wpisy ocenione tu na „tak” (GPT-6 — ten sam
  news miał już z openai.com w `data.csv`; Runway Praxis-1; Team Human) i wziął 4 z „może” (plugin ChatGPT do notatek,
  EmbeddingGemma 2, raport a16z, ogłoszenie Trumpa). Premiery i stanowiska relacjonowane przez ten agregator
  to „może”; „tak” tylko gdy brak źródła pierwotnego w partii i `data.csv`.
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

- Teksty inżynierskie o budowie agentów od dużych zespołów, nawet z bloga vendora (LangChain „The Art of Loop Engineering”,
  „How We Built Our Design Agent” — AI „może”/„nie”, Kuba wziął oba #44) i wyjaśnienia roli/praktyki z laboratorium
  (OpenAI „What FDE means at OpenAI”). Case study klienta nadal „nie”; własny agent/harness z lekcją — „może”.
- Polskie teksty o pracy z AI w programowaniu (JVM Bloggers „AI w SDLC: Model nie ma znaczenia” — wzięty #44, 1 z 8 „może”).
- Decoder i inne agregatory — stanowiska i spekulacje o rundach/wycenach (Jack Clark o 2027, Altman o alignmencie,
  OpenAI obniża wycenę, OpenAI podbiera klientów Anthropic — wszystkie AI „tak”, Kuba pominął #44): to „może”.
  „Tak” dla agregatora tylko przy konkretnym, dużym fakcie biznesowym (Meta–Nvidia 3 mld $, emisja akcji Meta 95 mld $ — wzięte #44).
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

Ile wpisów ze strony trafiło do wydań (link albo ten sam temat), stan z `zarzadzaj.py lista`, 2026-10-29 (po przeglądzie #44):

| Strona | Wzięte / wpisy | Komentarz |
|---|---|---|
| Addy Osmani | 8/10 | prawie wszystko — domyślnie „tak” |
| Martin Fowler | 7/38 | artykuły tak, „Fragments” i osobiste nie |
| OpenAI News | 15/226 | tylko duże premiery i stanowiska; case study, granty, regiony — nie |
| Future Tools News | 73/837 | agregator, największe źródło tematów; brać duże newsy, drobne launche — nie; w przeglądzie 8.10 premiery i stanowiska („tak”) pominięte, a „może” (plugin, raport rynku, polityka) wzięte — wszystko tu „może” |
| Anthropic News | 3/34, Research 1/35 | premiery modeli tak, reszta może |
| Google for Developers | 4/49 | premiery modeli i narzędzi AI; nowa funkcja SDK bez premiery — może |
| Google Antigravity | 4/12 | premiery modeli w Antigravity, o ile ten sam model nie ma już wpisu ze źródła pierwotnego |
| The Decoder | 17/376 | agregator; bierze tylko konkretne duże newsy biznesowe (IPO, Meta–Nvidia, emisja akcji), premiery modeli, stanowiska i spekulacje o rundach — może (4 „tak” pominięte w #44) |
| AIOAI.pl | 4/68 | polski agregator; duże tematy |
| GitHub Blog | 3/70 | ewaluacja i code review z AI tak; własne case studies/rewrite bez przenośnej lekcji, Copilot for Beginners, raporty — nie |
| Lovable | 3/35 | przejęcia i rundy tak, partnerstwa bez zmiany biznesowej — nie |
| XYZ Technologia | 7/54 | polskie wywiady, startupy i wdrożenia AI — może; w #43 wzięte 4 z 6 „może” |
| Mam Startup | 6/210 | polski agregator startupów i biznesu, prawie nic o AI — domyślnie „nie” (47 „nie” w #44, żaden nie wzięty), polskie tematy AI „może” (1 z 10 wzięty w #44: Meta Muse) |
| CNBC AI (1/126), Ministerstwo Cyfryzacji (1/43) | 1 | pojedyncze trafienia (koszty obrony przed AI; PLLuM w sądzie); reszta „nie”/„może” |
| Manus, ElevenLabs, ElevenLabs Product, Netflix (LLM-as-a-Judge), Simon Couch, Ashpreet Bedi | 1–2 na stronę | rundy, premiery modeli u nich, teksty techniczne |
| LangChain (2/136), JVM Bloggers (3/76) | 2–3 | posty inżynierskie o budowie agentów (LangChain), polskie teksty o AI w programowaniu (JVM) — „może”; reszta „nie” |
| Stack Overflow AI, JetBrains, Google Workspace Updates, Google Innovation & AI, Cursor (poza premierami modeli), ICEYE, Viktor, Datadog, LeadDev, The Batch, Perplexity, The Information | 0 | domyślnie „nie” lub „może” przy wyjątkowym temacie; JetBrains developer diary (bez premiery) — może, nie tak |

## Przykłady decyzji Kuby (AI → Kuba)

_(uzupełnia `ucz-sie` na podstawie `dziennik/strony_wybory.jsonl`)_

- Netflix Tech Blog: „The Lifecycle of LLM-as-a-Judge: Building, Aligning, and Monitoring at scale” — AI: może,
  Kuba: wzięty — tekst z przenośną lekcją o ewaluacji LLM od dużego zespołu; „może”, nie „nie”.
- Mam Startup: „ElevenLabs i Trasti… Polisy kupimy w trakcie rozmowy z botem” — AI: może, Kuba: wzięty —
  polskie wdrożenie głosowej AI; podobnie „Żabka Jush” (Nowy Marketing) i badanie o wynikach firm z AI.
- CNBC AI: „Bank of America hired 1,000 contractors to patch software flaws exposed by Anthropic's Mythos” —
  AI: może, Kuba: wzięty — koszty obrony przed AI to news; CNBC bez komentarza giełdowego bywa dobre.
- Future Tools News: „OpenAI Accuses Ex-Employee of Leaking 100+ Confidential Files to Apple” — AI: może, Kuba: wzięty —
  spór z byłym pracownikiem OpenAI wystarcza (obok „YouTube conversational search”); zostaje „może”.
- OpenAI News: „OpenAI acquires Orchestra Bio” — AI: tak, Kuba: pominięty — przejęcie niszowej firmy (biofarma) to „może”, nie „tak”.
- Future Tools News: „DeepSeek Launches V4.1-Flash-1017…” — AI: tak, Kuba: pominięty — migawka/wersja poboczna modelu to „może”, mimo źródła pierwotnego.
- Future Tools News: „OpenAI Brings Frontier Models and Codex to Google Cloud's Model Garden” — AI: nie (duplikat), Kuba: wzięty — gdy oryginał to „może” (partnerstwo), duplikat z agregatora też „może”.
- XYZ Technologia: „Wordware robi wielki zwrot… Sauna” (i Mam Startup: „Czy Sauna działa w saunie?”) — AI: może, Kuba: wzięty — polski start produktu AI z dużą wyceną; ten sam temat z dwóch źródeł zostaje „może”.
- Mam Startup: „PKO Bank Polski wdraża autorskie modele AI. Mała Genia i Duża Genia…” — AI: może, Kuba: wzięty — duże polskie wdrożenie AI w banku; polskie wdrożenia to „może”.
- Ministerstwo Cyfryzacji: „Asystent AI dla sędziów – PLLuM trafi do NSA” — AI: może, Kuba: wzięty — polski AI w administracji ze źródła pierwotnego (gov.pl).

- LangChain: „How We Built Our Design Agent” — AI: nie (case study vendora), Kuba: wzięty — własny agent open source z opisem harnessu to nie case study klienta; „może”.
- LangChain: „The Art of Loop Engineering” — AI: może, Kuba: wzięty — ogólna lekcja o pętli agentów; posty inżynierskie LangChain zostają „może”.
- OpenAI News: „What FDE means at OpenAI” — AI: może, Kuba: wzięty — wyjaśnienie praktyki z laboratorium; „może”, nie „nie”.
- The Decoder: „Anthropic co-founder Jack Clark moves his prediction for self-improving AI forward to 2027”, „Sam Altman says advanced AI will inevitably escape its sandbox…”, „OpenAI lowers valuation target, raises up to $30 billion”, „OpenAI offers discounts… to poach Anthropic's biggest customers” — AI: tak, Kuba: pominięty (wszystkie 4) — stanowiska i spekulacje o rundach przez agregator to „może”; wziął tylko Meta–Nvidia i emisję akcji Meta (konkretne fakty).
- Anthropic News / Future Tools News: „Anthropic files S-1 with the SEC…” — AI: tak, Kuba: pominięty — temat IPO był już w partii z innych źródeł; sprawdzać duplikat przed „tak”.
- JVM Bloggers: „AI w SDLC: Model nie ma znaczenia” — AI: może, Kuba: wzięty — polski tekst o pracy z Claude Code; z 8 wpisów JVM Bloggers wziął 1, reszta „nie”.
