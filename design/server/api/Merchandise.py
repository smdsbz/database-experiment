# -*- coding: utf-8 -*-

from typing import *
from decimal import Decimal

from flask import request
from flask_restful import Resource
from flask_restful import reqparse, abort

from db import MerchandiseDao
from .Auth import auth

merchlist_post_parser = reqparse.RequestParser()
merchlist_post_parser.add_argument('name', type=str)
merchlist_post_parser.add_argument('price', type=float)
merchlist_post_parser.add_argument('count', type=int)

dao = MerchandiseDao()


class MerchandiseApi(Resource):
    @auth.login_required
    def get(self, id_: int):
        result = dao.select('name', 'price', 'count', id=id_)
        if not result:
            return None
        result = result[0]
        return {
            'name': result[0],
            'price': float(result[1]),
            'count': int(result[2]) if result[2] is not None else None
        }, 200

    @auth.login_required
    def delete(self, id_: int):
        try:
            ret = dao.delete(id=id_)
        except Exception as e:
            abort(500, message=str(e))
        if ret != 1:
            abort(500, message=f'Deletion affected {ret} rows!')
        return '', 200

    @auth.login_required
    def put(self, id_: int):
        '''
        Update a merchandise.

        Fields to change should be given in JSON.
        '''
        new_vals = request.get_json()
        print(new_vals)
        try:
            if 'add' not in new_vals and 'minus' not in new_vals:
                ret = dao.update(id_, **new_vals)
                if ret == 0:
                    return 'No row affected', 200
                assert ret == 1
            else:
                if 'add' in new_vals:
                    ret = dao.store(id_, new_vals['add'])
                elif 'minus' in new_vals:
                    ret = dao.store(id_, -new_vals['minus'])
                if ret == -1:
                    return 'Illegal ID', 406
                elif ret == 1:
                    return 'Not enough in storage', 406
                elif ret == 2:
                    return 'UPDATE query finished with error', 406
                elif ret == 3:
                    return 'Row with ID not found', 406
        except Exception as e:
            return str(e), 406
        return '', 200


class MerchandiseListApi(Resource):
    @auth.login_required
    def get(self, start: int, count: int):
        try:
            ret = dao.get_by_id_range(start, count)
        except Exception as e:
            abort(500, message=str(e))
        return [
            {
                'id': int(row[0]),
                'name': row[1],
                'price': float(row[2]),
                'count': int(row[3]) if row[3] is not None else None
            }
            for row in ret
        ], 200

    @auth.login_required
    def post(self):
        '''
        Insert a new merchandise.

        JSON data format:

            {
                'name': str,
                'price': float,
                'count': [optional] int or None
            }
        '''
        values = request.get_json()
        if ('name' not in values) or ('price' not in values):
            abort(404, message='Name and price must be given!')
        if 'count' not in values:
            values['count'] = None
        try:
            ret = dao.insert(**values)
        except Exception as e:
            abort(500, message=str(e))
        if ret != 1:
            abort(500, message=f'Insertion affected {ret} rows!')
        return '', 200


class MerchandiseByNameApi(Resource):
    @auth.login_required
    def get(self, name: str):
        try:
            ret = dao.get_by_name_fuzzy(name)
            return [
                {
                    'merch_id': row[0],
                    'name': row[1],
                    'orig_price': float(row[2])
                }
                for row in ret
            ], 200
        except Exception as e:
            abort(500)
