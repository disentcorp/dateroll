import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
from unittest import expectedFailure
import dateroll.calendars.calendars as calendars
import code

from dateroll.settings import settings
from dateroll import ddh,cals
import dateroll
# import dateroll.duration.duration as durationModule


class TestDDH(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def testDateMathWithStr(self):
        """
        str->Date + str
        str->Date += str
        str + str->Date
        """

    def testDurationMathWithStr(self):
        """
        str->Duration + str
        str->Duration += str
        str + str->Duration

        """

    def testDateMathAdd(self):
        """
        str->Date + str->Date
        str->Date + str->Duration
        str->Duration + str->Date
        str->Duration + str->Duration
        """

    def testDateMathSub(self):
        """
        str->Date - str->Date
        str->Date - str->Duration
        str->Duration - str->Date
        str->Duration - str->Duration
        """

    def testSchedule(self):
        """
        str->Schedule (1bd,1d,1w,1m,1y)
        """

    def testPurge(self):
        '''
        purge all
        '''
        ddh.purge_all()
        base_cals = sorted(['FED', 'ECB', 'LN', 'WE', 'ALL', 'BR', 'NY'])
        self.assertEqual(sorted(cals.keys()),base_cals)

    def testConvention(self):
        original = settings.convention
        try: 
            # american
            settings.convention = 'MDY'
            _a = dateroll.Date(year=2024,month=12,day=1)
            a = ddh('12/1/24')
            self.assertEqual(_a,a)
            #european
            settings.convention = 'DMY'
            _b = dateroll.Date(year=2023,month=3,day=23)
            b = ddh('23/3/23')
            self.assertEqual(_b,b)
            #international
            settings.convention = 'YMD'
            _c = dateroll.Date(year=2022,month=10,day=5)
            c = ddh('20221005')      
            self.assertEqual(_c,c)
        finally:
            # back to original
            settings.convention = original

class TestsPracticalExamples(unittest.TestCase):
    def testNothing(self):
        """
        empty string
        """
        with self.assertRaises(dateroll.parser.parsers.ParserStringsError):
            ddh("")

    def testDate(self):
        """
        test for date strings
        """
        assert ddh("t") == datetime.date.today()
        assert ddh("5/5/05") == datetime.date(2005, 5, 5)

    def testDuration(self):
        """
        test for duration strings
        """

    def testSchedule1(self):
        """
        test for schedule strings
        """
        assert ddh("t") == datetime.date.today()

    def test_durationLike(self):
        '''
            pass durationlike into ddh
        '''
        x = ddh(datetime.timedelta(days=10))
        self.assertEqual(x,dateroll.Duration(years=0, months=0, days=10, modified=False, debug=False))
    
    def test_badObj(self):
        '''
            pass bad instace to rayse TypeError
        '''
        
        with self.assertRaises(TypeError):
            ddh(10)
if __name__ == "__main__":
    unittest.main()

    # x = "2/24/24+3bd|WEuNY"
    # print(x, "ddh=", ddh(x))
    # # print("answer:",ddh('3/1/24'))
    # # print("answer:",ddh('t'))
    # # print("answer:",ddh('-3m|NY'))
    # # print("answer:",ddh('9m|NY+ -11m'))
    # # print("answer:",ddh('9m|NY + 11m0bd|EU'))
    # # print("answer:",ddh('-6m7y2d5q8w|NYuEUuWEuBRuMXuARuCONZ/MF'))
    # # print("answer:",ddh('9m+6m7y2d5q8w|NYuEUuWEuBRuMXuARuCONZ/MF'))
    # # print("answer:",ddh('t+1bd'))
    # # print("answer:",ddh('t-5bd'))
    # # print("answer:",ddh('t-0bd'))
    # # print("answer:",ddh('t+3m'))
