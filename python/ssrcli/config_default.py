class ImmutableConfig:
    VERSION = '1.0.1'


class DefaultConfig(ImmutableConfig):
    DB_URL = 'data.sqlite3'

    SSR_CONF_PATH = 'config.json'
    SSR_CONF_EXTRA_FIELDS = {
        "local_address": "0.0.0.0",
        "local_port": 1080,
        "timeout": 300,
    }
