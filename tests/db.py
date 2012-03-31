#! /usr/bin/env python2.7
import unittest

class DatabaseTest(unittest.TestCase):
    '''Tests the database functionality'''

    def setUp(self):
        import sqlite3 as db
        import random

        self.valid_db = './good.db'
        self.invalid_db = 'bad.db'

        c = db.connect(self.valid_db)
        c.execute('CREATE TABLE dummy(foo INTEGER)')
        c.close()

        with open(self.invalid_db, 'w') as f:
            for i in range(0, 17):
                f.write(str(random.randint(0, 255)))

    def tearDown(self):
        import os

        os.unlink(self.valid_db)
        os.unlink(self.invalid_db)

        self.valid_db = None
        self.invalid_db = None

    def test_valid_file(self):
        from index import is_valid_sqlite3

        self.assertFalse(is_valid_sqlite3(self.invalid_db))
        self.assertTrue(is_valid_sqlite3(self.valid_db))

if __name__ == "__main__":
    unittest.main()
