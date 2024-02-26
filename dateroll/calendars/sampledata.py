import datetime
from dateutil.relativedelta import relativedelta as rd
from workalendar.usa import FederalReserveSystem
from workalendar.europe.european_central_bank import EuropeanCentralBank
from workalendar.europe.united_kingdom import UnitedKingdom
from workalendar.asia.japan import JapanBank
from workalendar.america.brazil import Brazil

DEFAULT_YEAR_RANGE=200

def generate_ALL_and_WE(n=DEFAULT_YEAR_RANGE):
    '''
    generate set of all days in some "big range"
    generate set of holidays where holiday is saturday or sunday in some "big range"
    return both sets
    '''
    t_start = datetime.date.today() - rd(years=n)
    t_end = datetime.date.today() + rd(years=n)

    t = t_start
    ALL = set()
    WE = set()
    while t < t_end:
        ALL |= {t,}
        if t.weekday() in (5,6):
            WE |= {t,}
        t += rd(days=1)
    
    return ALL,WE

def generate_Workalendar(cls,n=DEFAULT_YEAR_RANGE):
    '''
    use 3rd party library to get set of use federal holidays, return as set
    '''
    y = datetime.datetime.today().year
    l = set()
    inst = cls()
    for year in range(y-n,y+n):
        hols = inst.holidays(year)
        l |= set(_[0] for _ in hols)
    return l


def load_sample_data(cals,n=DEFAULT_YEAR_RANGE):
    ALL , WE = generate_ALL_and_WE(n)
    NY = FED = generate_Workalendar(FederalReserveSystem,n=n)
    EU = ECB = generate_Workalendar(EuropeanCentralBank,n=n)
    LN = BOE = generate_Workalendar(UnitedKingdom,n=n)
    BR = BCB = generate_Workalendar(Brazil,n=n)

    cals['ALL'] = ALL
    cals['WE'] = WE

    cals['NY'] = NY
    cals['LN'] = LN
    cals['BR'] = BR

    cals['ECB'] = ECB
    cals['FED'] = FED

if __name__ == '__main__':
    from dateroll.calendars.calendars import Calendars

    cals = Calendars()

    load_sample_data(cals,n=200)
