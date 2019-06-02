# -*- coding: utf-8 -*-

from typing import *
from decimal import Decimal

from flask import request
from flask_restful import Resource
from flask_restful import abort

from db import EmployeeDao, JobsDao, ShiftsDao
from .Auth import auth


employ_dao = EmployeeDao()
job_dao    = JobsDao()
shift_dao  = ShiftsDao()


class EmployeeListApi(Resource):
    @auth.login_required
    def get(self, start: int, count: int):
        '''
        Arguments
        ---------
            start: int
            count: int
        '''
        sql = f'''
            select E.`id`, E.`login`, J.`name`, E.`tel`
            from `{employ_dao._table}` as E, `{job_dao._table}` as J
            where E.`job` = J.`id` and E.`id` >= %s
            order by E.`id` asc
        '''
        if count > 0:
            sql += ' limit %s'
            value = (start, count)
        else:
            value = (start,)
        with employ_dao._conn.cursor() as cur:
            try:
                cur.execute(sql, value)
                ret = [row for row in cur]
                employ_dao._conn.commit()
            except Exception as e:
                employ_dao._conn.rollback()
                abort(500, message=str(e))
        return [
            {
                'employee_id': row[0],
                'name': row[1],
                'job': row[2],
                'tel': row[3]
            }
            for row in ret
        ], 200

    @auth.login_required
    def post(self):
        '''
        JSON data format:

            {
                'login': str,
                'passwd': str (MD5 hashed),
                'job': int (job_id),
                'tel': str
            }
        '''
        data = request.get_json()
        if ('login' not in data) or ('passwd' not in data)                      \
                or ('job' not in data) or ('tel' not in data):
            return 'Data incomplete', 406
        try:
            ret = employ_dao.insert(**data)
            assert ret == 1
        except Exception as e:
            abort(500, message=str(e))
        return '', 200


class ShiftsApi(Resource):
    @auth.login_required
    def get(self, employee_id: int):
        try:
            ret = shift_dao.get_all_by_emploee_id(employee_id)
        except Exception as e:
            abort(500, message=str(e))
        return [
            {
                'start': row[0].strftime('%Y-%m-%d %H:%M:%S'),
                'end': row[1].strftime('%Y-%m-%d %H:%M:%S') if row[1] is not None else None,
                'sum': float(row[2])
            }
            for row in ret
        ], 200


class JobsListApi(Resource):
    @auth.login_required
    def get(self):
        try:
            ret = job_dao.select('id', 'name')
        except Exception as e:
            abort(500, message=str(e))
        return [
            {
                'job_id': row[0],
                'name': row[1]
            }
            for row in ret
        ], 200
