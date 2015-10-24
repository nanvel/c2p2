import arrow
import datetime
import logging
import os
import time

from markdown import Markdown
from slugify import slugify
from tornado.ioloop import IOLoop
from tornado.options import options

from .extensions import TitleExtension, APIExtension
from .utils import absolute_path


__all__ = ('SOURCE_FOLDER', 'Watcher', 'pages')


logger = logging.getLogger(__name__)

SOURCE_FOLDER = absolute_path(options.SOURCE_FOLDER)


class Source(object):
    """Looks for updates in source files (.md)."""

    _sources = {}  # path: mtime

    def __init__(self, root):
        self._root = root

    def scan(self, callback):
        """:param callback: calls when source file was updated."""

        found = []
        for root, dirs, files in os.walk(self._root):
            for f in files:
                if f.endswith('.md'):
                    path = os.path.join(root, f)
                    found.append(path)
                    modified = time.ctime(os.path.getmtime(path))
                    if path not in self._sources:
                        callback(path)
                        self._sources[path] = modified
                    elif self._sources[path] != modified:
                        callback(path)
                        self._sources[path] = modified
        # look for deleted files
        for path in list(self._sources.keys()):
            if path not in found:
                callback(path, delete=True)
                del self._sources[path]


source = Source(root=SOURCE_FOLDER)


class Pages(object):
    """Pages content storage."""

    _pages = {}
    _labels = {}

    def __init__(self, root):
        self._root = root

    def get(self, path):
        return self._pages.get(path)

    def list(self):
        pages_list = [v for v in self._pages.values() if not v['hide']]
        pages_list = sorted(pages_list, key=lambda i: i['created'], reverse=True)
        return pages_list

    def labels(self):
        return sorted(self._labels.values(), key=lambda i: i['title'])

    def label(self, slug):
        label = dict(self._labels.get(slug, {'pages': {}, 'title': 'Not found', 'slug': slug}))
        label['pages'] = sorted(label['pages'].values(), key=lambda i: i['created'], reverse=True)
        return label

    def update(self, path, delete=False):
        """Update inmemory cache.
        :param path: absolute path to source file.
        :param delete: delete page is == True else - update.
        :return: None
        """
        relative_path = ('/'.join([s for s in path.split(self._root)[-1].split('/') if s])).split('.md')[0]
        try:
            if delete:
                logger.warning('Delete {path}.'.format(path=relative_path))
                del self._pages[relative_path]
                for label in self._labels.values():
                    if relative_path in label['pages']:
                        del label['pages'][relative_path]
                for slug in list(self._labels.keys()):
                    if not self._labels[slug]['pages']:
                        del self._labels[slug]
                return None
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
                APIExtension(),
            ])
            html = md.convert(source_md)
            created = md.Meta.get('created')
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(path)
            if created:
                created = arrow.get(created[0]).datetime
            else:
                created = arrow.get(ctime).datetime
            modified = md.Meta.get('modified')
            if modified:
                modified = arrow.get(modified[0]).datetime
            else:
                modified = created

            page = {
                'path': relative_path,
                'html': html,
                'title': md.Meta['title'][0] if md.Meta.get('title') else md.title,
                'meta': md.Meta,
                'created': created,
                'modified': modified,
                'hide': (md.Meta['hide'][0]).lower() == 'true' if 'hide' in md.Meta else False,
                'labels': [],
            }
            self._pages[relative_path] = page
            for label in md.Meta.get('labels', []):
                label_slug = slugify(label)
                page['labels'].append({'slug': label_slug, 'title': label})
                if not page['hide']:
                    if label_slug not in self._labels:
                        self._labels[label_slug] = {
                            'slug': label_slug,
                            'title': label,
                            'pages': {},
                        }
                    self._labels[label_slug]['pages'][page['path']] = page
        except Exception as e:
            logger.warning('Error while processing {path}: {error}'.format(
                path=relative_path, error=e
            ))


pages = Pages(root=SOURCE_FOLDER)


class Watcher(object):

    def __init__(self):
        self.ioloop = IOLoop.instance()

    def watch(self, repeat=True):
        source.scan(callback=pages.update)
        if repeat:
            self.ioloop.add_timeout(deadline=datetime.timedelta(seconds=2), callback=self.watch)
