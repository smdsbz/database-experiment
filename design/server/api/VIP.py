# -*- coding: utf-8 -*-

from typing import *
from decimal import Decimal
from datetime import datetime

from flask import request
from flask_restful import Resource
from flask_restful import abort

from db import VIPDao, VIPTransRecordDao
from .Auth import auth


vip_dao    = VIPDao()
viprec_dao = VIPTransRecordDao()


class VIPListApi(Resource):
    @auth.login_required
    def get(self, start: int, count: int):
        try:
            ret = vip_dao.get_by_id(start, count)
        except Exception as e:
            abort(500, message=str(e))
        return [
            {
                'id': row[0],
                'register-date': row[1].strftime('%Y-%m-%d'),
                'name': row[2] if row[2] is not None else None,
                'tel': row[3] if row[3] is not None else None
            }
            for row in ret
        ], 200

    @auth.login_required
    def put(self):
        data = request.get_json()
        if 'vip_id' in data and data['vip_id'] is not None:
            try:
                # test if no need for renew
                with viprec_dao._conn.cursor() as cur:
                    ret = viprec_dao.transact_cb(data['vip_id'], 0.00, cur)
                    viprec_dao._conn.commit()
                if ret in [0, 1]:
                    return {
                        'vip_id': data['vip_id'],
                        'reason': 'No need for renew'
                    }, 406
                ret = viprec_dao.renew_card(data['vip_id'])
            except Exception as e:
                abort(500, message=str(e))
            if ret:
                abort(500, message=f'Unknown error in VIPTransRecordDao.renew_card(): {ret}.')
            return {
                'vip_id': data['vip_id']
            }, 200
        with vip_dao._conn.cursor() as cur:
            try:
                vip_id, reg_date = vip_dao.create_new_card(
                    data['name'] if 'name' in data else None,
                    data['tel'] if 'tel' in data else None,
                    cur
                )
                ret = viprec_dao.create_new_card_cb(vip_id, reg_date, cur)
                if ret:
                    vip_dao._conn.rollback()
                    if ret == -1:
                        return {
                            'vip_id': vip_id,
                            'reason': 'Not a fresh card'
                        }, 406
                    abort(500, message=f'Unknown error in VIPTransRecordDao.create_new_card_cb(): {ret}.')
                vip_dao._conn.commit()
            except Exception as e:
                vip_dao._conn.rollback()
                abort(500, message=str(e))
        return {
            'vip_id': vip_id
        }, 200


class VIPTransRecordApi(Resource):
    @auth.login_required
    def get(self, vip_id: int):
        try:
            ret = viprec_dao.get_list_by_vip_id(vip_id)
        except Exception as e:
            abort(500, message=str(e))
        return [
            {
                'start-date': row[0].strftime('%Y-%m-%d'),
                'acc-consume': float(row[1])
            }
            for row in ret
        ], 200
