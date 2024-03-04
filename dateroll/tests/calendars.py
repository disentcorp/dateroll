import datetime
import os
import pathlib
import tempfile
import unittest
import uuid
import code
import sys
from io import StringIO
from unittest import expectedFailure

from dateroll.calendars.calendars import Calendars,Drawer
import dateroll


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename_base = (
            pathlib.Path(tempfile.gettempdir())
            / f"dateroll.testing.{uuid.uuid4()}.cals"
        )
        cls.cals = Calendars(home=cls.filename_base)

    @classmethod
    def tearDownClass(self):
        filename = str(self.filename_base)
        os.remove(filename)

    def test_keys(self):
        """
        ensure the keys method is returning a list-like object
        """
        k = self.cals.keys()
        assert isinstance(k, list)

    @expectedFailure
    def test_tests1(self):
        self.cals["aaaa"] = []

    @expectedFailure
    def test_tests2(self):
        self.cals["aa"] = []

    @expectedFailure
    def test_tests3(self):
        self.self.cals["AA"] = []

    def test_tests4(self):
        del self.cals['AA']
        self.cals["AA"] = []

    def test_tests5(self):
        del self.cals["AA"]

    def test_tests6(self):
        self.cals["AA"] = ()

    @expectedFailure
    def test_tests7(self):
        self.cals["AA"] = (1,)

    @expectedFailure
    def test_tests8(self):
        self.cals["AA"] = (1,)

    def test_tests9(self):
        dates = [datetime.date.today()]
        self.cals["BBB"] = dates
        assert self.cals["BBB"] == dates
    
    def test_exitReturnTrue(self):
        '''
            context manager fails in the __exit__
        '''
        cals = Calendars()
        with Drawer(cals) as db:
            try:
                db.update('Hello')
            except Exception as e:
                exc_type,exc_value,exc_traceback = sys.exc_info()
        self.assertEqual(exc_type.__name__,'ValueError')
        
    def test_contains(self):
        '''
            test contains has a k in its dict keys
        '''
        cals = Calendars()
        cond = 'FED' in cals
        self.assertTrue(cond)
    
    def test_setitemkeyNonString(self):
        '''
            when setitem key is Non String should raise error
        '''
        with self.assertRaises(Exception) as context:
            self.cals[30] = []
        self.assertEqual(str(context.exception),'Cal name must be string (got int)')
    
    def test_setitemValWrong(self):
        '''
            when setitem val is not list,tuple,set
        '''
        with self.assertRaises(Exception) as context:
            self.cals['AA'] = 10
        
        self.assertEqual(str(context.exception),'Cal values must be a set/list/tuple (got int)')
    
    def test_seitemValDate(self):
        '''
            when we assign the list of datetime.date
        '''
        self.cals['AA'] = [dateroll.Date(2023,1,1)]
        self.assertTrue(dateroll.Date(2023,1,1) in self.cals['AA'])
    
    def test_seitemValDateTime(self):
        '''
            when we assign the list of datetime.datetime
        '''
        del self.cals['AA']
        self.cals['AA'] = [datetime.datetime(2023,1,1)]
        self.assertTrue(dateroll.Date(2023,1,1) in self.cals['AA'])

    def test_seitemValDateClass(self):
        '''
            when we assign the list of Date Class
        '''
        x = dateroll.Date(2020,1,1)
        self.cals['AB'] = [x]
        
        self.assertTrue(dateroll.Date(2020,1,1) in self.cals['AB'])
    
    def test_setitemValWrong2(self):
        '''
            when we assign the val which is not date related
        '''
        del self.cals['AA']
        with self.assertRaises(Exception) as context:
            self.cals['AA'] = ['20230101']
        self.assertEqual(str(context.exception),'All cal dates must be of dateroll.Date or datetime.date{time} (got str)')
    
    def test_setitemKeyExistsAlready(self):
        '''
            when the key already exists, it wont set the new value
        '''
        cals = Calendars()
        with self.assertRaises(Exception) as cm:
            cals['FED'] = [dateroll.Date(2024,2,1)]
        self.assertEqual(str(cm.exception),'FED exists already, delete first.if you want to replace.')
    
    def test_getattrNotHashHome(self):
        '''
            when the key of getattr not in (hash,home)
        '''
        cals = Calendars()
        x = cals.FED
        self.assertIsInstance(x,list)
        self.assertTrue(len(x)>0)
    
    def test_getattrHashHome(self):
        '''
            when the key of getattr in (hash,home)
        '''
        cals = Calendars()
        x = cals.__getattr__('home')
        # dont want to put home/batu in the result
        x = x.split('dateroll')[-1]
        self.assertEqual(x,'/calendars/holiday_lists')

    def test_delitem(self):
        '''
            test delitem of calendar
        '''
        self.cals['AA'] = [dateroll.Date(2023,2,1)]
        self.assertTrue('AA' in self.cals)
        del self.cals['AA']
        self.assertFalse('AA' in self.cals)
    
    def test_repr(self):
        '''
            test __repr__ of calendar
        '''
        expected_str = 'Calendars(home="/tmp/dateroll.'
        self.assertEqual(repr(self.cals).split('testing')[0],expected_str)
    
    def test_copy(self):
        '''
            the copy of the db should be as same as cals
        '''
        cals = Calendars()
        copy_db = cals.copy()
        self.assertTrue(copy_db,self.cals.db)
    
    def test_info(self):
        '''
            test the info of calendar
        '''
        cals = Calendars()
        capt = StringIO()
        sys.stdout = capt

        cals.info
        sys.stdout = sys.__stdout__

        printed_output = capt.getvalue()
        expected_output = 'name  |  #dates|min date    |max date    \n------|--------|------------|------------\nFED   |    4556|1824-01-01  |2223-12-25  \nECB   |    2400|1824-01-01  |2223-12-26  \nLN    |    3951|1824-01-01  |2223-12-26  \nWE    |   41742|1824-02-29  |2224-02-28  \nALL   |  146097|1824-02-29  |2224-02-28  \nBR    |    3586|1824-01-01  |2223-12-25  \nNY    |    4556|1824-01-01  |2223-12-25  \n'
        self.assertTrue(printed_output,expected_output)
    
    def test_clear(self):
        '''
            clear the db
        '''
        self.assertTrue(len(self.cals.db)>0)
        self.cals.clear()
        # dict becomes 0
        self.assertTrue(len(self.cals.db)==0)
    
    def test_emptyDBInfo(self):
        '''
            clear the db and show the info
        '''
       
        capt = StringIO()
        sys.stdout = capt

        self.cals.info
        sys.stdout = sys.__stdout__

        printed_output = capt.getvalue()
        expected_output = 'name  |  #dates|min date    |max date    \n------|--------|------------|------------\nFED   |    4556|1824-01-01  |2223-12-25  \nECB   |    2400|1824-01-01  |2223-12-26  \nLN    |    3951|1824-01-01  |2223-12-26  \nWE    |   41742|1824-02-29  |2224-02-28  \nALL   |  146097|1824-02-29  |2224-02-28  \nBR    |    3586|1824-01-01  |2223-12-25  \nNY    |    4556|1824-01-01  |2223-12-25  \n'
        self.assertTrue(printed_output,expected_output)
        self.cals.clear()
        self.cals['AC'] = []
        capt = StringIO()
        sys.stdout = capt

        self.cals.info
        sys.stdout = sys.__stdout__
        printed_output_empty = capt.getvalue()
        expected_output_empty = 'name  |  #dates|min date    |max date    \n------|--------|------------|------------\nAC    |       0|None        |None        \n'
        self.assertTrue(printed_output_empty,expected_output_empty)

    


        


        

if __name__ == "__main__":
    unittest.main()
