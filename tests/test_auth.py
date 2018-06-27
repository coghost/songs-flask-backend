#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lihe <imanux@sina.com>'
__date__ = '2018/6/25 4:29 PM'
__description__ = '''
https://github.com/miguelgrinberg/REST-auth
'''

import os
import sys
import json
import base64

app_root = '/'.join(os.path.abspath(__file__).split('/')[:-2])
sys.path.append(app_root)

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from faker import Faker
from logzero import logger as log
from izen import helper
# 禁用安全请求警告
from iutils import parse_firefox_cookie_file

from http import cookiejar

requests.packages.urllib3.disable_warnings()
fake = Faker()
sess = requests.session()

uri = 'https://127.0.0.1/{}'
urls = {
    'users': 'users',
    'login': 'login',
    'token': 'api/token',
    'resource': 'api/resource',
}

urls = {
    k: uri.format(v) for k, v in urls.items()
}

headers = parse_firefox_cookie_file()
headers = {}


def dump_cookies(cookies, dst='cookie.txt'):
    _cookie_jar = cookiejar.LWPCookieJar(dst)
    requests.utils.cookiejar_from_dict({
        c.name: c.value
        for c in cookies
    }, _cookie_jar)
    _cookie_jar.save(dst, ignore_discard=True, ignore_expires=True)


def load_cookies(cookie_src_pth='cookie.txt'):
    if not helper.is_file_ok(cookie_src_pth):
        return
    _cookie_jar = cookiejar.LWPCookieJar(cookie_src_pth)
    _cookie_jar.load(cookie_src_pth, ignore_expires=True, ignore_discard=True)
    _cookies = requests.utils.dict_from_cookiejar(_cookie_jar)
    cookies = requests.utils.cookiejar_from_dict(_cookies)
    return cookies


def post_it(d):
    res = sess.post(urls.get('users'), data=d, verify=False)
    return res


def get_it_by_basic_auth(url, **kwargs):
    log.debug('Try {}'.format(url))
    #     res = sess.get(url, verify=False, headers=headers, **kwargs)
    res = sess.get(
        url, auth=HTTPBasicAuth('roberts', '123456'), verify=False, **kwargs
        # url, auth=('roberts', '123456'), verify=False, **kwargs # 简写形式
    )
    print(res.headers)
    return res


def get_it_by_auth(url):
    """
    直接使用 原生支持的 auth方式
    :param url:
    :type url:
    :return:
    :rtype:
    """
    log.debug('Try {}'.format(url))
    sess.auth = ('roberts', '123456')
    res = sess.get(url, verify=False)
    print(sess.headers)
    return res


def get_it_by_b64(url):
    """通过在 headers添加base64编码的数据实现
    :param url:
    :type url:
    :return:
    :rtype:
    """
    log.debug('Try {}'.format(url))
    tkn = b'roberts:123456'
    tkn = helper.to_str(base64.b64encode(tkn))
    sess.headers['Authorization'] = 'Basic {}'.format(tkn)
    res = sess.get(url, verify=False)
    return res


def get_by_token(url):
    # tk = 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzMDAwNTUwMSwiZXhwIjoxNTMwMDA2MTAxfQ.eyJpZCI6M30.iQ9YNhQevJcoiUEOXVBtd3iugCuQenjeq0XNR7b7lKI'
    tk = 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzMDAwNjUzNCwiZXhwIjoxNTMwMDA3MTM0fQ.eyJpZCI6M30.4YxKHUjrjG_BSqJSNrrhc3-GhpjiPF4M71IlhtxknuA'
    log.debug('Try {}'.format(url))
    res = sess.get(
        url, auth=HTTPBasicAuth(tk, 'anything'), verify=False,
    )
    return res


def gen_fak_user():
    d = {}
    for i in range(1):
        name = fake.name()
        if '.' in name:
            continue
        name = name.replace(' ', '_').lower()
        print(name)
        d['username'] = name
        post_it(d)


def get_users():
    rs = sess.get(urls.get('users'), verify=False)
    print(rs.content)


def run():
    print(urls)
    # res = get_it_by_b64(urls.get('token'))
    # res = get_it_by_auth(urls.get('token'))
    res = get_by_token(urls.get('token'))
    print(res.content)


if __name__ == '__main__':
    # print(headers)
    run()
