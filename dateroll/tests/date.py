import unittest
import datetime
from dateroll import Date

class TestDDH(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test___cmp__(self):
        '''
        test compares
        '''

        # dateroll.Date with dateroll.Date
        a = Date(2024,12,5)
        b1 = Date(2024,12,5)
        b2 = Date(2024,12,6)
        self.assertEqual(a,b1)
        self.assertNotEqual(a,b2)

        # dateroll.Date with datetime.date
        b1 = datetime.date(2024,12,5)
        b2 = datetime.date(2024,12,6)
        self.assertEqual(a,b1)
        self.assertNotEqual(a,b2)

        # dateroll.Date with datetime.datetime
        b1 = datetime.datetime(2024,12,5)
        b2 = datetime.datetime(2024,12,6)
        self.assertEqual(a,b1)
        self.assertNotEqual(a,b2)

    def test_date(self):
        pass
    def test_datetime(self):
        pass
    def test_dt(self):
        pass
    def test_from_dateti(self):
        pass
    def test_from_string(self):
        pass
    def test_isBd(self):
        pass
    def test_iso(self):
        pass
    def test_isoStr(self):
        pass
    def test_toExcel(self):
        pass
    def test_toUnix(self):
        pass
    def test_weekDay(self):
        pass
    def test_weekYear(self):
        pass

    def test___radd__(self):
        pass
    def test___repr__(self):
        pass
    def test___sub__(self):
        pass

if __name__ == "__main__":
    unittest.main()