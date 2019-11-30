import subprocess
import pathlib
import shutil
from time import sleep

import pytest

from .shared import CMD_PREFIX, SUBPROCESS_KWARGS, VENV_ENV
from ssrcli.config import config


@pytest.mark.first
def test_install_and_test_ssr():
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
    assert 'SSR: {}'.format('on' if status else 'off') == task.stdout.strip()


# As we use Popen to unblockedly run commands, we should sleep enough time to wait for SSR to make the action.
# 0.5s is OK on my laptop, and if failed on your device, set the below variable larger.
SLEEP_AFTER_POPEN = 0.5


@pytest.mark.second
def test_on_off_restart_status_ssr_with_multi():
    _test_ssr_status(False)
    subprocess.Popen(CMD_PREFIX + ['-O'], env=VENV_ENV)
    sleep(SLEEP_AFTER_POPEN)
    subprocess.Popen(CMD_PREFIX + ['-O'], env=VENV_ENV)
    _test_ssr_status(True)
    subprocess.Popen(CMD_PREFIX + ['-F'], env=VENV_ENV)
    sleep(SLEEP_AFTER_POPEN)
    subprocess.Popen(CMD_PREFIX + ['-F'], env=VENV_ENV)
    _test_ssr_status(False)
    subprocess.Popen(CMD_PREFIX + ['-R'], env=VENV_ENV)
    sleep(2 * SLEEP_AFTER_POPEN)  # As restart is simply a wrapper of off and then on
    _test_ssr_status(True)
    subprocess.Popen(CMD_PREFIX + ['-R'], env=VENV_ENV)
    sleep(2 * SLEEP_AFTER_POPEN)
    _test_ssr_status(True)
    subprocess.Popen(CMD_PREFIX + ['-F'], env=VENV_ENV)
    sleep(SLEEP_AFTER_POPEN)
    _test_ssr_status(False)
