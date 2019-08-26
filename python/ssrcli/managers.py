import base64
import json
import asyncio
from typing import Iterator, Type, Union, Tuple, Optional, Dict, Iterable, List

import requests

from .config import config
from .models import SsrConf, SsrSub
from .exceptions import SsrcliException, SsrUrlInvalid, RequireMoreParam, InvalidParam, NoSuchOperation

Models = Union[SsrConf, SsrSub]
Param = Union[str, List[int]]
UpdateResult = Tuple[Iterator[Dict[str, str]], Optional[int]]


class B64DecodeSsrException(SsrcliException):
    pass


def b64_decode_ssr(e_str: str) -> str:
    """add '=' at tail automatically to perform base64 decoding"""
    remainder = len(e_str) % 4
    if remainder == 2:
        e_str += '=='
    elif remainder == 3:
        e_str += '='
    elif remainder == 0:
        pass
    else:
        raise B64DecodeSsrException()
    return base64.urlsafe_b64decode(e_str.encode('utf-8')).decode('utf-8')


def b64_encode_ssr(r_str: str) -> str:
    """After base64 decoding, remove '=' at tail"""
    return base64.urlsafe_b64encode(r_str.encode('utf-8')).decode('utf-8').replace('=', '')


def to_ssr_url(ssr_conf: SsrConf) -> str:
    info = {
        'server': ssr_conf.server,
        'server_port': ssr_conf.server_port,
        'protocol': ssr_conf.protocol,
        'method': ssr_conf.method,
        'obfs': ssr_conf.obfs,
        'password': b64_encode_ssr(ssr_conf.password),
        'obfs_param': b64_encode_ssr(ssr_conf.obfs_param),
        'protocol_param': b64_encode_ssr(ssr_conf.protocol_param),
        'remarks': b64_encode_ssr(ssr_conf.remarks),
        'group': b64_encode_ssr(ssr_conf.group),
    }
    return 'ssr://' + b64_encode_ssr((
        '{server}:{server_port}:{protocol}:{method}:{obfs}:{password}/?'
        'obfsparam={obfs_param}&protoparam={protocol_param}&remarks={remarks}&group={group}'
    ).format(**info))


def from_ssr_url(ssr_url: str) -> Dict[str, str]:
    if ssr_url[:6] != 'ssr://':
        raise SsrUrlInvalid()
    info_list = b64_decode_ssr(ssr_url[6:]).split(':')
    try:
        info = {
            'server': ':'.join(info_list[:-5]),  # When comes to IPv6, ':' will be in it
            'server_port': int(info_list[-5]),
            'protocol': info_list[-4],
            'method': info_list[-3],
            'obfs': info_list[-2],
            'password': b64_decode_ssr(info_list[-1].split('/?')[0]),
        }
        info_list = info_list[-1].strip().split('/?')[1].split('&')
        info = {
            **info,
            'obfs_param': b64_decode_ssr(info_list[0][len('obfsparam='):]),
            'protocol_param': b64_decode_ssr(info_list[1][len('protoparam='):]),
            'remarks': b64_decode_ssr(info_list[2][len('remarks='):]),
            'group': b64_decode_ssr(info_list[3][len('group='):]),
        }
    except (IndexError, B64DecodeSsrException):
        raise SsrUrlInvalid()
    return info


def conf_to_json(conf: SsrConf) -> Dict[str, Union[str, int]]:
    return {
        'server': conf.server,
        'server_port': conf.server_port,
        'protocol': conf.protocol,
        'method': conf.method,
        'obfs': conf.obfs,
        'password': conf.password,
        'obfs_param': conf.obfs_param,
        'protocol_param': conf.protocol_param,
    }


class Manager:
    """
    Map the manager class to a model class for db

    Overwrite this field in subclass to set to existing model class for db
    """
    model = None  # type: Type[Models]

    def list(self, id_list: Optional[List[int]]) -> Iterable[Models]:
        if id_list:
            return self.model.select().where(self.model.id.in_(id_list))
        else:
            return self.model.select()

    def create(self, **kwargs: Param) -> Models:
        return self.model.create(**kwargs)

    def delete(self, pk: int) -> None:
        instance = self.model.get(pk)
        instance.delete_instance()

    def edit(self, pk: int, **kwargs: Param) -> None:
        instance = self.model.get(pk)
        for field, value in kwargs.items():
            setattr(instance, field, value)
        instance.save()


class SsrConfManager(Manager):
    model = SsrConf

    def take_use(self, pk: int) -> None:
        instance = self.model.get(pk)
        json_config = {**conf_to_json(instance), **config.SSR_CONF_EXTRA_FIELDS}
        with open(config.SSR_CONF_PATH, 'w') as file:
            file.write(json.dumps(json_config, indent=2, ensure_ascii=False))


async def _update_sub(url: str, pk: Optional[int] = None) -> UpdateResult:
    content = requests.get(url).content.decode('utf-8').strip()
    ssr_urls = b64_decode_ssr(content).splitlines()
    return map(from_ssr_url, ssr_urls), pk


class SsrSubManager(Manager):
    model = SsrSub

    @staticmethod
    def _update_result(result: UpdateResult, instance: SsrSub) -> None:
        for conf in instance.ssrconf_set:
            conf.delete_instance()
        for info in result[0]:
            SsrConf.create(**info, sub=instance)

    def update_one(self, pk: int) -> None:
        instance = SsrSub.get(pk)
        task = _update_sub(instance.url)
        result = asyncio.get_event_loop().run_until_complete(task)
        self._update_result(result, instance)

    def update_all(self) -> None:
        instances = [ins for ins in SsrSub.select().order_by(SsrSub.id.desc())]
        tasks = [_update_sub(ins.url, ins.id) for ins in instances]
        results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        for result in results:
            self._update_result(result, instances[result[1] - 1])


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
            for ins in manager.list(param_dict.get('ins_id', None)):
                print(ins)

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
            manager.delete(param_dict['ins_id'])

        elif action == 'edit':
            raise NotImplementedError()  # TODO(myl7)

        elif action == 'take':
            if model != SsrConf:
                raise NoSuchOperation('take')
            manager.take_use(param_dict['ins_id'].pop())

        elif action == 'update':
            if model != SsrSub:
                raise NoSuchOperation('update')
            manager.update(param_dict.get('ins_id', None))

        else:
            raise RuntimeError()
    except KeyError as error:
        raise RequireMoreParam(error.args[0])
