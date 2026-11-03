# Posty social — jak działa cały proces

Osobny etap po wydaniu: `/posty-social [nr]` (skill `.claude/skills/posty-social/SKILL.md` — instrukcja dla Claude).
Ten plik opisuje przepływ dla człowieka. Publikacja zawsze ręczna.

## Przepływ

```
/posty-social 44
  │
  ├─ 1. Claude czyta wydanie (meta.json, dane.csv) i reguły (redakcja/social.md, social-platformy.md, o-mnie.md)
  ├─ 2. Propozycje: 6–8 tematów z kątem i uzasadnieniem (3 polecane) → tematy_ai.json
  │                 post główny ze wstępu wydania (piątek, okładka, link w komentarzu)
  ├─ 3. Narzędzie http://localhost:8030 — Kuba zaznacza tematy (dowolnie dużo, też spoza propozycji, z wskazówką)
  │                 i klika „Generuj posty” → wybor.json + zadanie w kolejce .cache/social/NNN/zadania/
  ├─ 4. Claude: po jednym subagencie social-autor na temat (równolegle) → LinkedIn (+FB, Substack Notes),
  │             wątek X, infografika + prompt do zdjęcia, termin (wt/śr/czw) → posty_ai.json (wersja AI) i posty.json
  ├─ 4a. Weryfikacja: po jednym subagencie social-weryfikator na post — każdy fakt sprawdzony w źródle,
  │             cytat + link „pokaż w źródle” (#:~:text=…). Rozbieżności Claude poprawia od razu ([weryfikacja]).
  ├─ 5. Poprawki Kuby (dowolna kolejność, dowolnie wiele razy) — zawsze tylko w posty.json:
  │       • edycja w narzędziu (zapis automatyczny), wybór obrazka i stylu infografiki, „publikuję”, termin,
  │       • „Uwaga dla AI” przy poście — co się podoba / nie podoba,
  │       • „Wyślij do Claude” przy poście — prośba o poprawkę przez kolejkę,
  │       • w czacie, swoimi słowami — uwagi do jednego posta, do wszystkich albo do infografik;
  │         własne brzmienie zdania = wersja docelowa, wstawiana dosłownie.
  │     Ogólne uwagi trafiają od razu do dziennika i do reguł (następne posty już je uwzględniają).
  ├─ 6. „Zakończ i ucz” w narzędziu (albo „pasuje mi” w czacie) → posty.md do kopiowania,
  │      dziennik.py social → redakcja/dziennik/poprawki.jsonl, skill ucz-sie → reguły w redakcja/
  └─ 7. Po publikacji (opcjonalnie): /posty-social 44 → wyniki (wyświetlenia, reakcje) w narzędziu → znów 6.
```

## Co się uczy i skąd

| Sygnał | Skąd | Uczy |
|---|---|---|
| tematy wybrane / pominięte / dodane | `tematy_ai.json` vs `wybor.json` | „Wybór tematów” w `social.md` |
| zmiany tekstów, wątku X, komentarza, terminu | `posty_ai.json` vs `posty.json` | styl w `social.md`, `social-platformy.md` |
| obrazek i styl infografiki | `obrazek.wybrany`, `infografika.styl` | „Obrazki” w `social.md` |
| uwagi i prośby (`[czat]`, `[prośba]`) | `uwaga_kuby`, wpisy `uwaga` w dzienniku | reguły wprost |
| poprawki faktów (`[weryfikacja]`) | `uwaga_kuby` | nie są preferencją stylu — tylko dokładność |
| wyniki po publikacji | `wynik` | `social-platformy.md` (dopiero przy 6+ postach) |

Sekcje „Uwagi Kuby” w `redakcja/*.md` edytuje tylko Kuba.

## Pliki

- `wydania/NNN/social/` — `tematy_ai.json`, `wybor.json`, `posty_ai.json` (nie zmieniamy), `posty.json`,
  `posty.md`, `obrazki/` (archiwum, w repo)
- `.cache/social/NNN/` — kolejka zadań, robocze pliki subagentów, wyniki weryfikacji (poza repo)
- `narzedzia/social/posty.py` — `scal`, `podmien`, `sprawdz`, `grafiki`, `weryfikacja`, `eksport`
- `narzedzia/social/grafika.py` — infografiki (`liczba`, `porownanie`, `lista`, `cytat`; style `notatka`, `minimal`)
- `narzedzia/social/przeglad/` — narzędzie webowe
- `.claude/agents/social-autor.md`, `.claude/agents/social-weryfikator.md` — subagenci
- `narzedzia/dziennik.py social <nr>` — zapis poprawek do dziennika (można uruchamiać wielokrotnie)

## Test na #44 (2026-11-02)

Pierwsze uruchomienie: 4 posty (główny, rekrutacja/LeetCode, juniorzy, prospekt IPO Anthropic).
Uwagi Kuby z czatu zmieniły reguły (budowa haczyk → wstęp → rozwinięcie → zakończenie, pełne zdania zamiast
„statementów”, bez mocnych tez i hashtagów) i wygląd infografik (style `notatka` / `minimal` zamiast szablonu).
Weryfikacja znalazła 6 rozbieżności (m.in. „ponad 50 mld $ kwartalnie na AI” → prognoza capex za jeden kwartał).
