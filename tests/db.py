import unittest
from mock import MagicMock, patch

class DatabaseTest(unittest.TestCase):
    '''Tests the database functionality'''

    def test_valid_file(self):
        from index import is_valid_sqlite3

        with patch('index.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=file)
            fh = mock_open.return_value.__enter__.return_value

            fh.read.return_value = 'SQLite format 3'

            self.assertTrue(is_valid_sqlite3('db.db'))
            fh.read.assert_called_with(15)

            fh.read.return_value = 'SQLite format 3 '#notice the space

            self.assertFalse(is_valid_sqlite3('db.db'))
            fh.read.assert_called_with(15)


if __name__ == "__main__":
    unittest.main()
