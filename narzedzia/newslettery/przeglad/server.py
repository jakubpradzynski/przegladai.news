#!/usr/bin/env python3
"""Przeglad newsletterow do wypisania: http://localhost:8010

Dla kazdego kandydata (kandydaci.py) pokazuje statystyki, powod i dwa ostatnie maile.
Kuba oznacza "wypisz" albo "zostaw"; na koncu jednym przyciskiem wypisuje oznaczone.
Decyzje trafiaja do redakcja/newslettery.json ("zostaw" wraca do przegladu po 90 dniach).

Uzycie:
    python3 narzedzia/newslettery/przeglad/server.py [--port 8010]
"""
import argparse
import html
import http.server
import json
import os
import socketserver
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
NEWSLETTERY = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(NEWSLETTERY))
sys.path.insert(0, NEWSLETTERY)

from lib import gmail  # noqa: E402
import kandydaci  # noqa: E402
import wypisz  # noqa: E402

SESJA = os.path.join(os.path.dirname(kandydaci.MAILE), 'przeglad_sesja.json')
_mail_cache = {}


def latest_two():
    """Dwa najnowsze maile (id, temat, data) dla kazdej listy."""
    by_list = {}
    with open(kandydaci.MAILE, encoding='utf-8') as f:
        for line in f:
            mail = json.loads(line)
            sender = ' '.join(mail['sender'].replace('"', '').split())
            ident = kandydaci.list_id(sender, mail.get('list_unsubscribe'))
            by_list.setdefault(ident, []).append((mail['internal_date'], mail['id'], mail['subject']))
    return {k: sorted(v, reverse=True)[:2] for k, v in by_list.items()}


def build_candidates():
    two = latest_two()
    rows = []
    for c in kandydaci.candidates():
        rows.append({
            'id': c['id'], 'nadawca': c['nadawca'], 'warianty': c.get('warianty', []),
            'maile': c['maile'], 'na_tydzien': c['na_tydzien'], 'zrodlo': c['zrodlo'],
            'temat': c['temat_wszystkie'], 'pierwszy': c['pierwszy'], 'unikalne': c['unikalne'],
            'ai_pct': c['ai_pct'], 'znane_domeny_pct': c['znane_domeny_pct'],
            'powod': c['powod'], 'ostrzezenie': c.get('ostrzezenie', ''), 'adnotacja': c['adnotacja'],
            'przyklady': c.get('przyklady', []),
            'maile_ostatnie': [{'id': mid, 'temat': subj, 'data': ts} for ts, mid, subj in two.get(c['id'], [])],
        })
    return rows


def mail_html(message_id):
    if message_id not in _mail_cache:
        msg = gmail.get_message(message_id)
        body = msg.get('html') or '<pre style="white-space:pre-wrap;font:14px sans-serif">%s</pre>' % html.escape(msg.get('text', ''))
        # linki otwieraja sie w nowej karcie, a nie w ramce
        _mail_cache[message_id] = '<base target="_blank">' + body
    return _mail_cache[message_id]


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def reply(self, data, status=200, ctype='application/json; charset=utf-8'):
        body = data if isinstance(data, bytes) else (
            data.encode('utf-8') if isinstance(data, str) else json.dumps(data, ensure_ascii=False).encode('utf-8'))
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
        if path == '/api/kandydaci':
            session = {}
            if os.path.exists(SESJA):
                with open(SESJA, encoding='utf-8') as f:
                    session = json.load(f)
            return self.reply({'kandydaci': build_candidates(), 'decyzje': session})
        if path.startswith('/api/mail/'):
            try:
                return self.reply(mail_html(path.rsplit('/', 1)[1]), ctype='text/html; charset=utf-8')
            except Exception as exc:  # gws niedostepny, mail usuniety itp.
                return self.reply('<p>Nie udało się pobrać maila: %s</p>' % html.escape(str(exc)),
                                  ctype='text/html; charset=utf-8')
        self.reply({'blad': 'nie ma takiej strony'}, 404)

    def do_POST(self):
        path = self.path.split('?')[0]
        if path == '/api/sesja':
            with open(SESJA, 'w', encoding='utf-8') as f:
                json.dump(self.body().get('decyzje', {}), f, ensure_ascii=False)
            return self.reply({'ok': True})
        if path == '/api/zakoncz':
            decisions = self.body().get('decyzje', {})
            names = {c['id']: c['nadawca'] for c in build_candidates()}
            for ident, decision in decisions.items():
                if decision == 'zostaw':
                    wypisz.record(ident, names.get(ident, ident), 'zostaw')
            results = wypisz.run([i for i, d in decisions.items() if d == 'wypisz'], execute=True)
            if os.path.exists(SESJA):
                os.remove(SESJA)
            return self.reply({'wyniki': results,
                               'zostawione': sum(1 for d in decisions.values() if d == 'zostaw')})
        if path == '/api/shutdown':
            self.reply({'ok': True})
            return threading.Thread(target=self.server.shutdown).start()
        self.reply({'blad': 'nie ma takiej akcji'}, 404)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--port', type=int, default=8010)
    args = parser.parse_args()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', args.port), Handler) as httpd:
        print('Przegląd newsletterów: http://localhost:%d' % args.port, flush=True)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
