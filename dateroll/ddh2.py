from dateutil.parser import parse
import datetime
from dateroll import Date,Duration,Schedule
from dateroll.ddh import ddh as oddh

from dateroll.parser import parse_to_dateroll
from dateroll.parser import parse_to_native

class ddh:
    '''
    ddh is designed for people working with rule-based Gregorian dates. 
    It is built for uses in financial settings where dates are typically no older than 100 years, or no further out than 100 years.
    This means we get to ignore BCE, historical calendar changes (like before 1582, or when the Romans's added January and February to cover the full lunar year).

    credit to the python datetime library, dateutil library, and countless others.

    ddh itself is very light, it just splits into 1 or 3 pieces for processing
    ddh takes some_string and return either a Date, Duration, or Schedule

    features
        - string parsing
        - date algebra
        - date adjustment logic
        - schedule generation
    
    some_string can take 2 forms:
        1) no commas -> 1 "part"
            Date parsing
            Duration parsing
            Date algebra parsing
        2) two commas -> 3 "parts" 
            Schedule generation
    
    where each "part" is passed to DateStringProcessor

    Note:
        american (monthfirst) - default
        european (dayfirst) - TBD
        international (yearfirst) - TBD
    '''

    convention = 'american'

    def __new__(self,some_string):

        if self.convention == 'european':
            raise NotImplementedError('European dates')
        elif self.convention == 'international':
            raise NotImplementedError('Year first')
        
        parts = some_string.split(',')
        if some_string == '':
            TypeError('No empty strings')
        num_parts = len(parts)

        match num_parts:
            case 1:
                part = parts[0]
                date_or_period = parse_to_dateroll(part,convention=self.convention)
                return date_or_period
            case 3:
                _maybe_start, _maybe_stop, _maybe_step = parts
                
                maybe_start = parse_to_dateroll(_maybe_start,convention=self.convention)
                maybe_stop = parse_to_dateroll(_maybe_stop,convention=self.convention)
                maybe_step = parse_to_dateroll(_maybe_step,convention=self.convention)

                if isinstance(maybe_start,Date):
                    start = maybe_start
                else:
                    raise TypeError('Start of generation must be a valid Date')
                
                if isinstance(maybe_stop,Date):
                    stop = maybe_stop
                else:
                    raise TypeError('Stop of generation must be a valid Date')
                
                if isinstance(maybe_step,Duration):
                    step = maybe_step
                else:
                    raise TypeError('Step of generation must be a valid Duration')

                sch = Schedule(start=start,stop=stop,step=step)
                return sch

            case _:
                # Must 
                raise Exception(f'String must contain either 1 or 3 parts (not {num_parts})')

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

    # print('3/1/24')
    # print(ddh('t'))
    print(ddh('3m'))
    # print(ddh('t+3m'))