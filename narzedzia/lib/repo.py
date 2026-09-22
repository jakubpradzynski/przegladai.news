"""Wspolne sciezki repozytorium i pomocnicze funkcje wydan."""
import csv
import glob
import json
import os
import re
import unicodedata
from datetime import date, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PRACA = os.path.join(ROOT, 'praca')
WYDANIA = os.path.join(ROOT, 'wydania')
REDAKCJA = os.path.join(ROOT, 'redakcja')
DZIENNIK = os.path.join(REDAKCJA, 'dziennik', 'poprawki.jsonl')

# Pliki robocze biezacego wydania (katalog praca/ jest w .gitignore)
DATA_CSV = os.path.join(ROOT, 'data.csv')
DATA_WEJSCIE = os.path.join(PRACA, 'data_wejscie.csv')
LINKI = os.path.join(PRACA, 'linki.json')
OPISY_DIR = os.path.join(PRACA, 'opisy')
WERSJA_AI = os.path.join(PRACA, 'wersja_ai.csv')
PREPARED = os.path.join(PRACA, 'prepared_data.csv')
ROBOCZY = os.path.join(PRACA, 'roboczy.csv')
FINAL = os.path.join(PRACA, 'final_prepared_data.csv')
WYDANIE_AI = os.path.join(PRACA, 'wydanie_ai.json')
WYDANIE = os.path.join(PRACA, 'wydanie.json')

BASE_FIELDS = ['Link', 'Tytuł', 'Opis', 'Tagi', 'Czas']
AI_FIELDS = BASE_FIELDS + ['Sekcja', 'Ocena', 'Uzasadnienie', 'Rekomendacja']

TAGS = ['Bliżej technologii', 'Nowości i ogłoszenia', 'Polska', 'Za paywallem']
SECTIONS = ['Nowości', 'Technologia', 'Pozostałe']


def section_for(tags):
    tags = tags or ''
    if 'Nowości i ogłoszenia' in tags:
        return 'Nowości'
    if 'Bliżej technologii' in tags:
        return 'Technologia'
    return 'Pozostałe'


def read_csv(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, '') for k in fields})


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def issue_dirs():
    return sorted(glob.glob(os.path.join(WYDANIA, '[0-9][0-9][0-9]')))


def issue_dir(number):
    return os.path.join(WYDANIA, '%03d' % int(number))


def last_issue():
    """Metadane ostatniego zapisanego wydania."""
    dirs = issue_dirs()
    return read_json(os.path.join(dirs[-1], 'meta.json')) if dirs else None


def published_links():
    """Wszystkie linki opublikowane w dotychczasowych wydaniach."""
    links = []
    for d in issue_dirs():
        path = os.path.join(d, 'dane.csv')
        if os.path.exists(path):
            links.extend(r['Link'] for r in read_csv(path))
    return links


def next_friday(today=None):
    """Najblizszy piatek po dzisiejszym dniu (w piatek - za tydzien)."""
    today = today or date.today()
    days = 4 - today.weekday()
    if days <= 0:
        days += 7
    return today + timedelta(days=days)


def slugify(text):
    text = text.replace('ł', 'l').replace('Ł', 'L')
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def issue_slug(number, title):
    headline = title.split(':', 1)[1] if ':' in title else title
    return 'wydanie-%s-%s' % (number, slugify(headline))
