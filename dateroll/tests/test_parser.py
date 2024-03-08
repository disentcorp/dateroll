import unittest
import code

from dateroll.parser.parser import Parser
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
        convention = 'MDY'
        dt = Parser.parse_one_part('20240101',convention=convention)
        self.assertEqual(dt,Date(2024,1,1))

        dur = Parser.parse_one_part('3m',convention=convention)
        self.assertEqual(dur,Duration(years=0, months=3, days=0))

        dt_dur = Parser.parse_one_part('20240101+3m',convention=convention)
        
        self.assertEqual(dt_dur,Date(2024,4,1))
    
    def test_maybe_many_parts(self):
        '''
            test parse maybe many parts accepts 1 part or 3 parts (start,stop,step)
        '''
        
        convention = 'MDY'

        # 1 part
        dt = Parser.parse_maybe_many_parts('20240101',convention=convention)
        self.assertEqual(dt,Date(2024,1,1))

        # 3 parts
        dts = Parser.parse_maybe_many_parts('20240101,20240201,1bd',convention=convention)
        
        self.assertEqual(dts[0],Date(2024,1,1))
        self.assertEqual(dts[-1],Date(2024,2,1))
        self.assertEqual(len(dts),24)

        


    

if __name__=='__main__':
    unittest.main()