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
YMD = f"(({Y}){_}({M}){_}({D}))"
MDY = f"(({M}){_}({D}){_}({Y}))"
DMY = f"(({D}){_}({M}){_}({Y}))"

# DurationString patterns
PERIOD_LETTER = r"(?:bd|BD|[dDwWmMqQsShHyY])"
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

# patterns regarding the time string
# OPTIONAL_PART = r"(?:[+-]?[A-Z]? ?)"
OPTIONAL_PART = r"(?:[+-]?\d?[a-zA-Z]? ?)"

HOUR_LETTER = r"(?:[Hh])"
MINUTE_LETTER = r"(?:MIN|min)"
SECONDS_LETTER = r"(?:[Ss])"

MICROSECONDS_LETTER = r"(?:US|us)"
HOUR_NUMBER = fr"(?:({INT_PART})({HOUR_LETTER}))"
MINUTE_NUMBER = fr"(?:({INT_PART})({MINUTE_LETTER}))"
SECONDS_NUMBER = fr"(?:({INT_PART})({SECONDS_LETTER}))"
MICROSECONDS_NUMBER = fr"(?:({INT_PART})({MICROSECONDS_LETTER}))"

COMPLETE_TIME = f"(?:{OPTIONAL_PART}?{HOUR_NUMBER}?{MINUTE_NUMBER}?{SECONDS_NUMBER}?{MICROSECONDS_NUMBER}?)"

if __name__=="__main__":
    ...
