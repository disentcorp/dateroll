
import datetime
import re

import dateroll.date.date as dt
import dateroll.duration.duration as dur
from dateroll.parser import patterns
from dateroll.schedule.schedule import Schedule
from dateroll import utils
from dateroll.settings import settings
import calendar

TODAYSTRINGVALUES = ["today", "t0", "t"]

        
def validate_year(y):
    '''
        validate year using settings twodigityear_cutoff, and convert all 2-digit years to 4-digit
    '''

    len_y = len(str(y))
    if len_y == 3 or len_y >4:
        raise ParserStringsError(f'Year ({y}) must be 1, 2 (subject to cutoff setting) or 4 digits, not {len_y}')
    else:   
        if y < 100:
            cutoff = settings.twodigityear_cutoff
            if cutoff == 1900:
                adj = 1900
            elif cutoff == 2000:
                adj = 2000
            else:
                if y >= (cutoff - 2000):
                    adj = 1900
                else:
                    adj = 2000
        else:
            adj = 0
    return y + adj  

def validate_month(m):
    if m>12 or m<1:
        raise ParserStringsError(f'month should be between [1,12] but {m}')
    else:
        return m

def validate_monthday(y,m,d):
    num_days = utils.get_month_days(y,m)

    if d>num_days:
        msg = f"{calendar.month_name[m]}/{y} has {num_days} days (you're trying {d})."
        raise ParserStringsError(msg)
    if d < 1:
        raise ParserStringsError('Number of days must be a postive integer')

    return d
    
class ParserStringsError(Exception): ...

def parseTodayString(s):
    """
        this is [the] place where "t" is replaced
    """
    today = datetime.date.today()
    fmt = utils.convention_map[settings.convention]
    today_string = today.strftime(fmt)

    for t in TODAYSTRINGVALUES:
        # search order matters in TODAYSTRINGVALUES
        if t in s:
            return s.replace(t, today_string)
    return s


def parseDateString(s:str):
    '''
    takes string outputs date
    valid formats are:

    in either of 3 formats: MDY, YMD, or MDY
        one of two styles:

        1- with slashes and dashes:
            1 or 2 digit day
            1 or 2 digit month, or 3 letter or full name month
            No year limit

        2- without slashes and dashes:
            2 digit day
            2 digit month, or 3 letter or full name month
            2 or 4 digit year
    '''

    # swap month names for numbers
    s = utils.swap_month_names(s)

    if len(s) < 6:
        raise ValueError('Date string must be at least 6 chars')
    
    # slashes and dashes
    if '/' in s or '-' in s:
        # convert all to slash
        s = s.replace('-','/')
        # use slash as a splitter
        parts = s.split('/')
        # process according to convention
        y,m,d = parseDateString_rearrange(parts)
    else:
        # no slashes or dashes - more restrictive
        # either 6 digits or 8 digits forcing 2 digit month/day and 2 or 4 digit year according to user settings convention
        try:
            # lookup coords by convention and string length
            coords = utils.date_string_coordinates[settings.convention][len(s)]

            # map coords to string slicer, slice, then cast
            y = int(s[coords['y']])
            m = int(s[coords['m']])
            d = int(s[coords['d']])
        except:
            raise ParserStringsError('If no slashes or dashes, must be 2 digit year an dmonth, and 2 or 4 digit year in YMD format ONLY')

    # validate
    y = validate_year(y)
    m = validate_month(m)
    d = validate_monthday(y,m,d)
    
    # construct
    dte = dt.Date(year=y,month=m,day=d)

    return dte


def parseDateString_rearrange(tup):
    '''
    1950 is the cutoff for 2-digit years, i.e. 01 and 49 are 2001 and 2049 respectively
    50,99 are 1950 and 1999 respectively
    '''

    if settings.convention == "MDY":
        m,d,y = tup
    elif settings.convention == "DMY":
        d,m,y = tup
    elif settings.convention == "YMD":
        y,m,d = tup
    
    y,m,d = int(y),int(m),int(d)
    return y,m,d

def parseManyDateStrings(s,gen):
    """
    for a given convention, see if string contains 1 or more dates, extract them out for "letters" for parseDateMath

    it is a 2 pass process, once check for dates with regex, 2 actually check date in detail

    valid DateStrings for refence:

        MDY: american
        DMY: european
        YMD: international

        if using slashes or dashes as separators all of the above support:
        
        1 or 2 digit days
        1 or 2 digits months, or 3 letter or full named months
        1,2,3 or 4 digit years

        if using no slashes or dashes:
        
        2 digit days,
        2 digits months, or 3 letter or full named months
        2 or 4 digit years

    note: for excel and unix serial dates, use the Date.from_* methods with the values as integers, this is just string parsing.

    """
    # swap month names for numbers
    s = utils.swap_month_names(s)
    if settings.convention == "MDY":
        pattern = patterns.MDY
    elif settings.convention == "DMY":
        pattern = patterns.DMY
    elif settings.convention == "YMD":
        pattern = patterns.YMD
    
    dates = {}
    matches = re.findall(pattern, s)
    res = s
    
    for match,_,_,_ in matches:
        # must hav 4 components per match
        # match 0 is 1st capture group = whole thing
        # match 1,2,3 are the y/m/d's as strings
        
        date = parseDateString(match)
        date = dt.Date.from_datetime(date)
        next_letter = next(gen()) # match only 1st time!! or causes letter mismatch
        res = res.replace(match, '+'+next_letter,1)
        dates[next_letter]=date
    
    return dates, res


def parseDurationString_convert_capture_groups(capture_groups: tuple):
    """
    COMPLETE_DURATION regex matches a 23-item tuple
    This function extracts the parts and calls the Duration contructor appropriately
    Starts with empty, and adds as finds from incoming tuple
    """
    # operator becomes multiplier
    duration_constructor_args = {}

    # get initial multplier (if any)
    op = capture_groups[1]
    
    if op == "+" or op == "":
        mult = 1
    elif op == "-":
        mult = -1
    else: # pragma:no cover
        raise Exception(f"Unknown operator {op}")  

    # get all the pairs
    for i in range(2, 12, 2):
        number = capture_groups[i]
        unit = capture_groups[i + 1] 

        if number and unit:
            # cast number to integer y,s,q,m,w,d
            number = int(number) if unit!='bd' else float(number)
            if i < 4:
                # use multiplier on first pair
                number *= mult
            if unit in duration_constructor_args:
                raise ParserStringsError('Only 1 number of each unit per duration string (i.e. no 5d3d or 7m1m)')
            
            duration_constructor_args[unit] = number
    
    # attach calendars if any
    cals = capture_groups[13:21]
    
    # remove empty strings from cals
    cals = tuple(filter(lambda x:x!='',cals))
    for cal in cals:
        (
            duration_constructor_args.setdefault("cals", []).append(cal)
            if cal and cal.isupper()
            else None
        )

    # attach roll if any
    modified = capture_groups[22]
    if modified:
        duration_constructor_args["modified"] = True

    # add signed bd's if implicit scenario
    if 'bd' not in duration_constructor_args and 'BD' not in duration_constructor_args:
        if modified or len(cals) > 0:
            duration_constructor_args['bd'] = float(0.0)*mult
    
    duration = dur.Duration(**duration_constructor_args)
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

def parseDurationString(s:str):
        
    matches = re.findall(patterns.COMPLETE_DURATION, s)
    if len(matches)==0:
        raise ParserStringsError('No duration found')
    elif len(matches)>1:
        raise ParserStringsError('Multiple durations found, need 1')
    else:
        capture_groups = matches[0]
        dt = parseDurationString_convert_capture_groups(capture_groups)
        return dt
    

def parseManyDurationString(s,gen):
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
    durations = {}
    matches = re.findall(patterns.COMPLETE_DURATION, s)
    
    for match in matches:
        duration_string = match[0]
        duration = parseDurationString(duration_string)        
        next_letter = next(gen())
        s = s.replace(duration_string,'+'+next_letter,1)
        durations[next_letter] = duration
    return durations, s

def parseScheduleString(s):  # pragma: no cover
    """ """
    parts = s.split(',')
    num_parts = len(parts)
    if num_parts!=3:
        raise Exception(
                f"String must contain either 3 parts (not {num_parts})"
            )
    letters = [chr(i) for i in range(65, 65 + 26)]
    def gen():yield letters.pop(0)
    start,stop,step = parts
    dstart,_ = parseManyDateStrings(start,gen)
    dstop,_ = parseManyDateStrings(stop,gen)
    dstep,_ = parseManyDurationString(step,gen)
    if len(dstart)==0 or len(dstop)==0:
        raise ValueError(f'Please provide correct date format string')
    if len(dstep)==0:
        raise ValueError(f'Please provide correct duration format string')
    t1 = list(dstart.values())[0]
    t2 = list(dstop.values())[0]
    dur = list(dstep.values())[0]
    sch = Schedule(t1,t2,dur)
    return sch


def parseDateMathString(s, things):
    """
    Looks for any linear formula with plus or minus
    Uses substitution and evaluation. Safe because wouldn't get here if *things were not validated, and regex didn't match.
    """

    letters_used = re.findall(r'[A-Z]',s)
    
    # bad case, letter mismatch
    if len(things)==0:
        
        raise ParserStringsError("Cannot perform date math")
    for i in letters_used:
        if i not in things:
            raise ParserStringsError("Cannot recognize as date math", s)
    for j in things:
        if j.isalpha():
            if j not in letters_used:
                raise ParserStringsError("Cannot recognize as date math", s)

    # good case, do the math
    
    try:
        total = eval(s,{},things)
        return total
    except Exception as e:
        raise ParserStringsError("Cannot recognize as date math", s)


    
    