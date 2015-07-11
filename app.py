""" Site in Markdown in one file. """

# initialize options, keep it in top
from mdpages import settings

from tornado.ioloop import IOLoop
from tornado import options
from tornado import web

from mdpages.handlers import IndexHandler, PageHandler, SitemapHandler
from mdpages.models import Watcher, SOURCE_FOLDER
from mdpages.utils import rel


if __name__ == '__main__':
    options.parse_command_line()
    application = web.Application(handlers=[
            (r'/', IndexHandler),
            (r'/sitemap\.xml', SitemapHandler),
            (r'/(.+\.(?:png|jpg|css))', web.StaticFileHandler, {'path': SOURCE_FOLDER}),
            (r'/(?P<path>[\w/-]+)', PageHandler),
        ],
        debug=options.options.DEBUG,
        template_path=rel('templates'),
    )
    application.listen(port=options.options.PORT)
    Watcher().watch()
    IOLoop.instance().start()
