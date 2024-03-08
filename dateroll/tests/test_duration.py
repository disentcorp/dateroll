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
        self.assertIsInstance(x,Duration)
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
        dur = Duration(
                    y=1,
                    m=1,
                    w=2,
                    d=11
        )
        rd = dur.delta
        expected_rd = dateutil.relativedelta.relativedelta(years=1,months=1,weeks=2,days=11)
        self.assertEqual(rd,expected_rd)

    def test_adjust_bds(self):
        dur = Duration(bd=1)
        d = dur.adjust_bds(Date(2024,3,6))
        self.assertEqual(d,Date(2024,3,7))
    
    def test_apply_business_date_adjustment(self):
        d = Date(2024,3,6)
        expected_d = Date(2024,3,7)
        dur = Duration(bd=1)
        newd = dur.apply_business_date_adjustment(d)
        self.assertEqual(newd,expected_d)

        dur = Duration()
        newd = dur.apply_business_date_adjustment(d)
        self.assertEqual(newd,Date(2024,3,6))

        dur = Duration(roll='F')
        newd = dur.apply_business_date_adjustment(d)
        self.assertEqual(newd,expected_d)


    def test_apply_roll_convention(self):
        '''
            calc business day based on roll conventions of P,F,MP,MF
        '''

        dur = Duration()
        d = Date(2024,3,6)
        with self.assertRaises(Exception) as cm:
            dur.apply_roll_convention(d)
        self.assertEqual(str(cm.exception),'Unhandled roll: Must be /F, /P / MF/ /MP')
        dur = Duration(roll='P')
        new_d = dur.apply_roll_convention(d)
        self.assertEqual(new_d,Date(2024,3,5))
        dur = Duration(roll='MP')
        new_d = dur.apply_roll_convention(d)
        self.assertEqual(new_d,Date(2024,3,5))
        dur = Duration(roll='F')
        new_d = dur.apply_roll_convention(d)
        self.assertEqual(new_d,Date(2024,3,7))
        dur = Duration(roll='MF')
        new_d = dur.apply_roll_convention(d)
        self.assertEqual(new_d,Date(2024,3,7))
        

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

    def test_just_days(self):
        pass
    def test_rough_days(self):
        '''
            returns the rough or exact days of duration
        '''
        # dur = Duration(y=1,m=/1,w=1,d=1,bd=1)
        # rs = dur.rough_days
        # self.assertEqual(rs,(False, ))



    def test_math(self):
        # coveraged by all dunder methods
        '''
            test the add/sub of dur and dur or dur and d
        '''
        dur1 = Duration(d=13,roll='F')
        dur2 = Duration(d=1)
        dur3 = dur1+dur2
        with self.assertRaises(Exception) as cm:
            dur4 = dur1-dur2
        dur1 = Duration(d=13,roll='P')
        with self.assertRaises(Exception) as cm2:
            dur5 = dur1 + dur2
        expected_dur = Duration(d=14,roll='F')
        expected_dur2 = 'In the negative direction, roll should not be F'
        self.assertEqual(dur3,expected_dur)
        self.assertEqual(str(cm.exception),expected_dur2)
        self.assertEqual(str(cm2.exception),'In the positive direction, roll should not be P')

        d1 = Date(2024,1,1)
        newd1 = d1 + dur2
        self.assertEqual(newd1,Date(2024,1,2))
        newd2 = d1 - dur2
        self.assertEqual(newd2,Date(2023,12,31))
        d1 = 10
        with self.assertRaises(NotImplementedError):
            d1 + dur2
        
        dur_cal = Duration(d=13,cals='WE')
        ndur = dur_cal + dur2
        
        self.assertEqual(ndur,Duration(m=0, d=14, bd=0, cals=('WE',), roll="F"))
        dur_cal2 = Duration(d=1,cals='NY')
        ndur2 = dur_cal + dur_cal2
        self.assertEqual(ndur2,Duration(m=0, d=14, bd=0, cals=('NY', 'WE'), roll="F"))
        ndur3 = dur2 + dur_cal
        self.assertEqual(ndur3,Duration(m=0, d=14, bd=0, cals=('WE',), roll="F"))

        bd1 = Duration(bd=1)
        bd2 = Duration(bd=2)
        bd3 = bd1 + bd2
        self.assertEqual(bd3,Duration(m=0, bd=3, cals=('WE',), roll="F"))
        rough1 = Duration(y=1,m=1,d=1)
        rough2 = Duration(y=-2,m=-2,d=-20,cals='WE')
        capt = StringIO()
        sys.stdout = capt
        r3 = rough1+rough2
        sys.stdout = sys.__stdout__
        output = capt.getvalue().strip()
        self.assertEqual(output,'**Rare edge case, direction change, with bd/non-bday potential overlap. Check roll.**')
        self.assertEqual(r3,Duration(y=-1, m=-1, d=-19, bd=0, cals=('WE',), roll="P"))

        mdur = Duration(d=13,roll='MF')
        mdur2 = Duration(d=1,roll='MF')
        self.assertEqual(mdur+mdur2,Duration(m=0, d=14, roll="MF"))
        mdur3 = Duration(d=13,roll = 'MP')
        mdur4 = Duration(d=1,roll='MP')
        self.assertEqual(mdur3-mdur4,Duration(m=0, d=14, roll="MP"))
        
        nonedur1 = Duration(d=14)
        nonedur2 = Duration(d=1)
        self.assertEqual(nonedur1+nonedur2,Duration(m=0, d=15))

        # test dur + rd, should not add rd, should return dur only
        rd = dateutil.relativedelta.relativedelta(days=3)
        dur = Duration(days=4)
        x = dur + rd
        self.assertEqual(x,dur)

        # test dur +datelike and adjust business date if necessary
        dur = Duration(days=4,roll='F')
        dt = Date(2024,1,1)
        x = dur+dt
        self.assertEqual(x,datetime.date(2024,1,8))




    def test___eq__(self):
        '''
            test equality
        '''

        # pos testing
        self.assertEqual(Duration(days=5),Duration(days=5))
        self.assertEqual(Duration(days=5),dateutil.relativedelta.relativedelta(days=5))
        self.assertEqual(Duration(days=5),datetime.timedelta(days=5))

        # neg testing
        self.assertNotEqual(Duration(days=5),Duration(days=4))
        self.assertNotEqual(Duration(days=5),dateutil.relativedelta.relativedelta(days=4))
        self.assertNotEqual(Duration(days=5),datetime.timedelta(days=4))

        self.assertFalse(Duration(days=5)==10)

    def test___iadd__(self):
        dur = Duration(days=4,roll='F')
        dt = Date(2024,1,1)
        dur+=dt
        self.assertEqual(dur,datetime.date(2024,1,8))
    def test___init__(self):
        pass
    def test___isub__(self):
        dur = Duration(days=4,roll='F')
        dt = Date(2024,1,1)
        dur-=dt
        self.assertEqual(dur,datetime.date(2023,12,29))
    def test___neg__(self):
        '''
            test __neg__ means -dur
        '''
        dur = Duration(days=4,roll='F')
        with self.assertRaises(NotImplementedError):
            dur = -dur
    def test___pos__(self):
        '''
            test __pos__ means +dur
        '''
        dur = Duration(days=4,roll='F')
        dur2 = +dur
        self.assertEqual(dur2,dur)
    
    def test_justDays(self):
        '''
            test the number of days between two anchor dates
        '''
        dur = Duration(days=4,anchor_start=Date(2024,3,1),anchor_end=Date(2024,3,15),roll='F')
        x = dur.just_days()
        self.assertEqual(x,14)

    def test___radd__(self):
        pass
    def test___repr__(self):
        '''
            test repr of Duration instance
        '''
        dur = Duration(days=4,roll='F')
        repr(dur)
    def test___rsub__(self):
        pass
    def test___sub__(self):
        pass

if __name__=='__main__':
    unittest.main()