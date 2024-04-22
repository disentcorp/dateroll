
is_leap_year = lambda year: (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def dc_ACT360(a, b, cals):
    """ https://en.wikipedia.org/wiki/Day_count_convention """
    return (b - a).just_exact_days / 360.0

def dc_ACT365(a, b, cals):
    """ https://en.wikipedia.org/wiki/Day_count_convention """
    print('!!!!!!!!!!!!!!!!!!!!!!!',b-a,(b-a).days)
    return (b - a).just_exact_days / 365.0

def dc_30E360(a, b, cals):
    """ https://en.wikipedia.org/wiki/Day_count_convention """
    y2, m2, d2 = b.year, b.month, b.day
    y1, m1, d1 = a.year, a.month, a.day

    d1 = min(d1, 30)
    d2 = min(d2, 30)
    dcf = (360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)) / 360.00
    return dcf

def dc_BD252(a, b, cals=None):
    dur = (b-a)
    if cals is not None:
        dur._validate_cals(cals)
    return dur.just_bds / 252.0

yf_mapping = {
    "ACT/365": dc_ACT365,
    "ACT/360": dc_ACT360,
    "30E/360": dc_30E360,
    "BD/252": dc_BD252
}
