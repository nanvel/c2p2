# initialize options, keep it in top
from mdpages import settings

from tornado.ioloop import IOLoop
from tornado import options
from tornado import web

from mdpages.handlers import (
    GitHubPullHandler, PageHandler, SitemapHandler, LabelHandler, RobotsHandler, TEMPLATES_FOLDER)
from mdpages.models import Watcher, SOURCE_FOLDER
from mdpages.utils import rel


application = web.Application(handlers=[
        web.url(r'/pull', GitHubPullHandler, name='git-pull'),
        web.url(r'/', LabelHandler, name='index'),
        web.url(r'/sitemap\.xml', SitemapHandler, name='sitemap'),
        web.url(r'/robots\.txt', RobotsHandler, name='robots'),
        web.url(r'/static/(.+\.(?:png|jpg|css))', web.StaticFileHandler, {'path': TEMPLATES_FOLDER}, name='template'),
        web.url(r'/label/(?P<slug>[\w/-]+)', LabelHandler, name='label'),
        web.url(r'/(.+\.(?:png|jpg))', web.StaticFileHandler, {'path': SOURCE_FOLDER}, name='static'),
        web.url(r'/(?P<path>[\w/-]+)', PageHandler, name='page'),
    ],
    debug=options.options.DEBUG,
    template_path=rel('templates'),
)


if __name__ == '__main__':
    application.listen(port=options.options.PORT)
    Watcher().watch(repeat=options.options.WATCH)
    IOLoop.instance().start()
