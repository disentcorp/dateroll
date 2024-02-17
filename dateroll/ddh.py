import re

from dateutil.relativedelta import relativedelta

from dateroll.date import Date
from dateroll.period import Period
from dateroll.schedule import Schedule
from dateroll.utils import datePeriodParse, assign_kwargs
from dateroll.regex import PTNW,PTN,RHS_PATTERN_2

def handle_input(args):
    isit = all([isinstance(arg, str) for arg in args])
    if isit:
        dt_big_string = ",".join(args)
    else:
        dt_big_string = args[0]
    return dt_big_string


def ddh(*args):
    if not isinstance(args[0], str):  # assume this is going to use Date object
        try:
            rs = Date(*args)
        except:
            raise Exception("Input parameters are wrong")
        return rs
    else:

        dt_big_string = handle_input(args)
    str_l = dt_big_string.split(",")
    str_wor = re.findall(PTNW, dt_big_string)
    str_dts = re.findall(PTN, dt_big_string)
    str_dur = re.findall(RHS_PATTERN_2, dt_big_string)

    if len(str_dur) > 1 and len(str_dts) == 0 and len(str_wor) == 0:
        dur_l = ["".join(x) for x in str_dur]
        rs = [Period(x) for x in dur_l]
        return rs
    else:
        asof_st, dur_st = datePeriodParse(str_l[0])
        per, stub, ret, monthEndRule, ie, dc, asof_ed, dur_ed = assign_kwargs(str_l)

        if asof_st != "" and asof_ed != "":
            st = "".join([asof_st, dur_st])
            ed = "".join([asof_ed, dur_ed])
            # asof_st = ddh(st)
            # asof_ed = ddh(ed)
            # st = ddh(f'{asof_st}+0bd').strftime('%Y%m%d') if 'bd' in per.lower() else ...
            # ed = ddh(f'{ed}-0bd').strftime('%Y%m%d') if 'bd' in per.lower() else ...
            if isinstance(st,str):
                st = Date(st)
            if isinstance(ed,str):
                ed = Date(ed)
            rs = Schedule(
                st,
                ed,
                per,
                stub=stub,
                ret=ret,
                monthEndRule=monthEndRule,
                ie=ie,
                dc=dc,
            )()
            
            if not ret in ["l", "ll", "df", "lp"]:
                rs = set(rs)
                rs = list(sorted(rs))
            if ret == "lp":
                rs = [ddh(f"{p}d") for p in rs]
        else:

            # dts_l = [''.join(x) for x in str_dts]
            str_wor = re.findall(PTNW, asof_st)
            str_dts = re.findall(PTN, asof_st)
            str_dur = re.findall(RHS_PATTERN_2, asof_st)
            dur_l = ["".join(x) for x in str_dur]
            if len(str_dts) == 2:
                rs = Period(asof_st)
            elif len(str_dts) == 1:  # this is the format of '20220101'
                rs = Date(asof_st) + Period(dur_st)
            elif len(str_dts) == 0:
                if len(str_dur) > 0:
                    rs = Period(str_dur[0])
                else:
                    if dur_st == "" and asof_st != "":
                        rs = Date(asof_st)
                    elif dur_st != "" and asof_st != "":
                        rs = Date(asof_st) + Period(dur_st)
                    else:
                        rs = Period(dur_st)

        return rs


def unit_tests():
    # test date performs like datetime or a date
    d = Date(2015, 5, 12)
    print(d, type(d))
    d = Date("1/1/15")
    print(d, type(d))

    d = d + relativedelta(days=10)
    d = d - relativedelta(days=10)

    # test date period, and add and subtract
    date_period = Period("5d")
    print(date_period, repr(date_period), type(date_period))
    print(d + date_period)
    print(d)
    print(d - date_period)
    print(date_period.today())


def unit_tests2():
    dt = Date(2022, 1, 1)
    print(type(dt.__str__()))
    print(dt.__repr__())
    print(type(dt.__str__()))
    rd = Period("-1m")
    # rs = dt + rd
    rs = dt + rd
    rs1 = rd + dt
    print(rs)
    print(rs1)

    return rs


def test_dtRange(st, ed, per):
    # st = '20221010'
    # ed = '20221230'
    # per = '-1m'
    print("/" * 10 + " short")
    rs = ddh(f"{st},{ed},{per},ret=l")
    print(rs)
    rs = ddh(f"{st},{ed},{per},ret=ll")
    print(rs)
    rs = ddh(f"{st},{ed},{per},ret=df")
    print(rs)
    rs = ddh(f"{st},{ed},{per},ret=lp")
    print(rs)
    print("/" * 10 + " long")
    rs = ddh(f"{st},{ed},{per},stub=long,ret=l")
    print(rs)
    rs = ddh(f"{st},{ed},{per},stub=long,ret=ll")
    print(rs)
    rs = ddh(f"{st},{ed},{per},stub=long,ret=df")
    print(rs)
    rs = ddh(f"{st},{ed},{per},stub=long,ret=lp")
    print(rs)
    print("/" * 10 + " short end-to-end")
    rs = ddh(f"{st},{ed},{per},stub=short,ret=l,monthEndRule=end-to-end")
    print(rs)
    rs = ddh(f"{st},{ed},{per},stub=short,ret=ll,monthEndRule=end-to-end")
    print(rs)
    rs = ddh(f"{st},{ed},{per},stub=short,ret=df,monthEndRule=end-to-end")
    print(rs)
    rs = ddh(f"{st},{ed},{per},stub=short,ret=lp,monthEndRule=end-to-end")
    print(rs)


DTS_M = [
    ["20220131", "20220415"],
    ["20220131", "20220430"],
    ["20220115", "20220430"],
    ["20220115", "20220428"],
]
DTS_Q = [
    ["20220131", "20220615"],
    ["20220131", "20220630"],
    ["20220115", "20220630"],
    ["20220115", "20220628"],
]
DTS_Y = [
    ["20220131", "20230615"],
    ["20220131", "20230630"],
    ["20220115", "20230630"],
    ["20220115", "20230628"],
]
DTS_D = [
    ["20221230", "20230106"],
    ["20221230", "20230108"],
    ["20221231", "20230108"],
    ["20221231", "20230106"],
]
"////"
DTS_MP = [
    ["20220131+1BD|NY", "20220415+1BD|NY"],
    ["20220415-1M|NY", "20220430+1M"],
    ["20220115-1Y", "20220430+1Y2M"],
    ["20220115-1q", "20220428+1q"],
]


def test_dts(idx_):
    # dts = [['20220131','20220415'],['20220131','20220430'],['20220115','20220430'],['20220115','20220428']]
    dts = [
        ["20220131", "20220615"],
        ["20220131", "20220630"],
        ["20220115", "20220630"],
        ["20220115", "20220628"],
    ]
    # dts = [['20220131','20230615'],['20220131','20230630'],['20220115','20230630'],['20220115','20230628']]  # for year
    # dts = [['20221230','20230106'],['20221230','20230108'],['20221231','20230108'],['20221231','20230106']]
    # dts = [['20220115','20220428']]
    idx = idx_
    st = dts[idx][0]
    ed = dts[idx][1]
    test_dtRange(st, ed, "1q")


def test_ddh_rng(st, ed, per):
    lst = [
        f"{st},{ed},per={per},ret=l",
        f"{st},{ed},per={per},ret=ll",
        f"{st},{ed},per={per},ret=df",
        f"{st},{ed},per={per},ret=lp",
        f"{st},{ed},per={per},stub=long,ret=l",
        f"{st},{ed},per={per},stub=long,ret=ll",
        f"{st},{ed},per={per},stub=long,ret=df",
        f"{st},{ed},per={per},stub=long,ret=lp",
        f"{st},{ed},per={per},stub=short,ret=l,monthEndRule=end-to-end",
        f"{st},{ed},per={per},stub=short,ret=ll,monthEndRule=end-to-end",
        f"{st},{ed},per={per},stub=short,ret=df,monthEndRule=end-to-end",
        f"{st},{ed},per={per},stub=short,ret=lp,monthEndRule=end-to-end",
    ]
    for ls in lst:
        print(ddh(ls))
    # print(ddh(lst[idx]))
    return "complete"


def test_ddh_single(idx_):
    idx = idx_
    st = DTS_MP[idx][0]
    ed = DTS_MP[idx][1]
    per = "-1m"
    rs = test_ddh_rng(st, ed, per)


def test_bwdFwd():
    a = "20221031"  # a,b,per; a,b,per_; b,a,per; b,a,per_
    b = "20240310"
    per = "1d"
    per_ = "-1d"
    ls = [
        f"{a},{b},per={per}",
        f"{a},{b},per={per_}",
        f"{b},{a},per={per}",
        f"{b},{a},per={per_}",
    ]
    # rs = test_ddh_rng(a,b,per_)
    # print(rs)
    print("/" * 10)
    rs = test_ddh_rng(b, a, per)
    # test_ddh_rng(a,b,per_)


def testDate():
    rs = Date(2022, 10, 10)
    print(f"to excel {rs.toExcel()}")
    print("///")
    print(f"to unix {rs.toUnix()}")
    print("///")
    print(f"to isoStr {rs.isoStr()}")
    print("///")
    print(f"is weekDay {rs.weekDay()}")
    print("///")
    print(f"is weekMonth {rs.weekMonth()}")
    print("///")
    print(f"is weekYear {rs.weekYear()}")
    print("///")
    print(f"isBd {rs.isBd()}")
    print("///")
    print(f"to string {rs.toStr()}")


def test_feedback():
    print(ddh("t0,t+2y"))
    print(ddh("t0-1.5y"))
    print(ddh("10/25/22,20231015,1m,stub=long,ret=df"))
    print(ddh("t+0d"))
    print("////")
    # print(Schedule('10/25/22','20231015','1m','stub=hiiii','ret=df'))


if __name__ == "__main__":
    # unit_tests()
    # unit_tests2()
    # print(Schedule('20220101','t',per='1m'))
    # print(test_bwdFwd())
    t1 = "t-5y"
    t2 = "t"
    # x = ddh(f"t-1m,t,5d")
    # x = ddh(f't-1m','t','5d')
    # print(x)
    # x = Schedule('t-1m','t',per='-5d',ret='lp')()
    # x = ddh('t-1m,t,per=5d,ret=df')
    # x = ddh('t-5y,t,3m,ret=df')
    t1 = "20230125"
    t2 = "20230125"
    # x = ddh(f"{t1},{t2},1bd,ie=[]")
    # t1 = '20220817'
    # t2 = '20220901'
    x = ddh(f"{t1},{t2},1bd,ie=[]")
    # x = ddh(t1)+Period('0bd')
    print(x)

    # x = ddh('3m').convert(roughly='q')
    # print(x)
