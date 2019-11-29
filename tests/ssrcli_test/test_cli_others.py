import subprocess

from .shared import CMD_PREFIX, SUBPROCESS_KWARGS
from ssrcli import __version__


def test_version():
    process = subprocess.run(CMD_PREFIX + ['-V'], **SUBPROCESS_KWARGS)
    assert 'ssrcli {}'.format(__version__) in process.stdout
