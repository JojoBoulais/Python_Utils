import unittest

class CustomUnitTests(unittest.TestCase):
    def setUp(self):
        """Called before test method"""
        pass

    def tearDown(self):
        """Called before test method"""
        pass

    @classmethod
    def setUpClass(cls):
        """Called before any test method"""
        pass

    @classmethod
    def tearDownClass(cls):
    """Called after any test method"""
    pass

    # ------------------- TESTS -------------------

    def test_some_name_here(self):
        pass


if __name__ == '__main__':
    unittest.main()