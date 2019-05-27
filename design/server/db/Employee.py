# -*- coding: utf-8 -*-

from typing import List, Tuple, Dict, Union, Any

import hashlib

from . import DBCONFIG, UpdatableBaseMySQLDao


class JobsDao(UpdatableBaseMySQLDao):
    '''
    Jobs DAO.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table='Jobs', **kwargs)

    @property
    def _RootRoleID(self) -> int:
        '''
        ID of root role.
        '''
        initial_role = DBCONFIG['initial-data']['Jobs']
        for role in initial_role:
            if role['name'] == '管理员':
                return role['id']

    def delete(self, **kwargs):
        cols = list(kwargs.keys())
        values = tuple([kwargs[col] for col in cols] + [[self._RootRoleID]])
        where_block = self._generate_where_full_intersection(cols)
        where_block = ((where_block + ' and ') if where_block else 'where ')    \
                        + '`id` not in %s'
        sql = f'delete from `{self._table}` {where_block}'
        with self._conn.cursor() as cur:
            try:
                retval = cur.execute(sql, values)
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                raise e
        return retval


class EmployeeDao(UpdatableBaseMySQLDao):
    '''
    Employee DAO.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table='Employee', **kwargs)

    def verify_login(self, user: str, passwd: str, hash_alg=hashlib.md5) -> int:
        '''
        Verifies a login.

        Arguments
        ---------
            user: str
                User name.
            passwd: str
                Password (raw).
            hash_alg: function (default: hashlib.md5)
                Password hashing algorithm.

        Return
        ------
            0   - Ok.
            1   - User not found.
            2   - Wrong password.
        '''
        passwd = hash_alg(passwd.encode('utf-8')).hexdigest()
        passwds = [passwd[0] for passwd in self.select('passwd', login=user)]
        if not passwds:
            return 1
        if passwd not in passwds:
            return 2
        # push to session
        print('returning 0')
        return 0
