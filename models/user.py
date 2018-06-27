# -*- coding: utf-8 -*-
__author__ = 'lihe <imanux@sina.com>'
__date__ = '2018/6/25 2:12 PM'
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

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from izen import helper
from iutils.flask_app import db
from iutils import flask_app


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=True)
    create_time = db.Column(db.DateTime)

    def __init__(self, dat):
        self.username = dat.get('username')
        self.hash_password(dat.get('password'))
        self.create_time = helper.now()

    def __repr__(self):
        return '<User> {}@{}'.format(self.username, self.create_time)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=60):
        s = Serializer(flask_app.app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(flask_app.app.config['SECRET_KEY'])
        try:
            dat = s.loads(token)
        except (SignatureExpired, BadSignature) as _:
            return
        user_ = UserModel.query.get(dat['id'])
        return user_


class RAction(object):
    def __init__(self, model):
        self.model = model

    def C(self, dat):
        _user = self.model(dat)
        # _user.hash_password(dat.get('password'))
        db.session.add(_user)
        db.session.commit()

    # def R(self, params):
    #     _user = self.model.query.filter(UserModel.username == username).first()
    #     self.user
