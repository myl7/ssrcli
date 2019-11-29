import subprocess
import json

import pytest

from .shared import CMD_PREFIX, SSR_CONF, SUBPROCESS_KWARGS, ID_REGEX
from ssrcli.config import config
from ssrcli.models import db


def add_conf_get_id() -> int:
    process = subprocess.run(CMD_PREFIX + ['-Cnj', json.dumps(SSR_CONF['dict'])], **SUBPROCESS_KWARGS)
    return int(ID_REGEX.match(process.stdout).group(1))


def test_add_conf():
    c_id = add_conf_get_id()
    query_result = db.cursor().execute(
        "SELECT COUNT(id) FROM ssrconf WHERE id = {}".format(c_id)).fetchone()
    assert query_result[0] == 1


def test_add_conf_by_share_url():
    c_id = add_conf_get_id()
    query_result = db.cursor().execute(
        "SELECT COUNT(id) FROM ssrconf WHERE id = {}".format(c_id)).fetchone()
    assert query_result[0] == 1


def test_list_some_conf():
    c_ids = [add_conf_get_id(), add_conf_get_id(), add_conf_get_id()]
    process = subprocess.run(CMD_PREFIX + ['-Clc', str(c_ids[0]), '-c', str(c_ids[1])], **SUBPROCESS_KWARGS)
    assert 'id: {}'.format(c_ids[0]) in process.stdout
    assert 'id: {}'.format(c_ids[1]) in process.stdout


def test_list_some_conf_verbosely():
    c_ids = [add_conf_get_id(), add_conf_get_id(), add_conf_get_id()]
    process = subprocess.run(CMD_PREFIX + ['-vClc', str(c_ids[0]), '-c', str(c_ids[1])], **SUBPROCESS_KWARGS)
    for sign in ['"{}": "{}"'.format(*pair) for pair in SSR_CONF['dict'].items() if isinstance(pair[1], str)]:
        assert sign in process.stdout
    assert '"id": {}'.format(c_ids[0]) in process.stdout
    assert '"id": {}'.format(c_ids[1]) in process.stdout


def test_list_all_conf():
    c_ids = [add_conf_get_id(), add_conf_get_id(), add_conf_get_id()]
    process = subprocess.run(CMD_PREFIX + ['-Cl'], **SUBPROCESS_KWARGS)
    for c_id in c_ids:
        assert 'id: {}'.format(c_id) in process.stdout
    assert process.stdout.count('id: ') >= 2

    process = subprocess.run(CMD_PREFIX + ['-Cla'], **SUBPROCESS_KWARGS)
    for c_id in c_ids:
        assert 'id: {}'.format(c_id) in process.stdout
    assert process.stdout.count('id: ') >= 2


def test_edit_conf():
    pass  # TODO


def test_delete_conf():
    c_ids = [add_conf_get_id(), add_conf_get_id()]
    subprocess.run(CMD_PREFIX + ['-Cdc', str(c_ids[0]), '-c', str(c_ids[1])], **SUBPROCESS_KWARGS)
    query_result = db.cursor().execute(
        "SELECT COUNT(id) FROM ssrconf WHERE id = {} OR id = {}".format(*c_ids)).fetchone()
    assert query_result[0] == 0


def test_delete_all_conf():
    add_conf_get_id()
    subprocess.run(CMD_PREFIX + ['-Cda'], **SUBPROCESS_KWARGS)
    query_result = db.cursor().execute("SELECT COUNT(id) FROM ssrconf").fetchone()
    assert query_result[0] == 0


def test_delete_conf_without_info():
    c_id = add_conf_get_id()
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(CMD_PREFIX + ['-Cd'], **SUBPROCESS_KWARGS)
    query_result = db.cursor().execute(
        "SELECT COUNT(id) FROM ssrconf WHERE id = {}".format(c_id)).fetchone()
    assert query_result[0] == 1


def test_use_conf():
    c_id = add_conf_get_id()
    subprocess.run(CMD_PREFIX + ['-Csc', str(c_id)], **SUBPROCESS_KWARGS)
    config_dict = SSR_CONF['config_dict'].copy()
    config_dict['_meta']['id'] = c_id
    with open(config.SSR_CONF_PATH, 'r') as file:
        assert json.load(file) == {**config_dict, **config.SSR_CONF_EXTRA_FIELDS}


def test_list_current_conf():
    c_id = add_conf_get_id()
    subprocess.run(CMD_PREFIX + ['-Csc', str(c_id)], **SUBPROCESS_KWARGS)
    process = subprocess.run(CMD_PREFIX + ['-Clar'], **SUBPROCESS_KWARGS)
    assert 'Current:' in process.stdout
    assert '"id": {}'.format(c_id) in process.stdout
