import re

PTNW = r'\bt0\b|\bt\b|\bT\b|\btoday\b|\bToday\b|\bTODAY\b'
PTN = r'[0-9][0-9]?[0-9]?[0-9]?\/?\-?\.?\ ?[0-9]?[0-9]?[0-9]?[0-9]?[a-zA-Z]?[a-z]?[a-z]?\/?\-?\.?\ ?[0-9][0-9]?[0-9]?[0-9]?'
OPERATOR=r" ?(\+|-) ?"
INT_PART = r'\d+'
OPTIONAL_DECIMAL = r'(?:\.|\.\d+)?'
NUMBER = f'{INT_PART}{OPTIONAL_DECIMAL}'

# DurationString Patterns
PERIOD_LETTER = r'(?:cd|CD|bd|BD|[dDwWmMqQsShHyY])'
DATE_PERIOD = f"(?:({NUMBER})({PERIOD_LETTER}))"
REPEATING_DATE_PERIODS = f"(?:{DATE_PERIOD}{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?)"
PIPE = r'\|'
TWOLETTERCAL = r'[A-ZA-Z][A-ZA-Z]'
REPEATING_CALUNIONS = f" ?{PIPE} ?({TWOLETTERCAL})(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?"
PIPE_REPEAT_CAL_UNION = f"(?:{REPEATING_CALUNIONS})?"
ROLL = r' ?/ ?(MF|MP|F|P) ?'
PIPE_ROLL = f"(?:{ROLL})?"
RHS_PATTERN = f"{OPERATOR}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION}{PIPE_ROLL}"
MATCH_WITH_DTPERIOD = f"(.*)(?= ?){RHS_PATTERN}"
MATCH_WITHORWITHOUT_DTPERIOD = f"(?:{MATCH_WITH_DTPERIOD})|(.*)"
FULL_PATTERN=MATCH_WITHORWITHOUT_DTPERIOD
PIPE_2 = r'(\|)?'
TWOLETTERCAL_2 = r'[u]?[A-ZA-Z][A-ZA-Z]'
REPEATING_CALUNIONS_2 = f" ?(?:{PIPE_2}) ?({TWOLETTERCAL_2})({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?"
ROLL_2 = r' ?(/)? ?(MF|MP|F|P) ?'
PIPE_ROLL_2 = f"(?:{ROLL_2})?"
PIPE_REPEAT_CAL_UNION_2 = f"(?:{REPEATING_CALUNIONS_2})?"
OPERATOR_2 = r" ?(\+|-)? ?"
RHS_PATTERN_2 = f"{OPERATOR_2}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION_2}{PIPE_ROLL_2}"

# DateString Patterns (rough patterns, parser does validation)
ONE_OR_TWO_DIGIT = r'(?:\d|\d\d)'
TWO_OR_FOUR_DIGIT = r'(?:\d\d|\d\d\d\d)'
DASH_SLASH_NONE = r'(?:-|/|\A\Z)'
YMD = f'({TWO_OR_FOUR_DIGIT}){DASH_SLASH_NONE}({ONE_OR_TWO_DIGIT}){DASH_SLASH_NONE}({ONE_OR_TWO_DIGIT})'
MDY = f'({ONE_OR_TWO_DIGIT}){DASH_SLASH_NONE}({ONE_OR_TWO_DIGIT}){DASH_SLASH_NONE}({TWO_OR_FOUR_DIGIT})'
DMY = MDY

# DateMathString Patterns

ADD = r'LHS\ ?\+\ ?RHS'
SUB = r'LHS\ ?\-\ ?RHS'
IDENTITY = r'LHS'

def match_datestring(s):
    '''
    '''
    dates = []
    return dates,s

def match_durationstring(s):
    '''
    '''
    durations = []
    return durations,s

def match_datemathstring(l,s):
    '''
    '''
    result = ''
    return result