import unittest
import code

from dateroll.settings import settings
from dateroll.parser.parser import Parser, parse_to_native
from dateroll.date.date import Date
from dateroll.duration.duration import Duration
class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_new(self):
        '''
            tests things in __new__
        '''

        # only accepts string
        with self.assertRaises(Exception) as cm:
            pars = Parser(10)
        self.assertEqual(str(cm.exception),'Must be string')

        
        with self.assertRaises(NotImplementedError):
            Parser('s',use_native_types=True)
    
    def test_parse_one_part(self):
        '''
            test parse one part
        '''
        original = settings.convention
        try:
            settings.convention = 'YMD'
            
            dt = Parser.parse_one_part('20240101')
            self.assertEqual(dt,Date(2024,1,1))

            dur = Parser.parse_one_part('3m')
            
            self.assertEqual(dur,Duration(years=0, months=3, days=0, modified=False, debug=False))

            dt_dur = Parser.parse_one_part('20240101+3m')
            
            self.assertEqual(dt_dur,Date(2024,4,1))
        finally:
            settings.convention = original
    
    def test_maybe_many_parts(self):
        '''
            test parse maybe many parts accepts 1 part or 3 parts (start,stop,step)
        '''


        # 1 part
        dt = Parser.parse_maybe_many_parts('20240101')
        self.assertEqual(dt,Date(2024,1,1))

        # 3 parts - valid schedule generation
        dts = Parser.parse_maybe_many_parts('20240101,20240201,1bd')
        self.assertEqual(dts[0],Date(2024,1,1))
        self.assertEqual(dts[-1],Date(2024,2,1))
        self.assertEqual(len(dts),24)

        # 3 parts 1st part wrong
        with self.assertRaises(TypeError):
            dt = Parser.parse_maybe_many_parts('3m,t,1m')

        # 3 parts 2nd part wrong
        with self.assertRaises(TypeError):
            dt = Parser.parse_maybe_many_parts('t,3m,1m')

        # 3 parts 3rd part wrong
        with self.assertRaises(TypeError):
            dt = Parser.parse_maybe_many_parts('t,t+3m,t-1d')
            
        # parts stub
        dt = Parser.parse_maybe_many_parts('t,t+2m15d,1m')

        # 2 parts are wrong
        with self.assertRaises(Exception):
            dt = Parser.parse_maybe_many_parts('t,t+3m')
        

        # use_native NotImplmented for now
        with self.assertRaises(NotImplementedError):
            dt = parse_to_native('t')

    

if __name__=='__main__':
    unittest.main()