from ..context import Context
from .base import C2P2Handler


__all__ = ('PageHandler', 'SitemapHandler', 'LabelHandler', 'IndexHandler')


class PageHandler(C2P2Handler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, uri):
        self.render('page.html', c=Context(uri=uri))


class IndexHandler(C2P2Handler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render('index.html', c=Context())


class LabelHandler(C2P2Handler):

    SUPPORTED_METHODS = ('GET',)

    def get(self, slug):
        self.render('label.html', c=Context(label=slug))


class SitemapHandler(C2P2Handler):

    SUPPORTED_METHODS = ('GET',)

    def get(self):
        self.render('sitemap.xml', c=Context())
