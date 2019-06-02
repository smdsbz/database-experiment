# -*- coding: utf-8 -*-

import toml
from flask_restful import Resource
from flask_restful import reqparse, abort
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired
)

from db import EmployeeDao, JobsDao, ShiftsDao

auth = HTTPBasicAuth()  # exported symbol
employ_dao = EmployeeDao()
jobs_dao   = JobsDao()
shifts_dao = ShiftsDao()

SECRET_KEY = toml.load('config/server.toml')['server']['secret-key']
s = Serializer(SECRET_KEY, expires_in=5 * 60)

users = {}      # session holder

@auth.verify_password
def verify_password(user: str, passwd: str) -> bool:
    '''
    Arguments
    ---------
        user: int
            Login name, i.e. username.
        passwd: str
            MD5-hashed password.
    '''
    if user in users:
        try:
            assert user == s.loads(users[user])
            return True
        except SignatureExpired:
            pass
        else:
            pass
        users[user] = s.dumps(user)     # update timestamp
    # reaching to db
    ret = employ_dao.verify_login(user, passwd, hash_alg=lambda s: s)
    if ret < 0:
        return False
    users[user] = s.dumps(user)
    return True


class AuthApi(Resource):
    def get(self, user: str, passwd_md5: str):
        if user in users:
            try:
                assert user == s.loads(users[user])
                return 'User already logged-in elsewhere', 406
            except SignatureExpired:
                # will be updated later
                pass
            else:
                del users[user]
                abort(500)
        ret = employ_dao.verify_login(user, passwd_md5, hash_alg=lambda s: s)
        if ret < 0:
            if ret == -1:
                return 'User not found', 406
            elif ret == -2:
                return 'Wrong password', 406
            abort(500, message='Unknown error!')
        # assert user-password match
        # ret := employee_id
        # get job
        try:
            role = employ_dao.select('job', id=ret)[0][0]
        except Exception:
            abort(500)
        role = 'admin' if role == jobs_dao._RootRoleID else 'common'
        users[user] = s.dumps(user)
        try:
            assert shifts_dao.login_cb(ret) is not None
        except Exception:
            pass
        return {
            'employee_id': ret,
            'role': role
        }, 200

    @auth.login_required
    def delete(self, user: str):
        if user not in users:
            return 'User not logged-in', 406
        del users[user]
        try:
            assert shifts_dao.logout_cb(employ_dao.select('id', login=user)[0][0]) == 0
        except Exception:
            pass
        return '', 200

    @auth.login_required
    def post(self):
        abort(500, message='Use admin client!')
