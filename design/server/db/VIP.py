# -*- coding: utf-8 -*-

from typing import *
from decimal import Decimal
from datetime import datetime, timedelta

from . import BaseMySQLDao, RULES

MAX_SPAN = timedelta(RULES['VIP-span']['span-in-days'])
RENEW_VALVE = RULES['VIP-span']['renew-valve']      # type: float


class VIPDao(BaseMySQLDao):
    '''
    VIP DAO.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, table='VIP', **kwargs)

    def get_by_id(self, start: int, count: int)                                 \
            -> List[Tuple[int, datetime, Union[str, None], Union[str, None]]]:
        '''
        Arguments
        ---------
            start: int
            count: int
                Maximux count of records to return. If <= 0, return all.
        '''
        sql = f'''
            select `id`, `date`, `name`, `tel` from `{self._table}`
            where `id` >= %s
            order by `date` asc
        '''
        if count > 0:
            sql += ' limit %s'
            value = (start, count)
        else:
            value = (start,)
        with self._conn.cursor() as cur:
            try:
                cur.execute(sql, value)
                ret = [row for row in cur]
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                raise e
        return ret

    def create_new_card(self, name: str, tel: str, dbcursor)                    \
            -> Tuple[int, datetime]:
        '''
        Insert new VIP Card.

        Arguments
        ---------
            name: str or None
                Name.
            tel: str or None
                Telephone.
            dbcursor: MySQLdb Cursor

        Return
        ------
            (id, date)  - New VIP card ID, with its register date.
        '''
        dbcursor.execute(f'''
            insert into `{self._table}` (`date`, `name`, `tel`) values
            (curdate(), %s, %s)
        ''', (name, tel))
        dbcursor.execute('select last_insert_id()')
        vip_id = dbcursor.fetchone()[0]
        dbcursor.execute(f'''
            select `date` from `{self._table}` where `id` = %s
        ''', (vip_id,))
        register_date = dbcursor.fetchone()[0]
        return (vip_id, register_date)


class VIPTransRecordDao(BaseMySQLDao):
    '''
    VIP Transaction Record DAO.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, table='VIPTransRecord', **kwargs)

    def get_list_by_vip_id(self, vip_id: int) -> List[Tuple[datetime, Decimal]]:
        sql = f'''
            select `start_date`, `acc_consume` from `{self._table}`
            where `vip_id` = %s
            order by `start_date` desc
        '''
        value = (vip_id,)
        with self._conn.cursor() as cur:
            try:
                cur.execute(sql, value)
                ret = [row for row in cur]
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                raise e
        return ret

    def create_new_card_cb(self, vip_id: int, register_date: datetime, dbcursor)\
            -> int:
        '''
        Return
        ------
            -1  - Not a fresh new card.
            0   - Ok.
        '''
        dbcursor.execute(f'''
            select `vip_id` from `{self._table}`
            where `vip_id` = %s
            limit 1
        ''', (vip_id,))
        if dbcursor.fetchone() is not None:
            return -1
        dbcursor.execute(f'''
            insert into `{self._table}` values (%s, %s, 0.00)
        ''', (vip_id, register_date))

    def renew_card(self, vip_id: int) -> int:
        '''
        Return
        ------
            0   - Ok.
        '''
        sql = f'''
            insert into `{self._table}` values (%s, curdate(), 0.00)
        '''
        value = (vip_id,)
        with self._conn.cursor() as cur:
            try:
                cur.execute(sql, value)
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                raise e
        return 0

    def transact_cb(self, vip_id: int, sum_consume: float, dbcursor) -> int:
        '''
        Update total consume in current span.

        Argument
        --------
            vip_id: int
                If not using VIP card, don't call this method.
            sum_consume: float
            dbcursor: MySQLdb Cursor

        Return
        ------
            -2  - Error.
            -1  - invalid VIP ID.
            0   - Ok.
            1   - Timeout but renewed.
            2   - Timeout.

        NOTE
        ----
            If time out, reject or automatically renew if reached valve.
        '''
        # get latest span
        dbcursor.execute(f'''
            select curdate(), `start_date`, `acc_consume`
            from `{self._table}`
            where `vip_id` = %s
            order by `start_date` desc limit 1
        ''', (vip_id,))
        ret = dbcursor.fetchone()   # type: Tuple[datetime, datetime, Decimal]
        # invalid VIP ID
        if ret is None:
            return -1
        last_span_start = ret[1]
        span = ret[0] - last_span_start     # type: timedelta
        # add to acc_consume if card not time out or reached valve
        if span < MAX_SPAN:
            dbcursor.execute(f'''
                update `{self._table}` set `acc_consume` = `acc_consume` + %s
                where `vip_id` = %s and `start_date` = %s
            ''', (sum_consume, vip_id, last_span_start))
            return 0
        # if no action in last span, cannot be renewed
        if span >= MAX_SPAN * 2:
            return 2
        # renew card if time out (within one span margin) but reached valve
        if float(ret[2]) > RENEW_VALVE:
            # insert new span
            dbcursor.execute(f'''
                insert into `{self._table}` values (%s, %s, %s)
            ''', (vip_id, last_span_start + MAX_SPAN, sum_consume))
            return 1
        return 2
