import unittest

import code
import sys
from io import StringIO
import datetime
import dateutil.relativedelta
from dateroll import Date,Duration

class TestDuration(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...


    def test_from_string(self):
        '''
        good string bad string
        '''
        x = Duration.from_string('+3m|NY')
        self.assertIsInstance(x,Duration)
        self.assertRaises(TypeError,lambda :Duration.from_string('garbage'))
        self.assertRaises(TypeError,lambda :Duration.from_string(3))
        
    def test_from_rd(self):
        '''
        good rd non-rd
        '''
        rd = dateutil.relativedelta.relativedelta(years=3,months=2,weeks=1,days=1)
        x = Duration.from_relativedelta(rd)
        self.assertIsInstance(x,Duration)
        self.assertRaises(TypeError,lambda :Duration.from_relativedelta('garbage'))

    def test_from_td(self):
        '''
        good td non-td
        '''
        td = datetime.timedelta(weeks=1,days=12)
        x = Duration.from_timedelta(td)
        y = Duration.from_relativedelta(td)
        self.assertIsInstance(x,Duration)
        self.assertIsInstance(y,Duration)
        self.assertRaises(TypeError,lambda :Duration.from_timedelta('garbage'))

    def test_period_units(self):
        '''
        properties
        '''

        y,m,w,d,bd = 1,2,3,4,5
        dur1 = Duration(y=y,m=m,w=w,d=d,bd=bd)
        dur2 = Duration()
      
        #year
        self.assertEqual(dur1.y,y)
        self.assertEqual(dur1.year,y)
        self.assertEqual(dur1.years,y)

        #month
        self.assertEqual(dur1.m,m)
        self.assertEqual(dur1.month,m)
        self.assertEqual(dur1.months,m)

        #day
        self.assertEqual(dur1.d,d+7*w)
        self.assertEqual(dur1.day,d+7*w)
        self.assertEqual(dur1.days,d+7*w)
        
        #bd
        self.assertEqual(dur1.bd,bd)
        self.assertIsNone(dur2.bd)

    def test_roll_no_roll(self):
        '''
        test each perm, and bad versions, and neg
        '''
        dur = Duration(bd=1,modified=True)

        dur = Duration(bd=-3)
        

    def test_cals(self):
        cals1 = ['WE','NY']
        cals2 = 'WE'
        cals3 = 'WEuNY'
        good = ('NY','WE')

        cals4 = ['BAD','NY']
        cals5 = 'BAD'
        cals6 = 'NYuBAD'

        self.assertEqual(Duration(d=0,cals=cals1).cals,good)
        self.assertEqual(Duration(d=0,cals=cals2).cals,('WE',))
        self.assertEqual(Duration(d=0,cals=cals3).cals,good)

        self.assertRaises(ValueError,lambda : Duration(d=0,cals=cals4))
        self.assertRaises(ValueError,lambda : Duration(d=0,cals=cals5))
        self.assertRaises(ValueError,lambda : Duration(d=0,cals=cals6))
        

    def test_bdadj(self):
        '''
        test 0bd and >1bd and <1bd
        for each one of valid rolls
        '''

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
        dur = Duration(
                    y=1,
                    m=1,
                    w=2,
                    d=11
        )
        rd = dur.relativedelta
        expected_rd = dateutil.relativedelta.relativedelta(years=1,months=1,weeks=2,days=11)
        self.assertEqual(rd,expected_rd)

    def test_adjust_bds(self):
        dur = Duration(bd=1)
        _,d = dur.adjust_bds(Date(2024,3,6))
        self.assertEqual(d,Date(2024,3,7))
    
    def test_adjust_bds(self):
        '''
            test business date adjustment which adjust date into business date
        '''
        d = Date(2024,3,6)
        expected_d = Date(2024,3,7)
        dur = Duration(bd=1)
        sign, newd = dur.adjust_bds(d)
        self.assertEqual(newd,expected_d)

        dur = Duration()
        sign, newd = dur.adjust_bds(d)
        self.assertEqual(newd,Date(2024,3,6))

        dur = Duration(modified=True)
        sign, newd = dur.adjust_bds(d)
        self.assertEqual(newd,Date(2024,3,6))

    def test__validated_periodunits(self):
        pass
    def test__validate_cals(self):
        '''
            test the validate cals where cals string should be 2,3 letters
        '''
        cals = ['NYYY','WE']
        with self.assertRaises(Exception) as cm:
            d = Duration(cals=cals)
        
        self.assertEqual(str(cm.exception),'Calendars must be 2 or 3 letter strings (not NYYY)')
        # validate cals must be str
        cals = [10]
        with self.assertRaises(Exception) as cm:
            d = Duration(cals=cals)
        self.assertEqual(str(cm.exception),'Calendars must be strings (not int)')
    def test__validate_adj_roll(self):
        pass

    def test_math(self):
        # coveraged by all dunder methods
        '''
            test the add/sub of dur and dur or dur and d
        '''
        dur2 = Duration(d=1)
        d1 = Date(2024,1,1)
        # newd1 = d1 + dur2
        
        # self.assertEqual(newd1,Date(2024,1,2))
        newd2 = d1 - dur2
        self.assertEqual(newd2,Date(2023,12,31))
        d1 = 10
        with self.assertRaises(NotImplementedError):
            d1 + dur2
        
        dur_cal = Duration(d=13,cals='WE')
        ndur = dur_cal + dur2
        self.assertEqual(ndur,Duration(years=0, months=0, days=14, modified=False, cals="WE"))
        dur_cal2 = Duration(d=1,cals='NY')
        ndur2 = dur_cal + dur_cal2
        self.assertEqual(ndur2,Duration(years=0, months=0, days=14, modified=False, cals="NYuWE"))

        bd1 = Duration(bd=1)
        bd2 = Duration(bd=2)
        bd3 = bd1 + bd2
        self.assertEqual(bd3,Duration(years=0, months=0, days=0, modified=False, bd=3, cals="WE"))
        rough1 = Duration(y=1,m=1,d=1)
        rough2 = Duration(y=-2,m=-2,d=-20,cals='WE')
        capt = StringIO()
        sys.stderr = capt
        r3 = rough1+rough2
        sys.stderr = sys.__stderr__
        
        self.assertEqual(r3,Duration(years=-1, months=-1, days=-19, modified=False, cals="WE"))

        mdur = Duration(d=13,modified=True)
        mdur2 = Duration(d=1,modified=True)
        self.assertEqual(mdur+mdur2,Duration(years=0, months=0, days=14, modified=True))
        
        nonedur1 = Duration(d=14)
        nonedur2 = Duration(d=1)
        self.assertEqual(nonedur1+nonedur2,Duration(years=0, months=0, days=15, modified=False))

        # test dur + rd, should not add rd, should return dur only
        rd3 = dateutil.relativedelta.relativedelta(days=3)
        rd7 = dateutil.relativedelta.relativedelta(days=7)
        dur4 = Duration(days=4)
        dur7 = Duration(days=7)
        dur7_from_math = dur4 + rd3
        self.assertEqual(dur7,dur7_from_math)
        self.assertEqual(dur7_from_math,rd7)

        # test dur +datelike and adjust business date if necessary
        dur = Duration(days=4)
        dt = Date(2024,1,1)
        x = dur+dt
        self.assertEqual(x,datetime.date(2024,1,5))




    def test___eq__(self):
        '''
            test equality
        '''
        from dateroll import ddh
        self.assertEqual(Duration(months=14),Duration(years=1,months=2))
        self.assertEqual(Duration(years=2),Duration(months=24))
        self.assertEqual(ddh('4/15/24-4/15/23'),Duration(years=1))
        self.assertEqual(ddh('4/15/24-4/12/23'),Duration(years=1,days=3))
        self.assertEqual(ddh('4/15/24-1/12/23'),Duration(years=1,months=3,days=3))
        self.assertEqual(ddh('6/15/24-1/15/24'),Duration(months=5))
        self.assertEqual(ddh('6/15/24-6/10/24'),Duration(days=5))
        self.assertNotEqual(ddh('4/15/24-1/12/23'),Duration(years=1,months=3,days=35))

        self.assertEqual(Duration(years=1),ddh('4/15/24-4/15/23'))
        self.assertEqual(Duration(years=1,days=3),ddh('4/15/24-4/12/23'))
        self.assertEqual(Duration(years=1,months=3,days=3),ddh('4/15/24-1/12/23'))
        self.assertEqual(Duration(months=5),ddh('6/15/24-1/15/24'))
        self.assertEqual(Duration(days=5),ddh('6/15/24-6/10/24'))
        self.assertNotEqual(Duration(years=1,months=3,days=35),ddh('4/15/24-1/12/23'))


        
        # pos testing
        self.assertEqual(Duration(days=5),Duration(days=5))
        self.assertEqual(Duration(days=5),dateutil.relativedelta.relativedelta(days=5))
        self.assertEqual(Duration(days=5),datetime.timedelta(days=5))

        # neg testing
        self.assertNotEqual(Duration(days=5),Duration(days=4))
        self.assertNotEqual(Duration(days=5),dateutil.relativedelta.relativedelta(days=4))
        self.assertNotEqual(Duration(days=5),datetime.timedelta(days=4))

        with self.assertRaises(TypeError):
            Duration(days=5)=='23423'

    def test___iadd__(self):
        dur = Duration(bd=5)
        dt = Date(2024,1,1)
        dur+=dt
        self.assertEqual(dur,datetime.date(2024,1,8))
    def test___init__(self):
        pass
    def test___isub__(self):
        dur = Duration(days=4)
        dt = Date(2024,1,1)
        dur-=dt
        self.assertEqual(dur,datetime.date(2023,12,28))
    def test___neg__(self):
        '''
            test __neg__ means -dur
        '''
        dur = Duration(days=4,modified=True)
        
        dur_neg = -dur
        self.assertEqual(dur.days,dur_neg.days * -1)
    def test___pos__(self):
        '''
            test __pos__ means +dur
        '''
        dur = Duration(days=4,modified=True)
        dur2 = +dur
        self.assertEqual(dur2,dur)
    
    def test_just_days(self):
        '''
            test the number of days between two anchor dates
        '''
        from dateroll import ddh
        dur = ddh('4/15/24-1/15/24')
        x = dur.just_days
        self.assertEqual(x,91)
        y = dur.just_approx_days
        self.assertEqual(y,91)
        z = dur.just_exact_days
        self.assertEqual(z,91)


        z = Duration(months=3).just_days
        self.assertAlmostEqual(z,91.3125,2)

        z = Duration(year=1).just_days
        self.assertAlmostEqual(z,365.25,2)

        dur = Duration(bd=1)
        x = dur.just_days
        self.assertAlmostEqual(365.25/252,x,2)

        with self.assertRaises(ValueError):
            dur = Duration(years=1)
            dur.just_exact_days


    def test___radd__(self):
        pass
    def test___repr__(self):
        '''
            test repr of Duration instance
        '''
        dur = Duration(days=4,modified=True)
        repr(dur)
    def test___rsub__(self):
        pass
    def test___sub__(self):
        pass

    def test_anchor(self):
        from dateroll import ddh
        dur = ddh('4/15/24-1/12/23')
        self.assertEqual(dur._anchor_months,15)
        self.assertEqual(dur._anchor_days,3)

    def test_bd0_and_roll(self):
        dur = Duration(bd=0,modified=True)
        self.assertEqual(dur.bd,0)
        dur = Duration(BD=0,modified=True)
        self.assertEqual(dur.bd,0)
        dur = Duration(BD=1,bd=2,modified=True)
        self.assertEqual(dur.bd,3)

    def test_mod(self):
        
        from dateroll import ddh

        # check which roll wins if adding left and right

        # same roll
        dur = ddh('+5bd/MOD')+ddh('+3bd/MOD')
        self.assertTrue(dur.modified)

        # left only
        dur = ddh('+5bd/MOD')+ddh('+3bd')
        self.assertTrue(dur.modified)

        # right only
        dur = ddh('+5bd')+ddh('+3bd/MOD')
        self.assertTrue(dur.modified)


        

        # both, 0 -> /F
        # batuuuu test again why it fails now!!! ###########
        dur = ddh('+5bd/MOD')+ddh('-5bd/MOD')
        self.assertTrue(dur.modified)

        # equal approx
        dur = ddh('+3m/MOD')+ddh('-3m/MOD')
        self.assertTrue(dur.modified)

        # minus with approx w/ modifier
        dur = ddh('+3m/MOD')+ddh('-5m/MOD')
        self.assertTrue(dur.modified)
        
        # minus with approx
        dur = ddh('+3m/MOD')+ddh('-5m/MOD')
        self.assertTrue(dur.modified)

    def test_compare(self):
        
        dur1 = Duration(months=5)
        dur2 = Duration(days=-3)

        # same
        self.assertEqual(dur1,dur1)
        self.assertNotEqual(dur1,dur2)
        self.assertEqual(dur2,-3)

        # >
        self.assertGreater(dur1,dur2)
        self.assertGreater(dur2,-5)

        # >=
        self.assertGreaterEqual(dur1,dur2)
        self.assertGreaterEqual(dur2,-3)
        
        # <
        self.assertLess(dur2,dur1)
        self.assertLess(dur2,-2)
        
        # <=
        self.assertLessEqual(dur2,dur1)
        self.assertLessEqual(dur2,-3)





if __name__=='__main__':
    unittest.main()