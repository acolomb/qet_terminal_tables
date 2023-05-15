#!/usr/bin/env python3
"""Convenience functions for writing HTML tables."""


class TableGeneratorHTML:
    """HTML code generator for tables."""

    def __init__(self, htmlfile, table_attr='', indent=0):
        self.htmlfile = htmlfile
        self.indent = ' ' * indent
        self.table_attr = table_attr

    def __enter__(self):
        self.htmlfile.write(self.table(self.table_attr))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.htmlfile.write(self.table_end())

    def table(self, attributes=''):
        """Return indented opening table tag."""
        if attributes:
            attributes = ' ' + attributes
        return f'''{self.indent}\
<table{attributes}>
'''

    def tr(self, content, attributes=''):
        """Return indented opening table row tag."""
        if attributes:
            attributes = ' ' + attributes
        return f'''{self.indent}\
  <tr{attributes}>
{content}
'''

    def td(self, content, attributes='', tag='td'):
        """Return indented table cell tags with content."""
        if attributes:
            attributes = ' ' + attributes
        return f'''{self.indent}\
    <{tag}{attributes}>{content}</{tag}>\
'''

    def th(self, *args, **kwargs):
        """Return indented table header cell tags with content."""
        return self.td(*args, tag='th', **kwargs)

    def tr_end(self):
        """Return indented closing table row tag."""
        return f'''{self.indent}\
  </tr>
'''

    def table_end(self):
        """Return indented closing table tag."""
        return f'''{self.indent}\
</table>
'''

    def writerow(self, row, row_attr='', cell_attr='', classes=[], tagfunc=None):
        """Write the given data row to the output file object."""
        if tagfunc is None:
            tagfunc = self.td
        if len(classes):
            classes = list(classes) + [None] * (len(row) - len(classes))
            cells = [tagfunc(content, ' '.join((f'class="{cls}"', cell_attr)).strip())
                     for content, cls in zip(row, classes)]
        else:
            cells = [tagfunc(content, cell_attr) for content in row]
        row = self.tr('\n'.join(cells), row_attr) + self.tr_end()
        return self.htmlfile.write(row)

    def writeheader(self, *args, **kwargs):
        """Write the given data row as headers to the output file object."""
        return self.writerow(*args, tagfunc=self.th, **kwargs)
