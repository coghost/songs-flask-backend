__all__ = ['sfb_cfg']

from izen import chaos, helper
from iutils.sfb_cfg import cfg


# from iutils.mysql_db import db


def md5(plain):
    return chaos.Chaos().encrypt(plain, 'md5')


def parse_firefox_cookie_file(fpth='ffck.txt'):
    cnt = helper.to_str(helper.read_file(fpth))
    if not cnt:
        return
    _cookies = {}
    for line in cnt.split('\n'):
        _ = line.split(': ')
        k, v = _[0], ': '.join(_[1:])
        _cookies[k] = v
    return _cookies


def run():
    c = parse_firefox_cookie_file()
    print(c)


if __name__ == '__main__':
    run()
