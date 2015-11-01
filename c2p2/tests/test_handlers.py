from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncHTTPTestCase

from app import application

from ..models import pages
from ..utils import rel


class HandlersTestCase(AsyncHTTPTestCase):

    def get_app(self):
        return application

    def setUp(self):
        super(HandlersTestCase, self).setUp()
        self.page_path = rel('mdpages/tests/md/test.md')
        pages._root = 'mdpages/tests/md'
        pages.update(path=self.page_path)

    def test_page(self):
        client = AsyncHTTPClient(self.io_loop)
        client.fetch(self.get_url(application.reverse_url('page', 'test')), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertNotEqual(str(response.body).find('Text 1'), -1)

    def tearDown(self):
        pages.update(path=self.page_path, delete=True)
        super(HandlersTestCase, self).tearDown()
