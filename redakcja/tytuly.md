# Tytuły

## Uwagi Kuby

_(miejsce na Twoje uwagi — AI tej sekcji nie zmienia)_

## Tytuły newsów

- Zawsze po polsku. Nazwy własne (firm, modeli, produktów, narzędzi) zostają w oryginale:
  „GPT-6 Astra”, „Claude Code”, „Gemini 3.8 Flash”, „Forward Deployed Engineer”.
- Zapis zdaniowy: wielka litera tylko na początku i w nazwach własnych. Nigdy Title Case.
- Długość: zwykle 45–90 znaków (mediana w wydaniach #29–#38: 66). Powyżej ~100 skracać.
- Bez kropki na końcu. Pytajnik dozwolony, gdy oryginał jest pytaniem.
- Tytuł mówi, co się stało albo o czym jest tekst. Bez pustego clickbaitu i bez przymiotników
  typu „rewolucyjny”, „przełomowy”, „niesamowity”.
- Liczby i kwoty konkretnie i po polsku: „400 mln dolarów”, „3 mld euro”, „12,9 miliarda dolarów”,
  „10-krotnie”, „o 90%”.
- Cudzysłowy polskie „…” (albo proste "…", gdy tak było w źródle). Dopowiedzenia po półpauzie „–”.

### Wzorce według typu materiału

| Typ | Wzorzec | Przykłady z wydań |
|---|---|---|
| Premiera, ogłoszenie firmy | `<Firma> <czasownik w czasie teraźniejszym> <co> [– dopowiedzenie]` | „Anthropic prezentuje Claude Fable 5.1 i Claude Mythos 5.1”, „Slack wprowadza Surfaces – żywe interfejsy budowane w rozmowie”, „Waymo uruchamia autonomiczne przejazdy w Las Vegas” |
| Finansowanie, przejęcie | `<Firma> pozyskuje/przejmuje <kogo/ile> [przy wycenie …]` | „Mistral pozyskuje 3 mld euro na budowę suwerennej AI w Europie”, „Stripe przejmuje OpenRouter, bramkę do modeli AI, za ponad 7 miliardów dolarów” |
| Tekst techniczny, poradnik | `Jak …` albo pytanie z oryginału | „Jak Spotify zredukował zużycie tokenów Claude Code o 90%”, „Czy prawo Conwaya umarło w erze agentów AI?”, „Dlaczego prawdopodobnie nie chcesz fine-tune'ować własnego modelu LLM” |
| Tekst z wyraźnym autorem, opinia | `<Autor>: <teza>` albo `<Autor> <czasownik> …` — **tylko gdy autor jest powszechnie znany** (szefowie czołowych firm, rozpoznawalne nazwiska branży). Mniej znany autor → sam temat, a nazwisko w opisie. | „Dario Amodei: musimy kontrolować tempo rozwoju AI”, „Dan Luu sprawdza, czy agenci AI potrafią dobrze testować kod”; ale „Jak naprawdę zmierzyć wpływ AI na szybkość dostarczania kodu” (nie „James Shore: …”) |
| Wywiad, podcast, wideo | `<temat> – rozmowa z <kim>` albo `<Kto> w <podcast>: <wątki>` | „Jak powstawał Codex – rozmowa z Tibo Sottiaux z OpenAI”, „Jensen Huang w All-In Podcast: superinteligencja, doomerski hoax i telefon od Trumpa” |
| Badanie, raport, dane | `Badanie: <wniosek>` albo `Raport <kogo>: <wniosek>` | „Badanie: Google AI Mode poleca droższe produkty niż zwykła wyszukiwarka”, „Raport Anthropic: jak przestępcy wykorzystują Claude do cyberataków i oszustw” |
| Ciekawostka, wydarzenie | Zwykłe zdanie z faktem | „Chiński robot humanoidalny kopie swojego twórcę podczas testów” |

Gdy oryginał jest po polsku, tytuł zostaje oryginalny (najwyżej lekko skrócony).

## Tytuł wydania

Format: `Wydanie #<nr>: <temat A>, <temat B> i <temat C>`

- Trzy (czasem dwa) najmocniejsze tematy tygodnia, oddzielone przecinkiem, ostatni po „i”.
- Każdy temat to krótka fraza nominalna, 2–5 słów, z konkretem: firma, produkt, liczba, osoba.
  „Nowa Siri od Apple”, „GPT-6 Astra”, „Stripe kupuje OpenRouter”, „roboty na targach IFA”,
  „koniec ery Tima Cooka”.
- Mieszanka: jeden duży news produktowy + jeden temat biznesowo-społeczny + ciekawostka
  albo temat polski, jeśli jest mocny (Forum Cyfryzacji, ScamWatch, dymisja w rządzie).
- Lekko marketingowo, ale bez clickbaitu. Gra słów dozwolona, jeśli jest naturalna
  („(nie)bezpieczeństwo Grok CLI”).
- Całość do ~100 znaków. Pierwsze słowo po dwukropku wielką literą.
- Te trzy tematy muszą być w wydaniu i powinny się pojawić we wstępie.

Przykłady: „Wydanie #38: Nowa Siri od Apple, debata o spowolnieniu AI i Waymo w Las Vegas”,
„Wydanie #36: ScamWatch, OpenAI zrywa z Cursorem i koniec ery Tima Cooka”,
„Wydanie #34: Stripe kupuje OpenRouter, AI-szef zwalnia pracownika i DeepSeek bije rekord na GitHubie”.

Przy generowaniu zawsze 2–3 propozycje różniące się doborem tematów, nie tylko szykiem.

## Przykłady poprawek (AI → Kuba)

_(uzupełnia `ucz-sie` na podstawie dziennika)_

- #39 Tytuł: „James Shore: jak naprawdę zmierzyć wpływ AI…” → „Jak naprawdę zmierzyć wpływ AI…” — nazwisko mało znanego autora nie idzie do tytułu (tak samo: Orestis Ioannou, Paul Iusztin).
- #39 tytuł wydania: wybrana 1. propozycja „Claude Opus 5.5, wojna o agenta zakupowego Muse i AI Force Trumpa” — premiera modelu + konflikt biznesowy + polityka; odrzucone warianty z dwoma premierami modeli naraz i z mniej znanym wątkiem (Cowork).
