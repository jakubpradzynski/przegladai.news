#!/usr/bin/env python3
"""Kandydaci do wypisania: .cache/newslettery/raport.json (analizuj.py) -> lista z priorytetem i powodem.

Uzytecznosc nadawcy = (newsy wziete wprost + 3 x unikalne + 0.3 x opisane tematy) / liczba maili.
Kandydat: uzytecznosc < PROG i najwyzej 1 unikalny news. Kolejnosc: najwiecej "zmarnowanych"
maili na gorze (liczba maili x brak uzytecznosci).

Jednostka jest LISTA mailingowa, nie nazwa nadawcy: warianty nazwy z tego samego adresu
(np. "Gregor Ojstersek" i "Gregor Ojstersek and Ryan Murphy") to jedna lista - wypisanie
z jednego wypisaloby z obu. Wyjatek: jeden adres dla wielu list (TLDR) - listy rozroznia
parametr l= w linku wypisu.

Pomijani sa nadawcy:
    - bez naglowka List-Unsubscribe (maile serwisowe, wlasne),
    - oznaczeni "zostaw" w ciagu ostatnich DNI_ZOSTAW dni (redakcja/newslettery.json),
    - juz wypisani - chyba ze nadal przysylaja maile (wtedy wracaja z adnotacja).

Uzycie:
    python3 narzedzia/newslettery/kandydaci.py      # tabela
"""
import collections
import json
import os
import re
import sys
from urllib.parse import parse_qs, urlparse
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import repo  # noqa: E402

RAPORT = os.path.join(repo.ROOT, '.cache', 'newslettery', 'raport.json')
MAILE = os.path.join(repo.ROOT, '.cache', 'newslettery', 'maile.jsonl')
DECYZJE = os.path.join(repo.REDAKCJA, 'newslettery.json')
PROG = 0.4
DNI_ZOSTAW = 90


def usefulness(r):
    return (r['zrodlo'] + 3 * r['unikalne'] + 0.3 * r['temat_wszystkie']) / max(1, r['maile'])


def reason(r):
    parts = []
    if r['temat_wszystkie'] == 0:
        parts.append('żaden news z wydań')
    elif r['zrodlo'] == 0:
        parts.append('opisał %d tematów z wydań, ale żaden nie był wzięty stąd' % r['temat_wszystkie'])
    else:
        parts.append('%d newsów wziętych stąd na %d maili' % (r['zrodlo'], r['maile']))
    if r['temat_wszystkie'] and r['unikalne'] == 0:
        parts.append('0 unikalnych — wszystko jest też w innych newsletterach')
    if r['ai_pct'] < 30:
        parts.append('tylko %d%% treści o AI' % r['ai_pct'])
    if r['znane_domeny_pct'] == 0 and r['temat_wszystkie']:
        parts.append('linki do własnej strony, trackera albo paywalla')
    if r['na_tydzien'] >= 4:
        parts.append('%.0f maili tygodniowo' % r['na_tydzien'])
    if r['ai_pct'] >= 70 and (r['znane_domeny_pct'] or 0) >= 50:
        parts.append('uwaga: treść pasuje do profilu (potencjał)')
    return '; '.join(parts)


def list_id(sender, header):
    """Identyfikator listy mailingowej: adres nadawcy (+ parametr l= z linku wypisu, jesli jest)."""
    match = re.search(r'<([^>]+)>', sender or '')
    address = (match.group(1) if match else sender or '').lower()
    for url in re.findall(r'<(https?://[^>]+)>', header or ''):
        lists = parse_qs(urlparse(url).query).get('l')
        if lists:
            return '%s#%s' % (address, lists[0])
    return address


def load_decisions():
    return repo.read_json(DECYZJE, {}) or {}


def last_mail_dates():
    latest = {}
    with open(MAILE, encoding='utf-8') as f:
        for line in f:
            mail = json.loads(line)
            ident = list_id(' '.join(mail['sender'].replace('"', '').split()), mail.get('list_unsubscribe'))
            latest[ident] = max(latest.get(ident, 0), mail['internal_date'])
    return latest


def merge(rows):
    """Laczy warianty nazwy jednej listy w jedna pozycje."""
    main = max(rows, key=lambda r: r['maile'])
    total = sum(r['maile'] for r in rows)
    merged = dict(main)
    for field in ('maile', 'zrodlo', 'temat_pewny', 'temat_wszystkie', 'pierwszy', 'unikalne'):
        merged[field] = sum(r[field] for r in rows)
    merged['na_tydzien'] = round(sum(r['na_tydzien'] for r in rows), 1)
    merged['ai_pct'] = round(sum(r['ai_pct'] * r['maile'] for r in rows) / total)
    known = [r['znane_domeny_pct'] for r in rows if r['znane_domeny_pct'] is not None]
    merged['znane_domeny_pct'] = max(known) if known else None
    merged['przyklady'] = [x for r in rows for x in r['przyklady']][:6]
    merged['warianty'] = [r['nadawca'] for r in rows]
    return merged


def lists_from_report():
    report = repo.read_json(RAPORT)
    if not report:
        raise SystemExit('Brak .cache/newslettery/raport.json - uruchom najpierw analizuj.py')
    groups = collections.defaultdict(list)
    for r in report['nadawcy']:
        if r.get('wypis'):
            groups[list_id(r['nadawca'], r['wypis'])].append(r)
    return {ident: dict(merge(rows), id=ident) for ident, rows in groups.items()}


def candidates():
    decisions = load_decisions()
    latest = last_mail_dates()
    today = date.today()
    out = []
    for ident, r in lists_from_report().items():
        decision = decisions.get(ident, {})
        note = ''
        if decision.get('decyzja') == 'zostaw':
            if today - date.fromisoformat(decision['data'][:10]) < timedelta(days=DNI_ZOSTAW):
                continue
            note = 'zostawiony %s — ponowna ocena' % decision['data'][:10]
        if decision.get('decyzja') == 'wypisany':
            since = datetime.fromisoformat(decision['data'])
            if datetime.fromtimestamp(latest.get(ident, 0) / 1000) <= since + timedelta(days=3):
                continue
            note = 'NADAL WYSYŁA mimo wypisania %s' % decision['data'][:10]
        score = usefulness(r)
        if not note and (score >= PROG or r['unikalne'] > 1):
            continue
        waste = r['maile'] * max(0.0, PROG - score) / PROG
        out.append(dict(r, uzytecznosc=round(score, 3), marnowane=round(waste, 1), powod=reason(r), adnotacja=note))
    # ostrzezenie, gdy ten sam wydawca ma tez liste, ktora zostaje (np. sekcja Substacka)
    chosen = {c['id'] for c in out}
    kept = {}
    for ident, r in lists_from_report().items():
        if ident not in chosen:
            kept.setdefault(publisher(ident), r['nadawca'])
    for c in out:
        other = kept.get(publisher(c['id']))
        if other and '#' not in c['id']:
            c['ostrzezenie'] = 'Ten sam wydawca co „%s”, który zostaje — sprawdź w mailu, że wypis dotyczy tylko tej listy.' % other
    out.sort(key=lambda c: (not c['adnotacja'].startswith('NADAL'), -c['marnowane'], c['uzytecznosc']))
    return out


def publisher(ident):
    """'autor+sekcja@substack.com#lista' -> 'autor@substack.com'"""
    address = ident.split('#')[0]
    local, _, domain = address.partition('@')
    return '%s@%s' % (local.split('+')[0], domain)


def main():
    rows = candidates()
    print('%3s %5s %6s %6s %5s  %-45s %s' % ('#', 'MAILE', 'ZRODLO', 'TEMATY', 'UZYT', 'NADAWCA', 'POWOD'))
    for i, c in enumerate(rows, 1):
        print('%3d %5d %6d %6d %5.2f  %-45s %s %s' % (i, c['maile'], c['zrodlo'], c['temat_wszystkie'],
                                                      c['uzytecznosc'], c['nadawca'][:45], c['powod'],
                                                      c['adnotacja']))


if __name__ == '__main__':
    main()
