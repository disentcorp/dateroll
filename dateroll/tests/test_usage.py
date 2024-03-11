import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
from unittest import expectedFailure
import pandas as pd
import code

import dateroll.calendars.calendars as calendars
from dateroll import ddh,cals
import dateroll
from dateroll.tests.test_data.test_data import next_d,prev_d

def handle_sample_data_dates(x,inc,sign='+'):
    t = x['today']
    roll = x['roll']
    res = ddh(f'{t}{sign}{inc}|NYuWE/{roll}',convention='YMD')
    return res

class TestDDH(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_next_bd01(self):
        '''
            add 0 bd and 1bd from today
        
        '''
        df = pd.DataFrame(next_d)
        bd0 = df.apply(lambda x:handle_sample_data_dates(x,'0bd','+'),axis=1)
        bd0 = [l.strftime('%Y-%m-%d') for l in bd0.tolist()]
        self.assertEqual(bd0,df['0bd'].tolist())
        bd1 = df.apply(lambda x:handle_sample_data_dates(x,'1bd','+'),axis=1)
        bd1 = [l.strftime('%Y-%m-%d') for l in bd1.tolist()]
        
        self.assertEqual(bd1,df['1bd'].tolist())
        
    
    def test_prev_bd01(self):
        '''
            sub 0bd and 1bd from today
        '''
        df = pd.DataFrame(prev_d)
        bd0 = df.apply(lambda x:handle_sample_data_dates(x,'0bd','-'),axis=1)
        bd0 = [l.strftime('%Y-%m-%d') for l in bd0.tolist()]
        self.assertEqual(bd0,df['-0bd'].tolist())
        bd1 = df.apply(lambda x:handle_sample_data_dates(x,'1bd','-'),axis=1)
        bd1 = [l.strftime('%Y-%m-%d') for l in bd1.tolist()]
        self.assertEqual(bd1,df['-1bd'].tolist())
        


if __name__=='__main__':
    unittest.main()