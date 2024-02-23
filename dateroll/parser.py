import datetime
from dateroll.strings import match_datestring
from dateroll.strings import match_durationstring
from dateroll.strings import match_datemathstring

DEFAULT_CONVENTION = 'american'

class ParserError(Exception):
    ...

class Parser:
    '''
    Parser can process one of three strings:
    
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
                Duration        -   DateString      ->   raise Exce
                ption
                DurationString  -   DateString      ->   raise Exception
    '''
    possible_today_strings = ['t','t0','today']

    @classmethod
    def match_t(cls,s):
        '''
        this is [the] place where "t" is replaced
        '''
        today_string = datetime.date.today().strftime(r'%Y/%m/%d')
        for t in cls.possible_today_strings:
            str_no_t = s.replace('t',today_string)
        return str_no_t
        
    def __new__(
            self,
            s,
            convention = DEFAULT_CONVENTION,
            use_native_types = False
        ):
        '''
        Algorithm works left to right implicitly:
            1 - convert tString into DateString, swap in prinary string
            2 - [match] DateString, [parse] to Date, [store] in list l, [swap] in string for X
            3 - [match] DurationString, [parse] to Duration, [store] in list l, [swap] in string for X
            4 - if len(l)==1 and string=='' return l[0], otherwise 
                [match] DateMathString and perform math
        '''

        if convention != 'american':
            raise NotImplementedError('american only for now')
        if use_native_types:
            raise NotImplementedError('only dateroll types for now')
        
        self.convention = convention
        self.use_native_types = use_native_types

        #1
        s1 = Parser.match_t(s)

        #2        
        dates, s2 = match_datestring(s1)

        #4
        durations, s3 = match_datestring(s2)
        dates_durations = dates + durations

        #5
        # fund, arg_names = match_datemathstring(s3)
        # return processed_answer

        raise ParserError(f"Sorry, can't understand {s}") from None
    
def parse_to_native(string,convention=DEFAULT_CONVENTION):
    return Parser(string,convention=convention,use_native_types=True)

def parse_to_dateroll(string,convention=DEFAULT_CONVENTION):
    return Parser(string,convention=convention)