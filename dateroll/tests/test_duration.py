import unittest

from dateroll import Date,Duration

class TestDuration(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_just_days(self):
        d1 = Date(2024, 1, 3)
        d2 = Date(2024, 4, 3)
        dur = d2-d1

    def test_simplify(self):
        ...

    

if __name__=='__main__':
    unittest.main()