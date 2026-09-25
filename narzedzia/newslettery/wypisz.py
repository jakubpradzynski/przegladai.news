#!/usr/bin/env python3
"""Wypisuje skrzynke z wybranych list mailingowych (naglowek List-Unsubscribe).

Kolejnosc prob:
    1. one-click (RFC 8058): POST "List-Unsubscribe=One-Click" na adres https,
    2. mailto: mail "unsubscribe" wyslany przez gws,
    3. zostaje link do klikniecia w przegladarce.

Wynik kazdej listy trafia do redakcja/newslettery.json (decyzja "wypisany" albo "do_recznego").
Uzywane przez narzedzie przegladu (przeglad/server.py); mozna tez z linii polecen.

Uzycie:
    python3 narzedzia/newslettery/wypisz.py --lista plik.txt [--wykonaj]
    (plik: jeden identyfikator listy w linii - kolumna "id" z kandydaci.py)
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from email.message import EmailMessage
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from lib import repo  # noqa: E402
from lib.urlclean import HEADERS  # noqa: E402
import kandydaci  # noqa: E402


def latest_mails():
    """Najnowszy mail z naglowkiem wypisu dla kazdej listy (starsze tokeny moga wygasnac)."""
    latest = {}
    with open(kandydaci.MAILE, encoding='utf-8') as f:
        for line in f:
            mail = json.loads(line)
            if not mail.get('list_unsubscribe'):
                continue
            sender = ' '.join(mail['sender'].replace('"', '').split())
            ident = kandydaci.list_id(sender, mail['list_unsubscribe'])
            if mail['internal_date'] >= latest.get(ident, {}).get('internal_date', 0):
                latest[ident] = mail
    return latest


def one_click(url):
    import requests
    resp = requests.post(url, data={'List-Unsubscribe': 'One-Click'}, headers=HEADERS, timeout=20)
    return resp.status_code < 400, 'one-click HTTP %s' % resp.status_code


def send_mailto(target):
    address, _, query = target.partition('?')
    subject = re.search(r'subject=([^&]+)', query)
    msg = EmailMessage()
    msg['To'] = address
    msg['Subject'] = unquote(subject.group(1)) if subject else 'unsubscribe'
    msg.set_content('unsubscribe')
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    proc = subprocess.run(['gws', 'gmail', 'users', 'messages', 'send', '--params', '{"userId":"me"}',
                           '--json', json.dumps({'raw': raw})], capture_output=True, text=True)
    return proc.returncode == 0, ('mail do %s' % address) if proc.returncode == 0 else proc.stderr.strip()[:120]


def unsubscribe(ident, mail):
    """Zwraca (ok, metoda/opis, link_do_recznego)."""
    header = mail['list_unsubscribe']
    https = re.findall(r'<(https?://[^>]+)>', header)
    mailto = re.findall(r'<mailto:([^>]+)>', header)
    manual = https[0] if https else None
    if https and 'One-Click' in (mail.get('list_unsubscribe_post') or ''):
        ok, info = one_click(https[0])
        if ok:
            return True, info, None
    if mailto:
        ok, info = send_mailto(mailto[0])
        if ok:
            return True, info, None
    return False, 'wymaga kliknięcia w przeglądarce', manual


def record(ident, name, decision, note=''):
    decisions = kandydaci.load_decisions()
    decisions[ident] = {'nadawca': name, 'decyzja': decision,
                        'data': datetime.now().isoformat(timespec='seconds'), 'uwagi': note}
    repo.write_json(kandydaci.DECYZJE, dict(sorted(decisions.items())))


def run(idents, execute=True):
    latest = latest_mails()
    results = []
    for ident in idents:
        mail = latest.get(ident)
        name = ' '.join(mail['sender'].replace('"', '').split()) if mail else ident
        if not mail:
            results.append({'id': ident, 'nadawca': name, 'ok': False, 'info': 'brak maila z nagłówkiem wypisu', 'link': None})
            continue
        if not execute:
            results.append({'id': ident, 'nadawca': name, 'ok': None, 'info': 'podgląd', 'link': None})
            continue
        ok, info, link = unsubscribe(ident, mail)
        record(ident, name, 'wypisany' if ok else 'do_recznego', info if ok else (link or info))
        results.append({'id': ident, 'nadawca': name, 'ok': ok, 'info': info, 'link': link})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--lista', required=True)
    parser.add_argument('--wykonaj', action='store_true')
    args = parser.parse_args()
    with open(args.lista, encoding='utf-8') as f:
        idents = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    for r in run(idents, execute=args.wykonaj):
        mark = {True: 'OK ', False: '!! ', None: '.. '}[r['ok']]
        print('%s %s — %s%s' % (mark, r['nadawca'], r['info'], (' -> %s' % r['link']) if r['link'] else ''))


if __name__ == '__main__':
    main()
