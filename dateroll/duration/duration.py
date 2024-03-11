import datetime

import warnings
import dateutil
import dateutil.relativedelta
from dateroll.calendars.calendarmath import calmath
import dateroll.parser.parsers as parsers
import code

cals = calmath.cals

period_order = (*"yhsqmwd", "cals", "roll")

PeriodLike = (dateutil.relativedelta, datetime.timedelta)

WEEKEND_CALENDAR = 'WE'
VALID_ROLL_CONVENTIONS = {"F", "P", "MF", "MP"}

APPROX = {
    '1y1d' : 14610/40, # exact average length for post 1582AD change
    '1bd1d' : 14610/40/252 # assuming 252 denominator
}

def combine_none(a,b):
    if a is None and b is None:
        return None
    a = [] if a is None else a
    b = [] if b is None else b
    return tuple(sorted(set(a)|set(b)))

def add_none(a,b,dir=1):
    if a is None and b is None:
        return None
    else:
        a = 0 if a is None else a
        b = 0 if b is None else b
        return a + b*dir

class Duration(dateutil.relativedelta.relativedelta):
    """
    inherits from relativedelta

    Duration class represents a distance between two dates. The two dates MAY or MAY NOT be known.

    3 modes of operation:

        1 - Distance ignoring holidays
            e.g. 3 months from today, or t+3m
                why? normal parlance: 3 months from now
        2 - Distance of only non-holidays
            e.g. 2 business days from today (skip weekends and federal holidays), or t+2bd|WEuNY
                why? payment adjustment; bond settlement is t+2bd|WEuFED
        3 - Distance ignoring holidays + distance of only non-holidays
            e.g. 1 months from today and then 2 business days, or t+1m2bd|WEuNY
                why? payment adjustment: credit card is due on the 2nd business day in one month

    A duration can have a number of:
        business days
        days (1d = 1.44bd)
        weeks  (1w=7d)
        months (1m approx 28-31d)
        years (1y=12m)

    ^ in order of seniority


    We define the "reasonable business period" (naiively) as the interval of (t-100y,t+100y)
        this could be extended: from 1582 AD to future if we have historical vectors for holiday calendar changes (i.e. juneteenth 1st occured on X, to map backwards math, and assume last forward for futuree math (e.g. last jubilee was 5cd, and happens every 50years..))
        realistically 5-7 year perfect lookup would be more than substantial for more use cases.
    """

    def __init__(
        self,

        # switch mdy to days, months, years to match td and rd

        # primary initialization properties (match dateutil.relativedelta)
        years=0, months=0,

        # auxlillary initializers
        y=0, Y=0, year=0,
        q=0, Q=0, quarter=0, quarters=0,
        m=0, M=0, month=0,
        weeks=0, days=0, w=0, W=0, week=0,
        d=0, D=0, day=0,
        
        # bd initializer, must be none as 0 and no zero are different
        bd=None,
        # axuliliary bd initi
        BD=None,

        # bd adjustment initializer
        cals=None,
        roll=None,
        
        # anchor dates (if duration is the result of math with some date)
        _anchor_start=None,
        _anchor_end=None,
        _anchor_months=None,
        _anchor_days=None,
    ):
        """
        y = year
        q = quarter
        m = month
        w = week
        d = day
        bd = business days
        cals = list of 2-letter codes for calendars
        roll = roll convention (F,P,MF,MP) <-non means not supplied, 0 means zero supplied
        """

        self._anchor_start = _anchor_start
        self._anchor_end = _anchor_end

        # merge y/m/w/d
        self.years = years + year + y + Y
        self.months = months + month + m + M
        self.days = days + day + d + D + 7*(weeks + week + W + w)

        if abs(self.months) >= 12:
            self.years+= int(self.months/12)
            self.months-= 12*int(self.months/12)

        self.process_anchor_dates()

        # valid cals
        self._validate_cals(cals)

        # merge bd
        if bd is not None and BD is not None:
            self.bd = bd + BD
        elif bd is not None:
            self.bd = bd
        elif BD is not None:
            self.bd = BD
        else:
            self.bd = None

        # valid adj
        self._validate_adj_roll(cals,roll)

    def process_anchor_dates(self):
        from dateroll.date.date import Date
        if self._anchor_start and self._anchor_end:
            # anchor months -- month diff without days and years collapses into months
            self._anchor_start=Date.from_datetime(self._anchor_start)
            self._anchor_end=Date.from_datetime(self._anchor_end)
            ydiff = self._anchor_end.year - self._anchor_start.year
            mdiff = self._anchor_end.month - self._anchor_start.month
            diff = mdiff + ydiff*12
            self_anchor_years = ydiff
            self._anchor_months = diff        
            #anchor days  --- date diff but WITHOUT dates
            b = self._anchor_end.date
            a = self._anchor_start.date
            delta = dateutil.relativedelta.relativedelta(months=diff)
            if a.day==b.day:
                self._anchor_days=0
            else:
                self._anchor_days=(b-(a+delta)).days

    @staticmethod
    def from_string(string):
        if isinstance(string,str):
            from dateroll.parser.parsers import parseDurationString
            durs,s = parseDurationString(string)
            if len(durs)==1 and s in ('+X','X'):
                return durs[0]
            else:
                raise TypeError(f'Could not validate duration string: {string}')
        else:
            raise TypeError(f'Must be string not {type(string).__name__}') 

    @staticmethod
    def from_relativedelta(rd,_anchor_start=None,_anchor_end=None):
        if isinstance(rd,dateutil.relativedelta.relativedelta):
            return Duration(years=rd.years,months=rd.months,days=rd.days,_anchor_start=_anchor_start,_anchor_end=_anchor_end)
        elif isinstance(rd,datetime.timedelta):
            return Duration.from_timedelta(rd,_anchor_start=_anchor_start,_anchor_end=_anchor_end)
        else:
            raise TypeError(f'Must be relativedelta (or timedelta) not {type(rd).__name__}') 
    
    @staticmethod
    def from_timedelta(td,_anchor_start=None,_anchor_end=None):
        if isinstance(td,datetime.timedelta):
            return Duration(days=td.days,_anchor_start=_anchor_start,_anchor_end=_anchor_end)
        else:
            raise TypeError(f'Must be timedelta not {type(td).__name__}') 

    def _validate_adj_roll(self,cals,roll):

        # if roll and 0 raise error
        if self.bd==0 and roll is not None:
            self.bd = None

        if self.bd is None and cals and len(cals) > 0:
            self.bd = 0

        # clean calendars, add weekends
        if self.bd is not None:
            if self.cals:
                # sort and add weekends
                self.cals = tuple(sorted(set([*self.cals,WEEKEND_CALENDAR,])))
            else:
                self.cals = (WEEKEND_CALENDAR,)

        # now validate roll
        if roll is not None:
            if isinstance(roll, str):
                if roll in VALID_ROLL_CONVENTIONS:
                    self.roll = roll
                else:
                     raise ValueError(f"F, P, MF, or MP, not {roll}")
            else:
                raise TypeError("Roll must be a str")
        else:
            ...
            if self.bd is not None:
                if self.bd >= 0:
                    self.roll = "F"
                else:
                    self.roll = "P"
            else:
                self.roll = None

    def _validate_cals(self,cals):
        '''
        
        '''
        _cals = set()
        if cals is not None:
              
            # str parser if required
            if isinstance(cals, str):
                cals = parsers.parseCalendarUnionString(cals)
            
            # process normally
            if isinstance(cals, (list,set,tuple)):
                for cal in cals:
                    if isinstance(cal, str):
                        if len(cal) in (2,3):
                            if cal in calmath.cals:
                                _cals |= {
                                    cal,
                                }
                            else:
                                raise ValueError(f'Calendar {cal} not found')
                        else:
                            raise Exception(
                                f"Calendars must be 2 or 3 letter strings (not {cal})"
                            )
                    else:
                        raise Exception(
                            f"Calendars must be strings (not {type(cal).__name__})"
                        )
            
            _cals = tuple(sorted(_cals))
        else:
            _cals = None

        self.cals = _cals

    def __eq__(self, o):
        """
        equality
        """
        # convert td to rd
        
        if isinstance(o,int):
            return self.just_exact_days==o
        
        if isinstance(o, datetime.timedelta):
            o = dateutil.relativedelta.relativedelta(days = o.days)
        
        if isinstance(o,( dateutil.relativedelta.relativedelta,Duration)):
            if self.years == o.years:
                if self.months == o.months:
                    if self.days == o.days:
                        if isinstance(o, Duration):
                            if self.bd == o.bd:
                                if self.cals == o.cals:
                                    if self.roll == o.roll:
                                        if self._anchor_end == o._anchor_end and self._anchor_start == o._anchor_start:
                                            return True   
                        else:
                            return True

            if isinstance(o,Duration):
                '''
                for durations from date subtraction there is equivalency to whole units
                4/15/24-1/15/23 == 91d == 1y3m == 14m, and all combinations thereof, and vice-versa
                '''
                

                if self.compare_anchors(self,o) or self.compare_anchors(o,self):
                    return True

                
            return False
        else:
            raise TypeError(f'Cannot compare with {type(o).__name__}')

    
    def compare_anchors(self,a,b):
        if hasattr(a,'_anchor_months'):
            am = a._anchor_months
            ad = a._anchor_days
            cond1 = (am == b.months + b.years*12)
            cond2 = (ad == b.days)
            if cond1 and cond2:
                return True
        return False

    @property
    def relativedelta(self):
        '''
        create relativedelta
        '''
        rd = dateutil.relativedelta.relativedelta(years=self.years,months=self.months,days=self.days)

        return rd

    def apply_business_date_adjustment(self,from_date,direction):
        """
        2 steps:
        1 calendar count #bd's
        2 apply roll convention
        """
        from dateroll.date.date import Date
        
        if self.bd is not None:
            adjusted = self.adjust_bds(from_date)
        else:
            adjusted = from_date
        
        if self.roll is not None and (self.bd is None or (self.bd==0 and not Date(from_date.year,from_date.month,from_date.day).is_bd(cals=self.cals))):
            # if self.bd is not None, it will add another 1 bd which is wrong
            rolled_and_adjusted = self.apply_roll_convention(adjusted,direction)
            

        else:
            rolled_and_adjusted = adjusted
        
        if ((self.roll=='MF' and direction>0) or (self.roll=='MP' and direction<0)) and rolled_and_adjusted.month!=from_date.month:
            # find the last/first business date of the month
            new_date = rolled_and_adjusted
            while new_date.month!=from_date.month:
                new_date = Date(new_date.year,new_date.month,new_date.day) + Duration(bd=direction* -1)
            rolled_and_adjusted = new_date
        return rolled_and_adjusted

    def apply_roll_convention(self,from_date,direction):
        """
        uses CalendarMath for roll
        """
        roll = self.roll
        new_date = from_date
        if self.roll not in ['F','MF','P','MP']:
            raise Exception("Unhandled roll: Must be /F, /P / MF/ /MP")
        if roll == "P" and direction<0:
            new_date = calmath.prev_bd(from_date, cals=self.cals)
        elif roll == "MP" and direction<0:
            new_date = calmath.prev_bd(from_date, cals=self.cals, mod=True)
        elif roll == "F" and direction>0:
            new_date = calmath.next_bd(from_date, cals=self.cals)
        elif roll == "MF" and direction>0:
            new_date = calmath.next_bd(from_date, cals=self.cals, mod=True)
        return new_date
    def adjust_bds(self, from_date):
        """
        uses CalendarMath for bd adjustment
        """

        _d = calmath.add_bd(from_date, self.bd, cals=self.cals)
        return _d


    @property
    def just_days(self):
        # count cal days approx warn return always
        return self._just_days()
    
    @property
    def just_approx_days(self):
        #  always approx even if perfect days
        return self._just_days(_force_approx=True)
    
    @property
    def just_exact_days(self):
        # raise execption instead of warn
        return self._just_days(_force_exact=True)

    def _just_days(self,_force_approx=False,_force_exact=False):
        """
        if Duration is anchored (it's the result of date math)
            We know the EXACT days implied, so return the count

        If not,
            We MAY or MAY NOT be able to know the exact days

            years, months, and non-None BD's trigger approx calcs, and a WARNING is issued
            pure days and weeks is exact always       
        """
        warns = [] 
        just_days = 0
       
        if self._anchor_start and self._anchor_end and not _force_approx:
            # i am anchored
            just_days += (self._anchor_end-self._anchor_start).days
        else:      
            # i am not anchored 
            if self.years != 0:
                yeardays = APPROX['1y1d']*self.years
                just_days += yeardays
                warns.append(f"≈{yeardays:.6f}d")

            if self.months != 0:
                monthdays = APPROX['1y1d'] / 12 * self.months
                just_days += monthdays
                warns.append(f"≈{monthdays:.6f}m")

            just_days += self.days
            
            if self.bd is not None:
                if self.bd !=0:
                    dbds = APPROX['1bd1d']*self.bd
                    just_days += dbds
                    warns.append(f"≈{dbds:.6f}d")

        if len(warns)>0:
            w = ','.join(warns)
            message = f'[dateroll] just_days using approx: {w} '
            if not _force_exact:
                warnings.warn(message)
            else:
                raise ValueError(message)
        
        return just_days


    def math(self, b, direction):
        """
        c = a + b
        """
        from dateroll.date.date import Date, DateLike

        a = self
        # duration + duration
        if isinstance(b, Duration):
            """
            combine both
            """
            years   = a.years   +   direction*b.years
            months  = a.months  +   direction*b.months
            days    = a.days    +   direction*b.days
            bd = add_none(a.bd,b.bd,direction) # none or add
            cals = combine_none(a.cals,b.cals) # union

            if a.roll or b.roll:
                if a.roll == b.roll:
                    # covers both none or both same
                    roll = a.roll
                else:
                    if a.roll is not None and b.roll is None:
                        # a rolls, b doesn't use a
                        roll = a.roll
                    elif b.roll is not None and a.roll is None:
                        # b rolls, a doesn't use b
                        roll = b.roll
                    else:
                        # both roll, but differently
                        # BIGGER dominates, use just day to approxmate, if just_days needs conversion, warn

                        a_days , b_days = a.just_days, b.just_days
                        diff = a_days + direction*b_days

                        if diff > 0:
                            # a dominates
                            roll = a.roll
                            if b.roll and 'M' in b.roll:
                                if 'M' not in roll:
                                    roll = f'M{roll}'
                            if isinstance(diff,float):
                                warnings.warn(f"[dateroll] Using approx for roll dermination")
                        elif diff < 0:
                            # b dominates
                            roll = b.roll
                            if a.roll and 'M' in a.roll:
                                if 'M' not in roll:
                                    roll = f'M{roll}'
                            if isinstance(diff,float):
                                warnings.warn(f"[dateroll] Using approx for roll dermination")
                        else:
                            roll = 'F'
                            warnings.warn(f"[dateroll] Perfect offset, using first")
                
            else:
                roll = None
            c = Duration(years=years, months=months, days=days, bd=bd, roll=roll, cals=cals)
            return c

        # duration + rd() --- should not happen
        elif isinstance(b, dateutil.relativedelta.relativedelta):
            return self
            # raise NotImplementedError('need to cast rd')

        elif isinstance(b, DateLike):
            # adjust b for Non-bd's FIRST
            
            b_moved = b.date + self.relativedelta * direction

            # # if you have bd's, then use bd adj and roll:
            if self.bd or self.cals or self.roll:
                shift_adj = self.apply_business_date_adjustment(b_moved,direction)
            else:
                shift_adj = b_moved

            # convert back to dateroll.Date
            dt = Date.from_datetime(shift_adj)
            
            return dt

        else:
            raise NotImplementedError

    def __radd__(self, x):
        # print(type(x), "radd")
        return self.math(x, 1)

    def __rsub__(self, x):
        # print(type(x), "rsub")
        return self.math(x, -1)

    def __add__(self, x):
        # print(type(x), "add")
        return self.math(x, 1)

    def __sub__(self, x):
        # print(type(x), "sub")
        from dateroll import Date
        if isinstance(x,Date):
            raise TypeError('Cannot sub Date from Duration')
        return self.math(x, -1)

    def __iadd__(self, x):
        # print(type(x), "iadd")
        return self.math(x, 1)

    def __isub__(self, x):
        # print(type(x), "isub")
        return self.math(x, -1)

    def __neg__(self):
        raise NotImplementedError("need unary -negative on duration")
        

    def __pos__(self):
        return self

    def __repr__(self):
        """
        repr sorts units by seniority specificed in global

        future note: implicity call the simplify() method before sorting, and repr on the simpllifed version, not direct on __dict__
        consider moving ny/nm/nd/nbd to dict on class??
        """
        d = self.__dict__
        items = {k: d[k] for k in period_order if k in d}
        constructor = ""
        for k, v in self.__dict__.items():
            if v != None or (v == 0 and k == "bd"):
                if k == "roll":
                    v = f'"{v}"'
                constructor += f"{k}={v}, "
        return f'{self.__class__.__name__}({constructor.rstrip(", ")})'

    def __gt__(a,b):
        if isinstance(b,int):
            b = Duration(days=b)
        
        return a.just_days > b.just_days

    def __ge__(a,b):
        if isinstance(b,int):
            b = Duration(days=b)

        return a.just_days >= b.just_days
    
    def __lt__(a,b):
        if isinstance(b,int):
            b = Duration(days=b)

        return a.just_days < b.just_days
    
    def __le__(a,b):
        if isinstance(b,int):
            b = Duration(days=b)
        
        return a.just_days <= b.just_days



    @property
    def y(self): return self.years
    @property
    def Y(self): return self.years
    @property
    def year(self): return self.years
    @property
    def M(self): return self.months
    @property
    def m(self): return self.months
    @property
    def month(self): return self.months
    @property
    def D(self): return self.days
    @property
    def d(self): return self.days
    @property
    def day(self): return self.days

PeriodLike = PeriodLike + (Duration,)


if __name__ == "__main__": # pragma: no cover
    ...
    # dur2 = Duration()
    from dateroll.ddh.ddh import ddh
    dur = ddh('+5bd/F')+ddh('-5bd/P')
    # from dateroll.date.date import Date
    
    
    # dur = Duration(days=4,_anchor_start=Date(2024,3,1),_anchor_end=Date(2024,3,15),roll='F')
    # x = dur.just_days()
    

