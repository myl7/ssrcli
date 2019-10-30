import argparse
from typing import List, Optional

from .config import config
from .controllers import AppCliController


class AppCli:
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        self.parser = argparse.ArgumentParser(prog='ssrcli', argument_default=argparse.SUPPRESS,
                                              description='SSR client management tool with command line interface')
        self.parser.add_argument('-V', '--version', action='version', version='%(prog) {}'.format(config.VERSION))
        self.parser.add_argument('-v', '--verbose', action='store_true', default=False,
                                 help='show verbose information')
        self.parser.add_argument('-q', '--quiet', action='store_true', default=False,
                                 help='show concise information')  # TODO(myl7)
        subparsers = self.parser.add_subparsers(dest='model',
                                                help='manage certain model. Add "-h" to show sub-command help.')
        self._build_conf(subparsers)
        self._build_sub(subparsers)

    def _build_conf(self, subparsers):
        conf_parser: argparse.ArgumentParser = subparsers.add_parser('conf', argument_default=argparse.SUPPRESS,
                                                                     help='configuration management')
        conf_parser.add_argument('action', choices=['l', 'a', 'd', 'e', 's'],
                                 help='choose an action: l -> list, a -> add, d -> delete, e -> edit, s -> use')
        conf_parser.add_argument('-a', '--all', action='store_true', default=False,
                                 help='perform on all configurations')
        conf_parser.add_argument('-c', '--choose', type=int, action='append', dest='c_id_list',
                                 help='give configuration id (allow multi id)')
        conf_parser.add_argument('-U', '--url', help='give SSR share url')
        conf_parser.add_argument('-r', '--current', action='store_true', default=False,
                                 help='include currently used configuration')
        conf_parser.add_argument('-j', '--json', type=str, help='input required information with json')

    def _build_sub(self, subparsers):
        sub_parser: argparse.ArgumentParser = subparsers.add_parser('sub', argument_default=argparse.SUPPRESS,
                                                                    help='subscription management')
        sub_parser.add_argument('action', choices=['l', 'a', 'd', 'e', 'u'],
                                help='choose an action: l -> list, a -> add, d -> delete, e -> edit, u -> update')
        sub_parser.add_argument('-a', '--all', action='store_true', default=False,
                                help='perform on all subscriptions')
        sub_parser.add_argument('-c', '--choose', type=int, action='append', dest='c_id_list',
                                help='give subscription id (allow multi id)')
        sub_parser.add_argument('-j', '--json', type=str, help='input required information with json')

    def parse(self, arg_list: Optional[List[str]] = None) -> dict:
        arg_obj = self.parser.parse_args(arg_list)
        return vars(arg_obj)


def main():
    app_cli = AppCli()
    app_controller = AppCliController()
    'DEBUG'; print(app_cli.parse())
    app_controller.run(app_cli.parse())


if __name__ == '__main__':
    main()
