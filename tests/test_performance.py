# stdlib
import time
import itertools
import random

# 3rd party
import pandas as pd

# disent
from dateroll.ddh.ddh import ddh

DEBUG = True
xprint = lambda *args,**kwargs:print(*args,**kwargs) if DEBUG else None

def sample(p,n=2):
    p = list(p)
    s = []
    hi = len(p)
    for i in range(n):
        try:
            i = random.randrange(0,hi)
        except:
            print(p)
        s.append(p[i])
    return s


def get_dates():
    manyyears = 't-100y,t+100y,1d'
    dates = [i.to_string() for i in ddh(manyyears)]
    return dates
    
def get_durations():
    sign = ('+','-')
    nums = '1,2,3,5,7,10,15,30'.split(',')
    units = ('d','w','m','q','y')
    bds = ('bd',)
    cals = ('','|WE','|NYuLN','NYuLNuBR')
    mod = ('','/MOD')

    # singles
    combos = list(itertools.product(sign,nums,units,cals,mod))
    combos += list(itertools.product(sign,nums,bds,cals,mod))
    singles = [''.join(c) for c in combos]

    # two non-bd
    combos = list(itertools.product(sign,nums,units,nums,units,cals,mod))
    twonon = [''.join(c) for c in combos]

    # one non-bd with bd
    combos = itertools.product(sign,nums,units,nums,bds,cals,mod)
    oneandone =  [''.join(c) for c in combos]

    # two non-bd with bd
    combos = list(itertools.product(sign,nums,units,nums,units,nums,bds,cals,mod))
    threes = [''.join(c) for c in combos]

    # combine
    durations = singles + twonon + oneandone + threes

    return durations

def get_tests():

    dates = get_dates()
    durations = get_durations()

    # dates alone
    d = [{'category':'date parsing','string':i} for i in dates]
    xprint(sample(dates))

    # durations alone
    t = [{'category':'duration parsing','string':i} for i in durations]
    xprint(sample(durations))

    n = 50000

    # date - date
    date_pairs = zip(sample(dates,n),sample(dates,n))
    _ = [f'{d2}-{d1}' for d1,d2 in date_pairs]
    dmd = [{'category':'date math','string':i} for i in _]
    xprint(sample(dmd))

    # date + duration
    date_dur_pairs = zip(sample(dates,n),sample(durations,n))
    _ = [f'{d}+{dur}' for d,dur in date_dur_pairs]
    dpd = [{'category':'date math','string':i} for i in _]
    xprint(sample(dpd))

    # date - duration
    date_dur_pairs = zip(sample(dates,n),sample(durations,n))
    _ = [f'{d}-{dur}' for d,dur in date_dur_pairs]
    dmt = [{'category':'date math','string':i} for i in _]
    xprint(sample(dmt))

    # duation + duration
    dur_pairs = zip(sample(durations,n),sample(durations,n))
    _ = [f'{dur1}+{dur1}' for dur1,dur2 in dur_pairs]
    tpt = [{'category':'date math','string':i} for i in _]
    xprint(sample(tpt))

    # duration - duration
    dur_pairs = zip(sample(durations,n),sample(durations,n))
    _ = [f'{dur1}-{dur1}' for dur1,dur2 in dur_pairs]
    tmt = [{'category':'date math','string':i} for i in _]
    xprint(sample(tmt))

    # combinded
    tests = d + t + dmd + dpd + dmt + tpt + tmt
    return tests

def run(tests):
    results = []
    for idx,test in enumerate(tests):
        if idx%50000==0:
            print('test number',idx)
        a = time.time()
        try:
            answer = str(ddh(test['string']))
            success = True
        except:
            answer = None
            success = False
        b = time.time()
        diff = b-a
        µs = round(1e6*diff,0)
        result = {**test,'answer':answer,'success':success,'duration_µs':µs}
        results.append(result)
    return results


if __name__=='__main__':

    # get tests
    tests = get_tests()

    # run
    tests = get_tests()
    print('num tests',len(tests))
    results = run(tests)

    # presentation
    df = pd.DataFrame(results)
    df.to_excel('perf.xlsx',index=False)

    print(df)
