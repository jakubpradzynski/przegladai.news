# Opisy newsów

## Uwagi Kuby

_(miejsce na Twoje uwagi — AI tej sekcji nie zmienia)_


## Dla kogo piszemy (punkt wyjścia do każdego opisu)

Czytelnik to inżynier oprogramowania, engineering manager, czasem product manager lub UX, a do tego ktoś, kto
interesuje się finansami i tym, jak AI zmienia gospodarkę, startupy i rynek pracy. Opis ma odpowiadać na
pytanie **„co to znaczy dla mnie?”**, a nie tylko „co się stało?”. Sam suchy fakt nie wystarcza.

- **Inżynier:** co mogę z tym zrobić, co mi to upraszcza, co utrudnia, czego unikać.
- **Engineering manager / PM / UX:** co mogę wymagać od zespołu, jaki obraz sytuacji dostaję bez wchodzenia w szczegóły
  techniczne, na co zwracać uwagę przy decyzjach. Szczegóły implementacji zostają w źródle.
- **Finanse i biznes:** kto płaci, ile, po co, w jakim kierunku idą pieniądze, co to znaczy dla inwestora, założyciela
  albo klienta. Do tego ocena skali: duży czy mały wzrost, drogo czy tanio, na tle czego.

## Długość i budowa

- Jeden akapit, 3–4 zdania, zwykle 450–750 znaków (po #41 Kuba skracał do ~600, więc nie rozciągamy; ale nowe
  elementy poniżej mają pierwszeństwo przed upychaniem liczb). Walidator: 350–1200.
- **Zdanie 1: co się stało albo o czym jest materiał** – prosto, bez powtarzania tytułu. Gdy tytuł już mówi, kto i co
  zrobił, zaczynamy od szczegółu lub znaczenia.
- **Zdania 2–3: konkrety, które coś mówią.** Co się zmienia w praktyce, co to upraszcza lub utrudnia, na tle czego
  to wypada (poprzednia wersja, konkurencja, cena). Przykład z materiału, ale tylko taki, który da się zrozumieć bez
  czytania źródła.
- **Ostatnie zdanie: perspektywa czytelnika.** Dla kogo to jest istotne i dlaczego albo jaki wniosek z tego wynika
  („Jeśli masz dużo powtarzalnych procesów w przeglądarce, to może obniżyć rachunek.”). Zdanie ma być oparte na
  treści materiału i konkretne – nie ogólna recenzja tekstu („ciekawy, klarowny”) i nie „to ważny krok”.
  To zmiana wobec reguły z #39–#44, gdzie Kuba wycinał końcowe komentarze: wycinane były komentarze ogólne,
  oceny tekstu i drobne uwagi o braku danych, a nie konsekwencje dla czytelnika, o które teraz prosi.
- Opis zachęca do kliknięcia przez to, co obiecuje w środku („pokazuje, jak…”, „wylicza 11 pomysłów, wśród
  nich…”), bez wprost napisanego „warto przeczytać”.
- Osobny fakt doklejony po przecinku rozbijamy na dwa zdania. Krótsze zdania, ten sam komplet faktów.

## Liczby i wyniki testów

- **Wyniki benchmarków same w sobie nic nie mówią.** „88,2% w SEC-bench Pro”, „50,3% w Terminal-Bench” – nie podajemy
  bez kontekstu. Zamiast tego opisujemy słowami, w czym model jest dobry i co to oznacza.
- Liczba ma sens, gdy jest **porównaniem**: skok względem poprzedniej wersji („dwa razy mniej błędów”), przekroczony
  próg, miejsce na tle konkurencji, cena względem innych modeli. Maksymalnie 1–2 takie liczby na opis.
- Nowy model: do czego jest przeznaczony, co to zmienia dla producenta (wraca do czołówki?) i dla użytkowników
  (zadania, koszt, kto skorzysta), jak wypada cenowo na tle innych.
- Wyniki finansowe: zawsze z oceną skali („wzrost ponad 40-krotny w dwa lata”, „strata głównie księgowa”) i tym,
  co z tego wynika dla kogoś, kto interesuje się inwestowaniem. Szczegóły struktury (klasy akcji, instrumenty
  finansowe) pomijamy, zostaje to, co zmienia sens: kto kupuje, ile, po co, czy rozwadnia, dokąd idą pieniądze.
- Wprost mówimy, czy wynik jest dobry czy słaby, gdy da się to uzasadnić porównaniem.

## Autorzy, firmy, źródła

- **Nazwisko tylko wtedy, gdy podnosi wagę** (założyciel zespołu, szef dużej firmy, współtwórca znanego projektu).
  Zwykle lepsza jest rola i firma: „szef zespołu FDE w OpenAI”, „manager inżynierii w Anthropic, współtwórca
  Electrona”. Nazwiska bez znaczenia dla czytelnika pomijamy, tak samo nazwę bloga czy newslettera.
- Firmę podajemy, gdy skala lub renoma jest argumentem (duże firmy wdrażające rozwiązanie, laboratorium AI).
- Newsy „z USA”: pytamy, **co się pod tym kryje**, a nie kto konkretnie (nie „banki w USA”, tylko mechanizm: banki
  nie chcą obcych agentów na kontach klientów i dlaczego). Polski czytelnik może dostać pytanie, czy to dotrze też do nas.

## Język

- Proste słowa i krótkie zdania (zwykle do ~20 słów). Jedna myśl na zdanie. Jak w rozmowie z kolegą z branży:
  „cierpią na tym rodzice i opiekunowie”, a nie „wypychają z firmy”. „Jakie osoby zakładają firmy dzięki AI”,
  a nie „jakie profile założycieli awansują”.
- **Nie piszemy o niczym, czego sami nie rozumiemy.** Niejasne sformułowania z artykułu (np. „utrwalają harness”,
  „telewizory z dashboardami”) rozwijamy do konkretu w pół zdania albo pomijamy cały wątek. Każde zdanie ma być
  zrozumiałe bez czytania źródła.
- **Anglicyzmy:** zostają te, których w Polsce się używa (harness, prompt, pull request, feature flag, deployment,
  fine-tuning, sandbox, benchmark). Nie tłumaczymy ich na siłę. Pilnujemy jednak, żeby w jednym zdaniu nie stało
  kilka angielskich terminów obok siebie i nie było list nazw z branży bez wyjaśnienia.
- Jeśli materiał opiera się na kilku pojęciach, wybieramy dwa najważniejsze i wyjaśniamy je, zamiast wymieniać
  wszystkie („o wszystkim i o niczym”).
- Tekst o jednej tezie: podajemy tezę i 1–2 wnioski, które można zastosować.

## Pytania do czytelnika

Dozwolone **jedno konkretne pytanie** w opisie, najlepiej na końcu, gdy materiał sam skłania do przemyślenia
(„Czy podobne ograniczenia pojawią się w polskich bankach?”). Maks. 2–3 takie opisy w wydaniu, nie w sąsiednich newsach.

## Dodatkowe informacje z internetu

Gdy materiał mówi zbyt mało, by ocenić znaczenie (brak porównania ceny, nieznana firma, brak skali), agent może
poszukać 1–2 faktów w internecie (WebSearch): poprzednia wersja modelu, cena konkurencji, rozmiar firmy,
tło transakcji. Tylko fakty, które pasują do opisu i które da się potwierdzić; źródło dopisujemy do pola `Uwagi`.
Nie dodajemy spekulacji. Gdy strony nie da się odczytać, nie zgadujemy (reguła bez zmian).

## Ton

- Autor jest inżynierem i managerem, który przeczytał tekst i ma zdanie. Wolno ocenić skalę i znaczenie
  („duży skok”, „słaby wynik”, „tanio na tle konkurencji”), jeśli wynika to z porównania.
- Przy wideo i podcastach: kto rozmawia (rola, nie tylko nazwisko), 2–3 konkretne wątki, kto skorzysta.
- Bez uwag o tym, jak powstał opis i o czasie trwania demonstracji w odcinku – idzie do pola `Uwagi`.
- Przy tekstach za paywallem nie udawać, że przeczytało się całość – opisywać to, co widać. Samego paywalla
  nie komentujemy w opisie (od tego jest tag `Za paywallem`).
- Bez słów względnego czasu („dziś”, „wczoraj”, „w tym tygodniu”) – wydanie czyta się później.
- **Bez zdań o braku informacji w źródle, o wiarygodności źródła i o ograniczeniach badania** (Kuba wycinał je
  w #39–#44: „Wartość transakcji nie została ujawniona”, „bez niezależnej weryfikacji”, „typowo marketingowy”,
  „nie jest to ranking”). Takie uwagi idą do pola `Uwagi`.
- **Bez dopisków o dostępności, instalacji, cenniku, regionie i składzie zespołu**, chyba że to jest sedno newsa
  albo odpowiada na pytanie „czy to dla mnie” (np. model dostępny tylko dla wąskiej grupy obrońców). Maks. 1 takie
  zdanie.
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
- puste pytania retoryczne w stylu „Czy zastanawiałeś się…?” (konkretne pytanie o sytuację czytelnika – patrz „Pytania do czytelnika”)
- „bez niezależnej weryfikacji”, „typowo marketingowy”, „Informacje pochodzą ze strony producenta”
- listy i pogrubienia w opisie — opis to zwykły akapit

Oszczędnie (max 2 razy na wydanie, nie w sąsiednich newsach):
- „Obowiązkowa lektura dla każdego, kto…”, „Warto rzucić okiem”, „To pokazuje, że…”,
  „Ciekawy sygnał, że…”
- „stanowi” / „reprezentuje” tam, gdzie wystarczy „jest”
- imiesłowy doklejone na końcu zdania („…, podkreślając…”, „…, co czyni…”)
- struktura „nie tylko…, ale także…” i zasada trzech (zawsze dokładnie trzy przymiotniki)

Pełniejsza lista wzorców AI: skill `humanizer-pl`.

## Przykłady wzorcowe

> Morgan Stanley zaczął blokować zewnętrznych agentów AI, a JPMorgan, Bank of America i Citi ograniczają im dostęp. Powód jest prosty: banki nie potrafią odróżnić działań agenta od działań człowieka ani sprawdzić, czy agent ma upoważnienie, czy przejął konto. Część agentów dzwoni nawet na infolinię albo działa wbrew poleceniom właściciela. Banki przepisują regulaminy i zmierzają w stronę dostępu tylko do odczytu. Jeśli budujesz agentów, którzy mają obsługiwać finanse klientów, trzeba liczyć się z blokadami. Czy polskie banki pójdą tym samym tropem?

> Meta chce zebrać do 95 mld dolarów ze sprzedaży nowych akcji na centra danych i rozwój agenta Muse. Aż 60 mld ma pochodzić z nowej klasy akcji bez prawa głosu, więc Mark Zuckerberg zachowa pełną kontrolę nad firmą. Nvidia, AMD i Broadcom wstępnie zainteresowały się zakupem akcji za łącznie do 5 mld dolarów, czyli dostawcy chipów mogą inwestować w klienta, który kupuje od nich sprzęt. Dla inwestorów to sygnał, że wyścig o moc obliczeniową jest tak drogi, że nawet Meta sięga po pieniądze z rynku kapitałowego.

> Każdy agent AI składa się z modelu, pętli sterującej i narzędzi, a to, gdzie każdy z nich działa – na laptopie, w chmurze czy na maszynie wirtualnej – decyduje o kosztach, prywatności i bezpieczeństwie. Autor pokazuje to na znanych przykładach: w Claude Code model działa w chmurze, a reszta na twoim komputerze, a w ChatGPT wszystko jest u OpenAI. Najważniejsza rada dotyczy bezpieczeństwa. Agent, który ma dostęp do prywatnych danych, czyta niezaufane treści i może coś wysyłać na zewnątrz, jest groźny, a na laptopie szkody mogą być większe niż w odizolowanej maszynie wirtualnej. Przyda się każdemu, kto wybiera, gdzie w zespole uruchamiać agentów.

## Przykłady poprawek (AI → Kuba)

_(uzupełnia `ucz-sie` na podstawie dziennika)_

- #41 Opis (Nolla Derm, Bloomberry, TikTok): usunięte „Informacje pochodzą ze strony producenta, bez niezależnej weryfikacji skuteczności.”, „Dane pochodzą ze śladów technicznych…, więc to estymacja” i „Komunikat jest typowo marketingowy…” — wiarygodność źródła nie należy do opisu.
- #41 Opis (Claude w Google Workspace, 706 → 416 znaków): usunięte trzy zdania o trybach zatwierdzania, Compliance API i instalacji z Marketplace — opis zostaje przy tym, co Claude robi w Dokumentach, Arkuszach i Prezentacjach.
- #42 Opis (Fowler, harnessy): usunięte „Słusznie zaznacza też ograniczenia: jeden serwis i małe próbki.” — zastrzeżenie na końcu (jak #39), opis kończy się wnioskiem autora.
- #42 Opis (Pragmatic Engineer, sciencesays, ElevenLabs Brand Kit): usunięte „oraz o nowych otwartych modelach z UE i USA”, „Praca ukazała się w Journal of the Academy of Marketing Science.”, „bez podania terminów” — poboczne wątki, miejsce publikacji i brak terminu zapowiedzi.
- #42 Opis (Gemini w Workspace, Scion): „…miesięcznie, a wersja konsumencka pojawi się później.” → „…miesięcznie. Wersja konsumencka pojawi się później.”; „Migracja zajęła pięć miesięcy, a Scion nie jest…” → dwa zdania — osobny fakt po przecinku rozbijamy.
- #42 Opis (bug hunter Paolo Perrone): usunięte „i wyścigi, które przeżywają poprawkę” z listy czterech sposobów — techniczny detal spoza głównej tezy.
- #42 Opis (mamstartup EY): „dostosowaniu do regulacji” → „dostosowaniu do przepisów regulacyjnych”; Trasti: „NNW szkolnego” → „szkolnego NNW” — drobne korekty szyku i słownictwa (1×).
- #43 Opis (Cyberly, Iowa, Vals, Verna, Amazon memo): usunięte ostatnie zdania o braku danych i ocenie („Wartość transakcji nie została ujawniona.”, „Pozew nie wskazuje kwot ani kar.”, „…nie jest to ranking.”) — opis kończy się konkretem, nie komentarzem do źródła.
- #43 Opis (CNBC fundusz Anthropic, Stripe, Seth Godin, GitHub): usunięty poboczny wątek na końcu (komentarz Muska, blokada Muse przez Amazon, dwa dodatkowe modele biznesowe, lista otwartych pytań) — jeden główny fakt zamiast dopisków; w CNBC także „nie fundacja 501(c)(3), a” (amerykańska forma prawna).
- #43 Opis (Claude Duet, PLLuM, PKO): „jak planowanie spotkań, jak i…” → „czynności oraz planowanie spotkań…”; „sprawdzić i zatwierdzić sędzia” → „zostać sprawdzony i zatwierdzony przez sędziego”; „i” → „oraz” — drobne korekty składni, 1×.
- #43 Opis (Claude Code code review): „Past incydenty… testy sprawdzające reviewera” → „Przeszłe incydenty… testy sprawdzane” — literówka i uproszczenie (fakt, nie styl).
- #44 Opis (Genie 4, S-1 Anthropic, Microsoft, FDE OpenAI, YC RFS, Latent Space, Verna): znów wycięte ostatnie zdania — ograniczenia modelu („Szczegóły obrazu… dryfują, a całość znakuje SynthID”), brak ceny akcji i Long-Term Benefit Trust, termin decyzji pracowników („odejdą 31 grudnia”), projekt głosowy dla telekomu, „Sam przyznaje, że to model myślowy”, zdanie o tym, że start-upy nie muszą pracować nad pomysłami YC — opis kończy się na ostatnim konkrecie głównej tezy (9 wpisów w jednym wydaniu; reguła ostatniego zdania działa, wciąż do pilnowania).
