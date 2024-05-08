import pandas as pd

import QuantLib as ql

from dateroll import ddh

def get_ql_dayCount(x1,x2,count_convention="Act360",cals="NY"):
    d1 = ql.Date(x1.day,x1.month,x1.year)
    d2 = ql.Date(x2.day,x2.month,x2.year)
    if count_convention=="Act360":
        cnv = ql.Actual360().dayCount(d1,d2)/360
    elif count_convention=="Act365":
        cnv = ql.Actual365Fixed().dayCount(d1,d2)/365
    elif count_convention=="30E360":
        cnv = ql.Thirty360(ql.Thirty360.BondBasis).dayCount(d1,d2)/360
    elif count_convention=="bd252":
        # default ie=(], does not support other ie=[],(),[)
        if cals=="NY":
            cal = ql.UnitedStates(ql.UnitedStates.NYSE)
        elif cals=="BR":
            cal = ql.Brazil(ql.Brazil.Exchange)
        else:
            raise NotImplementedError
        cnv = cal.businessDaysBetween(d1,d2,False,True)/252
    return cnv 

if __name__=="__main__":
    df = pd.read_excel("tests/test_data/Day_Count.xlsx",sheet_name="from_to_dates",header=[0])
    f_act360 = lambda x: get_ql_dayCount(x['date1'],x['date2'],count_convention="Act360")
    f_act365 = lambda x: get_ql_dayCount(x['date1'],x['date2'],count_convention="Act365")
    f_30E360 = lambda x: get_ql_dayCount(x['date1'],x['date2'],count_convention="30E360")
    f_bd252 = lambda x: get_ql_dayCount(x['date1'],x['date2'],count_convention="bd252",cals="BR")
    # import code
    # code.interact(local=dict(globals(),**locals()))
    df['date1'] = [ddh(d) for d in df['date1']]
    df['date2'] = [ddh(d) for d in df['date2']]
    disent_act360 = lambda x: (x['date2']-x['date1']).yf('ACT/360')
    disent_act365 = lambda x: (x['date2']-x['date1']).yf('ACT/365')
    disent_30e360 = lambda x: (x['date2']-x['date1']).yf('30E/360')
    disent_bd252 = lambda x: (x['date2']-x['date1']).yf('BD/252',cals="NY")

    df['disent_act360'] = df.apply(disent_act360,axis=1)
    df['disent_act365'] = df.apply(disent_act365,axis=1)
    df['disent_30E360'] = df.apply(disent_30e360,axis=1)
    df['disent_bd252'] = df.apply(disent_bd252,axis=1)
    import code
    code.interact(local=dict(globals(),**locals()))
