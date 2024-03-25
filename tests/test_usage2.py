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
import re
import itertools

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
        with self.assertRaises(parsers.ParserStringsError):
            ddh(mdy)
        settings.convention = 'DMY'
        self.assertNotEqual(ddh(mdy),rs)

        # DMY
        settings.convention = 'DMY'
        dmy = '02102020'
        rs = dateModule.Date(2020,10,2)
        
        self.assertEqual(ddh(dmy),rs)
        settings.convention = 'YMD'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(dmy)
        settings.convention = 'MDY'
        self.assertNotEqual(ddh(dmy),rs)

        # YMD
        settings.convention = 'YMD'
        ymd = '20200220'

        rs = dateModule.Date(2020,2,20)
        self.assertEqual(ddh(ymd),rs)

        settings.convention = 'MDY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(ymd)
        settings.convention = 'DMY'
        with self.assertRaises(parsers.ParserStringsError):
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
        with self.assertRaises(parsers.ParserStringsError):
            ddh(dmy)
        settings.convention = 'MDY'
        self.assertNotEqual(ddh(dmy),rs)

        # YMD
        settings.convention = 'YMD'
        ymd = '2020/2/20'

        rs = dateModule.Date(2020,2,20)
        self.assertEqual(ddh(ymd),rs)

        settings.convention = 'MDY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(ymd)
        settings.convention = 'DMY'
        with self.assertRaises(parsers.ParserStringsError):
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
        with self.assertRaises(parsers.ParserStringsError):
            ddh(dmy)
        settings.convention = 'MDY'
        self.assertNotEqual(ddh(dmy),rs)

        # YMD
        settings.convention = 'YMD'
        ymd = '2020-2-20'

        rs = dateModule.Date(2020,2,20)
        self.assertEqual(ddh(ymd),rs)

        settings.convention = 'MDY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(ymd)
        settings.convention = 'DMY'
        with self.assertRaises(parsers.ParserStringsError):
            ddh(ymd)

        # # reset 
        settings.convention = 'MDY'
    
    def test_weirdDates(self):
        # convention is mdy

        with self.assertRaises(parsers.ParserStringsError):
            x = ddh('7/7/7')
        
        x = ddh('7/7/70')
        self.assertEqual(x,dateModule.Date(1970,7,7))

        with self.assertRaises(parsers.ParserStringsError):
            ddh('7770')

        with self.assertRaises(parsers.ParserStringsError):
            ddh('33553')
        
        with self.assertRaises(parsers.ParserStringsError):
            ddh('11553')
    
    def test_parseComboMDY(self):
        '''
            test combinations of m,d,y, where month can be 1,2,3 digits, 3 letter, 4 letter, full letter
            date can be 1,2,3,4,5 year 
            without slash,dash acceptable formats are: d:2digits,m:2digits,y:2,4 digits

            goal is to find the edge cases where it raises error when it is supposed to raise. In addition, the error is from disent error
            not from other errors from python package
        '''
        # without slashes,dashes
        dates = ['2','17','43','100','111']
        months = ['3','11','13','211','AUG','au','augu','august']
        years = ['5','23','211','2013','22414']
        months_full_name = ['January','February','March','April','May','June','July',
                            'August','September','October','November','December']
        # format mdy
        orig = 'MDY'
        settings.convention = orig
        combos = list(itertools.product(months,dates,years))
        combo_count = 0  # combo count should be same as len(combos) to cover the all scenarios
        for combo in combos:
            m,d,y = combo
            mdy = f'{m}{d}{y}'
            
            # m not month name 
            if not re.search('[a-zA-Z]',m):
                # combo of mdy can be m=1 d=113 y=2023 works so we need to find new mdy_new
                if len(mdy)==6 or len(mdy)==8:
                    # should be correct
                    mdy_new = f'{m}{d}{y}'
                    m2,d2,y2 = mdy_new[:2],mdy[2:4],mdy[4:]
                    combo_count +=1
                    if int(m2)>12 or int(m2)<1:
                        # month is wrong

                        with self.assertRaises(parsers.ParserStringsError):
                            ddh(mdy)
                        
                    elif int(d2)>31 or int(d2)<1:
                        # date is wrong
                        
                        with self.assertRaises(parsers.ParserStringsError):
                            ddh(mdy)
                    elif int(y2)<1000 and int(y2)>=100:
                        # eg y=0203
                        
                        with self.assertRaises(parsers.ParserStringsError):
                            ddh(mdy)
                    else:
                        # should not raise error
                        
                        ddh(mdy_new)
                else:
                    # should raise error
                    if len(mdy)<6 and len(mdy)>3:
                        # if less than 3 it wont match so parseError from dateMath
                        
                        with self.assertRaises(parsers.ParserStringsError):
                            ddh(mdy)
                    else:
                        
                        with self.assertRaises(parsers.ParserStringsError):
                            ddh(mdy)
                    combo_count+=1
            else:
                # m is correct month name 
                if len(m)==3 or m in months_full_name:  
                    dy_new = f'{d}{y}'
                    if len(dy_new)==4 or len(dy_new)==6:
                        # correct dy_new
                        d2,y2 = dy_new[:2],dy_new[2:]
                        combo_count+=1
                        if int(d2)>31 or int(d2)<1:
                            
                            with self.assertRaises(parsers.ParserStringsError):
                                ddh(mdy)
                        elif int(y2)<1000 and int(y2)>=100:
                            # eg y=0203
                            with self.assertRaises(parsers.ParserStringsError):
                                ddh(mdy)
                        else:
                            # it should not raise error
                            ddh(mdy)
                    else:
                        combo_count+=1
                        # will raise error parser
                        if len(dy_new)<4:
                            # raise value error 
                            with self.assertRaises(parsers.ParserStringsError):
                                ddh(mdy)
                        
                
                else:
                    combo_count+=1
                    # it will raise value error on month
                    with self.assertRaises(ValueError):
                        ddh(mdy)
        print(f'test_parseComboMDY:tested total of {combo_count} cases')
        self.assertEqual(combo_count,len(combos))

        # reset
        settings.convention = orig

                    

                    

            
            


        

        

        
        


    
        

if __name__=='__main__':
    unittest.main()