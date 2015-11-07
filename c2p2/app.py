# initialize options, keep it in top
from .settings import *

import os.path

from tornado.ioloop import IOLoop
from tornado import options
from tornado import web

from .handlers import GitHubPullHandler, PageHandler, SitemapHandler, LabelHandler, RobotsHandler
from .models import Watcher


__all__ = ('run',)


def run(source_folder):
    options.options.SOURCE_FOLDER = source_folder

    application = web.Application(
        handlers=[
            web.url(r'/', LabelHandler, name='index'),
            web.url(r'/pull', GitHubPullHandler, name='git-pull'),
            web.url(r'/sitemap\.xml', SitemapHandler, name='sitemap'),
            web.url(r'/robots\.txt', RobotsHandler, name='robots'),
            web.url(r'/label/(?P<slug>[\w/-]+)', LabelHandler, name='label'),
            web.url(r'/(.+\.(?:png|jpg|css|ico))',
                web.StaticFileHandler, {'path': options.options.SOURCE_FOLDER}, name='static'),
            web.url(r'/(?P<uri>[\w/-]+)', PageHandler, name='page'),
        ],
        debug=options.options.DEBUG,
        template_path=os.path.join(options.options.SOURCE_FOLDER, 'engine', 'templates'),
    )

    application.listen(port=options.options.PORT)
    Watcher().watch(repeat=options.options.WATCH)
    IOLoop.instance().start()
