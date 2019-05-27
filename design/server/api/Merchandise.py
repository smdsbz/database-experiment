# -*- coding: utf-8 -*-

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
        }

    @auth.login_required
    def delete(self, id_: int):
        try:
            ret = dao.delete(id=id_)
        except Exception as e:
            abort(500, message=str(e))
        if ret != 1:
            abort(500, message=f'Deletion affected {ret} rows!')
        return '', 204


class MerchandiseListApi(Resource):
    @auth.login_required
    def get(self, start: int, count: int):
        sql = f'''
            select `id`, `name`, `price`, `count` from {dao._table}
            where `id` >= %s
            limit %s
        '''
        with dao._conn.cursor() as cur:
            cur.execute(sql, (start, count))
            result = [row for row in cur]
        return [
            {
                'id': int(row[0]),
                'name': row[1],
                'price': float(row[2]),
                'count': int(row[3]) if row[3] is not None else None
            }
            for row in result
        ]

    @auth.login_required
    def post(self):
        '''
        Insert a new merchandise.
        '''
        values = merchlist_post_parser.parse_args(strict=False)
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
        return '', 201
