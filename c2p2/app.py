import os.path

from tornado import web
from tornado.ioloop import IOLoop, PeriodicCallback

from .handlers import GitHubPullHandler, PageHandler, SitemapHandler, LabelHandler, RobotsHandler
from .models import Site
from .settings import settings


__all__ = ('run',)


def run():

    application = web.Application(
        handlers=[
            web.url(r'/', LabelHandler, name='index'),
            web.url(r'/pull', GitHubPullHandler, name='git-pull'),
            web.url(r'/sitemap\.xml', SitemapHandler, name='sitemap'),
            web.url(r'/robots\.txt', RobotsHandler, name='robots'),
            web.url(r'/label/(?P<slug>[\w/-]+)', LabelHandler, name='label'),
            web.url(r'/(.+\.(?:png|jpg|css|ico))',
                web.StaticFileHandler, {'path': settings.SOURCE_FOLDER}, name='static'),
            web.url(r'/(?P<uri>[\w/-]+)', PageHandler, name='page'),
        ],
        debug=settings.DEBUG,
        template_path=os.path.join(settings.SOURCE_FOLDER, 'engine', 'templates'),
    )

    application.listen(port=settings.PORT)

    Site().update()

    if settings.UPDATE_TIMEOUT:
        PeriodicCallback(Site().update, settings.UPDATE_TIMEOUT * 1000).start()

    IOLoop.instance().start()
