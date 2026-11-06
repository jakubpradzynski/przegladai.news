#!/usr/bin/env python3
"""Infografiki do postow social: proste karty 1080x1350 (4:5).

Zasada: ma wygladac jak slajd zrobiony przez czlowieka, nie jak szablon z generatora.
Bez ozdobnikow (kropki, paski, zaokraglone pigulki, gradienty), jeden kolor akcentu, duzo powietrza,
tekst wyrownany do lewej. Dwa style (pole "styl"):
    notatka   cieple tlo jak papier, szeryfowy Charter, kluczowa liczba podkreslona "markerem" (domyslny)
    minimal   biale tlo, Avenir Next, czern + jeden akcent w kolorze marki, cienkie linie
Fonty systemowe macOS; gdy ich brak - Oswald z narzedzia/okladka (inny wyglad, ale dziala).

Specyfikacja (JSON, pole "infografika" w poscie):
    {"rodzaj": "liczba", "liczba": "16,3 mld $", "podpis": "przychodu Anthropic w I połowie 2026",
     "zrodlo": "prospekt IPO Anthropic"}
    {"rodzaj": "porownanie", "tytul": "Terminal-Bench 4.0", "jednostka": "%",
     "elementy": [{"etykieta": "GPT-5.6 Terra", "wartosc": 21.5}, {"etykieta": "GPT-6.1 Terra", "wartosc": 50.3}]}
    {"rodzaj": "lista", "tytul": "Co zmienia Terra", "punkty": ["…", "…", "…"]}      (2-4 punkty)
    {"rodzaj": "cytat", "cytat": "…", "autor": "Jensen Huang, CEO Nvidia"}
Wspolne pola opcjonalne: "styl", "numer" (wydanie, w stopce), "naglowek" (maly napis nad trescia),
"zrodlo", w porownaniu "tekst" i "wyroznij" przy elemencie.

Uzycie:
    python3 narzedzia/social/grafika.py spec.json wyjscie.png
    python3 narzedzia/social/grafika.py '{"rodzaj": "liczba", ...}' wyjscie.png
"""
import argparse
import json
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OSWALD = os.path.join(os.path.dirname(HERE), 'okladka', 'Oswald-Variable.ttf')
CHARTER = '/System/Library/Fonts/Supplemental/Charter.ttc'
AVENIR = '/System/Library/Fonts/Avenir Next.ttc'

W, H = 1080, 1350
MARGIN = 100

THEMES = {
    'notatka': {
        'bg': '#FAF7F0', 'ink': '#221E26', 'muted': '#8C8590', 'accent': '#5B2A86', 'marker': '#E4D6F0',
        'bar': '#221E26', 'bar_soft': '#D9D3CC', 'rule': '#DCD5CB',
        'fonts': {'num': (CHARTER, 3), 'title': (CHARTER, 3), 'text': (CHARTER, 0), 'italic': (CHARTER, 1),
                  'meta': (AVENIR, 5), 'meta_bold': (AVENIR, 2)},
    },
    'minimal': {
        'bg': '#FFFFFF', 'ink': '#111111', 'muted': '#8A8A8A', 'accent': '#2A053C', 'marker': None,
        'bar': '#2A053C', 'bar_soft': '#E2E2E2', 'rule': '#E6E6E6',
        'fonts': {'num': (AVENIR, 8), 'title': (AVENIR, 0), 'text': (AVENIR, 7), 'italic': (AVENIR, 4),
                  'meta': (AVENIR, 5), 'meta_bold': (AVENIR, 2)},
    },
}
STYLES = list(THEMES)
DEFAULT_STYLE = 'notatka'
OSWALD_FALLBACK = {'num': 'Bold', 'title': 'SemiBold', 'text': 'Regular', 'italic': 'Light',
                   'meta': 'Regular', 'meta_bold': 'Medium'}

T = THEMES[DEFAULT_STYLE]


def font(size, role='text'):
    path, index = T['fonts'][role]
    if os.path.exists(path):
        return ImageFont.truetype(path, size, index=index)
    f = ImageFont.truetype(OSWALD, size)
    f.set_variation_by_name(OSWALD_FALLBACK[role])
    return f


def wrap(text, f, max_width):
    lines, current = [], ''
    for word in text.split():
        candidate = (current + ' ' + word).strip()
        if f.getlength(candidate) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    # nie zostawiaj jednoliterowego slowa na koncu linii (polska typografia: "z", "w", "i")
    for i in range(len(lines) - 1):
        words = lines[i].split()
        if len(words) > 1 and len(words[-1]) == 1 and f.getlength(words[-1] + ' ' + lines[i + 1]) <= max_width:
            lines[i] = ' '.join(words[:-1])
            lines[i + 1] = words[-1] + ' ' + lines[i + 1]
    return lines


def fit(text, max_width, max_lines, sizes, role):
    """Najwiekszy font, przy ktorym tekst miesci sie w max_lines liniach."""
    for size in sizes:
        f = font(size, role)
        lines = wrap(text, f, max_width)
        if len(lines) <= max_lines and all(f.getlength(l) <= max_width for l in lines):
            return f, lines, size
    raise SystemExit('Tekst "%s" się nie mieści - skróć go.' % text[:60])


def line_height(f, spacing):
    ascent, descent = f.getmetrics()
    return (ascent + descent) * spacing


def draw_lines(draw, lines, f, top, fill, spacing=1.1, x=MARGIN):
    """Rysuje linie od gory; zwraca y pod ostatnia linia."""
    step = line_height(f, spacing)
    for i, line in enumerate(lines):
        draw.text((x, top + i * step), line, font=f, fill=fill, anchor='la')
    return top + len(lines) * step


def missing_glyphs(text):
    """Znaki, ktorych font nie ma (rysowalby je jako puste prostokaty)."""
    missing = set()
    for role in ('num', 'title', 'text', 'italic'):
        f = font(40, role)
        notdef = bytes(f.getmask('￿'))
        missing |= {ch for ch in text if not ch.isspace() and bytes(f.getmask(ch)) == notdef}
    return sorted(missing)


def marker(draw, box, seed):
    """Podkreslenie jak flamastrem: lekko nierowny pas za dolna czescia tekstu (tylko styl notatka)."""
    if not T['marker']:
        return
    x0, y0, x1, y1 = box
    rnd = random.Random(seed)
    j = lambda: rnd.uniform(-5, 5)  # noqa: E731
    draw.polygon([(x0 - 12 + j(), y0 + j()), (x1 + 14 + j(), y0 + 6 + j()),
                  (x1 + 8 + j(), y1 + j()), (x0 - 6 + j(), y1 + 4 + j())], fill=T['marker'])


def frame(spec):
    image = Image.new('RGB', (W, H), T['bg'])
    draw = ImageDraw.Draw(image)
    if spec.get('naglowek'):
        draw.text((MARGIN, 96), spec['naglowek'], font=font(30, 'meta_bold'), fill=T['muted'])
    draw.line((MARGIN, H - 120, W - MARGIN, H - 120), fill=T['rule'], width=2)
    meta = font(26, 'meta')
    left = 'przegladai.news' + (' · #%s' % spec['numer'] if spec.get('numer') else '')
    draw.text((MARGIN, H - 72), left, font=meta, fill=T['muted'], anchor='ls')
    if spec.get('zrodlo'):
        text = 'Źródło: ' + spec['zrodlo']
        room = W - 2 * MARGIN - meta.getlength(left) - 40
        while meta.getlength(text) > room and len(text) > 12:
            text = text[:-2].rstrip(' ,.…') + '…'
        draw.text((W - MARGIN, H - 72), text, font=meta, fill=T['muted'], anchor='rs')
    return image, draw


def render_liczba(spec, draw):
    width = W - 2 * MARGIN
    try:   # jedna linia, jesli sie da - liczba czyta sie wtedy najlepiej
        f, lines, _ = fit(spec['liczba'], width - 30, 1, range(220, 129, -6), 'num')
    except SystemExit:
        f, lines, _ = fit(spec['liczba'], width - 30, 2, range(180, 89, -6), 'num')
    sub_f, sub_lines, _ = fit(spec.get('podpis', ''), width, 5, range(54, 33, -2), 'text')
    cap = f.getbbox('0H')[3] - f.getbbox('0H')[1]
    step = cap * 1.4
    block = cap + (len(lines) - 1) * step + 90 + len(sub_lines) * line_height(sub_f, 1.1)
    top = 170 + (H - 320 - block) / 2
    for i, line in enumerate(lines):
        base = top + cap + i * step
        marker(draw, (MARGIN, base - cap * 0.42, MARGIN + f.getlength(line), base + cap * 0.1), line)
        draw.text((MARGIN, base), line, font=f, fill=T['ink'] if T['marker'] else T['accent'], anchor='ls')
    y = top + cap + (len(lines) - 1) * step
    draw_lines(draw, sub_lines, sub_f, y + 70, T['ink'])


def fmt(value, unit):
    text = ('%g' % value).replace('.', ',')
    return text + (unit or '')


def render_porownanie(spec, draw):
    width = W - 2 * MARGIN
    items = spec['elementy'][:5]
    unit = spec.get('jednostka', '')
    title_f, title_lines, _ = fit(spec.get('tytul', ''), width, 3, range(64, 39, -2), 'title')
    y = draw_lines(draw, title_lines, title_f, 170, T['ink'], 1.05) + 50
    max_value = max(i['wartosc'] for i in items) or 1
    label_f, value_f = font(34, 'meta'), font(64, 'num')
    labels = [item.get('tekst') or fmt(item['wartosc'], unit) for item in items]
    row = min(220, (H - 200 - y) / len(items))
    y += ((H - 200 - y) - row * len(items)) / 2
    top_item = max(items, key=lambda i: i['wartosc'])
    for item, label in zip(items, labels):
        highlight = item.get('wyroznij', item is top_item)
        draw.text((MARGIN, y), item['etykieta'], font=label_f, fill=T['muted'])
        draw.text((MARGIN, y + 46), label, font=value_f, fill=T['ink'] if highlight else T['muted'])
        bar_top = y + 46 + 100
        bar_w = max(6, width * item['wartosc'] / max_value)
        draw.rectangle((MARGIN, bar_top, MARGIN + bar_w, bar_top + 12), fill=T['bar'] if highlight else T['bar_soft'])
        y += row


def render_lista(spec, draw):
    width = W - 2 * MARGIN
    title_f, title_lines, _ = fit(spec.get('tytul', ''), width, 3, range(68, 41, -2), 'title')
    y = draw_lines(draw, title_lines, title_f, 170, T['ink'], 1.05) + 70
    points = spec['punkty'][:4]
    space = (H - 200 - y) / len(points)
    num_f = font(48, 'italic')
    for n, point in enumerate(points, 1):
        f, lines, _ = fit(point, width - 80, 3, range(48, 31, -2), 'text')
        draw.text((MARGIN, y), '%d.' % n, font=num_f, fill=T['accent'])
        draw_lines(draw, lines, f, y + 2, T['ink'], 1.12, x=MARGIN + 80)
        y += space


def render_cytat(spec, draw):
    width = W - 2 * MARGIN
    f, lines, _ = fit('„%s”' % spec['cytat'].strip('„”"'), width, 8, range(72, 37, -2), 'italic')
    a_f, a_lines, _ = fit(spec.get('autor', ''), width, 2, range(32, 23, -2), 'meta')
    block = len(lines) * line_height(f, 1.12) + 60 + len(a_lines) * line_height(a_f, 1.2)
    top = 170 + (H - 320 - block) / 2
    y = draw_lines(draw, lines, f, top, T['ink'], 1.12)
    if spec.get('autor'):
        draw.line((MARGIN, y + 34, MARGIN + 60, y + 34), fill=T['accent'], width=3)
        draw_lines(draw, a_lines, a_f, y + 60, T['muted'], 1.2)


RENDERERS = {'liczba': render_liczba, 'porownanie': render_porownanie,
             'lista': render_lista, 'cytat': render_cytat}


def render(spec, out_path):
    global T
    if spec.get('rodzaj') not in RENDERERS:
        raise SystemExit('Nieznany rodzaj infografiki: %s (dostępne: %s)'
                         % (spec.get('rodzaj'), ', '.join(RENDERERS)))
    style = spec.get('styl', DEFAULT_STYLE)
    if style not in THEMES:
        raise SystemExit('Nieznany styl: %s (dostępne: %s)' % (style, ', '.join(THEMES)))
    T = THEMES[style]
    texts = [v for k, v in spec.items() if isinstance(v, str) and k not in ('rodzaj', 'styl')]
    texts += spec.get('punkty', []) + [e.get('etykieta', '') for e in spec.get('elementy', [])]
    missing = missing_glyphs(' '.join(texts))
    if missing:
        raise SystemExit('Font nie ma znaków: %s - zamień je na słowa albo zwykłe znaki.' % ' '.join(missing))
    image, draw = frame(spec)
    RENDERERS[spec['rodzaj']](spec, draw)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    image.save(out_path, 'PNG', optimize=True)
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('spec', help='plik JSON albo JSON wprost')
    parser.add_argument('wyjscie')
    args = parser.parse_args()
    if os.path.exists(args.spec):
        with open(args.spec, encoding='utf-8') as f:
            spec = json.load(f)
    else:
        spec = json.loads(args.spec)
    print('Zapisano', render(spec, args.wyjscie))


if __name__ == '__main__':
    sys.exit(main())
