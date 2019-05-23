# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from db import BaseMySQLDao, UpdatableBaseMySQLDao
from db import MerchandiseDao


class TestBaseMySQLDao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dao = BaseMySQLDao(table='VIP')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        self.dao.delete()

    def test_insert_and_delete(self):
        self.assertEqual(self.dao.insert(name='AAA', date=datetime(1970, 1, 1).date()), 1)
        self.assertEqual(self.dao.insert(name='BBB', date=datetime(1970, 1, 1).date()), 1)
        self.assertEqual(self.dao.delete(), 2)

    def test_select(self):
        self.dao.insert(name='AAA', date=datetime(1970, 1, 1).date())
        self.dao.insert(name='BBB', date=datetime(1970, 1, 2).date())
        self.dao.insert(name='CCC', date=datetime(1970, 1, 2).date())
        self.assertListEqual(
            self.dao.select('name', 'date', name='AAA'),
            [('AAA', datetime(1970, 1, 1).date(),)]
        )
        self.assertListEqual(
            self.dao.select('name', date=datetime(1970, 1, 1).date()),
            [('AAA',)]
        )
        self.assertListEqual(
            self.dao.select('name', date=datetime(1970, 1, 2).date()),
            [('BBB',), ('CCC',)]
        )


class TestUpdatableBaseMySQLDao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dao = UpdatableBaseMySQLDao(table='VIP')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        self.dao.delete()

    def test_update(self):
        self.dao.insert(name='AAA', date=datetime(1970, 1, 1).date())
        id_ = self.dao.select('id', name='AAA')[0][0]
        self.assertEqual(self.dao.update(id_=id_, date=datetime(1970, 1, 2).date()), 1)
        self.assertListEqual(
            self.dao.select('date', id=id_),
            [(datetime(1970, 1, 2).date(),)]
        )


class TestMerchandiseDao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dao = MerchandiseDao()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        self.dao.delete()

    def test_delete(self):
        self.assertEqual(self.dao.delete(), 0)
        self.assertListEqual(
            self.dao.select('name'),
            [('会员卡',)]
        )

    def test_consume_noncountable(self):
        with self.dao._conn.cursor() as cur:
            try:
                self.assertEqual(self.dao.consume(self.dao._VIPCardID, 1, cur), 0)
            except Exception as e:
                raise e
            finally:
                self.dao._conn.rollback()   # no change to data table

    def test_consume_countable(self):
        with self.dao._conn.cursor() as cur:
            try:
                self.dao.insert(name='果粒橙', price=5.5, count=100)
                id_ = self.dao.select('id', name='果粒橙')[0][0]
                self.assertEqual(self.dao.consume(id_, 21, cur), 0)
                self.assertListEqual(
                    self.dao.select('count', id=id_),
                    [(100 - 21,)]
                )
            except Exception as e:
                raise e
            finally:
                self.dao._conn.rollback()

    def test_update(self):
        self.dao.insert(name='果粒橙', price=5.5, count=20)
        id_ = self.dao.select('id', name='果粒橙')[0][0]
        self.assertEqual(self.dao.update(id_, price=5.0), 1)
        self.assertListEqual(
            self.dao.select('price', id=id_),
            [(5.0,)]
        )


if __name__ == '__main__':
    unittest.main()
