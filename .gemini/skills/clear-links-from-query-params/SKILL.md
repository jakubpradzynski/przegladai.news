---
id: clear-links-from-query-params
name: Clear links from query params
description: Usuwa query parametry z linków w podanym pliku
---

# Kroki

1. Wczytaj podany plik
2. Usuń query parametry z linków
3. Zapisz zmiany w pliku `cleaned_...`

# Wytyczne

- Nie zmieniaj linków w żaden inny sposób niż usunięcie query parametrów
- Zachowaj kolejność linków
- Zachowaj format pliku
- Jeżeli na końcu linku jest `#` z tekstem po nim, ten tekst powinien zostać w linku

# Jakie query parametry usuwać

- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_term`
- `utm_content`
- `_bhlid`
- `lid`
- `r`
- `triedRedirect`
- `IR`
- `isFreemail`
- `mod`
- `module`
- `pgtype`
- `post_id`
- `publication_id`
- `reflink`
- `s`