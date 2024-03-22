import datetime
import unittest
import code

from dateroll import utils
from dateutil.relativedelta import relativedelta
from dateroll.settings import settings
from dateroll import Date, Duration


class TestDate(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test___cmp__(self):
        """
        test compares
        """

        # dateroll.Date with dateroll.Date
        a = Date(2024, 12, 5)
        b1 = Date(2024, 12, 5)
        b2 = Date(2024, 12, 6)
        self.assertEqual(a, b1)
        self.assertNotEqual(a, b2)

        # dateroll.Date with datetime.date
        b1 = datetime.date(2024, 12, 5)
        b2 = datetime.date(2024, 12, 6)
        self.assertEqual(a, b1)
        self.assertNotEqual(a, b2)

        # dateroll.Date with datetime.datetime
        b1 = datetime.datetime(2024, 12, 5)
        b2 = datetime.datetime(2024, 12, 6)
        self.assertEqual(a, b1)
        self.assertNotEqual(a, b2)

    def test_to_conversions(self):
        """
        dateroll.Date to datetime.datetime and datetime.date
        """

        a = Date(1900, 1, 1)
        b = datetime.date(1900, 1, 1)
        c = datetime.datetime(1900, 1, 1)

        self.assertEqual(b, a.date)
        self.assertEqual(c, a.datetime)

    def test_from_dateti(self):
        """conversion from"""

        ref = Date(1900, 1, 1)
        a = datetime.date(1900, 1, 1)
        b = datetime.datetime(1900, 1, 1)

        d1 = Date.from_datetime(a)
        self.assertEqual(ref, d1)

        d2 = Date.from_datetime(b)
        self.assertEqual(ref, d2)
        settings.convention = 'MDY'
        d3 = Date.from_string("1/1/1900")
        self.assertEqual(ref, d3)

    def test_is_bd(self):
        """
        check if day is a business day given a specific calendar
        """
        settings.convention = 'MDY'
        sunday = Date.from_string("3/3/2024")
        monday = Date.from_string("3/4/2024")
        christmas = Date.from_string("12/25/23")

        self.assertFalse(sunday.is_bd(cals="WEuLN"))
        self.assertTrue(monday.is_bd(cals="WEuNYuBR"))
        self.assertFalse(christmas.is_bd(cals="WEuNYuBR"))

    def test_conversions_out(self):
        """
        various properties
        """
        
        settings.convention = 'MDY'
        d = Date.from_string("3/3/24")
        # iso
        self.assertEqual(d.iso, "2024-03-03")

        # xls
        self.assertEqual(d.xls, 45354)

        # unix
        ts = d.datetime.timestamp()
        self.assertEqual(d.unix, ts)

        # #dotw
        dotw = d.dotw
        self.assertEqual(dotw, "Sun")

        # woty
        woty = d.woty
        self.assertEqual(woty, 9)

    def test_operations(self):
        """
        add, iadd, sub, rsub
        """
        d1 = Date(2024, 1, 3)
        d2 = Date(2024, 4, 3)
        d3 = datetime.date(2024,4,3)
        d4 = datetime.datetime(2024,4,3)
        dur = Duration(m=3)
        rd = relativedelta(months=3)
        td = datetime.timedelta(days=91)
        str_d1 = "1/3/24"
        str_dur = "+3m"
        int_dur = 91

        # add
        self.assertRaises(TypeError, lambda: d1 + d2)
        self.assertRaises(TypeError, lambda: d1 + str_d1)
        self.assertEqual(d1 + str_dur, d2)
        self.assertEqual(d1 + dur, d2)
        self.assertEqual(d1 + int_dur, d2)
        self.assertEqual(d1 + rd, d2)
        self.assertEqual(d1 + td, d2)
        self.assertEqual(d3-d2,Duration())

        self.assertRaises(TypeError,lambda: d1+3.0)
        self.assertRaises(TypeError,lambda: 3.0-d1)

        # # sub
        dur91d = Duration(y=0,m=3,w=0,d=0,_anchor_start=Date(2024,1,3),_anchor_end=Date(2024,4,3),)
        
        self.assertEqual((d2 - d1), dur91d)
        self.assertEqual(d2 - dur, d1)
        self.assertEqual(d2 - str_d1, dur91d)
        self.assertEqual(d2 - str_dur, d1)
        self.assertEqual(d2 - int_dur, d1)
        self.assertEqual(d2 - rd, d1)
        self.assertEqual(d2 - td, d1)
        self.assertEqual(d2 - d3,Duration(days=0))
        self.assertEqual(d2-d2,d3-d2)
        self.assertEqual(d2-d2,d4-d2)
        self.assertEqual(d2-d2,d2-d4)

        self.assertRaises(TypeError,lambda: dur-d1)
        self.assertRaises(TypeError,lambda: 3.0-d1)
        self.assertRaises(TypeError,lambda: d1-3.0)
        self.assertRaises(TypeError,lambda: d2-3.0)

        # iadd
        _d1 = d1
        try:
            _d1 += d2
            assert False
        except TypeError:
            assert True

        _d1 = d1
        _d1 += dur
        self.assertEqual(_d1, d2)

        _d1 = d1
        try:
            _d1 += str_d1
            assert False
        except TypeError:
            assert True

        _d1 = d1
        _d1 += int_dur

        self.assertEqual(_d1, d2)

        _d1 = d1
        _d1 += rd
        self.assertEqual(_d1, d2)

        _d1 = d1
        _d1 += td
        self.assertEqual(_d1, d2)

        # isub
        _d2 = d2
        _d2 -= d1
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= str_d1
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= dur
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= str_dur
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= int_dur
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= td
        self.assertEqual(_d2, d1)

        _d2 = d2
        _d2 -= rd
        self.assertEqual(_d2, d1)

    def test_repr(self):
        '''
            test the repr of date
        '''
        a = Date(2024, 12, 5)
        rs = repr(a)
        fmt = utils.convention_map[settings.convention]
        dstr = a.strftime(fmt)
        self.assertEqual(rs,f'Date(year=2024,month=12,day=5)')

    def test_from_string(self):
        '''
            test from string, pass Date or bad instance to raise TypeError
        '''

        x = '20230101'
        orig = settings.convention
        settings.convention = 'YMD'
        self.assertEqual(Date.from_string(x),Date(2023,1,1))
        with self.assertRaises(TypeError):
            Date.from_string(10)
        settings.convention = orig

    def test_fromDatetime(self):
        '''
            pass bad instance will raise Type error
        '''
        with self.assertRaises(TypeError):
            Date.from_datetime(10)
    
    def test_today(self):
        self.assertEqual(Date.today(),datetime.date.today())
    
    def test_toString(self):
        '''
            test src which prints calendar
        '''
        orig = settings.convention
        d = Date(2023,1,1)
        rs = d.to_string()
        self.assertEqual(rs,'01-01-2023')
        settings.convention = 'DMY'
        d = Date(2023,1,2)
        self.assertEqual(d.to_string(),'02-01-2023')
        settings.convention = 'YMD'
        self.assertEqual(d.to_string(),'2023-01-02')

        # reset
        settings.convention = orig
    
    def test_from_unix(self):
        '''
            test from timestamp
        '''
        good = {
            1711080000: datetime.datetime(2024, 3, 22, 0, 0),
            1426651200: datetime.datetime(2015, 3, 18, 0, 0),
            1372651200: datetime.datetime(2013, 7, 1, 0, 0),
            1470283200: datetime.datetime(2016, 8, 4, 0, 0),
            1745985600: datetime.datetime(2025, 4, 30, 0, 0),
            1940644800: datetime.datetime(2031, 7, 1, 0, 0),
            2108779200: datetime.datetime(2036, 10, 28, 0, 0),
            1856232000: datetime.datetime(2028, 10, 27, 0, 0),
            1644210000: datetime.datetime(2022, 2, 7, 0, 0),
            1684296000: datetime.datetime(2023, 5, 17, 0, 0),
            2104977600: datetime.datetime(2036, 9, 14, 0, 0),
            2015643600: datetime.datetime(2033, 11, 15, 0, 0),
            1745294400: datetime.datetime(2025, 4, 22, 0, 0),
            1548219600: datetime.datetime(2019, 1, 23, 0, 0),
            1263531600: datetime.datetime(2010, 1, 15, 0, 0),
            1244433600: datetime.datetime(2009, 6, 8, 0, 0),
            1436932800: datetime.datetime(2015, 7, 15, 0, 0),
            1199854800: datetime.datetime(2008, 1, 9, 0, 0),
            1589601600: datetime.datetime(2020, 5, 16, 0, 0),
            1217131200: datetime.datetime(2008, 7, 27, 0, 0),
            833256000.0: datetime.datetime(1996, 5, 28, 0, 0),
            528609600.0: datetime.datetime(1986, 10, 2, 0, 0),
            301464000.0: datetime.datetime(1979, 7, 22, 0, 0),
            174801600.0: datetime.datetime(1975, 7, 17, 0, 0),
            -83534400.0: datetime.datetime(1967, 5, 10, 0, 0),
            112161600.0: datetime.datetime(1973, 7, 22, 0, 0),
            -261864000.0: datetime.datetime(1961, 9, 14, 0, 0),
            94798800.0: datetime.datetime(1973, 1, 2, 0, 0),
            -203544000.0: datetime.datetime(1963, 7, 21, 0, 0),
            -83275200.0: datetime.datetime(1967, 5, 13, 0, 0)
        }
        bad1 =  { # 1st 5 are wrong dates,
            19058:datetime.date(1979, 7, 22),
            17592:datetime.date(1975, 7, 17),
            14602:datetime.date(1967, 5, 10),
            16867:datetime.date(1973, 7, 22),
            12538:datetime.date(1961, 9, 14),
        }
        bad2 ={ # bad strings
            "216.666":datetime.date(1973, 1, 2),
            "21321+3":datetime.date(1963, 7, 21),
            "21/4605":datetime.date(1967, 5, 13),
            ():datetime.date(1967, 5, 13),
        }

        # inbound

        for _a,_b in good.items():
            a,b = Date.from_unix(_a), Date.from_datetime(_b)
            self.assertEqual(a,b)
            
        for _a,_b in bad1.items():
            a,b = Date.from_timestamp(_a), Date.from_datetime(_b)
            self.assertNotEqual(a,b)     

        for _a in bad2:
            self.assertRaises(TypeError,lambda :Date.from_timestamp(_a))    

        # outbound
            
        for a,_b in good.items():
            b = Date.from_datetime(_b).unix
            self.assertEqual(a,b)
            
        for _a,_b in bad1.items():
            b = Date.from_datetime(_b).unix
            self.assertNotEqual(a,b)
    
    def test_from_xls(self):
        good = { # randomly generated from excel
            45373:datetime.date(2024, 3, 22),
            42081:datetime.date(2015, 3, 18),
            41456:datetime.date(2013, 7, 1),
            42586:datetime.date(2016, 8, 4),
            45777:datetime.date(2025, 4, 30),
            48030:datetime.date(2031, 7, 1),
            49976:datetime.date(2036, 10, 28),
            47053:datetime.date(2028, 10, 27),
            44599:datetime.date(2022, 2, 7),
            45063:datetime.date(2023, 5, 17),
            49932:datetime.date(2036, 9, 14),
            48898:datetime.date(2033, 11, 15),
            45769:datetime.date(2025, 4, 22),
            43488:datetime.date(2019, 1, 23),
            40193:datetime.date(2010, 1, 15),
            39972:datetime.date(2009, 6, 8),
            42200:datetime.date(2015, 7, 15),
            39456:datetime.date(2008, 1, 9),
            "43967":datetime.date(2020, 5, 16),
            "39656":datetime.date(2008, 7, 27),
            "35213":datetime.date(1996, 5, 28),
            "31687":datetime.date(1986, 10, 2),
            "29058":datetime.date(1979, 7, 22),
            "27592":datetime.date(1975, 7, 17),
            "24602":datetime.date(1967, 5, 10),
            "26867":datetime.date(1973, 7, 22),
            "22538":datetime.date(1961, 9, 14),
            "26666":datetime.date(1973, 1, 2),
            "23213":datetime.date(1963, 7, 21),
            "24605":datetime.date(1967, 5, 13),
        }
        
        bad1 =  { # 1st 5 are wrong dates,
            19058:datetime.date(1979, 7, 22),
            17592:datetime.date(1975, 7, 17),
            14602:datetime.date(1967, 5, 10),
            16867:datetime.date(1973, 7, 22),
            12538:datetime.date(1961, 9, 14),
        }
        bad2 ={ # bad strings
            "216.666":datetime.date(1973, 1, 2),
            "21321+3":datetime.date(1963, 7, 21),
            "21/4605":datetime.date(1967, 5, 13),
            ():datetime.date(1967, 5, 13),
        }

        # inbound

        for _a,_b in good.items():
            a,b = Date.from_xls(_a), Date.from_datetime(_b)
            self.assertEqual(a,b)
            
        for _a,_b in bad1.items():
            a,b = Date.from_xls(_a), Date.from_datetime(_b)
            self.assertNotEqual(a,b)     

        for _a in bad2:
            self.assertRaises(TypeError,lambda :Date.from_xls(_a))     

        # outbound   

        for a,_b in good.items():
            b = Date.from_datetime(_b).xls
            self.assertEqual(int(a),b)
            
        for _a,_b in bad1.items():
            b = Date.from_datetime(_b).xls
            self.assertNotEqual(a,b)

if __name__ == "__main__":
    unittest.main()
