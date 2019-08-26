from .shared_variables import SSR_CONF

from ssrcli.managers import b64_encode_ssr, b64_decode_ssr, from_ssr_url, to_ssr_url, conf_to_json, SsrConf

B64_SSR_STR = {
    'r': ['testtest1', 'testtest12', 'testtest123'],
    'e': ['dGVzdHRlc3Qx', 'dGVzdHRlc3QxMg', 'dGVzdHRlc3QxMjM'],
}


def test_b64_encode_ssr():
    for i in range(3):
        assert b64_encode_ssr(B64_SSR_STR['r'][i]) == B64_SSR_STR['e'][i]


def test_b64_decode_ssr():
    for i in range(3):
        assert b64_decode_ssr(B64_SSR_STR['e'][i]) == B64_SSR_STR['r'][i]


def test_from_ssr_url():
    assert from_ssr_url(SSR_CONF['url']) == SSR_CONF['info']


def test_to_ssr_url():
    assert to_ssr_url(SsrConf(**SSR_CONF['info'])) == SSR_CONF['url']


def test_conf_to_json():
    temp_ssr_conf = SSR_CONF['json'].copy()
    temp_ssr_conf['_meta']['id'] = None  # As the instance has not been saved, it does not have id field
    assert conf_to_json(SsrConf(**SSR_CONF['info'])) == temp_ssr_conf
