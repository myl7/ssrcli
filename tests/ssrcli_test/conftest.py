import shutil

import pytest


@pytest.fixture(scope='session', autouse=True)
def clean_test_files():
    yield None
    shutil.rmtree('ssrcli', ignore_errors=True)
