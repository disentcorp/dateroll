import pandas as pd
import requests
import datetime
from dateutil.relativedelta import relativedelta as rd
from zoneinfo import ZoneInfo
from dateroll import ddh
import yfinance as yf
import pandas_datareader.data as web
import code

# P = "tests/test_data/spy.csv"
P = "tests/test_data/tsla.csv"
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



def gdp():
    import pandas_datareader.data as web
    import datetime

    # Define the start and end dates
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical GDP data from FRED
    gdp_data = web.DataReader('GDP', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    gdp_data['Change'] = gdp_data['GDP'].pct_change()
    avg_growth = gdp_data['Change'].mean() * 100
    print("/////// GDP Data //////////")
    print(gdp_data.head())
    print('////////////////\n')

    print(f"Average Monthly GDP Growth: {avg_growth:.2f}%")

def cpi():
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical CPI data from FRED
    cpi_data = web.DataReader('CPIAUCSL', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    cpi_data['Change'] = cpi_data['CPIAUCSL'].pct_change()
    inflation_rate = cpi_data['Change'].mean() * 100
    print("/////// CPI Data //////////")
    print(cpi_data.head())
    print('////////////////\n')
    print(f"Average Monthly Inflation Rate: {inflation_rate:.2f}%")

def unemployment():
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical unemployment rate data from FRED
    unemployment_data = web.DataReader('UNRATE', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    unemployment_data['Change'] = unemployment_data['UNRATE'].pct_change()
    avg_unemployment = unemployment_data['Change'].mean() * 100
    print("/////// Unemployment Data //////////")
    print(unemployment_data.head())
    print('////////////////\n')
    print(f"Average Monthly Unemployment Rate Change: {avg_unemployment:.2f}%")

def interest():
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical Fed Funds Rate data from FRED
    fed_rate_data = web.DataReader('FEDFUNDS', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    fed_rate_data['Change'] = fed_rate_data['FEDFUNDS'].pct_change()
    avg_fed_rate_change = fed_rate_data['Change'].mean() * 100
    print("/////// Fed Rate Data //////////")
    print(fed_rate_data.head())
    print('////////////////\n')
    print(f"Average Monthly Fed Rate Change: {avg_fed_rate_change:.2f}%")

def exchange():
    eur_usd = yf.download('EURUSD=X', start='2010-01-01', end='2024-01-01', interval='1d')
    eur_usd['Change'] = eur_usd['Close'].pct_change()
    avg_exchange_rate_change = eur_usd['Change'].mean() * 100
    print("/////// EURUSD Data //////////")
    print(eur_usd.head())
    print('////////////////\n')
    print(f"Average Daily EUR/USD Change: {avg_exchange_rate_change:.2f}%")

def oil():
    oil_data = yf.download('CL=F', start='2010-01-01', end='2024-01-01', interval='1d')
    oil_data['Change'] = oil_data['Close'].pct_change()
    avg_oil_price_change = oil_data['Change'].mean() * 100
    print("/////// OIL Data //////////")
    print(oil_data.head())
    print('////////////////\n')
    print(f"Average Daily Oil Price Change: {avg_oil_price_change:.2f}%")

def yield_curv():
    yield_data = web.DataReader('DGS10', 'fred', start='2010-01-01', end='2024-01-01')
    yield_data['Change'] = yield_data['DGS10'].pct_change()
    avg_yield_change = yield_data['Change'].mean() * 100
    print("/////// Yield Data //////////")
    print(yield_data.head())
    print('////////////////\n')
    print(f"Average Monthly 10-Year Yield Change: {avg_yield_change:.2f}%")

def consumer():
    
    # Define the start and end dates
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical consumer confidence data from FRED
    consumer_confidence = web.DataReader('UMCSENT', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    consumer_confidence['Change'] = consumer_confidence['UMCSENT'].pct_change()
    avg_confidence_change = consumer_confidence['Change'].mean() * 100
    print("/////// Consumer Data //////////")
    print(consumer_confidence.head())
    print('////////////////\n')
    print(f"Average Monthly Consumer Confidence Change: {avg_confidence_change:.2f}%")

def housing():
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical housing starts data from FRED
    housing_starts = web.DataReader('HOUST', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    housing_starts['Change'] = housing_starts['HOUST'].pct_change()
    avg_housing_change = housing_starts['Change'].mean() * 100
    print("/////// Housing Data //////////")
    print(housing_starts.head())
    print('////////////////\n')
    print(f"Average Monthly Housing Starts Change: {avg_housing_change:.2f}%")

def corp_earn():
    earnings_data = yf.download('AAPL', start='2010-01-01', end='2024-01-01', interval='1d')
    earnings_data['Change'] = earnings_data['Close'].pct_change()
    avg_earnings_change = earnings_data['Change'].mean() * 100
    print("/////// Earnings Data //////////")
    print(earnings_data.head())
    print('////////////////\n')
    print(f"Average Daily Earnings Change (AAPL): {avg_earnings_change:.2f}%")

def trade_balance():
    import pandas_datareader.data as web
    import datetime

    # Define the start and end dates
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical trade balance data from FRED
    trade_balance = web.DataReader('BOPGSTB', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    trade_balance['Change'] = trade_balance['BOPGSTB'].pct_change()
    avg_trade_change = trade_balance['Change'].mean() * 100
    print("/////// Trade Balance Data //////////")
    print(trade_balance.head())
    print('////////////////\n')
    print(f"Average Monthly Trade Balance Change: {avg_trade_change:.2f}%")

def labor():
    import pandas_datareader.data as web
    import datetime

    # Define the start and end dates
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical jobless claims data from FRED
    jobless_claims = web.DataReader('ICSA', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    jobless_claims['Change'] = jobless_claims['ICSA'].pct_change()
    avg_claims_change = jobless_claims['Change'].mean() * 100
    print("/////// Jobless Data //////////")
    print(jobless_claims.head())
    print('////////////////\n')
    print(f"Average Monthly Jobless Claims Change: {avg_claims_change:.2f}%")

def industrial():
    import pandas_datareader.data as web
    import datetime

    # Define the start and end dates
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical industrial production data from FRED
    industrial_production = web.DataReader('INDPRO', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    industrial_production['Change'] = industrial_production['INDPRO'].pct_change()
    avg_production_change = industrial_production['Change'].mean() * 100
    print("/////// Inustrial Production Data //////////")
    print(industrial_production.head())
    print('////////////////\n')
    print(f"Average Monthly Industrial Production Change: {avg_production_change:.2f}%")

def retail():
    import pandas_datareader.data as web
    import datetime

    # Define the start and end dates
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical retail sales data from FRED
    retail_sales = web.DataReader('RSXFS', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    retail_sales['Change'] = retail_sales['RSXFS'].pct_change()
    avg_sales_change = retail_sales['Change'].mean() * 100
    print("/////// Retail Sales Data //////////")
    print(retail_sales.head())
    print('////////////////\n')
    print(f"Average Monthly Retail Sales Change: {avg_sales_change:.2f}%")

def treasury():
    import pandas_datareader.data as web
    import datetime

    # Define the start and end dates
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical 10-year Treasury yield data from FRED
    treasury_yield = web.DataReader('DGS10', 'fred', start_date, end_date)

    # Calculate the monthly percentage change
    treasury_yield['Change'] = treasury_yield['DGS10'].pct_change()
    avg_yield_change = treasury_yield['Change'].mean() * 100
    print("/////// Treasure Yield Data //////////")
    print(treasury_yield.head())
    print('////////////////\n')
    print(f"Average Monthly 10-Year Treasury Yield Change: {avg_yield_change:.2f}%")

def credit_risk():
    import pandas_datareader.data as web
    import datetime

    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    corp_bond_spread = web.DataReader('BAMLC0A0CM', 'fred', start_date, end_date)
    corp_bond_spread['Change'] = corp_bond_spread['BAMLC0A0CM'].pct_change()
    avg_spread_change = corp_bond_spread['Change'].mean() * 100
    print("/////// Bond Spread Data //////////")
    print(corp_bond_spread.head())
    print('////////////////\n')
    print(f"Average Monthly Corporate Bond Spread Change: {avg_spread_change:.2f}%")

def green_bond():
    import pandas_datareader.data as web
    import datetime

    start_date = datetime.datetime(2015, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    green_bonds = web.DataReader('GBBL', 'fred', start_date, end_date)
    green_bonds['Change'] = green_bonds['GBBL'].pct_change()
    avg_green_bonds_change = green_bonds['Change'].mean() * 100
    print("/////// Green Bonds Data //////////")
    print(green_bonds.head())
    print('////////////////\n')
    print(f"Average Monthly Green Bonds Change: {avg_green_bonds_change:.2f}%")

def high_yield():
    import pandas_datareader.data as web
    import datetime

    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    high_yield_bonds = web.DataReader('BAMLH0A0HYM2', 'fred', start_date, end_date)
    high_yield_bonds['Change'] = high_yield_bonds['BAMLH0A0HYM2'].pct_change()
    avg_high_yield_change = high_yield_bonds['Change'].mean() * 100
    print("/////// High Yield Bonds Data //////////")
    print(high_yield_bonds.head())
    print('////////////////\n')
    print(f"Average Monthly High-Yield Bonds Change: {avg_high_yield_change:.2f}%")

def investment_grade_bonds():

    start_date = datetime.datetime(2018, 1, 1)
    end_date = datetime.datetime(2024, 1, 1)

    # Fetch historical data for BWX from Yahoo Finance
    global_bonds = web.DataReader('BWX', 'yahoo', start_date, end_date)

    # Calculate the monthly percentage change
    global_bonds['Change'] = global_bonds['Close'].pct_change()
    avg_global_change = global_bonds['Change'].mean() * 100
    print(f"Average Monthly Global Bond Market Change: {avg_global_change:.2f}%")
if __name__=="__main__":
    
    print(investment_grade_bonds())
    
    
    

    