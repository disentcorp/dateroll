import datetime
from dateroll.ddh.ddh import ddh
import unittest

class Tests(unittest.TestCase):
    def testNothing(self):
        '''
        empty string
        '''
        try:
            x = ddh('')
        except TypeError as e:
            assert True

    def testDate(self):
        '''
        test for date strings
        '''
        assert ddh('t') == datetime.date.today() 
        assert ddh('5/5/5') == datetime.date(2005,5,5)

    def testDuration(self):
        '''
        test for duration strings
        '''
        

    def testSchedule1(self):
        '''
        test for schedule strings
        '''
        assert ddh('t')==datetime.date.today()



if __name__ == '__main__':
    # unittest.main()

    # print("answer:",ddh('3/1/24'))
    # print("answer:",ddh('t'))
    # print("answer:",ddh('-3m|NY'))
    # print("answer:",ddh('9m|NY+ -11m'))
    # print("answer:",ddh('9m|NY + 11m0bd|EU'))
    # print("answer:",ddh('-6m7y2d5q8w|NYuEUuWEuBRuMXuARuCONZ/MF'))
    # print("answer:",ddh('9m+6m7y2d5q8w|NYuEUuWEuBRuMXuARuCONZ/MF'))
    print("answer:",ddh('t+1bd'))
    # print("answer:",ddh('t-5bd'))
    # print("answer:",ddh('t-0bd'))
    # print("answer:",ddh('t+3m'))