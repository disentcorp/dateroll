import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
from unittest import expectedFailure
import pandas as pd
import code
import time

from dateroll.utils import color

import dateroll.calendars.calendars as calendars
from dateroll import ddh,cals
import dateroll.date.date as dateModule
from dateroll.settings import settings
import dateroll.duration.duration as durationModule
from tests.test_data.test_data import next_d,prev_d

def handle_sample_data_dates(x,inc,sign='+'):
    t = x['today']
    modified = x['modified']
    if modified:
        s = f'{t}{sign}{inc}|NYuWE/MOD'
    else:
        s = f'{t}{sign}{inc}|NYuWE'
    
    orig = settings.convention
    settings.convention = 'YMD'
    res = ddh(s)
    settings.convention = orig
    return res

class TestUsage(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_next_bd01(self):
        '''
            add 0 bd and 1bd from today
        
        '''
        df = pd.DataFrame(next_d)
        # print('in ddh')
        bd0 = df.apply(lambda x:handle_sample_data_dates(x,'0bd','+'),axis=1)
        bd0 = [l.strftime('%Y-%m-%d') for l in bd0.tolist()]
        expected0 = df['0bd'].tolist()
        expected1 = df['1bd'].tolist()
        self.assertEqual(bd0,expected0)
        bd1 = df.apply(lambda x:handle_sample_data_dates(x,'1bd','+'),axis=1)
        bd1 = [l.strftime('%Y-%m-%d') for l in bd1.tolist()]
        self.assertEqual(bd1,expected1)
        
    
    def test_prev_bd01(self):
        '''
            sub 0bd and 1bd from today
        '''
        df = pd.DataFrame(prev_d)
        bd0 = df.apply(lambda x:handle_sample_data_dates(x,'0bd','-'),axis=1)
        bd0 = [l.strftime('%Y-%m-%d') for l in bd0.tolist()]
        expected0 = df['-0bd'].tolist()
        expected1 = df['-1bd'].tolist()
        self.assertEqual(bd0,expected0)
        bd1 = df.apply(lambda x:handle_sample_data_dates(x,'1bd','-'),axis=1)
        bd1 = [l.strftime('%Y-%m-%d') for l in bd1.tolist()]
        self.assertEqual(bd1,expected1)
    
    def test_ddhCases(self):
        '''
            test edge cases of ddh and dates subtraction
        '''
        self.assertEqual(ddh('6m+6m'),durationModule.Duration(years=1, months=0, days=0, modified=False, debug=False))
        with self.assertRaises(Exception) as cm1:
            ddh('t+7dm')
        with self.assertRaises(Exception) as cm2:
            ddh('t+7g')
        
        self.assertEqual(ddh('6m+3m+1y+1/5/24'), dateModule.Date(2025,10,5))
        self.assertEqual(ddh('6m+3m+1y'),durationModule.Duration(years=1, months=9, days=0, modified=False, debug=False))
        self.assertEqual(ddh('2y-5m-4d'),durationModule.Duration(years=1, months=7, days=-4, modified=False, debug=False))
        self.assertEqual(dateModule.Date(2024,5,5)-dateModule.Date(2022,10,9),
                         durationModule.Duration(years=1, months=6, days=26, modified=False, _anchor_start=dateModule.Date(2022,10,9), _anchor_end=dateModule.Date(2024,5,5), _anchor_months=19, _anchor_days=-4, debug=False))
        d1 = ddh('10/9/22 - 5/5/24')
        d2 = dateModule.Date(2022,10,9) - dateModule.Date(2024,5,5)
        self.assertEqual(d1,d2)
        self.assertEqual(d2 + dateModule.Date(2024,5,5),dateModule.Date(2022,10,9))
        d3 = ddh('5/5/24 - 10/9/22')
        self.assertEqual(d3,
                         durationModule.Duration(years=1, months=6, days=26, modified=False, _anchor_start=dateModule.Date(2022,10,9), _anchor_end=dateModule.Date(2024,5,5), _anchor_months=19, _anchor_days=-4, debug=False))
        self.assertEqual(ddh('1/12/24+11m13d|NYuWE'),dateModule.Date(2024,12,26))

class TestUsageMore(unittest.TestCase):
    def tests_from_excel(self):
        #### TURN DEBUG ON OFF ####
        # ddh.debug = True
        ddh.debug = False
        #### TURN DEBUG ON OFF ####
        import pandas as pd
        
        df = pd.read_excel('tests/test_cases.xlsx')
        cols = ['from','ParserString','final','convention']
        df = df[cols]
        df = df.dropna()
        c = 0
        for idx,row in df.iterrows():
            s = row['ParserString']
            f = row['from']
            convention = row['convention']
            _a = time.time()
            a = ddh(row['final'])
            b = ddh(s)
            _b = time.time()
            ans = f'{str(b==a):<5}'
            res = color(ans,'green') if b==a else color(ans,'red')
            ms = round((_b -_a)*1000,0)
            if ms > 100:
                ms = f'{ms:>10} ms'
                ms = color(ms,'red')
            else:
                ms = f'{ms:>10} ms'
            
            print(f'tesing: {s:>28} = {b} == {a}',res,ms)
            if a==b:
                c+=1
        print(f'{c}/{len(df)} passed')
        # assert True if an only if all 32 pass
        self.assertTrue(c==len(df))
    
    

if __name__=='__main__':  

    # x = ddh('20231231+0bd|NYuWE/MOD',convention='YMD')
    # print(x)
    unittest.main()
