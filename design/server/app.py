# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Resource, Api
import toml

from api import *

SRVCONFIG = toml.load('config/server.toml')


app = Flask(__name__)
app.config['SECRET_KEY'] = SRVCONFIG['server']['secret-key']

api = Api(app)

api.add_resource(MerchandiseApi, '/api/query/merchandise/<int:id_>')
api.add_resource(
    MerchandiseListApi,
    '/api/list/merchandise/<int:start>/<int:count>',
    '/api/update/merchandise'
)
api.add_resource(
    TransactionApi,
    '/api/query/trans/<int:start>/<int:count>',
    '/api/trans'
)
api.add_resource(
    TransDetailApi,
    '/api/query/trans_detail/<int:trans_id>'
)

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=f"{SRVCONFIG['server']['port']}",
        debug=SRVCONFIG['server']['debug'],
    )
