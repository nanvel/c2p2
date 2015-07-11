import arrow
import datetime
import logging
import os
import six
import time

from markdown import Markdown
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
                    path = os.path.join(self._root, f)
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

    _pages = {}  # path: {html, meta}

    def __init__(self, root):
        self._root = root

    def get(self, path):
        return self._pages[path]

    def list(self):
        pages_list = [v for p, v in six.iteritems(self._pages)]
        pages_list = sorted(pages_list, key=lambda i: i['created'], reverse=True)
        return pages_list

    def update(self, path):
        relative_path = (''.join(path.split(self._root)[-1].split('/'))).split('.md')[0]
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
        self._pages[relative_path] = {
            'path': relative_path,
            'html': html,
            'title': md.Meta['title'][0] if md.Meta.get('title') else md.title,
            'toc': md.toc,
            'meta': md.Meta,
            'created': created,
            'modified': arrow.get(mtime).datetime,
        }


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
