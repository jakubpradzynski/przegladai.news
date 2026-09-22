#!/usr/bin/env python3
"""Sklada wydanie: praca/final_prepared_data.csv + praca/wydanie.json -> wydania/NNN/

Tworzy:
    wydania/NNN/substack.html  - tresc do skopiowania do edytora Substacka + blok metadanych
    wydania/NNN/dane.csv       - finalna selekcja (Link, Tytul, Opis, Tagi, Czas)
    wydania/NNN/meta.json      - numer, tytul, slug, data, wstep, opis SEO, napis na okladce
    wydania/NNN/okladka.jpeg   - okladka z szablonu

praca/wydanie.json (zapisuje adminka, zakladka "Wydanie"):
    {"numer": 39, "tytul": "Wydanie #39: ...", "wstep": "...", "opis_seo": "...",
     "slug": "wydanie-39-...", "data": "2026-09-25", "okladka": "#39: ..."}

Uzycie:
    python3 narzedzia/generuj_wydanie.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import repo, walidacja  # noqa: E402
import okladka  # noqa: E402

# Kolory tagow dokladnie takie, jakie sa na Substacku (data-color z opublikowanych wydan),
# zeby po wklejeniu nie trzeba bylo ich poprawiac recznie.
TAG_COLORS = {
    'Nowości i ogłoszenia': '#1555e2',
    'Bliżej technologii': '#bf9000',
    'Polska': '#ff0000',
}


def hex_to_rgb(color):
    color = color.lstrip('#')
    return 'rgb(%d, %d, %d)' % tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def label(text, color=None):
    if color:
        span = '<span data-color="%s" style="color: %s;">[%s]</span>' % (color, hex_to_rgb(color), html.escape(text))
    else:
        span = '<span>[%s]</span>' % html.escape(text)
    return '<strong>%s</strong>' % span


def sort_key(row):
    """Kolejnosc z redakcja/priorytety.md: Nowosci, Blizej technologii, Polska, reszta."""
    tags = row['Tagi']
    if 'Nowości i ogłoszenia' in tags:
        group = 0
    elif 'Bliżej technologii' in tags:
        group = 1
    elif 'Polska' in tags:
        group = 2
    else:
        group = 3
    return (group, 'Polska' not in tags, row['Tytuł'].lower())


def build_html(meta, rows):
    esc = html.escape
    parts = ['<h1>%s</h1>' % esc(meta['tytul']), '<p>Cześć!</p>']
    for paragraph in meta['wstep'].split('\n\n'):
        if paragraph.strip():
            parts.append('<p>%s</p>' % esc(paragraph.strip()))
    parts += ['<p>Zapraszam do lektury!</p>', '<hr>']

    for row in rows:
        parts.append('<h3><a href="%s">%s</a></h3>' % (esc(row['Link'], quote=True), esc(row['Tytuł'])))
        parts.append('<p>%s</p>' % esc(row['Opis']))
        labels = [label(t, TAG_COLORS.get(t)) for t in row['Tagi'].split(', ') if t]
        if row['Czas']:
            labels.append(label(row['Czas']))
        if labels:
            parts.append('<p>%s</p>' % ' '.join(labels))
        parts.append('<hr>')

    parts.append('<p>To tyle na dzisiaj.<br><strong>Dzięki, że jesteś ze mną!</strong></p>')
    parts.append('<p>Udanego tygodnia,<br><em>Kuba</em></p>')

    day = meta['data'].split('-')
    parts.append(
        '<div style="margin-top: 48px; padding: 20px 24px; background-color: #f5f5f5;'
        ' border: 1px solid #ddd; border-radius: 6px; font-size: 13px; line-height: 1.7;">'
        '<p style="margin: 0 0 12px 0; font-size: 15px; font-weight: bold;">📋 Metadane Substack (nie kopiować do posta)</p>'
        '<p><strong>Tytuł:</strong> %s</p>'
        '<p><strong>Opis SEO</strong> (%d znaków)<strong>:</strong> %s</p>'
        '<p><strong>URL posta:</strong> %s</p>'
        '<p><strong>Data publikacji:</strong> %s.%s.%s (piątek)</p>'
        '<p><strong>Okładka:</strong> wydania/%03d/okladka.jpeg</p>'
        '<p><strong>Na końcu posta:</strong> dodaj przycisk „Udostępnij” z podpisem „Jeżeli newsletter Ci się podoba, będę wdzięczny za jego udostępnienie.”</p>'
        '<p><strong>Tekst do social mediów:</strong> %s</p>'
        '</div>' % (esc(meta['tytul']), len(meta['opis_seo']), esc(meta['opis_seo']), esc(meta['slug']),
                    day[2], day[1], day[0], meta['numer'], esc(meta['wstep']))
    )
    return '\n'.join(parts) + '\n'


def main():
    meta = repo.read_json(repo.WYDANIE)
    if not meta:
        raise SystemExit('Brak praca/wydanie.json - zapisz zakladke "Wydanie" w admince.')
    missing = [k for k in ('numer', 'tytul', 'wstep', 'opis_seo', 'slug', 'data', 'okladka') if not meta.get(k)]
    if missing:
        raise SystemExit('W praca/wydanie.json brakuje: %s' % ', '.join(missing))
    if not os.path.exists(repo.FINAL):
        raise SystemExit('Brak praca/final_prepared_data.csv - zapisz selekcje w admince.')

    rows = [{k: r.get(k, '') for k in repo.BASE_FIELDS} for r in repo.read_csv(repo.FINAL)]
    problems = []
    for row in rows:
        row['Tagi'] = walidacja.normalize_tags(row['Tagi'])
        row['Czas'] = walidacja.normalize_time(row['Czas'])
        bad = [t for t in row['Tagi'].split(', ') if t and t not in repo.TAGS]
        if bad:
            problems.append('%s: nieznany tag %s' % (row['Tytuł'], bad))
    if problems:
        raise SystemExit('\n'.join(problems))
    rows.sort(key=sort_key)

    folder = repo.issue_dir(meta['numer'])
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, 'substack.html'), 'w', encoding='utf-8') as f:
        f.write(build_html(meta, rows))
    repo.write_csv(os.path.join(folder, 'dane.csv'), rows, repo.BASE_FIELDS)
    repo.write_json(os.path.join(folder, 'meta.json'),
                    {k: meta[k] for k in ('numer', 'slug', 'tytul', 'data', 'wstep', 'opis_seo', 'okladka')})
    lines, size = okladka.render(meta['okladka'], os.path.join(folder, 'okladka.jpeg'))

    rel = os.path.relpath(folder, repo.ROOT)
    print('Wydanie #%s gotowe w %s/ (%d newsow, okladka: %d linie, %dpx)'
          % (meta['numer'], rel, len(rows), len(lines), size))
    print('  %s/substack.html  - otworz w przegladarce i skopiuj do Substacka' % rel)
    print('  %s/okladka.jpeg' % rel)


if __name__ == '__main__':
    main()
