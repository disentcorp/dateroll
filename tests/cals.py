import tempfile
import os
import unittest
from dateroll.calendars.calendars import Calendars
from unittest import expectedFailure
import datetime
import pathlib
import uuid

class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename_base = pathlib.Path(tempfile.gettempdir()) / f"dateroll.testing.{uuid.uuid4()}"
        cls.cals = Calendars(home=cls.filename_base)

    @classmethod
    def tearDownClass(self):
        filename= str(self.filename_base)+'.db'
        os.remove(filename)


    def test_keys(self): k = self.cals.keys(); assert isinstance(k,list)

    @expectedFailure
    def test_tests1(self): self.cals['aaaa']=[]

    @expectedFailure
    def test_tests2(self): self.cals['aa']=[]
    
    @expectedFailure
    def test_tests3(self): self.self.cals['AA']=[]

    def test_tests4(self): self.cals['AA']=[]

    def test_tests5(self): del self.cals['AA']

    def test_tests6(self): self.cals['AA']=()
    
    @expectedFailure
    def test_tests7(self): self.cals['AA']=(1,)
    
    @expectedFailure
    def test_tests8(self): self.cals['AA']=(1,)
    
    def test_tests9(self): 
        dates = [datetime.date.today()]
        self.cals['BBB']= dates 
        assert self.cals['BBB'] == dates

if __name__ == '__main__':
    unittest.main()