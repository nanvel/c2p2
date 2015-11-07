"""
Title Extension for Python-Markdown
===================================
"""
import re

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import string_type


__all__ = ('ExtensionsRegistry',)


class ExtensionsRegistry(object):

    _extensions = set()

    @classmethod
    def register(cls, extension):
        cls._extensions.add(extension)

    @classmethod
    def list(cls):
        return list(cls._extensions)


class TitleTreeprocessor(Treeprocessor):

    def __init__(self, md):
        super(TitleTreeprocessor, self).__init__(md)
        self.header_rgx = re.compile('[Hh][123456]')

    def run(self, doc):
        title = None
        for el in doc.iter():
            if isinstance(el.tag, string_type) and self.header_rgx.match(el.tag):
                title = ''.join(el.itertext()).strip()
                break
        self.markdown.title = title


class TitleExtension(Extension):

    TreeProcessorClass = TitleTreeprocessor

    def __init__(self, *args, **kwargs):
        super(TitleExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        self.md = md
        self.reset()
        titleext = self.TreeProcessorClass(md)
        md.treeprocessors.add('title', titleext, '_end')

    def reset(self):
        self.md.title = ''


ExtensionsRegistry.register(extension=TitleExtension)
