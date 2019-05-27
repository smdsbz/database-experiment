# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from flask_restful import abort
import decimal as D

from db import MerchandiseDao, TransactionDao, TransDetailDao, EmployeeDao
from .Auth import auth

D.getcontext().prec = 2

merch_dao = MerchandiseDao()
trans_dao = TransactionDao()
detail_dao = TransDetailDao()
employ_dao = EmployeeDao()


class TransactionApi(Resource):
    @auth.login_required
    def get(self, start: int, count: int):
        pass

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
            abort(406, message='cashier, trans data must be given!')
        cashier, trans_items = data['cashier'], data['trans']
        if not employ_dao.has_id(cashier):
            abort(406, message=f'Cashier ID {cashier} is illegal!')
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
                conn.commit()
            except Exception as e:
                conn.rollback()
                abort(500, message=str(e))
        return '', 201
