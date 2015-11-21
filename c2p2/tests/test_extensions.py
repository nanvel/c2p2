from collections import namedtuple
from unittest import TestCase

from markdown import Markdown

from ..utils.md import TitleExtension, ExtensionsRegistry


__all__ = ('ExtensionsTestCase',)


class ExtensionsTestCase(TestCase):

    def test_title(self):
        md = Markdown(extensions=[TitleExtension()])
        title = "Title 1"
        md.convert("# {title}".format(title=title))
        self.assertEqual(md.title, title)

    def test_extensions_registry(self):
        save_extensions = ExtensionsRegistry._extensions
        NewExtension = namedtuple('NewExtension', ['name'])
        ExtensionsRegistry.register(NewExtension)
        self.assertIn(NewExtension, ExtensionsRegistry.list())
        ExtensionsRegistry._extensions = save_extensions
