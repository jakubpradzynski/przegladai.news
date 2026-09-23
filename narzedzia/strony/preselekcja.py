#!/usr/bin/env python3
"""Preselekcja wpisow ze stron: przygotowanie danych dla subagenta i sprawdzenie jego wyniku.

    przygotuj  .cache/strony/wynik.json (+ przegladarka.json) -> .cache/strony/do_oceny.json
               Kazdy wpis dostaje id; do tego statystyka strony i ostatnie decyzje Kuby
               z redakcja/dziennik/strony_wybory.jsonl (przyklady wzietych i pominietych).
    sprawdz    .cache/strony/preselekcja.json (wynik subagenta preselektor) - czy kazdy wpis
               ma ocene tak/moze/nie i powod. Kod wyjscia 1, gdy czegos brakuje.

Uzycie:
    python3 narzedzia/strony/preselekcja.py przygotuj
    python3 narzedzia/strony/preselekcja.py sprawdz
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, 'przeglad'))

from lib import repo  # noqa: E402

CACHE = os.path.join(repo.ROOT, '.cache', 'strony')
DO_OCENY = os.path.join(CACHE, 'do_oceny.json')
PRESELEKCJA = os.path.join(CACHE, 'preselekcja.json')
WYBORY = os.path.join(repo.REDAKCJA, 'dziennik', 'strony_wybory.jsonl')
PRZYKLADY_NA_STRONE = 12


def history():
    stats = collections.defaultdict(lambda: {'wziete': 0, 'wszystkie': 0})
    examples = collections.defaultdict(list)
    if os.path.exists(WYBORY):
        with open(WYBORY, encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                if entry['kuba'] == 'niewidziany':
                    continue
                site = stats[entry['strona']]
                site['wszystkie'] += 1
                site['wziete'] += entry['kuba'] == 'wziety'
                examples[entry['strona']].append(entry)
    return stats, examples


def cmd_przygotuj(_args):
    import server  # wczytanie wyniku razem z wpisami z przegladarki
    result = server.load(with_preselection=False)
    stats, examples = history()
    items, sites = [], {}
    for site in result['strony']:
        if not site['nowe']:
            continue
        past = examples.get(site['nazwa'], [])
        taken = [e['tytul'] for e in past if e['kuba'] == 'wziety'][-PRZYKLADY_NA_STRONE:]
        skipped = [e['tytul'] for e in past if e['kuba'] == 'pominiety'][-PRZYKLADY_NA_STRONE:]
        sites[site['nazwa']] = {'historia': stats.get(site['nazwa'], {'wziete': 0, 'wszystkie': 0}),
                                'ostatnio_wziete': taken, 'ostatnio_pominiete': skipped}
        for item in site['nowe']:
            if item.get('w_data_csv') or item.get('opublikowany'):
                continue
            items.append({'id': item['link'], 'strona': site['nazwa'], 'data': item['data'],
                          'tytul': item['tytul'], 'opis': item.get('opis', '')[:300]})
    repo.write_json(DO_OCENY, {'od': result['od'], 'strony': sites, 'wpisy': items})
    print('Do oceny: %d wpisów z %d stron -> %s' % (len(items), len(sites), os.path.relpath(DO_OCENY, repo.ROOT)))


def cmd_sprawdz(_args):
    todo = repo.read_json(DO_OCENY)
    done = repo.read_json(PRESELEKCJA)
    if not todo or done is None:
        raise SystemExit('Brak do_oceny.json albo preselekcja.json')
    by_id = {d['id']: d for d in done}
    missing = [i['id'] for i in todo['wpisy'] if i['id'] not in by_id]
    bad = [d['id'] for d in done if d.get('ocena') not in ('tak', 'moze', 'nie') or not d.get('powod')]
    counts = collections.Counter(d.get('ocena') for d in done)
    print('Ocenione: %d/%d (tak %d, może %d, nie %d)' % (len(done), len(todo['wpisy']),
                                                        counts['tak'], counts['moze'], counts['nie']))
    for ident in missing:
        print('  brak oceny: %s' % ident)
    for ident in bad:
        print('  zła ocena albo brak powodu: %s' % ident)
    if missing or bad:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='polecenie', required=True)
    sub.add_parser('przygotuj').set_defaults(func=cmd_przygotuj)
    sub.add_parser('sprawdz').set_defaults(func=cmd_sprawdz)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
