import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
import code
from unittest import expectedFailure

from dateroll.calendars.calendarmath import CalendarMath
from dateroll.date.date import Date


class TestStringMathMethods(unittest.TestCase):
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
        # without mod
        nonhol = Date(2023,1,3)
        x1 = self.cals.add_bd(nonhol,0,'WE')
        self.assertEqual(x1,Date(2023,1,3))
        hol = Date(2024,1,1)
        x2 = self.cals.add_bd(hol,0,['WE'])
        self.assertEqual(x2,Date(2024,1,1))
        x3 = self.cals.add_bd(nonhol,0,['WE','NY'])
        self.assertEqual(x3,Date(2023,1,3))
        hol2 = Date(2023,12,31)

        x4 = self.cals.add_bd(hol,0,['WE','NY'])
        x5 = self.cals.add_bd(hol2,0,['WE','NY'])
        
        self.assertEqual(x4,Date(2024,1,2))
        self.assertEqual(x5,Date(2024,1,2))
        x6 = self.cals.add_bd(hol,10000,'WE')

        self.assertEqual(x6,Date(2062,5,1))
        x7 = self.cals.add_bd(nonhol,10000,'WE')
        self.assertEqual(x7,Date(2061,5,3))
        

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
        hol2 = Date(2023,12,31)

        x4 = self.cals.sub_bd(hol,0,['WE','NY'])
        # code.interact(local=locals())
        x5 = self.cals.sub_bd(hol2,0,['WE','NY'])
    
        self.assertEqual(x4,Date(2023,12,29))
        self.assertEqual(x5,Date(2023,12,29))

        x6 = self.cals.sub_bd(hol,10000,'WE')
        x7 = self.cals.sub_bd(nonhol,10000,'WE')
        self.assertEqual(x6,Date(1985,9,2))
        self.assertEqual(x7,Date(1984,9,4))



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
        is_bd = self.cals.is_bd(hol)
        self.assertTrue(is_bd is True)
        is_bd = self.cals.is_bd(hol,['NY','WE'])
        self.assertFalse(is_bd is True)

        nonhol = Date(2024,1,4)
        is_bd = self.cals.is_bd(nonhol)
        self.assertTrue(is_bd is True)
        is_bd = self.cals.is_bd(nonhol,'WEuNY')
        self.assertTrue(is_bd is True)
        is_bd = self.cals.is_bd(nonhol,'WEuNYuBR')
        self.assertTrue(is_bd is True)


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
        cals = 'WEuNY'
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

    


    # def test_nextbd(self):
    #     """

    #     w/o mod

    #     from non-bd to bd on 1 cal
    #     from non-bd to bd on 2 cal union
    #     from bd to bd on 1 cal
    #     from bd to bd on 2 cal union

    #     w/ mod

    #     from non-bd to bd on 1 cal
    #     from non-bd to bd on 2 cal union
    #     from bd to bd on 1 cal
    #     from bd to bd on 2 cal union

    #     measure performance, put a threshold
    #     """

    # def test_prevbd(self):
    #     """

    #     w/o mod

    #     from non-bd to bd on 1 cal
    #     from non-bd to bd on 2 cal union
    #     from bd to bd on 1 cal
    #     from bd to bd on 2 cal union

    #     w/ mod

    #     from non-bd to bd on 1 cal
    #     from non-bd to bd on 2 cal union
    #     from bd to bd on 1 cal
    #     from bd to bd on 2 cal union

    #     measure performance, put a threshold
    #     """

    def test_dataBackendPresent(self):
        '''
            test data_backend_present function
        '''
        p = pathlib.Path('NonExist')
        if p.exists():
            os.remove(p)
        calmath = CalendarMath()
        hash = calmath.hash
        calmath.home = pathlib.Path('NonExist')
        calmath.data_backend_present
        hash2 = calmath.hash
        # code.interact(local=locals())
        self.assertEqual(hash,hash2)
        # code.interact(local=locals())
    
    # def test_emptyCalDates(self):
    #     '''
    #         when the dates are empty, e.g cals['AA'] = []
    #     '''
    #     cal = CalendarMath()
    #     cal.update({'AA':[]})
    #     cal.union('AA')
    #     code.interact(local=dict(globals(),**locals()))


if __name__ == "__main__":
    unittest.main()
