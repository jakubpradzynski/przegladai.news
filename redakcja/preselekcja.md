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
  Przykłady wziętych: „GPT-6 Astra”, „Introducing ChatGPT Images 2.5”, „Gemini 3.8 Live”,
  „Introducing Grok 4.6”. Ta sama premiera relacjonowana przez agregator (The Decoder i podobne)
  to „może”, nawet gdy laboratorium jest czołowe — zob. „Zwykle może” niżej.
- Duże ruchy biznesowe w AI: przejęcia, rundy od ~100 mln $, zmiany kierownictwa w czołowych firmach,
  zerwane partnerstwa („Our decision on Cursor following its acquisition by SpaceX”, „Lovable raised $400M”),
  starcia konkurencyjne dużych graczy („Amazon blocks Meta's AI agent Muse from online shopping”),
  wieści o IPO czołowych labów („Anthropic is also reportedly postponing its IPO”) — także gdy
  relacjonuje je agregator, bo to news biznesowy, nie premiera produktu.
- Stanowiska i eseje liderów branży, które wywołują dyskusję (Amodei o tempie rozwoju AI,
  „Pacing model development…”, „An Alien Mind”).
- Teksty inżynierskie z uniwersalną, przenośną lekcją o pracy z AI i agentami (metodyka, ewaluacja),
  od znanych autorów: Addy Osmani (8/10 wpisów trafiło do wydań), Martin Fowler (artykuły, nie
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
  z powodem „duplikat: <tytuł źródła>”.
- Ogłoszenia inicjatyw badawczych/biznesowych bez konkretnego produktu („Anthropic is setting up
  a biology lab…” — pominięty #39) i pojedyncze głośne incydenty relacjonowane przez agregator
  („U.S. military nearly boarded a Chinese ship over a hallucinated AI report” — pominięty #39,
  mimo dużego newsa: prawdopodobnie zbyt pośrednie źródło).
- Nowa funkcja SDK/narzędzia deweloperskiego bez własnej premiery modelu (Google for Developers
  „Introducing Support for Local AI Models in the Antigravity SDK” — pominięty #39, mimo że to
  Antigravity: sama integracja lokalnych modeli to za mało na „tak”).
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
                    "Google Workspace Updates"],
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

Ile wpisów ze strony trafiło do wydań (link albo ten sam temat), wydania #29–#38:

| Strona | Wzięte / wpisy | Komentarz |
|---|---|---|
| Addy Osmani | 8/10 | prawie wszystko — domyślnie „tak” |
| Martin Fowler | 6/29 | artykuły tak, „Fragments” i osobiste nie |
| OpenAI News | 12/161 | tylko duże premiery i stanowiska; case study, granty, regiony — nie |
| Future Tools News | 60/614 | agregator, największe źródło tematów; brać duże newsy, drobne launche — nie |
| Anthropic News | 3/16, Research 1/16 | premiery modeli tak, reszta może |
| Google for Developers | 3/22 | premiery modeli i narzędzi AI; nowa funkcja SDK bez premiery — może |
| Google Antigravity | 4/10 | premiery modeli w Antigravity |
| The Decoder | 6/142 | agregator; bierze tylko newsy biznesowe (IPO, starcia firm), premiery modeli relacjonowane tu — może |
| AIOAI.pl | 3/48 | polski agregator; duże tematy |
| GitHub Blog | 3/51 | ewaluacja i code review z AI tak; własne case studies/rewrite bez przenośnej lekcji, Copilot for Beginners, raporty — nie |
| Lovable | 3/24 | przejęcia i rundy tak, partnerstwa bez zmiany biznesowej — nie |
| XYZ Technologia | 1/11 | polskie wywiady o wpływie AI na firmy — może, czasem wziete |
| Manus, ElevenLabs, ElevenLabs Product, Netflix, Simon Couch, Ashpreet Bedi | 1–2 na stronę | rundy, premiery modeli u nich, teksty techniczne |
| LangChain, Stack Overflow AI, JetBrains, JVM Bloggers, Google Workspace Updates, Google Innovation & AI, Cursor (poza premierami modeli), ICEYE, Viktor, Datadog, LeadDev, The Batch | 0 | domyślnie „nie” lub „może” przy wyjątkowym temacie; JetBrains developer diary (bez premiery) — może, nie tak |

## Przykłady decyzji Kuby (AI → Kuba)

_(uzupełnia `ucz-sie` na podstawie `dziennik/strony_wybory.jsonl`)_

- The Decoder: „xAI launches Grok 4.7 at bargain prices…” — AI: tak, Kuba: pominięty — premiera modelu
  relacjonowana przez agregator to „może”, nie „tak”, nawet dla znanego laba.
- The Decoder: „Amazon blocks Meta's AI agent Muse from online shopping” — AI: tak, Kuba: wzięty —
  news biznesowy/konkurencyjny (nie premiera modelu) z agregatora jest OK jako „tak”.
- The Decoder: „Following OpenAI, Anthropic is also reportedly postponing its IPO” — AI: tak,
  Kuba: wzięty — wieści o IPO czołowego laba biorą, nawet z agregatora.
- The Decoder: „Anthropic is setting up a biology lab where Claude guides robots…” — AI: tak,
  Kuba: pominięty — ogłoszenie inicjatywy badawczej bez konkretnego produktu to „może”.
- GitHub Blog: „Migrating the GitHub Copilot runtime to Rust, using Copilot” — AI: tak, Kuba: pominięty —
  opis własnego rewrite u vendora bez przenośnej lekcji to „może”, nie „tak”.
- GitHub Blog: „Should you read the code, is RAG dead, and did Skills kill MCP?” — AI: może,
  Kuba: wzięty — odcinek podcastu z hot-takes o AI można wziąć.
- JetBrains: „Building a RAG Pipeline for Semantic Code Search: A Developer Diary…” — AI: tak,
  Kuba: pominięty — developer diary o budowie własnego narzędzia to „może”.
- Google for Developers: „Introducing Support for Local AI Models in the Antigravity SDK” — AI: tak,
  Kuba: pominięty — nowa funkcja SDK bez premiery modelu to „może”.
- XYZ Technologia: „AI wycina menedżerów. «Firmy traktują to jak szansę…»” (WYWIAD) — AI: może,
  Kuba: wzięty — polski wywiad o wpływie AI na zarządzanie firmą pasuje do wydania.
