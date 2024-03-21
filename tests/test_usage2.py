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
from dateroll.settings import settings
import dateroll.parser.parsers as parsers


class TestUsage(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_dateFormats(self):
        '''
            test date formats: ymd,dmy,mdy
        
        '''
        original = settings.convention
        
        settings.convention = 'MDY'
        mdy_wrong = '30032011'
        ymd_wrong = '20113003'
        dmy_wrong = '03302011'
        
        with self.assertRaises(parsers.ParserStringsError):
            ddh(mdy_wrong)
        
        
        
        settings.convention = 'YMD'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(ymd_wrong)
        

        settings.convention = 'DMY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(dmy_wrong)
        

        settings.convention = 'MDY'
        
        mdy = ['03032011','3/3/2011','3/3/11','03-03-11']
        ymd = ['20110303','2011/3/3','11/3/3','11-3-3']
        dmy = ['03032011','3/3/2011','3/3/11','3-3-11']
        false_happened = False
        
        date = ddh(mdy[0])
        # for d in mdy:
        #     try:
        #         ddh(d)
        #     except:
        #         code.interact(local=locals())
        #     if ddh(d)!=date:
        #         false_happened = True
        settings.convention = 'YMD'
        for d in ymd:
            if ddh(d)!=date:
                false_happened = True
        settings.convention = 'DMY'
        for d in dmy:
            if ddh(d)!=date:
                false_happened = True
        self.assertFalse(false_happened)

        # reset
        settings.convention = original
    
    def test_slashes_wrong(self):
        '''
            test wrong dates with slash format
        '''
        mdy_wrong = '30/03/2011'
        ymd_wrong = '2011/30/03'
        dmy_wrong = '03/30/2011'

        settings.convention = 'MDY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(mdy_wrong)
        
        settings.convention = 'YMD'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(ymd_wrong)
        

        settings.convention= 'DMY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(dmy_wrong)
        
        # reset
        settings.convention = 'MDY'
    
    def test_dashes_wrong(self):
        '''
            test wrong dates with dash format
        '''
        mdy_wrong = '30-03-2011'
        ymd_wrong = '2011-30-03'
        dmy_wrong = '03-30-2011'

        settings.convention = 'MDY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(mdy_wrong)
        
        settings.convention = 'YMD'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(ymd_wrong)
        
        
        settings.convention= 'DMY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(dmy_wrong)
        
        # reset
        settings.convention = 'MDY'
    
    def test_fromat_changesDate(self):
        '''
            changing format gives different date, eg 20230111---> y=2011, m=03 d=11 or y=2011, m = 11, d =3
        '''

        mdy = '01102020'
        rs = dateModule.Date(2020,1,10)
        # MDY
        settings.convention = 'MDY'
        self.assertEqual(ddh(mdy),rs)
        settings.convention = 'YMD'
        with self.assertRaises(ValueError):
            ddh(mdy)
        settings.convention = 'DMY'
        self.assertNotEqual(ddh(mdy),rs)

        # DMY
        settings.convention = 'DMY'
        dmy = '02102020'
        rs = dateModule.Date(2020,10,2)
        
        self.assertEqual(ddh(dmy),rs)
        settings.convention = 'YMD'
        with self.assertRaises(ValueError):
            ddh(dmy)
        settings.convention = 'MDY'
        self.assertNotEqual(ddh(dmy),rs)

        # YMD
        settings.convention = 'YMD'
        ymd = '20200220'

        rs = dateModule.Date(2020,2,20)
        self.assertEqual(ddh(ymd),rs)

        settings.convention = 'MDY'
        with self.assertRaises(ValueError):
            ddh(ymd)
        settings.convention = 'DMY'
        with self.assertRaises(ValueError):
            ddh(ymd)

        # slashed
        mdy = '01/10/2020'
        rs = dateModule.Date(2020,1,10)
        # MDY
        settings.convention = 'MDY'
        self.assertEqual(ddh(mdy),rs)
        settings.convention = 'YMD'
        
        with self.assertRaises(Exception):
            ddh(mdy)
        settings.convention = 'DMY'
        self.assertNotEqual(ddh(mdy),rs)

        # DMY
        settings.convention = 'DMY'
        dmy = '2/10/2020'
        rs = dateModule.Date(2020,10,2)
        
        self.assertEqual(ddh(dmy),rs)
        settings.convention = 'YMD'
        with self.assertRaises(ValueError):
            ddh(dmy)
        settings.convention = 'MDY'
        self.assertNotEqual(ddh(dmy),rs)

        # YMD
        settings.convention = 'YMD'
        ymd = '2020/2/20'

        rs = dateModule.Date(2020,2,20)
        self.assertEqual(ddh(ymd),rs)

        settings.convention = 'MDY'
        with self.assertRaises(ValueError):
            ddh(ymd)
        settings.convention = 'DMY'
        with self.assertRaises(ValueError):
            ddh(ymd)

        # dashed
        mdy = '01-10-2020'
        rs = dateModule.Date(2020,1,10)
        # MDY
        settings.convention = 'MDY'
        self.assertEqual(ddh(mdy),rs)
        settings.convention = 'YMD'
        
        with self.assertRaises(Exception):
            ddh(mdy)
        settings.convention = 'DMY'
        self.assertNotEqual(ddh(mdy),rs)

        # DMY
        settings.convention = 'DMY'
        dmy = '2-10-2020'
        rs = dateModule.Date(2020,10,2)
        
        self.assertEqual(ddh(dmy),rs)
        settings.convention = 'YMD'
        with self.assertRaises(ValueError):
            ddh(dmy)
        settings.convention = 'MDY'
        self.assertNotEqual(ddh(dmy),rs)

        # YMD
        settings.convention = 'YMD'
        ymd = '2020-2-20'

        rs = dateModule.Date(2020,2,20)
        self.assertEqual(ddh(ymd),rs)

        settings.convention = 'MDY'
        with self.assertRaises(ValueError):
            ddh(ymd)
        settings.convention = 'DMY'
        with self.assertRaises(ValueError):
            ddh(ymd)

        # # reset 
        settings.convention = 'MDY'
    
    def test_weirdDates(self):
        # convention is mdy

        with self.assertRaises(parsers.ParserStringsError):
            x = ddh('7/7/7')
        
        x = ddh('7/7/70')
        self.assertEqual(x,dateModule.Date(1970,7,7))

        with self.assertRaises(ValueError):
            ddh('7770')

        with self.assertRaises(ValueError):
            ddh('33553')
        
        with self.assertRaises(ValueError):
            ddh('11553')

        

        

        
        


    
        

if __name__=='__main__':
    unittest.main()