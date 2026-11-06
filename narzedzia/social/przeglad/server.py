#!/usr/bin/env python3
"""Narzedzie do postow social: http://localhost:8030

Etap 1 - tematy: propozycje AI (wydania/NNN/social/tematy_ai.json) + wszystkie newsy z wydania.
         Kuba zaznacza tematy (ile chce), moze dopisac wskazowke; "Generuj" zapisuje wybor.json
         i wrzuca zadanie do kolejki .cache/social/NNN/zadania/ - obsluguje je Claude (skill posty-social).
Etap 2 - posty: edycja tekstu LinkedIn (ten sam na FB i Substack Notes), pierwszego komentarza,
         watku na X, wybor obrazka (okladka / infografika / prompt), termin, "publikuje", uwaga dla AI,
         prosba do Claude o poprawke (tez przez kolejke), wyniki po publikacji.
Zapis automatyczny do posty.json. Zmiany zrobione przez Claude narzedzie wczytuje samo.
"Zakoncz" ustawia status "gotowe" - skill zapisuje poprawki do dziennika i uczy reguly.

Uzycie:
    python3 narzedzia/social/przeglad/server.py --numer 44 [--port 8030]
"""
import argparse
import http.server
import json
import os
import socketserver
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.dirname(HERE))

from lib import repo  # noqa: E402
import posty as P  # noqa: E402

LOCK = threading.Lock()
NUMER = None


def mtime(path):
    return os.path.getmtime(path) if os.path.exists(path) else 0


def queue_dir():
    return os.path.join(P.cache_dir(NUMER), 'zadania')


def pending():
    d = queue_dir()
    if not os.path.isdir(d):
        return []
    return [repo.read_json(os.path.join(d, f)) for f in sorted(os.listdir(d)) if f.endswith('.json')]


def enqueue(task):
    os.makedirs(queue_dir(), exist_ok=True)
    name = '%d-%s.json' % (time.time() * 1000, task['rodzaj'])
    task['utworzone'] = time.strftime('%Y-%m-%d %H:%M:%S')
    repo.write_json(os.path.join(queue_dir(), name), task)


def news():
    path = os.path.join(repo.issue_dir(NUMER), 'dane.csv')
    return [{'link': r['Link'], 'tytul': r['Tytuł'], 'opis': r['Opis'], 'tagi': r['Tagi']}
            for r in repo.read_csv(path)] if os.path.exists(path) else []


def state():
    p = P.paths(NUMER)
    return {'numer': NUMER, 'meta': repo.read_json(os.path.join(repo.issue_dir(NUMER), 'meta.json'), {}),
            'url_wydania': P.issue_url(NUMER), 'newsy': news(),
            'tematy_ai': repo.read_json(p['tematy_ai']), 'wybor': repo.read_json(p['wybor']),
            'posty': repo.read_json(p['posty']), 'wersja': mtime(p['posty']), 'zadania': pending()}


def check(data):
    phrases = P.banned_phrases()
    out = {}
    for post in (data or {}).get('posty', []):
        problems, warnings = P.check_post(post, phrases)
        out[post['id']] = {'bledy': problems, 'uwagi': warnings,
                           'x': [P.x_length(t) for t in post.get('x', [])]}
    return out


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

    def file(self, path, ctype):
        if not os.path.exists(path):
            return self.reply({'blad': 'brak pliku'}, 404)
        with open(path, 'rb') as f:
            self.reply(f.read(), ctype=ctype)

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/':
            return self.file(os.path.join(HERE, 'index.html'), 'text/html; charset=utf-8')
        if path == '/api/stan':
            s = state()
            s['kontrola'] = check(s['posty'])
            return self.reply(s)
        if path == '/okladka.jpeg':
            return self.file(os.path.join(repo.issue_dir(NUMER), 'okladka.jpeg'), 'image/jpeg')
        if path.startswith('/obrazki/') and '..' not in path:
            return self.file(os.path.join(P.social_dir(NUMER), path.lstrip('/')), 'image/png')
        self.reply({'blad': 'nie ma takiej strony'}, 404)

    def do_POST(self):
        path = self.path.split('?')[0]
        p = P.paths(NUMER)
        data = self.body()
        with LOCK:
            if path == '/api/wybor':
                old = repo.read_json(p['wybor'], {}) or {}
                done = set(old.get('tematy', []))
                new = [t for t in data['tematy'] if t['id'] not in done]
                merged = {'tematy': old.get('tematy', []) + [t['id'] for t in new],
                          'szczegoly': (old.get('szczegoly') or []) + new}
                repo.write_json(p['wybor'], merged)
                if new:
                    enqueue({'rodzaj': 'generuj', 'tematy': new})
                return self.reply({'ok': True, 'nowe': len(new)})
            if path == '/api/posty':
                if data.get('wersja') and abs(data['wersja'] - mtime(p['posty'])) > 1e-6:
                    return self.reply({'konflikt': True, 'wersja': mtime(p['posty'])}, 409)
                repo.write_json(p['posty'], data['posty'])
                return self.reply({'wersja': mtime(p['posty']), 'kontrola': check(data['posty'])})
            if path == '/api/grafika':
                posts = repo.read_json(p['posty'])
                post = next(x for x in posts['posty'] if x['id'] == data['id'])
                post.setdefault('obrazek', {})['infografika'] = data['spec']
                try:
                    P.render_images(NUMER, {'posty': [post]})
                except SystemExit as e:
                    return self.reply({'blad': str(e)}, 400)
                repo.write_json(p['posty'], posts)
                return self.reply({'wersja': mtime(p['posty']), 'plik': post['obrazek'].get('plik')})
            if path == '/api/prosba':
                enqueue({'rodzaj': 'popraw', 'post': data['id'], 'prosba': data['prosba']})
                return self.reply({'ok': True})
            if path == '/api/gotowe':
                posts = repo.read_json(p['posty'])
                posts['status'] = 'gotowe'
                repo.write_json(p['posty'], posts)
                return self.reply({'wersja': mtime(p['posty'])})
            if path == '/api/shutdown':
                self.reply({'ok': True})
                return threading.Thread(target=self.server.shutdown).start()
        self.reply({'blad': 'nie ma takiej akcji'}, 404)


def main():
    global NUMER
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--numer', type=int, required=True)
    parser.add_argument('--port', type=int, default=8030)
    args = parser.parse_args()
    NUMER = args.numer
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', args.port), Handler) as httpd:
        print('Posty social #%d: http://localhost:%d' % (NUMER, args.port), flush=True)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
