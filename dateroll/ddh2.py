from dateutil.parser import parse
import datetime
from dateroll import Date,Duration,Schedule
from dateroll.ddh import ddh as oddh

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

    def __init__(self,some_string):

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
                date_or_period = DateStringProcessor(part)
                return date_or_period
            case 3:
                _maybe_start, _maybe_stop, _maybe_step = parts
                
                maybe_start = DateStringProcessor(_maybe_start)
                maybe_stop = DateStringProcessor(_maybe_stop)
                maybe_step = DateStringProcessor(_maybe_step)

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

class DateStringProcessor:
    '''

    A DateStringProcessor can process one of three strings:
    
        1 - DateString (eg "1/2/93")
        2 - DurationString (eg "-3m/MF}")
        3 - DateMathString (combination of 1 and 2 above with +/-)
            't-1bd|NY'  DateStringProcessor('1bd') - 
            '3y+5/5/5'

    Up to 9 valid patterns with type detections (a-h below, 4 are invalid patterns):

        tString
            a   tString                             -> DateString
    
        DateString:

            b   DateString                          ->   Date
        
        DurationString:
            c   DurationString                      ->   Duration
        
        DateMathString (addition)                 
            d   DateString      +   Duration        ->   Date
            e   DurationString  +   DateString      ->   Date
            f   DurationString  +   DurationString  ->   Duration
                Duration        +   DateString      ->   raise Exception
                DateString      +   DateString      ->   raise Exception    
        
        DateMathString (subtraction)
            g   DateString      -   DateString      ->   Duration
            h   DateString      -   Duration        ->   Date
            i   DurationString  -   DurationString  ->   Duration   
                Duration        -   DateString      ->   raise Exception
                DurationString  -   DateString      ->   raise Exception
    '''

    @staticmethod
    def match_t(s):
        '''
        this is [the] place where "t" is replaced
        '''
        today_string = datetime.date.today().strftime(r'%Y/%m/%d')
        str_no_t = s.replace('t',today_string)
        return str_no_t
        
    def __new__(self,s):
        '''
        Algorithm works left to right implicitly:
            1 - convert tString into DateString, swap in prinary string
            2 - try date parser directly (performance cheat)
            3 - [match] DateString, [parse] to Date, [store] in list l, [swap] in string for X
            4 - [match] DurationString, [parse] to Duration, [store] in list l, [swap] in string for X
            5 - if len(l)==1 and string=='' return l[0], otherwise 
                [match] DateMathString and perform math
        '''

        #1
        str_no_t = DateStringProcessor.match_t(s)

        #2
        try:
            return Date.from_string(s)
        except:
            pass

        #3

        #4

        #5
        

        


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
    unittest.main()