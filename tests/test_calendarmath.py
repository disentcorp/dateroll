import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
import code
from unittest import expectedFailure

from dateroll.calendars.calendarmath import CalendarMath,DATA_LOCATION_FILE
from dateroll.date.date import Date
import dateroll.calendars.calendars as calendars



class TestStringMathMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename_base = (
            pathlib.Path(tempfile.gettempdir())
            / f"dateroll.testing.self.cals.{uuid.uuid4()}"
        )
        cls.cals = CalendarMath(home=cls.filename_base)

    @classmethod
    def tearDownClass(self):
        filename = str(self.filename_base)
        os.remove(filename)

    def test_addbd(self):
        """
        test add business days

        without mod:
            non-hol+0bd|WE
            hol+0bd|WE
            non-hol+0bd|WEuNY
            hol+0bd|WEuNY
            hol+1000bd
            nonhol+1000bd

        measure perf, put a threshold 

        """
        # without mod
        nonhol = Date(2023,1,3)
        x1 = self.cals.add_bd(nonhol,0,'WE')
        self.assertEqual(x1,Date(2023,1,3))
        hol = Date(2024,1,1)
        x2 = self.cals.add_bd(hol,0,['WE'])
        self.assertEqual(x2,Date(2024,1,1))
        x3 = self.cals.add_bd(nonhol,0,['WE','NY'])
        self.assertEqual(x3,Date(2023,1,3))

        x4 = self.cals.add_bd(hol,10000,'WE')

        self.assertEqual(x4,Date(2062,5,1))
        x5 = self.cals.add_bd(nonhol,10000,'WE')
        self.assertEqual(x5,Date(2061,5,3))
        

    def test_subbd(self):
        """
        just 1 or 2 from add, uses same mechanics

        """
        # without mod
        nonhol = Date(2023,1,3)
        hol = Date(2024,1,1)

        x1 = self.cals.sub_bd(nonhol,0,'WE')
        self.assertEqual(x1,Date(2023,1,3))
        
        x2 = self.cals.sub_bd(hol,0,['WE'])
        self.assertEqual(x2,Date(2024,1,1))
        x3 = self.cals.sub_bd(nonhol,0,['WE','NY'])
        self.assertEqual(x3,Date(2023,1,3))
        
        x4 = self.cals.sub_bd(hol,0,['WE','NY'])
        
        self.assertEqual(x4,Date(2023,12,29))
        x5 = self.cals.sub_bd(hol,10000,'WE')
        x6 = self.cals.sub_bd(nonhol,10000,'WE')
        self.assertEqual(x5,Date(1985,9,2))
        self.assertEqual(x6,Date(1984,9,4))



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
        hol = Date(2024,1,1)
        is_bd = self.cals.is_bd(hol,'WE')
        self.assertTrue(is_bd is True)
        is_bd = self.cals.is_bd(hol,['NY','WE'])
        self.assertFalse(is_bd is True)

        nonhol = Date(2024,1,4)
        is_bd = self.cals.is_bd(nonhol,'WE')
        self.assertTrue(is_bd is True)
        is_bd = self.cals.is_bd(nonhol,'WEuNY')
        self.assertTrue(is_bd is True)
        is_bd = self.cals.is_bd(nonhol,'WEuNYuBR')
        self.assertTrue(is_bd is True)


    def test_diffbd(self):
        """
        change global setting:  settings.ie='(])' do the test, then try again
                
        one liner test code:
        
        python -c "from dateroll import *; settings.ie='[]'; b=ddh('3/22/24'); a= ddh('3/18/24'); d=b-a; d.cals=['NY']; print(d.just_bds)"

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
    
        cals = 'NY'

        a = Date(2024,1,1)
        b = Date(2024,1,12)
        x = Date(2024,2,29)
        y = Date(2024,3,5)
        # [b,a) is here
        b_minus_a = self.cals.diff(a,b,cals)
        self.assertEqual(b_minus_a,9)
        a_minus_b = self.cals.diff(b,a,cals)
        self.assertEqual(a_minus_b,-9)

        #[y,x) here
        x_minus_y = self.cals.diff(x,y,cals)
        self.assertEqual(x_minus_y,3)
        x_minus_a = self.cals.diff(a,x,cals)
        self.assertEqual(x_minus_a,41)
        x_minus_b = self.cals.diff(x,b,cals)
        self.assertEqual(x_minus_b,-32)
        y_minus_a = self.cals.diff(a,y,cals)
        self.assertEqual(y_minus_a,44)
        y_minus_b = self.cals.diff(b,y,cals)
        self.assertEqual(y_minus_b,35)
        raise Exception('reimpliement test bd with i rules working using real test cases')

    

    def test_dataBackendPresent(self):
        '''
            test data_backend_present function
        '''
        p = pathlib.Path('NonExist')
        if p.exists():
            os.remove(p)
        calmath = self.cals
        hash = calmath.hash
        calmath.home = pathlib.Path('NonExist')
        calmath.data_backend_present
        hash2 = calmath.hash
        self.assertEqual(hash,hash2)

    
    def test_emptyCalDates(self):
        '''
            when the dates are empty, e.g cals['AA'] = []
        '''
        cal = self.cals.cals
        if 'AA' in cal.keys():
            del cal['AA']
        cal['AA'] = []
        calmath = self.cals
        nonhol = Date(2023,1,3)
        with self.assertRaises(Exception) as cm:
            self.cals.add_bd(nonhol,2,'AA')
        self.assertEqual(str(cm.exception),'Please provide holidays')

    
    def test_datetime(self):
        '''
            when pass datetime and date
        '''
        calmath = self.cals
        nonhol = datetime.datetime(2023,1,3)
        d = self.cals.add_bd(nonhol,1,None)
        self.assertEqual(d,Date(2023,1,4))

        # date
        nonhol2 = datetime.date(2023,1,3)
        d = self.cals.add_bd(nonhol2,1,'WE')
        self.assertEqual(d,Date(2023,1,4))
    
    def test_NonDate(self):
        '''
            when add non date should raise typeerror
        '''
        calmath = self.cals
        dt = 10
        with self.assertRaises(Exception) as cm:
            self.cals.add_bd(dt,2,'WE')
        self.assertEqual(str(cm.exception),'Date must be date (got int)')
    
    def test_calNotInCalKeys(self):
        '''
            when calendar is not in the Calendar instance
        
        '''

        nonhol = datetime.datetime(2023,1,3)
        
        with self.assertRaises(Exception) as cm:
            self.cals.add_bd(nonhol,1,'AB')
        self.assertEqual(str(cm.exception),"'There is no calendar AB'")
    
    def test_NonStringCal(self):
        '''
            calendar must be a string
        '''

        nonhol = datetime.datetime(2023,1,3)
        with self.assertRaises(Exception) as cm:
            self.cals.add_bd(nonhol,2,[10])
        
    def test_negativeN(self):
        '''
            when we try to pass n<0 in sub_bd, should raise error
        '''
        calmath = self.cals
        nonhol = datetime.datetime(2023,1,3)
        with self.assertRaises(Exception) as cm:
                    self.cals.sub_bd(nonhol,-1,'WE')
                
        self.assertEqual(str(cm.exception),'n needs to be positive number')
    def test_repr(self):
        calmath = self.cals
        x = repr(calmath)

    def test_nextBd(self):
        '''
            find the next bd
        '''

        nonhol = datetime.datetime(2023,12,29)
        hol = Date(2023,12,31)
        d = self.cals.next_bd(hol,'NYuWE')
        d2 = self.cals.next_bd(nonhol,'NYuWE')
        self.assertEqual(d,Date(2024,1,2))
        self.assertEqual(d2,Date(2024,1,2))
    
    def test_prevBd(self):
        '''
        
            find the previous bd
        '''
        
        
        nonhol = datetime.datetime(2024,1,2)
        hol = Date(2024,1,1)
        d = self.cals.prev_bd(hol,'NYuWE')
        d2 = self.cals.prev_bd(nonhol,'NYuWE')
        self.assertEqual(d,Date(2023,12,29))
        self.assertEqual(d2,Date(2023,12,29))
    
    def test_compileAll(self):
        self.cals.cached_compile_all()
    
    def test_generate_union(self):
        '''
            when calendar does not exist, raise keyError
        '''
        
        with self.assertRaises(KeyError):
            self.cals._generate_union('BAD')



    



if __name__ == "__main__":
    unittest.main()
