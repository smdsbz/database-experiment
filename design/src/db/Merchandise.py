# -*- coding: utf-8 -*-

from typing import List, Tuple, Union

from . import BaseMySQLDao


class MerchandiseDao(BaseMySQLDao):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, table='Merchandise', **kwargs)

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
        pass

    def update_info(self, merch: Union[int, str]) -> bool:
        if isinstance(merch, int):
            merchid = merch
        elif isinstance(merch, str):
            merchid = self.get_id_by_name(merch)
        if merchid == 0:    # infos of VIP Card cannot be changed!
            return False

        # TODO

        return False
