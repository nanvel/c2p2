from markdown import Markdown
from unittest import TestCase

from ..extensions import TitleExtension


__all__ = ['ExtensionsTestCase']


class ExtensionsTestCase(TestCase):

    def test_title(self):
        md = Markdown(extensions=[TitleExtension()])
        title = "Title 1"
        html = md.convert("# {title}".format(title=title))
        self.assertEqual(md.title, title)
