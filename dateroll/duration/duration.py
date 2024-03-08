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

def add_none(a,b):
    if a is None and b is None:
        return None
    else:
        a = 0 if a is None else a
        b = 0 if b is None else b
        return a + b

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
        anchor_start=None,
        anchor_end=None,
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

        self.anchor_start = anchor_start
        self.anchor_end = anchor_end

        # merge y/m/w/d
        self.years = years + year + y + Y
        self.months = months + month + m + M
        self.days = days + day + d + D + 7*(weeks + week + W + w)

        if abs(self.months) >= 12:
            self.years+= int(self.months/12)
            self.months-= 12*int(self.months/12)

        self.process_anchor_dates()

        # merge bd
        self.bd = None if (bd is None and BD is None) else bd or BD

        # valid cals
        self._validate_cals(cals)

        # valid adj
        self._validate_adj_roll(cals,roll)

    def process_anchor_dates(self):
        from dateroll.date.date import Date
        if self.anchor_start and self.anchor_end:
            # anchor months -- month diff without days and years collapses into months
            self.anchor_start=Date.from_datetime(self.anchor_start)
            self.anchor_end=Date.from_datetime(self.anchor_end)
            ydiff = self.anchor_end.year - self.anchor_start.year
            mdiff = self.anchor_end.month - self.anchor_start.month
            diff = mdiff + ydiff*12
            self_anchor_years = ydiff
            self._anchor_months = diff        
            #anchor days  --- date diff but WITHOUT dates
            b = self.anchor_end.date
            a = self.anchor_start.date
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
    def from_relativedelta(rd,anchor_start=None,anchor_end=None):
        if isinstance(rd,dateutil.relativedelta.relativedelta):
            return Duration(years=rd.years,months=rd.months,days=rd.days,anchor_start=anchor_start,anchor_end=anchor_end)
        elif isinstance(rd,datetime.timedelta):
            return Duration.from_timedelta(rd,anchor_start=anchor_start,anchor_end=anchor_end)
        else:
            raise TypeError(f'Must be relativedelta (or timedelta) not {type(rd).__name__}') 
    
    @staticmethod
    def from_timedelta(td,anchor_start=None,anchor_end=None):
        if isinstance(td,datetime.timedelta):
            return Duration(days=td.days,anchor_start=anchor_start,anchor_end=anchor_end)
        else:
            raise TypeError(f'Must be timedelta not {type(td).__name__}') 

    def _validate_adj_roll(self,cals,roll):

        # if roll and 0 raise error
        if self.bd==0 and roll:
            raise Exception('cannot have bd=0 and roll at same time')

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
                                        if self.anchor_end == o.anchor_end and self.anchor_start == o.anchor_start:
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

    def apply_business_date_adjustment(self, from_date):
        """
        2 steps:
        1 calendar count #bd's
        2 apply roll convention
        """
        if self.bd is not None:
            adjusted = self.adjust_bds(from_date)
        else:
            adjusted = from_date
        if self.roll is not None and self.bd is None:
            # if self.bd is not None, it will add another 1 bd which is wrong
            rolled_and_adjusted = self.apply_roll_convention(adjusted)
        else:
            rolled_and_adjusted = adjusted
        
        return rolled_and_adjusted

    def apply_roll_convention(self, from_date):
        """
        uses CalendarMath for roll
        """
        roll = self.roll
        if roll == "P":
            return calmath.prev_bd(from_date, cals=self.cals)
        elif roll == "MP":
            return calmath.prev_bd(from_date, cals=self.cals, mod=True)
        elif roll == "F":
            return calmath.next_bd(from_date, cals=self.cals)
        elif roll == "MF":
            return calmath.next_bd(from_date, cals=self.cals, mod=True)
        else:
            raise Exception("Unhandled roll: Must be /F, /P / MF/ /MP")

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
        
        if self.anchor_start and self.anchor_end and not _force_approx:
            # i am anchored
            just_days += (self.anchor_end-self.anchor_start).days
        else:      
            # i am not anchored 
            if self.years != 0:
                yeardays = APPROX['1y1d']*self.years
                just_days += yeardays
                warns.append(f"1y≈{yeardays:.6f}d")

            if self.months != 0:
                monthdays = APPROX['1y1d'] / 12 * self.months
                just_days += monthdays
                warns.append(f"1m≈{monthdays:.6f}m")

            just_days += self.days
            
            if self.bd is not None:
                dbds = APPROX['1bd1d']*self.bd
                just_days += dbds
                warns.append(f"1bd≈{dbds:.6f}d")

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
            years   = a.years   +   b.years
            months  = a.months  +   b.months
            days    = a.days    +   b.days
            bd = add_none(a.bd,b.bd) # none or add
            cals = combine_none(a.cals,b.cals) # union

            if a.roll == b.roll:
                # covers both none or both same
                roll = a.roll
            else:
                if a and not b:
                    # a rolls, b doesn't use a
                    roll = a.roll
                elif b and not a:
                    # b rolls, a doesn't use b
                    roll = b.roll
                else:
                    # both roll, but differently
                    # BIGGER dominates, use just day to approxmate, if just_days needs conversion, warn

                    a_days , b_days = a.just_days, b.just_days
                    if (a_days+b_days) > 0:
                        # a dominates
                        roll = a.roll
                        if b.roll and 'M' in b.roll:
                            if 'M' not in roll:
                                roll = f'M{roll}'
                        if isinstance(a_days+b_days,float):
                            warnings.warn(f"[dateroll] Using approx for roll dermination")
                    elif (a_days+b_days) < 0:
                        # b dominates
                        roll = b.roll
                        if a.roll and 'M' in a.roll:
                            if 'M' not in roll:
                                roll = f'M{roll}'
                        if isinstance(a_days+b_days,float):
                            warnings.warn(f"[dateroll] Using approx for roll dermination")
                    else:
                        # perfect offset, indeterminate roll
                        raise ValueError('Dates offset, cannot determine roll direction')

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
                shift_adj = self.apply_business_date_adjustment(b_moved)
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
        return self

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


if __name__ == "__main__":
    ...
    # dur2 = Duration()
    from dateroll.date.date import Date
    dt2 = Date(2024,1,15)
    dt1 = Date(2024,1,1)
    dur = dt2 - dt1

