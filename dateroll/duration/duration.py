import datetime

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
        years=0, months=0, weeks=0, days=0,

        # auxlillary initializers
        y=0, Y=0, year=0,
        q=0, Q=0, quarter=0, quarters=0,
        m=0, M=0, month=0,
        w=0, W=0, week=0,
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
        self.days = days + day + d + D + 7*(weeks+week+W+w)
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
            return Duration(d=rd.days,m=rd.months,y=rd.years)
        else:
            raise TypeError(f'Must be relativedelta not {type(rd).__name__}') 
    
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
        if isinstance(o, dateutil.relativedelta.relativedelta):
            
            if self.years == o.years:
                if self.months == o.months:
                    if self.weeks == o.weeks:
                        if self.days == o.days:
                            if isinstance(o, Duration):
                                if self.bd == o.bd:
                                    if self.cals == o.cals:
                                        if self.roll == o.roll:
                                            return True
                            else:
                                return True
            return False
        else:
            return False

    @property
    def delta(self):
        """ """
        rd_args = {}
        if self.years:
            rd_args["years"] = self.years 
        if self.months:
            rd_args["months"] = self.months 
        if self.days:
            rd_args["days"] = self.days 

        rd = dateutil.relativedelta.relativedelta(**rd_args)

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

    def simmplify(self):
        """
        excluding business days, from smallest unit (d) to largest (y)
        if units is larger than the next largest unit, and it is perfectly divisible,
        subtract equivalent units from smaller and increment the larger

        e.g.

        25mo = 2y1m (exact)
        5w = 1m1w (approx)
        28d = 1m (approx)

        make a setting to enable approx calculations

        approx:
            28-31 days is 1m
            4w is 1m
        exact:
            12m is 1y

        note - we skip 1w = exactly 7d, because no human knows what 2w3d but they know 17d is roughly 1/2 a month in their head

        note: q, s, and h are automatically converted to more senior buckets

        """
        

    """
    if 3m with calenda
    
    """

    @property
    def rough_days(self):
        """
        convert duration units to "days" with non-anchored period approximations
            e.g. 1y = 365.25 days
                 1bd = 365/252 days
        returns tuple (exact/approx,num days)
        that is if an approximation is used, the 1st part of the return is true
        """
        exact = True
        days = 0
        if self.years is not None:
            exact = exact and False
            days += 365.25 * self.years
        if self.months is not None:
            exact = exact and True
            days += 12 * self.months
        if self.days is not None:
            exact = exact and True
            days + self.days
        if self.bd is not None:
            exact = exact and False
            days += 365 / 252 * self.bd
        return exact, days

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
            b_moved = b.date + self.delta * direction

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

    def just_days(self):
        if self.anchor_start and self.anchor_end:
            return (self.anchor_end-self.anchor_start).days
            

    def simplify(self):
        ...

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

