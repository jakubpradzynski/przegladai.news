#!/usr/bin/env python3
"""Zarzadzanie lista stron (redakcja/strony.json).

    lista                   wszystkie strony z trybem (feed / html / przegladarka) i skutecznoscia z historii
    dodaj URL [--nazwa N]   szuka kanalu RSS/Atom, sprawdza, czy wpisy i daty sie czytaja, dopiero wtedy dopisuje
          [--feed URL] [--filtr TEKST] [--przegladarka] [--wymus]
    usun NAZWA|URL          usuwa strone z listy
    sprawdz [NAZWA]         pobiera wpisy ze strony (albo wszystkich) z ostatnich 30 dni i pokazuje wynik

Uzycie:
    python3 narzedzia/strony/zarzadzaj.py dodaj https://example.com/blog --nazwa "Example"
"""
import argparse
import collections
import json
import os
import re
import sys
from datetime import date, timedelta
from urllib.parse import urljoin, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from bs4 import BeautifulSoup  # noqa: E402

from lib import repo  # noqa: E402
import zbierz  # noqa: E402

FEED_GUESSES = ('feed', 'feed/', 'rss', 'rss.xml', 'atom.xml', 'feed.xml', 'index.xml',
                'feeds/posts/default', 'blog/rss.xml', 'rss/')
WYBORY = os.path.join(repo.REDAKCJA, 'dziennik', 'strony_wybory.jsonl')


def load_config():
    return repo.read_json(zbierz.CONFIG)


def save_config(cfg):
    repo.write_json(zbierz.CONFIG, cfg)


def find(cfg, key):
    key_low = key.lower().rstrip('/')
    for site in cfg['strony']:
        if site['nazwa'].lower() == key_low or site['url'].lower().rstrip('/') == key_low:
            return site
    return None


def try_feed(url):
    try:
        items = zbierz.parse_feed(zbierz.get(url).content, url)
        return items if items else None
    except Exception:
        return None


def discover_feed(url):
    """Kanal z <link rel=alternate> albo pod typowymi adresami. Zwraca (url_kanalu, wpisy) albo (None, None)."""
    try:
        page = zbierz.get(url).text
    except Exception as exc:
        raise SystemExit('Strona nie odpowiada: %s' % exc)
    soup = BeautifulSoup(page, 'html.parser')
    candidates = [urljoin(url, l['href']) for l in soup.find_all('link', attrs={'type': re.compile('rss|atom')})
                  if l.get('href') and 'comments' not in l['href']]
    parsed = urlparse(url)
    root = '%s://%s/' % (parsed.scheme, parsed.netloc)
    section = url if url.endswith('/') else url + '/'
    candidates += [urljoin(section, g) for g in FEED_GUESSES] + [urljoin(root, g) for g in FEED_GUESSES]
    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        items = try_feed(candidate)
        if items:
            return candidate, items
    return None, page


def describe(items):
    dated = [i for i in items if i['data']]
    newest = max((i['data'] for i in dated), default=None)
    return '%d wpisów, %d z datą, najnowszy: %s' % (len(items), len(dated), newest or '-')


def cmd_dodaj(args):
    cfg = load_config()
    if find(cfg, args.url):
        raise SystemExit('Ta strona już jest na liście.')
    name = args.nazwa or urlparse(args.url).netloc.replace('www.', '')
    site = {'nazwa': name, 'url': args.url}
    if args.przegladarka:
        site['przegladarka'] = True
        print('Dodaję jako stronę do sprawdzania w przeglądarce (bez testu pobierania).')
    else:
        if args.feed:
            feed, items = args.feed, try_feed(args.feed)
            if not items:
                raise SystemExit('Podany kanał nie zwraca wpisów: %s' % args.feed)
        else:
            feed, found = discover_feed(args.url)
            items = found if feed else None
        if feed:
            site['feed'] = feed
            print('Kanał: %s — %s' % (feed, describe(items)))
        else:
            items = zbierz.listing_links(args.url, found, args.filtr)
            articles = {}
            for item in items[:10]:
                if item['data'] is None:
                    meta = zbierz.article_meta(item['link'], articles)
                    item['data'] = date.fromisoformat(meta['data']) if meta['data'] else None
            print('Brak kanału RSS/Atom — tryb HTML: %s' % describe(items[:10]))
        if args.filtr:
            site['filtr'] = args.filtr
        dated = [i for i in items if i['data']]
        for item in sorted(dated, key=lambda i: i['data'], reverse=True)[:5]:
            print('   %s  %s' % (item['data'], item['tytul'][:90]))
        if not dated and not args.wymus:
            raise SystemExit('Nie udało się odczytać dat wpisów — strona NIE została dodana.\n'
                             'Spróbuj --feed <url kanału>, --filtr <fragment adresu artykułów> albo --przegladarka.')
    cfg['strony'].append(site)
    save_config(cfg)
    print('Dodano „%s” do redakcja/strony.json.' % name)


def cmd_usun(args):
    cfg = load_config()
    site = find(cfg, args.strona)
    if not site:
        raise SystemExit('Nie ma takiej strony. Nazwy: python3 narzedzia/strony/zarzadzaj.py lista')
    cfg['strony'].remove(site)
    save_config(cfg)
    print('Usunięto „%s” (%s).' % (site['nazwa'], site['url']))


def cmd_lista(_args):
    stats = collections.defaultdict(lambda: [0, 0])
    if os.path.exists(WYBORY):
        with open(WYBORY, encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                if entry['kuba'] != 'niewidziany':
                    stats[entry['strona']][0] += entry['kuba'] == 'wziety'
                    stats[entry['strona']][1] += 1
    cfg = load_config()
    print('%-13s %-10s %s' % ('TRYB', 'WZIĘTE', 'STRONA'))
    for site in cfg['strony']:
        mode = 'przegladarka' if site.get('przegladarka') else 'feed' if site.get('feed') else 'html'
        taken, total = stats[site['nazwa']]
        print('%-13s %-10s %s  %s' % (mode, '%d/%d' % (taken, total), site['nazwa'], site['url']))
    print('Razem: %d stron' % len(cfg['strony']))


def cmd_sprawdz(args):
    cfg = load_config()
    sites = cfg['strony'] if not args.strona else [find(cfg, args.strona)]
    if sites == [None]:
        raise SystemExit('Nie ma takiej strony.')
    since = date.today() - timedelta(days=30)
    articles = repo.read_json(zbierz.ARTYKULY, {}) or {}
    for site in sites:
        info = zbierz.collect_site(site, since, articles)
        print('%-12s %3d wpisów z 30 dni, najnowszy %s  %s %s' % (
            info['status'], len(info['nowe']), info['najnowszy'] or '-', site['nazwa'],
            ('- ' + info['komunikat']) if info['komunikat'] else ''))
    repo.write_json(zbierz.ARTYKULY, articles)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='polecenie', required=True)
    p = sub.add_parser('dodaj')
    p.add_argument('url')
    p.add_argument('--nazwa')
    p.add_argument('--feed')
    p.add_argument('--filtr')
    p.add_argument('--przegladarka', action='store_true')
    p.add_argument('--wymus', action='store_true', help='dodaj mimo braku dat')
    p.set_defaults(func=cmd_dodaj)
    p = sub.add_parser('usun')
    p.add_argument('strona')
    p.set_defaults(func=cmd_usun)
    sub.add_parser('lista').set_defaults(func=cmd_lista)
    p = sub.add_parser('sprawdz')
    p.add_argument('strona', nargs='?')
    p.set_defaults(func=cmd_sprawdz)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
