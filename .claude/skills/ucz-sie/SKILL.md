---
name: ucz-sie
description: Uczy reguły redakcyjne PrzeglądAI na poprawkach i decyzjach Kuby - czyta nowe wpisy z redakcja/dziennik/poprawki.jsonl (teksty, selekcja) i strony_wybory.jsonl (preselekcja wpisów ze stron) i sam aktualizuje redakcja/*.md. Uruchamiany automatycznie przez zakoncz-wydanie, zbierz-dane i przeglad-stron; także na "ucz się z poprawek".
---

Twoim zadaniem jest, żeby Kuba co tydzień poprawiał mniej. Każda jego poprawka jest informacją
o tym, czego reguły jeszcze nie mówią. Działasz sam — **nie pytasz Kuby o zgodę**. Zmiany trafiają
do PR-a wydania, więc Kuba zobaczy je w diffie i może je cofnąć.

## Krok 1 — Nowe wpisy

```bash
python3 narzedzia/dziennik.py nowe
```

Brak nowych wpisów → zakończ jednym zdaniem.

## Krok 2 — Analiza

Przeczytaj wszystkie pliki `redakcja/*.md` i pogrupuj nowe wpisy:

| Wpisy | Plik |
|---|---|
| `zmiana` pola `Tytuł`, `wybrany_tytul`, `zmiana` pola `tytul` | `tytuly.md` |
| `zmiana` pola `Opis` | `opisy.md` |
| `zmiana` pól `Tagi`, `Czas` | `tagi.md` |
| `odrzucony_top`, `wybrany_z_rezerwy`, `dodany_przez_kube`, `usuniety_w_substacku`, `podsumowanie`, `zmiana` pola `kolejnosc` | `priorytety.md` (kolejność: sekcja „Kolejność w wydaniu”) |
| `zmiana` pola `wstep` | `wstep.md` |
| `zmiana` pól `opis_seo`, `slug`, `okladka` | `seo.md` |

Dla każdej zmiany tekstu porównaj wersję AI z wersją Kuby i nazwij, **co dokładnie** zmienił
(skrócił? usunął frazę? zmienił szyk? dodał kontekst? zmienił ton? poprawił fakt?). Zmiany czysto
faktograficzne (literówka w nazwie, zła liczba) nie są regułą stylu — pomiń je, chyba że się powtarzają.

## Krok 3 — Aktualizacja reguł

Zasady:
- **Nigdy nie edytuj sekcji „Uwagi Kuby”.**
- **Pojedyncza poprawka** → para w sekcji „Przykłady poprawek (AI → Kuba)” właściwego pliku:
  `- #<nr> <pole>: „<AI>” → „<Kuba>” — <czego uczy, jednym zdaniem>` (długie opisy skróć do fragmentu, który się zmienił).
  Trzymaj najwyżej 12 przykładów na plik — najstarsze usuwaj (zostają w dzienniku).
- **Wzorzec powtarzający się (2+ razy w dzienniku, także w starszych wpisach)** → reguła w odpowiedniej
  sekcji pliku (zmień istniejącą albo dodaj nową). Przykłady, na których się opiera, możesz wtedy usunąć.
- **Fraza, którą Kuba konsekwentnie usuwa** → dopisz ją do listy „Nie używać” w `opisy.md`
  (w cudzysłowie „…” — walidator czyta ją stamtąd automatycznie).
- **Selekcja** → w `priorytety.md`, sekcja „Czego się nauczyliśmy z selekcji”: jakie typy newsów, źródła
  i tematy Kuba odrzuca mimo wysokiej oceny, a jakie bierze z rezerwy. Gdy wzorzec jest wyraźny,
  popraw rubrykę ocen albo proporcje sekcji.
- Przy konflikcie z istniejącą regułą wygrywa nowsza — zmień starą i odnotuj to w kroku 4.

## Krok 4 — Dziennik zmian reguł

Dopisz na końcu `redakcja/zmiany-regul.md`:

```markdown
## <RRRR-MM-DD> — wydanie #<nr>

- <plik>: <co się zmieniło> (na podstawie: <krótko które poprawki, np. 3× skrócony opis wideo>)
```

## Krok 5 — Oznacz jako przetworzone

```bash
python3 narzedzia/dziennik.py oznacz
```

Na koniec podaj Kubie 2–5 punktów: czego się nauczyłeś i co zmieniłeś.

## Część 2: preselekcja wpisów ze stron

Gdy skill uruchomiono z przeglądu stron (albo są nowe decyzje ze stron), zrób dodatkowo:

```bash
python3 narzedzia/dziennik.py nowe --strony
```

Pokazuje tabelę zgodności AI z Kubą (np. `tak->wziety: 12, tak->pominiety: 3, moze->wziety: 5`) i listę
rozbieżności: AI dało „tak”, a Kuba pominął; AI dało „może”/„nie”, a Kuba wziął. Zgodne decyzje
niczego nie uczą, więc lista ich nie zawiera.

Zaktualizuj `redakcja/preselekcja.md` (sekcji „Uwagi Kuby” nie ruszasz):
- **AI „nie”, a Kuba wziął** — najważniejszy sygnał: reguła odrzucenia jest za szeroka. Zawęź ją
  albo przenieś ten typ tematu do „Zwykle może”.
- **AI „tak”, a Kuba pominął** — typ tematu (albo strona) przechodzi z „Bierzemy” do „Zwykle może”;
  przy powtórce (2+ razy) do „Odrzucamy”.
- **AI „może”** — gdy dany typ tematu z danej strony Kuba konsekwentnie bierze (albo pomija) 3+ razy,
  zamień to w regułę „tak” (albo „nie”), żeby następnym razem nie trafiał do „Do decyzji”.
- Reguły automatyczne (blok JSON w sekcji „Reguły automatyczne”) zmieniaj ostrożnie — działają bez AI
  i bez podglądu: dopisz wzorzec do `wzorce_nie` albo stronę do `strony_ogolne` dopiero, gdy Kuba
  pominął taki typ wpisu 5+ razy i ani razu go nie wziął. Gdy Kuba wziął wpis, który reguła automatyczna
  odrzuciła (widać to po `powod_ai` zaczynającym się od „reguła:”), popraw albo usuń tę regułę od razu.
- Zaktualizuj tabelę „Skuteczność stron” (liczby z `python3 narzedzia/strony/zarzadzaj.py lista`).
- Dopisz do „Przykłady decyzji Kuby” pary w formacie
  `- <strona>: „<tytuł>” — AI: <ocena>, Kuba: <decyzja> — <czego uczy>` (najwyżej 15, najstarsze usuń).

Opisz zmiany w `redakcja/zmiany-regul.md` (jak w kroku 4) i oznacz: `python3 narzedzia/dziennik.py oznacz --strony`.
