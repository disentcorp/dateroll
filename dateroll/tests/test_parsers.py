import code
import unittest

import dateroll.parser.parsers as parsers
import datetime
from dateroll.date.date import Date
from dateroll.duration.duration import Duration
class TestParsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_parseTodayString(self):
        '''
            get today date, we pass t,today,t0 and get the date in a string format
        '''
        
        expected_mdy = datetime.date.today().strftime('%m/%d/%Y')
        expected_dmy = datetime.date.today().strftime('%d/%m/%Y')
        expected_ymd = datetime.date.today().strftime('%Y/%m/%d')
        t = parsers.parseTodayString('t')
        self.assertEqual(t,expected_mdy)
        t = parsers.parseTodayString('t',convention='DMY')
        self.assertEqual(t,expected_dmy)
        t = parsers.parseTodayString('t',convention='YMD')
        self.assertEqual(t,expected_ymd)
        # wrong convention raises error
        with self.assertRaises(Exception) as cm:
            t = parsers.parseTodayString('t',convention='MYD')
        self.assertEqual(str(cm.exception),'MYD')
    
    def test_parseDateString(self):
        '''
            test the parse date string based on convention
        '''
        mdy = '03/08/2024'
        dmy = '08/03/2024'
        ymd = '2024/03/08'
        expected_date = Date(2024,3,8)
        d = parsers.parseDateString(mdy,None)
        self.assertEqual(d[0],[expected_date])
        # ymd
        d_ymd = parsers.parseDateString(ymd,'YMD')
        self.assertEqual(d_ymd[0],[expected_date])
        # dmy
        d_dmy = parsers.parseDateString(dmy,'DMY')
        self.assertEqual(d_dmy[0],[expected_date])
        # other convention raise error
        with self.assertRaises(Exception) as cm:
            parsers.parseDateString(mdy,'other')
        self.assertEqual(str(cm.exception),'No convention provided!')
    
    def test_process_duration_match(self):
        '''
            test duration match
        '''
        s = ('','+','1','y','0','q','0','m','1','w','1','d','0','bd','WE','NY','BR','ECB','FED','LN','','','MOD')
        dur = parsers.process_duration_match(s)
        self.assertEqual(dur,Duration(years=1, months=0, days=8, modified=True, cals="BRuECBuFEDuLNuNYuWE"))

        s2 = ('','-','1','y','0','q','0','m','1','w','1','d','0','bd','WE','NY','BR','ECB','FED','LN','','','MOD')
        dur2 = parsers.process_duration_match(s2)
        self.assertEqual(dur2,Duration(years=-1, months=0, days=8, modified=True, cals="BRuECBuFEDuLNuNYuWE"))

        s3 = ('','*','1','y','0','q','0','m','1','w','1','d','0','bd','WE','NY','BR','ECB','FED','LN','','','P')
        with self.assertRaises(Exception) as cm:
            parsers.process_duration_match(s3)
        self.assertEqual(str(cm.exception),'Unknown operator')
        
        # no roll but it will have roll P
        s4 = ('','-','1','y','0','q','0','m','1','w','1','d','0','bd','WE','NY','BR','ECB','FED','LN','','','')
        dur4 = parsers.process_duration_match(s4)
        self.assertEqual(dur4,Duration(years=-1, months=0, days=8, modified=False, cals="BRuECBuFEDuLNuNYuWE"))
    def test_parseCalendarUnionString(self):
        '''
            test cal union string e.g, NYuBR --> [NY,BR]
        '''
        
        s = 'NYuWE'
        s2 = parsers.parseCalendarUnionString(s)
        self.assertEqual(s2,('NY','WE'))

        # wrong string raise error
        with self.assertRaises(Exception) as cm:
            parsers.parseCalendarUnionString('ab')
        self.assertEqual(str(cm.exception),'ab not a valid calendar string')

    def test_parseDurationString(self):
        '''
            parse duration string
        '''

        s = '1y3m4d'
        s2 = parsers.parseDurationString(s)
        self.assertEqual(s2,([Duration(years=1, months=3, days=4)], '+X'))
    
    def test_parseDateMathString(self):
        '''
            test parse date math string, +X-X
        '''
        s = ' +X -X'
        s2 = ' +X -X -X'
        s3 = ' +X'
        things = [4,5]
        things2 = [4]
        rs = parsers.parseDateMathString(s,things)
        self.assertEqual(rs,-1)
        with self.assertRaises(Exception) as cm:
            parsers.parseDateMathString(s2,things)
        
        self.assertEqual(str(cm.exception),"('Cannot recognize as date math', '+X-X-X')")

        wrong_things = 'qwertyuiop[;lkjhgfdaszxcvbnm'

        with self.assertRaises(Exception) as cm:
            parsers.parseDateMathString(s,wrong_things)
        
        self.assertEqual(str(cm.exception),"('Cannot recognize as date math', '+X-X')")

        with self.assertRaises(Exception) as cm:
            parsers.parseDateMathString(s,things2)
        
        self.assertEqual(str(cm.exception),'Unmatched math (+X-X)')
        rs3 = parsers.parseDateMathString(s3,things2)
        self.assertEqual(rs3,4)
        







if __name__=='__main__':
    unittest.main()