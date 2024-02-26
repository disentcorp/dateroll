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
    '''
    generate set of all days in some "big range"
    generate set of holidays where holiday is saturday or sunday in some "big range"
    return both sets
    '''
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
    '''
    use 3rd party library to get set of use federal holidays, return as set
    '''
    from workalendar.usa import FederalReserveSystem as Fed
    y = datetime.datetime.today().year
    US = set()
    fed = Fed()
    for year in range(y-200,y+200):
        _ = fed.holidays(year)
        US |= set(i[0] for i in _)

    return US


def gen_calendar_dict(cal,ALL):
    '''
    for a given set of holidays, and a list of all days

    1 - align the all days with the first holiday
    2 - create dictionary k = day in all days, v = number of business days
    3 - create dictionary k = number of business days, v = date of first appearance

    4 - next bdday dictionary 
    5 - previous bday dictionary -- or store on same key
    return both dicts

    '''
    cal = sorted(cal)
    all = sorted(ALL)

    calbds = {}
    rev = {}
    
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

    return calbds,rev

def add_bd(d,n,cal):
    '''
    add's n business days on cal to d
    careful, if n==0, B should auto backtrack, need to verify
    '''
    A = cals_dict[cal]['A']
    B = cals_dict[cal]['B']
    return B[A[d]+n]

def sub_bd(d,n,cal):
    '''
    see commennt under add_bd
    '''
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

def get_next_bd(d,cal,fp=None):
    '''
    go forward, and modify if required....this is same as add_bd n=0, make sure handled 
    '''
    dnew = add_bd(d,0,cal)
    droll = modify(d,dnew,cal,fp)

def get_prev_bd(d,cal):
    '''
    follow get next
    '''
    ...


'''
no need for a roll convention
only to modify whenn you roll too much

add/subb is roll fwd, roll back
if overrolled, then back it up from either side.



'''

def modify(orig_d,adjusted_d,cal,fp=None):
    '''
    only modify if roll is present, only roll is adj on bd in the first place
    push if forward, then take it back until its 'aight
    '''
    from dateroll.duration.duration import Duration
    oy,om, = orig_d.year,orig_d.month
    ay,am = adjusted_d.year, adjusted_d.month
    while oy!=ay and om!=am:
        if fp=='F':
            adjusted_d = adjusted_d - Duration(bd=1,cal=cal)
        elif fp=='P':
            adjusted_d = adjusted_d + Duration(bd=1,cal=cal)
        ay,am = adjusted_d.year, adjusted_d.month
    return adjusted_d

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


class Calendars:
    def __init__(self):
        ...
    def load(self,name):
        ...
    def save(self,name,dates):
        ...


if __name__ == '__main__':

    cals = Calendars()
    US = cals.load('US')
    WE = cals.load('WE')
    l =[a,b,c,d,e,f]
    cals.Save('ME')

    from dateroll import ddh

    from dateroll import ddh,cals


    /F
    /P
    /MF
    /MP

    3m|NUuLN
    
    cals.is_bd(d,cals=[])
    cals.next_bd(d,cals=[],mod=True)
    cals.prev_bd(d,cals=[],mod=False)
    cals.addsub_bd(d,n,cals=['WE','NY'],mod=True)
    cals.bd_diff(d1,d2,cals=[],ie='(]')

    mod if target.monthyear != inception.monthyear, roll in reverse

    

    # save min/max holiday in cal class, why, throw error or warning or setting if calcl' out of range
    ## we do not have a "calendar class" a calendar is just a "list of holidays"
    
    cals.data_location '/home/.dateroll/cals.data'
    cals.info
    cals.keys()
    cals['WE']=[...]
    cals.get('WE')
    x = cals['WE']
    del cals['WE']

    ddh('t+3m|NY')

    cals(Disktionary)

    class Calendar(shelve.shelf):
        ..

WKD
FED x
ECB x
BCB x
BOE x
BOJ x
NY = US = FED
LN = BOE
EU = ECB

cals.add('FED',list_of_dates,aliases=['NY','US'])


class CalendarMath:
    def __init__(self):
        self.cals = Calendar()

Calendar(shelve):
    ...# saves to ~/.daterol/calendar.data