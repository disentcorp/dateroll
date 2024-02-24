import re
from dateroll import regex
from dateroll import Date
from dateroll import Duration
from dateroll import Schedule

class ParserStringsError(Exception):
    ...

def parseDateString(s,convention):
    '''
    for a given convention, see if string contains 1 or 2 dates
    regex to extract string, and Date.from_string(), which calls dateutil.parser.parse

    valid DateStrings for refence:

        american: 1 or 2 digit month, 1 or 2 digit day, and 2 or 4 digit year
        european: 1 or 2 digit day, 1 or 2 digit month, and 2 or 4 digit year
        international: 2 or 4 digit year, 1 or 2 digit month, 1 or 2 digit day

    '''

    match convention:
        case 'american': 
            pattern = regex.MDY
            dateparser_kwargs = {}
        case 'european': 
            pattern = regex.DMY
            dateparser_kwargs = {'dayfirst':True}
        case 'international': 
            pattern = regex.YMD
            dateparser_kwargs = {'yearfirst ':True}
    
    dates = []
    matches =re.findall(pattern,s)

    if len(matches)>2:
        raise Exception('Too many dates')
    
    for match in matches:
        date = Date.from_string(match,**dateparser_kwargs)
        s = s.replace(match,'X')
        dates.append(date)

    return dates,s

def process_duration_match(m:tuple):
    '''
    COMPLETE_DURATION regex matches a 23-item tuple
    This function extracts the parts and calls the Duration contructor appropriately
    Starts with empty, and adds as finds from incoming tuple
    '''
    # operator becomes multiplier
    duration_contructor_args = {}

    # get initial multplier (if any)
    op = m[1]
    match op:
        case ''|'+': mult=1
        case '-': mult = -1
        case '_': raise Exception('Unknown operator')
    
    # get all the pairs
    for i in range(2,12,2):
        number = m[i] 
        unit = m[i+1]

        if number and unit:
            # cast number to integer
            number = int(number)
            if i>2:
                # use multiplier on first pair
                number *= mult

            duration_contructor_args[unit]=number

    # attach calendars if any
    cals = m[13:21]
    for cal in cals:
        duration_contructor_args.setdefault('cals',[]).append(cal) if cal and cal.isupper() else None

    # attach roll if any
    roll = m[22]
    if roll:
        duration_contructor_args['roll']=roll

    duration = Duration(**duration_contructor_args)
    return duration


def parseDurationString(s):
    '''
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

        modifiers after |
            roll convention:
                /F following
                /P previous
                /MF modified following
                /MP modified previous
            calendar as any uppercase 2 letter combo that map's to installed calendars
                WE -> by default is weekend calendar (list of all sat and sun from -100y to +100y)
                NY -> new york federal holidays
                EU -> ECB holidays
            calender unions: repreating calendars with "u" for union
                WEuNY -> all weekend holidays + NY holidays
                WUuNYuEU -> union of all 3 sets
    '''
    durations = []
    matches = re.findall(regex.COMPLETE_DURATION,s)

    if len(matches)>2:
        raise Exception('Too many dates')
    
    for m in matches:
        full = m[0]
        duration = process_duration_match(m)
        s = s.replace(m[0],'X')
        durations.append(duration)

    return durations,s


def parseDateMathString(s):
    '''
    '''
    result = ''
    return result

def parseScheduleString(s):
    '''
    '''
    return s
