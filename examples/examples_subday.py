import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta as rd

from dateroll import ddh

import code

P = "tests/test_data/spy.csv"

def get_data():

    df = pd.read_csv(P,header=[0],index_col=[0])

    df["t"] = df["t"].apply(lambda x:ddh.Date.from_timestamp(x / 1000).est.naive.iso)
    df.index = pd.to_datetime(df['t'])
    return df

def cut_data(df,cut_date="10102022"):
    cut = ddh(cut_date).iso
    df = df[df["t"] >= cut]
    return df

def get_mkt(df):
    
    st = ddh('9h30min').time
    ed = ddh('16h').time
    df = df.between_time(st,ed)
    return df

def get_max_pre_mkt(df):
    # 1 choose date
    # 2 premarket high
    # 3 mkt high
    # old way
    od = datetime.date(2022,10,10).strftime('%Y-%m-%d')
    old = df.loc[od]
    opre = old.between_time(datetime.time(4,0),datetime.time(9,29))['h'].max()
    omkt = old.between_time(datetime.time(9,30),datetime.time(16,0))['h'].max()

    ### new way
    nd = ddh('10102022').strftime('%Y-%m-%d')
    new = df.loc[nd]
    npre = new.between_time(ddh('4h').time,ddh('9h29min').time)['h'].max()
    nmkt = new.between_time(ddh('9h30min').time,ddh('16h').time)['h'].max()
    
    return omkt,opre,nmkt,npre

def get_interval(df):
    ### get price at 3 minute interval with eastern time zone
    interval = ddh('2022-10-10T09:30:00,2022-10-10T16:00:00,3min').est.naive.iso.list
    new_3min = df[df['t'].isin(interval)]
    # old way

    ed = datetime.datetime(2022,10,10,16)
    x = datetime.datetime(2022,10,10,9,30)
    interval_old = [x.isoformat()]
    while x<ed:
        x = x+rd(minutes=3)
        interval_old.append(x.isoformat())

    old_3min = df[df['t'].isin(interval_old)]
    return new_3min,old_3min

def get_mkt_high_time_interval(df,interval="3m"):
    """
        get the average high time for the last interval
        then you can take a short position around that time
    """
    mkt = get_mkt(df)
    # sort index descending
    mkt = mkt.sort_index(ascending=False)
    last_day_iso = mkt['t'][0]
    last_day_ddh = ddh(last_day_iso)
    # get date 3m before the last day
    day_3m = (last_day_ddh - ddh('3m')).mdy
    mkt = cut_data(mkt,cut_date=day_3m)

    # get daily high on each day
    
    mx_daily = mkt['h'].resample('D').apply(lambda x: x.idxmax())
    print('in get mkt high')
    import code;code.interact(local=dict(globals(),**locals()))
    # max_times = []
    # for t in mx_daily.index:
    #     d = mkt.iloc[t]
    #     max_tm = d.argmax()
        

    return 











if __name__=="__main__":
    df = get_data()
    highs = get_mkt_high_time_interval(df)

    # get the last 3 month of data
    last_3m_df = df[df['t']>=ddh('t-3m').iso]