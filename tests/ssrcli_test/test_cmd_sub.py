import subprocess
import json

import pytest

from .shared import CMD_PREFIX, SUBPROCESS_KWARGS

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
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 1


@init_sub_table
def test_list_some_sub():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    process = subprocess.run(CMD_PREFIX + ['-Slc', '1'], **SUBPROCESS_KWARGS)
    assert 'name: test' in process.stdout


@init_sub_table
def test_list_some_sub_verbosely():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    process = subprocess.run(CMD_PREFIX + ['-vSlc', '1'], **SUBPROCESS_KWARGS)
    stdout = process.stdout
    for sign in ['{}: {}'.format(*pair) for pair in SSR_SUB.items()]:
        assert sign in stdout  # TODO(myl7): assert ssrconf_set


@init_sub_table
def test_list_all_sub():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    process = subprocess.run(CMD_PREFIX + ['-Sl'], **SUBPROCESS_KWARGS)
    assert process.stdout.count('name: test') >= 2


@init_sub_table
def test_list_all_sub_with_a():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    process = subprocess.run(CMD_PREFIX + ['-Sla'], **SUBPROCESS_KWARGS)
    assert process.stdout.count('name: test') >= 2


@init_sub_table
def test_edit_sub():
    pass  # TODO(myl7): Not implement


@init_sub_table
def test_delete_sub():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Sdc', '1'], **SUBPROCESS_KWARGS)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 0


@init_sub_table
def test_delete_all_sub():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Sda'], **SUBPROCESS_KWARGS)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 0


@init_sub_table
def test_delete_sub_without_info():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(SSR_SUB)], **SUBPROCESS_KWARGS)
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(CMD_PREFIX + ['-Sd'], **SUBPROCESS_KWARGS)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT COUNT(id) FROM ssrsub WHERE name = 'test'").fetchone()
    assert query_result[0] == 1


@init_sub_table
def test_update_some_sub():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(LOCAL_TEST_SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Suc', '1'], **SUBPROCESS_KWARGS)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 1").fetchone()
    assert query_result == ('::1', 30000)


@init_sub_table
def test_update_all_sub():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(LOCAL_TEST_SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(LOCAL_TEST_SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Su'], **SUBPROCESS_KWARGS)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 1").fetchone()
    assert query_result == ('::1', 30000)
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 2").fetchone()
    assert query_result == ('::1', 30000)


@init_sub_table
def test_update_all_sub_with_a():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(LOCAL_TEST_SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(LOCAL_TEST_SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Sua'], **SUBPROCESS_KWARGS)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 1").fetchone()
    assert query_result == ('::1', 30000)
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 2").fetchone()
    assert query_result == ('::1', 30000)


def test_omit_current_in_sub_list():
    subprocess.run(CMD_PREFIX + ['-Sl'], **SUBPROCESS_KWARGS)


@init_sub_table
def test_update_sub_with_proxies():
    subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(LOCAL_TEST_SSR_SUB)], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-Suap', '{"http": "http://127.0.0.1:8002"}'], **SUBPROCESS_KWARGS)
    cursor = db.cursor()
    query_result = cursor.execute("SELECT server, server_port FROM ssrconf WHERE sub_id = 1").fetchone()
    assert query_result == ('::1', 30000)
