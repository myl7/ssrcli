import json
import subprocess
import pathlib
import shutil
from time import sleep

import pytest

from .shared import CMD_PREFIX, SUBPROCESS_KWARGS, SSR_CONF
from ssrcli.config import config


@pytest.mark.first
def test_install_and_test_ssr():
    # Prepare config
    with open(config.SSR_CONF_PATH, 'w') as f:
        json.dump({**SSR_CONF['config_dict'], **config.SSR_CONF_EXTRA_FIELDS}, f)

    # Install
    shutil.rmtree(config.SSR_APP_PATH, ignore_errors=True)
    subprocess.run(CMD_PREFIX + ['--install'], **SUBPROCESS_KWARGS)
    assert pathlib.Path(config.SSR_APP_PATH).is_dir()
    assert (pathlib.Path(config.SSR_APP_PATH) / '.git').is_dir()

    # Test
    process = subprocess.run(CMD_PREFIX + ['--test'], **SUBPROCESS_KWARGS)
    assert '' == process.stdout
    with open(pathlib.Path(config.SSR_APP_PATH) / 'shadowsocks' / 'local.py', 'w'):
        pass
    process = subprocess.run(CMD_PREFIX + ['--test'], **SUBPROCESS_KWARGS)
    assert 'Found {} MD5 different'.format(
        pathlib.Path(config.SSR_APP_PATH) / 'shadowsocks' / 'local.py') in process.stdout
    subprocess.run(['git', 'checkout', '.'], **SUBPROCESS_KWARGS, cwd=config.SSR_APP_PATH)
    process = subprocess.run(CMD_PREFIX + ['--test'], **SUBPROCESS_KWARGS)
    assert '' == process.stdout


@pytest.mark.last
def test_remove_ssr():
    subprocess.run(CMD_PREFIX + ['--remove'], **SUBPROCESS_KWARGS)
    assert not pathlib.Path(config.SSR_APP_PATH).is_dir()


def _test_ssr_status(status: bool):
    task = subprocess.run(CMD_PREFIX + ['-T'], **SUBPROCESS_KWARGS)
    assert 'on' if status else 'off' in task.stdout


@pytest.mark.second
def test_on_off_restart_status_ssr_with_multi():
    # On, off and restart
    _test_ssr_status(False)
    subprocess.run(CMD_PREFIX + ['-O'], **SUBPROCESS_KWARGS)
    sleep(0.1)
    _test_ssr_status(True)
    subprocess.run(CMD_PREFIX + ['-F'], **SUBPROCESS_KWARGS)
    sleep(0.1)
    _test_ssr_status(False)
    subprocess.run(CMD_PREFIX + ['-R'], **SUBPROCESS_KWARGS)
    sleep(0.1)
    _test_ssr_status(True)
    subprocess.run(CMD_PREFIX + ['-R'], **SUBPROCESS_KWARGS)
    sleep(0.1)
    _test_ssr_status(True)
    subprocess.run(CMD_PREFIX + ['-R'], **SUBPROCESS_KWARGS)
    _test_ssr_status(True)
    subprocess.run(CMD_PREFIX + ['-F'], **SUBPROCESS_KWARGS)

    # Multi ops should be handled
    _test_ssr_status(False)
    subprocess.run(CMD_PREFIX + ['-O'], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-O'], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-O'], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-O'], **SUBPROCESS_KWARGS)
    _test_ssr_status(True)
    subprocess.run(CMD_PREFIX + ['-F'], **SUBPROCESS_KWARGS)
    _test_ssr_status(False)

    subprocess.run(CMD_PREFIX + ['-O'], **SUBPROCESS_KWARGS)
    _test_ssr_status(True)
    subprocess.run(CMD_PREFIX + ['-F'], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-F'], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-F'], **SUBPROCESS_KWARGS)
    subprocess.run(CMD_PREFIX + ['-F'], **SUBPROCESS_KWARGS)
    _test_ssr_status(False)
    subprocess.run(CMD_PREFIX + ['-O'], **SUBPROCESS_KWARGS)
    _test_ssr_status(True)
