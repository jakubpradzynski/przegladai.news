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

- Premiery i duże aktualizacje modeli czołowych laboratoriów: OpenAI, Google/DeepMind, Anthropic, Meta,
  xAI, Mistral, DeepSeek, Apple. Przykłady wziętych: „GPT-6 Astra”, „Introducing ChatGPT Images 2.5”,
  „Gemini 3.8 Live”, „Introducing Grok 4.6”.
- Duże ruchy biznesowe w AI: przejęcia, rundy od ~100 mln $, zmiany kierownictwa w czołowych firmach,
  zerwane partnerstwa („Our decision on Cursor following its acquisition by SpaceX”, „Lovable raised $400M”).
- Stanowiska i eseje liderów branży, które wywołują dyskusję (Amodei o tempie rozwoju AI,
  „Pacing model development…”, „An Alien Mind”).
- Teksty inżynierskie z uniwersalną lekcją o pracy z AI i agentami, od znanych autorów:
  Addy Osmani (8/10 wpisów trafiło do wydań), Martin Fowler (artykuły, nie „Fragments”),
  GitHub Blog o ewaluacji i code review z AI („How to evaluate LLMs before production”).
- Nowe kategorie produktów AI albo coś, co przebiło się do mediów (Tavus Phoenix, TypeSafe Jev).

## Zwykle „może”

- Relacje agregatorów (The Decoder, Future Tools, AIOAI.pl, LLM Stats) o dużych premierach. Temat bywa
  dobry, ale do wydania trafia źródło pierwotne. Gdy w tej samej partii jest wpis ze źródła pierwotnego,
  ocena agregatora = „nie” z powodem „duplikat: <tytuł źródła>”.
- Polskie tematy o AI: prawo, administracja, polskie firmy (gov.pl, AIOAI.pl, Nowy Marketing, XYZ).
  Tylko gdy dotyczą AI; sama cyfryzacja czy cyberbezpieczeństwo bez AI to „nie”.
- Badania i raporty z danymi (Anthropic Economic Index, raporty o rynku pracy).
- Ogłoszenia narzędzi developerskich AI (Cursor, JetBrains AI, Antigravity), gdy to nowa funkcja,
  a nie poprawka.

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
- Marketing platform agentowych bez ogólnej lekcji (LangChain: 0/96 w historii, Stack Overflow Blog: 0/39).

## Skuteczność stron (historia)

Ile wpisów ze strony trafiło do wydań (link albo ten sam temat), wydania #29–#38:

| Strona | Wzięte / wpisy | Komentarz |
|---|---|---|
| Addy Osmani | 8/10 | prawie wszystko — domyślnie „tak” |
| Martin Fowler | 5/28 | artykuły tak, „Fragments” i osobiste nie |
| OpenAI News | 12/140 | tylko duże premiery i stanowiska; case study, granty, regiony — nie |
| Future Tools News | 60/573 | agregator, największe źródło tematów; brać duże newsy, drobne launche — nie |
| Anthropic News | 3/12, Research 1/12 | premiery modeli tak, reszta może |
| Google for Developers | 3/19 | premiery modeli i narzędzi AI |
| Google Antigravity | 4/10 | premiery modeli w Antigravity |
| The Decoder | 4/92 | agregator; zwykle źródło pierwotne jest lepsze |
| AIOAI.pl | 3/43 | polski agregator; duże tematy |
| GitHub Blog | 2/47 | ewaluacja i code review z AI tak; Copilot for Beginners, raporty — nie |
| Lovable, Manus, ElevenLabs, Netflix, Simon Couch, Ashpreet Bedi | 1–2 na stronę | rundy, premiery modeli u nich, teksty techniczne |
| LangChain, Stack Overflow AI, JetBrains, JVM Bloggers, Google Workspace Updates, Google Innovation & AI, Cursor (poza premierami modeli), ICEYE, Viktor, Datadog, LeadDev, The Batch | 0 | domyślnie „nie” lub „może” przy wyjątkowym temacie |

## Przykłady decyzji Kuby (AI → Kuba)

_(uzupełnia `ucz-sie` na podstawie `dziennik/strony_wybory.jsonl`)_
