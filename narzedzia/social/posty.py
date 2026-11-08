#!/usr/bin/env python3
"""Posty social do wydania PrzegladAI: wydania/NNN/social/

Pliki (wszystkie w wydania/NNN/social/):
    tematy_ai.json   propozycje tematow od AI (nie zmieniamy po zapisaniu)
    wybor.json       tematy zaznaczone przez Kube w narzedziu (+ jego wskazowki)
    posty_ai.json    wersja AI postow (nie zmieniamy - z niej liczymy poprawki Kuby)
    posty.json       wersja robocza / finalna (edytuje narzedzie i Claude na prosbe Kuby)
    posty.md         czytelny eksport do kopiowania
    obrazki/         infografiki (grafika.py)
Robocze pliki subagentow i kolejka prosb z narzedzia: .cache/social/NNN/

Post:
    {"id": "glowny" | "t1"..., "rodzaj": "glowny" | "temat", "temat": "...", "link_newsa": "...",
     "tytul_newsa": "...", "kat": "...",
     "linkedin": "...",          tekst na LinkedIn (ten sam idzie na Facebooka i Substack Notes)
     "komentarz": "...",         pierwszy komentarz: link do wydania / zrodla
     "x": ["...", "..."],        watek na X, kazdy wpis <= 280 (wazona dlugosc)
     "obrazek": {"wybrany": "okladka|infografika|prompt|mem|brak", "infografika": {spec}, "prompt": "...",
                 "mem": {"szablon": "Drake Hotline Bling", "link": "https://imgflip.com/...", "tekst": "góra: ...\ndół: ..."},
                 "plik": "obrazki/t1.png"},
     "termin": "2026-11-03 08:30", "publikuj": true, "uwaga_kuby": "", "wynik": {}}

Polecenia:
    sprawdz <nr> [--ai]   walidacja postow wedlug redakcja/social*.md
    scal <nr>             dolacza posty z .cache/social/NNN/robocze/*.json do posty_ai.json i posty.json
    grafiki <nr>          rysuje infografiki ze spec do obrazki/
    eksport <nr>          posty.md (do kopiowania)
    podmien <nr>          podmienia posty w posty.json wersjami z .cache/social/NNN/poprawki/*.json (prosby Kuby);
                          zachowuje pola Kuby (publikuj, uwaga_kuby, wynik) i NIE rusza posty_ai.json
    weryfikacja <nr>      dolacza wyniki subagenta social-weryfikator (.cache/social/NNN/weryfikacja/*.json)
                          do posty.json (pole "weryfikacja" - nie jest poprawka, dziennik go nie porownuje)
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from lib import repo  # noqa: E402

SUBSTACK = 'https://przegladai.substack.com'
URL_RE = re.compile(r'https?://\S+')
LINKEDIN_FOLD = 210        # mniej wiecej tyle widac przed "...wiecej"
LINKEDIN_MAX = 3000
X_MAX = 280


def social_dir(numer):
    return os.path.join(repo.issue_dir(numer), 'social')


def cache_dir(numer):
    return os.path.join(repo.ROOT, '.cache', 'social', '%03d' % int(numer))


def paths(numer):
    d = social_dir(numer)
    return {k: os.path.join(d, v) for k, v in (('tematy_ai', 'tematy_ai.json'), ('wybor', 'wybor.json'),
                                                ('posty_ai', 'posty_ai.json'), ('posty', 'posty.json'),
                                                ('md', 'posty.md'), ('obrazki', 'obrazki'))}


def issue_url(numer):
    meta = repo.read_json(os.path.join(repo.issue_dir(numer), 'meta.json'), {}) or {}
    return '%s/p/%s' % (SUBSTACK, meta['slug']) if meta.get('slug') else SUBSTACK


# --- dlugosc na X (twitter-text v3: wiekszosc znakow lacinskich = 1, emoji/CJK = 2, link = 23) ---

LIGHT = ((0, 4351), (8192, 8205), (8208, 8223), (8242, 8247))
IGNORED = {0xFE0F, 0x200D} | set(range(0x1F3FB, 0x1F400))   # selektory wariantu, ZWJ, odcienie skory


def x_length(text):
    total = 0
    for part in re.split(r'(https?://\S+)', text):
        if URL_RE.fullmatch(part):
            total += 23
            continue
        prev_zwj = False
        for ch in part:
            cp = ord(ch)
            if cp in IGNORED:
                prev_zwj = cp == 0x200D
                continue
            if prev_zwj:           # element sekwencji emoji po ZWJ nie liczy sie osobno
                prev_zwj = False
                continue
            total += 1 if any(a <= cp <= b for a, b in LIGHT) else 2
    return total


EMOJI_RE = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿]')


def banned_phrases():
    """Frazy z list "Nie używać" w redakcja/opisy.md i redakcja/social.md."""
    phrases = []
    for name in ('opisy.md', 'social.md'):
        path = os.path.join(repo.REDAKCJA, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8') as f:
            text = f.read()
        for match in re.finditer(r'Nie używać.*?\n(.*?)\n\s*\n', text, re.DOTALL):
            phrases += [p.strip(' ,.…') for p in re.findall(r'„([^”]+)”', match.group(1)) if len(p.strip()) > 3]
    return phrases


def check_post(post, phrases):
    problems, warnings = [], []
    li = post.get('linkedin', '')
    if not li.strip():
        problems.append('pusty tekst LinkedIn')
    if URL_RE.search(li):
        problems.append('link w treści posta LinkedIn - przenieś go do pierwszego komentarza')
    if len(li) > LINKEDIN_MAX:
        problems.append('LinkedIn: %d znaków (limit %d)' % (len(li), LINKEDIN_MAX))
    first = li.strip().split('\n\n')[0] if li.strip() else ''
    if len(first) > LINKEDIN_FOLD:
        warnings.append('LinkedIn: pierwszy akapit ma %d znaków - haczyk powinien zmieścić się przed „…więcej” (~%d)'
                        % (len(first), LINKEDIN_FOLD))
    hashtags = [h for h in re.findall(r'(?<!\w)#\w+', li) if not re.fullmatch(r'#\d+', h)]   # "#44" to numer wydania
    if hashtags:
        warnings.append('LinkedIn: hashtagi %s - domyślnie bez hashtagów (social-platformy.md)' % ' '.join(hashtags))
    emoji = EMOJI_RE.findall(li)
    if len(emoji) > 5:
        warnings.append('LinkedIn: %d emoji - za dużo' % len(emoji))
    lower = (li + ' ' + ' '.join(post.get('x', []))).lower()
    for phrase in phrases:
        if phrase.lower() in lower:
            problems.append('zakazana fraza: „%s”' % phrase)
    if post.get('publikuj', True) and not URL_RE.search(post.get('komentarz', '')):
        warnings.append('pierwszy komentarz bez linku')
    tweets = post.get('x', [])
    if not tweets:
        problems.append('brak wątku na X')
    for i, tweet in enumerate(tweets, 1):
        n = x_length(tweet)
        if n > X_MAX:
            problems.append('X wpis %d: %d znaków (limit %d)' % (i, n, X_MAX))
        if URL_RE.search(tweet) and i != len(tweets):
            problems.append('X wpis %d: link tylko w ostatnim wpisie wątku' % i)
        if not tweet.strip():
            problems.append('X wpis %d: pusty' % i)
    image = post.get('obrazek') or {}
    if image.get('wybrany') == 'infografika' and not image.get('infografika'):
        problems.append('obrazek: wybrana infografika bez specyfikacji')
    if image.get('wybrany') == 'mem' and not (image.get('mem') or {}).get('tekst'):
        problems.append('obrazek: wybrany mem bez tekstu')
    return problems, warnings


def load(numer, ai=False):
    p = paths(numer)
    data = repo.read_json(p['posty_ai'] if ai else p['posty'])
    if not data:
        raise SystemExit('Brak %s' % os.path.relpath(p['posty_ai'] if ai else p['posty'], repo.ROOT))
    return data


def cmd_sprawdz(args):
    data = load(args.numer, args.ai)
    phrases = banned_phrases()
    bad = 0
    for post in data['posty']:
        problems, warnings = check_post(post, phrases)
        bad += len(problems)
        status = 'OK' if not problems else 'BŁĘDY'
        print('[%s] %s (%s)' % (status, post['id'], post.get('temat', '')))
        for p in problems:
            print('   ✗ ' + p)
        for w in warnings:
            print('   ! ' + w)
        print('   X: ' + ', '.join(str(x_length(t)) for t in post.get('x', [])))
    if bad:
        raise SystemExit(1)


def render_images(numer, data):
    from grafika import render
    out_dir = paths(numer)['obrazki']
    meta = repo.read_json(os.path.join(repo.issue_dir(numer), 'meta.json'), {}) or {}
    done = []
    for post in data['posty']:
        image = post.setdefault('obrazek', {})
        spec = image.get('infografika')
        if image.get('wybrany') == 'okladka':
            image['plik'] = '../okladka.jpeg'
        if image.get('wybrany') == 'mem' and (image.get('mem') or {}).get('plik'):
            image['plik'] = image['mem']['plik']      # gotowy mem zrobiony przez Kube (obrazki/<id>_mem.jpg)
        if not spec:
            continue
        spec = dict({'numer': meta.get('numer', numer)}, **spec)
        target = os.path.join(out_dir, '%s.png' % post['id'])
        render(spec, target)
        if image.get('wybrany') not in ('okladka', 'mem'):
            image['plik'] = 'obrazki/%s.png' % post['id']
        done.append(post['id'])
    return done


def cmd_grafiki(args):
    p = paths(args.numer)
    done = []
    for key in ('posty_ai', 'posty'):
        data = repo.read_json(p[key])
        if data:
            done = render_images(args.numer, data)
            repo.write_json(p[key], data)
    print('Infografiki: %s' % (', '.join(done) or 'brak'))


def cmd_scal(args):
    p = paths(args.numer)
    files = sorted(glob.glob(os.path.join(cache_dir(args.numer), 'robocze', '*.json')))
    if not files:
        raise SystemExit('Brak plików w .cache/social/%03d/robocze/' % args.numer)
    meta = repo.read_json(os.path.join(repo.issue_dir(args.numer), 'meta.json'), {}) or {}
    ai = repo.read_json(p['posty_ai']) or {'numer': args.numer, 'tytul': meta.get('tytul'), 'posty': []}
    work = repo.read_json(p['posty']) or {'numer': args.numer, 'tytul': meta.get('tytul'), 'status': 'robocze',
                                          'posty': []}
    known = {post['id'] for post in ai['posty']}
    added = []
    for path in files:
        post = repo.read_json(path)
        if post['id'] in known:
            continue
        post.setdefault('publikuj', True)
        post.setdefault('uwaga_kuby', '')
        post.setdefault('wynik', {})
        ai['posty'].append(post)
        work['posty'].append(json.loads(json.dumps(post)))
        known.add(post['id'])
        added.append(post['id'])
    order = lambda post: (post['rodzaj'] != 'glowny', post.get('termin') or '9999')  # noqa: E731
    ai['posty'].sort(key=order)
    work['posty'].sort(key=order)
    work['status'] = 'robocze'
    render_images(args.numer, ai)
    render_images(args.numer, work)
    repo.write_json(p['posty_ai'], ai)
    repo.write_json(p['posty'], work)
    print('Dołączono: %s' % (', '.join(added) or 'nic nowego'))


KUBA_FIELDS = ('publikuj', 'uwaga_kuby', 'wynik')


def cmd_podmien(args):
    p = paths(args.numer)
    data = load(args.numer)
    by_id = {post['id']: i for i, post in enumerate(data['posty'])}
    done = []
    for path in sorted(glob.glob(os.path.join(cache_dir(args.numer), 'poprawki', '*.json'))):
        new = repo.read_json(path)
        if new.get('id') not in by_id:
            print('Pomijam %s - nie ma takiego posta' % os.path.basename(path))
            continue
        old = data['posty'][by_id[new['id']]]
        for key in KUBA_FIELDS:
            if key in old:
                new[key] = old[key]
        new.pop('weryfikacja', None)          # stara weryfikacja nie dotyczy nowego tekstu
        data['posty'][by_id[new['id']]] = new
        os.remove(path)
        done.append(new['id'])
    render_images(args.numer, data)
    repo.write_json(p['posty'], data)
    print('Podmieniono: %s' % (', '.join(done) or 'nic'))


def cmd_weryfikacja(args):
    p = paths(args.numer)
    data = load(args.numer)
    by_id = {post['id']: post for post in data['posty']}
    done = []
    for path in sorted(glob.glob(os.path.join(cache_dir(args.numer), 'weryfikacja', '*.json'))):
        result = repo.read_json(path)
        if result.get('id') in by_id:
            by_id[result['id']]['weryfikacja'] = result
            bad = [f for f in result.get('fakty', []) if f.get('status') != 'potwierdzony']
            done.append('%s (%d/%d ok)' % (result['id'], len(result.get('fakty', [])) - len(bad), len(result.get('fakty', []))))
            for f in bad:
                print('  %s [%s] %s - %s' % (result['id'], f.get('status'), f.get('fakt'), f.get('uwaga', '')))
    repo.write_json(p['posty'], data)
    print('Weryfikacja: %s' % (', '.join(done) or 'brak wyników'))


def cmd_eksport(args):
    data = load(args.numer)
    lines = ['# Posty social — %s' % data.get('tytul', '#%s' % args.numer), '']
    for post in data['posty']:
        if not post.get('publikuj', True):
            continue
        image = post.get('obrazek') or {}
        lines += ['## %s — %s' % (post.get('termin', 'bez terminu'), post.get('temat') or post['id']), '']
        if post.get('link_newsa'):
            lines += ['Źródło: %s' % post['link_newsa'], '']
        facts = (post.get('weryfikacja') or {}).get('fakty', [])
        bad = [f for f in facts if f.get('status') != 'potwierdzony']
        if facts:
            lines += ['Weryfikacja faktów: %d/%d potwierdzone%s' % (len(facts) - len(bad), len(facts),
                      '' if not bad else ' — DO SPRAWDZENIA: ' + '; '.join(f['fakt'] for f in bad)), '']
        # tekst w bloku kodu: kopiowanie zachowuje puste linie miedzy akapitami (z renderowanego markdownu zlewaja sie w jeden)
        lines += ['### LinkedIn / Facebook / Substack Notes', '', '```text', post['linkedin'], '```', '',
                  '**Pierwszy komentarz:**', '', '```text', post.get('komentarz', ''), '```', '']
        lines += ['### X (wątek)', '']
        for i, tweet in enumerate(post.get('x', []), 1):
            lines += ['%d/ %s' % (i, tweet), '']
        chosen = image.get('wybrany', 'brak')
        lines += ['### Obrazek: %s' % chosen, '']
        if chosen in ('infografika', 'okladka', 'mem') and image.get('plik'):
            lines += ['![](%s)' % image['plik'], '']
        if chosen == 'prompt' and image.get('prompt'):
            lines += ['Prompt:', '', '```', image['prompt'], '```', '']
        if chosen == 'mem' and image.get('mem'):
            mem = image['mem']
            lines += ['Mem: %s%s' % (mem.get('szablon', ''), ' (%s)' % mem['link'] if mem.get('link') else ''), '',
                      '```', mem.get('tekst', ''), '```', '']
        lines += ['---', '']
    with open(paths(args.numer)['md'], 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('Zapisano %s' % os.path.relpath(paths(args.numer)['md'], repo.ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='polecenie', required=True)
    for name, func in (('sprawdz', cmd_sprawdz), ('scal', cmd_scal), ('grafiki', cmd_grafiki),
                       ('eksport', cmd_eksport), ('weryfikacja', cmd_weryfikacja), ('podmien', cmd_podmien)):
        p = sub.add_parser(name)
        p.add_argument('numer', type=int)
        if name == 'sprawdz':
            p.add_argument('--ai', action='store_true', help='sprawdz posty_ai.json')
        p.set_defaults(func=func)
    args = parser.parse_args()
    sys.path.insert(0, HERE)
    args.func(args)


if __name__ == '__main__':
    main()
