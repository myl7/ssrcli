import json

from . import managers
from . import exceptions


class AppCliController:
    def run(self, arg_dict: dict):
        try:
            manager = {'conf': managers.SsrConfManager, 'sub': managers.SsrSubManager}[arg_dict['model']]()

            if arg_dict['action'] == 'l':
                c_id_list = None if arg_dict['all'] else arg_dict.get('c_id_list', None)
                for model in manager.list(c_id_list, verbose=arg_dict['verbose']):
                    print(model)
                if arg_dict['current']:
                    print('\nCurrent:')
                    print(manager.current())

            elif arg_dict['action'] == 'a':
                if arg_dict['model'] == 'conf' and 'ssr_url' in arg_dict.keys():
                    json_info = managers.ssr_url_to_dict(arg_dict['url'])
                else:
                    try:
                        json_info = json.loads(arg_dict['json'])
                    except json.JSONDecodeError:
                        raise exceptions.InvalidArgument(arg='json')
                print(manager.create(**json_info))

            elif arg_dict['action'] == 'd':
                print()
                manager.delete(None if arg_dict['all'] else arg_dict['c_id_list'])

            elif arg_dict['action'] == 'e':
                raise NotImplementedError()  # TODO(myl7)

            elif arg_dict['model'] == 'conf' and arg_dict['action'] == 's':
                manager.use(arg_dict['c_id_list'][0])

            elif arg_dict['model'] == 'sub' and arg_dict['action'] == 'u':
                c_id_list = None if arg_dict['all'] else arg_dict.get('c_id_list', None)
                manager.update(c_id_list)

            else:
                raise exceptions.NoSuchOperation(model=arg_dict['model'], action=arg_dict['action'])
        except (KeyError, IndexError) as error:
            raise exceptions.RequireMoreArgument(key=error.args[0])
