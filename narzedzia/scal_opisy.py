#!/usr/bin/env python3
"""Krok 3 /zbierz-dane: praca/opisy/*.json -> praca/prepared_data.csv

Scala opisy przygotowane przez subagentow, waliduje je wedlug redakcja/*.md,
wylicza sekcje i rekomendacje (TOP / rezerwa) wedlug redakcja/priorytety.md
i zapisuje:
    praca/prepared_data.csv  - wejscie adminki
    praca/wersja_ai.csv      - nietykalna kopia wersji AI (do porownania z selekcja)

Kod wyjscia 1, gdy sa problemy walidacji - trzeba je poprawic w praca/opisy/*.json
i uruchomic skrypt ponownie.

Uzycie:
    python3 narzedzia/scal_opisy.py [--na-sekcje 10] [--bez-walidacji]
"""
import argparse
import collections
import glob
import json
import os
import shutil
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import repo, walidacja  # noqa: E402
from lib.urlclean import dedup_key  # noqa: E402

MAX_PER_DOMAIN = 3
MAX_PAYWALL = 2
MIN_SCORE = 5


def domain(url):
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith('www.') else host


def recommend(rows, per_section):
    """TOP dla najlepszych w kazdej sekcji, z limitami domen i paywalla."""
    for row in rows:
        row['Rekomendacja'] = 'rezerwa'
    ranked = sorted(rows, key=lambda r: -int(r['Ocena']))
    per_domain = collections.Counter()
    taken = collections.Counter()
    paywall = 0

    def allowed(row):
        dom = domain(row['Link'])
        if row.get('Duplikat'):
            return False
        if dom not in ('youtube.com', 'youtu.be') and per_domain[dom] >= MAX_PER_DOMAIN:
            return False
        if 'Za paywallem' in row['Tagi'] and paywall >= MAX_PAYWALL:
            return False
        return int(row['Ocena']) >= MIN_SCORE

    def take(row):
        nonlocal paywall
        row['Rekomendacja'] = 'TOP'
        per_domain[domain(row['Link'])] += 1
        taken[row['Sekcja']] += 1
        if 'Za paywallem' in row['Tagi']:
            paywall += 1

    for row in ranked:
        if taken[row['Sekcja']] < per_section and allowed(row):
            take(row)
    # wolne miejsca z sekcji, ktorym zabraklo dobrych kandydatow
    free = per_section * len(repo.SECTIONS) - sum(taken.values())
    for row in ranked:
        if free <= 0:
            break
        if row['Rekomendacja'] == 'rezerwa' and allowed(row):
            take(row)
            free -= 1
    return taken


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--na-sekcje', type=int, default=10)
    parser.add_argument('--bez-walidacji', action='store_true',
                        help='zapisz mimo problemow (np. gdy czegos nie da sie poprawic)')
    args = parser.parse_args()

    links = repo.read_json(repo.LINKI, {}).get('linki', [])
    items = {}
    for path in sorted(glob.glob(os.path.join(repo.OPISY_DIR, '*.json'))):
        with open(path, encoding='utf-8') as f:
            for item in json.load(f):
                items[dedup_key(item['Link'])] = item

    missing = [l for l in links if dedup_key(l) not in items]
    phrases = walidacja.banned_phrases()
    problems = {}
    rows = []
    for item in items.values():
        if item.get('Pominac'):
            continue
        row = {k: str(item.get(k, '') or '').strip() for k in repo.AI_FIELDS}
        row['Duplikat'] = str(item.get('Duplikat', '') or '').strip()
        found = walidacja.check(row, phrases)
        if found:
            problems[row['Link']] = found
        row['Sekcja'] = repo.section_for(row['Tagi'])
        if row['Duplikat'] and 'duplikat' not in row['Uzasadnienie'].lower():
            row['Uzasadnienie'] = (row['Uzasadnienie'] + ' (duplikat: %s)' % row['Duplikat']).strip()
        rows.append(row)

    if missing:
        print('Brak opisow dla %d linkow:' % len(missing))
        for link in missing:
            print('  - %s' % link)
    if problems:
        print('Problemy walidacji (%d newsow):' % len(problems))
        for link, found in problems.items():
            print('  - %s\n      %s' % (link, '; '.join(found)))
    if (problems or missing) and not args.bez_walidacji:
        print('\nPopraw praca/opisy/*.json i uruchom ponownie (albo --bez-walidacji).')
        sys.exit(1)

    for row in rows:
        row['Ocena'] = row['Ocena'] if row['Ocena'].isdigit() else '0'
    taken = recommend(rows, args.na_sekcje)

    order = {s: i for i, s in enumerate(repo.SECTIONS)}
    rows.sort(key=lambda r: (order[r['Sekcja']], r['Rekomendacja'] != 'TOP', -int(r['Ocena'])))
    repo.write_csv(repo.PREPARED, rows, repo.AI_FIELDS)
    shutil.copyfile(repo.PREPARED, repo.WERSJA_AI)
    for path in (repo.ROBOCZY, repo.FINAL):
        if os.path.exists(path):
            os.remove(path)

    counts = collections.Counter(r['Sekcja'] for r in rows)
    print('Zapisano %d newsow -> %s' % (len(rows), os.path.relpath(repo.PREPARED, repo.ROOT)))
    for section in repo.SECTIONS:
        print('  %-12s kandydatow %2d, TOP %2d' % (section, counts[section], taken[section]))
    print('  Polska: %d, wideo: %d, paywall: %d' % (
        sum('Polska' in r['Tagi'] for r in rows if r['Rekomendacja'] == 'TOP'),
        sum(bool(r['Czas']) for r in rows if r['Rekomendacja'] == 'TOP'),
        sum('Za paywallem' in r['Tagi'] for r in rows if r['Rekomendacja'] == 'TOP')))


if __name__ == '__main__':
    main()
