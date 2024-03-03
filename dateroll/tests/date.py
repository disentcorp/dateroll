import unittest
import datetime
from dateroll import Date

class TestDDH(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test___cmp__(self):
        '''
        test compares
        '''

        # dateroll.Date with dateroll.Date
        a = Date(2024,12,5)
        b1 = Date(2024,12,5)
        b2 = Date(2024,12,6)
        self.assertEqual(a,b1)
        self.assertNotEqual(a,b2)

        # dateroll.Date with datetime.date
        b1 = datetime.date(2024,12,5)
        b2 = datetime.date(2024,12,6)
        self.assertEqual(a,b1)
        self.assertNotEqual(a,b2)

        # dateroll.Date with datetime.datetime
        b1 = datetime.datetime(2024,12,5)
        b2 = datetime.datetime(2024,12,6)
        self.assertEqual(a,b1)
        self.assertNotEqual(a,b2)

    def test_to_conversions(self):
        '''
        dateroll.Date to datetime.datetime and datetime.date
        '''

        a = Date(1900,1,1)
        b = datetime.date(1900,1,1)        
        c = datetime.datetime(1900,1,1)        

        self.assertEqual(b,a.date)
        self.assertEqual(c,a.datetime)

    def test_from_dateti(self):
        ''' conversion from '''
        
        ref = Date(1900,1,1)
        a = datetime.date(1900,1,1)        
        b = datetime.datetime(1900,1,1)

        d1 = Date.from_datetime(a)
        self.assertEqual(ref,d1)

        d2 = Date.from_datetime(b)
        self.assertEqual(ref,d2)

        d3 = Date.from_string('1/1/1900')
        self.assertEqual(ref,d3)

    def test_isBd(self):
        '''
        check if day is a business day given a specific calendar
        '''
        sunday = Date.from_string('3/3/24')
        monday = Date.from_string('3/4/24')
        christmas = Date.from_string('12/25/23')

        self.assertFalse(sunday.is_bd(cals='WEuLN'))
        self.assertTrue(monday.is_bd(cals='WEuNYuBR'))
        self.assertFalse(christmas.is_bd(cals='WEuNYuBR'))

    def test_conversions_out(self):
        '''
        various properties
        '''
        d = Date.from_string('3/3/24')
        # iso
        self.assertEqual(d.iso,'2024-03-03')

        # xls
        self.assertEqual(d.xls,45354)

        # unix
        ts = d.datetime.timestamp()
        self.assertEqual(d.unix,ts)

        # #dotw
        dotw = d.dotw
        self.assertEqual(dotw,'Sun')
        
        # woty
        woty = d.woty
        self.assertEqual(woty,9)


    def test___radd__(self):
        pass
    def test___repr__(self):
        pass
    def test___sub__(self):
        pass

if __name__ == "__main__":
    unittest.main()