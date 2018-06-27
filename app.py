#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lihe <imanux@sina.com>'
__date__ = '2018/6/21 3:49 PM'
__description__ = '''
    ☰
  ☱   ☴
☲   ☯   ☵
  ☳   ☶
    ☷
'''

import os
import sys
import json
import importlib

app_root = '/'.join(os.path.abspath(__file__).split('/')[:-2])
sys.path.append(app_root)

from logzero import logger as log
from izen import dec
from flask_cors import CORS

from iutils import cfg
from iutils.flask_app import app

import routes

# 针对前后端分离产生的跨域情况
CORS(app)


def auto_reg():
    """auto register all bp modules named with ``route_`` in routes dir

    :return:
    :rtype:
    """

    @dec.catch(True, AttributeError)
    def reg(rt):
        module_ = importlib.import_module('routes.{}'.format(rt))
        if not module_:
            return
        md = getattr(module_, 'route_')
        if not md:
            return
        app.register_blueprint(md, url_prefix='')

    for rt in routes.__all__:
        reg(rt)


def run():
    svr = {
        'host': cfg.get('svr.host', '0.0.0.0'),
        'port': cfg.get('svr.port', 5000),
        'debug': cfg.get('svr.debug'),
    }
    # log.debug('Server Running @ ({0[host]}:{0[port]})'.format(svr))
    log.debug('Server Running @ ({host}:{port})'.format(**svr))
    auto_reg()
    app.run(**svr)


if __name__ == '__main__':
    run()
