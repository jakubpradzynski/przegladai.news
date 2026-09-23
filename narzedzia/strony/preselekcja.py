#!/usr/bin/env python3
"""Preselekcja wpisow ze stron: reguly automatyczne + paczki dla subagentow + scalenie wyniku.

    przygotuj  .cache/strony/wynik.json (+ przegladarka.json)
               1. reguly automatyczne: wpisy, ktore byly w 2 ostatnich wydaniach (ten sam link albo
                  ten sam temat - lib/tematy.py), oraz z redakcja/preselekcja.md (sekcja "Reguly
                  automatyczne"): wpisy bez zwiazku z AI na stronach ogolnych i tytuly pasujace do wzorcow -> "nie"
                  (bez AI, natychmiast) -> .cache/strony/oceny/auto.json
               2. reszta w paczkach po --paczka wpisow -> .cache/strony/do_oceny/paczka_NN.json,
                  kazda z kontekstem tylko swoich stron (skutecznosc + ostatnie decyzje Kuby)
    sprawdz    scala .cache/strony/oceny/*.json -> .cache/strony/preselekcja.json;
               kod wyjscia 1, gdy ktorys wpis nie ma oceny tak/moze/nie z powodem

Uzycie:
    python3 narzedzia/strony/preselekcja.py przygotuj [--paczka 25]
    python3 narzedzia/strony/preselekcja.py sprawdz
"""
import argparse
import collections
import glob
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, 'przeglad'))

from lib import repo, tematy  # noqa: E402

CACHE = os.path.join(repo.ROOT, '.cache', 'strony')
DO_OCENY = os.path.join(CACHE, 'do_oceny')
OCENY = os.path.join(CACHE, 'oceny')
PRESELEKCJA = os.path.join(CACHE, 'preselekcja.json')
PODOBNE = os.path.join(CACHE, 'podobne.json')
SESJA = os.path.join(CACHE, 'sesja.json')
WYBORY = os.path.join(repo.REDAKCJA, 'dziennik', 'strony_wybory.jsonl')
REGULY = os.path.join(repo.REDAKCJA, 'preselekcja.md')
PRZYKLADY_NA_STRONE = 10

AI_RE = re.compile(
    r'\b(ai|a\.i\.|artificial intelligence|sztuczn\w* inteligencj\w*|llms?|gpt[\w.-]*|chatgpt|claude|gemini|'
    r'openai|anthropic|copilot|agent\w*|agentow\w*|language models?|model\w* językow\w*|machine learning|'
    r'uczeni\w* maszynow\w*|neural|genai|generative|generatywn\w*|deepmind|nvidia|robot\w*|humanoid\w*|'
    r'chatbot\w*|czatbot\w*|mistral|llama|deepseek|perplexity|cursor|codex|diffusion|inference|inferencj\w*|'
    r'rag|mcp|prompt\w*|automatyzacj\w*|automation|elevenlabs|hugging ?face|midjourney|runway|xai|grok|'
    r'waymo|autonomous|autonomiczn\w*|deepfake\w*|deep fake|scamwatch|siri|alexa|meta ai|muse|synthesia|'
    r'scale ai|databricks|snowflake cortex|nvidia)\b', re.IGNORECASE)


def auto_rules():
    with open(REGULY, encoding='utf-8') as f:
        text = f.read()
    match = re.search(r'## Reguły automatyczne.*?```json\n(.*?)\n```', text, re.DOTALL)
    if not match:
        return set(), []
    rules = json.loads(match.group(1))
    patterns = [(re.compile(r['wzorzec'], re.IGNORECASE), r['powod']) for r in rules.get('wzorce_nie', [])]
    return set(rules.get('strony_ogolne', [])), patterns


def history():
    stats = collections.defaultdict(lambda: {'wziete': 0, 'wszystkie': 0})
    examples = collections.defaultdict(list)
    if os.path.exists(WYBORY):
        with open(WYBORY, encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                if entry['kuba'] == 'niewidziany':
                    continue
                stats[entry['strona']]['wszystkie'] += 1
                stats[entry['strona']]['wziete'] += entry['kuba'] == 'wziety'
                examples[entry['strona']].append(entry)
    return stats, examples


def site_context(name, stats, examples):
    past = examples.get(name, [])
    return {'historia': stats.get(name, {'wziete': 0, 'wszystkie': 0}),
            'ostatnio_wziete': [e['tytul'] for e in past if e['kuba'] == 'wziety'][-PRZYKLADY_NA_STRONE:],
            'ostatnio_pominiete': [e['tytul'] for e in past if e['kuba'] == 'pominiety'][-PRZYKLADY_NA_STRONE:]}


def cmd_przygotuj(args):
    import server  # wczytanie wyniku razem z wpisami z przegladarki
    result = server.load(with_preselection=False)
    general_sites, patterns = auto_rules()
    stats, examples = history()

    for folder in (DO_OCENY, OCENY):
        shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder)
    for path in (PRESELEKCJA, SESJA):   # nowy przeglad: stare oceny i zaznaczenia nie obowiazuja
        if os.path.exists(path):
            os.remove(path)

    issues = tematy.Wydania(ostatnie=2)
    auto, todo, similar = [], [], {}
    for site in result['strony']:
        for item in site['nowe']:
            if item.get('w_data_csv'):
                continue
            text = '%s %s' % (item['tytul'], item.get('opis', ''))
            seen = issues.sprawdz(item['link'], text)
            rule = next((reason for pattern, reason in patterns if pattern.search(item['tytul'])), None)
            if seen and seen['poziom'] in ('link', 'pewne'):
                auto.append({'id': item['link'], 'ocena': 'nie',
                             'powod': 'reguła: było w #%d — %s' % (seen['wydanie'], seen['tytul'][:70])})
            elif rule:
                auto.append({'id': item['link'], 'ocena': 'nie', 'powod': 'reguła: ' + rule})
            elif site['nazwa'] in general_sites and not AI_RE.search(text):
                auto.append({'id': item['link'], 'ocena': 'nie', 'powod': 'reguła: brak związku z AI w tytule i opisie'})
            else:
                entry = {'id': item['link'], 'strona': site['nazwa'], 'data': item['data'],
                         'tytul': item['tytul'], 'opis': item.get('opis', '')[:250]}
                if seen:   # 'mozliwe' - tylko podpowiedz dla AI i dla Kuby
                    entry['podobne_do_wydania'] = '#%d: %s' % (seen['wydanie'], seen['tytul'])
                    similar[item['link']] = entry['podobne_do_wydania']
                todo.append(entry)
    repo.write_json(os.path.join(OCENY, 'auto.json'), auto)
    repo.write_json(PODOBNE, similar)

    # paczki: wpisy jednej strony trzymamy razem (duplikaty tematow najczesciej sa w obrebie agregatora)
    todo.sort(key=lambda i: i['strona'])
    batches = [todo[i:i + args.paczka] for i in range(0, len(todo), args.paczka)]
    for n, batch in enumerate(batches, 1):
        sites = sorted({i['strona'] for i in batch})
        repo.write_json(os.path.join(DO_OCENY, 'paczka_%02d.json' % n), {
            'od': result['od'],
            'strony': {s: site_context(s, stats, examples) for s in sites},
            'wszystkie_tytuly_w_przegladzie': [i['tytul'] for i in todo],   # do wykrywania duplikatow miedzy paczkami
            'wpisy': batch,
        })
    print('Reguły automatyczne: %d wpisów -> "nie" (bez AI), w tym było w ostatnich wydaniach: %d'
          % (len(auto), sum('było w #' in a['powod'] for a in auto)))
    print('Podobne do newsów z ostatnich wydań (podpowiedź dla AI): %d' % len(similar))
    print('Do oceny AI: %d wpisów w %d paczkach -> .cache/strony/do_oceny/paczka_NN.json' % (len(todo), len(batches)))
    for n, batch in enumerate(batches, 1):
        print('  paczka_%02d: %d wpisów (%s)' % (n, len(batch), ', '.join(sorted({i['strona'] for i in batch}))))


def cmd_sprawdz(_args):
    expected = set()
    for path in glob.glob(os.path.join(DO_OCENY, 'paczka_*.json')):
        expected |= {i['id'] for i in repo.read_json(path)['wpisy']}
    ratings, missing_batches = {}, []
    for path in sorted(glob.glob(os.path.join(DO_OCENY, 'paczka_*.json'))):
        out = os.path.join(OCENY, os.path.basename(path))
        if not os.path.exists(out):
            missing_batches.append(os.path.basename(path))
    for path in glob.glob(os.path.join(OCENY, '*.json')):
        for r in repo.read_json(path) or []:
            ratings[r['id']] = r
    missing = [i for i in expected if i not in ratings]
    bad = [r['id'] for r in ratings.values() if r.get('ocena') not in ('tak', 'moze', 'nie') or not r.get('powod')]
    repo.write_json(PRESELEKCJA, list(ratings.values()))
    counts = collections.Counter(r.get('ocena') for r in ratings.values())
    print('Ocenione: %d (tak %d, może %d, nie %d) -> .cache/strony/preselekcja.json'
          % (len(ratings), counts['tak'], counts['moze'], counts['nie']))
    for name in missing_batches:
        print('  brak wyniku paczki: %s' % name)
    for ident in missing:
        print('  brak oceny: %s' % ident)
    for ident in bad:
        print('  zła ocena albo brak powodu: %s' % ident)
    if missing_batches or missing or bad:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='polecenie', required=True)
    p = sub.add_parser('przygotuj')
    p.add_argument('--paczka', type=int, default=25)
    p.set_defaults(func=cmd_przygotuj)
    sub.add_parser('sprawdz').set_defaults(func=cmd_sprawdz)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
