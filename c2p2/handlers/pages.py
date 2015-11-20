from tornado.httpclient import HTTPError

from ..models import Label, Site
from ..settings import settings
from .base import C2P2Handler


__all__ = ('PageHandler', 'SitemapHandler', 'LabelHandler', 'RobotsHandler')


class PageHandler(C2P2Handler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, uri):
        page = Site().get_page(uri)
        if not page:
            raise HTTPError(code=404)
        self.render('page.html', page=page)


class LabelHandler(C2P2Handler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, slug=settings.DEFAULT_LABEL):
        label = Label(slug, slug=slug)
        site = Site()
        self.render('label.html', pages=site.get_pages(label=label), labels=site.get_labels(), current=label)


class SitemapHandler(C2P2Handler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render('sitemap.xml', pages=Site().get_pages())


class RobotsHandler(C2P2Handler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render('robots.txt')
