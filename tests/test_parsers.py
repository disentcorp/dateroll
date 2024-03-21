import code
import unittest

import dateroll.parser.parsers as parsers
import datetime
from dateroll.settings import settings
from dateroll.date.date import Date
from dateroll.duration.duration import Duration
from dateroll.ddh.ddh import ddh
from dateroll.schedule.schedule import Schedule

class TestParsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_parseTodayString(self):
        '''
            get today date, we pass t,today,t0 and get the date in a string format
        '''
        #store convention
        orig = settings.convention
        try:

            #american
            settings.convention = 'MDY'
            expected_mdy = datetime.date.today().strftime('%m/%d/%Y')
            t = parsers.parseTodayString('t')
            self.assertEqual(t.replace('-','/'),expected_mdy)

            #european
            settings.convention = 'DMY'
            expected_dmy = datetime.date.today().strftime('%d/%m/%Y')
            t = parsers.parseTodayString('t')
            self.assertEqual(t.replace('-','/'),expected_dmy)

            #international
            settings.convention = 'YMD'
            expected_ymd = datetime.date.today().strftime('%Y/%m/%d')
            t = parsers.parseTodayString('t')
            self.assertEqual(t.replace('-','/'),expected_ymd)

            #negative testing
            self.assertTrue('cannot do with a more stricter parser than dateutil.parser.parse')

        finally:
            #reset convention
            settings.convention = orig
    
    def test_parseManyDateStrings(self):
        '''
            test the parse date string based on convention
        '''
        #store convention
        orig = settings.convention
        letters = [chr(i) for i in range(65, 65 + 26)]
        def gen(): yield letters.pop(0)
        try:

            #american
            settings.convention = 'MDY'
            a = '03/08/2024'
            l,s = parsers.parseManyDateStrings(a,gen)
            b = list(l.values())[0].strftime('%m/%d/%Y')
            self.assertEqual(a,b)

            #european
            settings.convention = 'DMY'
            a = '08/03/2024'
            l,s = parsers.parseManyDateStrings(a,gen)
            b = list(l.values())[0].strftime('%d/%m/%Y')
            self.assertEqual(a,b)

            #international
            settings.convention = 'YMD'
            a = '2024/03/08'
            l,s = parsers.parseManyDateStrings(a,gen)
            b = list(l.values())[0].strftime('%Y/%m/%d')
            self.assertEqual(a,b)

            #negative testing
            self.assertTrue('cannot do with a more stricter parser than dateutil.parser.parse')

        finally:
            #reset convention
            settings.convention = orig
    
    def test_parseDurationString(self):
        '''
            test duration match
        '''
        s = ('','+','1','y','0','q','0','m','1','w','1','d','0','bd','WE','NY','BR','ECB','FED','LN','','','MOD')
        dur = parsers.parseDurationString(s)
        self.assertEqual(dur,Duration(years=1, months=0, days=8, modified=True, cals="BRuECBuFEDuLNuNYuWE"))

        s2 = ('','-','1','y','0','q','0','m','1','w','1','d','0','bd','WE','NY','BR','ECB','FED','LN','','','MOD')
        dur2 = parsers.parseDurationString(s2)
        self.assertEqual(dur2,Duration(years=-1, months=0, days=8, modified=True, cals="BRuECBuFEDuLNuNYuWE"))

        s3 = ('','*','1','y','0','q','0','m','1','w','1','d','0','bd','WE','NY','BR','ECB','FED','LN','','','P')
        with self.assertRaises(Exception) as cm:
            parsers.parseDurationString(s3)
        self.assertEqual(str(cm.exception),'Unknown operator')
        
        # no roll but it will have roll P
        s4 = ('','-','1','y','0','q','0','m','1','w','1','d','0','bd','WE','NY','BR','ECB','FED','LN','','','')
        dur4 = parsers.parseDurationString(s4)
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
        letters = [chr(i) for i in range(65, 65 + 26)]
        def gen(): yield letters.pop(0)
        s = '1y3m4d'
        s2 = parsers.parseManyDurationString(s,gen)
        
        self.assertEqual(s2,({'A': Duration(years=1, months=3, days=4, modified=False, debug=False)}, '+A'))
    
    def test_parseDateMathString(self):
        '''
            test parse date math string, +X-X
        '''

        # good
        self.assertEqual(parsers.parseDateMathString("A",{'A':4}),4)
        self.assertEqual(parsers.parseDateMathString("-A",{'A':4}),-4)
        self.assertEqual(parsers.parseDateMathString("+A",{'A':4}),4)
        self.assertEqual(parsers.parseDateMathString('A+B', {'A':4,'B':5}),9)
        self.assertEqual(parsers.parseDateMathString("A+B-C",{'A':4,'B':3,'C':1}),6)
        self.assertEqual(parsers.parseDateMathString("A+B-C-D",{'A':4,'B':3,'C':1,'D':1}),5)

        # bad
        with self.assertRaises(Exception) as cm:
            parsers.parseDateMathString("A+B", {'A':4})
    
        # bad
        with self.assertRaises(Exception) as cm:
            parsers.parseDateMathString('B',{'A':4,'B':5})        
    
    def test_parsersConvention(self):
        s = settings
    
    def test_validates(self):
        '''
            test validate month and dates and other validation
        '''
        settings.convention = 'MDY'
        with self.assertRaises(ValueError):
            Date.from_string('13/1/2023')
        with self.assertRaises(Exception):
            Date.from_string('02/29/2022')
        
        mdy = '0312023'
        with self.assertRaises(ValueError):
            Date.from_string(mdy)
        
        
        mdy = '01/10/2020'
        # MDY
        settings.convention = 'YMD'
        with self.assertRaises(TypeError):
            Date.from_string(mdy)
        settings.convention = 'MDY'

        with self.assertRaises(Exception):
            ddh('03012020,03302020,*1bd')
        with self.assertRaises(Exception):
            Schedule.from_string('03012020,1bd')
        
        with self.assertRaises(ValueError):
            Schedule.from_string('xyz,dfs,1bd')
        with self.assertRaises(ValueError):
            Schedule.from_string('03012020,03302020,xssssssss')
        
        







if __name__=='__main__':
    unittest.main()