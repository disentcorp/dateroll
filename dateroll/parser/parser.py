import datetime
import dateutil
import dateutil.relativedelta
import dateutil.rrule
import code

# from dateroll.date.date import Date
import dateroll.date.date as dateModule
# from dateroll.duration.duration import Duration
import dateroll.duration.duration as durationModule
from dateroll.parser import parsers
from dateroll.schedule.schedule import Schedule


class ParserError(Exception): ...


class Parser:
    """

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


    """

    native_date = datetime.date
    native_delta = dateutil.relativedelta.relativedelta

    def __new__(
        self, string, use_native_types=False,
    ):
        """
        Algorithm works left to right implicitly:
        Check for how many parts (1 or 3 allowed, "," separator)
        For each part
            1 - convert TodayStrings into DateStrings
            2 Match DateString's -> Date
            3 Match DurationString's -> Duration
            4 Match DateMathString -> Date or Duration
        """

        if not isinstance(string, str):
            raise ParserError("Must be string")

        if use_native_types: 
            raise NotImplementedError("only dateroll types for now")

        self.use_native_types = use_native_types
        
        
        part = Parser.parse_maybe_many_parts(string)
        return part

    @classmethod
    def parse_one_part(cls, untouched):
        letters = [chr(i) for i in range(65, 65 + 26)]
        def gen():yield letters.pop(0)
        # 1
        notoday = parsers.parseTodayString(untouched)

        # 2
        dates, nodates = parsers.parseDateString(notoday,gen)
        # print('s before/after:', untouched,nodates)

        # 3
        durations, nodatesordurations = parsers.parseDurationString(nodates,gen)
        # print('s before/after:', nodates,nodatesordurations)
        dates_durations = {**dates,**durations}
        
        # 4
        # print('before pdms',nodatesordurations)
        processed_answer = parsers.parseDateMathString(
            nodatesordurations, dates_durations
        )
        return processed_answer

    @classmethod
    def parse_maybe_many_parts(cls, s):
        parts = s.split(",")
        if not s:
            TypeError("No empty strings")

        num_parts = len(parts)

        if num_parts == 1:
            part = parts[0]
            date_or_period = cls.parse_one_part(part)
            return date_or_period

        elif num_parts == 3:
            _maybe_start, _maybe_stop, _maybe_step = parts

            maybe_start = cls.parse_one_part(_maybe_start)
            maybe_stop = cls.parse_one_part(_maybe_stop)
            maybe_step = cls.parse_one_part(_maybe_step)

            if isinstance(maybe_start, dateModule.Date):
                start = maybe_start
            else:
                raise TypeError("Start of generation must be a valid Date")

            if isinstance(maybe_stop, dateModule.Date):
                stop = maybe_stop
            else:
                raise TypeError("Stop of generation must be a valid Date")

            if isinstance(maybe_step, durationModule.Duration):
                step = maybe_step
            else:
                raise TypeError("Step of generation must be a valid Duration")

            sch = Schedule(start=start, stop=stop, step=step, origin_string=s)
            return sch

        else:
            # Must
            raise Exception(
                f"String must contain either 1 or 3 parts (not {num_parts})"
            )

        


def parse_to_native(string):
    return Parser(string, use_native_types=True)


def parse_to_dateroll(string):
    return Parser(string)
