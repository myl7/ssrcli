import re
import os
import sys
import json
import pathlib
import subprocess

import xdg

from . import pkg_dir

SSR_CONF = {
    'url': ('ssr://OjoxOjMwMDAwOm9yaWdpbjpub25lOnBsYWluOmRHVnpkQS8_b2Jmc3BhcmFtP'
            'SZwcm90b3BhcmFtPSZyZW1hcmtzPWRHVnpkQSZncm91cD1kR1Z6ZEE'),
    'dict': {
        'server': '::1',
        'server_port': 30000,
        'protocol': 'origin',
        'method': 'none',
        'obfs': 'plain',
        'password': 'test',
        'obfs_param': '',
        'protocol_param': '',
        'remarks': 'test',
        'group': 'test',
    },
    'config_dict': {
        'server': '::1',
        'server_port': 30000,
        'protocol': 'origin',
        'method': 'none',
        'obfs': 'plain',
        'password': 'test',
        'obfs_param': '',
        'protocol_param': '',
        '_meta': {
            'id': 1,
            'remarks': 'test',
            'group': 'test',
            'sub': None,
        },
    },
}

CMD_PREFIX = ['python3', '-m', 'ssrcli']

_venv_env = os.environ.copy()
if _venv_env.get('PYTHONPATH', None):
    _venv_env['PYTHONPATH'] += ':{}'.format(str(pkg_dir))
else:
    _venv_env['PYTHONPATH'] = str(pkg_dir)
VENV_ENV = _venv_env

if sys.version_info[2] >= 7:
    SUBPROCESS_KWARGS = {
        'env': VENV_ENV,
        'check': True,
        'universal_newlines': True,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'timeout': 10,
    }
else:
    SUBPROCESS_KWARGS = {
        'env': VENV_ENV,
        'check': True,
        'text': True,
        'capture_output': True,
        'timeout': 10,
    }

ID_REGEX = re.compile(r'^id: (\d+)$', flags=re.MULTILINE)

if not pathlib.Path(xdg.XDG_CONFIG_HOME / 'ssrcli').exists():
    pathlib.Path(xdg.XDG_CONFIG_HOME / 'ssrcli').mkdir()

SSRCLI_CONFIG = dict(
    update_retry=6,
    UPDATE_TIMEOUT=11,
    SSR_CONF_EXTRA_FIELDS={
        'local_address': '127.0.0.1',
        'local_port': 1080,
        'timeout': 300,
        'fast_open': True,
    },
)
with open(xdg.XDG_CONFIG_HOME / 'ssrcli' / 'ssrcli-config.json', 'w') as f:
    f.write(json.dumps(SSRCLI_CONFIG))

with open(xdg.XDG_CONFIG_HOME / 'ssrcli' / 'ssr-config.json', 'w') as f:
    f.write(json.dumps({**SSR_CONF['config_dict'], **SSRCLI_CONFIG['SSR_CONF_EXTRA_FIELDS']}))
