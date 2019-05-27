# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from flask_restful import abort
import decimal as D

from db import MerchandiseDao, TransactionDao, TransDetailDao, EmployeeDao, ShiftsDao
from .Auth import auth

D.getcontext().prec = 2

merch_dao  = MerchandiseDao()
trans_dao  = TransactionDao()
detail_dao = TransDetailDao()
employ_dao = EmployeeDao()
shift_dao  = ShiftsDao()


class TransactionApi(Resource):
    @auth.login_required
    def get(self, start: int, count: int):
        sql = f'''
            select T.`id`, T.`time`, T.`cashier`, E.`login`
            from `{trans_dao._table}` as T, `{employ_dao._table}` as E
            where T.`id` >= %s and T.`cashier` = E.`id`
            limit %s
        '''
        with trans_dao._conn.cursor() as cur:
            cur.execute(sql, (start, count))
            result = [row for row in cur]
        return [
            {
                'trans_id': row[0],
                'time': row[1].strftime('%Y-%m-%d %H:%M:%S'),
                'cashier_id': row[2],
                'cashier_login': row[3]
            }
            for row in result
        ]

    @auth.login_required
    def post(self):
        '''
        JSON data format:

            {
                'cashier': cashier_id,
                'trans': [
                    [merch_id, actual_price, count],
                    ...
                ]
            }
        '''
        data = request.get_json()
        if 'cashier' not in data or 'trans' not in data:
            return {
                'reason': 'cashier, trans data must be given!'
            }, 406
        cashier, trans_items = data['cashier'], data['trans']
        if not employ_dao.has_id(cashier):
            return {
                'reason': f'Cashier ID {cashier} is illegal!'
            }, 406
        conn = trans_dao._conn
        with conn.cursor() as cur:
            try:
                trans_id = trans_dao.start(cashier, cur)
                # create transaction master record
                if trans_id < 0:
                    conn.rollback()
                    abort(500, message='Failed to start transaction!')
                # consume stored merchandise
                for merch_id, _, count in trans_items:
                    ret = merch_dao.consume(merch_id, count, cur)
                    if ret:
                        conn.rollback()
                        if ret == -1 or ret == 3:
                            return {
                                'merch_id': merch_id,
                                'reason': 'Illegal ID'
                            }, 406
                        elif ret == 1:
                            return {
                                'merch_id': merch_id,
                                'reason': 'Not enough in storage'
                            }, 406
                        elif ret == 2:
                            return {
                                'merch_id': merch_id,
                                'reason': 'UPDATE finished with error'
                            }, 406
                        abort(500, message=f'Unknown error at consume(): {ret}.')
                # fill transaction details
                if detail_dao.fill(trans_id, trans_items, cur):
                    conn.rollback()
                    abort(500, message='Error occured while filling '
                                        'transaction details!')
                # update shift sum
                trans_sum = detail_dao.get_sum(trans_id, cur)
                if trans_sum is None:
                    conn.rollback()
                    abort(500)
                if shift_dao.transact_cb(cashier, trans_sum, cur):
                    conn.rollback()
                    return {
                        'reason': f'Employee {cashier} not logged in!'
                    }, 406
                conn.commit()
            except Exception as e:
                conn.rollback()
                abort(500, message=str(e))
        return '', 201


class TransDetailApi(Resource):
    @auth.login_required
    def get(self, trans_id: int):
        sql = f'''
            select D.`merch_id`, M.`name`, D.`price`, M.`price` as orig_price,
                D.`count`
            from `{merch_dao._table}` as M, `{detail_dao._table}` as D
            where D.`trans_id` = %s and M.`id` = D.`merch_id`
        '''
        value = (trans_id,)
        with detail_dao._conn.cursor() as cur:
            cur.execute(sql, value)
            ret = [row for row in cur]
            detail_dao._conn.commit()
        return [
            {
                'merch_id': row[0],
                'name': row[1],
                'actual_price': float(row[2]),
                'orig_price': float(row[3]),
                'count': row[4]
            }
            for row in ret
        ]
