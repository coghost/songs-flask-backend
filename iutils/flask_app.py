# -*- coding: utf-8 -*-
__author__ = 'lihe <imanux@sina.com>'
__date__ = '2018/6/25 4:23 PM'
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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from iutils import sfb_cfg

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sfb_cfg.SQL_DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

db = SQLAlchemy(app)

with app.app_context():
    db.init_app(app)
    db.create_all()
