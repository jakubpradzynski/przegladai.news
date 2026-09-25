"""Czy dany news byl juz w ostatnich wydaniach - takze pod innym linkiem?

Porownanie po temacie (TF-IDF): tekst kandydata (tytul + opis, dowolny jezyk) vs profil newsa z wydania
(nasz polski tytul i nazwy wlasne z opisu + oryginalny tytul i opis strony, pobierane raz do cache).
Uzywane w przegladzie stron (preselekcja) i w /zbierz-dane (scal_opisy).

    from lib import tematy
    checker = tematy.Wydania(ostatnie=2)
    checker.sprawdz(link, 'Apple launches new Siri ...')
      -> {'poziom': 'link'|'pewne'|'mozliwe', 'wydanie': 38, 'tytul': '...', 'podobienstwo': 0.41} albo None

Poziomy (skalibrowane na przegladzie stron z wrzesnia 2026):
    link    - ten sam adres; pewny duplikat,
    pewne   - podobienstwo >= 0.40 i min. 2 wspolne slowa z tytulu; traktujemy jako duplikat,
    mozliwe - 0.20-0.40; czesto inne wydarzenie o podobnych slowach -> tylko podpowiedz, nie odrzucenie.
"""
import collections
import math
import os
import re
from concurrent.futures import ThreadPoolExecutor

from . import repo
from .urlclean import HEADERS, dedup_key

CACHE = os.path.join(repo.ROOT, '.cache', 'wydania_strony.json')
WORD_RE = re.compile(r"[\wąćęłńóśźż][\wąćęłńóśźż'\.\-\$%]*[\wąćęłńóśźż%]|\w", re.IGNORECASE)
STOPWORDS = set('''the a an and or of to in on for with by from at as is are was were be been its it this that
these those your you our we they their his her how why what who when new into about over after than more most
just now will can could not no all has have had via vs one two first says said say also up out ai
i w z na do o po się jak co od dla to nie jest są oraz który która które czy ale już tak jego jej ich'''.split())
PEWNE = 0.40
MOZLIWE = 0.20


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


def fetch_page(url):
    """Oryginalny tytul i opis strony (og:title / og:description)."""
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


def original_pages(links):
    pages = repo.read_json(CACHE, {}) or {}
    missing = [l for l in links if l not in pages]
    if missing:
        with ThreadPoolExecutor(16) as pool:
            pages.update(zip(missing, pool.map(fetch_page, missing)))
        repo.write_json(CACHE, pages)
    return pages


class Wydania:
    """Newsy z `ostatnie` wydan, gotowe do porownan."""

    def __init__(self, ostatnie=2):
        self.news = []
        for folder in repo.issue_dirs()[-ostatnie:]:
            number = int(os.path.basename(folder))
            path = os.path.join(folder, 'dane.csv')
            if os.path.exists(path):
                for row in repo.read_csv(path):
                    self.news.append({'wydanie': number, 'link': row['Link'], 'pl': row['Tytuł'], 'opis': row['Opis']})
        pages = original_pages([n['link'] for n in self.news])
        self.by_link = {dedup_key(n['link']): n for n in self.news}
        for n in self.news:
            page = pages.get(n['link'], {})
            en = page.get('title', '') if len(page.get('title', '')) > 12 else ''
            n['profil'] = collections.Counter(tokens(en) * 2 + tokens(page.get('desc', '')) + tokens(n['pl']) * 2
                                              + entities_pl(n['pl']) * 2 + entities_pl(n['opis'][:400])
                                              + tokens(n['opis'][:400]))
            n['tytulowe'] = set(tokens(en)) | set(tokens(n['pl'])) | set(entities_pl(n['pl']))
        self.df = collections.Counter()
        for n in self.news:
            self.df.update(set(n['profil']))
        self.total = max(1, len(self.news))
        for n in self.news:
            n['vec'], n['norm'] = self._vector(n['profil'])

    def _idf(self, token):
        return math.log((self.total + 1) / (self.df.get(token, 0) + 1)) + 1

    def _vector(self, counts):
        vec = {t: (1 + math.log(f)) * self._idf(t) for t, f in counts.items()}
        return vec, math.sqrt(sum(v * v for v in vec.values())) or 1

    def sprawdz(self, link, text):
        same = self.by_link.get(dedup_key(link)) if link else None
        if same:
            return {'poziom': 'link', 'wydanie': same['wydanie'], 'tytul': same['pl'], 'podobienstwo': 1.0}
        vec, norm = self._vector(collections.Counter(tokens(text)))
        best, best_news, best_shared = 0.0, None, []
        for n in self.news:
            shared = [t for t in vec if t in n['vec']]
            if len(shared) < 2:
                continue
            score = sum(vec[t] * n['vec'][t] for t in shared) / (norm * n['norm'])
            if score > best:
                best, best_news, best_shared = score, n, shared
        if not best_news:
            return None
        from_title = [t for t in best_shared if t in best_news['tytulowe'] and self._idf(t) > 1.5]
        if best >= PEWNE and len(from_title) >= 2:
            level = 'pewne'
        elif best >= MOZLIWE and len(from_title) >= 2:
            level = 'mozliwe'
        else:
            return None
        return {'poziom': level, 'wydanie': best_news['wydanie'], 'tytul': best_news['pl'],
                'podobienstwo': round(best, 2)}
