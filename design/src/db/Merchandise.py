# -*- coding: utf-8 -*-

from typing import List, Tuple, Dict, Union, Any

import toml
from . import DBCONFIG, UpdatableBaseMySQLDao


class MerchandiseDao(UpdatableBaseMySQLDao):
    '''
    Merchandise DAO.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table='Merchandise', **kwargs)
        # self checks
        _ = self._VIPCardID

    def get_id_by_name(self, merch: str) -> int:
        '''
        Get ID of merchandise by name.

        Arguments
        ---------
            merch: str
                Name of the merchandise.

        Return
        ------
            -2      - Multiple records found.
            -1      - No records found.
            other   - ID of the merchandise.
        '''
        ids = [tup[0] for tup in self.select('id', name=merch)]
        if not ids:
            return -1
        if len(ids) > 1:
            return -2
        return ids[0][0]

    @property
    def _VIPCardID(self) -> int:
        '''
        ID of VIPCard in database.
        '''
        initial_merch = DBCONFIG['initial-data']['Merchandise']
        for merch in initial_merch:
            if merch['name'] == '会员卡':
                return merch['id']

    def delete(self, **kwargs) -> int:
        cols = list(kwargs.keys())
        values = tuple([kwargs[col] for col in cols] + [[self._VIPCardID]])
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

    def update(self, merch: Union[int, str], **kwargs: Dict[str, Any]) -> bool:
        '''
        Update info of merchandise.

        Arguments
        ---------
            merch: Union[int, str]
                ID or unique name.
            kwargs: Dict[str, Any]
                Fields to be updated.

        Return
        ------
            Whether the operation was successful.
        '''
        if isinstance(merch, int):
            merchid = merch
        elif isinstance(merch, str):
            merchid = self.get_id_by_name(merch)
        else:
            raise TypeError(f'merch: expecting int or str, got {type(merch)}.')
        if merchid == self._VIPCardID:  # infos of VIP Card cannot be changed!
            return False
        elif merchid < 0:
            return False
        if super().update(merchid, **kwargs) != 1:
            return False
        return True

    def consume(self, merch: int, count: int, dbcursor) -> int:
        '''
        Consume a merchandise.

        Arguments
        ---------
            merch: int
                ID (must be legit).
            count: int
                Numbers of items to be consumed.
            dbcursor: MySQLdb Cursor
                Transaction context.

        Return
        ------
            -1  - Illegal ID.
            0   - OK.
            1   - Not enough in storage.
            2   - UPDATE query finished with error.
            3   - Row with ID not fount.

        NOTE
        ----
            - This method should only be executed in a with-block.

                with connection.cursor() as cur:
                    try:
                        ...
                        merch_dao.comsume(merch=x, count=y, dbcursor=cur)
                        ...
                        connection.commit()
                    except Exception as e:
                        ...
        '''
        if merch != self._VIPCardID and merch < 0:
            return -1
        # get count of item
        dbcursor.execute(f'''
            select `count` from `{self._table}`
            where `id` = %s
        ''', (merch,))
        stored_count = dbcursor.fetchone()
        if stored_count is None:
            return 3
        stored_count = stored_count[0]
        # if has sufficient in storage, consume() does nothing to this table
        if stored_count is None:
            return 0
        if count > stored_count:
            return 1
        # do consume
        if dbcursor.execute(f'''
                    update `{self._table}` set `count` = %s where `id` = %s
                ''', (stored_count - count, merch)) != 1:
            return 2
        return 0
