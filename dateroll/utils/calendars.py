import pickle
from dateutil.relativedelta import relativedelta as rd
import datetime
from dateutil.rrule import DAILY,SU,SA,rrule
from bidict import bidict

YEAR_RANGE = 100
t = datetime.date.today()
t1 = t - rd(years=YEAR_RANGE)
t2 = t + rd(years=YEAR_RANGE)

def generate_WE():
    _t = t1
    ALL = set()
    WE = set()
    while _t < t2:
        ALL |= {_t,}
        if _t.weekday() in (5,6):
            WE |= {_t,}
        _t += rd(days=1)
    
    return ALL,WE

def generate_US():
    from workalendar.usa import FederalReserveSystem as Fed
    y = datetime.datetime.today().year
    US = set()
    fed = Fed()
    for year in range(y-200,y+200):
        _ = fed.holidays(year)
        US |= set(i[0] for i in _)

    return US


def gen_calendar_dict(cal,ALL):
    cal = sorted(cal)
    all = sorted(ALL)

    calbds = {}
    rev = {}
    
    cal_idx=0
    last_cal = cal[0]

    prev = 0
    for idx,dt in enumerate(sorted(ALL)):
        if dt>=last_cal:
            calbds[dt]=prev
            try:
                last_cal = cal.pop(0)
            except:
                break
        else:
            prev +=1
            calbds[dt]=prev
            rev[prev]=dt

    # for k,v in calbds.items():
    #     print(k.strftime('%a %d%b%y'),v)

    return calbds,rev

def add_bd(d,n,cal):
    A = cals_dict[cal]['A']
    B = cals_dict[cal]['B']
    return B[A[d]+n]

def sub_bd(d,n,cal):
    A = cals_dict[cal]['A']
    B = cals_dict[cal]['B']
    return B[A[d]-n]

def is_bd(d,cal):
    CAL = cals_dict[cal]['CAL']
    return d in CAL

def diff(t1,t2,cal):
    A = cals_dict[cal]['A']
    n = A[t2]-A[t1]
    return n

def create():
    ALL,WE = generate_WE()
    US = generate_US()
    cals = {
        'ALL':ALL,
        'WE':WE,
        'US':US,
        'US_WE':US | WE
    }

    cals_dict = {}
    for k,v in cals.items():
        A,B = gen_calendar_dict(v,ALL)
        cals_dict[k]={'A':A,'B':B,'CAL':v}

    pickle.dump(cals_dict,open('cals.pkl','wb'))

def load():
    cals_dict = pickle.load(open('cals.pkl','rb'))
    return cals_dict

    

if __name__ == '__main__':

    # create()
    cals_dict = load()

    
    t1=t+rd(days=1)
    n=6
    t2 = add_bd(t1,n,"US_WE")
    print(t1.strftime('%a %d%b%y'))
    print(t2.strftime('%a %d%b%y'))
    print((t2-t1).days)

    t1 = t1
    t2 = t1+rd(days=17)
    print(t1.strftime('%a %d%b%y'))
    print(t2.strftime('%a %d%b%y'))
    print(diff(t1,t2,"US_WE"))

    print(is_bd(t,"WE"))
    print(is_bd(t1,"WE"))

    print(sub_bd(t1,21,"WE").strftime('%a %d%b%y'))

# # 5/5/20 + 3bd|NY
# # 5/5/20 -> unix 
# # 5/5/20 - 5/2/1
    


# load/save calendars from json
# load/save calendars to/from pickle with hash
