import subprocess
import json
from typing import Optional, List

import pytest

from .shared import CMD_PREFIX, SUBPROCESS_KWARGS, ID_REGEX
from ssrcli.models import db

SSR_SUB = {
    'name': 'test',
    'url': 'http://127.0.0.1:8000/',
}

LOCAL_TEST_SSR_SUB = {
    'name': 'local test',
    'url': 'http://127.0.0.1:8001/index.txt',
}


def add_sub_get_id(sub: Optional[dict] = None) -> int:
    process = subprocess.run(CMD_PREFIX + ['-Snj', json.dumps(sub if sub else SSR_SUB)], **SUBPROCESS_KWARGS)
    return int(ID_REGEX.match(process.stdout).group(1))


def test_add_sub():
    s_id = add_sub_get_id()
    query_result = db.cursor().execute("SELECT COUNT(id) FROM ssrsub WHERE id = {}".format(s_id)).fetchone()
    assert query_result[0] == 1


def test_list_some_sub():
    s_ids = [add_sub_get_id(), add_sub_get_id(), add_sub_get_id()]
    process = subprocess.run(CMD_PREFIX + ['-Slc', str(s_ids[0]), '-c', str(s_ids[1])], **SUBPROCESS_KWARGS)
    assert 'id: {}'.format(s_ids[0]) in process.stdout
    assert 'id: {}'.format(s_ids[1]) in process.stdout


def test_list_some_sub_verbosely():
    s_ids = [add_sub_get_id(), add_sub_get_id(), add_sub_get_id()]
    process = subprocess.run(CMD_PREFIX + ['-vSlc', str(s_ids[0]), '-c', str(s_ids[1])], **SUBPROCESS_KWARGS)
    stdout = process.stdout
    for sign in ['{}: {}'.format(*pair) for pair in SSR_SUB.items()]:
        assert sign in stdout  # TODO: Assert conf belonging to the sub
    assert 'id: {}'.format(s_ids[0]) in process.stdout
    assert 'id: {}'.format(s_ids[1]) in process.stdout


def test_list_all_sub():
    s_ids = [add_sub_get_id(), add_sub_get_id(), add_sub_get_id()]
    process = subprocess.run(CMD_PREFIX + ['-Sl'], **SUBPROCESS_KWARGS)
    for s_id in s_ids:
        assert 'id: {}'.format(s_id) in process.stdout
    assert process.stdout.count('id: ') >= 2

    process = subprocess.run(CMD_PREFIX + ['-Sla'], **SUBPROCESS_KWARGS)
    for s_id in s_ids:
        assert 'id: {}'.format(s_id) in process.stdout
    assert process.stdout.count('id: ') >= 2


def test_edit_sub():
    pass  # TODO


def test_delete_sub():
    s_ids = [add_sub_get_id(), add_sub_get_id()]
    subprocess.run(CMD_PREFIX + ['-Sdc', str(s_ids[0]), '-c', str(s_ids[1])], **SUBPROCESS_KWARGS)
    query_result = db.cursor().execute(
        "SELECT COUNT(id) FROM ssrsub WHERE id = {} OR id = {}".format(*s_ids)).fetchone()
    assert query_result[0] == 0


def test_delete_all_sub():
    add_sub_get_id()
    subprocess.run(CMD_PREFIX + ['-Sda'], **SUBPROCESS_KWARGS)
    query_result = db.cursor().execute("SELECT COUNT(id) FROM ssrsub").fetchone()
    assert query_result[0] == 0


def test_delete_sub_without_info():
    s_id = add_sub_get_id()
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(CMD_PREFIX + ['-Sd'], **SUBPROCESS_KWARGS)
    query_result = db.cursor().execute("SELECT COUNT(id) FROM ssrsub WHERE id = {}".format(s_id)).fetchone()
    assert query_result[0] == 1


def _check_updated_subs(s_ids: List[int]):
    cursor = db.cursor()
    for s_id in s_ids:
        query_result = cursor.execute(
            "SELECT server, server_port FROM ssrconf WHERE sub_id = {}".format(s_id)).fetchone()
        assert query_result == ('::1', 30000)


def test_update_some_sub():
    s_id = add_sub_get_id(LOCAL_TEST_SSR_SUB)
    subprocess.run(CMD_PREFIX + ['-Suc', str(s_id)], **SUBPROCESS_KWARGS)
    _check_updated_subs([s_id])


def test_update_all_sub():
    subprocess.run(CMD_PREFIX + ['-Sda'], **SUBPROCESS_KWARGS)
    s_ids = [add_sub_get_id(LOCAL_TEST_SSR_SUB), add_sub_get_id(LOCAL_TEST_SSR_SUB)]
    subprocess.run(CMD_PREFIX + ['-Su'], **SUBPROCESS_KWARGS)
    _check_updated_subs(s_ids)


def test_update_all_sub_with_a():
    subprocess.run(CMD_PREFIX + ['-Sda'], **SUBPROCESS_KWARGS)
    s_ids = [add_sub_get_id(LOCAL_TEST_SSR_SUB), add_sub_get_id(LOCAL_TEST_SSR_SUB)]
    subprocess.run(CMD_PREFIX + ['-Sua'], **SUBPROCESS_KWARGS)
    _check_updated_subs(s_ids)


def test_update_sub_with_proxies():
    s_id = add_sub_get_id(LOCAL_TEST_SSR_SUB)
    subprocess.run(CMD_PREFIX + ['-Suc', str(s_id), '-p', '{"http": "http://127.0.0.1:8002"}'],
                   **SUBPROCESS_KWARGS)
    _check_updated_subs([s_id])
