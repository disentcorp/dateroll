import re

# General patterns
OPERATOR = r" ?(\+|-)? ?"
INT_PART = r"\d+"
OPTIONAL_DECIMAL = r"(?:\.|\.\d+)?"
NUMBER = f"{INT_PART}{OPTIONAL_DECIMAL}"

# DateString Patterns (rough patterns, parser does validation)
D = M = r"\d{1,2}"
Y = r"\d{2,4}"
_ = r"(?:-|/|\A\Z)"
YMD = f"{Y}{_}{M}{_}{D}"
MDY = f"{M}{_}{D}{_}{Y}"
DMY = f"{D}{_}{M}{_}{Y}"

# DurationString atterns
PERIOD_LETTER = r"(?:bd|BD|[dDwWmMqQsShHyY])"
DATE_PERIOD = f"(?:({NUMBER})({PERIOD_LETTER}))"
REPEATING_DATE_PERIODS = (
    f"(?:{DATE_PERIOD}{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?)"
)

## MARKETED FOR DELETEION IF NO FUCKUPS
# PIPE = r"\|"
# TWOLETTERCAL = r"[A-ZA-Z][A-ZA-Z]"
# REPEATING_CALUNIONS = f" ?{PIPE} ?({TWOLETTERCAL})(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?"
# PIPE_REPEAT_CAL_UNION = f"(?:{REPEATING_CALUNIONS})?"
# ROLL = r" ?/ ?(MF|MP|F|P) ?"
# PIPE_ROLL = f"(?:{ROLL})?"
# RHS_PATTERN = f"{OPERATOR}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION}{PIPE_ROLL}"
# MATCH_WITH_DTPERIOD = f"(.*)(?= ?){RHS_PATTERN}"
# MATCH_WITHORWITHOUT_DTPERIOD = f"(?:{MATCH_WITH_DTPERIOD})|(.*)"
# FULL_PATTERN = MATCH_WITHORWITHOUT_DTPERIOD
## MARKETED FOR DELETEION IF NO FUCKUPS


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

# Compile
YMD = re.compile(DMY)
MDY = re.compile(DMY)
DMY = re.compile(DMY)
MATH = re.compile(MATH)
COMPLETE_DURATION = re.compile(COMPLETE_DURATION)
