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

import dateroll.duration.duration as durationModule
from tests.test_data.test_data import next_d,prev_d


class TestUsage(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_dateFormats(self):
        '''
            test date formats: ymd,dmy,mdy
        
        '''
        
        mdy_wrong = '30032011'
        ymd_wrong = '20113003'
        dmy_wrong = '03302011'
        with self.assertRaises(ValueError):
            ddh(mdy_wrong)
        
        # settings.convention = 'YMD'
        # with self.assertRaises(ValueError):
        #     ddh(ymd_wrong)
        # print('her23----')
        # code.interact(local=dict(globals(),**locals()))
        # settings.convention = 'DMY'
        # with self.assertRaises(ValueError):
        #     ddh(dmy_wrong)

        
        mdy = ['03032011','3/3/2011','3/3/11','03-03-11']
        # ymd = ['20110303','2011/3/3','11/3/3','11-3-3']
        # dmy = ['03032011','3/3/2011','3/3/11','3-3-11']
        false_happened = False
        # code.interact(local=dict(globals(),**locals()))
        date = ddh(mdy[0])
        for d in mdy:
            try:
                ddh(d)
            except:
                code.interact(local=locals())
            if ddh(d)!=date:
                false_happened = True
        # settings.convention = 'YMD'
        # for d in ymd:
        #     if ddh(d)!=date:
        #         false_happened = True
        # settings.convention = 'DMY'
        # for d in dmy:
        #     if ddh(d)!=date:
        #         false_happened = True
        self.assertFalse(false_happened)


        # code.interact(local=dict(globals(),**locals()))

if __name__=='__main__':
    unittest.main()