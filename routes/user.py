# -*- coding: utf-8 -*-
__author__ = 'lihe <imanux@sina.com>'
__date__ = '2018/6/22 3:07 PM'
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

app_root = '/'.join(os.path.abspath(__file__).split('/')[:-2])
sys.path.append(app_root)

from flask import Blueprint, jsonify, g, abort
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth

from models.user import UserModel, RAction
from iutils.flask_app import app

auth = HTTPBasicAuth()
route_ = Blueprint('user', __name__)

parser = reqparse.RequestParser()
parser.add_argument('username')


class UserList(Resource):
    @auth.login_required
    def get(self):
        users = UserModel.query.all()
        res = {'data': [{
            'username': u.username
        }] for u in users}
        return res, 201

    def post(self):
        dat = parser.parse_args()
        _ = {
            'username': dat.get('username', ''),
            'password': dat.get('password', '123456'),
        }
        # user_m.create(_)
        RAction(UserModel).C(_)
        return _, 201


class User(Resource):
    def get(self, username):
        user = UserModel.query.filter(UserModel.username == username).first()
        if user is None or user.username.strip == '':
            return {
                'success': False,
                'msg': '无用户'
            }
        else:
            return '%s 用户登陆' % user.username


api = Api()
api.init_app(route_)
api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<username>')
