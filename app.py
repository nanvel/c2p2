# initialize options, keep it in top
from mdpages import settings

from tornado.ioloop import IOLoop
from tornado import options
from tornado import web

from mdpages.handlers import PageHandler, SitemapHandler, LabelHandler, RobotsHandler
from mdpages.models import Watcher, SOURCE_FOLDER
from mdpages.utils import rel


if __name__ == '__main__':
    options.parse_command_line()
    application = web.Application(handlers=[
            web.url(r'/', LabelHandler, name='index'),
            web.url(r'/sitemap\.xml', SitemapHandler, name='sitemap'),
            web.url(r'/robots\.txt', RobotsHandler, name='robots'),
            web.url(r'/label/(?P<slug>[\w/-]+)', LabelHandler, name='label'),
            web.url(r'/(.+\.(?:png|jpg|css))', web.StaticFileHandler, {'path': SOURCE_FOLDER}, name='static'),
            web.url(r'/(?P<path>[\w/-]+)', PageHandler, name='page'),
        ],
        debug=options.options.DEBUG,
        template_path=rel('templates'),
    )
    application.listen(port=options.options.PORT)
    if options.options.WATCH:
        Watcher().watch()
    IOLoop.instance().start()
