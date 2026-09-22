#!/usr/bin/env python3
"""Dziennik poprawek: redakcja/dziennik/poprawki.jsonl

Kazda roznica miedzy tym, co wygenerowalo AI, a tym, co ostatecznie zostalo
(po poprawkach Kuby), trafia do dziennika jako jeden wpis JSON. Plik tylko rosnie.

Polecenia:
    selekcja        praca/wersja_ai.csv  vs praca/final_prepared_data.csv
    wydanie         praca/wydanie_ai.json vs praca/wydanie.json (tytul, wstep, SEO, slug, okladka)
    substack <nr>   wydania/NNN/ vs post opublikowany na Substacku (poprawki zrobione juz w edytorze)
    nowe            wypisuje wpisy jeszcze nieprzetworzone przez ucz-sie
    oznacz          oznacza wszystkie wpisy jako przetworzone
"""
import argparse
import html
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import repo  # noqa: E402
from lib.urlclean import dedup_key  # noqa: E402

STAN = os.path.join(os.path.dirname(repo.DZIENNIK), 'stan.json')
SUBSTACK_API = 'https://przegladai.substack.com/api/v1/posts/%s'
FIELDS = ['Tytuł', 'Opis', 'Tagi', 'Czas']


def norm(text):
    """Porownanie odporne na typografie wprowadzana przez Substacka."""
    text = html.unescape(text or '')
    for a, b in (('’', "'"), ('‘', "'"), ('\xa0', ' '), ('“', '"'), ('”', '"'), ('„', '"')):
        text = text.replace(a, b)
    return ' '.join(text.split())


def append(entries):
    if not entries:
        return 0
    os.makedirs(os.path.dirname(repo.DZIENNIK), exist_ok=True)
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(repo.DZIENNIK, 'a', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(dict({'data': stamp}, **entry), ensure_ascii=False) + '\n')
    return len(entries)


def current_issue():
    meta = repo.read_json(repo.WYDANIE, {}) or repo.read_json(repo.WYDANIE_AI, {})
    if meta.get('numer'):
        return meta['numer']
    last = repo.last_issue()
    return (last['numer'] + 1) if last else None


def cmd_selekcja(_args):
    if not (os.path.exists(repo.WERSJA_AI) and os.path.exists(repo.FINAL)):
        raise SystemExit('Brak praca/wersja_ai.csv albo praca/final_prepared_data.csv')
    ai_rows = {dedup_key(r['Link']): r for r in repo.read_csv(repo.WERSJA_AI)}
    final_rows = repo.read_csv(repo.FINAL)
    final_keys = set()
    issue = current_issue()
    entries = []

    for pos, row in enumerate(final_rows, 1):
        key = dedup_key(row['Link'])
        final_keys.add(key)
        ai = ai_rows.get(key)
        if ai is None:
            entries.append({'wydanie': issue, 'etap': 'selekcja', 'rodzaj': 'dodany_przez_kube',
                            'link': row['Link'], 'kuba': {k: row.get(k, '') for k in FIELDS}})
            continue
        context = {'sekcja_ai': ai.get('Sekcja'), 'ocena_ai': ai.get('Ocena'),
                   'uzasadnienie_ai': ai.get('Uzasadnienie'), 'tytul': row['Tytuł']}
        if ai.get('Rekomendacja') != 'TOP':
            entries.append({'wydanie': issue, 'etap': 'selekcja', 'rodzaj': 'wybrany_z_rezerwy',
                            'link': row['Link'], 'kontekst': context})
        for field in FIELDS:
            if norm(ai.get(field)) != norm(row.get(field)):
                entries.append({'wydanie': issue, 'etap': 'selekcja', 'rodzaj': 'zmiana',
                                'pole': field, 'link': row['Link'], 'ai': ai.get(field, ''),
                                'kuba': row.get(field, ''), 'kontekst': context})

    for key, ai in ai_rows.items():
        if key in final_keys or ai.get('Rekomendacja') != 'TOP':
            continue
        entries.append({'wydanie': issue, 'etap': 'selekcja', 'rodzaj': 'odrzucony_top',
                        'link': ai['Link'],
                        'kontekst': {'tytul': ai['Tytuł'], 'tagi': ai['Tagi'], 'sekcja_ai': ai['Sekcja'],
                                     'ocena_ai': ai['Ocena'], 'uzasadnienie_ai': ai['Uzasadnienie']}})

    ai_order = [dedup_key(r['Link']) for r in repo.read_csv(repo.WERSJA_AI) if r['Rekomendacja'] == 'TOP']
    entries.append({'wydanie': issue, 'etap': 'selekcja', 'rodzaj': 'podsumowanie',
                    'kontekst': {'kandydatow_ai': len(ai_rows), 'top_ai': len(ai_order),
                                 'wybranych': len(final_rows),
                                 'top_zachowanych': len(final_keys & set(ai_order))}})
    print('Dopisano do dziennika: %d wpisow' % append(entries))


def cmd_wydanie(_args):
    ai = repo.read_json(repo.WYDANIE_AI)
    final = repo.read_json(repo.WYDANIE)
    if not ai or not final:
        raise SystemExit('Brak praca/wydanie_ai.json albo praca/wydanie.json')
    issue = final.get('numer')
    entries = []
    proposals = ai.get('propozycje_tytulu', [])
    if final.get('tytul') in proposals:
        entries.append({'wydanie': issue, 'etap': 'wydanie', 'rodzaj': 'wybrany_tytul',
                        'pole': 'tytul', 'kuba': final['tytul'],
                        'kontekst': {'propozycje': proposals, 'wybrana': proposals.index(final['tytul']) + 1}})
    elif final.get('tytul'):
        entries.append({'wydanie': issue, 'etap': 'wydanie', 'rodzaj': 'zmiana', 'pole': 'tytul',
                        'ai': proposals, 'kuba': final['tytul']})
    # slug i napis na okladce same podazaja za wybranym tytulem - to nie sa poprawki
    derived = {'slug': repo.issue_slug(issue, final.get('tytul', '')),
               'okladka': re.sub(r'^\s*Wydanie\s*', '', final.get('tytul', ''))}
    for field in ('wstep', 'opis_seo', 'slug', 'okladka'):
        if field in derived and norm(final.get(field)) == norm(derived[field]):
            continue
        if norm(ai.get(field)) != norm(final.get(field)):
            entries.append({'wydanie': issue, 'etap': 'wydanie', 'rodzaj': 'zmiana', 'pole': field,
                            'ai': ai.get(field, ''), 'kuba': final.get(field, '')})
    print('Dopisano do dziennika: %d wpisow' % append(entries))


def parse_published(body):
    """Wstep i newsy z HTML-a posta na Substacku (ten sam uklad co nasz substack.html)."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(body, 'html.parser')
    intro = []
    for el in soup.find_all(['p', 'h3', 'hr']):
        if el.name in ('h3', 'hr'):
            break
        text = el.get_text(' ', strip=True)
        if text and text not in ('Cześć!', 'Zapraszam do lektury!'):
            intro.append(text)
    items = {}
    for h3 in soup.find_all('h3'):
        link = h3.find('a')
        if not link:
            continue
        desc, tags, czas = '', [], ''
        for el in h3.find_all_next(['p', 'h3', 'hr']):
            if el.name in ('h3', 'hr'):
                break
            labels = re.findall(r'\[([^\]]+)\]', el.get_text())
            if el.find('span') and labels:
                for label in labels:
                    if re.match(r'^\d+\s*(h|min)', label):
                        czas = label
                    else:
                        tags.append(label)
            else:
                desc = (desc + ' ' + el.get_text(' ', strip=True)).strip()
        items[dedup_key(link['href'])] = {'Link': link['href'], 'Tytuł': link.get_text(' ', strip=True),
                                          'Opis': desc, 'Tagi': ', '.join(sorted(tags)), 'Czas': czas}
    return '\n\n'.join(intro), items


def cmd_substack(args):
    import requests
    folder = repo.issue_dir(args.numer)
    meta = repo.read_json(os.path.join(folder, 'meta.json'))
    if not meta:
        raise SystemExit('Brak %s/meta.json' % folder)
    if meta.get('porownano_z_substackiem'):
        print('Wydanie #%s bylo juz porownane z Substackiem.' % args.numer)
        return
    resp = requests.get(SUBSTACK_API % meta['slug'], timeout=20)
    if resp.status_code != 200:
        print('Post %s jeszcze niedostepny na Substacku (HTTP %s) - pomijam.' % (meta['slug'], resp.status_code))
        return
    post = resp.json()
    if not post.get('is_published', True):
        print('Post jeszcze nieopublikowany - pomijam.')
        return

    issue = meta['numer']
    entries = []
    for field, remote in (('tytul', post.get('title')), ('opis_seo', post.get('search_engine_description'))):
        if remote and norm(remote) != norm(meta.get(field)):
            entries.append({'wydanie': issue, 'etap': 'substack', 'rodzaj': 'zmiana', 'pole': field,
                            'ai': meta.get(field, ''), 'kuba': remote})
    intro, published = parse_published(post.get('body_html', ''))
    if intro and norm(intro) != norm(meta.get('wstep')):
        entries.append({'wydanie': issue, 'etap': 'substack', 'rodzaj': 'zmiana', 'pole': 'wstep',
                        'ai': meta.get('wstep', ''), 'kuba': intro})

    local = {dedup_key(r['Link']): r for r in repo.read_csv(os.path.join(folder, 'dane.csv'))}
    for key, row in local.items():
        remote = published.get(key)
        if remote is None:
            entries.append({'wydanie': issue, 'etap': 'substack', 'rodzaj': 'usuniety_w_substacku',
                            'link': row['Link'], 'kontekst': {'tytul': row['Tytuł']}})
            continue
        for field in FIELDS:
            if norm(row.get(field)) != norm(remote.get(field)):
                entries.append({'wydanie': issue, 'etap': 'substack', 'rodzaj': 'zmiana', 'pole': field,
                                'link': row['Link'], 'ai': row.get(field, ''), 'kuba': remote.get(field, '')})
    for key, remote in published.items():
        if key not in local:
            entries.append({'wydanie': issue, 'etap': 'substack', 'rodzaj': 'dodany_w_substacku',
                            'link': remote['Link'], 'kuba': remote})

    print('Dopisano do dziennika: %d wpisow' % append(entries))
    meta['porownano_z_substackiem'] = True
    repo.write_json(os.path.join(folder, 'meta.json'), meta)


def read_all():
    if not os.path.exists(repo.DZIENNIK):
        return []
    with open(repo.DZIENNIK, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def cmd_nowe(_args):
    done = (repo.read_json(STAN, {}) or {}).get('przetworzone_wpisy', 0)
    entries = read_all()[done:]
    print('Nowych wpisow: %d (przetworzonych wczesniej: %d)' % (len(entries), done))
    for entry in entries:
        print(json.dumps(entry, ensure_ascii=False))


def cmd_oznacz(_args):
    total = len(read_all())
    repo.write_json(STAN, {'przetworzone_wpisy': total,
                           'data': datetime.now().strftime('%Y-%m-%d %H:%M')})
    print('Oznaczono jako przetworzone: %d wpisow' % total)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='polecenie', required=True)
    sub.add_parser('selekcja').set_defaults(func=cmd_selekcja)
    sub.add_parser('wydanie').set_defaults(func=cmd_wydanie)
    p = sub.add_parser('substack')
    p.add_argument('numer', type=int)
    p.set_defaults(func=cmd_substack)
    sub.add_parser('nowe').set_defaults(func=cmd_nowe)
    sub.add_parser('oznacz').set_defaults(func=cmd_oznacz)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
