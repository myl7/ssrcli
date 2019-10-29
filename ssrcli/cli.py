import argparse
import json
from typing import Dict

from .config import config
from .managers import SsrConfManager, SsrSubManager, Param, SsrConf, SsrSub, from_ssr_url
from .exceptions import RequireMoreParam, InvalidParam, NoSuchOperation


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='ssrcli', description='SSR client: resource management tool',
                                     argument_default=argparse.SUPPRESS)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(config.VERSION))
    parser.add_argument('model', choices=['conf', 'sub'], help='choose which kind of resources to manage')
    parser.add_argument(
        'action', choices=['ls', 'add', 'rm', 'edit', 'take', 'update', 'get'], help='choose which action to take')
    # `get` is deprecated
    parser.add_argument('-a', '--all', action='store_true', help='work on all instances', default=False)
    parser.add_argument('-i', '--id', type=int, action='append', help='give instance id', dest='ins_id')
    parser.add_argument('-j', '--json', help='give instance json-format information', dest='ins_json')
    parser.add_argument('-u', '--url', help='give SSR sharing URL', dest='ssr_url')
    parser.add_argument('-c', '--current', action='store_true', default=False,
                        help='show currently-used configuration for SSR')
    parser.add_argument('-V', '--verbose', action='store_true', default=False,
                        help='show more information of the instances')
    return parser


def take_action(param_dict: Dict[str, Param]) -> None:
    try:
        model, manager = {
            'conf': (SsrConf, SsrConfManager()),
            'sub': (SsrSub, SsrSubManager()),
        }[param_dict['model']]

        action = param_dict['action']
    except KeyError as error:
        raise RequireMoreParam(error.args[0])

    try:
        if action in ['ls', 'get']:  # `get` is deprecated
            if action == 'get':
                print('`get` is deprecated! Use `ls` as it can work the same as `get`')
            id_list = param_dict.get('ins_id', None) if param_dict['all'] else None
            if not (id_list is None and not param_dict['all'] and param_dict['current']):
                for info in manager.list(id_list, verbose=param_dict['verbose']):
                    print(info)
            if param_dict['current']:
                print('\nCurrently-used configuration is:')
                print(manager.load_use())

        elif action == 'add':
            if model == SsrConf:
                if 'ssr_url' in param_dict.keys():
                    json_info = from_ssr_url(param_dict['ssr_url'])
                else:
                    try:
                        json_info = json.loads(param_dict['ins_json'])
                    except ValueError:
                        raise InvalidParam('ins_json')
                print(manager.create(**json_info))

            elif model == SsrSub:
                try:
                    json_info = json.loads(param_dict['ins_json'])
                except ValueError:
                    raise InvalidParam('ins_json')
                print(manager.create(**json_info))

            else:
                raise RuntimeError()

        elif action == 'rm':
            if param_dict['all']:
                id_list = None
            else:
                id_list = param_dict['ins_id']
            manager.delete(id_list)

        elif action == 'edit':
            raise NotImplementedError()  # TODO(myl7)

        elif action == 'take':
            if model != SsrConf:
                raise NoSuchOperation('take')
            manager.take_use(param_dict['ins_id'].pop())

        elif action == 'update':
            if model != SsrSub:
                raise NoSuchOperation('update')
            id_list = param_dict.get('ins_id', None) if param_dict['all'] else None
            manager.update(id_list)

        else:
            raise RuntimeError()
    except KeyError as error:
        raise RequireMoreParam(error.args[0])


if __name__ == '__main__':
    arg_parser = create_parser()
    arg_param_dict = vars(arg_parser.parse_args())
    take_action(arg_param_dict)
