# -*- coding: utf-8 -*-

import unittest
from db import BaseMySQLDao, UpdatableBaseMySQLDao


class TestBaseMySQLDao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dao = BaseMySQLDao(table='Jobs')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        self.dao.delete()

    def test_insert_and_delete(self):
        self.assertEqual(self.dao.insert(name='AAA', ac_merch=True), 1)
        self.assertEqual(self.dao.insert(name='BBB', ac_merch=False), 1)
        self.assertEqual(self.dao.delete(), 2)

    def test_select(self):
        self.dao.insert(name='AAA', ac_merch=True)
        self.dao.insert(name='BBB', ac_merch=False)
        self.dao.insert(name='CCC')
        self.assertListEqual(
            self.dao.select('name', 'ac_merch', name='AAA'),
            [('AAA', True)]
        )
        self.assertListEqual(
            self.dao.select('name', ac_merch=True),
            [('AAA',)]
        )
        self.assertListEqual(
            self.dao.select('name', ac_merch=False),
            [('BBB',), ('CCC',)]
        )


class TestUpdatableBaseMySQLDao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dao = UpdatableBaseMySQLDao(table='Jobs')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        self.dao.delete()

    def test_update(self):
        self.dao.insert(name='AAA')
        id_ = self.dao.select('id', name='AAA')[0][0]
        self.assertEqual(self.dao.update(id_=id_, ac_merch=True), 1)
        self.assertListEqual(
            self.dao.select('ac_merch', id=id_),
            [(True,)]
        )


if __name__ == '__main__':
    unittest.main()
