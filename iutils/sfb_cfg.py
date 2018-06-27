# -*- coding: utf-8 -*-
__author__ = 'lihe <imanux@sina.com>'
__date__ = '2018/6/22 4:16 PM'
__description__ = '''
    ☰
  ☱   ☴
☲   ☯   ☵
  ☳   ☶
    ☷
'''

import os
import sys

app_root = '/'.join(os.path.abspath(__file__).split('/')[:-2])
sys.path.append(app_root)

import logzero

from izen.icfg import Conf, LFormatter

__all__ = ['cfg']

_pth_cfg = os.path.join(app_root, 'configs/.code.cnf')
cfg = Conf(
    pth=_pth_cfg,
    dat={
        'svr.host': '127.0.0.1',
        'svr.port': 5000,
        'svr.debug': True,
        'mysql.enabled': True,
        'mysql.host': '127.0.0.1',
        'mysql.port': 3306,
        'mysql.db': 'sio',
        'mysql.username': 'root',
        'mysql.password': '123456',
        'mg.host': '127.0.0.1',
        'mg.port': 27027,
        'mg.db': 'test_db',
        'mg.username': '',
        'mg.password': '',
        'rds.host': '127.0.0.1',
        'rds.port': 6379,
        'rds.socket_timeout': 2,
        'rds.socket_connect_timeout': 2,
        'rds.password': '',
        'rds.db': {
            'val': 0,
            'proto': str
        },
        'log.file_pth': os.path.join(os.path.expanduser('~'), '.sfb/sfb.log')
    }
).cfg

# 检查日志配置, 是否写入文件
if cfg.get('log.enabled', False):
    logzero.logfile(
        cfg.get('log.file_pth', '/tmp/sfb.log'),
        maxBytes=cfg.get('log.file_size', 5) * 1000000,
        backupCount=cfg.get('log.file_backups', 3),
        loglevel=cfg.get('log.level', 10),
    )

# bagua = '☼✔❄✖✄'
# bagua = '☰☷☳☴☵☲☶☱'  # 乾(天), 坤(地), 震(雷), 巽(xun, 风), 坎(水), 离(火), 艮(山), 兑(泽)
_log_pre = '🍺🍻♨️️😈☠'
logzero.formatter(LFormatter(_log_pre))

if cfg.get('mysql.enabled'):
    SQL_DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        cfg.get('mysql.username', ''),
        cfg.get('mysql.password', ''),
        cfg.get('mysql.host', ''),
        cfg.get('mysql.port', 3306),
        cfg.get('mysql.db', ''),
    )
else:
    SQL_DB_URI = ''
