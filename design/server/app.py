# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Resource, Api
import toml

from api import *

SRVCONFIG = toml.load('config/server.toml')


app = Flask(__name__)
app.config['SECRET_KEY'] = SRVCONFIG['server']['secret-key']

api = Api(app)

api.add_resource(
    MerchandiseApi,
    '/api/query/merchandise/<int:id_>'                  # GET, DELETE, PUT
)
api.add_resource(
    MerchandiseByNameApi,
    '/api/byname/merchandise/<name>'                    # GET
)
api.add_resource(
    MerchandiseListApi,
    '/api/list/merchandise/<int:start>/<int:count>',    # GET
    '/api/update/merchandise'                           # POST
)
api.add_resource(
    TransactionApi,
    '/api/list/trans/<int:start>/<int:count>',
    '/api/trans'
)
api.add_resource(
    TransDetailApi,
    '/api/query/trans-detail/<int:trans_id>'
)
api.add_resource(
    AuthApi,
    '/api/auth/login/<user>/<passwd_md5>',              # GET
    '/api/auth/logout/<user>',                          # DELETE
    '/api/auth/signup'                                  # POST (not implemented)
)
api.add_resource(
    EmployeeListApi,
    '/api/list/employee/<int:start>/<int:count>'        # GET
)
api.add_resource(
    ShiftsApi,
    '/api/query/shifts/<int:employee_id>'               # GET
)

if __name__ == '__main__':
    app.run(
        host=SRVCONFIG['server']['host'],
        port=SRVCONFIG['server']['port'],
        debug=SRVCONFIG['server']['debug'],
    )
