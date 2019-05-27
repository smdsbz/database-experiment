# -*- coding: utf-8 -*-

import toml
from flask_restful import Resource
from flask_restful import reqparse, abort
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired
)

from db import EmployeeDao

auth = HTTPBasicAuth()
dao = EmployeeDao()

SECRET_KEY = toml.load('config/server.toml')['server']['secret-key']
s = Serializer(SECRET_KEY, expires_in=120)

users = dict()

@auth.verify_password
def verify_password(user: str, passwd: str) -> bool:
    if user in users:
        try:
            s.loads(users[user])
            return True
        except SignatureExpired:
            print(f'Signature for user {user} expired.')
            pass
        else:
            pass
        users[user] = s.dumps(user)     # update timestamp
    print("Reaching to db")
    ret = dao.verify_login(user, passwd)
    if ret == 0:
        users[user] = s.dumps(user)
        return True
    return False
