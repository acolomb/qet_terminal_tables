#!/usr/bin/env python3
"""Extract terminal block connections from QElectroTech SQLite database."""

import sqlite3

from .html_table import TableGeneratorHTML


def query_blocks():
    """Generate SQL query string for block summary."""
    return '''
SELECT
    substr("label", 0, instr("label", ':')) AS "tblock",
    MAX(substr("label", instr("label", ':')+1)+0) AS "maxtnum",
    COUNT(*) AS "mentions",
    group_concat("folio" || '-' || "position", ', ') as "fpositions"
FROM "element_nomenclature_view" AS "t"
WHERE "element_type" = 'terminal' AND "label" LIKE '%:%'
GROUP BY "tblock"
ORDER BY "tblock" ASC
'''


def query_terminals(add_where=''):
    """Generate SQL query string for terminal mentions."""
    return f'''
SELECT
    substr("label", 0, instr("label", ':')) AS "tblock",
    substr("label", instr("label", ':')+1)+0 AS "tnum",
    ( SELECT COUNT(*) FROM "element_nomenclature_view" AS "ct"
      WHERE "ct"."label" = "t"."label" ) AS "mentions",
    group_concat("folio" || '-' || "position", ', ') as "fpositions"
FROM "element_nomenclature_view" AS "t"
WHERE "element_type" = 'terminal' AND "label" LIKE '%:%' {add_where}
GROUP BY "label"
ORDER BY "tblock" ASC, "tnum" ASC
'''


def process_db(dbfile, header=None, footer=None, indent=0):
    """Generate HTML files from the given SQLite database."""
    con = sqlite3.connect(dbfile)

    blocks = con.cursor()
    blocks.execute(query_blocks())

    table_attr = 'border="0" cellspacing="0" cellpadding="0"'

    for tblock, maxtnum, mentions, fpositions in blocks:
        with open(f'terminals_{tblock}.html', 'wt') as outfile:
            if header:
                outfile.write(header)

            with TableGeneratorHTML(outfile, table_attr, indent) as table:
                table.writeheader((f'Block {tblock}',),
                                  cell_attr='colspan="3"')
                terminals = con.cursor()
                terminals.execute(query_terminals(f"AND tblock='{tblock}'"))

                rows = 0
                for term_block, tnum, term_mentions, fpositions in terminals:
                    rows += 1
                    while rows < tnum:
                        # Insert blank rows for never mentioned terminals
                        table.writerow((rows, '(0)', ' '),
                                       classes=('tnum', 'mentions', 'positions'))
                        rows += 1
                    table.writerow((tnum, f'({term_mentions})', fpositions),
                                   classes=('tnum', 'mentions', 'positions'))
            print(f'{outfile.name}: {mentions=} {maxtnum=} {rows=}')

            if footer:
                outfile.write(footer)

    con.close()


def main(dbfile, wrap=False, css_add=''):
    """Run HTML generator with default output adjustments."""
    footer = ''
    indent = 0
    # Mandatory style settings for grid alignment
    css = '''\
td { line-height: 20px; }
th { line-height: 12px; }
'''
    css += css_add
    if not wrap:
        header = f'''\
<style type="text/css">
{css}</style>
'''
    else:
        header = '''\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
  <head>
'''
        if css:
            header += f'''\
    <style type="text/css">
{css}
    </style>
'''
        header += '''\
  </head>
  <body>
'''
        indent = 4
        footer = '''\
  </body>
</html>
'''

    return process_db(dbfile, header, footer, indent)
