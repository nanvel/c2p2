import json

from unittest import mock

from tornado.httpclient import AsyncHTTPClient, HTTPError, HTTPRequest
from tornado.testing import AsyncHTTPTestCase

from ..app import create_application
from ..context import Context
from ..settings import settings


__all__ = ('PagesHandlersTestCase', 'ErrorPagesHandlersTestCase', 'GitHubHandlersTestCase')


class PagesHandlersTestCase(AsyncHTTPTestCase):

    def setUp(self):
        self.application = create_application()
        super(PagesHandlersTestCase, self).setUp()

    def get_app(self):
        return self.application

    @mock.patch('c2p2.handlers.base.C2P2Handler.render')
    def test_page(self, render_mock):
        client = AsyncHTTPClient(self.io_loop)
        client.fetch(self.get_url(self.application.reverse_url('page', 'test')), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(render_mock.call_count, 1)
        self.assertEqual(render_mock.call_args[0][0], 'page.html')
        self.assertTrue(isinstance(render_mock.call_args[1]['c'], Context))

    @mock.patch('c2p2.handlers.base.C2P2Handler.render')
    def test_index(self, render_mock):
        client = AsyncHTTPClient(self.io_loop)
        client.fetch(self.get_url(self.application.reverse_url('index')), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(render_mock.call_count, 1)
        self.assertEqual(render_mock.call_args[0][0], 'index.html')
        self.assertTrue(isinstance(render_mock.call_args[1]['c'], Context))

    @mock.patch('c2p2.handlers.base.C2P2Handler.render')
    def test_label(self, render_mock):
        client = AsyncHTTPClient(self.io_loop)
        client.fetch(self.get_url(self.application.reverse_url('label', 'test')), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(render_mock.call_count, 1)
        self.assertEqual(render_mock.call_args[0][0], 'label.html')
        self.assertTrue(isinstance(render_mock.call_args[1]['c'], Context))

    @mock.patch('c2p2.handlers.base.C2P2Handler.render')
    def test_sitemap(self, render_mock):
        client = AsyncHTTPClient(self.io_loop)
        client.fetch(self.get_url(self.application.reverse_url('sitemap').replace('\.', '.')), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(render_mock.call_count, 1)
        self.assertEqual(render_mock.call_args[0][0], 'sitemap.xml')
        self.assertTrue(isinstance(render_mock.call_args[1]['c'], Context))


class ErrorPagesHandlersTestCase(AsyncHTTPTestCase):

    def setUp(self):
        self.save_settings_debug = settings.DEBUG
        settings.DEBUG = False
        self.application = create_application()
        super(ErrorPagesHandlersTestCase, self).setUp()

    def get_app(self):
        return self.application

    @mock.patch('c2p2.handlers.base.C2P2Handler.prepare')
    @mock.patch('c2p2.handlers.base.C2P2Handler.render')
    def test_404(self, render_mock, prepare_mock):
        prepare_mock.side_effect = HTTPError(code=404)
        client = AsyncHTTPClient(self.io_loop)
        client.fetch(self.get_url(self.application.reverse_url('index')), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)
        self.assertEqual(render_mock.call_count, 1)
        self.assertEqual(render_mock.call_args[0][0], '404.html')

    @mock.patch('c2p2.handlers.base.C2P2Handler.prepare')
    @mock.patch('c2p2.handlers.base.C2P2Handler.render')
    def test_500(self, render_mock, prepare_mock):
        prepare_mock.side_effect = ValueError
        client = AsyncHTTPClient(self.io_loop)
        client.fetch(self.get_url(self.application.reverse_url('index')), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 500)
        self.assertEqual(render_mock.call_count, 1)
        self.assertEqual(render_mock.call_args[0][0], '500.html')

    def tearDown(self):
        settings.DEBUG = self.save_settings_debug
        super(ErrorPagesHandlersTestCase, self).tearDown()


class GitHubHandlersTestCase(AsyncHTTPTestCase):

    def setUp(self):
        self.save_settings_debug = settings.DEBUG
        settings.DEBUG = False
        self.application = create_application()
        super(GitHubHandlersTestCase, self).setUp()

    def get_app(self):
        return self.application

    def test_pull(self):
        settings.GITHUB_VALIDATE_IP = False
        settings.GITHUB_SECRET = ''
        settings.GITHUB_BRANCH = 'master'

        client = AsyncHTTPClient(self.io_loop)

        # test ping
        request = HTTPRequest(
            self.get_url(self.application.reverse_url('git-pull')),
            headers={
                'X-GitHub-Event': 'ping'
            },
            method='POST',
            body='{}'
        )
        client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body.decode()), {'msg': 'pong'})
