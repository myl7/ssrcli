import base64

from . import models
from . import exceptions


class B64DecodeSsrException(exceptions.SsrcliException):
    pass


def b64_decode_ssr(e_str: str) -> str:
    """add "=" at tail automatically to perform base64 decoding"""
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
    """After base64 decoding, remove "=" at tail"""
    return base64.urlsafe_b64encode(r_str.encode('utf-8')).decode('utf-8').replace('=', '')


def conf_to_ssr_url(ssr_conf: models.SsrConf) -> str:
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
    return 'ssr://' + b64_encode_ssr(
        '{server}:{server_port}:{protocol}:{method}:{obfs}:{password}/?'
        'obfsparam={obfs_param}&protoparam={protocol_param}&remarks={remarks}&group={group}'.format(**info))


def ssr_url_to_dict(ssr_url: str) -> dict:
    if ssr_url[:6] != 'ssr://':
        raise exceptions.InvalidSsrUrl()
    info_list = b64_decode_ssr(ssr_url[6:]).split(':')
    try:
        info = {
            'server': ':'.join(info_list[:-5]),  # When comes to IPv6, ":" will be in it
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
        raise exceptions.InvalidSsrUrl()
    return info


def conf_to_json(conf: models.SsrConf):
    return {
        'server': conf.server,
        'server_port': conf.server_port,
        'protocol': conf.protocol,
        'method': conf.method,
        'obfs': conf.obfs,
        'password': conf.password,
        'obfs_param': conf.obfs_param,
        'protocol_param': conf.protocol_param,
        '_meta': {
            'id': conf.id,
            'remarks': conf.remarks,
            'group': conf.group,
            'sub': conf.sub_id if conf.sub_id else None,
        },
    }
