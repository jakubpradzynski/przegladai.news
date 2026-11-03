---
name: posty-social
description: Po wydaniu PrzeglądAI przygotowuje posty na LinkedIn (ten sam tekst na Facebook i Substack Notes) i wątki na X - post główny ze wstępu i posty pogłębione o wybranych newsach, z infografikami i promptami do zdjęć. Kuba wybiera tematy i poprawia posty w narzędziu na http://localhost:8030 albo prosząc Claude; poprawki trafiają do dziennika i uczą reguły. Reaguje na "/posty-social", "posty na LinkedIn", "posty social do wydania".
---

Etap po wydaniu (po `/zakoncz-wydanie`, osobny). Argument: numer wydania; bez niego — ostatni katalog
w `wydania/`. Wszystkie pliki: `wydania/NNN/social/` (opis w `narzedzia/social/posty.py`).
**Nic nie publikujesz** — publikuje Kuba ręcznie.

## Krok 0 — Stan

```bash
ls wydania/<NNN>/social/ 2>/dev/null; ls .cache/social/<NNN>/zadania/ 2>/dev/null
```

- Jest `posty.json` → to powrót do wydania (poprawki, nowe tematy, wyniki po publikacji). Ustaw w nim
  `"status": "robocze"` (żeby pętla z kroku 4 nie skończyła się od razu), pomiń kroki 1–2,
  uruchom narzędzie (krok 3) i obsłuż kolejkę (krok 4).
- Nie ma → zacznij od kroku 1.

## Krok 1 — Przeczytaj

- `wydania/<NNN>/meta.json` (tytuł, wstęp, slug) i `wydania/<NNN>/dane.csv` (wszystkie newsy z opisami),
- `redakcja/social.md`, `redakcja/social-platformy.md`, `redakcja/o-mnie.md` — zwłaszcza „Uwagi Kuby”
  i „Przykłady poprawek”,
- `wydania/*/social/posty.json` z 2 poprzednich wydań (jeśli są) — żeby nie powtarzać tematów i otwarć.

URL wydania: `https://przegladai.substack.com/p/<slug>`.

## Krok 2 — Propozycje tematów i post główny

**Tematy** → `wydania/<NNN>/social/tematy_ai.json` (wersja AI — potem jej nie zmieniasz):

```json
{"numer": 44, "tematy": [
  {"id": "t1", "link": "...", "tytul_newsa": "...", "kat": "co Kuba ma do powiedzenia (1 zdanie)",
   "dlaczego": "czemu zadziała u odbiorców (1 zdanie)", "rekomendowany": true}]}
```

6–8 tematów według „Wybór tematów” w `social.md`, dokładnie 3 z `"rekomendowany": true`.
Link i tytuł newsa przepisz dokładnie z `dane.csv`.

**Post główny** — napisz sam (bez subagenta) według „Rodzaje postów” w `social.md`, na bazie `wstep`
z `meta.json`, i zapisz do `.cache/social/<NNN>/robocze/glowny.json` w formacie z `.claude/agents/social-autor.md`,
z `"id": "glowny"`, `"rodzaj": "glowny"`, `"temat": "Wstęp wydania"`, `"obrazek": {"wybrany": "okladka"}`
(+ opcjonalnie infografika z najmocniejszą liczbą tygodnia), `"termin"`: data wydania z `meta.json`, 08:30.
Potem:

```bash
python3 narzedzia/social/posty.py scal <NNN>
python3 narzedzia/social/posty.py sprawdz <NNN>
```

Popraw błędy w `posty_ai.json` i `posty.json` (obu — to jeszcze wersja AI) i sprawdź ponownie.

## Krok 3 — Narzędzie

```bash
curl -s http://localhost:8030/api/stan >/dev/null || (python3 narzedzia/social/przeglad/server.py --numer <NNN> &)
```

(w tle, `run_in_background`). Napisz Kubie krótko: narzędzie na http://localhost:8030, tam zaznacza tematy
(polecane są zaznaczone; może wybrać więcej i dopisać wskazówkę) i klika „Generuj posty”. Wypisz w terminalu
listę tematów z kątami.

## Krok 4 — Kolejka (pętla)

Narzędzie wrzuca prośby do `.cache/social/<NNN>/zadania/*.json`. Czekaj na nie Monitorem:

```bash
until ls .cache/social/<NNN>/zadania/ 2>/dev/null | grep -q '\.json$' || grep -q '"status": "gotowe"' wydania/<NNN>/social/posty.json 2>/dev/null; do sleep 3; done
```

Obsłuż wszystkie pliki w kolejności nazw, każdy usuń dopiero po obsłużeniu, i wróć do czekania:

**`"rodzaj": "generuj"`** — lista tematów `{id, link, tytul_newsa, kat, wskazowka, z_propozycji_ai}`.
Terminy: według harmonogramu z `social-platformy.md` — kolejne wolne dni wt/śr/czw po dacie wydania
(sprawdź terminy zajęte w `posty.json`; tematy polecane dostają najwcześniejsze), dalsze — kolejne dni robocze.
Uruchom **równolegle** po jednym subagencie `social-autor` na temat (jedna wiadomość, wiele wywołań Agent).
Prompt: numer wydania, URL wydania, dane tematu + opis newsa z `dane.csv`, termin, ścieżka wyniku
`.cache/social/<NNN>/robocze/<id>.json`. Potem `posty.py scal <NNN>` i `posty.py sprawdz <NNN>`;
błędy popraw w obu plikach (nowe posty to wciąż wersja AI). Narzędzie wczyta posty samo.
Na koniec **weryfikacja faktów** (krok 4a) dla nowych postów.

**`"rodzaj": "popraw"`** — `{post, prosba}`: Kuba prosi o zmianę posta. Popraw post **tylko w `posty.json`**
(nigdy `posty_ai.json` — różnica to nauka) i dopisz do jego `uwaga_kuby` linię `[prośba] <treść prośby>`.
Drobna zmiana — edytuj sam. Przepisanie posta — subagent `social-autor` z prośbą Kuby i ścieżką
`.cache/social/<NNN>/poprawki/<id>.json`, potem `posty.py podmien <NNN>` (zachowuje pola Kuby) — dopiero
gdy subagent **skończył** (potrafi nadpisać plik kilka razy, zanim odda wynik). To samo dotyczy `scal`.
Gdy prośba dotyczy infografiki — zmień `obrazek.infografika` i uruchom `posty.py grafiki <NNN>`.
Po zapisie: `posty.py sprawdz <NNN>`.

**Poprawki w czacie.** Kuba często pisze uwagi w czacie (także dyktowane, luźno, do kilku postów naraz).
Traktuj je jak `popraw`: edycja tylko `posty.json` + w `uwaga_kuby` danego posta linia `[czat] <jego uwaga
jego słowami>`. Gdy Kuba podaje **własne brzmienie** („ja bym napisał: …”), to jest wersja docelowa —
wstaw ją dosłownie (popraw tylko literówki z dyktowania), nie „ulepszaj”. Gdy opisuje, o co mu chodzi
(„bardziej pod to, że…”), przepisz post (subagent `social-autor` z jego uwagami dosłownie) i pokaż w narzędziu.
Ogólne uwagi z czatu (dotyczące wszystkich postów albo infografik) zapisz od razu do dziennika jako wpis
`{"etap": "social", "rodzaj": "uwaga", "pole": "ogolne" | "infografika", "kuba": "<jego słowa>"}`
(`python3 -c "import sys; sys.path.insert(0,'narzedzia'); import dziennik; dziennik.append([...])"`),
a wyraźne uwagi od razu zamień na reguły w `redakcja/social*.md` (+ wpis w `zmiany-regul.md`) — następne posty
mają je już uwzględniać. Gdy prośba zmienia fakty w poście — po poprawce zweryfikuj go ponownie (krok 4a).

### Krok 4a — Weryfikacja faktów

Po każdym napisaniu albo przepisaniu posta uruchom **równolegle** po jednym subagencie `social-weryfikator`
na post (numer wydania, id posta, wynik do `.cache/social/<NNN>/weryfikacja/<id>.json`), a potem:

```bash
python3 narzedzia/social/posty.py weryfikacja <NNN>
```

Narzędzie pokazuje przy poście listę faktów (✓ / ✗ / ?), cytat ze źródła i link „pokaż w źródle” prowadzący
do podświetlonego fragmentu. Rozbieżności popraw od razu w `posty.json` (to poprawka faktów, nie stylu —
dopisz w `uwaga_kuby` linię `[weryfikacja] …`, żeby `ucz-sie` nie brał jej za preferencję Kuby) i zweryfikuj
post ponownie. Kubie wypisz tylko to, czego nie dało się potwierdzić.

Status `gotowe` → krok 5. Gdy Kuba w czacie powie, że posty mu pasują („podoba mi się ten stan”) —
ustaw `"status": "gotowe"` w `posty.json` sam i przejdź do kroku 5.

## Krok 5 — Zakończenie i nauka

```bash
python3 narzedzia/social/posty.py eksport <NNN>
python3 narzedzia/dziennik.py social <NNN>
```

Potem uruchom skill `ucz-sie` (sam, bez pytania). Na koniec podaj Kubie:
- `wydania/<NNN>/social/posty.md` — posty do publikacji z terminami, w kolejności,
- przypomnienie: link wklejać w pierwszym komentarzu, obrazki w `wydania/<NNN>/social/obrazki/`,
- 2–4 punkty z `ucz-sie`: czego nauczyły się reguły.

Narzędzie zostaw włączone, jeśli Kuba chce jeszcze coś poprawić; inaczej
`curl -s -X POST http://localhost:8030/api/shutdown`.

**Wyniki po publikacji**: gdy Kuba wróci (`/posty-social <NNN>`) i wpisze wyniki w narzędziu, a potem kliknie
„Zakończ i ucz” — `dziennik.py social` dopisze je jako wpisy `wynik` (tylko nowe), a `ucz-sie` porówna, które
posty działały (haczyk, obrazek, temat, dzień).

## Git

Pliki: `wydania/<NNN>/social/` i zmienione `redakcja/*`. Jeśli PR wydania (`issue-<nr>`) nie jest jeszcze
scalony — commit na tym branchu. Jeśli scalony — branch `social-<nr>` i PR bez `/schedule`.
Zanim zrobisz commit, zapytaj Kubę (to osobny etap; czasem chce najpierw opublikować posty).
