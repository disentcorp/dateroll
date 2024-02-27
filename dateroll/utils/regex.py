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
YMD = re.compile(f"{Y}{_}{M}{_}{D}")
MDY = re.compile(f"{M}{_}{D}{_}{Y}")
DMY = re.compile(f"{D}{_}{M}{_}{Y}")

# DurationString atterns
PERIOD_LETTER = r"(?:bd|BD|[dDwWmMqQsShHyY])"
DATE_PERIOD = f"(?:({NUMBER})({PERIOD_LETTER}))"
REPEATING_DATE_PERIODS = (
    f"(?:{DATE_PERIOD}{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?)"
)
PIPE = r"\|"
TWOLETTERCAL = r"[A-ZA-Z][A-ZA-Z]"
REPEATING_CALUNIONS = f" ?{PIPE} ?({TWOLETTERCAL})(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?"
PIPE_REPEAT_CAL_UNION = f"(?:{REPEATING_CALUNIONS})?"
ROLL = r" ?/ ?(MF|MP|F|P) ?"
PIPE_ROLL = f"(?:{ROLL})?"
RHS_PATTERN = f"{OPERATOR}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION}{PIPE_ROLL}"
MATCH_WITH_DTPERIOD = f"(.*)(?= ?){RHS_PATTERN}"
MATCH_WITHORWITHOUT_DTPERIOD = f"(?:{MATCH_WITH_DTPERIOD})|(.*)"
FULL_PATTERN = MATCH_WITHORWITHOUT_DTPERIOD
PIPE_2 = r"(\|)?"
TWOLETTERCAL_2 = r"[u]?([A-ZA-Z][A-ZA-Z])"
REPEATING_CALUNIONS_2 = f" ?(?:{PIPE_2}) ?{TWOLETTERCAL_2}{TWOLETTERCAL_2}?{TWOLETTERCAL_2}?{TWOLETTERCAL_2}?{TWOLETTERCAL_2}?{TWOLETTERCAL_2}?{TWOLETTERCAL_2}?{TWOLETTERCAL_2}?"
ROLL_2 = r" ?(/)? ?(MF|MP|F|P) ?"
PIPE_ROLL_2 = f"(?:{ROLL_2})?"
PIPE_REPEAT_CAL_UNION_2 = f"(?:{REPEATING_CALUNIONS_2})?"
COMPLETE_DURATION = re.compile(
    f"({OPERATOR}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION_2}{PIPE_ROLL_2})"
)

# DateMathString Patterns
IDENT = r"^ ?(\+|-) ?X ?$"
MATH = r"^ ?((\+|-)? ?)?X(\+|-) ?X$"
