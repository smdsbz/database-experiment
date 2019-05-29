# -*- coding: utf-8 -*-

import unittest
import decimal as D
import requests as R

url_base = 'http://localhost:2233/api/'
auth = ('root', '123456')


class TestTransaction(unittest.TestCase):

    def test_get_list_transaction(self):
        print()
        r= R.get(url_base + 'query/trans/0/50', auth=auth)
        print(r.text)

    def test_post_transaction(self):
        print()
        r = R.post(
            url_base + 'trans',
            json={
                'cashier': 2,
                'trans': [
                    (2, 8000.00, 1),
                    (3, 199.99, 1)
                ]
            },
            auth=auth
        )
        print(f'status code: {r.status_code}')
        print(f'return:\n{r.text}')

    def test_get_transdetail(self):
        print()
        r = R.get(
            url_base + 'query/trans_detail/3',
            auth=auth
        )
        print(f'status code: {r.status_code}')
        print(f'return:\n{r.text}')


if __name__ == '__main__':
    unittest.main()
