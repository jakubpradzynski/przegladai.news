#!/usr/bin/env python3
"""Wypisuje skrzynke z wybranych newsletterow (naglowek List-Unsubscribe).

Kolejnosc prob:
    1. one-click (RFC 8058): POST "List-Unsubscribe=One-Click" na adres https,
    2. mailto: pusty mail "unsubscribe" wyslany przez gws,
    3. zostaje link do klikniecia w przegladarce (wypisany na koncu).

Bez --wykonaj tylko pokazuje, co by zrobil. Wynik trafia do
redakcja/zrodla.md (sekcja "Wypisane newslettery").

Uzycie:
    python3 narzedzia/newslettery/wypisz.py --lista praca/do_wypisania.txt [--wykonaj]
    (plik: jeden nadawca w linii, dokladnie jak w raporcie, np. "AlphaSignal <news@alphasignal.ai>")
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
from datetime import date
from email.message import EmailMessage

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import repo  # noqa: E402
from lib.urlclean import HEADERS  # noqa: E402

MAILE = os.path.join(repo.ROOT, '.cache', 'newslettery', 'maile.jsonl')
ZRODLA = os.path.join(repo.REDAKCJA, 'zrodla.md')


def sender_key(raw):
    return ' '.join((raw or '').replace('"', '').split())


def latest_headers():
    """Najnowszy naglowek wypisu dla kazdego nadawcy (starsze tokeny moga wygasnac)."""
    latest = {}
    with open(MAILE, encoding='utf-8') as f:
        for line in f:
            mail = json.loads(line)
            key = sender_key(mail['sender'])
            if mail.get('list_unsubscribe') and mail['internal_date'] >= latest.get(key, {}).get('internal_date', 0):
                latest[key] = mail
    return latest


def one_click(url):
    import requests
    resp = requests.post(url, data={'List-Unsubscribe': 'One-Click'}, headers=HEADERS, timeout=20)
    return resp.status_code < 400, 'HTTP %s' % resp.status_code


def send_mailto(target):
    address, _, query = target.partition('?')
    subject = re.search(r'subject=([^&]+)', query)
    msg = EmailMessage()
    msg['To'] = address
    msg['Subject'] = subject.group(1).replace('%20', ' ') if subject else 'unsubscribe'
    msg.set_content('unsubscribe')
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    proc = subprocess.run(['gws', 'gmail', 'users', 'messages', 'send', '--params', '{"userId":"me"}',
                           '--json', json.dumps({'raw': raw})], capture_output=True, text=True)
    return proc.returncode == 0, (proc.stderr.strip() or 'wyslano')[:120]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--lista', required=True)
    parser.add_argument('--wykonaj', action='store_true')
    args = parser.parse_args()

    with open(args.lista, encoding='utf-8') as f:
        wanted = [sender_key(line) for line in f if line.strip() and not line.startswith('#')]
    headers = latest_headers()

    done, manual = [], []
    for key in wanted:
        mail = headers.get(key)
        if not mail:
            manual.append((key, 'brak naglowka List-Unsubscribe - wypisz sie recznie'))
            continue
        header = mail['list_unsubscribe']
        https = re.findall(r'<(https?://[^>]+)>', header)
        mailto = re.findall(r'<mailto:([^>]+)>', header)
        is_one_click = 'One-Click' in (mail.get('list_unsubscribe_post') or '')

        if not args.wykonaj:
            method = 'one-click' if (https and is_one_click) else 'mailto' if mailto else 'przegladarka'
            print('[podglad] %-12s %s' % (method, key))
            continue

        ok, info = False, ''
        if https and is_one_click:
            ok, info = one_click(https[0])
        if not ok and mailto:
            ok, info = send_mailto(mailto[0])
        if ok:
            done.append(key)
            print('[OK]  %s (%s)' % (key, info))
        else:
            manual.append((key, https[0] if https else info))
            print('[!!]  %s -> recznie' % key)

    if manual:
        print('\nDo wypisania recznie:')
        for key, how in manual:
            print('  - %s\n      %s' % (key, how))

    if args.wykonaj and done:
        with open(ZRODLA, encoding='utf-8') as f:
            text = f.read()
        if '## Wypisane newslettery' not in text:
            text = text.rstrip() + '\n\n## Wypisane newslettery\n\nNie zapisywac sie ponownie bez powodu.\n'
        text = text.rstrip() + '\n' + ''.join('- %s — %s\n' % (date.today().isoformat(), k) for k in done)
        with open(ZRODLA, 'w', encoding='utf-8') as f:
            f.write(text)
        print('\nWypisano: %d. Zapisano w redakcja/zrodla.md' % len(done))


if __name__ == '__main__':
    main()
