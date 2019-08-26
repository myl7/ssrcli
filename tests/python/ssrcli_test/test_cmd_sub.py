import subprocess
import json
from typing import Callable

from .shared_variables import CMD_PREFIX, VENV_ENV

from ssrcli.models import db, SsrSub

SSR_SUB = {
    'name': 'test',
    'url': 'http://127.0.0.1:8000/',
}


def init_sub_table(func: Callable[[], None]) -> Callable[[], None]:
    def wrapper():
        SsrSub.truncate_table()
        func()

    return wrapper


@init_sub_table
def test_add_sub():
    pass
    subprocess.run(CMD_PREFIX + ['sub', 'add', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 1


# `get` is deprecated
@init_sub_table
def test_get_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'add', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['sub', 'get', '-i', '1'], capture_output=True, env=VENV_ENV)
    assert 'name: test' in process.stdout.decode('utf-8')


@init_sub_table
def test_list_some_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'add', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['sub', 'ls', '-i', '1'], capture_output=True, env=VENV_ENV)
    assert 'name: test' in process.stdout.decode('utf-8')


@init_sub_table
def test_list_all_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'add', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'add', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['sub', 'ls'], capture_output=True, env=VENV_ENV)
    assert process.stdout.decode('utf-8').count('name: test') >= 2


@init_sub_table
def test_edit_sub():
    pass  # TODO(myl7): Not implement


@init_sub_table
def test_delete_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'add', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'rm', '-i', '1'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 0


@init_sub_table
def test_update_some_sub():
    pass


@init_sub_table
def test_update_all_sub():
    pass
