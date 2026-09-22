# Źródła: wiedza techniczna

Uzupełniane automatycznie przy pracy. Każdy wpis z datą.

## Uwagi Kuby

_(miejsce na Twoje uwagi — AI tej sekcji nie zmienia)_

## Strony, które trzeba otwierać w przeglądarce

Zwykłe pobranie (WebFetch) nie zwraca treści — od razu Chrome:
- x.com, twitter.com, linkedin.com — zawsze
- youtube.com — opis i długość przez skill `youtube-watcher` (napisy), tytuł/czas w razie potrzeby przez Chrome

## Paywalle

Zwykle za paywallem (tag `Za paywallem`, gdy kluczowa część jest płatna):
- newsletter.pragmaticengineer.com — deep dives płatne, „The Pulse” częściowo
- newsletter.eng-leadership.com — część wydań płatna
- wsj.com, forbes.com, bloomberg.com, theinformation.com, ft.com
- reuters.com — czasem

## Trackery w linkach z newsletterów

Rozwijane przez `narzedzia/lib/urlclean.py` (`resolve_redirect`). Substack w mailach
używa bramek z `meta refresh`, beehiiv i TLDR — zwykłych przekierowań HTTP.

## Newslettery (skrzynka przegladai.news)

Raport skuteczności nadawców: `narzedzia/newslettery/` (skill `porzadki-newsletterow`).
