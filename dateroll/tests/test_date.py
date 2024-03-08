import datetime
import unittest
import code

from dateutil.relativedelta import relativedelta

from dateroll import Date, Duration


class TestDate(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test___cmp__(self):
        """
        test compares
        """

        # dateroll.Date with dateroll.Date
        a = Date(2024, 12, 5)
        b1 = Date(2024, 12, 5)
        b2 = Date(2024, 12, 6)
        self.assertEqual(a, b1)
        self.assertNotEqual(a, b2)

        # dateroll.Date with datetime.date
        b1 = datetime.date(2024, 12, 5)
        b2 = datetime.date(2024, 12, 6)
        self.assertEqual(a, b1)
        self.assertNotEqual(a, b2)

        # dateroll.Date with datetime.datetime
        b1 = datetime.datetime(2024, 12, 5)
        b2 = datetime.datetime(2024, 12, 6)
        self.assertEqual(a, b1)
        self.assertNotEqual(a, b2)

    def test_to_conversions(self):
        """
        dateroll.Date to datetime.datetime and datetime.date
        """

        a = Date(1900, 1, 1)
        b = datetime.date(1900, 1, 1)
        c = datetime.datetime(1900, 1, 1)

        self.assertEqual(b, a.date)
        self.assertEqual(c, a.datetime)

    def test_from_dateti(self):
        """conversion from"""

        ref = Date(1900, 1, 1)
        a = datetime.date(1900, 1, 1)
        b = datetime.datetime(1900, 1, 1)

        d1 = Date.from_datetime(a)
        self.assertEqual(ref, d1)

        d2 = Date.from_datetime(b)
        self.assertEqual(ref, d2)

        d3 = Date.from_string("1/1/1900")
        self.assertEqual(ref, d3)

    def test_is_bd(self):
        """
        check if day is a business day given a specific calendar
        """
        sunday = Date.from_string("3/3/24")
        monday = Date.from_string("3/4/24")
        christmas = Date.from_string("12/25/23")

        self.assertFalse(sunday.is_bd(cals="WEuLN"))
        self.assertTrue(monday.is_bd(cals="WEuNYuBR"))
        self.assertFalse(christmas.is_bd(cals="WEuNYuBR"))

    def test_conversions_out(self):
        """
        various properties
        """
        d = Date.from_string("3/3/24")
        # iso
        self.assertEqual(d.iso, "2024-03-03")

        # xls
        self.assertEqual(d.xls, 45354)

        # unix
        ts = d.datetime.timestamp()
        self.assertEqual(d.unix, ts)

        # #dotw
        dotw = d.dotw
        self.assertEqual(dotw, "Sun")

        # woty
        woty = d.woty
        self.assertEqual(woty, 9)

    def test_operations(self):
        """
        add, iadd, sub, rsub
        """
        d1 = Date(2024, 1, 3)
        d2 = Date(2024, 4, 3)
        d3 = datetime.date(2024,4,3)
        d4 = datetime.datetime(2024,4,3)
        dur = Duration(m=3)
        rd = relativedelta(months=3)
        td = datetime.timedelta(days=91)
        str_d1 = "1/3/24"
        str_dur = "+3m"
        int_dur = 91

        # add
        self.assertRaises(TypeError, lambda: d1 + d2)
        self.assertRaises(TypeError, lambda: d1 + str_d1)
        self.assertEqual(d1 + str_dur, d2)
        self.assertEqual(d1 + dur, d2)
        self.assertEqual(d1 + int_dur, d2)
        self.assertEqual(d1 + rd, d2)
        self.assertEqual(d1 + td, d2)
        self.assertEqual(d3-d2,Duration())

        self.assertRaises(TypeError,lambda: d1+3.0)
        self.assertRaises(TypeError,lambda: 3.0-d1)

        # # sub
        dur91d = Duration(y=0,m=3,w=0,d=0)
        self.assertEqual(d2 - d1, dur91d)
        self.assertEqual(d2 - dur, d1)
        self.assertEqual(d2 - str_d1, dur91d)
        self.assertEqual(d2 - str_dur, d1)
        self.assertEqual(d2 - int_dur, d1)
        self.assertEqual(d2 - rd, d1)
        self.assertEqual(d2 - td, d1)
        self.assertEqual(d2 - d3,Duration(days=0))
        self.assertEqual(d2-d2,d3-d2)
        self.assertEqual(d2-d2,d4-d2)
        self.assertEqual(d2-d2,d2-d4)

        self.assertRaises(TypeError,lambda: dur-d1)
        self.assertRaises(TypeError,lambda: 3.0-d1)
        self.assertRaises(TypeError,lambda: d1-3.0)
        self.assertRaises(TypeError,lambda: d2-3.0)

        # iadd
        _d1 = d1
        try:
            _d1 += d2
            assert False
        except TypeError:
            assert True

        _d1 = d1
        _d1 += dur
        self.assertEqual(_d1, d2)

        _d1 = d1
        try:
            _d1 += str_d1
            assert False
        except TypeError:
            assert True

        _d1 = d1
        _d1 += int_dur

        self.assertEqual(_d1, d2)

        _d1 = d1
        _d1 += rd
        self.assertEqual(_d1, d2)

        _d1 = d1
        _d1 += td
        self.assertEqual(_d1, d2)

        # isub
        _d2 = d2
        _d2 -= d1
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= str_d1
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= dur
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= str_dur
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= int_dur
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= td
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= rd
        self.assertEqual(_d2, d1)

    def test_repr(self):
        '''
            test the repr of date
        '''
        a = Date(2024, 12, 5)
        rs = repr(a)
        self.assertEqual(rs,'Date("2024-12-05")')
        

if __name__ == "__main__":
    unittest.main()
