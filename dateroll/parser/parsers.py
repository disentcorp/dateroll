import traceback
import datetime
import re
import code

# from dateroll.date.date import Date

import dateroll.date.date as dt
import dateroll.duration.duration as dur
from dateroll.parser import patterns
from dateroll.schedule.schedule import Schedule
from dateroll import utils
from dateroll.settings import settings
import dateroll.parser.parser as parserModule
import calendar

TODAYSTRINGVALUES = ["today", "t0", "t"]

def validate_month(m):
    if m>12 or m<1:
        raise ValueError(f'month should be between [1,12] but {m}')

def validate_date(y,m,d):
    
    num_days = utils.get_month_days(y,m)
    # leapyear = lambda x: ((x%4==0) and (x%100!=0)) or x%400==0
    if m==2 and num_days==29:
        txt = f'Feb {y} has {num_days}(leapyear) the date {d} is out of range'
    else:
        txt = f'the date {d} is out of range'
    if d<1 or d>num_days:
        raise ValueError(txt)
    
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



def parseDateString(s):
    '''
    1950 is the cutoff for 2-digit years, i.e. 01 and 49 are 2001 and 2049 respectively
    50,99 are 1950 and 1999 respectively
    '''
    if not re.search(r'[-/]',s):
        if len(s)!=8:
            raise ValueError('Date without [-/] needs to have 8 digits,eg, yyyymmdd')
        if settings.convention == "MDY":
            m,d,y = s[:2],s[2:4],s[4:]
        elif settings.convention == "DMY":
            d,m,y = s[:2],s[2:4],s[4:]
                
        elif settings.convention == "YMD":
            y,m,d = s[:4],s[4:6],s[6:]
        y,m,d = int(y),int(m),int(d)
    else:
        s = s.replace('-','/')
        ls = [int(i) for i in s.split('/')]
        if settings.convention == "MDY":
            m,d,y = ls
        elif settings.convention == "DMY":
            d,m,y = ls
        elif settings.convention == "YMD":
            y,m,d = ls
    if y<100:
        # convert two digit year into 4 digit
        y = 2000+y if y<50 else 1900+y
    validate_month(m)
    validate_date(y,m,d)
    date_time = datetime.datetime(y,m,d)
    #     fmt = '%Y/%m/%d'
    # if not re.search(r'[-/]',s):
    #     if len(s)!=8:
    #         raise ValueError('Date without [-/] needs to have 8 digits,eg, yyyymmdd')
    #     s = re.sub(cpattern,r'\1/\2/\3',s)
    # else:
    #     # create dict e.g {Y:20,M:03,D:1} to find the Y without if statements
    #     s = s.replace('-','/')
    #     splitted = s.split('/')
    #     convention = [char for char in settings.convention]
    #     dic = {k:v for k,v in zip(convention,splitted)}
    #     if len(dic)!=len(convention):
    #         raise ValueError('Please check the convention matches with the date format')
    #     y,m,d = dic['Y'],dic['M'],dic['D']
    #     if len(y)==2:
    #         # convert two digit year into 4 digit
    #         y = f'20{y}' if int(y)<50 else f'19{y}'
    #     validate_month(m)
    #     validate_date(y,m,d)
    #     dic['Y'],dic['M'],dic['D'] = y,m,d
    #     s = '/'.join(list(dic.values()))
    # date_time = datetime.datetime.strptime(s,fmt)
    return date_time

    # if settings.convention=='YMD':
    #     fmt_string = '%Y/%m/%d'

    # if '/' not in s:
    #     raise ValueError('date string needs to have a format with dashes, e.g Y/m/d')
    
    # s2 = s.split('/')
    # if settings.convention=='YMD':
    #     fmt_string = '%Y/%m/%d'
    #     if len(s2[0])==2:
    #         # make year 4 digit
    #         s2[0] = f'20{s2[0]}'
    #         validate_month(s2[1])
    # else:
    #     if len(s2[-1])==2:
    #         # lis is mutable
    #         s2[-1] = f'20{s2[-1]}'
    #     if settings.convention=='MDY':
    #         fmt_string = '%m/%d/%Y'
    #         m = s2[0]
    #     else:
    #         fmt_string = '%d/%m/%Y'
    #         m = s2[1]
    #     validate_month(m)
        
    #     s = '/'.join(s2)  # 03/19/2024
    #     date_time = datetime.datetime.strptime(s, fmt_string)
    #     return date_time
    
    # if settings.convention=='YMD':
    #     fmt_string = '%Y/%m/%d'
    #     d = s[-2:]
    #     m = s[-4:-2]
    #     y = s[:-4]
    #     if len(y)==2:
    #         # to avoid the error of datetime.strptime which requires 4 digit in year
    #         y = f'20{y}'
    #     after = f'{y}/{m}/{d}'
    # elif settings.convention=='MDY':
    #     fmt_string = '%m/%d/%Y'
    #     m = s[:2]
    #     d = s[2:4]
    #     y = s[4:]
    #     if len(y)==2:
    #         y = f'20{y}'
    #     after = f'{m}/{d}/{y}'
    # elif settings.convention=='DMY':
    #     fmt_string = '%d/%m/%Y'
    #     d = s[:2]
    #     m = s[2:4]
    #     y = s[4:]
    #     if len(y)==2:
    #         y = f'20{y}'
    #     after = f'{d}/{m}/{y}'
    
    # validate_month(m)

    # date_time = datetime.datetime.strptime(after,fmt_string)

    # return date_time

def parseManyDateStrings(s,gen):
    """
    for a given convention, see if string contains 1 or 2 dates
    regex to extract string, and Date.from_string(), which calls dateutil.parser.parse

    valid DateStrings for refence:

        MDY: american: 1 or 2 digit month, 1 or 2 digit day, and 2 or 4 digit year
        DMY: european: 1 or 2 digit day, 1 or 2 digit month, and 2 or 4 digit year
        YMD: international: 2 or 4 digit year, 1 or 2 digit month, 1 or 2 digit day

    """
    
    if settings.convention == "MDY":
        pattern = patterns.MDY
    elif settings.convention == "DMY":
        pattern = patterns.DMY
    elif settings.convention == "YMD":
        pattern = patterns.YMD

    dates = {}
    matches = re.findall(pattern, s)
    res = s

    for match in matches:
        date_time = parseDateString(match)
        date = dt.Date.from_datetime(date_time)
        
        next_letter = next(gen()) # match only 1st time!! or causes letter mismatch
        res = res.replace(match, '+'+next_letter,1)
        dates[next_letter]=date

    
    
    return dates, res


def parseDurationString(m: tuple):
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
    else: # pragma:no cover
        raise Exception("Unknown operator")  

    # get all the pairs
    for i in range(2, 12, 2):
        number = m[i]
        unit = m[i + 1] 

        if number and unit:
            # cast number to integer y,s,q,m,w,d
            number = int(number) if unit!='bd' else float(number)
            if i < 4:
                # use multiplier on first pair
                number *= mult
            duration_contructor_args[unit] = number
    
    # attach calendars if any
    cals = m[13:21]
    
    # remove empty strings from cals
    cals = tuple(filter(lambda x:x!='',cals))
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
    
    duration = dur.Duration(**duration_contructor_args)
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
    
    for m in matches:
        duration = parseDurationString(m)
        dur_str = m[0]
        
        next_letter = next(gen())
        s = s.replace(dur_str,'+'+next_letter,1)
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
    
    for i in letters_used:
        if i not in things:
            print(s,things)
            raise ParserStringsError("Cannot recognize as date math", s)
    for j in things:
        if j.isalpha():
            if j not in letters_used:
                print(s,things)
                raise ParserStringsError("Cannot recognize as date math", s)
        
    # good case, do the math
    gs = {k: v for k, v in things.items()}
    try:
        total = eval(s,{},gs)
        return total
    except Exception as e:
        raise ParserStringsError("Cannot recognize as date math", s)

if __name__=='__main__':  # pragma: no cover
    s = ' A+B'
    s2 = ' +A+B -C'
    s3 = ' +A'
    things = {'A':4,'B':5}
    things2 = {'A':4}
    # rs = parseDateMathString(s,things)
    # print(rs)
    # rs = parseScheduleString('03012022,03302022,-1bd')
    # print(rs.dates)
    letters = [chr(i) for i in range(65, 65 + 26)]
    def gen():yield letters.pop(0)
    rs = parseManyDurationString('//1Y',gen)
    