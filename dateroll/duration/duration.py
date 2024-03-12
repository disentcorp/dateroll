import datetime
import copy
import math
import warnings
import dateutil
import dateutil.relativedelta
from dateroll.calendars.calendarmath import calmath
import dateroll.parser.parsers as parsers
import code
from functools import cache

from dateroll.utils import color, xprint

cals = calmath.cals

period_order = (*"yhsqmwd", "cals", "modifier")

DurationLike = (dateutil.relativedelta, datetime.timedelta)
WEEKEND_CALENDAR = 'WE'

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
    global DEBUG_PRINT
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
        modified=False,
        
        # anchor dates (if duration is the result of math with some date)
        _anchor_start=None,
        _anchor_end=None,
        _anchor_months=None,
        _anchor_days=None,

        # debug
        debug = False
    ):
        """
        y = year
        q = quarter
        m = month
        w = week
        d = day
        bd = business days
        cals = list of 2-letter codes for calendars
        modified = False or True (True means stay in month with BD adjustment)
        """
        # merge y/m/w/d
        self.years = years + year + y + Y
        self.months = months + month + m + M
        self.days = days + day + d + D

        # collapse quarters into months
        self.months += 3*(quarters + quarter + Q + q)

        # collapse weeks into days
        self.days += 7*(weeks + week + W + w)

        # assign modified
        self.modified = modified

        # roll up months>12 into years
        if abs(self.months) >= 12:
            self.years+= int(self.months/12)
            self.months-= 12*int(self.months/12)

        # process anchor periods / dates
        self.process_anchor_dates(_anchor_start,_anchor_end)


        # merge bd - FLOAT(x) ensures sign is copied for direction of BD travel
        if bd is not None and BD is not None:
            self.bd = bd + BD
        elif bd is not None:
            self.bd = float(bd)
        elif BD is not None:
            self.bd = float(BD)
        else:
            if cals is not None:
                # implicity calendar for weekends will be set in validate_cals
                self.bd = float(0.0)
            else:
                # definately no bd adjustment 
                self.bd = None
        
        # valid cals
        self._validate_cals(cals)

        # debug
        self.debug = debug

    def process_anchor_dates(self,_anchor_start, _anchor_end):
        '''
        if a period is the result of dates, we can be "more exact" when the user needs the number of days in the period
        '''

        self._anchor_start = _anchor_start
        self._anchor_end = _anchor_end

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
        if isinstance(rd,Duration):
            return rd
        elif isinstance(rd,dateutil.relativedelta.relativedelta):
            return Duration(years=rd.years,months=rd.months,days=rd.days,_anchor_start=_anchor_start,_anchor_end=_anchor_end)
        elif isinstance(rd,datetime.timedelta):
            return Duration.from_timedelta(rd,_anchor_start=_anchor_start,_anchor_end=_anchor_end)
        else:
            raise TypeError(f'Must be relativedelta (or timedelta) not {type(rd).__name__}') 
    
    @staticmethod
    def from_timedelta(td,_anchor_start=None,_anchor_end=None):
        if isinstance(td,Duration):
            return td
        elif isinstance(td,datetime.timedelta):
            return Duration(days=td.days,_anchor_start=_anchor_start,_anchor_end=_anchor_end)
        else:
            raise TypeError(f'Must be timedelta not {type(td).__name__}') 

    def _validate_cals(self,cals):
        '''
        validates calendars are correct
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
            # implicit weekend when using cals
            _cals |= set([WEEKEND_CALENDAR])
            _cals = tuple(sorted(_cals))
            
        else:
            if self.bd is not None:
                # implicit weekend calendar if bd is defined
                _cals = (WEEKEND_CALENDAR,)
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
                                    if self.modified == o.modified:
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
                warns.append(f"≈{monthdays:.6f}d")

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
        from dateroll.date.date import DateLike,Date

        a = self
        # duration + duration
        
        if isinstance(b, Duration):
            """
            combine both

            3 potential sign changers
            if a has direction use as multiplier
            if b has direciton use as multiple
            if subtraction use incoming direction as multipler
            """
            
            # non bd adjustments
            years   = a.years   +   direction * b.years
            months  = a.months  +   direction * b.months
            days    = a.days    +   direction * b.days
            
            # bd adjustments w/o MOD
            bd = add_none(a.bd, b.bd, direction) # none or add
            cals = combine_none(a.cals, b.cals) # union

            # modified / if either has, inherit it
            modified = a.modified or b.modified

            # check combined Duration net direction
            dur = Duration(years=years, months=months, days=days, bd=bd, cals=cals, modified=modified)
           
            return dur

        elif isinstance(b, dateutil.relativedelta.relativedelta):
            '''
            combine rd with self via copy then combine years+months+days from rd into self
            '''
            dur = copy.deepcopy(self)
            dur.years += b.years
            dur.months += b.months
            dur.days += b.days

            return dur

        elif isinstance(b, DateLike):
            '''
            if direction > 0:
                    (Date + Duration) 
                or  (Duration + Date)
            if direction < 0:
                        (Date - Duration) 
            NOT (Duration - Date)
                Date.__rsub__ throws TypeError before it gets here (non-sensical situation)
            '''

            modifed = self.adjust_from_date(b,direction)
            
            dt = Date.from_datetime(modifed)
            return dt

        else:
            raise NotImplementedError

    def adjust_from_date(self,date_unadj,direction):
        """
        4 steps:
            1 - if being subtracted, negate
            2 - perform non-holiday adjustments first, i.e. y's, m's, d's (returns datetime.date)
            3 - perform holiday adjustments second, i.e. bd's (impliying roll from direction via sign on neg, includes -0.0 as backwards)
            4 - perform modified operation, if supplied
            5 - cast datetime.date back into Date
        """
        xprint(f'Adjusting date [[{date_unadj}]] with [[{direction}*{self}]]') if self.debug else None

        # 1 negate if being subtracted
        if direction < 0:
            # Date - Duration
            # if negative, flip sign using __neg__
            negated_self = self.__neg__()
            xprint('negation','before:    ',self,'after:    ',negated_self) if self.debug else None
        else:
            negated_self = self
            xprint('negation: none') if self.debug else None

        # 2 non-holiday adjustments, add D,M,Y
        date_nonhol_adj = date_unadj.date + negated_self.relativedelta
        xprint(lbl='cal adj',before=date_unadj,after=date_nonhol_adj) if self.debug else None
            
        # 3 holiday adjustment, add BD and if modified check, if BD results in diff month, bounce
        if negated_self.bd is not None:
            bd_sign, date_hol_adj = negated_self.adjust_bds(date_nonhol_adj)
            xprint(lbl='hol adj',before=date_nonhol_adj,after=date_hol_adj) if self.debug else None
            if negated_self.modified:
                # modifying from non-hol adjusted to hol-ajusted, could be subjective arg in future that modification is from date_unadj to date_hol_adj
                date_modifed = negated_self.apply_modifier(date_nonhol_adj,date_hol_adj,bd_sign)
                xprint(lbl='mod adj',before=date_hol_adj,after=date_modifed) if self.debug else None
            else:
                date_modifed = date_hol_adj
                xprint('mod: no mod') if self.debug else None
        else:
            date_modifed = date_nonhol_adj
            xprint('no modifier') if self.debug else None

        # 4 convert back to Date
        from dateroll.date.date import Date
        Date_modifed = Date.from_datetime(date_modifed)

        return Date_modifed

    def adjust_bds(self, from_date):
        """
        This moves business days, using the sign of BD, yes, -0.0 means go backwards to the previous business day
        note: calmath.add_bd ALSO handles -0.0BD as well

        returns TUPLE, the holiday/bizday ajusted date, and it's sign: (bd_sign,date_hol_adj)
        """

        if self.bd is None:
            # non-case
            return (1,from_date)
        
        bd_sign = math.copysign(1,self.bd)
        if bd_sign >= 0:
            # FOLLOWING ROLL CONVENTION is handled in +0.0 BD
            date_hol_adj = calmath.add_bd(from_date, abs(self.bd), cals=self.cals)
        else:
            # PREVIOUS ROLL CONVENTION is handled in -0.0 BD
            date_hol_adj = calmath.sub_bd(from_date, abs(self.bd), cals=self.cals)

        return bd_sign, date_hol_adj


    def __hash__(self):
        return hash(str(self.__dict__))

    def apply_modifier(self,before,after,bd_sign):
        '''
        based upon the sign of the business date (yes, includes -0.0 as a previous) perform MODIFIER

        FOLLOWING is handled in +0.0 BD
        PREVIOUS is handled in -0.0 BD

        MODOFIED FOLLOWING is +0.0, then HERE
        MODIFIED PREVIOUS is -0.0, then HERE

        '''
        from dateroll.date.date import Date
        if bd_sign > 0:
            # if went to far, bounce BACKWARD
            
            if after.month != before.month:
                # MODIFIED FOLLOWING SCENARIO
                c = 0
                while after.month != before.month and c < 35:
                    after = Date.from_datetime(after) - Duration(bd=bd_sign)
                    c+=1
                    if c >=35:
                        raise Exception('Unhandled rolling order')
        else:
            # if went to soon, bounce FORWARD
            
            if after.month != before.month:
                # MODIFIED PREVIOUS SCENARIO
                c = 0
                while after.month != before.month and c < 35:
                    after = Date.from_datetime(after) - Duration(bd=bd_sign)
                    c+=1
                    if c >=35:
                        
                        raise Exception('Unhandled rolling order')
            
        
        return after

    def __radd__(self, x):
        xprint(type(x), "radd") if self.debug else None
        return self.math(x, 1)

    def __rsub__(self, x):
        xprint(type(x), "rsub")  if self.debug else None
        
        return self.math(x, -1)

    def __add__(self, x):
        xprint(type(x), "add") if self.debug else None
        return self.math(x, 1)

    def __sub__(self, x):
        xprint(type(x), "sub") if self.debug else None
        from dateroll import Date
        if isinstance(x,Date):
            raise TypeError('Cannot sub Date from Duration')
        return self.math(x, -1)

    def __iadd__(self, x):
        xprint(type(x), "iadd",type(self.math(x, 1))) if self.debug else None
        return self.math(x, 1)

    def __isub__(self, x):
        xprint(type(x), "isub")  if self.debug else None
        return self.math(x, -1)
       
    def __neg__(self):
        '''
        apply negative across all units (distributive property)
        '''
        copy_self = copy.deepcopy(self)
        copy_self.years = -1 * self.years
        copy_self.months = -1 * self.months
        copy_self.days = -1 * self.days

        if copy_self.bd is not None:
            copy_self.bd = -1 * float(self.bd)
        
        return copy_self

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
            if v != None:
                if k=='cals':
                    v = '"'+ 'u'.join(v) + '"'
                constructor += f"{k}={str(v)}, "
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

DurationLike = (Duration,datetime.timedelta,dateutil.relativedelta.relativedelta)


if __name__ == "__main__": # pragma: no cover
    from dateroll.ddh.ddh import ddh
    from dateroll import Date
    from dateroll import Duration
    # from dateroll.duration.duration import Duration ---- if I import like this, isinstance(dur2,Duration) is False
    d1 = Date(2024,1,1)
    dur2 = Duration(d=1)
    newd2 = d1 - dur2
    print(newd2)
    


