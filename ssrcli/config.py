import pathlib
import json

import xdg

from . import __version__
from .log import logger

APP_CONFIG_SUFFIX = pathlib.Path('ssrcli/ssrcli-config.json')
SSR_CONFIG_SUFFIX = pathlib.Path('ssrcli/ssr-config.json')


class DefaultConfig:
    VERSION = __version__
    DB_PATH = str(xdg.XDG_DATA_HOME / 'ssrcli' / 'data.sqlite3')
    SSR_CONF_PATH = str(xdg.XDG_CONFIG_HOME / SSR_CONFIG_SUFFIX)
    SSR_APP_PATH = str(xdg.XDG_DATA_HOME / 'shadowsocksr')
    SSR_CONF_EXTRA_FIELDS = dict(local_address='0.0.0.0', local_port=1080, timeout=300)


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
                for k, v in config_json.items():
                    k.upper()
                    if k not in attrs:
                        logger.warn('Config key {} is not supported'.format(k))
                    else:
                        setattr(self, k, v)
            break


config = Config()
