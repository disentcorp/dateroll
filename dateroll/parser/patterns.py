import re

# General patterns
OPERATOR = r" ?(\+|-)? ?"
INT_PART = r"\d+"
OPTIONAL_DECIMAL = r"(?:\.|\.\d+)?"
NUMBER = f"{INT_PART}{OPTIONAL_DECIMAL}"

# DateString Patterns (rough patterns, parser does validation)
D = M = r"\d{1,2}"
Y = r"\d{2,4}"
_ = r"(?: ?-|/|\A\Z)?"
YMD = f"{Y}{_}{M}{_}{D}"
MDY = f"{M}{_}{D}{_}{Y}"
DMY = f"{D}{_}{M}{_}{Y}"

# DurationString patterns
PERIOD_LETTER = r"(?:bd|BD|[dDwWmMqQsShHyY])"
DATE_PERIOD = f"(?:({NUMBER})({PERIOD_LETTER}))"
REPEATING_DATE_PERIODS = (
    f"(?:{DATE_PERIOD}{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?)"
)
PIPE = r"(\|)?"
CAL = r"([A-Z]{2,3})"
OPTIONAL_CALS= f'(?:u{CAL})?'*7
CALS = f'{CAL}{OPTIONAL_CALS}'
REPEATING_CALUNIONS = f" ?(?:{PIPE}) ?{CALS}"
ROLL = r" ?(/)? ?(MF|MP|F|P) ?"
PIPE_ROLL = f"(?:{ROLL})?"
PIPE_REPEAT_CAL_UNION = f"(?:{REPEATING_CALUNIONS})?"
COMPLETE_DURATION = (
    f"({OPERATOR}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION}{PIPE_ROLL})"
)

# DateMathString Patterns
MATH = r"^ ?((\+|-)? ?)?X( ?(\+|-) ?X)?$"

# Compiled
YMD = re.compile(YMD)
MDY = re.compile(MDY)
DMY = re.compile(DMY)
MATH = re.compile(MATH)
COMPLETE_DURATION = re.compile(COMPLETE_DURATION)
