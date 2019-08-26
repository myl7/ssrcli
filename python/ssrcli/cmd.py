import argparse

from .config import config
from .managers import take_action


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='ssrcli', description='SSR client: resource management tool',
                                     argument_default=argparse.SUPPRESS)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(config.VERSION))
    parser.add_argument('model', choices=['conf', 'sub'], help='choose which kind of resources to manage')
    parser.add_argument(
        'action', choices=['get', 'ls', 'add', 'rm', 'edit', 'take', 'update'], help='choose which action to take',
    )
    parser.add_argument('-i', '--id', type=int, help='give instance id', dest='ins_id')
    parser.add_argument('-j', '--json', help='give instance json-format information', dest='ins_json')
    parser.add_argument('-u', '--url', help='give SSR sharing URL', dest='ssr_url')
    return parser


if __name__ == '__main__':
    arg_parser = create_parser()
    param_dict = vars(arg_parser.parse_args())
    take_action(param_dict)
