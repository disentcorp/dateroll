import calendar
import datetime
import math
import re
import time

import numpy
import pandas
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from dateroll.holidays import date_adjust, f_dates_in_year, generate_cal
from dateroll.regex import NUMBER, date_matcher, match_st_ed

units_rd_date = {
    "BD": lambda date, sgn, num, hol, roll_conv: date_adjust(
        date, sgn, num, hol, roll_conv=roll_conv
    ),  # BD always weekend adjusted so included WE
    # if CD|NY means the calendar date should be adjusted by holiday only,
    "CD": lambda date, sgn, num, hol, roll_conv: date
    + relativedelta(
        days=sgn * num
    ),  # if len(hol_list)==0 else holiday_weekend_adjust(date + relativedelta(days=num),*get_holidays_list(date + relativedelta(days=num),hol_list),1),
    "D": lambda date, sgn, num, hol, roll_conv: date
    + relativedelta(
        days=sgn * num
    ),  # if len(hol_list)==0 else holiday_weekend_adjust(date + relativedelta(days=num),*get_holidays_list(date + relativedelta(days=num),hol_list),1),
}
units_rd = {
    "W": relativedelta(days=7),
    "M": relativedelta(months=1),
    "Q": relativedelta(months=3),
    "S": relativedelta(months=6),
    "H": relativedelta(months=6),
    "Y": relativedelta(years=1),
}

dtRange_mapping = {
    "BD": lambda cal, bgnY, endY: get_BDRange(cal, bgnY, endY),
    "CD": lambda cal, bgnY, endY: f_dates_in_year(bgnY, endY),
    "D": lambda cal, bgnY, endY: f_dates_in_year(bgnY, endY),
}


# this wrapper gives list of datetime in Business dates
def generate_calWrapper(func):
    def Wrapper(*args, **kwargs):
        dtRange = func(*args, **kwargs)
        dtRange = [
            datetime.date.strptime(k, "%Y%m%d")
            for k, v in dtRange.items()
            if list(v.keys())[0] == "r"
        ]
        return dtRange

    return Wrapper


@generate_calWrapper
def get_BDRange(cal, bgnY, endY):
    """returns list of business dates"""
    return generate_cal(cal, bgnY, endY)


def get_test_dates_formats(dts_dict):
    dts = list(dts_dict.values())
    fmt = list(dts_dict.keys())
    return dts, fmt


def test_dates(fmts):
    new_fmt = []
    if isinstance(fmts, list):
        for fmt in fmts:
            fmt_ = parse(fmt)
            try:
                fmt_ = parse(fmt)
                new_fmt.append(fmt_)
            except:
                new_fmt.append(fmt)
    else:
        ...

    return new_fmt


def tmWrapper(func):
    def wrapper(*args, **kwargs):
        be = time.time()
        rs = func(*args, **kwargs)
        en = time.time()
        tm = round(en - be, 6)
        return rs, tm

    return wrapper


def month_adjust(mwho, ywho, swho, qwho):
    """adjust months when month > 12 to make month to become <= 12"""
    if mwho / 12 < 1:
        mwho = mwho
    else:
        y_add = int(mwho / 12)
        mwho = mwho % 12
        ywho += y_add
    if swho != 0:
        if mwho / 6 < 1:
            mwho = mwho
        else:
            s_add = int(mwho / 6)
            mwho = mwho % 6
            swho += s_add
    if qwho != 0:
        if mwho / 3 < 1:
            mwho = mwho
        else:
            q_add = int(mwho / 3)
            mwho = mwho % 3
            qwho += q_add

    return mwho, ywho, swho, qwho


def catch_YMD(txt):
    """get y,s,q,m,d from texts, return like 3y2m1d"""
    txt = txt.replace(" ", "")
    Y_pattern = f" ?{NUMBER} ?[yY] ?"
    S_pattern = f" ?{NUMBER} ?[sShH] ?"
    Q_pattern = f" ?{NUMBER} ?[qQ] ?"
    M_pattern = f" ?{NUMBER} ?[mM] ?"
    W_pattern = f" ?{NUMBER} ?[wW] ?"
    D_pattern = f" ?{NUMBER} ?[cCbB]?[dD]"  # cd|CD|bd|BD|
    Y_matches = re.findall(Y_pattern, txt)  # this part might give wrong format ??
    Y_matches = Y_matches[0] if len(Y_matches) > 0 else "0y"
    S_matches = re.findall(S_pattern, txt)
    S_matches = S_matches[0] if len(S_matches) > 0 else "0s"
    Q_matches = re.findall(Q_pattern, txt)
    Q_matches = Q_matches[0] if len(Q_matches) > 0 else "0q"
    M_matches = re.findall(M_pattern, txt)
    M_matches = M_matches[0] if len(M_matches) > 0 else "0m"
    W_matches = re.findall(W_pattern, txt)
    W_matches = W_matches[0] if len(W_matches) > 0 else "0w"
    D_matches = re.findall(D_pattern, txt)
    D_matches = D_matches[0] if len(D_matches) > 0 else "0d"
    return Y_matches, S_matches, Q_matches, M_matches, W_matches, D_matches


f_getYear = lambda y: float(y[:-1])
f_getSemi = lambda s: float(s[:-1])
f_getQuarter = lambda q: float(q[:-1])
f_getMonth = lambda m: float(m[:-1])
f_getWeek = lambda w: float(w[:-1])
f_getDate = lambda d: (
    float(d[:-1]) if not ("C" in d.upper() or "B" in d.upper()) else float(d[:-2])
)


def ymd_to_dates(txt):
    y, s, q, m, d = catch_YMD(txt)
    y = f_getYear(y)
    y = y * 12 * 30
    s = f_getSemi(s)
    s = s * 6 * 30
    q = f_getQuarter(q)
    q = q * 3 * 30
    m = f_getMonth(m)
    m = m * 30
    d = f_getDate(d)
    d = round(y + s + q + m + d, 0)
    return d


def test_YMD(txt):
    d = ymd_to_dates(txt)
    txt1 = fractionYMD_convert(txt)
    d_converted = ymd_to_dates(txt1)

    return d == d_converted, d, d_converted


def get_YMDs(txt):
    Y_match, S_match, Q_match, M_match, W_match, D_match = catch_YMD(txt)
    Y_matches = f_getYear(Y_match)
    S_matches = f_getSemi(S_match)
    Q_matches = f_getQuarter(Q_match)
    M_matches = f_getMonth(M_match)
    W_matches = f_getWeek(W_match)
    D_matches = f_getDate(D_match)
    y_unit = Y_match[-1]
    s_unit = S_match[-1]
    q_unit = Q_match[-1]
    m_unit = M_match[-1]
    w_unit = W_match[-1]
    d_unit = (
        D_match[-1]
        if not ("C" in D_match.upper() or "B" in D_match.upper())
        else D_match[-2:]
    )
    return (
        Y_matches,
        S_matches,
        Q_matches,
        M_matches,
        W_matches,
        D_matches,
        y_unit,
        s_unit,
        q_unit,
        m_unit,
        w_unit,
        d_unit,
    )


def dtYMD_convert(txt):
    """to catch dt1 - dt2 from string and compute duration of these 2 dates"""

    txt = txt.replace(" ", "")
    asof, dur = datePeriodParse(txt)
    st, ed = None, None

    if asof == "":
        return dur, st, ed
    elif asof != "" and dur != "":  # to catch 20220101+3BD|NY
        st = asof
        return dur, st, ed
    else:
        str_ = match_st_ed(asof)
        if len(str_) == 6:
            st = "/".join(str_[:3])
            ed = "/".join(str_[3:6])
            st = parse(st)
            ed = parse(ed)
            numY = st.year - ed.year
            numM = st.month - ed.month
            numD = st.day - ed.day
            dur = negYMD_convert(numY, numM, numD, st)

        elif len(str_) == 4:
            st = "/".join([str_[0], str_[1][:2], str_[1][2:]])
            ed = "/".join([str_[2], str_[3][:2], str_[3][2:]])
            st = parse(st)
            ed = parse(ed)
            numY = st.year - ed.year
            numM = st.month - ed.month
            numD = st.day - ed.day
            dur = negYMD_convert(numY, numM, numD, st)
        return dur, st, ed


def negYMD_convert(numY, numM, numD, dt):
    """to fix if 2y-4m3d---> 1y8m3d"""
    LM = calendar.monthrange(dt.year, dt.month)[1]
    if numD < 0:
        if numY == 0 and numM == 0:
            return f"-{numY}y{numM}m{-1 * numD}d"
        numM = numM + numpy.sign(numM) * -1
        numD = LM + numD
    if numM < 0:
        if numY == 0:
            return f"-{numY}y{-1*numM}m{numD}d"
        numY = numY + numpy.sign(numY) * -1  # add or subtract month from year
        numM = 12 + numM
    return f"{numY}y{numM}m{numD}d"


def fractionYMD_convert(txt):
    """if fraction years, e.g. 3.4y2.3m3d, it will convert to integer years"""
    (
        Y_matches,
        S_matches,
        Q_matches,
        M_matches,
        W_matches,
        d,
        y_unit,
        s_unit,
        q_unit,
        m_unit,
        w_unit,
        d_unit,
    ) = get_YMDs(txt)
    ydec, ywho = math.modf(Y_matches)
    m_add = ydec * 12
    sdec, swho = math.modf(S_matches)
    m_add_s = sdec * 6
    qdec, qwho = math.modf(Q_matches)
    m_add_q = qdec * 3
    m = M_matches + m_add + m_add_s + m_add_q
    mdec, mwho = math.modf(m)
    d += mdec * 30
    wdec, wwho = math.modf(W_matches)
    d += wdec * 7
    if d / 30 < 1:
        d = int(round(d, 0))
    else:
        d, m_add = math.modf(d / 30)
        d *= 30
        d = int(round(d, 0))
        mwho += m_add

    mwho, ywho, swho, qwho = month_adjust(
        mwho, ywho, swho, qwho
    )  # if month is > 12 it will adjust month to become <= 12
    ymd = f"{ywho}{y_unit}{swho}{s_unit}{qwho}{q_unit}{mwho}{m_unit}{wwho}{w_unit}{d}{d_unit}"
    return ymd


def datePeriodParse(date_period_string):
    """to separate date and duration from string"""
    tenor_string = str(date_period_string).replace(" ", "")
    str_list = date_matcher(tenor_string)
    asof = str_list[0]
    tnr = [l for l in str_list[1:12] if l != ""]
    tenor_string = ""
    if len(tnr) > 0:
        hols = [l for l in str_list[12:20] if l != ""]
        tenor_string = "".join(tnr)
        if len(hols) > 0:
            hols = "u".join(hols)
            tenor_string = "|".join([tenor_string, hols])
            roll = [l for l in str_list[20:] if l != ""]
            if len(roll) > 0:
                roll = "".join(str_list[20:])
                tenor_string = "/".join([tenor_string, roll])
    return asof, tenor_string


# duplicate version, conversion function, can keep fraction
def datePeriodStringToDatePeriod(date_period_string):
    """split string into y,m,d and returns lambda func where
    lambda func calculates BD or D adjustment on years"""
    tenor_string = str(date_period_string).replace(" ", "")
    str_list = date_matcher(tenor_string)

    asof, sgn = str_list[:2]
    n1, p1, n2, p2, n3, p3, n4, p4, n5, p5 = str_list[2:12]
    holidays_list = str_list[12:20]
    roll = str_list[20]
    rd_tenor = "".join([n1, p1, n2, p2, n3, p3, n4, p4, n5, p5])
    try:
        rd_tenor1 = fractionYMD_convert(rd_tenor)
    except:
        raise Exception("DisentTenor", f"Format not valid #1 {date_period_string}")

    sgn = -1 if "-" in sgn else 1
    numY, numS, numQ, numM, numW, numD, unitY, unitS, unitQ, unitM, unitW, unitD = (
        get_YMDs(rd_tenor1)
    )
    holidays_list = list(filter(lambda x: x != "", holidays_list))

    holidays = "u".join(holidays_list)
    unitD = "BD" if holidays != "" else unitD
    holidays = "WE" if holidays == "" else holidays
    roll_conv = roll

    addition = (
        numY * units_rd[unitY.upper()]
        + numS * units_rd[unitS.upper()]
        + numQ * units_rd[unitQ.upper()]
        + numM * units_rd[unitM.upper()]
        + numW * units_rd[unitW.upper()]
    )
    rs = lambda yr, sgn2: units_rd_date[unitD.upper()](
        yr + sgn * sgn2 * addition, sgn * sgn2, numD, holidays, roll_conv
    )

    return rs


LASTDATEOFMONTH = lambda d: datetime.date(
    d.year, d.month, calendar.monthrange(d.year, d.month)[1]
)
IERULE_MAPPING = {
    "()": lambda st, ed, dur: [st + dur, ed - dur],
    "(]": lambda st, ed, dur: [st + dur, ed],
    "[]": lambda st, ed, dur: [st, ed],
    "[)": lambda st, ed, dur: [st, ed - dur],
}


def genEndtoEnd(l):
    l2 = [l[i] if i == len(l) - 1 else LASTDATEOFMONTH(l[i]) for i in range(len(l))]

    return l2


def assign_kwargs(str_l):
    per, stub, ret, monthEndRule, ie, dc = (
        "1m",
        "short",
        "l",
        "anniv",
        "[)",
        NotImplementedError,
    )
    asof_ed, dur_ed = "", ""
    if len(str_l) > 1:
        for str_ in str_l[1:]:
            val = str_.split("=")[-1]
            if "per" in str_:
                per = val
            elif "stub" in str_:
                stub = val
            elif "ret" in str_:
                ret = val
            elif "monthEndRule" in str_:
                monthEndRule = val
            elif "ie" in str_:
                ie = val
            elif "dc" in str_:
                dc = val
            else:
                str_0, str_1 = datePeriodParse(str_)
                if str_0 != "":
                    asof_ed, dur_ed = str_0, str_1
                elif str_0 == "" and str_1 != "":
                    per = str_1

                else:
                    ...
    return per, stub, ret, monthEndRule, ie, dc, asof_ed, dur_ed


def fwd_or_bwd(st, ed, per):
    bwd = False
    if st < ed and not "-" in per:
        ...
    elif st < ed and "-" in per:
        ed, st = st, ed
        bwd = True
    elif st > ed and not "-" in per:
        per = "".join(["-", per])
        bwd = True
    elif st > ed and "-" in per:
        st, ed = ed, st
        per = per.split("-")[-1]
    return st, ed, per, bwd


def genLL(l):
    """returns list of lists"""
    return [[l[i], l[i + 1]] for i in range(len(l) - 1)]


def genDF(l, stub):
    """returns two column dataframe, input needs to be list of lists e.g, [[1,3],[3,4]]"""
    bwd = True if l[0][0] > l[0][1] else False
    df = pandas.DataFrame(l, columns=["start", "end"])
    df["start"] = df["start"]  # df['start'].dt.date
    df["end"] = df["end"]  # df['end'].dt.date
    lp = genLP(l)
    lp = [f"{l}d" for l in lp]
    stb = ["full" if i != len(lp) - 1 else stub for i in range(len(lp))]
    df["dur"] = lp
    df["stub"] = stb
    if bwd:
        df1 = df[["end", "start", "dur", "stub"]]
        df1.columns = ["start", "end", "dur", "stub"]
        df1 = df1.iloc[::-1]
        df1 = df1.reset_index(drop=True)
        df = df1.copy()
    df.index += 1
    df.index.name = "per"
    return df


def genLP(l):
    """returns list of periods w.r.t list of dates"""
    l2 = [abs((x[0] - x[1]).days) for x in l]
    return l2


DATE_RANGE_HELPER_DICT = {
    "l": lambda l, stub: l,
    "ll": lambda l, stub: genLL(l),
    "df": lambda l, stub: genDF(genLL(l), stub),
    "lp": lambda l, stub: genLP(genLL(l)),
}
if __name__ == "__main__":
    dt = datetime.date(2022, 2, 20)
    rs = negYMD_convert(-2, 5, 3, dt)
    print(rs)
