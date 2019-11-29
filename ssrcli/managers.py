import json
import asyncio
from typing import Optional, Iterable, List, AnyStr, Dict, Union

import requests
from requests.adapters import HTTPAdapter
import peewee

from .config import config
from . import models
from .utils import ssr_url_to_dict, conf_to_json, b64_decode_ssr


class Manager:
    """
    For below code
    Map the manager class to a model class for db

    Overwrite this field in subclass to set the existing model class for db
    """
    model = None  # type: peewee.Model

    def list(self, c_id_list: Optional[List[int]], verbose: bool = False) -> Iterable[AnyStr]:
        if c_id_list is None:
            return self.model.select()
        else:
            return self.model.select().where(self.model.id.in_(c_id_list))

    def create(self, **kwargs) -> peewee.Model:
        return self.model.create(**kwargs)

    def delete(self, c_id_list: Optional[List[int]]) -> None:
        if c_id_list is None:
            query = self.model.select()
        else:
            query = self.model.select().where(self.model.id.in_(c_id_list))
        for ins in query:
            ins.delete_instance()

    def edit(self, c_id: int, **kwargs) -> None:
        instance = self.model.get(c_id)
        for field, value in kwargs.items():
            setattr(instance, field, value)
        instance.save()


class SsrConfManager(Manager):
    model = models.SsrConf

    def list(self, c_id_list: Optional[List[int]], verbose: bool = False) -> Iterable[AnyStr]:
        if verbose:
            return map(lambda x: json.dumps(conf_to_json(x), indent=2, ensure_ascii=False), super().list(c_id_list))
        else:
            return super().list(c_id_list)

    def use(self, c_id: int) -> None:
        json_config = {**conf_to_json(self.model.get(c_id)), **config.SSR_CONF_EXTRA_FIELDS}
        with open(config.SSR_CONF_PATH, 'w') as file:
            file.write(json.dumps(json_config, indent=2))

    def share(self):  # TODO(myl7)
        pass

    @staticmethod
    def current() -> str:
        with open(config.SSR_CONF_PATH, 'r') as file:
            return json.dumps(json.load(file), indent=2, ensure_ascii=False)


async def _update_sub(url: str, c_id: Optional[int] = None, proxies: Optional[Union[bool, Dict[str, str]]] = None):
    proxies = proxies if proxies else None
    s = requests.Session()
    s.mount('http://stackoverflow.com', HTTPAdapter(max_retries=config.UPDATE_RETRY))
    content = s.get(url, proxies=proxies, timeout=config.UPDATE_TIMEOUT).content.decode('utf-8').strip()
    ssr_urls = b64_decode_ssr(content).splitlines()
    return map(ssr_url_to_dict, ssr_urls), c_id


class SsrSubManager(Manager):
    model = models.SsrSub

    def list(self, c_id_list: Optional[List[int]], verbose: bool = False) -> Iterable[AnyStr]:
        if verbose:
            if c_id_list is None:
                sub_query = models.SsrSub.select()
            else:
                sub_query = models.SsrSub.select().where(models.SsrSub.id.in_(c_id_list))
            conf_query = models.SsrConf.select()
            sub_with_conf = peewee.prefetch(sub_query, conf_query)
            # Print sub with all conf belong to it
            return map(lambda x: '[\n{}\n{}]'.format(x, '\n'.join(map(str, x.ssrconf_set))), sub_with_conf)
        else:
            return super().list(c_id_list)

    @staticmethod
    def _update_result(result, instance: models.SsrSub) -> None:
        for conf in instance.ssrconf_set:
            conf.delete_instance()
        for info in result[0]:
            models.SsrConf.create(**info, sub=instance)

    # TODO(myl7): There update func require refactoring
    def update(self, c_id_list: Optional[List[int]], proxies: Optional[Union[bool, Dict[str, str]]] = None) -> None:
        """Update selected sub

        :param c_id_list: Id of sub that will be updated
        :param proxies: None or {} to disable proxies, or dict with per-protocol proxy host url that will be sent to
            requests.get()
        :return: None
        """
        if c_id_list is None:
            instance_dict = {instance.id: instance for instance in models.SsrSub.select()}
        else:
            instance_dict = {
                instance.id: instance for instance in models.SsrSub.select().where(models.SsrSub.id.in_(c_id_list))
            }
        tasks = [_update_sub(instance.url, instance.id, proxies) for instance in instance_dict.values()]
        results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        for result in results:
            self._update_result(result, instance_dict[result[1]])
