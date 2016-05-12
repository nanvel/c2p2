import logging
import os
import time

import arrow

from markdown import Markdown
from slugify import slugify

from .settings import settings
from .utils import ExtensionsRegistry


__all__ = ('Label', 'Site')


logger = logging.getLogger(__name__)


SOURCE_SUFFIX = '.md'


class Label(object):

    def __init__(self, title, slug=None):
        self.title = title
        self.slug = slug
        if slug is None:
            self.slug = slugify(title)

    def __hash__(self):
        return hash(self.slug)

    def __eq__(self, other):
        return self.slug == other.slug

    def __repr__(self):
        return 'Label(title={title}, slug={slug})'.format(title=self.title, slug=self.slug)


class PageMeta(object):

    def __init__(self, meta):
        self.meta = meta

    def get_list(self, item):
        return self.meta.get(item, [])

    def get(self, item):
        result = self.meta.get(item)
        if result and len(result):
            return result[0]
        return None

    def __getattr__(self, item):
        return self.get(item=item)


class Page(object):

    def __init__(self, uri, path):
        """
        :param path: relative path to md file.
        """
        self.uri = uri
        self.path = path
        self.html = None
        self.created = None
        self.modified = None
        self.title = None
        self.meta = None
        self.labels = set()
        self.visible = True

        self._md_extensions = [
            'markdown.extensions.toc',
            'markdown.extensions.meta',
            'markdown.extensions.attr_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.admonition',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br',
        ]
        self._md_extensions.extend([
            extension() for extension in ExtensionsRegistry.list()
        ])

        self.update()

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        return self.path == other.path

    def update(self):
        logger.warning('Update {path}.'.format(path=self.path))

        with open(self.path, 'r', encoding='utf-8') as f:
            source_md = f.read()

        md = Markdown(extensions=self._md_extensions)

        self.html = md.convert(source_md)

        self.meta = PageMeta(meta=md.Meta)

        modified = self.meta.modified
        created = self.meta.created

        if created:
            created = arrow.get(created).datetime
        else:
            created = arrow.get(os.path.getctime(self.path)).datetime

        if modified:
            modified = arrow.get(modified).datetime
        else:
            modified = created

        self.created = created
        self.modified = modified

        self.title = self.meta.title or md.title

        self.visible = str(self.meta.visible).lower() != 'false'

        self.labels = set()
        for label in self.meta.get_list('labels'):
            self.labels.add(Label(label))


class Source(object):
    """Looks for updates in source files (.md)."""

    _sources = {}  # path: modification time

    def __init__(self, root):
        self._root = root

    def path_to_uri(self, path):
        uri = path.split(self._root)[-1][:-len(SOURCE_SUFFIX)]
        if uri[0] == '/':
            return uri[1:]
        return uri

    def scan(self, update_cb, delete_cb):

        found = []
        for root, dirs, files in os.walk(self._root):
            for f in files:
                if f.endswith(SOURCE_SUFFIX):
                    path = os.path.join(root, f)
                    found.append(path)
                    modified = time.ctime(os.path.getmtime(path))
                    if path not in self._sources:
                        update_cb(self.path_to_uri(path=path), path)
                        self._sources[path] = modified
                    elif self._sources[path] != modified:
                        update_cb(self.path_to_uri(path=path), path)
                        self._sources[path] = modified

        # look for deleted files
        for path in list(self._sources.keys()):
            if path not in found:
                delete_cb(self.path_to_uri(path=path))
                del self._sources[path]


class Site(object):

    _instance = None
    _source = None
    _pages = {}
    _labels = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Site, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    @classmethod
    def reset(cls):
        cls._source = Source(root=settings.SOURCE_FOLDER)
        cls._pages = {}
        cls._labels = set()

    def _update_page(self, uri, path):
        """Update page content."""
        if uri in self._pages:
            self._pages[uri].update()
        else:
            self._pages[uri] = Page(uri=uri, path=path)

    def _delete_page(self, uri):
        """Delete page from pages dict."""
        if uri in self._pages:
            del self._pages[uri]

    def _update_labels(self):
        """Updates list of available labels."""
        labels = set()
        for page in self.get_pages():
            for label in page.labels:
                labels.add(label)
        to_delete = self._labels - labels
        for label in labels:
            self._labels.add(label)
        for label in to_delete:
            self._labels.discard(label)

    def get_labels(self):
        return sorted(list(self._labels), key=lambda i: i.slug)

    def get_pages(self, label=None):
        """Returns list of pages with specified label."""
        return (
            page for page in sorted(
                self._pages.values(), key=lambda i: i.created, reverse=True
            ) if ((not label or label in page.labels) and page.visible)
        )

    def get_page(self, uri):
        page = self._pages.get(uri)
        if page and page.visible:
            return page
        return None

    def update(self):
        self._source.scan(
            update_cb=self._update_page,
            delete_cb=self._delete_page
        )
        self._update_labels()
