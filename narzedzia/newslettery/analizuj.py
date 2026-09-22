#!/usr/bin/env python3
"""Ktore newslettery faktycznie dostarczaja newsy do wydan?

Wejscie:
    .cache/newslettery/maile.jsonl   (pobierz_maile.py)
    wydania/NNN/dane.csv             (linki opublikowane w wydaniach)

Dopasowanie linku z maila do newsa z wydania, od najtanszego:
    1. ten sam znormalizowany URL,
    2. podobienstwo tekstu wokol linku do ORYGINALNEGO tytulu strony
       (nasze tytuly sa po polsku, maile po angielsku), a dla linkow
       w trackerach - rozwiniecie przekierowania i potwierdzenie URL-em.
       Samo podobienstwo tekstu liczy sie jako trafienie dopiero od progu --prog-tekst.

Wynik: .cache/newslettery/raport.json i tabela na stdout.

Uzycie:
    python3 narzedzia/newslettery/analizuj.py --wydania 29-38
"""
import argparse
import collections
import csv
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.urlclean import clean_url, dedup_key, looks_like_redirect, resolve_redirect  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CACHE_DIR = os.path.join(ROOT, '.cache', 'newslettery')

WORD_RE = re.compile(r'[a-z0-9ąćęłńóśźż][a-z0-9ąćęłńóśźż\-\.]+', re.IGNORECASE)
STOPWORDS = set('''the a an and or of to in on for with by from at as is are was were be been
its it this that these those your you our we they their his her how why what who when new
into about over after than more most just now will can could not no all has have had
via vs de la le et w i z na do o po się jak co od dla'''.split())
NAV_HINTS = ('unsubscribe', 'preferences', 'view in browser', 'view online', 'advertise',
             'sponsor', 'refer', 'share', 'privacy', 'forward', 'subscribe', 'sign up')


def tokens(text):
    return {t.strip('.-').lower() for t in WORD_RE.findall(text or '')} - STOPWORDS - {''}


def parse_range(spec):
    start, _, end = spec.partition('-')
    return range(int(start), int(end or start) + 1)


def load_published(numbers):
    items = []
    for n in numbers:
        path = os.path.join(ROOT, 'wydania', '%03d' % n, 'dane.csv')
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                items.append({'wydanie': n, 'link': clean_url(row['Link']), 'tytul_pl': row['Tytuł']})
    return items


def fetch_title(url):
    import requests
    from bs4 import BeautifulSoup
    from lib.urlclean import HEADERS
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text[:300000], 'html.parser')
        for attrs in ({'property': 'og:title'}, {'name': 'twitter:title'}):
            meta = soup.find('meta', attrs=attrs)
            if meta and meta.get('content'):
                return meta['content'].strip()
        return soup.title.get_text(strip=True) if soup.title else ''
    except Exception:
        return ''


def original_titles(items):
    """Oryginalne tytuly stron, z cache - pobierane tylko raz."""
    cache_path = os.path.join(CACHE_DIR, 'tytuly.json')
    cache = json.load(open(cache_path, encoding='utf-8')) if os.path.exists(cache_path) else {}
    missing = [i['link'] for i in items if i['link'] not in cache]
    if missing:
        print('Pobieram oryginalne tytuly: %d stron' % len(missing), file=sys.stderr)
        with ThreadPoolExecutor(16) as pool:
            for url, title in zip(missing, pool.map(fetch_title, missing)):
                cache[url] = title
        json.dump(cache, open(cache_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return cache


def sender_key(raw):
    return ' '.join((raw or '').replace('"', '').split())


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--wydania', default='29-38')
    parser.add_argument('--prog', type=float, default=0.6,
                        help='od jakiej czesci slow tytulu rozwijamy przekierowanie linku')
    parser.add_argument('--prog-tekst', type=float, default=0.85,
                        help='od jakiej czesci slow tytulu uznajemy trafienie bez zgodnosci URL-a')
    args = parser.parse_args()

    published = load_published(parse_range(args.wydania))
    titles = original_titles(published)
    by_key = {dedup_key(p['link']): idx for idx, p in enumerate(published)}

    # indeks odwrocony: slowo z tytulu -> newsy
    title_tokens = []
    inverted = collections.defaultdict(set)
    for idx, item in enumerate(published):
        toks = tokens(titles.get(item['link'], ''))
        # tytuly stron X/LinkedIn bywaja bezuzyteczne ("X", "LinkedIn") - wtedy tylko URL
        if len(toks) < 3:
            toks = set()
        title_tokens.append(toks)
        for tok in toks:
            inverted[tok].add(idx)

    with open(os.path.join(CACHE_DIR, 'maile.jsonl'), encoding='utf-8') as f:
        mails = [json.loads(line) for line in f if line.strip()]
    print('Maili: %d, newsow z wydan %s: %d' % (len(mails), args.wydania, len(published)),
          file=sys.stderr)

    hits = []           # (mail_idx, news_idx, rodzaj)
    to_resolve = {}     # href -> [(mail_idx, news_idx, podobienstwo)]
    content_links = collections.Counter()

    for m_idx, mail in enumerate(mails):
        seen_news = set()
        for link in mail['links']:
            href = link['href']
            label = (link['anchor'] + ' ' + link['context']).lower()
            if any(h in label for h in NAV_HINTS) and len(link['anchor']) < 40:
                continue
            content_links[m_idx] += 1

            n_idx = by_key.get(dedup_key(href))
            if n_idx is not None and n_idx not in seen_news:
                seen_news.add(n_idx)
                hits.append((m_idx, n_idx, 'url'))
                continue

            ctx = tokens(link['anchor'] + ' ' + link['context'])
            counts = collections.Counter()
            for tok in ctx:
                for cand in inverted.get(tok, ()):
                    counts[cand] += 1
            for cand, overlap in counts.items():
                if cand in seen_news or overlap < 3:
                    continue
                score = overlap / len(title_tokens[cand])
                if score < args.prog:
                    continue
                if looks_like_redirect(href):
                    to_resolve.setdefault(href, []).append((m_idx, cand, score))
                elif score >= args.prog_tekst:
                    seen_news.add(cand)
                    hits.append((m_idx, cand, 'tekst'))

    resolved_path = os.path.join(CACHE_DIR, 'przekierowania.json')
    resolved = json.load(open(resolved_path, encoding='utf-8')) if os.path.exists(resolved_path) else {}
    hrefs = [h for h in to_resolve if h not in resolved]
    print('Rozwijam %d przekierowan kandydatow (%d z cache)'
          % (len(hrefs), len(to_resolve) - len(hrefs)), file=sys.stderr)
    with ThreadPoolExecutor(16) as pool:
        resolved.update(zip(hrefs, pool.map(resolve_redirect, hrefs)))
    json.dump(resolved, open(resolved_path, 'w', encoding='utf-8'), indent=0)

    confirmed = set()
    for href, candidates in to_resolve.items():
        target = by_key.get(dedup_key(resolved[href]))
        for m_idx, n_idx, score in candidates:
            if (m_idx, n_idx) in confirmed:
                continue
            if target == n_idx:
                hits.append((m_idx, n_idx, 'url'))
            elif score >= args.prog_tekst:
                # inny URL, ale ten sam temat opisany obok linku - to nadal ten news
                hits.append((m_idx, n_idx, 'tekst'))
            else:
                continue
            confirmed.add((m_idx, n_idx))

    # agregacja per nadawca
    senders = collections.defaultdict(lambda: {'maile': 0, 'linki_tresci': 0, 'dlugosc_tekstu': 0,
                                               'newsy': set(), 'newsy_url': set(), 'tematy': [],
                                               'ostatni_mail': 0, 'ostatnie_trafienie': 0,
                                               'wypis': '', 'wypis_post': ''})
    for m_idx, mail in enumerate(mails):
        s = senders[sender_key(mail['sender'])]
        s['maile'] += 1
        s['linki_tresci'] += content_links[m_idx]
        s['dlugosc_tekstu'] += mail.get('text_len', 0)
        s['ostatni_mail'] = max(s['ostatni_mail'], mail['internal_date'])
        s['wypis'] = s['wypis'] or mail.get('list_unsubscribe', '')
        s['wypis_post'] = s['wypis_post'] or mail.get('list_unsubscribe_post', '')
        if len(s['tematy']) < 4:
            s['tematy'].append(mail['subject'])

    news_sources = collections.defaultdict(set)
    for m_idx, n_idx, kind in hits:
        key = sender_key(mails[m_idx]['sender'])
        senders[key]['newsy'].add(n_idx)
        if kind == 'url':
            senders[key]['newsy_url'].add(n_idx)
        senders[key]['ostatnie_trafienie'] = max(senders[key]['ostatnie_trafienie'],
                                                 mails[m_idx]['internal_date'])
        news_sources[n_idx].add(key)

    def day(ms):
        return datetime.fromtimestamp(ms / 1000).strftime('%Y-%m-%d') if ms else ''

    report = []
    for key, s in senders.items():
        unique = [n for n in s['newsy'] if len(news_sources[n]) == 1]
        report.append({
            'nadawca': key,
            'maile': s['maile'],
            'linki_na_mail': round(s['linki_tresci'] / s['maile'], 1),
            'tekst_na_mail': s['dlugosc_tekstu'] // s['maile'],
            'trafienia': len(s['newsy']),
            'trafienia_url': len(s['newsy_url']),
            'unikalne': len(unique),
            'ostatnie_trafienie': day(s['ostatnie_trafienie']),
            'ostatni_mail': day(s['ostatni_mail']),
            'przyklady_trafien': [published[n]['tytul_pl'] for n in sorted(s['newsy'])][:5],
            'tematy_maili': s['tematy'],
            'wypis': s['wypis'],
            'wypis_one_click': 'One-Click' in s['wypis_post'],
        })
    report.sort(key=lambda r: (-r['trafienia'], -r['maile']))

    covered = len(news_sources)
    json.dump({'wydania': args.wydania, 'newsy': len(published), 'newsy_znalezione_w_mailach': covered,
               'nadawcy': report}, open(os.path.join(CACHE_DIR, 'raport.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    print('Newsy z wydan znalezione w mailach: %d/%d' % (covered, len(published)))
    print('%-5s %-5s %-5s %-5s %-6s %-11s %s' % ('MAILE', 'TRAF', 'URL', 'UNIK', 'L/MAIL', 'OST.TRAF', 'NADAWCA'))
    for r in report:
        print('%-5d %-5d %-5d %-5d %-6s %-11s %s' % (r['maile'], r['trafienia'], r['trafienia_url'],
                                                     r['unikalne'], r['linki_na_mail'],
                                                     r['ostatnie_trafienie'] or '-', r['nadawca'][:70]))


if __name__ == '__main__':
    main()
