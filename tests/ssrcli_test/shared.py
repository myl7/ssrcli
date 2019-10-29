import os

from . import pkg_dir

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
        '_meta': {
            'id': 1,
            'remarks': 'test',
            'group': 'test',
            'sub': None,
        },
    },
}

CMD_PREFIX = ['python3', '-m', 'ssrcli.cli']

_venv_env = os.environ.copy()
if _venv_env.get('PYTHONPATH', None):
    _venv_env['PYTHONPATH'] += ':{}'.format(str(pkg_dir))
else:
    _venv_env['PYTHONPATH'] = str(pkg_dir)
VENV_ENV = _venv_env
