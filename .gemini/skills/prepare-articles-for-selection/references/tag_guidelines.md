# Wytyczne wyboru Tagów oraz ustalania Czasu

Do wygenerowania pliku CSV potrzebne są kolumny "Tagi" oraz "Czas". Przestrzegaj bezwzględnie poniższych zasad.

## Tagi
Tagi służą do skategoryzowania zawartości pod danym linkiem.
1. Możesz wybrać **TYLKO** tagi z poniższej krótkiej listy. Żadne inne (np. nazwy firm, technologie) nie są dozwolone.
2. Link może mieć kilka pasujących tagów, ale `Bliżej technologii` i `Nowości i ogłoszenia` nie mogą być używane razem. Wybierz ten, który lepiej pasuje do treści.
3. W przypadku użycia wielu tagów, oddziel je przecinkiem i spacją, i koniecznie **posortuj je alfabetycznie**.
4. Nie wszystkie linki muszą mieć tagi! Jeśli nie pasuje do żadnej kategorii, zostaw pole puste.

**Dozwolona i zamknięta lista tagów:**
- `Bliżej technologii`: Materiały techniczne dla ludzi z branży IT (developerów, inżynierów ML, PMów itp.).
- `Nowości i ogłoszenia`: Informacje o premierach, nowościach w narzędziach, przejęciach firm i ważnych ogłoszeniach w świecie AI.
- `Polska`: Treść dotyczy bezpośrednio Polski jako kraju, projektów polskiego pochodzenia lub nowości z polskiego rynku.

*Przykład formatowania wielu tagów (jeśli pasują do siebie):* `Bliżej technologii, Polska`

## Czas
To pole ma zastosowanie **wyłącznie** dla wideo (np. YouTube, Vimeo) lub materiałów audio.
1. Czas powinien być wyciągnięty ze strony i zapisany w formie tekstowej podającej same godziny i/lub minuty, w zaokrągleniu do minuty w dół.
2. Ignoruj sekundy.
3. Przykłady dozwolonego formatowania: `2 min`, `59 min`, `1h`, `1h 10 min`, `2h 15 min`.
4. Jeżeli link odsyła do standardowego artykułu tekstowego, repozytorium na GitHub, tweeta w mediach społecznościowych lub oficjalnej notatki prasowej – pole `Czas` musi być w 100% **puste** (bez wpisywania "Brak" itp.).
