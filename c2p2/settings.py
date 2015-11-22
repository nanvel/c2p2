import os

from tornado import options


__all__ = ('settings',)


DEFAULT = {
    'DEBUG': (bool, True, "Enable tornado debug mode."),
    'PORT': (int, 5000, "Port the app listening to."),
    'SOURCE_FOLDER': (str, '..', "Path to folder that contains pages source."),
    'UPDATE_TIMEOUT': (int, 2, "Number of seconds to rescan source folder. 0 - disable."),
    'GITHUB_VALIDATE_IP': (bool, True, "Enable GitHub ip validation."),
    'GITHUB_SECRET': (str, '', "GitHub web hook secret, optional."),
    'GITHUB_BRANCH': (str, 'master', "GitHub branch to watch."),
}


ENV_PREFIX = 'C2P2_'


for name, v in DEFAULT.items():
    v_type, v_default, v_help = v
    v_value = os.getenv(ENV_PREFIX + name, v_default)
    if v_type == bool and isinstance(v_default, str):
        v_default = v_default.lower() == 'true'
    options.define(name=name, default=v_default, type=v_type, help=v_help)


options.parse_command_line()


settings = options.options
