import json

from . import managers
from . import exceptions
from .ssr import SsrApp


class AppController:
    def run(self, arg_dict: dict):
        if arg_dict['conf']:
            self._run_with_conf(arg_dict)

        elif arg_dict['sub']:
            self._run_with_sub(arg_dict)

        elif arg_dict['status']:
            print('SSR: {}'.format('on' if SsrApp().status() else 'off'))

        else:
            for k in ['install', 'remove', 'test', 'on', 'off', 'restart']:
                if arg_dict[k]:
                    getattr(SsrApp(), k)()
                    return

            raise exceptions.RequireMoreArgument(arg='target')

    def _run_with_conf(self, arg_dict: dict):
        manager = managers.SsrConfManager()

        action = None
        for k in ['ls', 'new', 'del', 'edit', 'use']:
            if arg_dict[k]:
                action = k
                break
        if not action:
            raise exceptions.RequireMoreArgument(arg='action')

        if action == 'ls':
            ids = None if arg_dict['all'] else arg_dict.get('ids', None)
            for model in manager.list(ids, verbose=arg_dict['verbose']):
                print(model)
            if arg_dict['current']:
                print('')
                print('Current:')
                print(manager.current())

        elif action == 'new':
            if arg_dict['url']:
                dict_info = managers.ssr_url_to_dict(arg_dict['url'])
            else:
                try:
                    dict_info = json.loads(arg_dict['json'])
                except json.JSONDecodeError:
                    raise exceptions.InvalidArgument(arg='json')
            print(manager.create(**dict_info))

        elif action == 'del':
            if arg_dict['ids'] or arg_dict['all']:
                manager.delete(arg_dict['ids'])
            else:
                raise exceptions.RequireMoreArgument(arg='ids')

        elif action == 'edit':
            raise NotImplementedError()  # TODO(myl7)

        elif action == 'use':
            if arg_dict['ids']:
                manager.use(arg_dict['ids'][0])
            else:
                raise exceptions.RequireMoreArgument(arg='ids')

    def _run_with_sub(self, arg_dict: dict):
        manager = managers.SsrSubManager()

        action = None
        for k in ['ls', 'new', 'del', 'edit', 'update']:
            if arg_dict[k]:
                action = k
                break
        if not action:
            raise exceptions.RequireMoreArgument(arg='action')

        if action == 'ls':
            ids = None if arg_dict['all'] else arg_dict.get('ids', None)
            for model in manager.list(ids, verbose=arg_dict['verbose']):
                print(model)

        elif action == 'new':
            try:
                dict_info = json.loads(arg_dict['json'])
            except json.JSONDecodeError:
                raise exceptions.InvalidArgument(arg='json')
            print(manager.create(**dict_info))

        elif action == 'del':
            if arg_dict['ids'] or arg_dict['all']:
                manager.delete(arg_dict['ids'])
            else:
                raise exceptions.RequireMoreArgument(arg='ids')

        elif action == 'edit':
            raise NotImplementedError()  # TODO(myl7)

        elif action == 'update':
            ids = None if arg_dict['all'] else arg_dict.get('ids', None)
            try:
                proxies = json.loads(arg_dict['proxies']) if arg_dict['proxies'] else None
            except json.JSONDecodeError:
                raise exceptions.InvalidArgument(arg='proxies')
            manager.update(ids, proxies)
