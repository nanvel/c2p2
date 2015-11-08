import datetime
import logging
import os
import time

import arrow

from markdown import Markdown
from slugify import slugify
from tornado.ioloop import IOLoop
from tornado.options import options

from .utils import ExtensionsRegistry


__all__ = ('Watcher', 'pages', 'label_pages', 'labels', 'Label')


logger = logging.getLogger(__name__)


SOURCE_SUFFIX = '.md'


def get_md_extensions():
    extensions = [
        'markdown.extensions.toc',
        'markdown.extensions.meta',
        'markdown.extensions.attr_list',
        'markdown.extensions.fenced_code',
        'markdown.extensions.admonition',
        'markdown.extensions.codehilite',
        'markdown.extensions.nl2br',
    ]
    extensions.extend([
        extension() for extension in ExtensionsRegistry.list()
    ])
    return extensions


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

        self.update()

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        return self.path == other.path

    def update(self):
        logger.warning('Update {path}.'.format(path=self.path))

        with open(self.path, 'r') as f:
            source_md = f.read()

        md = Markdown(extensions=get_md_extensions())

        self.html = md.convert(source_md)

        created = md.Meta.get('created')
        modified = md.Meta.get('modified')
        if created:
            created = arrow.get(created[0]).datetime
        else:
            created = arrow.get(os.path.getctime(self.path)).datetime

        if modified:
            modified = arrow.get(modified[0]).datetime
        else:
            modified = created
        self.created = created
        self.modified = modified

        self.title = md.Meta['title'][0] if md.Meta.get('title') else md.title

        self.meta = md.Meta

        self.visible = 'hide' not in md.Meta or md.Meta['hide'][0].lower() != 'true'

        self.labels = set()
        for label in md.Meta.get('labels', []):
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


pages = {}
labels = set()


def _update_page(uri, path):
    """Update page content."""
    if uri in pages:
        pages[uri].update()
    else:
        pages[uri] = Page(uri=uri, path=path)


def _delete_page(uri):
    """Delete page from pages dict."""
    if uri in pages:
        del pages[uri]


def _update_labels():
    """Updates list of available labels."""
    global labels
    _labels = set()
    for page in pages.values():
        for label in page.labels:
            _labels.add(label)
    to_delete = labels - _labels
    for label in _labels:
        labels.add(label)
    for label in to_delete:
        labels.discard(label)


def label_pages(label):
    """Returns list of pages with specified label."""
    return (
        page for page in sorted(
            pages.values(), key=lambda i: i.created, reverse=True
        ) if (label in page.labels and page.visible)
    )


class Watcher(object):

    def __init__(self):
        self.ioloop = IOLoop.instance()
        self.source = Source(root=options.SOURCE_FOLDER)

    def watch(self, repeat=True):
        self.source.scan(
            update_cb=_update_page,
            delete_cb=_delete_page
        )
        _update_labels()
        if repeat:
            self.ioloop.add_timeout(deadline=datetime.timedelta(seconds=2), callback=self.watch)
