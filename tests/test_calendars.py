import datetime
import os
import pathlib
import sys
import tempfile
import unittest
import uuid
from io import StringIO
from unittest import expectedFailure

import dateroll
from dateroll.calendars.calendars import Calendars, DateSet, Drawer
from dateroll.ddh.ddh import ddh


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
        ensure the keys method is returning a list-like object
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
        self.cals.AA = []
        del self.cals["AA"]
        self.cals["AA"] = []

    def test_tests5(self):
        if "AA" in self.cals:
            del self.cals["AA"]
        else:
            ...

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
        back_out = list(self.cals["BBB"])

        self.assertEqual(dates, back_out)

    def test_exitReturnTrue(self):
        """
        context manager fails in the __exit__
        """
        cals = Calendars()
        with Drawer(cals) as db:
            try:
                db.update("Hello")
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
        self.assertEqual(exc_type.__name__, "ValueError")

    def test_contains(self):
        """
        test contains has a k in its dict keys
        """
        cals = Calendars()
        cond = "FED" in cals
        self.assertTrue(cond)

    def test_setitemkeyNonString(self):
        """
        when setitem key is Non String should raise error
        """
        with self.assertRaises(Exception) as context:
            self.cals[30] = []
        self.assertEqual(str(context.exception), "Cal name must be string (got int)")

    def test_setitemValWrong(self):
        """
        when setitem val is not list,tuple,set
        """
        with self.assertRaises(Exception) as context:
            self.cals["AA"] = 10

    def test_seitemValDate(self):
        """
        when we assign the list of datetime.date
        """
        self.cals["AA"] = [dateroll.Date(2023, 1, 1)]
        self.assertTrue(dateroll.Date(2023, 1, 1) in self.cals["AA"])

    def test_seitemValDateTime(self):
        """
        when we assign the list of datetime.datetime
        """
        del self.cals["AA"]
        self.cals["AA"] = [datetime.datetime(2023, 1, 1)]
        self.assertTrue(dateroll.Date(2023, 1, 1) in self.cals["AA"])
        del self.cals["AA"]
        with self.assertRaises(ValueError):
            # when date is before 2/29/1824 will raise error

            self.cals["AA"] = [datetime.datetime(1823, 12, 12)]

    def test_seitemValDateClass(self):
        """
        when we assign the list of Date Class
        """
        x = dateroll.Date(2020, 1, 1)
        self.cals["AB"] = [x]

        self.assertTrue(dateroll.Date(2020, 1, 1) in self.cals["AB"])

    def test_setitemValWrong2(self):
        """
        when we assign the val which is not date related
        """
        if "AA" in self.cals:
            del self.cals["AA"]
        with self.assertRaises(Exception) as context:
            self.cals["AA"] = ["20230101"]
        self.assertEqual(
            str(context.exception),
            "All cal dates must be of dateroll.Date or datetime.date{time} (got str)",
        )

    def test_setitemKeyExistsAlready(self):
        """
        when the key already exists, it wont set the new value
        """
        self.cals["EEE"] = []
        with self.assertRaises(Exception) as cm:
            self.cals["EEE"] = [dateroll.Date(2024, 2, 1)]

    def test_getattrNotHashHome(self):
        """
        test get calendar via getattr
        """
        self.cals.DDD = [datetime.date(1984, 7, 2)]
        x = self.cals.DDD
        self.assertIsInstance(x, DateSet)
        self.assertTrue(len(x) > 0)

    def test_getattrHashHome(self):
        """
        when the key of getattr in (hash,home)
        """
        cals = Calendars()
        x = cals.__getattr__("home")
        # dont want to put home/batu in the result
        x = x.split("dateroll")[-1]
        self.assertEqual(x, "/calendars/holiday_lists")

    def test_delitem(self):
        """
        test delitem of calendar
        """
        print(self.cals)
        self.cals["AA"] = [dateroll.Date(2023, 2, 1)]
        print(self.cals)
        import time

        time.sleep(0.5)
        self.assertTrue("AA" in self.cals)
        del self.cals["AA"]
        self.assertFalse("AA" in self.cals)

    def test_repr(self):
        """
        test __repr__ of calendar
        """

        self.assertTrue(len(repr(self.cals)) > 300)

    def test_copy(self):
        """
        the copy of the db should be as same as cals
        """
        cals = Calendars()
        copy_db = cals.copy()
        self.assertTrue(copy_db, self.cals.db)

    def test_info(self):
        """
        test the info of calendar
        """
        cals = Calendars()
        capt = StringIO()
        sys.stdout = capt

        cals.info
        sys.stdout = sys.__stdout__

        printed_output = capt.getvalue()
        expected_output = "name  |  #dates|min date    |max date    \n------|--------|------------|------------\nFED   |    4556|1824-01-01  |2223-12-25  \nECB   |    2400|1824-01-01  |2223-12-26  \nLN    |    3951|1824-01-01  |2223-12-26  \nWE    |   41742|1824-02-29  |2224-02-28  \nALL   |  146097|1824-02-29  |2224-02-28  \nBR    |    3586|1824-01-01  |2223-12-25  \nNY    |    4556|1824-01-01  |2223-12-25  \n"
        self.assertTrue(printed_output, expected_output)

    def test_clear(self):
        """
        clear the db
        """

        self.cals.BOB = []

        self.assertTrue(len(self.cals.db) != 0)
        self.cals.clear()
        self.assertTrue(len(self.cals.db) == 0)

    def test_emptyDBInfo(self):
        """
        clear the db and show the info
        """

        capt = StringIO()
        sys.stdout = capt

        self.cals.info
        sys.stdout = sys.__stdout__

        printed_output = capt.getvalue()
        expected_output = "name  |  #dates|min date    |max date    \n------|--------|------------|------------\nFED   |    4556|1824-01-01  |2223-12-25  \nECB   |    2400|1824-01-01  |2223-12-26  \nLN    |    3951|1824-01-01  |2223-12-26  \nWE    |   41742|1824-02-29  |2224-02-28  \nALL   |  146097|1824-02-29  |2224-02-28  \nBR    |    3586|1824-01-01  |2223-12-25  \nNY    |    4556|1824-01-01  |2223-12-25  \n"
        self.assertTrue(printed_output, expected_output)
        self.cals.clear()
        self.cals["AC"] = []
        capt = StringIO()
        sys.stdout = capt

        self.cals.info
        sys.stdout = sys.__stdout__
        printed_output_empty = capt.getvalue()
        expected_output_empty = "name  |  #dates|min date    |max date    \n------|--------|------------|------------\nAC    |       0|None        |None        \n"
        self.assertTrue(printed_output_empty, expected_output_empty)

    def test_dateset(self):
        """
        test adding,extend
        """
        # test add
        dt = [datetime.datetime(2023, 1, 1), datetime.datetime(2023, 1, 3)]
        dateset = DateSet(dt)
        dateset.add(datetime.datetime(2023, 1, 5))
        self.assertTrue(dateset._data[datetime.date(2023, 1, 5)])

        # extend
        with self.assertRaises(TypeError):
            dateset.extend("20230101")
        dateset.extend([datetime.date(2023, 2, 1), datetime.date(2023, 2, 3)])
        self.assertTrue(datetime.date(2023, 2, 1) in dateset)
        self.assertTrue(datetime.datetime(2023, 2, 1) in dateset)

        # repr
        repr(dateset)
        dateset = DateSet(dt, name="dates")
        dateset.add(datetime.datetime(2023, 1, 5))
        self.assertTrue(dateset._data[datetime.date(2023, 1, 5)])

    def test_delattr(self):
        """
        test delattr where some attributes are protected to delete
        """

        # a test deletion of a calendar via delattr
        self.cals.CCC = [datetime.date(1984, 7, 2)]
        test_func = lambda: hasattr(self.cals, "CCC")
        self.assertTrue(test_func())
        del self.cals.CCC
        self.assertFalse(test_func())

        # b test deletion of an attribute (bad actually, just calling super) - back it up!

        backup_home = self.cals.home
        test_func = lambda: hasattr(self.cals, "home")
        self.assertTrue(test_func())
        del self.cals.home
        self.assertFalse(test_func())

        # restore backup
        self.cals.home = backup_home
        self.assertTrue(test_func())

    def test_corrupt_cache(self):
        """
        corrupt the calendar cache
        """
        cals = Calendars()
        # corrupt file
        with open(cals.home, "wb") as f:
            f.seek(10)
            f.write(b"corrupt")

        import io

        capt = io.StringIO()
        sys.stdout = capt
        cals.keys()
        sys.stdout = sys.__stdout__
        txt = capt.getvalue().strip()
        self.assertTrue("Cache is corrupted" in txt)

    def test_getitem(self):
        """
        Dateset, it receives a slice, if not raise typeError
        """

        ds = ddh("02012023,12312023,1bd").list

        dset = DateSet(ds)
        self.assertEqual(dset["05012023":], ddh("05012023,12312023,1bd").list)
        self.assertEqual(dset[:"03012023"], ddh("02012023,03012023,1bd").list)

        ds_compare = [l for l in ds if l >= ddh("04012023") and l <= ddh("06012023")]
        self.assertEqual(dset["04012023":"06012023"], ds_compare)
        self.assertEqual(dset[:], ds)
        self.assertRaises(Exception, dset["05012023":"06012023":"2bd"])
        with self.assertRaises(TypeError):
            dset[10]

        self.assertEqual(dset[ddh("05012023") :], ddh("05012023,12312023,1bd").list)
        with self.assertRaises(Exception):
            dset[10:]
        # when step is not None
        with self.assertRaises(Exception):
            dset[::"1bd"]

    def test_str(self):
        """
        test str
        """

        cal = Calendars()
        cal["AA"] = []
        str(cal)


if __name__ == "__main__":
    unittest.main()
