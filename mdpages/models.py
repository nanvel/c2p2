import arrow
import datetime
import logging
import os
import time

from markdown import Markdown
from slugify import slugify
from tornado.ioloop import IOLoop
from tornado.options import options

from .extensions import TitleExtension
from .utils import absolute_path


__all__ = ['SOURCE_FOLDER', 'Watcher', 'pages']


logger = logging.getLogger(__name__)

SOURCE_FOLDER = absolute_path(options.SOURCE_FOLDER)


class Source(object):
    """ Looks for updates in source files (.md).
    """

    _sources = {}  # path: mtime

    def __init__(self, root):
        self._root = root

    def scan(self, callback):
        """ :param callback: calls when source file was updated.
        """
        for root, dirs, files in os.walk(self._root):
            for f in files:
                if f.endswith('.md'):
                    path = os.path.join(root, f)
                    modified = time.ctime(os.path.getmtime(path))
                    if path not in self._sources:
                        callback(path)
                        self._sources[path] = modified
                    elif self._sources[path] != modified:
                        callback(path)
                        self._sources[path] = modified


source = Source(root=SOURCE_FOLDER)


class Pages(object):
    """ Pages content storage.
    """

    _pages = {}
    _labels = {}

    def __init__(self, root):
        self._root = root

    def get(self, path):
        return self._pages[path]

    def list(self):
        pages_list = [v for v in self._pages.values() if not v['hide']]
        pages_list = sorted(pages_list, key=lambda i: i['created'], reverse=True)
        return pages_list

    def labels(self):
        return sorted(self._labels.values(), key=lambda i: len(i['pages']), reverse=True)

    def label(self, slug):
        return self._labels.get(slug, {'pages': [], 'title': 'Not found.', 'slug': slug})

    def update(self, path):
        relative_path = ('/'.join([s for s in path.split(self._root)[-1].split('/') if s])).split('.md')[0]
        logger.warning('Update {path}.'.format(path=relative_path))
        with open(path, 'r') as f:
            source_md = f.read()
        md = Markdown(extensions=[
            'markdown.extensions.toc',
            'markdown.extensions.meta',
            'markdown.extensions.attr_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.admonition',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br',
            TitleExtension(),
        ])
        html = md.convert(source_md)
        created = md.Meta.get('created')
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(path)
        if created:
            created = arrow.get(created[0]).datetime
        else:
            created = arrow.get(ctime).datetime
        page = {
            'path': relative_path,
            'html': html,
            'title': md.Meta['title'][0] if md.Meta.get('title') else md.title,
            'toc': md.toc,
            'meta': md.Meta,
            'created': created,
            'modified': arrow.get(mtime).datetime,
            'hide': (md.Meta['hide'][0]).lower() == 'true' if 'hide' in md.Meta else False
        }
        self._pages[relative_path] = page
        if not page['hide']:
            for label in md.Meta.get('labels', []):
                label_slug = slugify(label)
                if label_slug not in self._labels or self._labels[label_slug]['title'] != label:
                    self._labels[label_slug] = {
                        'slug': label_slug,
                        'title': label,
                        'pages': [],
                    }
                self._labels[label_slug]['pages'].append(page)


pages = Pages(root=SOURCE_FOLDER)


class Watcher(object):

    def __init__(self):
        self.ioloop = IOLoop.instance()
        self.watch()

    def watch(self):
        source.scan(callback=pages.update)
        self.ioloop.add_timeout(
            deadline=datetime.timedelta(seconds=2),
            callback=self.watch)
