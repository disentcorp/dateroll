import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
from unittest import expectedFailure

from dateroll.calendars.calendars import Calendars


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename_base = (
            pathlib.Path(tempfile.gettempdir())
            / f"dateroll.testing.{uuid.uuid4()}.cals"
        )
        cls.cals = Calendars(home=cls.filename_base)

    @classmethod
    def tearDownClass(self):
        filename = str(self.filename_base)
        os.remove(filename)

    def test_keys(self):
        """
        ensure the keys method is returing a list-like object
        """
        k = self.cals.keys()
        assert isinstance(k, list)

    @expectedFailure
    def test_tests1(self):
        self.cals["aaaa"] = []

    @expectedFailure
    def test_tests2(self):
        self.cals["aa"] = []

    @expectedFailure
    def test_tests3(self):
        self.self.cals["AA"] = []

    def test_tests4(self):
        self.cals["AA"] = []

    def test_tests5(self):
        del self.cals["AA"]

    def test_tests6(self):
        self.cals["AA"] = ()

    @expectedFailure
    def test_tests7(self):
        self.cals["AA"] = (1,)

    @expectedFailure
    def test_tests8(self):
        self.cals["AA"] = (1,)

    def test_tests9(self):
        dates = [datetime.date.today()]
        self.cals["BBB"] = dates
        assert self.cals["BBB"] == dates


if __name__ == "__main__":
    unittest.main()
