#!/usr/bin/env python3
"""Krok 1 /zbierz-dane: data.csv -> praca/linki.json

Wyciaga linki z data.csv (dowolny format, byle URL-e), usuwa smieci i parametry
sledzace, rozwija przekierowania trackerow, usuwa duplikaty oraz linki, ktore byly
juz w poprzednich wydaniach. Dzieli wynik na paczki dla subagentow.

Uzycie:
    python3 narzedzia/przygotuj_linki.py [data.csv] [--paczka 10]
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import repo  # noqa: E402
from lib.urlclean import clean_url, dedup_key, extract_urls, looks_like_redirect, resolve_redirect  # noqa: E402

# Linki, ktore nigdy nie sa newsami (skrzynka, logowanie, udostepnianie).
JUNK_HOSTS = ('mail.google.com', 'accounts.google.com', 'calendar.google.com', 'drive.google.com',
              'docs.google.com', 'substack.com/redirect', 'localhost')
JUNK_PATH_PARTS = ('/unsubscribe', '/manage-preferences', '/share', '/intent/', '/sharer',
                   '/login', '/signup', '/subscribe')


def junk_reason(url):
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    low = url.lower()
    if not host:
        return 'brak-domeny'
    for junk in JUNK_HOSTS:
        if junk in low:
            return 'smieci:%s' % junk
    for part in JUNK_PATH_PARTS:
        if part in (parsed.path or '').lower():
            return 'nawigacja:%s' % part
    if (parsed.path or '/') in ('', '/') and not parsed.query:
        return 'strona-glowna'
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('plik', nargs='?', default=os.path.join(repo.ROOT, 'data.csv'))
    parser.add_argument('--paczka', type=int, default=10)
    args = parser.parse_args()

    if not os.path.exists(args.plik):
        raise SystemExit('Brak pliku %s' % args.plik)
    with open(args.plik, encoding='utf-8') as f:
        content = f.read()
    raw_urls = extract_urls(content)
    # kopia wejscia: zakoncz-wydanie usunie z data.csv tylko te linie, ktore tu przetworzylismy
    os.makedirs(repo.PRACA, exist_ok=True)
    with open(repo.DATA_WEJSCIE, 'w', encoding='utf-8') as f:
        f.write(content)

    rejected = []
    urls = []
    for url in raw_urls:
        reason = junk_reason(url)
        if reason:
            rejected.append((url, reason))
        else:
            urls.append(url)

    to_resolve = sorted({u for u in urls if looks_like_redirect(u)})
    if to_resolve:
        print('Rozwijam przekierowania: %d' % len(to_resolve), file=sys.stderr)
        with ThreadPoolExecutor(12) as pool:
            resolved = dict(zip(to_resolve, pool.map(resolve_redirect, to_resolve)))
        urls = [resolved.get(u, u) for u in urls]

    published = {dedup_key(u) for u in repo.published_links()}
    seen = set()
    unique = []
    for url in urls:
        url = clean_url(url)
        key = dedup_key(url)
        if key in published:
            rejected.append((url, 'bylo-w-wydaniu'))
            continue
        if key in seen:
            rejected.append((url, 'duplikat'))
            continue
        reason = junk_reason(url)
        if reason:
            rejected.append((url, reason))
            continue
        seen.add(key)
        unique.append(url)

    batches = [unique[i:i + args.paczka] for i in range(0, len(unique), args.paczka)]
    repo.write_json(repo.LINKI, {
        'linki': unique,
        'paczki': [{'id': '%02d' % (i + 1), 'linki': b} for i, b in enumerate(batches)],
        'odrzucone': [{'link': u, 'powod': r} for u, r in rejected],
    })

    print('Linkow w pliku: %d, do opisania: %d, odrzuconych: %d, paczek: %d'
          % (len(raw_urls), len(unique), len(rejected), len(batches)))
    for url, reason in rejected:
        print('  - %s  (%s)' % (url[:100], reason))
    print('Zapisano: %s' % os.path.relpath(repo.LINKI, repo.ROOT))


if __name__ == '__main__':
    main()
