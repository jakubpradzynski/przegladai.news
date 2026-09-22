#!/usr/bin/env python3
"""Adminka wydania: http://localhost:8000

Zakladka "Selekcja": praca/prepared_data.csv -> praca/final_prepared_data.csv
    (postep zapisywany na biezaco do praca/roboczy.csv)
Zakladka "Wydanie": propozycje AI z praca/wydanie_ai.json -> praca/wydanie.json
    -> narzedzia/generuj_wydanie.py -> wydania/NNN/

Uzycie:
    python3 narzedzia/adminka/server.py [--port 8000]
"""
import argparse
import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from lib import repo  # noqa: E402

WORK_FIELDS = repo.AI_FIELDS + ['Wybrany']


def run(script, *args):
    proc = subprocess.run([sys.executable, os.path.join(repo.ROOT, 'narzedzia', script)] + list(args),
                          capture_output=True, text=True, cwd=repo.ROOT)
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


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

    def issue_file(self, name):
        meta = repo.read_json(repo.WYDANIE, {}) or {}
        return os.path.join(repo.issue_dir(meta['numer']), name) if meta.get('numer') else None

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/':
            with open(os.path.join(HERE, 'index.html'), 'rb') as f:
                return self.reply(f.read(), ctype='text/html; charset=utf-8')
        if path == '/api/dane':
            source = repo.ROBOCZY if os.path.exists(repo.ROBOCZY) else repo.PREPARED
            rows = repo.read_csv(source) if os.path.exists(source) else []
            if source == repo.PREPARED:
                for row in rows:
                    row['Wybrany'] = '1' if row.get('Rekomendacja') == 'TOP' else ''
            return self.reply({'wiersze': rows, 'zrodlo': os.path.basename(source)})
        if path == '/api/wydanie':
            last = repo.last_issue() or {}
            return self.reply({'ai': repo.read_json(repo.WYDANIE_AI),
                               'zapisane': repo.read_json(repo.WYDANIE),
                               'selekcja_zapisana': os.path.exists(repo.FINAL),
                               'nastepny_numer': (last.get('numer') or 0) + 1,
                               'piatek': repo.next_friday().isoformat()})
        if path == '/podglad/substack':
            target = self.issue_file('substack.html')
            if target and os.path.exists(target):
                with open(target, 'rb') as f:
                    return self.reply(f.read(), ctype='text/html; charset=utf-8')
            return self.reply({'blad': 'wydanie jeszcze niewygenerowane'}, 404)
        if path in ('/podglad/okladka', '/podglad/okladka-robocza'):
            target = (self.issue_file('okladka.jpeg') if path == '/podglad/okladka'
                      else os.path.join(repo.PRACA, 'okladka_podglad.jpeg'))
            if target and os.path.exists(target):
                with open(target, 'rb') as f:
                    return self.reply(f.read(), ctype='image/jpeg')
            return self.reply({'blad': 'brak okladki'}, 404)
        self.reply({'blad': 'nie ma takiej strony'}, 404)

    def do_POST(self):
        path = self.path.split('?')[0]
        if path == '/api/roboczy':
            repo.write_csv(repo.ROBOCZY, self.body().get('wiersze', []), WORK_FIELDS)
            return self.reply({'ok': True})
        if path == '/api/zapisz':
            rows = self.body().get('wiersze', [])
            chosen = [r for r in rows if r.get('Wybrany')]
            repo.write_csv(repo.ROBOCZY, rows, WORK_FIELDS)
            repo.write_csv(repo.FINAL, chosen, repo.BASE_FIELDS)
            return self.reply({'ok': True, 'zapisano': len(chosen)})
        if path == '/api/okladka':
            ok, out = run('okladka.py', self.body().get('napis', ''), '--podglad')
            return self.reply({'ok': ok, 'wynik': out})
        if path == '/api/wydanie':
            repo.write_json(repo.WYDANIE, self.body())
            ok, out = run('generuj_wydanie.py')
            return self.reply({'ok': ok, 'wynik': out})
        if path == '/api/shutdown':
            self.reply({'ok': True})
            return threading.Thread(target=self.server.shutdown).start()
        self.reply({'blad': 'nie ma takiej akcji'}, 404)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', args.port), Handler) as httpd:
        print('Adminka: http://localhost:%d' % args.port, flush=True)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
