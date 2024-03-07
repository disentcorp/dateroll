import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
from unittest import expectedFailure
import dateroll.calendars.calendars as calendars
import code

from dateroll import ddh,cals
import dateroll


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
        a = ddh('12/4/24',convention='MDY')
        b = ddh('04/12/24',convention='DMY')
        c = ddh('20241204',convention='YMD')
        
        self.assertEqual(a,b)
        self.assertEqual(a,c)
        self.assertEqual(a,b)

        # RESET CONVENTION
        ddh.convention = 'MDY'

class TestsPracticalExamples(unittest.TestCase):
    def testNothing(self):
        """
        empty string
        """
        self.assertRaises(dateroll.parser.parsers.ParserStringsError,lambda: ddh(""))

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
