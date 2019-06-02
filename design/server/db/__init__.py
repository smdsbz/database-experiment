# -*- coding: utf-8 -*-

import toml
import MySQLdb

from typing import List, Tuple, Dict, Union, Any

import toml
DBCONFIG = toml.load('config/db_dev.toml')
RULES = toml.load('config/rules.toml')


class BaseMySQLDao:
    '''
    Base MySQL DAO. Offers basic INSERT, DELETE, SELECT abstractions.

    Arguments
    ---------
        config_path: str
            Path to TOML config file.
        table: str
            Name of the data table.

    Usage
    -----
        Basic INSERT, DELETE, SELECT operations can be done with insert(),
        delete(), select() methods.
        For more advanced usage, you may want to use the _conn member hoding
        the actual connection to the database.

        DO NOT CLOSE _conn!
    '''
    def __init__(self, config: Dict=DBCONFIG, table: str=None):
        self._conn = MySQLdb.connect(**DBCONFIG['connection'])
        # NOTE Turn off auto-commit explicity to enable transaction
        self._conn.autocommit(False)
        with self._conn.cursor() as cur:
            cur.execute('set transaction isolation level serializable')
        if table is None:
            raise ValueError('BaseMySQLDao(): parameter table is None.')
        self._table = table

    def __del__(self):
        self._conn.close()

    def insert(self, **kwargs: Dict[str, Any]) -> int:
        '''
        Perform an INSERT operation.

        Arguments
        ---------
            kwargs: Dict[str, Any]
                Provide your data as key-value pairs, where key is column name,
                and value is data.

        Return
        ------
            Rows affected.
        '''
        cols = list(kwargs.keys())
        values = tuple(kwargs[col] for col in cols)
        sql = f'''
            insert into `{self._table}`
            ({','.join([f'`{col}`' for col in cols])})
            values ({','.join(['%s',] * len(cols))})
        '''
        with self._conn.cursor() as cur:
            try:
                retval = cur.execute(sql, values)
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                raise e
        return retval

    @staticmethod
    def _generate_where_full_intersection(cols: List[str]) -> str:
        '''
        Arguments
        ---------
            cols: List[str]
                column names.

        Return
        ------
            Prepared WHERE-clause.
        '''
        if not cols:
            return ''
        conditions = []
        for col in cols:
            col = col.lower()
            if col.lower() == 'limit':
                continue
            conditions.append(f'`{col}` = %s')
        return 'where ' + ' and '.join(conditions)

    def select(self, *args: List[str], **kwargs: Dict[str, Any]) -> List[Tuple]:
        '''
        Perform a SELECT operation.

        Arguments
        ---------
            args: List[str]
                Columns to be projected.
            kwargs: Dict[str, Any]
                Provide conditions as key-value pairs, where the column given
                as key must equal to the value.

        Return
        ------
            List of data rows satisfying ALL conditions.

        NOTE
        ----
            - Only '=' relation is supported.
            - No 'JOIN' support.
        '''
        cols = list(key for key in kwargs.keys() if key != 'limit')
        values = [kwargs[col] for col in cols]
        if 'limit' in kwargs:
            values.append(kwargs['limit'])
        values = tuple(values)
        sql = f'''
            select {','.join([f'`{col}`' for col in args])}
            from `{self._table}`
            {BaseMySQLDao._generate_where_full_intersection(cols)}
            {'limit %s' if 'limit' in kwargs else ''}
        '''
        retval = []
        with self._conn.cursor() as cur:
            try:
                cur.execute(sql, values)
            except Exception as e:
                raise e
            for vals in cur:
                retval.append(vals)
        return retval

    def delete(self, **kwargs: Dict[str, Any]) -> int:
        '''
        Perform a DELETE operation.

        Arguments
        ---------
            kwargs: Dict[str, Any]
                Provide conditions as key-value pairs, where the column given
                as key must equal to the value.

        Return
        ------
            Rows affected.

        NOTE
        ----
            - Only '=' relation is supported.
            - No 'JOIN' support.
        '''
        cols = [key for key in kwargs.keys()]
        values = tuple(kwargs[col] for col in cols)
        sql = f'''
            delete from `{self._table}`
            {BaseMySQLDao._generate_where_full_intersection(cols)}
        '''
        with self._conn.cursor() as cur:
            try:
                retval = cur.execute(sql, values)
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                raise e
        return retval


class UpdatableBaseMySQLDao(BaseMySQLDao):
    '''
    Extends UPDATE (queried by field 'id') for BaseMySQLDao.
    '''
    def update(self, id_: int, **kwargs) -> int:
        '''
        Perform an UPDATE operation.

        Arguments
        ---------
            id_: int
                ID of the row to be updated.
            kwargs: Dict[str, Any]
                Provide conditions as key-value pairs, where the column given
                as key must equal to the value.

        Return
        ------
            Rows affected.
        '''
        assert isinstance(id_, int)
        assert kwargs
        cols = [key for key in kwargs.keys()]
        values = tuple([kwargs[col] for col in cols] + [id_])
        sql = f'''
            update `{self._table}`
            set {','.join(f'`{col}` = %s' for col in cols)}
            where `id` = %s
        '''
        with self._conn.cursor() as cur:
            try:
                retval = cur.execute(sql, values)
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                raise e
        return retval


from .Merchandise import MerchandiseDao
from .Employee import JobsDao, EmployeeDao, ShiftsDao
from .Transaction import TransactionDao, TransDetailDao
from .VIP import VIPDao, VIPTransRecordDao

__all__ = [
    'DBCONFIG', 'RULES'
    'BaseMySQLDao', 'UpdatableBaseMySQLDao',
    'MerchandiseDao', 'JobsDao', 'EmployeeDao', 'ShiftsDao',
    'TransactionDao', 'TransDetailDao', 'VIPDao', 'VIPTransRecordDao'
]
