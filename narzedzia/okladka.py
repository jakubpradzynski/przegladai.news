#!/usr/bin/env python3
"""Okladka wydania: napis "#<nr>: <tytul>" na stalym szablonie, bez AI.

Uzycie:
    python3 narzedzia/okladka.py "#39: Nowa Siri, debata o AI i Waymo" wydania/039/okladka.jpeg
    python3 narzedzia/okladka.py "#39: ..." --podglad      # -> praca/okladka_podglad.jpeg

Parametry (font, ramka, kolor) sa w narzedzia/okladka/ustawienia.json.
Gdy napis sie nie miesci, skrypt konczy sie bledem - skroc napis (redakcja/seo.md),
zamiast zmniejszac font ponizej font_min.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import repo  # noqa: E402

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'okladka')


def load_config():
    with open(os.path.join(ASSETS, 'ustawienia.json'), encoding='utf-8') as f:
        return json.load(f)


def load_font(cfg, size):
    font = ImageFont.truetype(os.path.join(ASSETS, cfg['font']), size)
    font.set_variation_by_name(cfg['wariant_fontu'])
    return font


def wrap(text, font, max_width):
    lines, current = [], ''
    for word in text.split():
        candidate = (current + ' ' + word).strip()
        if font.getlength(candidate) <= max_width:
            current = candidate
        elif not current:
            return None
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit(text, cfg):
    box = cfg['ramka']
    for size in range(cfg['font_max'], cfg['font_min'] - 1, -2):
        font = load_font(cfg, size)
        lines = wrap(text, font, box['w'])
        if lines and len(lines) <= cfg['max_linii'] and len(lines) * size * cfg['odstep_linii'] <= box['h']:
            return font, lines, size
    raise SystemExit('Napis "%s" nie miesci sie w %d liniach nawet przy %dpx. Skroc go.'
                     % (text, cfg['max_linii'], cfg['font_min']))


def render(text, out_path):
    cfg = load_config()
    image = Image.open(os.path.join(ASSETS, cfg['szablon'])).convert('RGB')
    draw = ImageDraw.Draw(image)
    font, lines, size = fit(' '.join(text.split()), cfg)

    box = cfg['ramka']
    line_height = size * cfg['odstep_linii']
    top = box['y'] + (box['h'] - len(lines) * line_height) / 2
    center_x = box['x'] + box['w'] / 2
    for index, line in enumerate(lines):
        draw.text((center_x, top + (index + 0.5) * line_height), line, font=font,
                  fill=cfg['kolor'], anchor='mm')

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    image.save(out_path, 'JPEG', quality=cfg['jakosc_jpeg'], subsampling=0)
    return lines, size


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('napis')
    parser.add_argument('wyjscie', nargs='?')
    parser.add_argument('--podglad', action='store_true')
    args = parser.parse_args()

    out = os.path.join(repo.PRACA, 'okladka_podglad.jpeg') if args.podglad or not args.wyjscie else args.wyjscie
    lines, size = render(args.napis, out)
    print('Zapisano %s (%d linie, font %dpx)' % (os.path.relpath(out, repo.ROOT), len(lines), size))


if __name__ == '__main__':
    main()
