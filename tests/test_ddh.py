import datetime
import unittest
from zoneinfo import ZoneInfo
from tzlocal import get_localzone

import dateroll
import dateroll.date.date as dateModule
import dateroll.duration.duration as durationModule
import dateroll.schedule.schedule as scheduleModule
from dateroll import ddh
from dateroll.settings import settings

# import dateroll.duration.duration as durationModule

LOCAL_ZONE = get_localzone()

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

        d1 = dateModule.Date(2023, 3, 1)
        d1 += "1d"

        d2 = d1 + "1d"
        self.assertEqual(d1, dateModule.Date(2023, 3, 2))
        self.assertEqual(d2, dateModule.Date(2023, 3, 3))

    def testDurationMathWithStr(self):
        """
        str->Duration + str
        str->Duration += str
        str + str->Duration

        """
        dur1 = durationModule.Duration(years=1)
        dur1 += "1bd"
        self.assertEqual(
            dur1,
            durationModule.Duration(
                years=1, months=0, days=0, modified=False, bd=1.0, cals="WE"
            ),
        )
        dur2 = dur1 + "1bd"
        self.assertEqual(
            dur2,
            durationModule.Duration(
                years=1, months=0, days=0, modified=False, bd=2.0, cals="WE"
            ),
        )

    def testDateMathAdd(self):
        """
        str->Date + str->Date
        str->Date + str->Duration
        str->Duration + str->Date
        str->Duration + str->Duration
        """

        d1 = dateModule.Date(2023, 3, 1)
        with self.assertRaises(TypeError):
            d2 = d1 + "02012023"

    def testDateMathSub(self):
        """
        str->Date - str->Date
        str->Date - str->Duration
        str->Duration - str->Date
        str->Duration - str->Duration
        """
        d1 = dateModule.Date(2023, 3, 1)

        d2 = d1 - "02012023"
        self.assertEqual(d2.to_string(), "+1m")

    def testSchedule(self):
        """
        str->Schedule (1bd,1d,1w,1m,1y)
        """

        
        #
        start = dateModule.Date(2023, 1, 3)
        end = dateModule.Date(2023, 6, 3)
        
        self.assertEqual(
            ddh("01032023,06032023,1bd").list,
            scheduleModule.Schedule(start, end, durationModule.Duration(bd=1)).list,
        )
        self.assertEqual(
            ddh("01032023,06032023,1d").list,
            scheduleModule.Schedule(start, end, durationModule.Duration(days=1)).list,
        )
        self.assertEqual(
            ddh("01032023,06032023,1w").list,
            scheduleModule.Schedule(start, end, durationModule.Duration(weeks=1)).list,
        )
        self.assertEqual(
            ddh("01032023,06032023,1m").list,
            scheduleModule.Schedule(start, end, durationModule.Duration(months=1)).list,
        )
        self.assertEqual(
            ddh("01032023,06032023,1y").list,
            scheduleModule.Schedule(start, end, durationModule.Duration(years=1)).list,
        )

    def testPurge(self):
        """
        purge all
        """
        ddh.purge_all()
        base_cals = sorted(["FED", "ECB","EU", "LN", "WE", "ALL", "BR", "NY"])
        self.assertEqual(sorted(ddh.hols.keys()), base_cals)

    def testConvention(self):
        original = settings.convention
        try:
            # american
            settings.convention = "MDY"
            _a = dateroll.Date(year=2024, month=12, day=1)
            a = ddh("12/1/24")
            self.assertEqual(_a, a)
            # european
            settings.convention = "DMY"
            _b = dateroll.Date(year=2023, month=3, day=23)
            b = ddh("23/3/23")
            self.assertEqual(_b, b)
            # international
            settings.convention = "YMD"
            _c = dateroll.Date(year=2022, month=10, day=5)
            c = ddh("20221005")
            self.assertEqual(_c, c)
        finally:
            # back to original
            settings.convention = original

    def testLocalCOnvention(self):
        """
        test the local convention, with statement converts convention and returns to the original convention
        """

        # YMD
        with ddh.YMD():
            self.assertEqual(ddh("20230101"), dateModule.Date(2023, 1, 1))
            self.assertEqual(settings.convention, "YMD")
        self.assertEqual(settings.convention, "MDY")

        # DMY
        with ddh.DMY():
            self.assertEqual(ddh("01022023"), dateModule.Date(2023, 2, 1))
            self.assertEqual(settings.convention, "DMY")
        self.assertEqual(settings.convention, "MDY")

        # MDY
        with ddh.MDY():
            self.assertEqual(ddh("02012023"), dateModule.Date(2023, 2, 1))
            self.assertEqual(settings.convention, "MDY")
        self.assertEqual(settings.convention, "MDY")


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

        assert ddh("5/5/05").datetime == datetime.datetime(2005, 5, 5,0,0).astimezone(LOCAL_ZONE)

    def testDuration(self):
        """
        test for duration strings
        """

    def testSchedule1(self):
        """
        test for schedule strings
        """
        try:
            settings.convention = "YMD"
            result = ddh("t").datetime
        finally:
            settings.convention = "MDY"
        expected = datetime.datetime.now(LOCAL_ZONE)
        
        assert result.date() == expected.date()
        assert result.hour == expected.hour and result.minute == expected.minute and result.tzinfo==expected.tzinfo

    def test_durationLike(self):
        """
        pass durationlike into ddh
        """

        x = ddh(datetime.timedelta(days=10))
        self.assertEqual(
            x,
            dateroll.Duration(years=0, months=0, days=10, h=0, min=0, s=0, us=0, modified=False),
        )

    def test_badObj(self):
        """
        pass bad instace to raise TypeError
        """

        with self.assertRaises(TypeError):
            ddh(10)

    def test_bds(self):
        """
        when string has years and bds with a negative sign
        """

        x = ddh("-1y2q3m4w5d6BD")
        self.assertEqual(
            x,
            durationModule.Duration(
                years=-1, months=-9, days=-33, modified=False, bd=-6.0, cals="WE"
            ),
        )


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
