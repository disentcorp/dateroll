import unittest

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
        self.assertIsInstance(x,Duration)
        self.assertRaises(TypeError,lambda :Duration.from_timedelta('garbage'))

    def test_period_units(self):
        '''
        properties
        '''

        y,m,w,d,bd = 1,2,3,4,5
        dur1 = Duration(y=y,m=m,w=w,d=d,bd=bd)
        dur2 = Duration()

        #month
        self.assertEqual(dur1.m,m)
        self.assertEqual(dur1.month,m)
        self.assertEqual(dur1.months,m)
        self.assertIsNone(dur2.m)
        self.assertIsNone(dur2.month)
        self.assertIsNone(dur2.months)
       
        #week
        self.assertEqual(dur1.w,w)
        self.assertEqual(dur1.week,w)
        self.assertEqual(dur1.weeks,w)
        self.assertIsNone(dur2.w)
        self.assertIsNone(dur2.week)
        self.assertIsNone(dur2.week)

        #year
        self.assertEqual(dur1.y,y)
        self.assertEqual(dur1.year,y)
        self.assertEqual(dur1.years,y)
        self.assertIsNone(dur2.y)
        self.assertIsNone(dur2.year)
        self.assertIsNone(dur2.years)

        #day
        self.assertEqual(dur1.d,d)
        self.assertEqual(dur1.day,d)
        self.assertEqual(dur1.days,d)
        self.assertIsNone(dur2.d)
        self.assertIsNone(dur2.day)
        self.assertIsNone(dur2.days)
        
        #bd
        self.assertEqual(dur1.bd,bd)
        self.assertIsNone(dur2.bd)

    def test_roll_no_roll(self):
        '''
        test each perm, and bad versions, and neg
        '''
        dur = Duration(bd=1,roll='MF')
        dur = Duration(bd=1,roll='P')
        dur = Duration(bd=1,roll='F')
        dur = Duration(bd=1,roll='MP')

        self.assertRaises(ValueError,lambda: Duration(bd=1,roll='shit'))
        self.assertRaises(TypeError,lambda: Duration(bd=1,roll=3))

        dur = Duration(bd=-3)
        self.assertEqual(dur.roll,'P')

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
        pass

    def test_adjust_bds(self):
        pass
    def test_apply_business_date_adjustment(self):
        pass
    def test_apply_roll_convention(self):
        pass

    def test__validated_periodunits(self):
        pass
    def test__validate_cals(self):
        pass
    def test__validate_adj_roll(self):
        pass

    def test_bd_only(self):
        pass
    def test_just_days(self):
        pass
    def test_rough_days(self):
        pass



    def test_math(self):
        ...# coveraged by all dunder methods

    def test___add__(self):
        pass
    def test___eq__(self):
        pass
    def test___iadd__(self):
        pass
    def test___init__(self):
        pass
    def test___isub__(self):
        pass
    def test___neg__(self):
        pass
    def test___pos__(self):
        pass
    def test___radd__(self):
        pass
    def test___repr__(self):
        pass
    def test___rsub__(self):
        pass
    def test___sub__(self):
        pass

if __name__=='__main__':
    unittest.main()