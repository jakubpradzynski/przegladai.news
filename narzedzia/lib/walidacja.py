"""Walidacja newsow wedlug regul z redakcja/*.md.

Zakazane frazy czytamy wprost z redakcja/opisy.md (sekcja "Zakazane i nadużywane",
akapit "Nie używać"), wiec gdy ucz-sie dopisze tam fraze, walidator od razu ja lapie.
"""
import os
import re
from urllib.parse import urlparse

from . import repo

TIME_RE = re.compile(r'^(\d+h( \d+ min)?|\d+ min)$')
MEDIA_HOSTS = ('youtube.com', 'youtu.be', 'vimeo.com', 'open.spotify.com', 'podcasts.apple.com')
TAG_FIXES = {'za paywałem': 'Za paywallem', 'za paywalem': 'Za paywallem'}


def banned_phrases():
    path = os.path.join(repo.REDAKCJA, 'opisy.md')
    with open(path, encoding='utf-8') as f:
        text = f.read()
    match = re.search(r'Nie używać.*?\n(.*?)\n\s*\n', text, re.DOTALL)
    if not match:
        return []
    return [p.strip(' ,.…') for p in re.findall(r'„([^”]+)”', match.group(1)) if len(p.strip()) > 3]


def normalize_tags(raw):
    tags = []
    for tag in (raw or '').split(','):
        tag = tag.strip()
        if not tag:
            continue
        tag = TAG_FIXES.get(tag.lower(), tag)
        if tag not in tags:
            tags.append(tag)
    return ', '.join(sorted(tags))


def normalize_time(raw):
    raw = (raw or '').strip()
    raw = re.sub(r'(\d)min', r'\1 min', raw)
    raw = re.sub(r'\s+', ' ', raw)
    return raw


def check(row, phrases=None):
    """Zwraca liste problemow (pusta = OK). Normalizuje tagi i czas w miejscu."""
    problems = []
    phrases = banned_phrases() if phrases is None else phrases

    row['Tagi'] = normalize_tags(row.get('Tagi'))
    row['Czas'] = normalize_time(row.get('Czas'))
    tags = [t for t in row['Tagi'].split(', ') if t]

    for tag in tags:
        if tag not in repo.TAGS:
            problems.append('niedozwolony tag: %s' % tag)
    if 'Nowości i ogłoszenia' in tags and 'Bliżej technologii' in tags:
        problems.append('Nowości i ogłoszenia + Bliżej technologii razem')

    host = urlparse(row.get('Link', '')).netloc.lower()
    is_media = any(h in host for h in MEDIA_HOSTS)
    if row['Czas'] and not TIME_RE.match(row['Czas']):
        problems.append('zly format czasu: %s' % row['Czas'])
    if row['Czas'] and not is_media:
        problems.append('czas przy materiale, ktory nie jest wideo/audio')
    if is_media and 'youtube' in host and not row['Czas']:
        problems.append('brak czasu dla wideo')

    title = (row.get('Tytuł') or '').strip()
    if not title:
        problems.append('brak tytulu')
    elif len(title) > 110:
        problems.append('tytul za dlugi (%d znakow)' % len(title))
    elif title.endswith('.'):
        problems.append('kropka na koncu tytulu')

    desc = (row.get('Opis') or '').strip()
    if len(desc) < 350:
        problems.append('opis za krotki (%d znakow)' % len(desc))
    elif len(desc) > 1200:
        problems.append('opis za dlugi (%d znakow)' % len(desc))
    low = desc.lower()
    for phrase in phrases:
        if phrase.lower() in low:
            problems.append('zakazana fraza: "%s"' % phrase)

    try:
        score = int(row.get('Ocena') or 0)
        if not 1 <= score <= 10:
            raise ValueError
    except ValueError:
        problems.append('ocena spoza 1-10: %s' % row.get('Ocena'))
    return problems
