import os

from . import SRC_DIR

SSR_CONF = {
    'url': (
        'ssr://'
        'OjoxOjMwMDAwOm5vbmU6dGVzdDpwbGFpbjpkR1Z6ZEEvP29iZnNwYXJhbT'
        '0mcHJvdG9wYXJhbT0mcmVtYXJrcz1kR1Z6ZEEmZ3JvdXA9ZEdWemRB'),
    'info': {
        'server': '::1',
        'server_port': 30000,
        'protocol': 'none',
        'method': 'test',
        'obfs': 'plain',
        'password': 'test',
        'obfs_param': '',
        'protocol_param': '',
        'remarks': 'test',
        'group': 'test',
    },
    'json': {
        'server': '::1',
        'server_port': 30000,
        'protocol': 'none',
        'method': 'test',
        'obfs': 'plain',
        'password': 'test',
        'obfs_param': '',
        'protocol_param': '',
    }
}

CMD_PREFIX = ['python3', '-m', 'ssrcli.cmd']

_venv_env = os.environ.copy()
if _venv_env.get('PYTHONPATH', None):
    _venv_env['PYTHONPATH'] += ':{}'.format(SRC_DIR)
else:
    _venv_env['PYTHONPATH'] = SRC_DIR
VENV_ENV = _venv_env
