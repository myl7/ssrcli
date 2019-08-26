import subprocess
import json
from typing import Callable

from .shared_variables import SRC_DIR, CMD_PREFIX, SSR_CONF, VENV_ENV

from ssrcli.config import config
from ssrcli.models import db, SsrConf


def init_conf_table(func: Callable[[], None]) -> Callable[[], None]:
    def wrapper():
        SsrConf.truncate_table()
        func()

    return wrapper


@init_conf_table
def test_add_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'add', '-j', json.dumps(SSR_CONF['info'])], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute(
        "SELECT COUNT(id) FROM ssrconf WHERE remarks = 'test' AND `group` = 'test'").fetchone()
    assert query_result[0] == 1


@init_conf_table
def test_get_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'add', '-j', json.dumps(SSR_CONF['info'])], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['conf', 'get', '-i', '1'], capture_output=True, env=VENV_ENV)
    assert 'remarks: test' in process.stdout.decode('utf-8')


@init_conf_table
def test_list_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'add', '-j', json.dumps(SSR_CONF['info'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 'add', '-j', json.dumps(SSR_CONF['info'])], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['conf', 'ls'], capture_output=True, env=VENV_ENV)
    assert process.stdout.decode('utf-8').count('remarks: test') >= 2


@init_conf_table
def test_edit_conf():
    pass  # TODO(myl7): Not implement


@init_conf_table
def test_delete_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'add', '-j', json.dumps(SSR_CONF['info'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 'rm', '-i', '1'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute(
        "SELECT COUNT(id) FROM ssrconf WHERE remarks = 'test' AND `group` = 'test'").fetchone()
    assert query_result[0] == 0


@init_conf_table
def test_take_conf():
    subprocess.run(CMD_PREFIX + ['conf', 'add', '-j', json.dumps(SSR_CONF['info'])], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['conf', 'take', '-i', '1'], env=VENV_ENV)
    with open('config.json', 'r') as file:
        assert json.load(file) == {**SSR_CONF['json'], **config.SSR_CONF_EXTRA_FIELDS}
