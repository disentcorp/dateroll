import datetime
from datetime import timedelta

import numpy as np
from dateutil.relativedelta import relativedelta as rd
from workalendar import america, asia, europe, oceania, usa

f_YRS = lambda bgn_y, end_y: [bgn_y + i for i in range(end_y - bgn_y + 1)]
holiday_mapping = {
    "NY": lambda y: eval(f"usa.NewYork().holidays({y})"),
    "EU": lambda y: eval(f"europe.EuropeanCentralBank().holidays({y})"),
    "GB": lambda y: eval(f"europe.UnitedKingdom().holidays({y})"),
    "JP": lambda y: eval(f"asia.Japan().holidays({y})"),
    "AU": lambda y: eval(f"oceania.Australia().holidays({y})"),
    "BR": lambda y: eval(f"america.BrazilBankCalendar().holidays({y})"),
    "MX": lambda y: eval(f"america.Mexico().holidays({y})"),
    "CA": lambda y: eval(f"america.Canada().holidays({y})"),
    "WE": lambda y: [],
}
weekend_u_holiday_mapping = {
    "WE_only": lambda dates, hol_list: eval(f"{dates.weekday()} in [5,6]"),
    "WE_u_HOL": lambda dates, hol_list: eval(
        f"{dates.weekday()} in [5,6] or {dates in hol_list}"
    ),  # in {hol_list}
    "HOL_only": lambda dates, hol_list: eval(f" {dates in hol_list}"),
}
years_mapping = {
    "ASIA": f_YRS(2000, 2050),
    "OTHER": f_YRS(1990, 2080),
}
COUNTRY_HOLIDAYS = ["NY", "EU", "AU", "BR", "MX", "JP", "UK", "CA"]
JSON_FILE = "holidaysJson/holidays.json"
BGN_Y = 2022
END_Y = 2022
YRS = f_YRS(BGN_Y, END_Y)
f_DT_STR = lambda x: x.strftime("%Y%m%d")
f_dates_in_year = lambda bgn_yr, end_yr: [
    bgn_yr + timedelta(days=i) for i in range(int((end_yr - bgn_yr).days) + 1)
]


def get_hol_list(yrs, cal="WE", dic={}):
    """returns list of holidays with corresponding yrs"""
    bgn = yrs[0]
    end = yrs[-1]
    key_ = f"{cal}_{bgn}_{end}"
    val_ = []
    calendars = cal.split("u")
    for ca in calendars:
        if ca in holiday_mapping.keys():
            for yr in yrs:

                val_ += holiday_mapping[ca](yr)
        else:
            raise Exception(
                f"{ca} holidays are not supported yet, please contact Disent"
            )
    val_ = [dt[0] for dt in val_]
    val_ = sorted(val_)
    dic.update({key_: val_})
    return val_


def date_conv_adjust(dic, prev_, now_, roll_conv):
    """this part adjust MF or MP when date goes to different month"""
    rs = now_
    if roll_conv == "MF":
        if now_ > prev_ and prev_[:-2] != now_[:-2]:
            try:
                rs = dic[f"{prev_[:-2]}_MF"][f"{prev_[:-2]}_MF"]
            except:
                raise Exception(f"the YYMM {prev_[:-2]} does not have MF value")
    elif roll_conv == "MP":
        if now_ < prev_ and prev_[:-2] != now_[:-2]:
            try:
                rs = dic[f"{prev_[:-2]}_MP"][f"{prev_[:-2]}_MP"]

            except:

                raise Exception(f"the YYMM {prev_[:-2]} does not have MP value")
    else:
        ...
    return rs


def date_adjust(d, sgn, n, cal="WE", roll_conv=None):
    """use dictionary to get date after sutraction or addition"""

    d1 = d + (rd(days=sgn * n * 4) if n > 1 else rd(days=sgn * 7))
    d2 = d + rd(days=-1 * sgn * 7)

    dic = get_cal(cal, d2, d1)
    if isinstance(d, datetime.date):
        yr = d.strftime("%Y%m%d")
    if yr in dic.keys():
        val = list(dic[yr].values())[0] + sgn * n
        dic_rs = {
            k: v
            for k, v in dic.items()
            if list(v.keys())[0] == "r" and list(v.values())[0] == val
        }
        rs = list(dic_rs.keys())[0]
        rs = date_conv_adjust(dic, yr, rs, roll_conv)

        return rs
    else:
        raise Exception(
            f"{yr} year is not within the year range.Asian holidays between 2000-2050, Other countries between 1990-2080"
        )


def get_cal(cal, d, d1):
    dic = generate_cal(cal, d, d1)
    return dic


def generate_cal(cal, d, d1):
    """generate dictionary key is YYYYmmdd, value is count starts from begin year"""

    yr = d.year
    yr1 = d1.year
    yrs = set([yr, yr1])
    yrs = sorted(list(yrs))
    combo = "WE_u_HOL"
    count = 0
    bgn = d if d <= d1 else d1
    end = d1 if d1 > d else d
    if bgn == end:
        end = end + rd(days=2)

    holidays_list = get_hol_list(yrs, cal=cal)  # if passes dic will be updated
    dts = f_dates_in_year(bgn, end)
    dic_local = {}
    # WARN: please notice that this part gives a result even holidays_list is empty which conflicts the assumption of Business Date change

    dt_regular_prev = dts[0]
    for dt in dts:
        # if weekend_u_holiday_mapping[combo](dt,holidays_list):

        if dt.weekday() in [5, 6] or dt in holidays_list:
            dt = dt.strftime("%Y%m%d")
            dic_local[dt] = {"h": count}  # h means holiday and r means regular day
        else:
            prev_ = f_DT_STR(dt_regular_prev)
            now_ = f_DT_STR(dt)
            if now_[:-2] != prev_[:-2]:  # this part is used for date convention
                dic_local[f"{now_[:-2]}_MP"] = {f"{now_[:-2]}_MP": now_}
                dic_local[f"{prev_[:-2]}_MF"] = {f"{prev_[:-2]}_MF": prev_}
            dic_local[now_] = {"r": count}
            count += 1
            dt_regular_prev = dt
    # print('in generate cal')
    return dic_local


def test_1():

    rs = get_cal("1 BD|CA")
    return rs


def test_2():  # this is main function test: get_or_create_json. This will get previous result and check if the current search is there. If not, add current search into the result
    for cal in COUNTRY_HOLIDAYS:
        rs = get_cal(cal)


if __name__ == "__main__":
    # get_hol_list(YRS)
    # save_hol_json(YRS,cal='NY',combo='WE_u_HOL',dic={})
    # read_hol_json()
    # dic = {'NY_2022_2022':{'1':'a','2':'b','3':'c','4':'z'}}
    dic = {"NY_2022_2022": {"4": "z"}}
    vals_ = dic["NY_2022_2022"]
    key = "dcanvas:holidays:NY_2022_2022"

    rs = get_cal("NY")
