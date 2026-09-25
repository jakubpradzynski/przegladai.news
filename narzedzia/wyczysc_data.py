#!/usr/bin/env python3
"""Usuwa z data.csv linie przetworzone w tym wydaniu (kopia w praca/data_wejscie.csv).

Linie dopisane do data.csv juz po /zbierz-dane zostaja - trafia do kolejnego wydania.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import repo  # noqa: E402


def main():
    if not os.path.exists(repo.DATA_WEJSCIE):
        raise SystemExit('Brak praca/data_wejscie.csv - nie wiem, ktore linie byly przetworzone. data.csv bez zmian.')
    with open(repo.DATA_WEJSCIE, encoding='utf-8') as f:
        processed = {line.strip() for line in f if line.strip()}
    with open(repo.DATA_CSV, encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]
    keep = [line for line in lines if line.strip() not in processed]
    with open(repo.DATA_CSV, 'w', encoding='utf-8') as f:
        f.writelines(keep)
    print('data.csv: usunieto %d przetworzonych linii, zostalo %d nowych' % (len(lines) - len(keep), len(keep)))


if __name__ == '__main__':
    main()
