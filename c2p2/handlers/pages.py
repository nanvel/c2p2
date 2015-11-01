from tornado.httpclient import HTTPError
from tornado.options import options
from tornado.web import RequestHandler

from ..models import pages


__all__ = ('PageHandler', 'SitemapHandler', 'LabelHandler', 'RobotsHandler')


class PageHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, path):
        page = pages.get(path=path)
        if not page:
            raise HTTPError(code=404)
        self.render(
            'page.html',
            title=page['title'], page=page)


class LabelHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, slug=options.DEFAULT_LABEL):
        label = pages.label(slug=slug)
        self.render(
            'label.html',
            pages=label['pages'], title=label['title'],
            labels=pages.labels(),
            current=slug)


class SitemapHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        pages_list = pages.list()
        self.render('sitemap.xml', pages=pages_list)


class RobotsHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render('robots.txt')
