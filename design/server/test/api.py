# -*- coding: utf-8 -*-

import unittest
import decimal as D
import requests as R

url_base = 'http://localhost:2233/api/'
auth = ('root', '123456')


class TestTransaction(unittest.TestCase):

    def test_post(self):
        print()
        r = R.post(
            url_base + 'trans',
            json={
                'cashier': 1,
                'trans': [
                    (2, 8000.00, 1),
                    (3, 199.99, 1)
                ]
            },
            auth=auth
        )
        print(f'status code: {r.status_code}')
        print(f'return: {r.text}')


if __name__ == '__main__':
    unittest.main()
