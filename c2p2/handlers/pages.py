from tornado.httpclient import HTTPError
from tornado.web import RequestHandler

from ..models import Label, Site
from ..settings import settings


__all__ = ('PageHandler', 'SitemapHandler', 'LabelHandler', 'RobotsHandler')


class PageHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, uri):
        page = Site().get_page(uri)
        if not page:
            raise HTTPError(code=404)
        self.render('page.html', page=page)


class LabelHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, slug=settings.DEFAULT_LABEL):
        label = Label(slug, slug=slug)
        site = Site()
        self.render('label.html', pages=site.get_pages(label=label), labels=site.get_labels(), current=label)


class SitemapHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render('sitemap.xml', pages=Site().get_pages())


class RobotsHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render('robots.txt')
