#!/usr/bin/env python3
"""Nowe wpisy ze stron z redakcja/strony.json od dnia przed ostatnim wydaniem -> .cache/strony/wynik.json

Dla kazdej strony:
    feed  - kanal RSS/Atom: tytul, link i data wprost z kanalu,
    html  - linki z listingu; data z listingu (<time>, tekst daty), z adresu (/2026/09/22/)
            albo ze strony artykulu (article:published_time, JSON-LD, <time>),
    przegladarka - strona blokuje pobieranie; wpisy zbiera Claude przez Chrome
            i zapisuje do .cache/strony/przegladarka.json (patrz skill przeglad-stron).

Wpisy bez ustalonej daty NIE sa brane (liczone w statystyce strony). Strona, z ktorej nie udalo sie
wyciagnac zadnego wpisu albo zadnej daty, dostaje status "problem" - do sprawdzenia w przegladarce.

Uzycie:
    python3 narzedzia/strony/zbierz.py                 # od dnia przed ostatnim wydaniem
    python3 narzedzia/strony/zbierz.py --od 2026-09-17
    python3 narzedzia/strony/zbierz.py --strona Cursor # tylko wybrane (fragment nazwy)
"""
import argparse
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from urllib.parse import urljoin, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402
from dateutil import parser as dateparser  # noqa: E402

from lib import repo  # noqa: E402
from lib.urlclean import HEADERS, clean_url, dedup_key  # noqa: E402

CONFIG = os.path.join(repo.REDAKCJA, 'strony.json')
CACHE = os.path.join(repo.ROOT, '.cache', 'strony')
WYNIK = os.path.join(CACHE, 'wynik.json')
ARTYKULY = os.path.join(CACHE, 'artykuly.json')
MAX_LINKS = 25

PL_MONTHS = {'sty': 1, 'lut': 2, 'mar': 3, 'kwi': 4, 'maj': 5, 'cze': 6, 'lip': 7, 'sie': 8, 'wrz': 9,
             'paź': 10, 'paz': 10, 'lis': 11, 'gru': 12}
DATE_PATTERNS = [
    re.compile(r'\b(20\d\d)-(\d\d)-(\d\d)'),                                              # 2026-09-22
    re.compile(r'\b(\d{1,2})\.(\d{1,2})\.(20\d\d)\b'),                                    # 22.09.2026
    re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.? (\d{1,2}),? (20\d\d)', re.I),
    re.compile(r'\b(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?,? (20\d\d)', re.I),
    re.compile(r'\b(\d{1,2}) (sty|lut|mar|kwi|maj|cze|lip|sie|wrz|paź|paz|lis|gru)[a-ząćęłńóśźż]*\.? (20\d\d)', re.I),
]
URL_DATE = re.compile(r'/(20\d\d)/(\d\d)/(\d\d)?/?')
NAV_WORDS = ('subscribe', 'newsletter', 'sign in', 'log in', 'privacy', 'cookie', 'careers', 'contact',
             'pricing', 'przejdź do', 'zaloguj', 'polityka', 'regulamin', 'kontakt')


def text_date(text):
    """Pierwsza data w tekscie (angielska, polska, ISO, dd.mm.rrrr) albo None."""
    for i, pattern in enumerate(DATE_PATTERNS):
        match = pattern.search(text or '')
        if not match:
            continue
        g = match.groups()
        try:
            if i == 0:
                return date(int(g[0]), int(g[1]), int(g[2]))
            if i == 1:
                return date(int(g[2]), int(g[1]), int(g[0]))
            if i == 4:
                return date(int(g[2]), PL_MONTHS[g[1].lower()[:3]], int(g[0]))
            return dateparser.parse(re.sub(r'\bSept\b', 'Sep', match.group(0))).date()
        except (ValueError, KeyError, OverflowError):
            continue
    return None


def parse_any_date(value):
    try:
        parsed = dateparser.parse(value)
        return parsed.astimezone().date() if parsed.tzinfo else parsed.date()
    except (ValueError, TypeError, OverflowError):
        return text_date(value)


def clean_text(value, limit=400):
    text = BeautifulSoup(html.unescape(value or ''), 'html.parser').get_text(' ')
    text = ' '.join(text.split())
    return text[:limit] + ('…' if len(text) > limit else '')


def get(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp


# --- kanaly RSS/Atom -------------------------------------------------------------

def local(tag):
    return tag.rsplit('}', 1)[-1]


def child(node, *names):
    for el in node:
        if local(el.tag) in names:
            return el
    return None


def parse_feed(xml_text, base):
    root = ET.fromstring(xml_text.encode('utf-8') if isinstance(xml_text, str) else xml_text)
    items = []
    for node in root.iter():
        if local(node.tag) not in ('item', 'entry'):
            continue
        title = child(node, 'title')
        link = None
        for el in node:
            if local(el.tag) == 'link':
                if el.get('href') and el.get('rel', 'alternate') == 'alternate':
                    link = el.get('href')
                    break
                if el.text and el.text.strip():
                    link = el.text.strip()
        if not link:
            guid = child(node, 'guid', 'id')
            link = guid.text.strip() if guid is not None and guid.text and guid.text.startswith('http') else None
        stamp = child(node, 'pubDate', 'published', 'date', 'issued', 'updated')
        summary = child(node, 'description', 'summary', 'content', 'encoded')
        if not link or title is None:
            continue
        items.append({
            'tytul': clean_text(title.text or ''.join(title.itertext()), 300),
            'link': urljoin(base, link),
            'data': parse_any_date(stamp.text) if stamp is not None and stamp.text else None,
            'opis': clean_text(summary.text if summary is not None else ''),
        })
    return items


def feed_pages(feed_url, base, since, max_pages=5):
    """Kanal z kolejnymi stronami (WordPress: ?paged=N), dopoki nie dojdziemy do wpisow sprzed `since`."""
    items = parse_feed(get(feed_url).content, base)
    seen = {dedup_key(i['link']) for i in items}
    for page in range(2, max_pages + 1):
        dated = [i['data'] for i in items if i['data']]
        if not dated or min(dated) < since:
            break
        try:
            more = parse_feed(get('%s%spaged=%d' % (feed_url, '&' if '?' in feed_url else '?', page)).content, base)
        except Exception:
            break
        fresh = [i for i in more if dedup_key(i['link']) not in seen]
        if not fresh:
            break
        seen.update(dedup_key(i['link']) for i in fresh)
        items.extend(fresh)
    return items


# --- strony HTML -----------------------------------------------------------------

def listing_links(url, page, filtr=None):
    soup = BeautifulSoup(page, 'html.parser')
    for tag in soup.find_all(['nav', 'footer', 'header', 'script', 'style']):
        tag.decompose()
    base_host = urlparse(url).netloc.replace('www.', '')
    base_path = urlparse(url).path.rstrip('/')
    seen, out = set(), []
    for a in soup.find_all('a', href=True):
        href = urljoin(url, a['href']).split('#')[0]
        parsed = urlparse(href)
        if parsed.netloc.replace('www.', '') != base_host or parsed.path.rstrip('/') in ('', base_path):
            continue
        if filtr and filtr not in href:
            continue
        text = ' '.join(a.get_text(' ').split())
        if len(text) < 20 or any(w in text.lower() for w in NAV_WORDS):
            continue
        if re.search(r'/(tag|tags|category|categories|author|page|kategoria|autor)/', parsed.path):
            continue
        key = dedup_key(href)
        if key in seen:
            continue
        seen.add(key)
        # data z listingu: <time> albo tekst daty w najblizszym kontenerze
        found = None
        node = a
        for _ in range(4):
            if node is None:
                break
            time_tag = node.find('time') if hasattr(node, 'find') else None
            if time_tag is not None:
                found = parse_any_date(time_tag.get('datetime') or time_tag.get_text())
            if not found:
                snippet = node.get_text(' ')
                if len(snippet) < 600:
                    found = text_date(snippet)
            if found:
                break
            node = node.parent
        match = URL_DATE.search(parsed.path)
        if not found and match and match.group(3):
            found = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        out.append({'tytul': text[:300], 'link': href, 'data': found, 'opis': ''})
        if len(out) >= MAX_LINKS:
            break
    return out


def article_meta(url, cache):
    """Data publikacji, tytul i opis ze strony artykulu (z cache - kazdy artykul pobieramy raz)."""
    if url in cache:
        return cache[url]
    result = {'data': None, 'tytul': '', 'opis': ''}
    try:
        soup = BeautifulSoup(get(url).text[:600000], 'html.parser')

        def meta(*attrs):
            for attr in attrs:
                tag = soup.find('meta', attrs=attr)
                if tag and tag.get('content'):
                    return tag['content'].strip()
            return ''
        stamp = meta({'property': 'article:published_time'}, {'name': 'article:published_time'},
                     {'itemprop': 'datePublished'}, {'name': 'date'}, {'name': 'pubdate'},
                     {'property': 'og:published_time'}, {'name': 'publish-date'})
        if not stamp:
            for script in soup.find_all('script', type='application/ld+json'):
                found = re.search(r'"datePublished"\s*:\s*"([^"]+)"', script.string or '')
                if found:
                    stamp = found.group(1)
                    break
        if not stamp:
            time_tag = soup.find('time')
            if time_tag:
                stamp = time_tag.get('datetime') or time_tag.get_text()
        day = parse_any_date(stamp) if stamp else None
        result = {'data': day.isoformat() if day else None,
                  'tytul': meta({'property': 'og:title'}, {'name': 'twitter:title'}) or (soup.title.get_text(strip=True) if soup.title else ''),
                  'opis': meta({'property': 'og:description'}, {'name': 'description'})[:400]}
    except Exception:
        pass
    cache[url] = result
    return result


# --- przebieg dla jednej strony ---------------------------------------------------

def collect_site(site, since, articles):
    info = {'nazwa': site['nazwa'], 'url': site['url'], 'status': 'ok', 'komunikat': '', 'sprawdzono': 0,
            'bez_daty': 0, 'najnowszy': None, 'nowe': []}
    if site.get('przegladarka'):
        info.update(status='przegladarka', komunikat='strona blokuje pobieranie - wpisy zbiera Claude przez Chrome')
        return info
    try:
        if site.get('feed'):
            items = feed_pages(site['feed'], site['url'], since)
            info['tryb'] = 'feed'
        else:
            items = listing_links(site['url'], get(site['url']).text, site.get('filtr'))
            info['tryb'] = 'html'
        # kanal bez dat (np. Google for Developers) albo listing bez dat: data ze strony artykulu
        for item in items[:MAX_LINKS]:
            if item['data'] is None:
                found = article_meta(item['link'], articles)
                item['data'] = date.fromisoformat(found['data']) if found['data'] else None
    except requests.HTTPError as exc:
        info.update(status='blad', komunikat='HTTP %s' % exc.response.status_code)
        return info
    except Exception as exc:
        info.update(status='blad', komunikat=str(exc)[:160])
        return info

    info['sprawdzono'] = len(items)
    dated = [i for i in items if i['data']]
    info['bez_daty'] = len(items) - len(dated)
    if dated:
        info['najnowszy'] = max(i['data'] for i in dated).isoformat()
    if not items:
        info.update(status='problem', komunikat='nie znaleziono żadnych wpisów - układ strony mógł się zmienić')
    elif not dated:
        info.update(status='problem', komunikat='żaden wpis nie ma daty - sprawdź w przeglądarce')
    elif min(i['data'] for i in dated) >= since:
        info.update(status='uwaga', komunikat='wszystkie %d pobrane wpisy są nowe - mogło coś umknąć, '
                                              'przejrzyj stronę ręcznie' % len(dated))

    fresh = [i for i in dated if i['data'] >= since]
    for item in fresh:
        if info.get('tryb') == 'html' or not item['opis']:
            found = article_meta(item['link'], articles)
            item['tytul'] = found['tytul'] or item['tytul']
            item['opis'] = item['opis'] or found['opis']
        item['data'] = item['data'].isoformat()
        item['link'] = clean_url(item['link'])
    fresh.sort(key=lambda i: i['data'], reverse=True)
    info['nowe'] = fresh
    return info


def default_since():
    last = repo.last_issue()
    if not last:
        return date.today() - timedelta(days=8)
    return date.fromisoformat(last['data']) - timedelta(days=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--od', help='RRRR-MM-DD (domyślnie dzień przed ostatnim wydaniem)')
    parser.add_argument('--strona', help='tylko strony, których nazwa zawiera ten tekst')
    args = parser.parse_args()

    since = date.fromisoformat(args.od) if args.od else default_since()
    sites = repo.read_json(CONFIG)['strony']
    if args.strona:
        sites = [s for s in sites if args.strona.lower() in s['nazwa'].lower()]
    os.makedirs(CACHE, exist_ok=True)
    articles = repo.read_json(ARTYKULY, {}) or {}

    with ThreadPoolExecutor(10) as pool:
        results = list(pool.map(lambda s: collect_site(s, since, articles), sites))
    repo.write_json(ARTYKULY, articles)

    # oznacz linki, ktore juz sa w data.csv albo byly w wydaniach
    known = set()
    if os.path.exists(repo.DATA_CSV):
        with open(repo.DATA_CSV, encoding='utf-8') as f:
            known |= {dedup_key(u) for u in re.findall(r'https?://\S+', f.read())}
    published = {dedup_key(u) for u in repo.published_links()}
    for site in results:
        for item in site['nowe']:
            key = dedup_key(item['link'])
            item['w_data_csv'] = key in known
            item['opublikowany'] = key in published

    previous = repo.read_json(WYNIK, {}) or {}
    if args.strona and previous.get('od') == since.isoformat():
        merged = {s['nazwa']: s for s in previous.get('strony', [])}
        merged.update({s['nazwa']: s for s in results})
        results = [merged[s['nazwa']] for s in repo.read_json(CONFIG)['strony'] if s['nazwa'] in merged]
    repo.write_json(WYNIK, {'od': since.isoformat(), 'wygenerowano': datetime.now().isoformat(timespec='seconds'),
                            'strony': results})

    print('Wpisy od %s' % since.isoformat())
    print('%-13s %5s %5s %6s %-11s  %s' % ('STATUS', 'NOWE', 'SPR.', 'BEZ D.', 'NAJNOWSZY', 'STRONA'))
    for s in results:
        print('%-13s %5d %5d %6d %-11s  %s %s' % (s['status'], len(s['nowe']), s['sprawdzono'], s['bez_daty'],
                                                 s['najnowszy'] or '-', s['nazwa'],
                                                 ('- ' + s['komunikat']) if s['komunikat'] else ''))
    print('Razem nowych wpisów: %d' % sum(len(s['nowe']) for s in results))


if __name__ == '__main__':
    main()
