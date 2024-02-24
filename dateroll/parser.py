import datetime
import dateutil
import dateutil.relativedelta
import dateutil.rrule

from dateroll import Date
from dateroll import Duration
from dateroll import Schedule

DEFAULT_CONVENTION = 'american'

class ParserError(Exception):
    ...

class Parser:
    '''

    Parser input/output:

        dateroll types:

        str -> dateroll.Date
        str -> dateroll.Duration
        str -> dateutil.Schedule

        or to python native types (with flag):
        
        str -> datetime.date
        str -> datetime.timedelta
        str -> dateutil.relativedelta.relativedelta
        str -> dateutil.rrule.rrule


    str "string" must one of the following formats:

        1 - TodayString (today's date)
        2 - DateString (represents a date)
        3 - DurationString (represents a duration)
        4 - DateMathString (e.g. date + duration, date - date, etc...)
        5 - DateScheduleString (represents a trip of end-to-end dates)

        ^^ details on each is in the subsequent parsing sub-fucntion

    Patterns:

        TodayString

            a   TodayString                         ->   DateString
    
        DateString:

            b   DateString                          ->   Date | datetime.date | datetime.datetime
        
        DurationString:

            c   DurationString                      ->   Duration | datetime.timedelta | datetime.relativedelta.relativedelta
        
        DateMathString (addition subtypes:)       

            d   DateString      +   Duration        ->   Date | datetime.date | datetime.datetime
            e   DurationString  +   DateString      ->   Date | datetime.date | datetime.datetime
            f   DurationString  +   DurationString  ->   Duration | datetime.timedelta | datetime.relativedelta.relativedelta
                Duration        +   DateString      ->   raise Exception
                DateString      +   DateString      ->   raise Exception    
        
        DateMathString (subtraction subtypes:)

            g   DateString      -   DateString      ->   Duration | datetime.timedelta | datetime.relativedelta.relativedelta
            h   DateString      -   Duration        ->   Date | datetime.date | datetime.datetime
            i   DurationString  -   DurationString  ->   Duration | datetime.timedelta | datetime.relativedelta.relativedelta   
                Duration        -   DateString      ->   raise Exception
                DurationString  -   DateString      ->   raise Exception

        DateScheduleString:

            j    DateString      ,   DateString      ,    Schedule | dateutil.rrule.rrule
            k    DateString      ,   DateMathString  ,    Schedule | dateutil.rrule.rrule
            l    DateMathString  ,   DateString      ,    Schedule | dateutil.rrule.rrule
                 DateMathString  ,   DateMathString  ,    Schedule | dateutil.rrule.rrule


    '''
    native_date = datetime.date
    native_delta = dateutil.relativedelta.relativedelta
    possible_today_strings = ['t','t0','today']

    @classmethod
    def parseTodayString(cls,s,convention=DEFAULT_CONVENTION):
        '''
        this is [the] place where "t" is replaced
        '''
        today = datetime.date.today()
        match convention:
            case 'american': today_string = today.strftime(r'%m/%d/%Y')
            case 'european': today_string = today.strftime(r'%d/%m/%Y')
            case 'international': today_string = today.strftime(r'%Y/%m/%d')

        for t in cls.possible_today_strings:
            if t in s:
                return s.replace(t,today_string)
        return s
        
    def __new__(
            self,
            s,
            convention = DEFAULT_CONVENTION,
            use_native_types = False
        ):
        '''
        Algorithm works left to right implicitly:
            1 - make + -> ++ and - -> +- to avoid conflict (note below)
            2 - convert tString into DateString, swap in prinary string
            3 - Check for how many parts (1 or 3 allowed), For each part:
                3a. Match DateString's -> Date
                3b. Match DurationString's -> Duration
                3c. Match DateMathString -> Date or Duration
        '''

        if not isinstance(s,str):
            raise ParserError('Must be string')

        if convention != 'american':
            raise NotImplementedError('american only for now')
        if use_native_types:
            raise NotImplementedError('only dateroll types for now')
        
        self.convention = convention
        self.use_native_types = use_native_types

        #1 replace minus with plusminus and plus with plusplus, 
        # this avoids conflict with DateMathString and DateDurationString
        s0 = s.replace('-','+-').replace('+','++')

        #2
        s1 = Parser.parseTodayString(s0)

        #3
        part = Parser.parse_maybe_many_parts(s1,convention=self.convention)        
        return part
    
    @classmethod
    def parse_one_part(cls,untouched,convention=DEFAULT_CONVENTION):
        ##### MOVE THESE HERE WHEN READY
        from dateroll.strings import parseDateString
        from dateroll.strings import parseDurationString
        from dateroll.strings import parseDateMathString

        #3a      
        dates, nodates = parseDateString(untouched,convention=convention)
        if nodates=='X':
            return dates[0]

        #3b
        durations, nodatesordurations = parseDurationString(nodates)
        if nodatesordurations=='X':
            return durations[0]
        dates_durations = dates + durations

        #3c
        processed_answer = parseDateMathString(nodatesordurations,dates_durations)
        return processed_answer
    
    @classmethod
    def parse_maybe_many_parts(cls,s,convention=DEFAULT_CONVENTION):
        parts = s.split(',')
        if not s:
            TypeError('No empty strings')
        num_parts = len(parts)

        match num_parts:
            case 1:
                part = parts[0]
                date_or_period = cls.parse_one_part(part,convention=convention)
                return date_or_period
            case 3:
                _maybe_start, _maybe_stop, _maybe_step = parts
                
                maybe_start = cls.parse_one_part(_maybe_start,convention=convention)
                maybe_stop = cls.parse_one_part(_maybe_stop,convention=convention)
                maybe_step = cls.parse_one_part(_maybe_step,convention=convention)

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
        
        raise ParserError(f"Sorry, can't understand {s}") from None

    
def parse_to_native(string,convention=DEFAULT_CONVENTION):
    return Parser(string,convention=convention,use_native_types=True)

def parse_to_dateroll(string,convention=DEFAULT_CONVENTION):
    return Parser(string,convention=convention)
