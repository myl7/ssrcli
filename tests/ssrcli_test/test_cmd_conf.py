import subprocess
import json

from .shared import CMD_PREFIX, SSR_CONF, VENV_ENV

from ssrcli.config import config
from ssrcli.models import db, SsrConf


def init_conf_table(func):
    def wrapper():
        SsrConf.truncate_table()
        func()

    return wrapper


@init_conf_table
def test_add_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute(
        "SELECT COUNT(id) FROM ssrconf WHERE remarks = 'test' AND `group` = 'test'").fetchone()
    assert query_result[0] == 1


@init_conf_table
def test_list_some_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['conf', 'l', '-c', '1'], stdout=subprocess.PIPE, env=VENV_ENV)
    assert 'remarks: test' in process.stdout.decode('utf-8')


@init_conf_table
def test_list_some_conf_verbosely():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['-v', 'conf', 'l', '-c', '1'], stdout=subprocess.PIPE, env=VENV_ENV)
    stdout = process.stdout.decode('utf-8')
    for sign in ['"{}": "{}"'.format(*pair) for pair in SSR_CONF['dict'].items() if isinstance(pair[1], str)]:
        assert sign in stdout


@init_conf_table
def test_list_all_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['conf', 'l'], stdout=subprocess.PIPE, env=VENV_ENV)
    assert process.stdout.decode('utf-8').count('remarks: test') >= 2


@init_conf_table
def test_list_all_conf_with_a():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['conf', 'l', '-a'], stdout=subprocess.PIPE, env=VENV_ENV)
    assert process.stdout.decode('utf-8').count('remarks: test') >= 2


@init_conf_table
def test_edit_conf():
    pass  # TODO(myl7): Not implement


@init_conf_table
def test_delete_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 'd', '-c', '1'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute(
        "SELECT COUNT(id) FROM ssrconf WHERE remarks = 'test' AND `group` = 'test'").fetchone()
    assert query_result[0] == 0


@init_conf_table
def test_delete_conf_without_info():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 'd'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute(
        "SELECT COUNT(id) FROM ssrconf WHERE remarks = 'test' AND `group` = 'test'").fetchone()
    assert query_result[0] == 1


@init_conf_table
def test_use_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 's', '-c', '1'], env=VENV_ENV)
    with open(config.SSR_CONF_PATH, 'r') as file:
        assert json.load(file) == {**SSR_CONF['config_dict'], **config.SSR_CONF_EXTRA_FIELDS}


@init_conf_table
def test_list_current_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'a', '-j', json.dumps(SSR_CONF['dict'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 's', '-c', '1'], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['conf', 'l', '-a', '-r'], stdout=subprocess.PIPE, env=VENV_ENV)
    assert '"remarks": "test"' in process.stdout.decode('utf-8')
