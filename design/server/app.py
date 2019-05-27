# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Resource, Api

from api import *

app = Flask(__name__)
api = Api(app)

api.add_resource(MerchandiseApi, '/api/query/merchandise/<int:id_>')
api.add_resource(MerchandiseListApi,
        '/api/list/merchandise/<int:start>/<int:count>',
        '/api/update/merchandise')

if __name__ == '__main__':
    app.run(
        host='localhost',
        port='2233',
        debug=True,
    )
