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
    '1y1d' : 14610/4000, # exact average length for post 1582AD change
    '1bd1d' : 14610/4000/252 # assuming 252 denominator
}

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
        years=0, months=0, weeks=0, days=0, w=0, W=0, week=0,

        # auxlillary initializers
        y=0, Y=0, year=0,
        q=0, Q=0, quarter=0, quarters=0,
        m=0, M=0, month=0,
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
        anchor_end=None
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

        self.years = years + year + y + Y
        self.months = months + month + m + M
        self.weeks = + 7*(weeks+week+W+w)
        self.days = days + day + d + D 
        # ^ rd.days included weeks so no need to add again weeks
        self.bd = None if (bd is None and BD is None) else bd or BD

        self._validate_cals(cals)
        self._validate_adj_roll(cals,roll)

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
    def from_relativedelta(rd):
        if isinstance(rd,dateutil.relativedelta.relativedelta):
            return Duration(years=rd.years,months=rd.months,weeks=rd.weeks,days=rd.days)
        elif isinstance(rd,datetime.timedelta):
            return Duration.from_timedelta(rd)
        else:
            raise TypeError(f'Must be relativedelta (or timedelta) not {type(rd).__name__}') 
    
    @staticmethod
    def from_timedelta(td):
        if isinstance(td,datetime.timedelta):
            return Duration(d=td.days)
        else:
            raise TypeError(f'Must be timedelta not {type(td).__name__}') 

    def _validate_adj_roll(self,cals,roll):
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
        elif isinstance(o,( dateutil.relativedelta.relativedelta,Duration)):
            if self.years == o.years:
                if self.months == o.months:
                    if self.weeks == o.weeks:
                        if self.days == o.days:
                            if isinstance(o, Duration):
                                if self.bd == o.bd:
                                    if self.cals == o.cals:
                                        if self.roll == o.roll:
                                            if self.anchor_end == o.anchor_end and self.anchor_start == o.anchor_start:
                                                return True
                        else:
                            return True
            return False
        else:
            raise TypeError(f'Cannot compare with {type(o).__name__}')

    @property
    def relativedelta(self):
        '''
        create relativedelta
        '''
        rd = dateutil.relativedelta.relativedelta(years=self.years,months=self.months,weeks=self.weeks,days=self.days)

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
        """
        if Duration is anchored (it's the result of date math)
            We know the EXACT days implied, so return the count

        If not,
            We MAY or MAY NOT be able to know the exact days

            years, months, and non-None BD's trigger approx calcs, and a WARNING is issued
            pure days and weeks is exact always       
        """

        just_days = 0
        
        if self.anchor_start and self.anchor_end:
            # i am anchored
            just_days += (self.anchor_end-self.anchor_start).days
        else:      
            # i am not anchored
            warns = []  
            if self.years > 0:
                yeardays = APPROX['1y1d']
                just_days += yeardays
                warns.append(f"1y≈{yeardays:.6f}d")

            if self.months >0:
                monthdays = APPROX['1y1d'] / 12
                just_days += monthdays
                warns.append(f"1m≈{monthdays:.6f}m")

            if self.weeks > 0:
                # exact
                just_days += 7
            
            if self.days >0:
                # exact
                just_days += self.days
            
            if self.bd is not None:
                dbds = APPROX['1bd1d']
                just_days += dbds
                warns.append(f"1bd≈{dbds:.6f}d")

        if len(warns)>0:
            w = ','.join(warns)
            message = f'[dateroll] just_days using approx: {w} '
            warnings.warn(message)
        
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
            years = a.years+b.years
            months = a.months+b.months
            days = a.days+b.days
            bd = None if a.bd is None and b.bd is None else (0 if a.bd is None else a.bd) + (0 if b.bd is None else b.bd)
            # union cal sets
            # future, switch these to orNone
            
            if a.cals is not None:
                if b.cals is not None:
                    
                    cals = tuple(set(a.cals) | set(b.cals))
                else:
                    cals = a.cals
            else:
                if b.cals is not None:
                    cals = b.cals
                else:
                    cals = None

            # roll adjustment form math (can be approx)
            # first compute diff, then roll
            """
            add error tolerlance to rough days calc, return n + epsilon
            if epsilon > tolerance, throw error11
            tol = 366/365*y+31/28*m+7/7+1/1+365/252
            see slack for c+b a/e - 8 scenarios, only 2 need approx
            
            """
            if a.roll or b.roll or a.cals or b.cals:
                abd = a.bd
                bbd = b.bd
                if abd and bbd:
                    # only bd's so EXACT diff
                    diff = abd + bbd
                else:
                    ae, adays = a.rough_days
                    be, bdays = b.rough_days
                    diff = adays + bdays
                    
                    if not (ae and be) and diff < 0:
                        # EXACT diff failed, need to tell user approx is involved
                        print(
                            f"**Rare edge case, direction change, with bd/non-bday potential overlap. Check roll.**"
                        )

                # not if net diff is positive, rolling forwards
                _aroll = a.roll if a.roll is not None else ""
                _broll = a.roll if a.roll is not None else ""
                if diff > 0 or (diff==0 and direction==1):
                    if 'P' in _aroll or 'P' in _broll:
                        raise ValueError('In the positive direction, roll should not be P')
                    if "M" in _aroll or "M" in _broll:
                        roll = "MF"
                    else:
                        roll = "F"
                # if net diff is negative, rolling backwards
                else:
                    if 'F' in _aroll or 'F' in _broll:
                        raise ValueError('In the negative direction, roll should not be F')
                    if "M" in _aroll or "M" in _broll:
                        roll = "MP"
                    else:
                        roll = "P"
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
    @property
    def w(self): return self.weeks
    @property
    def W(self): return self.weeks
    @property
    def week(self): return self.weeks

PeriodLike = PeriodLike + (Duration,)


if __name__ == "__main__":
    ...
    # dur2 = Duration()
    from dateroll.date.date import Date
    dt2 = Date(2024,1,15)
    dt1 = Date(2024,1,1)
    dur = dt2 - dt1

