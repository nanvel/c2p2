import os

from tornado import options


__all__ = ('settings',)


DEFAULT = {
    'DEBUG': (bool, True, "Enable debug mode."),
    'PORT': (int, 5000, "Port app listening to."),
    'SOURCE_FOLDER': (str, '..', "Relative or absolute path to the folder contains pages source."),
    'UPDATE_TIMEOUT': (int, 2, "Rescan source folder for updates every number of seconds, 0 - disable."),
    'GITHUB_VALIDATE_IP': (bool, True, "Enable github ip validation."),
    'GITHUB_SECRET': (str, '', "GitHub hooks secret, not required."),
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
