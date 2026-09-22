#!/usr/bin/env python3
"""Ktore newslettery faktycznie dostarczaja newsy do wydan, a ktore maja potencjal?

Wejscie:
    .cache/newslettery/maile.jsonl   (pobierz_maile.py)
    wydania/NNN/dane.csv, meta.json  (newsy opublikowane w wydaniach)

Trzy poziomy dopasowania maila do newsa z wydania:
    ZRODLO - ten sam link (takze po rozwinieciu trackera) albo temat maila = tytul artykulu
             (newsletter autorski na Substacku: mail JEST artykulem),
    TEMAT  - ten sam news opisany innymi slowami / z innym linkiem (podobienstwo TF-IDF
             tekstu wokol linku do tytulu i opisu oryginalu + nazw wlasnych z naszego opisu),
             w oknie 12 dni przed wydaniem. "pewne" od podobienstwa 0.30, nizej "prawdopodobne"
             (wymaga min. 2 rzadkich slow z tytulu; precyzja z recznej proby ok. 2/3).
    POTENCJAL - udzial linkow z probki ostatnich maili prowadzacych do domen, ktore
             czesto trafiaja do wydan, oraz udzial tresci o AI.

Wynik: .cache/newslettery/raport.json i tabela na stdout.

Uzycie:
    python3 narzedzia/newslettery/analizuj.py --wydania 29-38
"""
import argparse
import collections
import json
import math
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import repo  # noqa: E402
from lib.urlclean import HEADERS, clean_url, dedup_key, looks_like_redirect, resolve_redirect  # noqa: E402

CACHE_DIR = os.path.join(repo.ROOT, '.cache', 'newslettery')
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\.\-\$%]*[A-Za-z0-9%]|[A-Za-z0-9]")
STOPWORDS = set('''the a an and or of to in on for with by from at as is are was were be been its it this that
these those your you our we they their his her how why what who when new into about over after than more most
just now will can could not no all has have had via vs it's one two first says said say also up out ai'''.split())
NAV_HINTS = ('unsubscribe', 'preferences', 'view in browser', 'view online', 'advertise', 'sponsor', 'refer',
             'share', 'privacy', 'forward', 'subscribe', 'sign up', 'manage', 'read online', 'upgrade')
AI_RE = re.compile(r'\b(ai|llm|gpt|claude|gemini|openai|anthropic|model|agents?|agentic|nvidia|deepmind|copilot|'
                   r'cursor|chatbot|machine learning|neural|robot|humanoid)\b', re.IGNORECASE)
WINDOW = timedelta(days=12)
SURE = 0.30
CANDIDATE = 0.18


def tokens(text):
    return [w.lower().strip(".-'") for w in WORD_RE.findall(text or '')
            if w.lower() not in STOPWORDS and len(w) > 1]


def entities_pl(text):
    """Nazwy wlasne i liczby z polskiego tekstu - wspolne dla obu jezykow."""
    out = []
    for sentence in re.split(r'[.!?]\s+', text or ''):
        for i, word in enumerate(sentence.split()):
            word = re.sub(r'[^\w\.\-\$%]', '', word)
            if word and ((i > 0 and word[0].isupper()) or re.search(r'\d', word) or re.match(r'^[A-Z]{2,}', word)):
                out.append(word.lower().strip('.-'))
    return out


def sender_key(raw):
    return ' '.join((raw or '').replace('"', '').split())


def parse_range(spec):
    start, _, end = spec.partition('-')
    return range(int(start), int(end or start) + 1)


def fetch_page(url):
    import requests
    from bs4 import BeautifulSoup
    try:
        soup = BeautifulSoup(requests.get(url, headers=HEADERS, timeout=15).text[:400000], 'html.parser')

        def meta(*attrs):
            for attr in attrs:
                tag = soup.find('meta', attrs=attr)
                if tag and tag.get('content'):
                    return tag['content'].strip()
            return ''
        title = meta({'property': 'og:title'}, {'name': 'twitter:title'}) or (
            soup.title.get_text(strip=True) if soup.title else '')
        desc = meta({'property': 'og:description'}, {'name': 'description'}, {'name': 'twitter:description'})
        return {'title': title, 'desc': desc}
    except Exception:
        return {'title': '', 'desc': ''}


def load_news(numbers):
    cache_path = os.path.join(CACHE_DIR, 'strony.json')
    pages = repo.read_json(cache_path, {}) or {}
    news = []
    for n in numbers:
        meta = repo.read_json(os.path.join(repo.issue_dir(n), 'meta.json'))
        issue_date = datetime.strptime(meta['data'], '%Y-%m-%d')
        for row in repo.read_csv(os.path.join(repo.issue_dir(n), 'dane.csv')):
            news.append({'wydanie': n, 'data': issue_date, 'link': row['Link'], 'pl': row['Tytuł'], 'opis': row['Opis']})
    missing = [x['link'] for x in news if x['link'] not in pages]
    if missing:
        print('Pobieram tytuly i opisy oryginalow: %d stron' % len(missing), file=sys.stderr)
        with ThreadPoolExecutor(16) as pool:
            pages.update(zip(missing, pool.map(fetch_page, missing)))
        repo.write_json(cache_path, pages)
    for x in news:
        page = pages.get(x['link'], {})
        x['en'] = page.get('title', '') if len(page.get('title', '')) > 12 else ''
        profile = tokens(x['en']) * 2 + tokens(page.get('desc', '')) + entities_pl(x['pl']) * 2 + entities_pl(x['opis'][:400])
        x['profile'] = collections.Counter(profile)
        x['title_tokens'] = set(tokens(x['en'])) | set(entities_pl(x['pl'])) | set(tokens(x['pl']))
    return news


def mail_items(mails):
    """Pozycje tresci z maili: tekst wokol linku (bez nawigacji i stopek)."""
    items = []
    for m_idx, mail in enumerate(mails):
        seen = set()
        for link in mail['links']:
            text = (link['anchor'] + ' | ' + link['context']).strip(' |')
            low = text.lower()
            if len(link['context']) < 40 or (any(h in low for h in NAV_HINTS) and len(link['anchor']) < 40):
                continue
            if link['context'][:200] in seen:
                continue
            seen.add(link['context'][:200])
            items.append({'m': m_idx, 'href': link['href'], 'text': text[:700]})
    return items


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--wydania', default='29-38')
    args = parser.parse_args()

    news = load_news(parse_range(args.wydania))
    with open(os.path.join(CACHE_DIR, 'maile.jsonl'), encoding='utf-8') as f:
        mails = [json.loads(line) for line in f if line.strip()]
    for mail in mails:
        mail['_date'] = datetime.fromtimestamp(mail['internal_date'] / 1000)
        mail['_sender'] = sender_key(mail['sender'])
    items = mail_items(mails)
    print('Maili: %d, pozycji tresci: %d, newsow z wydan %s: %d'
          % (len(mails), len(items), args.wydania, len(news)), file=sys.stderr)

    by_key = {dedup_key(x['link']): i for i, x in enumerate(news)}
    resolved_path = os.path.join(CACHE_DIR, 'przekierowania.json')
    resolved = repo.read_json(resolved_path, {}) or {}
    hits = collections.defaultdict(dict)   # news -> nadawca -> (czas, poziom)
    rank = {'zrodlo': 0, 'pewne': 1, 'prawdopodobne': 2}

    def hit(n_idx, mail, level):
        prev = hits[n_idx].get(mail['_sender'])
        if prev is None or rank[level] < rank[prev[1]] or (level == prev[1] and mail['internal_date'] < prev[0]):
            hits[n_idx][mail['_sender']] = (mail['internal_date'], level)

    # 1. ZRODLO: link wprost albo temat maila = tytul artykulu
    titles = [set(tokens(x['en'].split('|')[0].split(' - ')[0])) for x in news]
    for mail in mails:
        for link in mail['links']:
            n_idx = by_key.get(dedup_key(link['href']))
            if n_idx is None and link['href'] in resolved:
                n_idx = by_key.get(dedup_key(resolved[link['href']]))
            if n_idx is not None:
                hit(n_idx, mail, 'zrodlo')
        subject = set(tokens(mail['subject']))
        if len(subject) >= 3:
            for n_idx, x in enumerate(news):
                title = titles[n_idx]
                if len(title) >= 3 and len(subject & title) / len(title) >= 0.7 \
                        and x['data'] - timedelta(days=14) <= mail['_date'] <= x['data']:
                    hit(n_idx, mail, 'zrodlo')

    # 2. TEMAT: TF-IDF tekstu wokol linku vs profil newsa
    df = collections.Counter()
    for item in items:
        item['tf'] = collections.Counter(tokens(item['text']))
        df.update(set(item['tf']))
    total = len(items)

    def idf(t):
        return math.log((total + 1) / (df.get(t, 0) + 1)) + 1

    def vector(counts):
        vec = {t: (1 + math.log(f)) * idf(t) for t, f in counts.items()}
        return vec, math.sqrt(sum(v * v for v in vec.values())) or 1

    inverted = collections.defaultdict(list)
    for n_idx, x in enumerate(news):
        x['vec'], x['norm'] = vector(x['profile'])
        for t in x['vec']:
            inverted[t].append(n_idx)

    candidates = []
    for item in items:
        vec, norm = vector(item['tf'])
        mail = mails[item['m']]
        dots, shared = collections.defaultdict(float), collections.defaultdict(list)
        for t, w in vec.items():
            for n_idx in inverted.get(t, ()):
                dots[n_idx] += w * news[n_idx]['vec'][t]
                shared[n_idx].append(t)
        for n_idx, dot in dots.items():
            x = news[n_idx]
            if not x['data'] - WINDOW <= mail['_date'] <= x['data']:
                continue
            score = dot / (norm * x['norm'])
            rare = [t for t in shared[n_idx] if idf(t) > 5]
            if score < CANDIDATE or len(rare) < 2:
                continue
            from_title = [t for t in rare if t in x['title_tokens']]
            if score >= SURE:
                hit(n_idx, mail, 'pewne')
            elif len(rare) >= 3 and len(from_title) >= 2:
                hit(n_idx, mail, 'prawdopodobne')
            else:
                continue
            if looks_like_redirect(item['href']) and item['href'] not in resolved:
                candidates.append(item['href'])

    # rozwiniecie przekierowan kandydatow - moze zamienic TEMAT w ZRODLO
    candidates = sorted(set(candidates))
    if candidates:
        print('Rozwijam %d przekierowan kandydatow' % len(candidates), file=sys.stderr)
        with ThreadPoolExecutor(16) as pool:
            resolved.update(zip(candidates, pool.map(resolve_redirect, candidates)))
        repo.write_json(resolved_path, resolved)
    for mail in mails:
        for link in mail['links']:
            target = resolved.get(link['href'])
            n_idx = by_key.get(dedup_key(target)) if target else None
            if n_idx is not None:
                hit(n_idx, mail, 'zrodlo')

    # 3. POTENCJAL: domeny linkow z probki ostatnich maili
    known_domains = collections.Counter()
    for folder in repo.issue_dirs():
        for row in repo.read_csv(os.path.join(folder, 'dane.csv')):
            known_domains[urlparse(row['Link']).netloc.lower().replace('www.', '')] += 1
    by_sender = collections.defaultdict(list)
    for m_idx, mail in enumerate(mails):
        by_sender[mail['_sender']].append(m_idx)
    latest_by_sender = {s: set(sorted(idxs, key=lambda i: -mails[i]['internal_date'])[:4])
                        for s, idxs in by_sender.items()}
    sample = collections.defaultdict(list)
    recent_texts = collections.defaultdict(list)
    for item in items:
        sender = mails[item['m']]['_sender']
        if item['m'] in latest_by_sender[sender]:
            recent_texts[sender].append(item['text'])
            if len(sample[sender]) < 25:
                sample[sender].append(item['href'])
    todo = sorted({h for hs in sample.values() for h in hs if looks_like_redirect(h) and h not in resolved})
    if todo:
        print('Rozwijam probke linkow do oceny potencjalu: %d' % len(todo), file=sys.stderr)
        with ThreadPoolExecutor(24) as pool:
            resolved.update(zip(todo, pool.map(resolve_redirect, todo)))
        repo.write_json(resolved_path, resolved)

    first, unique = collections.Counter(), collections.Counter()
    for n_idx, senders in hits.items():
        first[min(senders, key=lambda s: senders[s][0])] += 1
        if len(senders) == 1:
            unique[next(iter(senders))] += 1

    report = []
    weeks = max(1, (max(m['_date'] for m in mails) - min(m['_date'] for m in mails)).days / 7)
    for sender, idxs in by_sender.items():
        levels = collections.Counter()
        examples = []
        for n_idx, senders in hits.items():
            if sender in senders:
                levels[senders[sender][1]] += 1
                if len(examples) < 6:
                    examples.append('#%d %s' % (news[n_idx]['wydanie'], news[n_idx]['pl']))
        domains = [urlparse(resolved.get(h, clean_url(h))).netloc.lower().replace('www.', '') for h in sample[sender]]
        contexts = recent_texts[sender]
        last = mails[max(idxs, key=lambda i: mails[i]['internal_date'])]
        report.append({
            'nadawca': sender,
            'maile': len(idxs),
            'na_tydzien': round(len(idxs) / weeks, 1),
            'zrodlo': levels['zrodlo'],
            'temat_pewny': levels['zrodlo'] + levels['pewne'],
            'temat_wszystkie': sum(levels.values()),
            'pierwszy': first[sender],
            'unikalne': unique[sender],
            'znane_domeny_pct': round(100 * sum(known_domains.get(d, 0) >= 2 for d in domains) / len(domains)) if domains else None,
            'ai_pct': round(100 * sum(bool(AI_RE.search(c)) for c in contexts) / len(contexts)) if contexts else 0,
            'top_domeny': collections.Counter(domains).most_common(4),
            'przyklady': examples,
            'tematy_maili': [mails[i]['subject'] for i in sorted(idxs, key=lambda i: -mails[i]['internal_date'])[:4]],
            'wypis': last.get('list_unsubscribe', ''),
            'wypis_one_click': 'One-Click' in (last.get('list_unsubscribe_post') or ''),
        })
    report.sort(key=lambda r: (-r['zrodlo'], -r['temat_wszystkie'], -r['maile']))
    repo.write_json(os.path.join(CACHE_DIR, 'raport.json'),
                    {'wydania': args.wydania, 'newsy': len(news), 'newsy_w_mailach': len(hits), 'nadawcy': report})

    print('Newsy z wydan %s znalezione w mailach: %d/%d' % (args.wydania, len(hits), len(news)))
    print('%5s %5s %6s %5s %5s %5s %5s %5s %4s  %s' % ('MAILE', '/TYDZ', 'ZRODLO', 'TEMAT', 'T+PR', '1SZY',
                                                      'UNIK', 'DOM%', 'AI%', 'NADAWCA'))
    for r in report:
        print('%5d %5s %6d %5d %5d %5d %5d %5s %4d  %s' % (
            r['maile'], r['na_tydzien'], r['zrodlo'], r['temat_pewny'], r['temat_wszystkie'], r['pierwszy'],
            r['unikalne'], r['znane_domeny_pct'] if r['znane_domeny_pct'] is not None else '-', r['ai_pct'],
            r['nadawca'][:60]))


if __name__ == '__main__':
    main()
