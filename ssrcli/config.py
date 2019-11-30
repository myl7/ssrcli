import pathlib
import json

import xdg

from . import __version__
from .log import logger

for path in [xdg.XDG_DATA_HOME, xdg.XDG_CONFIG_HOME]:
    if not (path / 'ssrcli').exists():
        (path / 'ssrcli').mkdir()

APP_CONFIG_SUFFIX = pathlib.Path('ssrcli/ssrcli-config.json')
SSR_CONFIG_SUFFIX = pathlib.Path('ssrcli/ssr-config.json')


class DefaultConfig:
    VERSION: str = __version__
    DB_PATH = str(xdg.XDG_DATA_HOME / 'ssrcli' / 'db.sqlite3')
    UPDATE_TIMEOUT = 10
    UPDATE_RETRY = 5
    SSR_CONF_PATH = str(xdg.XDG_CONFIG_HOME / SSR_CONFIG_SUFFIX)
    SSR_APP_PATH = str(xdg.XDG_DATA_HOME / 'shadowsocksr')
    SSR_LOCAL_PORT = 1080
    SSR_CONF_EXTRA_FIELDS = {
        'local_address': '127.0.0.1',
        'local_port': SSR_LOCAL_PORT,
        'timeout': 300,
    }


class Config(DefaultConfig):
    def __init__(self):
        super().__init__()
        for xdg_config_dir in xdg.XDG_CONFIG_DIRS:
            if (xdg_config_dir / APP_CONFIG_SUFFIX).is_file():
                with open(xdg_config_dir / APP_CONFIG_SUFFIX, 'r') as f:
                    try:
                        config_json: dict = json.load(f)
                    except json.JSONDecodeError:
                        logger.error('Can not parse the json config file located at {}'.format(
                            xdg_config_dir / APP_CONFIG_SUFFIX))
                attrs = [attr.upper() for attr in dir(self) if attr[0] != '_']
                attrs.remove('VERSION')
                for k, v in config_json.items():
                    k = k.upper()
                    if k not in attrs:
                        logger.warn('Config key {} is not supported'.format(k))
                    else:
                        setattr(self, k, v)
                break


config = Config()
