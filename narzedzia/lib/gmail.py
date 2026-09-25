"""Cienka warstwa na Google Workspace CLI (`gws`) dla Gmaila.

Tylko odczyt. Zadna funkcja w tym module nie modyfikuje skrzynki -
nie oznacza maili jako przeczytanych, nie przenosi i nie kasuje.
Wypisywanie z newsletterow jest osobno, w narzedzia/newslettery/wypisz.py.
"""
import base64
import json
import random
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

GWS = 'gws'
_UA_TIMEOUT = 90


class GwsError(RuntimeError):
    pass


def _run(args, timeout=_UA_TIMEOUT, attempts=3):
    """Wywoluje gws z ponawianiem.

    Przy kilku rownoleglych procesach gws potrafi zwrocic blad przejsciowy
    (limit API, kolizja na keyringu). Bez ponawiania gubilismy w ten sposob
    ponad polowe maili.
    """
    last = None
    for attempt in range(attempts):
        try:
            proc = subprocess.run([GWS] + args, capture_output=True, text=True,
                                  timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            last = 'timeout po %ss' % timeout
        else:
            if proc.returncode == 0:
                return proc.stdout
            last = proc.stderr.strip() or 'kod %d' % proc.returncode
        if attempt < attempts - 1:
            time.sleep(1.5 * (attempt + 1) + random.random())
    raise GwsError('gws %s -> %s' % (' '.join(args[:4]), last))


def _json_lines(raw):
    """gws --page-all zwraca NDJSON (jedna linia = jedna strona wynikow)."""
    raw = raw.strip()
    if not raw:
        return []
    try:
        return [json.loads(raw)]
    except json.JSONDecodeError:
        pass
    pages = []
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(raw):
        while idx < len(raw) and raw[idx] in ' \t\r\n':
            idx += 1
        if idx >= len(raw):
            break
        obj, end = decoder.raw_decode(raw, idx)
        pages.append(obj)
        idx = end
    return pages


def list_messages(query, max_messages=250, page_limit=10):
    """Zwraca liste id wiadomosci pasujacych do zapytania Gmaila."""
    params = json.dumps({'userId': 'me', 'q': query, 'maxResults': 100})
    raw = _run(['gmail', 'users', 'messages', 'list', '--params', params,
                '--page-all', '--page-limit', str(page_limit), '--format', 'json'])
    ids = []
    for page in _json_lines(raw):
        for msg in page.get('messages', []) or []:
            ids.append(msg['id'])
            if len(ids) >= max_messages:
                return ids
    return ids


def _b64(data):
    if not data:
        return ''
    padding = '=' * (-len(data) % 4)
    try:
        return base64.urlsafe_b64decode(data + padding).decode('utf-8', errors='replace')
    except Exception:
        return ''


def _walk_parts(part, acc):
    mime = part.get('mimeType', '')
    body = part.get('body', {}) or {}
    if body.get('data'):
        acc.setdefault(mime, _b64(body['data']))
    for child in part.get('parts', []) or []:
        _walk_parts(child, acc)


def get_message(message_id):
    """Zwraca dict: id, sender, subject, date (epoch ms), naglowki wypisu, html, text."""
    params = json.dumps({'userId': 'me', 'id': message_id, 'format': 'full'})
    raw = _run(['gmail', 'users', 'messages', 'get', '--params', params, '--format', 'json'])
    data = json.loads(raw)

    headers = {h['name'].lower(): h['value']
               for h in (data.get('payload', {}).get('headers', []) or [])}
    bodies = {}
    _walk_parts(data.get('payload', {}) or {}, bodies)

    return {
        'id': data.get('id'),
        'sender': headers.get('from', ''),
        'subject': headers.get('subject', ''),
        'internal_date': int(data.get('internalDate', 0)),
        'list_unsubscribe': headers.get('list-unsubscribe', ''),
        'list_unsubscribe_post': headers.get('list-unsubscribe-post', ''),
        'html': bodies.get('text/html', ''),
        'text': bodies.get('text/plain', ''),
    }


def get_messages(message_ids, workers=4, on_error=None):
    """Pobiera wiele wiadomosci rownolegle - kazde wywolanie gws ma wlasny narzut startu."""
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(get_message, mid): mid for mid in message_ids}
        for future in futures:
            try:
                results.append(future.result())
            except Exception as exc:  # pojedynczy mail nie moze wywrocic calego przebiegu
                if on_error:
                    on_error(futures[future], exc)
    results.sort(key=lambda m: m.get('internal_date', 0))
    return results


def get_headers(message_id, wanted=('From', 'Subject', 'Date')):
    """Lekki odczyt samych naglowkow (format=metadata) - do rankingu nadawcow."""
    params = json.dumps({'userId': 'me', 'id': message_id, 'format': 'metadata',
                         'metadataHeaders': list(wanted)})
    raw = _run(['gmail', 'users', 'messages', 'get', '--params', params, '--format', 'json'])
    data = json.loads(raw)
    headers = {h['name'].lower(): h['value']
               for h in (data.get('payload', {}).get('headers', []) or [])}
    return {
        'id': data.get('id'),
        'sender': headers.get('from', ''),
        'subject': headers.get('subject', ''),
        'internal_date': int(data.get('internalDate', 0)),
    }


def get_many_headers(message_ids, workers=4):
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for future in [pool.submit(get_headers, mid) for mid in message_ids]:
            try:
                results.append(future.result())
            except Exception:
                pass
    return results


def check_available():
    try:
        _run(['gmail', 'users', 'labels', 'list', '--params', '{"userId":"me"}',
              '--format', 'json'], timeout=30)
        return True, None
    except Exception as exc:
        return False, str(exc)
