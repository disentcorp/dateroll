import datetime
import sys
import unittest
from io import StringIO
import json

import dateutil.relativedelta

from dateroll import Date, Duration, ddh
from dateroll.parser import parsers
from dateroll.utils import ParserStringsError
from dateroll.settings import settings

EXPECTED_DAY_COUNT_PATH = lambda:"tests/test_data/ql_data.json"

class TestDuration(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_from_string(self):
        """
        good string bad string
        """
        x = Duration.from_string("+3m|NY")
        self.assertIsInstance(x, Duration)
        self.assertRaises(
            ParserStringsError, lambda: Duration.from_string("garbage")
        )
        self.assertRaises(TypeError, lambda: Duration.from_string(3))

    def test_from_rd(self):
        """
        good rd non-rd
        """
        rd = dateutil.relativedelta.relativedelta(years=3, months=2, weeks=1, days=1)
        x = Duration.from_relativedelta(rd)
        self.assertIsInstance(x, Duration)
        self.assertRaises(TypeError, lambda: Duration.from_relativedelta("garbage"))

    def test_from_td(self):
        """
        good td non-td
        """
        td = datetime.timedelta(weeks=1, days=12)
        x = Duration.from_timedelta(td)
        y = Duration.from_relativedelta(td)
        self.assertIsInstance(x, Duration)
        self.assertIsInstance(y, Duration)
        self.assertRaises(TypeError, lambda: Duration.from_timedelta("garbage"))

    def test_period_units(self):
        """
        properties
        """

        y, m, w, d, bd = 1, 2, 3, 4, 5
        dur1 = Duration(y=y, m=m, w=w, d=d, bd=bd)
        dur2 = Duration()

        # year
        self.assertEqual(dur1.y, y)
        self.assertEqual(dur1.Y, y)
        self.assertEqual(dur1.year, y)
        self.assertEqual(dur1.years, y)

        # month
        self.assertEqual(dur1.m, m)
        self.assertEqual(dur1.M, m)
        self.assertEqual(dur1.month, m)
        self.assertEqual(dur1.months, m)

        # day
        self.assertEqual(dur1.d, d + 7 * w)
        self.assertEqual(dur1.D, d + 7 * w)
        self.assertEqual(dur1.day, d + 7 * w)
        self.assertEqual(dur1.days, d + 7 * w)

        # bd
        self.assertEqual(dur1.bd, bd)
        self.assertIsNone(dur2.bd)

    def test_roll_no_roll(self):
        """
        test each perm, and bad versions, and neg
        """
        dur = Duration(bd=1, modified=True)

        dur = Duration(bd=-3)

    def test_cals(self):
        cals1 = ["WE", "NY"]
        cals2 = "WE"
        cals3 = "WEuNY"
        good = ("NY", "WE")

        cals4 = ["BAD", "NY"]
        cals5 = "BAD"
        cals6 = "NYuBAD"

        self.assertEqual(Duration(d=0, cals=cals1).cals, good)
        self.assertEqual(Duration(d=0, cals=cals2).cals, ("WE",))
        self.assertEqual(Duration(d=0, cals=cals3).cals, good)

        self.assertRaises(ValueError, lambda: Duration(d=0, cals=cals4))
        self.assertRaises(ValueError, lambda: Duration(d=0, cals=cals5))
        self.assertRaises(ValueError, lambda: Duration(d=0, cals=cals6))

    def test_bdadj(self):
        """
        test 0bd and >1bd and <1bd
        for each one of valid rolls
        """

        # zero day adjustments

        # sun+0bd=mon
        # sun-0bd=fri
        # sun+1bd/F=mon
        # sat+1d/F=mon
        # error roll with 0bd that conflicts

        # non-zero bd follows
        # +1bd/F
        # +1bd/P
        # -1bd/F
        # -1bd/P

        # modified

        # +1bd/MF
        # +1bd/MP
        # -1bd/MF
        # -1bd/MP

    def test_delta(self):
        dur = Duration(y=1, m=1, w=2, d=11)
        rd = dur.relativedelta
        expected_rd = dateutil.relativedelta.relativedelta(
            years=1, months=1, weeks=2, days=11
        )
        self.assertEqual(rd, expected_rd)

    def test_adjust_bds(self):
        dur = Duration(bd=1)
        _, d = dur.adjust_bds(Date(2024, 3, 6))
        self.assertEqual(d, Date(2024, 3, 7))

    def test_adjust_bds(self):
        """
        test business date adjustment which adjust date into business date
        """
        d = Date(2024, 3, 6)
        expected_d = Date(2024, 3, 7)
        dur = Duration(bd=1)
        sign, newd = dur.adjust_bds(d)
        
        self.assertEqual(newd, expected_d)

        dur = Duration()
        sign, newd = dur.adjust_bds(d)
        self.assertEqual(newd, Date(2024, 3, 6))

        dur = Duration(modified=True)
        sign, newd = dur.adjust_bds(d)
        self.assertEqual(newd, Date(2024, 3, 6))

    def test__validated_periodunits(self):
        pass

    def test__validate_cals(self):
        """
        test the validate cals where cals string should be 2,3 letters
        """
        cals = ["NYYY", "WE"]
        with self.assertRaises(Exception) as cm:
            d = Duration(cals=cals)

        self.assertEqual(
            str(cm.exception), "Calendars must be 2 or 3 letter strings (not NYYY)"
        )
        # validate cals must be str
        cals = [10]
        with self.assertRaises(Exception) as cm:
            d = Duration(cals=cals)
        self.assertEqual(str(cm.exception), "Calendars must be strings (not int)")

    def test__validate_adj_roll(self):
        pass

    def test_math(self):
        # coveraged by all dunder methods
        """
        test the add/sub of dur and dur or dur and d
        """
        dur2 = Duration(d=1)
        d1 = Date(2024, 1, 1)
        # newd1 = d1 + dur2

        # self.assertEqual(newd1,Date(2024,1,2))
        newd2 = d1 - dur2
        self.assertEqual(newd2, Date(2023, 12, 31))
        d1 = 10
        with self.assertRaises(NotImplementedError):
            d1 + dur2

        dur_cal = Duration(d=13, cals="WE")
        ndur = dur_cal + dur2
        self.assertEqual(
            ndur, Duration(years=0, months=0, days=14, modified=False, cals="WE")
        )
        dur_cal2 = Duration(d=1, cals="NY")
        ndur2 = dur_cal + dur_cal2
        self.assertEqual(
            ndur2, Duration(years=0, months=0, days=14, modified=False, cals="NYuWE")
        )

        bd1 = Duration(bd=1)
        bd2 = Duration(bd=2)
        bd3 = bd1 + bd2
        self.assertEqual(
            bd3, Duration(years=0, months=0, days=0, modified=False, bd=3, cals="WE")
        )
        rough1 = Duration(y=1, m=1, d=1)
        rough2 = Duration(y=-2, m=-2, d=-20, cals="WE")
        capt = StringIO()
        sys.stderr = capt
        r3 = rough1 + rough2
        sys.stderr = sys.__stderr__

        self.assertEqual(
            r3, Duration(years=-1, months=-1, days=-19, modified=False, cals="WE")
        )

        mdur = Duration(d=13, modified=True)
        mdur2 = Duration(d=1, modified=True)
        self.assertEqual(
            mdur + mdur2, Duration(years=0, months=0, days=14, modified=True)
        )

        nonedur1 = Duration(d=14)
        nonedur2 = Duration(d=1)
        self.assertEqual(
            nonedur1 + nonedur2, Duration(years=0, months=0, days=15, modified=False)
        )

        # test dur + rd, should not add rd, should return dur only
        rd3 = dateutil.relativedelta.relativedelta(days=3)
        rd7 = dateutil.relativedelta.relativedelta(days=7)
        dur4 = Duration(days=4)
        dur7 = Duration(days=7)
        dur7_from_math = dur4 + rd3
        self.assertEqual(dur7, dur7_from_math)
        self.assertEqual(dur7_from_math, rd7)

        # test dur +datelike and adjust business date if necessary
        dur = Duration(days=4)
        dt = Date(2024, 1, 1)
        x = dur + dt
        self.assertEqual(x.date, datetime.date(2024, 1, 5))

    def test___eq__(self):
        """
        test equality
        """
        from dateroll import ddh

        self.assertEqual(Duration(months=14), Duration(years=1, months=2))
        self.assertEqual(Duration(years=2), Duration(months=24))
        self.assertEqual(
            ddh("4/15/24-4/15/23"),
            Duration(
                years=1,
                months=0,
                days=0,
                modified=False,
                _anchor_start=Date(2023, 4, 15),
                _anchor_end=Date(2024, 4, 15),
                _anchor_months=12,
                _anchor_days=366,
                debug=False,
            ),
        )
        self.assertEqual(
            ddh("4/15/24-4/12/23"),
            Duration(
                years=1,
                months=0,
                days=3,
                modified=False,
                _anchor_start=Date(2023, 4, 12),
                _anchor_end=Date(2024, 4, 15),
                _anchor_months=12,
                _anchor_days=369,
                debug=False,
            ),
        )
        self.assertEqual(
            ddh("4/15/24-1/12/23"),
            Duration(
                years=1,
                months=3,
                days=3,
                modified=False,
                _anchor_start=Date(2023, 1, 12),
                _anchor_end=Date(2024, 4, 15),
                _anchor_months=15,
                _anchor_days=459,
                debug=False,
            ),
        )
        self.assertEqual(
            ddh("6/15/24-1/15/24"),
            Duration(
                years=0,
                months=5,
                days=0,
                modified=False,
                _anchor_start=Date(2024, 1, 15),
                _anchor_end=Date(2024, 6, 15),
                _anchor_months=5,
                _anchor_days=152,
                debug=False,
            ),
        )
        self.assertEqual(
            ddh("6/15/24-6/10/24"),
            Duration(
                years=0,
                months=0,
                days=5,
                modified=False,
                _anchor_start=Date(2024, 6, 10),
                _anchor_end=Date(2024, 6, 15),
                _anchor_months=0,
                _anchor_days=5,
                debug=False,
            ),
        )
        self.assertEqual(
            ddh("4/15/24-1/12/23"),
            Duration(
                years=1,
                months=3,
                days=3,
                modified=False,
                _anchor_start=Date(2023, 1, 12),
                _anchor_end=Date(2024, 4, 15),
                _anchor_months=15,
                _anchor_days=459,
                debug=False,
            ),
        )

        self.assertEqual(Duration(years=1).years, ddh("4/15/24-4/15/23").years)
        self.assertEqual(Duration(years=1, days=3).days, ddh("4/15/24-4/12/23").days)
        self.assertEqual(
            Duration(years=1, months=3, days=3).months, ddh("4/15/24-1/12/23").months
        )
        self.assertEqual(Duration(months=5).months, ddh("6/15/24-1/15/24").months)
        self.assertEqual(Duration(days=5).days, ddh("6/15/24-6/10/24").days)
        self.assertNotEqual(
            Duration(years=1, months=3, days=35).days, ddh("4/15/24-1/12/23").days
        )

        # pos testing
        self.assertEqual(Duration(days=5), Duration(days=5))
        self.assertEqual(Duration(days=5), dateutil.relativedelta.relativedelta(days=5))
        self.assertEqual(Duration(days=5), datetime.timedelta(days=5))

        # neg testing
        self.assertNotEqual(Duration(days=5), Duration(days=4))
        self.assertNotEqual(
            Duration(days=5), dateutil.relativedelta.relativedelta(days=4)
        )
        self.assertNotEqual(Duration(days=5), datetime.timedelta(days=4))

        with self.assertRaises(TypeError):
            Duration(days=5) == "23423"

    def test___iadd__(self):
        dur = Duration(bd=5)
        dt = Date(2024, 1, 1)
        dur += dt
        self.assertEqual(dur.date, datetime.date(2024, 1, 8))

    def test___init__(self):
        pass

    def test___isub__(self):
        dur = Duration(days=4)
        dt = Date(2024, 1, 1)
        dur -= dt
        self.assertEqual(dur.date, datetime.date(2023, 12, 28))

    def test___neg__(self):
        """
        test __neg__ means -dur
        """
        dur = Duration(days=4, modified=True)

        dur_neg = -dur
        self.assertEqual(dur.days, dur_neg.days * -1)

    def test___pos__(self):
        """
        test __pos__ means +dur
        """
        dur = Duration(days=4, modified=True)
        dur2 = +dur
        self.assertEqual(dur2, dur)

    def test_just_days(self):
        """
        test the number of days between two anchor dates
        """
        from dateroll import ddh

        dur = ddh("4/15/24-1/15/24")
        x = dur.just_days
        self.assertEqual(x, 91)
        y = dur.just_approx_days
        self.assertEqual(y, 91.3125)
        z = dur.just_exact_days
        self.assertEqual(z, 91)

        z = Duration(months=3).just_days
        self.assertAlmostEqual(z, 91.3125, 2)

        z = Duration(year=1).just_days
        self.assertAlmostEqual(z, 365.25, 2)

        dur = Duration(bd=1)
        x = dur.just_days
        self.assertAlmostEqual(365.25 / 252, x, 2)

        with self.assertRaises(ValueError):
            dur = Duration(years=1)
            dur.just_exact_days

    def test___radd__(self):
        pass

    def test___repr__(self):
        """
        test repr of Duration instance
        """
        dur = Duration(days=4, modified=True)
        dur2 = Duration(days=1, cals="NYuWE")
        repr(dur)
        repr(dur2)

    def test___rsub__(self):
        pass

    def test___sub__(self):
        pass

    def test_anchor(self):
        from dateroll import ddh

        dur = ddh("4/15/24-1/12/23")
        self.assertEqual(dur._anchor_months, 15)
        self.assertEqual(dur._anchor_days, 459)

    def test_bd0_and_roll(self):
        dur = Duration(bd=0, modified=True)
        self.assertEqual(dur.bd, 0)
        dur = Duration(BD=0, modified=True)
        self.assertEqual(dur.bd, 0)
        dur = Duration(BD=1, bd=2, modified=True)
        self.assertEqual(dur.bd, 3)

    def test_mod(self):

        from dateroll import ddh

        # check which roll wins if adding left and right
        # same roll
        dur = ddh("+5bd/MOD") + ddh("+3bd/MOD")
        self.assertTrue(dur.modified)

        # left only
        dur = ddh("+5bd/MOD") + ddh("+3bd")
        self.assertTrue(dur.modified)

        # right only
        dur = ddh("+5bd") + ddh("+3bd/MOD")
        self.assertTrue(dur.modified)

        # both, 0 -> /F
        # batuuuu test again why it fails now!!! ###########
        dur = ddh("+5bd/MOD") + ddh("-5bd/MOD")
        self.assertTrue(dur.modified)

        # equal approx
        dur = ddh("+3m/MOD") + ddh("-3m/MOD")
        self.assertTrue(dur.modified)

        # minus with approx w/ modifier
        dur = ddh("+3m/MOD") + ddh("-5m/MOD")
        self.assertTrue(dur.modified)

        # minus with approx
        dur = ddh("+3m/MOD") + ddh("-5m/MOD")
        self.assertTrue(dur.modified)

    def test_compare(self):

        dur1 = Duration(months=5)
        dur2 = Duration(days=-3)

        # same
        self.assertEqual(dur1, dur1)
        self.assertNotEqual(dur1, dur2)
        self.assertEqual(dur2, -3)

        # >
        self.assertGreater(dur1, dur2)
        self.assertGreater(dur2, -5)

        # >=
        self.assertGreaterEqual(dur1, dur2)
        self.assertGreaterEqual(dur2, -3)

        # <
        self.assertLess(dur2, dur1)
        self.assertLess(dur2, -2)

        # <=
        self.assertLessEqual(dur2, dur1)
        self.assertLessEqual(dur2, -3)

    def test_staticMethods(self):
        """
        passing durationlike would return duration
        """
        x = Duration(bd=1)
        self.assertEqual(x, Duration.from_relativedelta(x))
        self.assertEqual(x, Duration.from_timedelta(x))

    def test_hash(self):
        x = Duration(bd=1)
        rs = hash(x)
        self.assertIsInstance(rs, int)

    def test_failMod(self):
        x = ddh("12/1/2023+12m/MOD")

    def test_sub(self):
        dur1 = Duration(days=12)
        dur2 = Duration(days=1)
        rs = dur2 - dur1

        self.assertEqual(
            rs, Duration(years=0, months=0, days=-11, modified=False, debug=False)
        )

    def test_tostring(self):
        dur = Duration(
            years=1, months=2, days=3, bd=4, cals=["NY", "WE"], modified=True
        )
        dur2 = Duration(
            years=1, months=-2, days=3, bd=4, cals=["NY", "WE"], modified=True
        )
        dur3 = Duration(years=0)

        self.assertEqual(dur.to_string(), "+1y+2m+3d+4bd|NYuWE/MOD")
        self.assertEqual(dur2.to_string(), "+1y-2m+3d+4bd|NYuWE/MOD")
        self.assertEqual(dur3.to_string(), "+0d")

    def test_just_bds(self):
        """
            pick a calendar where on WEuNY you have 5 dates:

            a. MTWRF No hol
            b. M holiday, TWU no hol
            c. F holiday, TWU no hol
            d. MF holiday, TWU no hol
            e. W holiday, MTU no hol

        for each of the 5 above, you have 4 cases to test, so 20 test cases:

        MTWRF No hol
            () - 3
            (] - 4
            [) - 4
            [] - 5
        M holiday, TWU no hol
            () - 3
            (] - 4
            [) - 3
            [] - 4
        F holiday, TWU no hol
            () - 3
            (] - 3
            [) - 4
            [] - 4
        MF holiday, TWU no hol
            () - 3
            (] - 3
            [) - 3
            [] - 3
        W holiday, MTU no hol
            () - 2
            (] - 3
            [) - 3
            [] - 4

        e.g.
        """
        # a MTWRF No hol
        a = Date(2024, 1, 8)
        b = Date(2024, 1, 12)
        b_minus_a = b - a
        b_minus_a.cals = ["NY", "WE"]
        settings.ie = "(]"
        self.assertEqual(b_minus_a.just_bds, 4)
        settings.ie = "()"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "[)"
        self.assertEqual(b_minus_a.just_bds, 4)
        settings.ie = "[]"
        self.assertEqual(b_minus_a.just_bds, 5)

        # b. M holiday, TWU no hol
        a = Date(2024, 1, 1)
        b = Date(2024, 1, 5)
        b_minus_a = b - a
        b_minus_a.cals = ["NY", "WE"]
        settings.ie = "(]"
        self.assertEqual(b_minus_a.just_bds, 4)
        settings.ie = "()"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "[)"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "[]"
        self.assertEqual(b_minus_a.just_bds, 4)

        # c F holiday, MTWU no hol
        a = Date(2020, 12, 28)
        b = Date(2021, 1, 1)  # friday
        b_minus_a = b - a
        b_minus_a.cals = ["NY", "WE"]
        settings.ie = "(]"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "()"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "[)"
        self.assertEqual(b_minus_a.just_bds, 4)
        settings.ie = "[]"
        self.assertEqual(b_minus_a.just_bds, 4)

        # d Tu holiday, MWUF no hol
        a = Date(2018, 12, 31)
        b = Date(2019, 1, 4)  # friday
        b_minus_a = b - a
        b_minus_a.cals = ["NY", "WE"]
        settings.ie = "(]"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "()"
        self.assertEqual(b_minus_a.just_bds, 2)
        settings.ie = "[)"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "[]"
        self.assertEqual(b_minus_a.just_bds, 4)

        # e W holiday, MTU no hol
        a = Date(2019, 12, 23)
        b = Date(2019, 12, 27)  # friday
        b_minus_a = b - a
        b_minus_a.cals = ["NY", "WE"]
        settings.ie = "(]"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "()"
        self.assertEqual(b_minus_a.just_bds, 2)
        settings.ie = "[)"
        self.assertEqual(b_minus_a.just_bds, 3)
        settings.ie = "[]"
        self.assertEqual(b_minus_a.just_bds, 4)

        dur = Duration(year=1)
        with self.assertRaises(Exception):
            dur.just_bds
        # reset
        settings.ie = "(]"

    def test_duration_syntax_extras(self):
        """pass some invalid duration strings
        it must throw exception ParserStringsError
        """

        # junk
        self.assertRaises(Exception, lambda: ddh("1z"))
        # duplicate, only 1 of bd, d, w, m, q, y allowed for parseDurationString, currently picks one of them
        self.assertRaises(ParserStringsError, lambda: ddh("1bd1bd"))
        self.assertRaises(ParserStringsError, lambda: ddh("1d1d"))
        self.assertRaises(ParserStringsError, lambda: ddh("1w1w"))
        self.assertRaises(ParserStringsError, lambda: ddh("1m1m"))
        self.assertRaises(ParserStringsError, lambda: ddh("1q1q"))
        self.assertRaises(ParserStringsError, lambda: ddh("1y1y"))
        self.assertRaises(ParserStringsError, lambda: ddh("1y1y1m1d"))

    def test_yfs(self):
        d1 = ddh('5/15/2021')
        d2 = ddh('5/15/2024')
        # get expected answers from json file
        with open(EXPECTED_DAY_COUNT_PATH(),"r") as f:
            expected_daycount_dic = json.load(f)
        d1_rs = d1.to_string().split(" ")[0]
        d2_rs = d2.to_string().split(" ")[0]
        expected_dcf_ACT360 = expected_daycount_dic[f"{d1_rs}:{d2_rs}:ACT/360:NY"]
        
        dcf_ACT360 = (d2-d1).yf('ACT/360')
        # print('here')
        # import code;code.interact(local=dict(globals(),**locals()))
        self.assertEqual(dcf_ACT360, expected_dcf_ACT360)

        expected_dcf_ACT365 = expected_daycount_dic[f"{d1_rs}:{d2_rs}:ACT/365:NY"]
        dcf_ACT365 = (d2-d1).yf('ACT/365')
        self.assertEqual(dcf_ACT365, expected_dcf_ACT365)

        expected_dcf_30E360 = expected_daycount_dic[f"{d1_rs}:{d2_rs}:30E360:NY"]
        dcf_30E360 = (d2-d1).yf('30E/360')
        self.assertEqual(dcf_30E360, expected_dcf_30E360)

        # if we change to BR the difference is quite big eg, toler=0.083
        expected_dcf_BD252 = expected_daycount_dic[f"{d1_rs}:{d2_rs}:bd252:NY"]
        dcf_bd252 = (d2-d1).yf('BD/252',cals="NY") 
        toler = abs(expected_dcf_BD252 - dcf_bd252)
        
        self.assertTrue(toler<0.03)

        with self.assertRaises(ValueError):
            (d2-d1).yf("none")
        dur2 = (d2-d1)
        dur2.__setattribute__("cals","NY") 
        dcf_bd252 = (d2-d1).yf('BD/252',cals="NY") 
        toler = abs(expected_dcf_BD252 - dcf_bd252)
        
    def test_gt(self):
        """
        test when b = 0 to compare a= Duration(something) and a>b


        """

        b = 0
        # a is positive duration
        a = Duration(days=10)
        self.assertTrue(a > b)

        # a is negative
        a = Duration(days=-10)
        self.assertFalse(a > b)
        
            
    def test_init(self):
        with self.assertRaises(TypeError):
            Duration(days="10")
        with self.assertRaises(ValueError):
            Duration(bus_days=10)

    def test_durationstr_on_second(self):
        """
        make duration string work on the end date of schedule, eg, ddh(t,5y,3m)
        """
        result = ddh("t,t+5y,3m").list
        expected = ddh("t,5y,3m").list
        result = [d.date for d in result]
        expected = [d.date for d in expected]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
