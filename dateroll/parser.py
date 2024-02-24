import datetime
import dateutil
import dateutil.relativedelta
import dateutil.rrule

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
            1 - convert tString into DateString, swap in prinary string
            2 - [match] DateString, [parse] to Date, [store] in list l, [swap] in string for X
            3 - [match] DurationString, [parse] to Duration, [store] in list l, [swap] in string for X
            4 - if len(l)==1 and string=='' return l[0], otherwise 
                [match] DateMathString and perform math
        '''

        if not isinstance(s,str):
            raise ParserError('Must be string')

        if convention != 'american':
            raise NotImplementedError('american only for now')
        if use_native_types:
            raise NotImplementedError('only dateroll types for now')
        
        self.convention = convention
        self.use_native_types = use_native_types

        #1
        s1 = Parser.parseTodayString(s)
        
        ##### MOVE THESE HERE WHEN READY
        from dateroll.strings import parseDateString
        from dateroll.strings import parseDurationString
        from dateroll.strings import parseDateMathString


        #2        
        dates, s2 = parseDateString(s1,self.convention)
        if s2=='X':
            return dates[0]

        #4
        durations, s3 = parseDurationString(s2)
        if s3=='X':
            return durations[0]
        dates_durations = dates + durations

        #5
        # fund, arg_names = match_datemathstring(s3)
        # return processed_answer

        raise ParserError(f"Sorry, can't understand {s}") from None
    
def parse_to_native(string,convention=DEFAULT_CONVENTION):
    return Parser(string,convention=convention,use_native_types=True)

def parse_to_dateroll(string,convention=DEFAULT_CONVENTION):
    return Parser(string,convention=convention)




### SCHEDULE CODE FOR LATER


# from dateutil.parser import parse
# import datetime
# from dateroll import Date,Duration,Schedule
# from dateroll.ddh import ddh as oddh

# from dateroll.parser import parse_to_dateroll
# from dateroll.parser import parse_to_native

        
#         parts = some_string.split(',')
#         if some_string == '':
#             TypeError('No empty strings')
#         num_parts = len(parts)

#         match num_parts:
#             case 1:
#                 part = parts[0]
#                 date_or_period = parse_to_dateroll(part,convention=self.convention)
#                 return date_or_period
#             case 3:
#                 _maybe_start, _maybe_stop, _maybe_step = parts
                
#                 maybe_start = parse_to_dateroll(_maybe_start,convention=self.convention)
#                 maybe_stop = parse_to_dateroll(_maybe_stop,convention=self.convention)
#                 maybe_step = parse_to_dateroll(_maybe_step,convention=self.convention)

#                 if isinstance(maybe_start,Date):
#                     start = maybe_start
#                 else:
#                     raise TypeError('Start of generation must be a valid Date')
                
#                 if isinstance(maybe_stop,Date):
#                     stop = maybe_stop
#                 else:
#                     raise TypeError('Stop of generation must be a valid Date')
                
#                 if isinstance(maybe_step,Duration):
#                     step = maybe_step
#                 else:
#                     raise TypeError('Step of generation must be a valid Duration')

#                 sch = Schedule(start=start,stop=stop,step=step)
#                 return sch

#             case _:
#                 # Must 
#                 raise Exception(f'String must contain either 1 or 3 parts (not {num_parts})')