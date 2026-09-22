#!/usr/bin/env python3
"""Pobiera maile z etykiety Newsletter do .cache/newslettery/maile.jsonl

Kazdy mail zapisywany jest jako: nadawca, temat, data, naglowki wypisu,
dlugosc tekstu i lista linkow (href, tekst linku, zdanie wokol linku).
Na tej podstawie analizuj.py dopasowuje maile do newsow z wydan.

Uzycie:
    python3 narzedzia/newslettery/pobierz_maile.py --od 2026-07-08 --do 2026-09-19
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bs4 import BeautifulSoup  # noqa: E402

from lib import gmail  # noqa: E402

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.cache', 'newslettery')
BLOCK_TAGS = ('p', 'td', 'li', 'h1', 'h2', 'h3', 'h4', 'div', 'blockquote')
SPACES_RE = re.compile(r'[\s​‌‍⁠﻿\xa0͏]+')


def squash(text):
    return SPACES_RE.sub(' ', text or '').strip()


def extract(html, plain):
    """Zwraca (dlugosc tekstu, linki) dla jednego maila."""
    if not html:
        urls = re.findall(r'https?://[^\s<>"\'\])]+', plain or '')
        return len(plain or ''), [{'href': u, 'anchor': '', 'context': ''} for u in urls]

    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(('style', 'script', 'head')):
        tag.decompose()

    links = []
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        if not href.startswith('http'):
            continue
        anchor = squash(a.get_text(' '))
        block = a.find_parent(BLOCK_TAGS)
        context = squash(block.get_text(' ')) if block else anchor
        links.append({'href': href, 'anchor': anchor[:300], 'context': context[:600]})
    return len(squash(soup.get_text(' '))), links


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--od', required=True, help='YYYY-MM-DD')
    parser.add_argument('--do', required=True, help='YYYY-MM-DD')
    parser.add_argument('--etykieta', default='Newsletter')
    parser.add_argument('--watki', type=int, default=8)
    args = parser.parse_args()

    os.makedirs(CACHE_DIR, exist_ok=True)
    out_path = os.path.join(CACHE_DIR, 'maile.jsonl')

    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding='utf-8') as f:
            done = {json.loads(line)['id'] for line in f if line.strip()}

    query = 'label:%s after:%s before:%s' % (args.etykieta, args.od.replace('-', '/'),
                                             args.do.replace('-', '/'))
    ids = gmail.list_messages(query, max_messages=10000, page_limit=100)
    todo = [i for i in ids if i not in done]
    print('Zapytanie: %s -> %d maili, do pobrania %d' % (query, len(ids), len(todo)), file=sys.stderr)

    errors = []
    batch = 100
    with open(out_path, 'a', encoding='utf-8') as out:
        for start in range(0, len(todo), batch):
            chunk = todo[start:start + batch]
            messages = gmail.get_messages(chunk, workers=args.watki,
                                          on_error=lambda mid, exc: errors.append(mid))
            for msg in messages:
                text_len, links = extract(msg.pop('html'), msg.pop('text'))
                msg['text_len'] = text_len
                msg['links'] = links
                out.write(json.dumps(msg, ensure_ascii=False) + '\n')
            out.flush()
            print('  %d/%d' % (min(start + batch, len(todo)), len(todo)), file=sys.stderr)

    if errors:
        print('Nie pobrano %d maili (uruchom ponownie, dociagnie brakujace).' % len(errors),
              file=sys.stderr)


if __name__ == '__main__':
    main()
