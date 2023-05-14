#!/usr/bin/env python3
"""Script module to run HTML generator with command-line options."""

import argparse

from . import extract_tables


parser = argparse.ArgumentParser()
parser.add_argument('dbfile',
                    nargs='?', default='qet.sqlite',
                    help='read database from the given FILE')
parser.add_argument('-s', '--styles', metavar='FILE',
                    nargs='?', const='styles.css',
                    help='include CSS stylesheet (default "styles.css")')
parser.add_argument('-w', '--wrap', action='store_true',
                    help='output a complete HTML document with framing')
args = parser.parse_args()

if args.styles:
    with open(args.styles, 'r') as f:
        css = ''.join(f.readlines())
else:
    css = ''

extract_tables.main(args.dbfile, args.wrap, css)
