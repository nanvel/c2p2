from unittest import TestCase

from ..models import Site
from ..settings import settings
from ..utils import rel


__all__ = ('ModelsTestCase',)


class ModelsTestCase(TestCase):

    def setUp(self):
        settings.SOURCE_FOLDER = rel('c2p2/tests/md')
        super(ModelsTestCase, self).setUp()

    def test_site(self):
        site = Site()
        site.update()
        pages = list(site.get_pages())
        self.assertEqual(len(pages), 1)
        self.assertEqual(len(pages[0].labels), 1)
        self.assertEqual(pages[0].title, 'Header 1')
