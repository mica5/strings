#!/usr/bin/env python
"""Convert csv or xlsx to mediawiki format

Generate a table as described by https://www.mediawiki.org/wiki/Help:Tables

It's heavy because it uses pandas, but that also simplifies the complexity of this code.

Version 0.1
2018-10-09
"""
import argparse

import pandas as pd

def run_main():
    args = parse_cl_args()

    if args.file.lower().endswith('csv'):
        df = pd.read_excel(args.file)
    else:
        df = pd.read_excel(args.file)

    print('{| class="wikitable sortable"')

    for c in df.columns:
        print('!', c)

    for index, row in df.iterrows():
        print('|-')
        for val in row:
            print('|', val, sep='')

    print("|}")

    success = True
    return success

def parse_cl_args():


    argParser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argParser.add_argument('file')

    args = argParser.parse_args()
    return args


if __name__ == '__main__':
    success = run_main()
    exit_code = 0 if success else 1
    exit(exit_code)
