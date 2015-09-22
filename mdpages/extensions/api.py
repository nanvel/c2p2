"""
API extension for Python-Markdown
========================================

Usage:

```
!API! POST:/auth/login
    "username", "str", "required", "4 chars minimal length"
    "password", "str", "required", ""
```

Author: Oleksandr Polieno (polienoom@gmail.com)
License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""

import re

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


__all__ = ['APIExtension']


class APIProcessor(BlockProcessor):

    CLASSNAME = 'api'
    RE_ENDPOINT = re.compile(r'^!API!\ (GET|POST|PUT|DELETE):([\w/{}-]+)(?:\ \[(.*?)\])(?:\ "(.*?)")?')
    RE_ATTRIBUTES = re.compile(r'"([\w_-]+)", ?"([\w_-]+)", ?"([?:\ \w_\'-]+)", ?"(|.+)"')

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        return self.RE_ENDPOINT.search(block) or \
            (block.startswith(' ' * self.tab_length) and sibling is not None and
             sibling.get('class', '').find(self.CLASSNAME) != -1)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE_ENDPOINT.search(block)

        if m:
            block = block[m.end() + 1:]  # removes the first line

        block, rest = self.detab(block)

        if m:
            table = etree.SubElement(parent, 'table')
            tr = etree.SubElement(table, 'tr')
            td = etree.SubElement(tr, 'td', attrib={'colspan': '4'})
            method_span = etree.SubElement(td, 'span')
            method = m.group(1)
            method_span.text = method
            method_span.set('class', 'method')
            endpoint_span = etree.SubElement(td, 'span')
            endpoint_span.text = m.group(2)
            tr.set('class', 'method-{method}'.format(method=method.lower()))
            table.set('class', self.CLASSNAME)
            if block:
                tr = etree.SubElement(table, 'tr')
                for col in ['Name', 'Type', 'Required', 'Notes']:
                    td = etree.SubElement(tr, 'td')
                    td.text = col
            for l in block.split('\n'):
                found = self.RE_ATTRIBUTES.search(l)
                if found:
                    tr = etree.SubElement(table, 'tr')
                    for i in range(1, 5):
                        td = etree.SubElement(tr, 'td')
                        td.text = found.group(i)
            permissions = m.group(3).split(',')
            if permissions:
                tr = etree.SubElement(table, 'tr')
                td = etree.SubElement(tr, 'td', attrib={'colspan': '4'})
                td.set('class', 'permissions')
                td.text = "Permissions required:"
                for permission in permissions:
                    endpoint_span = etree.SubElement(td, 'span')
                    endpoint_span.text = permission.strip()
        if rest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, rest)


class APIExtension(Extension):
    """ API extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add API to Markdown instance. """
        md.registerExtension(self)
        md.parser.blockprocessors.add('api', APIProcessor(md.parser), '_begin')
