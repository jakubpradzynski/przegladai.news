#!/usr/bin/env python3
"""Przeglad nowych wpisow ze stron: http://localhost:8020

Wczytuje .cache/strony/wynik.json (zbierz.py) i .cache/strony/przegladarka.json (wpisy zebrane
przez Claude w Chrome), pokazuje nowe wpisy pogrupowane po stronach i stan kazdej strony.
Wybrane linki dopisuje do data.csv; statystyke (ile nowych, ile wybranych na strone) dopisuje
do redakcja/dziennik/strony.jsonl - na jej podstawie mozna potem porzadkowac liste stron.

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


def load():
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
    for site in result['strony']:
        for item in site['nowe']:
            item['w_data_csv'] = dedup_key(item['link']) in known
    return result


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
