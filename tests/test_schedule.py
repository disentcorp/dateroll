import unittest
import datetime
import io
import re
import sys
import numpy as np
import code

from dateroll.schedule.schedule import Schedule
from dateroll.date.date import Date
from dateroll.duration.duration import Duration
from dateroll.ddh.ddh import ddh

class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_dates_forward(self):
        '''
            test dates which give a range of dates and step>0
        '''
        
        start = Date(2023,1,1)
        stop = Date(2023,2,1)
        step = Duration(bd=1)
        sch = Schedule(start,stop,step)
        dts = sch.dates
        # convert into datetime
        dts = [d.datetime for d in dts]
        expected = [datetime.datetime(2023, 1, 1, 0, 0), datetime.datetime(2023, 1, 2, 0, 0), datetime.datetime(2023, 1, 3, 0, 0), datetime.datetime(2023, 1, 4, 0, 0), datetime.datetime(2023, 1, 5, 0, 0), datetime.datetime(2023, 1, 6, 0, 0), datetime.datetime(2023, 1, 9, 0, 0), datetime.datetime(2023, 1, 10, 0, 0), datetime.datetime(2023, 1, 11, 0, 0), datetime.datetime(2023, 1, 12, 0, 0), datetime.datetime(2023, 1, 13, 0, 0), datetime.datetime(2023, 1, 16, 0, 0), datetime.datetime(2023, 1, 17, 0, 0), datetime.datetime(2023, 1, 18, 0, 0), datetime.datetime(2023, 1, 19, 0, 0), datetime.datetime(2023, 1, 20, 0, 0), datetime.datetime(2023, 1, 23, 0, 0), datetime.datetime(2023, 1, 24, 0, 0), datetime.datetime(2023, 1, 25, 0, 0), datetime.datetime(2023, 1, 26, 0, 0), datetime.datetime(2023, 1, 27, 0, 0), datetime.datetime(2023, 1, 30, 0, 0), datetime.datetime(2023, 1, 31, 0, 0), datetime.datetime(2023, 2, 1, 0, 0)]
        self.assertEqual(dts,expected)

    def test_dates_backward(self):
        '''
            test dates when step<0
        '''
        start = Date(2023,1,1)
        stop = Date(2023,2,1)
        step = Duration(bd=-1)
        sch = Schedule(start,stop,step)
        dts = sch.dates
        # convert into datetime
        dts = [d.datetime for d in dts]
        expected = [datetime.datetime(2023, 1, 1, 0, 0),datetime.datetime(2023, 1, 2, 0, 0), datetime.datetime(2023, 1, 3, 0, 0), datetime.datetime(2023, 1, 4, 0, 0), datetime.datetime(2023, 1, 5, 0, 0), datetime.datetime(2023, 1, 6, 0, 0), datetime.datetime(2023, 1, 9, 0, 0), datetime.datetime(2023, 1, 10, 0, 0), datetime.datetime(2023, 1, 11, 0, 0), datetime.datetime(2023, 1, 12, 0, 0), datetime.datetime(2023, 1, 13, 0, 0), datetime.datetime(2023, 1, 16, 0, 0), datetime.datetime(2023, 1, 17, 0, 0), datetime.datetime(2023, 1, 18, 0, 0), datetime.datetime(2023, 1, 19, 0, 0), datetime.datetime(2023, 1, 20, 0, 0), datetime.datetime(2023, 1, 23, 0, 0), datetime.datetime(2023, 1, 24, 0, 0), datetime.datetime(2023, 1, 25, 0, 0), datetime.datetime(2023, 1, 26, 0, 0), datetime.datetime(2023, 1, 27, 0, 0), datetime.datetime(2023, 1, 30, 0, 0), datetime.datetime(2023, 1, 31, 0, 0), datetime.datetime(2023, 2, 1, 0, 0)]
        
        self.assertEqual(dts,expected)
    
    
    def test_cal(self):
        '''
            catch the print statement of cal property
        '''
        start = Date(2023,1,1)
        stop = Date(2023,2,1)
        step = Duration(bd=-1)
        sch = Schedule(start,stop,step)
        capt = io.StringIO()
        sys.stdout = capt
        sch.cal

        sys.stdout = sys.__stdout__

        txt = capt.getvalue().strip()
        expected = "from 01-01-2023 to 02-01-2023 cals ('WE',)\n\x1b[33m        Jan 2023Feb 2023                \x1b[0m\n   Su Mo Tu We Th Fr Sa    Su Mo Tu We Th Fr Sa\n  \x1b[94m  1\x1b[0m\x1b[96m  2\x1b[0m\x1b[96m  3\x1b[0m\x1b[96m  4\x1b[0m\x1b[96m  5\x1b[0m\x1b[96m  6\x1b[0m\x1b[38;5;239m  7\x1b[0m            \x1b[94m  1\x1b[0m  2  3  4\n  \x1b[38;5;239m  8\x1b[0m\x1b[96m  9\x1b[0m\x1b[96m 10\x1b[0m\x1b[96m 11\x1b[0m\x1b[96m 12\x1b[0m\x1b[96m 13\x1b[0m\x1b[38;5;239m 14\x1b[0m     5  6\x1b[38;5;239m  7\x1b[0m\x1b[38;5;239m  8\x1b[0m  9 10 11\n  \x1b[38;5;239m 15\x1b[0m\x1b[96m 16\x1b[0m\x1b[96m 17\x1b[0m\x1b[96m 18\x1b[0m\x1b[96m 19\x1b[0m\x1b[96m 20\x1b[0m\x1b[38;5;239m 21\x1b[0m    12 13\x1b[38;5;239m 14\x1b[0m\x1b[38;5;239m 15\x1b[0m 16 17 18\n  \x1b[38;5;239m 22\x1b[0m\x1b[96m 23\x1b[0m\x1b[96m 24\x1b[0m\x1b[96m 25\x1b[0m\x1b[96m 26\x1b[0m\x1b[96m 27\x1b[0m\x1b[38;5;239m 28\x1b[0m    19 20\x1b[38;5;239m 21\x1b[0m\x1b[38;5;239m 22\x1b[0m 23 24 25\n  \x1b[38;5;239m 29\x1b[0m\x1b[96m 30\x1b[0m\x1b[96m 31\x1b[0m26 27\x1b[38;5;239m 28\x1b[0m"
        txt = re.sub(r"\s+","",txt)
        expected = re.sub(r"\s+","",expected)
        self.assertEqual(txt,expected)
    
    def test_toString(self):
        '''
            to_string 
        '''
        schedule = ddh('20230101,20230201,1bd|NYuWE',convention='YMD')
        self.assertEqual(schedule.to_string(),'20230101,20230201,1bd|NYuWE')
        sch = Schedule(Date(2023,1,1),Date(2023,2,1),Duration(bd=1))
        with self.assertRaises(NotImplementedError):
            sch.to_string()
    
    def test_split(self):
        '''
            test split properties which return dataframe with columns of start,stop, and step
        '''
        sch = Schedule(Date(2023,1,1),Date(2023,2,1),Duration(bd=3))
        df = sch.split
        start = df.loc[0,'start']
        stop = df.loc[0,'stop']
        step = df.loc[0,'step']
        self.assertEqual(stop,start+ddh(step))
        
    
    def test_split_bond(self):
        '''
            test split bonds 
        '''
        sch = Schedule(Date(2023,1,1),Date(2023,2,1),Duration(bd=3))
        df = sch.split_bond
        df = df.dropna()
        starts = [i for i in df['starts'] if i is not None]
        ends = [i for i in df['ends'] if i is not None]
        days = [i for i in df['days'] if i is not None]
        ends_expected = [start + Duration(days=day) for start,day in zip(starts,days)]
        self.assertEqual(ends,ends_expected)
    
    def test_repr(self):
        sch = Schedule(Date(2023,1,1),Date(2023,2,1),Duration(bd=3))
        repr(sch)

    def test_str(self):
        sch = Schedule(Date(2023,1,1),Date(2023,2,1),Duration(bd=3))
        self.assertIsInstance(sch.__str__(),str)
        
        


        


    




if __name__=='__main__':
    unittest.main()