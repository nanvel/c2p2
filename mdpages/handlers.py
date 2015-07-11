from tornado.options import options
from tornado.web import RequestHandler

from .models import pages


__all__ = ['PageHandler', 'IndexHandler', 'SitemapHandler']


class PageHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, path):
        page = pages.get(path=path)
        self.render(
            '{theme}/page.html'.format(theme=options.THEME),
            title=page['title'], page=page)


class IndexHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        pages_list = pages.list()
        self.render(
            '{theme}/index.html'.format(theme=options.THEME),
            pages=pages_list, title='Index')


class SitemapHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        pages_list = pages.list()
        self.render(
            '{theme}/sitemap.xml'.format(theme=options.THEME),
            pages=pages_list, base_url=options.BASE_URL)
