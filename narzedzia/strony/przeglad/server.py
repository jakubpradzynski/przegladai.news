#!/usr/bin/env python3
"""Przeglad nowych wpisow ze stron: http://localhost:8020

Wczytuje .cache/strony/wynik.json (zbierz.py) i .cache/strony/przegladarka.json (wpisy zebrane
przez Claude w Chrome), pokazuje nowe wpisy pogrupowane po stronach i stan kazdej strony.
Jesli jest .cache/strony/preselekcja.json (subagent preselektor), wpisy maja ocene AI:
tak (od razu zaznaczone), moze (do decyzji), nie (zwiniete).
Wybrane linki dopisuje do data.csv. Do redakcja/dziennik/strony_wybory.jsonl trafia kazdy pokazany
wpis: ocena AI i decyzja Kuby (wziety / pominiety / niewidziany - odrzucony przez AI i nie rozwiniety).
Z tego dziennika skill ucz-sie aktualizuje redakcja/preselekcja.md. Statystyka stron (ile nowych,
ile wybranych) idzie do redakcja/dziennik/strony.jsonl.

Uzycie:
    python3 narzedzia/strony/przeglad/server.py [--port 8020]
"""
import argparse
import http.server
import json
import os
import socketserver
import sys
import threading
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from lib import repo  # noqa: E402
from lib.urlclean import dedup_key  # noqa: E402

CACHE = os.path.join(repo.ROOT, '.cache', 'strony')
WYNIK = os.path.join(CACHE, 'wynik.json')
PRZEGLADARKA = os.path.join(CACHE, 'przegladarka.json')
SESJA = os.path.join(CACHE, 'sesja.json')
HISTORIA = os.path.join(repo.REDAKCJA, 'dziennik', 'strony.jsonl')
WYBORY = os.path.join(repo.REDAKCJA, 'dziennik', 'strony_wybory.jsonl')
PRESELEKCJA = os.path.join(CACHE, 'preselekcja.json')
PODOBNE = os.path.join(CACHE, 'podobne.json')


def load(with_preselection=True):
    result = repo.read_json(WYNIK)
    if not result:
        raise SystemExit('Brak .cache/strony/wynik.json - uruchom najpierw narzedzia/strony/zbierz.py')
    manual = repo.read_json(PRZEGLADARKA, {}) or {}
    if manual.get('od') == result['od']:
        by_site = {}
        for item in manual.get('wpisy', []):
            if item.get('data', '') >= result['od']:
                by_site.setdefault(item['strona'], []).append(dict(item, przegladarka=True))
        for site in result['strony']:
            if site['nazwa'] in manual.get('sprawdzone', []):
                known = {dedup_key(i['link']) for i in site['nowe']}
                extra = [i for i in by_site.get(site['nazwa'], []) if dedup_key(i['link']) not in known]
                site['nowe'] = sorted(site['nowe'] + extra, key=lambda i: i['data'], reverse=True)
                if site['status'] in ('przegladarka', 'problem', 'blad', 'uwaga'):
                    site['status'] = 'ok'
                    site['komunikat'] = 'sprawdzone w przeglądarce'
    known = set()
    if os.path.exists(repo.DATA_CSV):
        with open(repo.DATA_CSV, encoding='utf-8') as f:
            known = {dedup_key(line.strip()) for line in f if line.strip().startswith('http')}
    ratings, similar = {}, {}
    if with_preselection:
        ratings = {r['id']: r for r in (repo.read_json(PRESELEKCJA, []) or [])}
        similar = repo.read_json(PODOBNE, {}) or {}
    for site in result['strony']:
        for item in site['nowe']:
            item['w_data_csv'] = dedup_key(item['link']) in known
            rating = ratings.get(item['link'])
            item['ocena'] = rating['ocena'] if rating else 'moze'
            item['powod'] = rating['powod'] if rating else ('' if not ratings else 'brak oceny AI')
            if item['link'] in similar:
                item['podobne'] = similar[item['link']]
    result['preselekcja'] = bool(ratings)
    return result


def log_decisions(result, chosen, rejected_opened):
    stamp = datetime.now().isoformat(timespec='seconds')
    chosen = {dedup_key(l) for l in chosen}
    os.makedirs(os.path.dirname(WYBORY), exist_ok=True)
    logged = set()   # drugi zapis w tym samym przegladzie nie dubluje wpisow
    if os.path.exists(WYBORY):
        with open(WYBORY, encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                if entry.get('zrodlo') == 'przeglad' and entry.get('od') == result['od']:
                    logged.add(dedup_key(entry['link']))
    with open(WYBORY, 'a', encoding='utf-8') as f:
        for site in result['strony']:
            for item in site['nowe']:
                key = dedup_key(item['link'])
                if key in logged or (item.get('w_data_csv') and key not in chosen):
                    continue
                if key in chosen:
                    decision = 'wziety'
                elif item['ocena'] == 'nie' and not rejected_opened:
                    decision = 'niewidziany'
                else:
                    decision = 'pominiety'
                f.write(json.dumps({'data': stamp, 'zrodlo': 'przeglad', 'od': result['od'], 'strona': site['nazwa'],
                                    'wpis_z': item['data'], 'tytul': item['tytul'][:200], 'link': item['link'],
                                    'opis': item.get('opis', '')[:200], 'ai': item['ocena'] if result['preselekcja'] else None,
                                    'powod_ai': item.get('powod', ''), 'kuba': decision}, ensure_ascii=False) + '\n')


def save(links, result, chosen_by_site):
    existing = set()
    if os.path.exists(repo.DATA_CSV):
        with open(repo.DATA_CSV, encoding='utf-8') as f:
            content = f.read()
        existing = {dedup_key(line.strip()) for line in content.splitlines() if line.strip()}
    else:
        content = ''
    new = [l for l in links if dedup_key(l) not in existing]
    with open(repo.DATA_CSV, 'a', encoding='utf-8') as f:
        if content and not content.endswith('\n'):
            f.write('\n')
        for link in new:
            f.write(link + '\n')
    os.makedirs(os.path.dirname(HISTORIA), exist_ok=True)
    stamp = datetime.now().isoformat(timespec='seconds')
    with open(HISTORIA, 'a', encoding='utf-8') as f:
        for site in result['strony']:
            f.write(json.dumps({'data': stamp, 'od': result['od'], 'strona': site['nazwa'], 'status': site['status'],
                                'nowe': len(site['nowe']), 'wybrane': chosen_by_site.get(site['nazwa'], 0)},
                               ensure_ascii=False) + '\n')
    return len(new), len(links) - len(new)


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def reply(self, data, status=200, ctype='application/json; charset=utf-8'):
        body = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length).decode('utf-8')) if length else {}

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/':
            with open(os.path.join(HERE, 'index.html'), 'rb') as f:
                return self.reply(f.read(), ctype='text/html; charset=utf-8')
        if path == '/api/wpisy':
            return self.reply({'wynik': load(), 'sesja': repo.read_json(SESJA, {}) or {}})
        self.reply({'blad': 'nie ma takiej strony'}, 404)

    def do_POST(self):
        path = self.path.split('?')[0]
        if path == '/api/sesja':
            repo.write_json(SESJA, self.body())
            return self.reply({'ok': True})
        if path == '/api/zapisz':
            data = self.body()
            result = load()
            log_decisions(result, data.get('linki', []), data.get('odrzucone_otwarte', False))
            added, skipped = save(data.get('linki', []), result, data.get('na_strone', {}))
            if os.path.exists(SESJA):
                os.remove(SESJA)
            return self.reply({'dodane': added, 'pominiete': skipped})
        if path == '/api/shutdown':
            self.reply({'ok': True})
            return threading.Thread(target=self.server.shutdown).start()
        self.reply({'blad': 'nie ma takiej akcji'}, 404)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--port', type=int, default=8020)
    args = parser.parse_args()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', args.port), Handler) as httpd:
        print('Przegląd stron: http://localhost:%d' % args.port, flush=True)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
