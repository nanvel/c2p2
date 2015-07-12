from tornado.options import options
from tornado.web import RequestHandler

from .models import pages


__all__ = ['PageHandler', 'IndexHandler', 'SitemapHandler', 'LabelHandler', 'RobotsHandler']


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
        self.render(
            '{theme}/list.html'.format(theme=options.THEME),
            pages=pages.list(), title='Index', labels=pages.labels())


class LabelHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, slug):
        label = pages.label(slug=slug)
        self.render(
            '{theme}/list.html'.format(theme=options.THEME),
            pages=label['pages'], title=label['title'], labels=pages.labels())


class SitemapHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        pages_list = pages.list()
        self.render(
            '{theme}/sitemap.xml'.format(theme=options.THEME),
            pages=pages_list, base_url=options.BASE_URL)


class RobotsHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render(
            '{theme}/robots.txt'.format(theme=options.THEME),
            domain=options.BASE_URL.split('//')[-1])
