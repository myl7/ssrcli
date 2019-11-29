import os
import subprocess
import shutil
import glob
import hashlib
import pathlib

import xdg

from .config import config
from .managers import SsrConfManager


class SsrApp:
    SSR_FILE_MD5 = {
        'obfsplugin/verify.py': '4769b5a8e3e6012a5da57533ce2c62b8',
        'obfsplugin/__init__.py': '7ff9a30b272bb2077d229a3d0b12c86a',
        'obfsplugin/auth.py': '5d79f3fbd42e71493232294662663359',
        'obfsplugin/auth_chain.py': '6eaef7733d3515809125101be6147cbc',
        'obfsplugin/plain.py': '95dffa5a32514458158c03f1ce657e94',
        'obfsplugin/obfs_tls.py': '513c28c82d76c99e3c4e119b5bcae1af',
        'obfsplugin/http_simple.py': '1abc81ce2d14da585d9f3eb17a4f4956',
        'crypto/rc4_md5.py': '5e70a54986295913974ba6d60b5b7bb5',
        'crypto/openssl.py': '5e786a490e3adfb13f33d5bc3ed9c998',
        'crypto/ctypes_libsodium.py': '1a957242cad3346e2e0d7251b62b2a7b',
        'crypto/__init__.py': '7ff9a30b272bb2077d229a3d0b12c86a',
        'crypto/sodium.py': 'a3a773b4ec49373f0028d32560f408a9',
        'crypto/util.py': 'd6a806fc2e11ff8f7f0667b91f8a6f58',
        'crypto/table.py': '751169759aa43e84602118ca7957047e',
        'crypto/ctypes_openssl.py': '112cda4dffac340142d7a894ee5d9232',
        'run.sh': '87d802870a57a56749b84aee7d01bdc7',
        'common.py': '41572dc942869db57b1e431f4951764e',
        'encrypt.py': '97b6271a61593d99a051afeee6ba8202',
        'manager.py': 'db54e7a547dd5a653ce651b271f2e68e',
        '__init__.py': '9b4f7d2f38afb96b0708d303262e07fd',
        'asyncdns.py': '1f42746074acc7ff7638b60bcd06e0ab',
        'version.py': '1fe5c2894450886a02caff9aaa10f4c2',
        'encrypt_test.py': 'f0001a6d92ba6dc0b731801db2b98530',
        'eventloop.py': 'ee6e1f2a6341d0649dbfbc898dbef2ca',
        'daemon.py': '4b1ca6c81201ca582478acc223ebeab8',
        'tcprelay.py': '0adfeb81724b5f1b6f415ccdcd1b4f34',
        'obfs.py': '2764716a6e6f132d978445bbb85da184',
        'lru_cache.py': 'e8cfd8b1494df5999c9e3f25d39d0a7c',
        'local.py': 'a51c10ba21606910371e20dfd739eea4',
        'shell.py': '5c3973dff66a33de5c567909fa0a1eaf',
        'server.py': 'ef90038f209ec504cd42780d9eb16866',
        'ordereddict.py': '397c5dee3496749e0c692d9c43d3c698',
        'udprelay.py': 'a2c5ecccbcf2cee90c4e007774787eaf',
        'tail.sh': '78abecdddc0f388111026f36e23c1068',
        'stop.sh': '439363b356eecad5eda5574535b7f32c',
        'logrun.sh': '34d0334cd13b07a54436c0ec6cf6d823',
    }

    def __init__(self):
        self.config_path = config.SSR_CONF_PATH

    @staticmethod
    def install():
        if pathlib.Path(config.SSR_APP_PATH).exists():
            print('The target folder already exists: {}'.format(config.SSR_APP_PATH))
            return
        try:
            subprocess.run(['git', 'clone', 'https://github.com/shadowsocksr-backup/shadowsocksr', '-b', 'manyuser',
                            '--depth=1', config.SSR_APP_PATH], check=True)
        except subprocess.CalledProcessError:
            print('Running git clone failed. Have you installed git?')

    @staticmethod
    def remove():
        shutil.rmtree(config.SSR_APP_PATH, ignore_errors=True)

    @staticmethod
    def test() -> bool:
        files = glob.glob(os.path.join(config.SSR_APP_PATH, 'shadowsocks', '**', '*'), recursive=True)
        ok: bool = True
        for file in files:
            key = file[len(os.path.join(config.SSR_APP_PATH, 'shadowsocks')) + 1:]
            if key in SsrApp.SSR_FILE_MD5.keys():
                hash_md5 = hashlib.md5()
                with open(file, "rb") as f:  # TODO: Move to utils
                    for chunk in iter(lambda: f.read(4096), b''):
                        hash_md5.update(chunk)
                res = hash_md5.hexdigest()
                if res != SsrApp.SSR_FILE_MD5[key]:
                    print('Found {} MD5 different'.format(file))
                    ok = False
        return ok

    def on(self):
        if self.status():
            print('SSR has been launched')
            return
        print(SsrConfManager().current())
        task = subprocess.Popen(['python', '-m', 'shadowsocks.local', '-c', self.config_path, 'start'],
                                cwd=config.SSR_APP_PATH)  # shadowsocksr has no deps so being without env=... is OK
        with open(xdg.XDG_DATA_HOME / 'ssrcli' / 'ssr.pid', 'w') as f:
            print(task.pid, file=f)

    def off(self):
        if not self.status():
            print('SSR has already been off')
            return
        with open(xdg.XDG_DATA_HOME / 'ssrcli' / 'ssr.pid', 'r') as f:
            content = f.read().strip()
        if content.isdigit():
            pid = int(content)
            try:
                subprocess.run(['kill', str(pid)], check=True)
            except subprocess.CalledProcessError:
                print('Running kill failed: pid {}'.format(pid))
                return
            with open(xdg.XDG_DATA_HOME / 'ssrcli' / 'ssr.pid', 'w'):
                pass
        else:
            print('Invalid pid file: {}'.format(xdg.XDG_DATA_HOME / 'ssrcli' / 'ssr.pid'))

    def restart(self):
        self.off()
        self.on()

    def status(self) -> bool:
        try:
            subprocess.run(['lsof', '-i:{}'.format(config.SSR_LOCAL_PORT)], check=True, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            return False
        return True
