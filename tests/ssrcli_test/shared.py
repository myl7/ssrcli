import re
import os
import sys
import subprocess

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
