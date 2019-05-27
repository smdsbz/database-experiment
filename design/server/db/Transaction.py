# -*- coding: utf-8 -*-

from typing import List, Tuple, Dict, Union, Any

import decimal as D
from datetime import datetime

from . import DBCONFIG, BaseMySQLDao


class TransactionDao(BaseMySQLDao):
    '''
    Transaction DAO.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table='Transaction', **kwargs)

    def start(self, cashier: str, dbcursor) -> int:
        '''
        Creates a record in Transaction table, in the current connection.

        Arguments
        ---------
            cashier: str
                Employee ID (must be legit).
            dbcursor: MySQLdb Cursor

        Return
        ------
            -1      - Error.
            else    - Transaction ID.
        '''
        if cashier < 0:
            return -1
        ret = dbcursor.execute(f'''
            insert into {self._table} (`time`, `cashier`)
            values (utc_timestamp(), %s)
        ''', (cashier,))
        if ret != 1:
            return -1
        dbcursor.execute('select last_insert_id()')
        return dbcursor.fetchone()[0]


class TransDetailDao(BaseMySQLDao):
    '''
    TransDetail DAO.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table='TransDetail', **kwargs)

    def fill(self, trans_id: int,
            items: List[Tuple[int, D.Decimal, int]],
            dbcursor) -> int:
        '''
        Arguments
        ---------
            trans_id: int
            items: List[Tuple[int, Decimal, int]]
                List of merchandise transaction in tuples of 3:

                    (merch_id, actual_price, count)

            dbcursor: MySQLdb Cursor

        Return
        ------
            -1  - Error.
            0   - Ok.
        '''
        if dbcursor.executemany(f'''
                    insert into {self._table} values (%s,%s,%s,%s)
                ''', [(trans_id, *item) for item in items]) != len(items):
            return -1
        return 0

    def get_sum(self, trans_id: int, dbcursor=None) -> Union[None, float]:
        '''
        Arguments
        ---------
            trans_id: int
            dbcursor: MySQLdb Cursor or None
                Transaction context.

        Return
        ------
            Sum of transaction or None if trans_id not present.
        '''
        if dbcursor is None:
            ret = [
                row[0] for row in
                self.select('sum(`price` * `count`)', trans_id=trans_id)
            ]
        else:
            dbcursor.execute(f'''
                select sum(`price` * `count`) from `{self._table}`
                where `trans_id` = %s
            ''', (trans_id,))
            ret = [row[0] for row in dbcursor]
        if not ret:
            return None
        return ret[0]
