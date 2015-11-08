from tornado.httpclient import HTTPError
from tornado.options import options
from tornado.web import RequestHandler

from ..models import pages, labels, label_pages, Label


__all__ = ('PageHandler', 'SitemapHandler', 'LabelHandler', 'RobotsHandler')


class PageHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, uri):
        page = pages.get(uri)
        if not page:
            raise HTTPError(code=404)
        self.render('page.html', page=page)


class LabelHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, slug=options.DEFAULT_LABEL):
        label = Label(slug, slug=slug)
        if label not in labels:
            raise HTTPError(code=404)
        self.render('label.html', pages=label_pages(label), labels=labels, current=label)


class SitemapHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        pages_list = (page for page in pages.values() if page.visible)
        self.render('sitemap.xml', pages=pages_list)


class RobotsHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render('robots.txt')
