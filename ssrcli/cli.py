import argparse
from typing import List, Optional

from .config import config
from .controllers import AppController


class AppCli:
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        self.parser = argparse.ArgumentParser(prog='ssrcli', description='SSR client with shell interface')
        self.parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(config.VERSION))
        self.parser.add_argument('-v', '--verbose', action='store_true', help='show verbose information')
        self.parser.add_argument('-q', '--quiet', action='store_true', help='show concise information')  # TODO

        self.parser.add_argument('--install', action='store_true', help='install SSR')
        self.parser.add_argument('--remove', action='store_true', help='remove SSR')
        self.parser.add_argument('--test', action='store_true', help='test SSR integrity')
        self.parser.add_argument('-O', '--on', action='store_true', help='start SSR')
        self.parser.add_argument('-F', '--off', action='store_true', help='stop SSR')
        self.parser.add_argument('-R', '--restart', action='store_true', help='restart SSR')
        self.parser.add_argument('-T', '--status', action='store_true', help='check SSR status')

        self.parser.add_argument('-C', '--conf', action='store_true', help='manage SSR configuration')
        self.parser.add_argument('-S', '--sub', action='store_true', help='manage SSR subscription')

        self.parser.add_argument('-l', '--ls', action='store_true', help='list one or some')
        self.parser.add_argument('-n', '--new', action='store_true', help='add new one')
        self.parser.add_argument('-d', '--del', action='store_true', help='delete one or some')
        self.parser.add_argument('-e', '--edit', action='store_true', help='edit existed one')
        self.parser.add_argument('-s', '--use', action='store_true', help='use a SSR configuration')
        self.parser.add_argument('-u', '--update', action='store_true', help='update SSR subscription')

        self.parser.add_argument('-a', '--all', action='store_true', help='do to all')
        self.parser.add_argument('-c', '--ids', action='append', type=int, help='choose ids')
        self.parser.add_argument('-r', '--current', action='store_true', help='show current configuration')
        self.parser.add_argument('-p', '--proxies', help='used json-format requests-like proxies to update')
        self.parser.add_argument('-w', '--url', help='give SSR share url')
        self.parser.add_argument('-j', '--json', help='give json-format information')
        self.parser.add_argument('-f', '--file', help='give file path')

    def parse(self, arg_list: Optional[List[str]] = None) -> dict:
        arg_obj = self.parser.parse_args(arg_list)
        return vars(arg_obj)


def main():
    app_cli = AppCli()
    app_controller = AppController()
    app_controller.run(app_cli.parse())


if __name__ == '__main__':
    main()
