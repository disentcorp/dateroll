"""
used to generate dateroll/sampledata/*.csv before packaging wheel
"""

import datetime
import os
import pathlib

from dateutil.relativedelta import relativedelta as rd
from workalendar.america.brazil import Brazil
from workalendar.asia.japan import JapanBank
from workalendar.europe.european_central_bank import EuropeanCentralBank
from workalendar.europe.united_kingdom import UnitedKingdom
from workalendar.usa import FederalReserveSystem

DEFAULT_YEAR_RANGE = 200


def generate_Workalendar(cls, n=DEFAULT_YEAR_RANGE):
    """
    use 3rd party library to get set of use federal holidays, return as set
    """
    y = datetime.datetime.today().year
    l = set()
    inst = cls()
    for year in range(y - n, y + n):
        hols = inst.holidays(year)
        l |= set(_[0] for _ in hols)
    return l


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
    ALL, WE = generate_ALL_and_WE(n)
    data = {
        "ALL": ALL,
        "WE": WE,
        "NY": generate_Workalendar(FederalReserveSystem, n=n),
        "EU": generate_Workalendar(EuropeanCentralBank, n=n),
        "LN": generate_Workalendar(UnitedKingdom, n=n),
        "BR": generate_Workalendar(Brazil, n=n),
    }

    for calendar_name, list_of_dates in data.items():
        filename = pathlib.Path(ROOT_DIR / "sampledata/" / f"{calendar_name}.csv")
        with open(filename, "w") as f:
            l = [i.isoformat() + "\n" for i in list_of_dates]
            f.writelines(l)


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    data = generate_sample_data('Na')
    for k, v in data.items():
        print(k, len(v))
