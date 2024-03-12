import datetime
import re
import code

# from dateroll.date.date import Date

import dateroll.date.date as dt
import dateroll.duration.duration as dur
from dateroll.parser import patterns
from dateroll.schedule.schedule import Schedule

DEFAULT_CONVENTION = "MDY"
TODAYSTRINGVALUES = ["today", "t0", "t"]

AtoZ = tuple(chr(i) for i in range(65, 65 + 26))


class ParserStringsError(Exception): ...


def parseTodayString(s, convention=DEFAULT_CONVENTION, debug=False):
    """
        this is [the] place where "t" is replaced
    """
    today = datetime.date.today()
    if convention == "MDY":
        today_string = today.strftime(r"%m/%d/%Y")
    elif convention == "DMY":
        today_string = today.strftime(r"%d/%m/%Y")
    elif convention == "YMD":
        today_string = today.strftime(r"%Y/%m/%d")
    else:
        raise ValueError(convention)

    for t in TODAYSTRINGVALUES:
        # search order matters in TODAYSTRINGVALUES
        if t in s:
            if debug:
                print('MATCH(ES) FOR TODAY',t,s)
            return s.replace(t, today_string)
    return s


def parseDateString(s, convention, debug=False):
    """
    for a given convention, see if string contains 1 or 2 dates
    regex to extract string, and Date.from_string(), which calls dateutil.parser.parse

    valid DateStrings for refence:

        MDY: american: 1 or 2 digit month, 1 or 2 digit day, and 2 or 4 digit year
        DMY: european: 1 or 2 digit day, 1 or 2 digit month, and 2 or 4 digit year
        YMD: international: 2 or 4 digit year, 1 or 2 digit month, 1 or 2 digit day

    """
    
    if convention is None:
        convention = DEFAULT_CONVENTION

    if convention == "MDY":
        pattern = patterns.MDY
        dateparser_kwargs = {}
    elif convention == "DMY":
        pattern = patterns.DMY
        dateparser_kwargs = {"dayfirst": True}
    elif convention == "YMD":
        pattern = patterns.YMD
        dateparser_kwargs = {"yearfirst": True}
    else:
        raise ParserStringsError("No convention provided!")

    dates = []
    matches = re.findall(pattern, s)

    res = s
    for match in matches:
        date = dt.Date.from_string(match, **dateparser_kwargs)
        res = res.replace(match, "X")
        dates.append(date)

    return dates, res


def process_duration_match(m: tuple, debug=False):
    """
    COMPLETE_DURATION regex matches a 23-item tuple
    This function extracts the parts and calls the Duration contructor appropriately
    Starts with empty, and adds as finds from incoming tuple
    """
    # operator becomes multiplier
    duration_contructor_args = {}

    # get initial multplier (if any)
    op = m[1]
    if op == "+" or op == "":
        mult = 1
    elif op == "-":
        mult = -1
    else:
        raise Exception("Unknown operator")

    # get all the pairs
    for i in range(2, 12, 2):
        number = m[i]
        unit = m[i + 1]

        if number and unit:
            # cast number to integer y,s,q,m,w,d
            number = int(number)
            if i < 4:
                # use multiplier on first pair
                if unit=='bd':
                    
                    number = float(number) * mult
                else:
                    number *= mult

            duration_contructor_args[unit] = number
    
    # attach calendars if any
    cals = m[13:21]
    for cal in cals:
        (
            duration_contructor_args.setdefault("cals", []).append(cal)
            if cal and cal.isupper()
            else None
        )

    # attach roll if any
    modified = m[22]
    if modified:
        duration_contructor_args["modified"] = True

    # add signed bd's if implicit scenario
    if 'bd' not in duration_contructor_args and 'BD' not in duration_contructor_args:
        if modified or len(cals) > 0:
            duration_contructor_args['bd'] = float(0.0)*mult
    
    duration = dur.Duration(**duration_contructor_args, debug=debug)
    return duration

def parseCalendarUnionString(s):
    '''
    use regex for validation of calendar string, if valid, then split on 'u' is SAFE
    '''
    matches = re.match(patterns.CALS,s)
    if matches:
        cals = tuple(sorted(s.split('u')))
        return cals
    else:
        raise Exception(f'{s} not a valid calendar string')

def parseDurationString(s,debug=False):
    """
    check for any DurationString:

        units:      1-9
        period's:   d,D day
                    bd,BD business day
                    w,W week
                    m,M month
                    q,Q quarter
                    y,Y year
        e.g. 1d, or 3M, or 9Y

        they can repeat: 1y3m9d = 1y + 3m + 9d

        calendars after |
            calendar as any uppercase 2 letter combo that map's to installed calendars
                WE -> by default is weekend calendar (list of all sat and sun from -100y to +100y)
                NY -> new york federal holidays
                EU -> ECB holidays
            calender unions: repreating calendars with "u" for union
                WEuNY -> all weekend holidays + NY holidays
                WUuNYuEU -> union of all 3 sets
        modifier after  /
                /MOD means modified the direction of travel for bd's to stay in current month
    """
    durations = []
    matches = re.findall(patterns.COMPLETE_DURATION, s)
    for m in matches:
        duration = process_duration_match(m, debug=debug)
        dur_str = m[0]
        s = s.replace(dur_str,'+X')
        durations.append(duration)
    
    return durations, s


def parseDateMathString(s, things, debug=False):
    """
    Looks for any linear formula with plus or minus
    Uses substitution and evaluation. Safe because wouldn't get here if *things were not validated, and regex didn't match.
    """
    before = s
    s = s.replace(" ", "").replace("++", "+").replace("+-", "-").replace("-+", "-")
    
    if s == "+X":
        s = "X"

    math_matches = re.match(patterns.MATH, s)
    if math_matches:
        n1 = len(things)
        n2 = s.count("X")
        
        if n1 > len(AtoZ):
            raise ParserStringsError("Cannot recognize as date math", s)
        
        if n1 != n2:
            raise Exception(f"Unmatched math ({s})")

        for idx in range(n2):
            s = s.replace("X", AtoZ[idx], 1)

        gs = {k: v for k, v in zip(AtoZ[: len(things)], things)}
        
        if debug:
            print('debug date math string (before eval)',before,s)

        total = eval(s,{},gs)
        
        return total
    
    raise ParserStringsError("Cannot recognize as date math", s)


def parseScheduleString(s,debug=False):  # pragma: no cover
    """ """
    raise NotImplementedError

if __name__=='__main__':  # pragma: no cover
    ...
     