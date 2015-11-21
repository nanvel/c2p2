from tornado.httpclient import HTTPError

from .models import Site, Label


__all__ = ('Context',)


class PagesContext(object):

    def __init__(self, site, label):
        self.site = site
        self.label = label

    def __iter__(self):
        return self.site.get_pages(label=self.label).__iter__()

    def __getitem__(self, item):
        return self.site.get_page(uri=item)


class Context(object):

    def __init__(self, uri=None, label=None):
        self.uri = uri
        if label and isinstance(label, str):
            self.label = Label(title=label, slug=label)
        else:
            self.label = label
        self.site = Site()

    @property
    def page(self):
        if not self.uri:
            raise HTTPError(code=500, message="page attribute doesn't available.")
        p = self.site.get_page(uri=self.uri)
        if not p:
            raise HTTPError(code=404, message="Page was not found.")
        return p

    @property
    def pages(self):
        return PagesContext(site=self.site, label=self.label)

    @property
    def labels(self):
        return self.site.get_labels()
