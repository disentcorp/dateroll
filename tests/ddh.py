import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
from unittest import expectedFailure

from dateroll import ddh

class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ...

    @classmethod
    def tearDownClass(self):
        ...

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

if __name__ == "__main__":
    unittest.main()
