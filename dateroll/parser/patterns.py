import re

# General patterns
OPERATOR = r" ?(\+|-)? ?"
INT_PART = r"\d+"
OPTIONAL_DECIMAL = r"(?:\.|\.\d+)?"
NUMBER = f"{INT_PART}{OPTIONAL_DECIMAL}"

# # DateString Patterns (rough patterns, parser does validation)
D = M = r"\d{1,2}"
Y = r"\d{2,4}"
_ = r"(?: ?-|/|\A\Z)?"
no_letters_digit = r"(?![\d\w])"
YMD = f"(({Y}){_}({M}){_}({D})){no_letters_digit}"
MDY = f"(({M}){_}({D}){_}({Y})){no_letters_digit}"
DMY = f"(({D}){_}({M}){_}({Y})){no_letters_digit}"

# DurationString patterns
# PERIOD_LETTER = r"(?:bd|BD|[dDwWmMqQyY])"
PERIOD_LETTER = r"(?:us|US|MIN|min|bd|BD|[dDwWmMqQyYhHsS])"
DATE_PERIOD = f"(?:({NUMBER})({PERIOD_LETTER}))"
REPEATING_DATE_PERIODS = f"(?:{DATE_PERIOD}{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?)"
PIPE = r"(\|)?"
CAL = r"([A-Z]{2,3})"
OPTIONAL_CALS = f"(?:u{CAL})?" * 10
CALS = f"{CAL}{OPTIONAL_CALS}"
REPEATING_CALUNIONS = f" ?(?:{PIPE}) ?{CALS}"
ROLL = r" ?(/)? ?(MOD) ?"
PIPE_ROLL = f"(?:{ROLL})?"
PIPE_REPEAT_CAL_UNION = f"(?:{REPEATING_CALUNIONS})?"
COMPLETE_DURATION = (
    f"({OPERATOR}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION}{PIPE_ROLL})"
)

MONTHNAMES = re.compile(
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)"
)

# iso date patter before T
ISO_D = r"\d{1,2}T\d{2}:\d{2}:\d{2}(?:(?:[+-]\d{2}:\d{2})|(?:[.]\d+))?"
# ISO_D = r"\d{1,2}T\d{2}:\d{2}:\d{2}"
ISO_YMD = f"({OPERATOR}({Y}){_}({M}){_}({ISO_D}))"
