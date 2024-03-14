import code
import unittest
import os

import dateroll.parser.parsers as parsers
import datetime
from dateroll.settings import Settings,path
from dateroll.date.date import Date
from dateroll.duration.duration import Duration


class TestSettings(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_init(self):
        '''
            test init of settings
        '''
        
        settings = Settings()
        settings.load_default()
        
        self.assertEqual(settings.convention,'MDY')

        os.remove(path)
        settings = Settings()
        self.assertEqual(settings.convention,'MDY')
    
    def test_load(self):
        settings = Settings()
        settings.load_default()
        settings.load()
        self.assertEqual(settings.convention,'MDY')
        
    
    def test_validate(self):
        settings = Settings()
        settings.convention = 'YMD'
        settings.validate()
        self.assertEqual(settings.convention,'YMD')
        settings.convention = 'MDY'
        # settings.new = 'helloo'
        settings.validate()

    def test_setattr(self):
        settings = Settings()
        with self.assertRaises(Exception):
            settings.debug = 'hello'
    
    def test_repr(self):
        settings = Settings()
        x = repr(settings)


if __name__=='__main__':
    unittest.main()