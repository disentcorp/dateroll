import code
import unittest

import dateroll.parser.parsers as parsers
import datetime
from dateroll.settings import settings
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
    
    def test_parseDateString(self):
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
            l,s = parsers.parseDateString(a,gen)
            
            b = list(l.values())[0].to_string().replace('-','/')
            self.assertEqual(a,b)

            #european
            settings.convention = 'DMY'
            a = '08/03/2024'
            l,s = parsers.parseDateString(a,gen)
            b = list(l.values())[0].to_string().replace('-','/')
            self.assertEqual(a,b)

            #international
            settings.convention = 'YMD'
            a = '2024/03/08'
            l,s = parsers.parseDateString(a,gen)
            b = list(l.values())[0].to_string().replace('-','/')
            self.assertEqual(a,b)

            #negative testing
            self.assertTrue('cannot do with a more stricter parser than dateutil.parser.parse')

        finally:
            #reset convention
            settings.convention = orig
    
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
        letters = [chr(i) for i in range(65, 65 + 26)]
        def gen(): yield letters.pop(0)
        s = '1y3m4d'
        s2 = parsers.parseDurationString(s,gen)
        
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
        
        







if __name__=='__main__':
    unittest.main()