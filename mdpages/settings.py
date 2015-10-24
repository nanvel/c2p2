import os

from six import iteritems

from tornado import options


__all__ = []


DEFAULT = {
    'DEBUG': (bool, True, "Enable debug mode."),
    'PORT': (int, 5000, "Port app listening to."),
    'SITE_NAME': (str, 'Site name', "Site name, show in title."),
    'BASE_URL': (str, 'http://mysite.com', "Site base url, uses in sitemap.xml."),
    'SOURCE_FOLDER': (str, 'source', "Relative or absolute path to the folder contains pages source."),
    'DEFAULT_LABEL': (str, 'public', "Default label (for index page)."),
    'THEME': (str, 'default', "Theme."),
    'WATCH': (bool, True, "Watch for changes in the source files."),
    'GITHUB_VALIDATE_IP': (bool, True, "Enable github ip validation."),
    'GITHUB_SECRET': (str, '', "GitHub hooks secret, not required."),
    'GITHUB_BRANCH': (str, 'master', "GitHub branch to watch."),
}

ENV_PREFIX = 'MDPAGES_'


for name, v in iteritems(DEFAULT):
    v_type, v_default, v_help = v
    v_value = os.getenv(ENV_PREFIX + name, v_default)
    options.define(name=name, default=v_default, type=v_type, help=v_help)


options.parse_command_line()
