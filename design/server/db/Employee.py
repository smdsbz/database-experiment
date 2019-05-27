# -*- coding: utf-8 -*-

from typing import List, Tuple, Dict, Union, Any

import hashlib
import decimal as D
from datetime import datetime

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

    def has_id(self, id_: str) -> bool:
        '''
        Arguments
        ---------
            id_: str

        Return
        ------
            Whether the employee ID is legit.
        '''
        return bool(self.select('id', id=id_))

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
        return 0


class ShiftsDao(UpdatableBaseMySQLDao):
    '''
    Shifts DAO.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table='Shifts', **kwargs)

    def login_cb(self, id_: int) -> Union[None, datetime]:
        '''
        Login callback, creates new shift record in table.

        Arguments
        ---------
            id_: int

        Return
        ------
            None    - Error.
            datetime- Start timestamp.

        NOTE
        ----
            This method does NOT marks ends to previous un-ended shitfs.
        '''
        if self.get_current_login_start_time(id_)[0] != 2:
            return None
        insert_sql = f'''
            insert into `{self._table}` (`start_time`, `employee_id`)
            values (utc_timestamp(), %s)
        '''
        select_sql = f'''
            select max(`start_time`) from `{self._table}`
            where `employee_id` = %s
        '''
        value = (id_,)
        with self._conn.cursor() as cur:
            if cur.execute(insert_sql, value) != 1:
                self._conn.rollback()
                return None
            cur.execute(select_sql, value)
            ret = cur.fetchone()[0]
            self._conn.commit()
        return ret

    def get_current_login_start_time(self, employee_id: int, dbcursor=None)     \
            -> Tuple[int, Union[datetime, None]]:
        '''
        Arguments
        ---------
            employee_id: int
            dbcursor: MySQLdb Cursor or None

        Return
        ------
            (0, d)  - Start time of current login.
            (2, ?)  - Employee is not yet logged in.
            (3, ?)  - Employee has multiple dirty logins.
        '''
        last_logout_sql = f'''
            select max(`end_time`) from `{self._table}`
            where `employee_id` = %s
        '''
        ongoing_sql = f'''
            select `start_time` from `{self._table}`
            where `employee_id` = %s and `start_time` >= %s
        '''
        ongoing_only_sql = f'''
            select `start_time` from `{self._table}`
            where `employee_id` = %s
        '''
        cur = dbcursor or self._conn.cursor()
        # get latest logged out login
        cur.execute(last_logout_sql, (employee_id,))
        ret = [row[0] for row in cur]
        last_end_time = ret[0]
        # get latest sole on-going login
        if last_end_time is not None:   # if there is ongoing login
            cur.execute(ongoing_sql, (employee_id, last_end_time))
        else:   # if only ongoing logins (may have dirty logins)
            cur.execute(ongoing_only_sql, (employee_id,))
        ret = [row[0] for row in cur]
        if not ret:
            return (2, None)
        if len(ret) > 1:
            return (3, None)
        if dbcursor is None:
            cur.close()
            self._conn.commit()
        return (0, ret[0])

    def transact_cb(self, employee_id: int, sum: D.Decimal, dbcursor) -> int:
        '''
        Updates sum of current shift.

        Arguments
        ---------
            employee_id: int
            sum: Decimal
            dbcursor: MySQLdb Cursor

        Return
        ------
            -1  - Login error.
            -2  - UPDATE error.
            0   - Ok.
        '''
        ret, start = self.get_current_login_start_time(employee_id, dbcursor)
        if ret:
            return -1
        ret = dbcursor.execute(f'''
            update `{self._table}` set
                `sum_consume` = `sum_consume` + %s
            where `employee_id` = %s and `start_time` = %s
        ''', (float(sum), employee_id, start))
        if ret == 0:
            return -2
        return 0

    def logout_cb(self, id_: int) -> int:
        '''
        Logout callback, marks end date to latest unmarked record in table.

        Arguments
        ---------
            id_: int

        Return
        ------
            -1  - Error.
            0   - Ok.
        '''
        sql = f'''
            update `{self._table}` set
                `end_time` = utc_timestamp()
            where `employee_id` = %s and `end_time` is null
            order by `start_time` desc
            limit 1
        '''
        value = (id_,)
        with self._conn.cursor() as cur:
            if cur.execute(sql, value) != 1:
                self._conn.rollback()
                return -1
            self._conn.commit()
        return 0

    def logout_all(self) -> int:
        '''
        Marks all unmarked records.

        Return
        ------
            Rows updated.
        '''
        with self._conn.cursor() as cur:
            ret = cur.execute(f'''
                update `{self._table}` set
                    `end_time` = utc_timestamp()
                where `end_time` is null
            ''')
            self._conn.commit()
        return ret
