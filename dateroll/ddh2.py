import datetime
from dateroll.parser import parse_to_dateroll


def ddh(string):
    return parse_to_dateroll(string)

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
        assert oddh('t')==datetime.date.today()



if __name__ == '__main__':
    # unittest.main()

    print('3/1/24')
    print(ddh('t'))
    print(ddh('3m'))
    # print(ddh('t+3m'))