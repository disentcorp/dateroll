import datetime
import io
import re
import sys
import unittest

from dateroll.date.date import Date
from dateroll.ddh.ddh import ddh
from dateroll.duration.duration import Duration
from dateroll.schedule.schedule import Schedule
from dateroll.settings import settings


class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_dates_forward(self):
        """
        test dates which give a range of dates and step>0
        """

        start = Date(2023, 1, 1)
        stop = Date(2023, 2, 1)
        step = Duration(bd=1)
        sch = Schedule(start, stop, step)
        dts = sch.dates
        # convert into datetime
        dts = [d.datetime for d in dts]
        expected = [
            datetime.datetime(2023, 1, 1, 0, 0),
            datetime.datetime(2023, 1, 2, 0, 0),
            datetime.datetime(2023, 1, 3, 0, 0),
            datetime.datetime(2023, 1, 4, 0, 0),
            datetime.datetime(2023, 1, 5, 0, 0),
            datetime.datetime(2023, 1, 6, 0, 0),
            datetime.datetime(2023, 1, 9, 0, 0),
            datetime.datetime(2023, 1, 10, 0, 0),
            datetime.datetime(2023, 1, 11, 0, 0),
            datetime.datetime(2023, 1, 12, 0, 0),
            datetime.datetime(2023, 1, 13, 0, 0),
            datetime.datetime(2023, 1, 16, 0, 0),
            datetime.datetime(2023, 1, 17, 0, 0),
            datetime.datetime(2023, 1, 18, 0, 0),
            datetime.datetime(2023, 1, 19, 0, 0),
            datetime.datetime(2023, 1, 20, 0, 0),
            datetime.datetime(2023, 1, 23, 0, 0),
            datetime.datetime(2023, 1, 24, 0, 0),
            datetime.datetime(2023, 1, 25, 0, 0),
            datetime.datetime(2023, 1, 26, 0, 0),
            datetime.datetime(2023, 1, 27, 0, 0),
            datetime.datetime(2023, 1, 30, 0, 0),
            datetime.datetime(2023, 1, 31, 0, 0),
            datetime.datetime(2023, 2, 1, 0, 0),
        ]
        self.assertEqual(dts, expected)
        settings.convention = "MDY"
        Ssch = Schedule.from_string("01012023,02012023,1bd")
        self.assertEqual(Ssch.dates, sch.dates)

    def test_dates_backward(self):
        """
        test dates when step<0
        """
        start = Date(2023, 1, 1)
        stop = Date(2023, 2, 1)
        step = Duration(bd=-1)
        sch = Schedule(start, stop, step)
        dts = sch.dates
        # convert into datetime
        dts = [d.datetime for d in dts]
        expected = [
            datetime.datetime(2023, 1, 1, 0, 0),
            datetime.datetime(2023, 1, 2, 0, 0),
            datetime.datetime(2023, 1, 3, 0, 0),
            datetime.datetime(2023, 1, 4, 0, 0),
            datetime.datetime(2023, 1, 5, 0, 0),
            datetime.datetime(2023, 1, 6, 0, 0),
            datetime.datetime(2023, 1, 9, 0, 0),
            datetime.datetime(2023, 1, 10, 0, 0),
            datetime.datetime(2023, 1, 11, 0, 0),
            datetime.datetime(2023, 1, 12, 0, 0),
            datetime.datetime(2023, 1, 13, 0, 0),
            datetime.datetime(2023, 1, 16, 0, 0),
            datetime.datetime(2023, 1, 17, 0, 0),
            datetime.datetime(2023, 1, 18, 0, 0),
            datetime.datetime(2023, 1, 19, 0, 0),
            datetime.datetime(2023, 1, 20, 0, 0),
            datetime.datetime(2023, 1, 23, 0, 0),
            datetime.datetime(2023, 1, 24, 0, 0),
            datetime.datetime(2023, 1, 25, 0, 0),
            datetime.datetime(2023, 1, 26, 0, 0),
            datetime.datetime(2023, 1, 27, 0, 0),
            datetime.datetime(2023, 1, 30, 0, 0),
            datetime.datetime(2023, 1, 31, 0, 0),
            datetime.datetime(2023, 2, 1, 0, 0),
        ]

        self.assertEqual(dts, expected)
        # string
        settings.convention = "MDY"
        ssch = Schedule.from_string("01012023,02012023,-1bd")
        sdts = ssch.dates
        sdts = [d.datetime for d in sdts]
        self.assertEqual(sdts, expected)

    def test_cal(self):
        """
        catch the print statement of cal property
        """
        settings.convention = "MDY"
        start = Date(2023, 1, 1)
        stop = Date(2023, 2, 1)
        step = Duration(bd=-1)
        sch = Schedule(start, stop, step)
        capt = io.StringIO()
        sys.stdout = capt
        sch.cal

        sys.stdout = sys.__stdout__

        txt = capt.getvalue().strip()

        self.assertGreater(len(txt), 500)
        settings.convention = "MDY"
        Ssch = Schedule.from_string("01012023,02012023,-1bd")
        capt = io.StringIO()
        sys.stdout = capt
        Ssch.cal

        sys.stdout = sys.__stdout__

        Stxt = capt.getvalue().strip()

        Stxt = re.sub(r"\s+", "", Stxt)
        txt = re.sub(r"\s+", "", txt)
        # self.assertEqual(len(Stxt),len(txt))
        self.assertEqual(Stxt, txt)

    def test_toString(self):
        """
        to_string
        """
        orig = settings.convention
        settings.convention = "YMD"
        schedule = ddh("20230101,20230201,1bd|NYuWE")
        self.assertEqual(schedule.to_string(), "20230101,20230201,1bd|NYuWE")
        sch = Schedule(Date(2023, 1, 1), Date(2023, 2, 1), Duration(bd=1))
        with self.assertRaises(NotImplementedError):
            sch.to_string()
        settings.convention = "MDY"
        Ssch = Schedule.from_string("01012023,02012023,1bd|NYuWE")
        with self.assertRaises(NotImplementedError):
            Ssch.to_string()
        settings.convention = orig

    def test_split(self):
        """
        test split properties which return dataframe with columns of start,stop, and step
        """
        sch = Schedule(Date(2023, 1, 1), Date(2023, 2, 1), Duration(bd=3))
        df = sch.split
        start = df.loc[0, "start"]
        stop = df.loc[0, "stop"]
        step = df.loc[0, "step"]
        self.assertEqual(stop, start + ddh(step))
        settings.convention = "MDY"
        Ssch = Schedule.from_string("01012023,02012023,3bd")
        self.assertTrue(df.equals(Ssch.split))

    def test_split_bond(self):
        """
        test split bonds
        """
        sch = Schedule(Date(2023, 1, 1), Date(2023, 2, 1), Duration(bd=3))
        df = sch.split_bond
        df = df.dropna()
        starts = [i for i in df["starts"] if i is not None]
        ends = [i for i in df["ends"] if i is not None]
        days = [i for i in df["days"] if i is not None]
        ends_expected = [start + Duration(days=day) for start, day in zip(starts, days)]
        self.assertEqual(ends, ends_expected)
        settings.convention = "MDY"
        Ssch = Schedule.from_string("01012023,02012023,3bd")
        self.assertTrue(df.equals(Ssch.split_bond.dropna()))

    def test_repr(self):
        sch = Schedule(Date(2023, 1, 1), Date(2023, 2, 1), Duration(bd=3))
        repr(sch)
        settings.convention = "MDY"
        Ssch = Schedule.from_string("01012023,02012023,3bd")
        self.assertEqual(repr(sch), repr(Ssch))

    def test_str(self):
        sch = Schedule(Date(2023, 1, 1), Date(2023, 2, 1), Duration(bd=3))
        self.assertIsInstance(sch.__str__(), str)
        settings.convention = "MDY"
        Ssch = Schedule.from_string("01012023,02012023,3bd")
        self.assertEqual(sch.__str__(), Ssch.__str__())

        with self.assertRaises(TypeError):
            Schedule.from_string(10)

    def test_badparts(self):
        from dateroll.parser.parsers import ParserStringsError

        # bad start
        self.assertRaises(TypeError, lambda: ddh("3m,t+5y,1m"))
        # bad stop
        self.assertRaises(ParserStringsError, lambda: ddh("t,5v,1m"))
        # bad end
        self.assertRaises(TypeError, lambda: ddh("t,t+5y,t"))

    def test_getitem(self):
        """
        test getitem which gets int, str, or slice
        """
        d1 = ddh("03012022")
        d2 = ddh("03202022")
        dur = Duration(bd=1)
        ds = Schedule(d1, d2, dur)
        self.assertEqual(ds[-1], d2)
        self.assertEqual(ds["03032022"], ddh("03032022"))
        with self.assertRaises(KeyError):
            ds["01012022"]
        settings.ie = "[]"

        self.assertEqual(ds["03012022":"03112022"], ddh("03012022,03112022,1bd").list)
        with self.assertRaises(TypeError):
            ds[datetime.datetime(2022, 3, 3)]

        # reset settings
        settings.ie = "(]"

    def test_iter(self):
        """
        test getiter
        """
        d1 = ddh("03012022")
        d2 = ddh("03102022")
        dur = Duration(bd=1)
        ds = Schedule(d1, d2, dur)

        ls = []
        for d in ds:
            ls.append(d)

        self.assertTrue(ls, ds.list)

    def test_contains(self):
        """
        test contains which returns boolean value True or False
        """

        d1 = ddh("03012022")
        d2 = ddh("03102022")
        dur = Duration(bd=1)
        ds = Schedule(d1, d2, dur)

        self.assertTrue(d1 in ds)
        self.assertTrue(d1.datetime in ds)
        self.assertFalse(ddh("01012022") in ds)


if __name__ == "__main__":
    unittest.main()
