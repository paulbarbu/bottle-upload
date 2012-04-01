import unittest

class ValidationTest(unittest.TestCase):
    '''Tests the validation functions'''

    def test_nick(self):
        from index import is_valid_nick

        self.assertFalse(is_valid_nick('!me'))
        self.assertFalse(is_valid_nick(''))
        self.assertTrue(is_valid_nick('foobar2'))
        self.assertTrue(is_valid_nick('foobar'))
        self.assertTrue(is_valid_nick('1foo'))
        self.assertTrue(is_valid_nick('1'))
        self.assertTrue(is_valid_nick('a'))

    def test_pass(self):
        from index import is_valid_password

        self.assertFalse(is_valid_password('!me'))
        self.assertFalse(is_valid_password(''))
        self.assertTrue(is_valid_password('foobar2'))

    def test_email(self):
        from index import is_valid_email

        self.assertFalse(is_valid_email('!me'))
        self.assertFalse(is_valid_email(''))
        self.assertFalse(is_valid_email('foobar2'))
        self.assertTrue(is_valid_email('foobar.b@mail.com'))
        self.assertTrue(is_valid_email('foobar.b+name@mail.com'))
        self.assertTrue(is_valid_email('fo_obar.b+name@mail.com'))

if __name__ == "__main__":
    unittest.main()
