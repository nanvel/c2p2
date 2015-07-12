from tornado.options import define


__all__ = []


define(name='DEBUG', default=True, type=bool, help="Enable debug mode.")
define(name='PORT', default='5000', type=int, help="Port app listening to.")
define(name='SITE_NAME', default='Site name', type=str, help="Site name, show in title.")
define(name='BASE_URL', default='http://mysite.com', type=str, help="Site base url, uses in sitemap.xml.")
define(
    name='SOURCE_FOLDER', default='source', type=str,
    help="Relative or absolute path to the folder contains pages source.")
define(name='DEFAULT_LABEL', default='public', type=str, help="Default label (for index page).")
define(name='THEME', default='default', type=str, help="Theme.")
define(name='WATCH', default=True, type=bool, help="Watch for changes in the source files.")
