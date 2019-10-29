import subprocess
import json

from .shared import CMD_PREFIX, VENV_ENV

from ssrcli.models import db, SsrSub

SSR_SUB = {
    'name': 'test',
    'url': 'http://127.0.0.1:8000/',
}

LOCAL_TEST_SSR_SUB = {
    'name': 'local test',
    'url': 'http://127.0.0.1:8001/index.txt',
}


def init_sub_table(func):
    def wrapper():
        SsrSub.truncate_table()
        func()

    return wrapper


@init_sub_table
def test_add_sub():
    pass
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 1


@init_sub_table
def test_list_some_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['sub', 'l', '-c', '1'], stdout=subprocess.PIPE, env=VENV_ENV)
    assert 'name: test' in process.stdout.decode('utf-8')


@init_sub_table
def test_list_some_sub_verbosely():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['-v', 'sub', 'l', '-c', '1'], stdout=subprocess.PIPE, env=VENV_ENV)
    stdout = process.stdout.decode('utf-8')
    for sign in ['{}: {}'.format(*pair) for pair in SSR_SUB.items()]:
        assert sign in stdout  # TODO(myl7): assert ssrconf_set


@init_sub_table
def test_list_all_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['sub', 'l'], stdout=subprocess.PIPE, env=VENV_ENV)
    assert process.stdout.decode('utf-8').count('name: test') >= 2


@init_sub_table
def test_list_all_sub_with_a():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    process = subprocess.run(CMD_PREFIX + ['sub', 'l', '-a'], stdout=subprocess.PIPE, env=VENV_ENV)
    assert process.stdout.decode('utf-8').count('name: test') >= 2


@init_sub_table
def test_edit_sub():
    pass  # TODO(myl7): Not implement


@init_sub_table
def test_delete_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'd', '-c', '1'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 0


@init_sub_table
def test_delete_all_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'd', '-a'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 0


@init_sub_table
def test_delete_sub_without_info():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'd'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 1


@init_sub_table
def test_update_some_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(LOCAL_TEST_SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'u', '-c', '1'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 1").fetchone()
    assert query_result == ('::1', 30000)


@init_sub_table
def test_update_all_sub():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(LOCAL_TEST_SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(LOCAL_TEST_SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'u'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 1").fetchone()
    assert query_result == ('::1', 30000)
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 2").fetchone()
    assert query_result == ('::1', 30000)


@init_sub_table
def test_update_all_sub_with_a():
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(LOCAL_TEST_SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'a', '-j', json.dumps(LOCAL_TEST_SSR_SUB)], env=VENV_ENV)
    subprocess.run(CMD_PREFIX + ['sub', 'u', '-a'], env=VENV_ENV)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 1").fetchone()
    assert query_result == ('::1', 30000)
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 2").fetchone()
    assert query_result == ('::1', 30000)
