
HTML Table Generator From QElectroTech Terminal Elements
========================================================

A command line tool to extract terminal element references from a
QElectroTech project and generate pretty HTML tables for labelling
terminal strips diagrams.  It's written for Python version 3 and works
from the exported SQLite database.

Author: André Colomb <src@andre.colomb.de>


License
-------

Copyright (C) 2023  André Colomb

`qet_terminal_tables` is free software: you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

`qet_terminal_tables` is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this program.  If not, see
<http://www.gnu.org/licenses/>.


Motivation
----------

*QElectroTech* (as of version 0.9) does not yet integrate a good way
to build cross-referenced terminal block lists that summarize where to
find the placed terminal elements.  It does however provide access to
its internal SQLite database (by exporting it) where most of the
relevant information can be found.  This program generates pretty HTML
tables from that, which fit nicely next to a schematic drawing of the
terminal block.  The output can be placed next to that in a simple
HTML-formatted text field.

The sources of information are the user-defined labels assigned to
elements of type *terminal*, other element types are ignored.  The
label must have two pieces of information: the **terminal block
name**, delimited by a colon (`:`) from the **terminal number**.
Example:

    -X10:8  <<<< terminal number
    ^^^^
    block name

The same terminal label can appear several times in the project,
e.g. for terminal strips with two or more connection points.  There is
no requirement that they have the same potential or a wire connecting
them.  The list is solely assembled with cross-references to the folio
positions where the terminal elements with identical labels appear.
The *terminal number* part should be strictly numeric, without
additional characters.

Note that terminals within a block are always assumed to have
consecutive numbers starting from one.  For the example above, the
table for block `-X10` will have entries numbered `1` through `8` at
least.


### Features ###
+ Extract element data from the exported SQLite database.
+ Group by terminal block / group.
+ Fill in missing rows for terminal numbers never used, to avoid gaps
  in the counting.
+ Output one HTML file per block, summarizing the associated
  terminals.
+ Align to the standard 20 pixel grid for putting next to a graphical
  element representation.
+ Reference a CSS style sheet file to adjust the appearance.
+ HTML code is ready for copy & paste into QElectroTech text field.
+ Optionally wrap the generated table and styling code in a complete
  HTML page structure (otherwise only `<style>` and `<table>` tags).
+ Easy to read / extend Python code.
+ No external dependencies, only Python standard library.


### Limitations ###

- No instant integration: needs a DB export, generate step, pasting
  code back into project.  If the project changes, this needs to be
  re-done every time.
- The "function" field of the associated wire connection is not
  available from the database, thus no semantic info what the
  connection is used for can be displayed.
- No actual cross-reference links, the folio positions are not
  "clickable" for jumping to the referenced place.
- Limited HTML styling [as supported by the QT engine][qt-html].
- QElectroTech overrides some table layout settings, so some standard
  HTML / CSS techniques have no effect.
- Pasted code is mangled heavily in QElectroTech, cannot be easily
  adjusted later on.  Better just replace it completely with a freshly
  generated version.

[qt-html]: https://doc.qt.io/qt-5/richtext-html-subset.html "Supported HTML Subset"


Installation
------------

This tool needs a working *Python (version 3)* runtime environment.
Head to [its homepage][python] to get started.

Simply clone the [repository on GitHub][github] or download a release
archive and unpack it somewhere on your computer.  No further setup
procedure required.

It is advisable to keep the code next to the project files (`.qet` and
`.sqlite` files), as the `.html` files are written to the current
working directory, and invoking the package is easiest from the parent
directory.

[python]: https://www.python.org "Official home of the Python Programming Language"
[github]: https://github.com/acolomb/qet_terminal_tables "Project repository on GitHub"


Usage
-----

`qet_terminal_tables` is a runnable Python package, invoked from the
command line like this:

    python3 -m qet_terminal_tables PATH-TO-DATABASE.sqlite

The output of `python3 -m qet_terminal_tables --help` shows a summary
of all available options.


### Input Database ###

If no database file name is given, the tool looks for a file named
`qet.sqlite` in the current working directory.  The database file must
already exist, exported from QElectroTech using the **Project** >
**Export the internal project database** menu item.

**Note: The internal database is only updated when needed, such as
during project loading or when an index table is reloaded.  If you
have no index tables in your project, the exported database may be
outdated until the project is closed and re-opened!**


### Style Sheet ###

A CSS file can be specified using the `--styles` (or shorter `-s`)
option.  Without a further argument, it looks for a file named
`styles.css` in the current working directory.  The included
`samples/style-template.css` can be used as a basis to see what
styling is possible.


### Output to HTML Files ###

The resulting tables are written to individual HTML files, named after
the terminal block labels (part before the colon).  They end up in the
current working directory, where `qet_terminal_tables` was called
from.  The content of each file can be pasted directly into a
QElectroTech text field:

1. Create an empty text field on the target folio.
2. Select *Edit the text field* from the context menu (right click) or
   open the *Advanced Editor* from the *Selection properties* panel.
3. Switch to the *Source* tab on the bottom.
4. Mark all text there and delete it.
5. Copy & paste the contents of the desired HTML file instead.
6. Click *OK* and enjoy your pretty table.

Note that when you look at the *Source* tab again later, the code will
be transformed into the rich text engine's internal representation.
Some manual modifications may not be applied at all or rewritten.

When invoked with the `--wrap` (or shorter `-w`) option, the generated
code will resemble a complete HTML document, ready to look at with a
web browser.  Note however that QElectroTech / QT renders the HTML
differently, as it supports only a [subset of the HTML
specification][qt-html].  Especially geometry settings (width, height)
and borders will not work like in a browser.

For each generated HTML file, `qet_terminal_tables` prints the file
name, followed by some statistics, such as number of used terminals in
the block, number of overall mentions and the number of HTML rows
generated.
