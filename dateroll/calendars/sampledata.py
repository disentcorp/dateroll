"""
used to generate dateroll/sampledata/*.csv before packaging wheel
"""

import datetime
import os
import pathlib

from dateutil.relativedelta import relativedelta as rd
from workalendar.america.brazil import Brazil
from workalendar.europe.european_central_bank import EuropeanCentralBank
from workalendar.europe.united_kingdom import UnitedKingdom
from workalendar.usa import FederalReserveSystem
import QuantLib as ql

DEFAULT_YEAR_RANGE = 200

def generate_Workalendar(cls, n=DEFAULT_YEAR_RANGE):
    """
    use 3rd party library to get set of use federal holidays, return as set
    """
    y = datetime.datetime.today().year
    list_ = set()
    inst = cls()
    for year in range(y - n, y + n):
        hols = inst.holidays(year)
        list_ |= set(_[0] for _ in hols)
    return list_

def generate_ql_holidays(cls,n=DEFAULT_YEAR_RANGE):
    """
        t1 and t2 must be in [1901,2199]
    """
    t = datetime.date.today()
    begin_year = max(t.year-n,1901)
    end_year = min(t.year+n,2199)
    t1 = ql.Date(t.day,t.month,begin_year)
    t2 = ql.Date(t.day,t.month,end_year)
    if cls=="BR":
        cal = ql.Brazil(ql.Brazil.Exchange)
    else:
        raise NotImplementedError("Currently only support brazil holidays")
    list_ = ql.Calendar.holidayList(cal,t1,t2)
    list_ = set([d.to_date() for d in list_])
    list_ = sorted(list_)
    return list_




def generate_ALL_and_WE(n=DEFAULT_YEAR_RANGE):
    """
    generate set of all days in some "big range"
    generate set of holidays where holiday is saturday or sunday in some "big range"
    return both sets
    """
    t_start = datetime.date.today() - rd(years=n)
    t_end = datetime.date.today() + rd(years=n)

    t = t_start
    ALL = set()
    WE = set()
    while t < t_end:
        ALL |= {
            t,
        }
        if t.weekday() in (5, 6):
            WE |= {
                t,
            }
        t += rd(days=1)

    return ALL, WE


def generate_sample_data(cals, n=DEFAULT_YEAR_RANGE):
    """
        brazil holidays are not complete in workalender so we used 
        brazil holidays of quantlibe
    """
    ALL, WE = generate_ALL_and_WE(n)
    
    data = {
        "ALL": ALL,
        "WE": WE,
        "NY": generate_Workalendar(FederalReserveSystem, n=n),
        "EU": generate_Workalendar(EuropeanCentralBank, n=n),
        "LN": generate_Workalendar(UnitedKingdom, n=n),
        "BR": generate_ql_holidays("BR", n=n),
    }

    for calendar_name, list_of_dates in data.items():
        p = f"{ROOT_DIR}/dateroll/sampledata/{calendar_name}.csv"
        filename = pathlib.Path(p)
        
        with open(filename, "w") as f:
            list_ = [i.isoformat() + "\n" for i in list_of_dates]
            f.writelines(list_)



if __name__ == "__main__":
    ROOT_DIR = pathlib.Path(__file__).parents[2]
    data = generate_sample_data("Na")
    
