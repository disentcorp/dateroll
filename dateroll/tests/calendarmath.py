import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
from unittest import expectedFailure

from dateroll.calendars.calendarmath import CalendarMath


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename_base = (
            pathlib.Path(tempfile.gettempdir())
            / f"dateroll.testing.calmath.{uuid.uuid4()}"
        )
        cls.cals = CalendarMath(home=cls.filename_base)

    @classmethod
    def tearDownClass(self):
        filename = str(self.filename_base)
        os.remove(filename)

    def test_addbd(self):
        """
        test add business days

        with mod:
            non-hol+0bd|WE
            hol+0bd|WE
            non-hol+0bd|WEuNY
            hol+0bd|WEuNY
            hol+1000bd
            nonhol+1000bd
        without mod:
            non-hol+0bd|WE
            hol+0bd|WE
            non-hol+0bd|WEuNY
            hol+0bd|WEuNY
            hol+1000bd
            nonhol+1000bd

        measure perf, put a threshold

        """

    def test_subbd(self):
        """
        just 1 or 2 from add, uses same mechanics

        """

    def test_isbd(self):
        """
        test is business day

        test a holiday is bd on non-union
        test a holiday in a is bd on union of a u b
        test a holiday in b is bd on union of a u b u c
        test nonholiday is not bd on non-union
        test nonholiday is not bd on union

        measure perf, put a threshold
        """

    def test_diffbd(self):
        """

        a - non-bd
        b - non-bd
        x - bd
        y - bd

        (a,b)
        (a,b]
        [a,b]
        [a,b)

        (a,y)
        (a,y]
        [a,y]
        [a,y)

        (x,b)
        (x,b]
        [x,b]
        [x,b)

        (x,y)
        (x,y]
        [x,y]
        [x,y)

        measure performance, put a threshold

        """

    def test_nextbd(self):
        """

        w/o mod

        from non-bd to bd on 1 cal
        from non-bd to bd on 2 cal union
        from bd to bd on 1 cal
        from bd to bd on 2 cal union

        w/ mod

        from non-bd to bd on 1 cal
        from non-bd to bd on 2 cal union
        from bd to bd on 1 cal
        from bd to bd on 2 cal union

        measure performance, put a threshold
        """

    def test_prevbd(self):
        """

        w/o mod

        from non-bd to bd on 1 cal
        from non-bd to bd on 2 cal union
        from bd to bd on 1 cal
        from bd to bd on 2 cal union

        w/ mod

        from non-bd to bd on 1 cal
        from non-bd to bd on 2 cal union
        from bd to bd on 1 cal
        from bd to bd on 2 cal union

        measure performance, put a threshold
        """


if __name__ == "__main__":
    unittest.main()
