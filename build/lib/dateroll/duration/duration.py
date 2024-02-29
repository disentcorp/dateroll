import datetime

import dateutil
import dateutil.relativedelta

from dateroll.calendars.calendarmath import calmath

cals = calmath.cals

period_order = (*"yhsqmwd", "cals", "roll")

PeriodLike = (dateutil.relativedelta, datetime.timedelta)

VALID_ROLL_CONVENTIONS = {"F", "P", "MF", "MP"}


def addNones(*args, zeros=False):
    """
    helper to add None's with numbers
    None+0 = 0
    None+1 = 1
    0 + None = 0
    None+None = None (if zeros=False)
    None+None = 0 (if zeros = True)
    """
    if zeros:
        sum = 0
    else:
        sum = None
        for arg in args:
            if arg is not None:
                if not sum:
                    sum = arg
                else:
                    sum += arg
    return sum


class Duration(dateutil.relativedelta.relativedelta):
    """
    we do not inherit from relativedelta or timedelta, it is something to be considered

    Duration class represents a period of time, a duration of time, an interval of time
    i.e. some distance of time between two specific (yet unknown) dates

    there's implicitly 2 modes:

    calendar day mode - no knowledge of holidays or non-working days
        When counting days, there is no skipping over some days over others because a governing body declares that the offices are closed.

    business day mode -
        a) implicit assumption that 'WE' is always used in bd calcs
            'WE' stands for [W]eek[End] which is our internal two-letter code for the holiday of Saturdays and Sunday's during the "reasonable business period"
        b) user supplied holiday vectors can be unioned for adjusting accordingly

        bd adjustment is O(1) assuming the calenders are in memory or the unions are cached, worst
        bd adjustment is O(n) on bd's between two dates.

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

    # on init, should we turn hemi/sem into 6mo and quarters into 3m?
    collapse_hemi_sem_quart_on_init = True

    def __init__(
        self,
        y=None,
        Y=None,
        h=None,
        H=None,
        s=None,
        S=None,
        q=None,
        Q=None,
        m=None,
        M=None,
        w=None,
        W=None,
        d=None,
        D=None,
        cals=None,
        bd=None,
        BD=None,
        roll=None,
    ):
        """
        y = year
        h = half year
        s = semester = half year
        q = quarter
        m = month
        w = week
        d = day
        bd = business days
        cals = list of 2-letter codes for calendars
        roll = roll convention (F,P,MF,MP)

        ^ non means not supplied, 0 means zero supplied

        collapse_hemi_sem_quart_on_init keeps just:
        y,m,w,d (for dateutil support)

        class instance keeps one of each, None if no value
        """
        self.y = addNones(y, Y)
        if self.collapse_hemi_sem_quart_on_init:
            _m = addNones(
                addNones(m, M),
                3 * addNones(q, Q, zeros=True),
                6 * addNones(s, S, h, H, zeros=True),
            )
            if _m != 0:
                self.m = _m
            else:
                self.m = None
        else:
            self.m = addNones(m, M)
        self.w = addNones(w, W)
        self.d = addNones(d, D)
        self.bd = addNones(bd, BD)

        if cals is not None:
            _cals = set()
            if isinstance(cals, str):
                cals = [cals]
            elif hasattr(cals, "__iter__"):
                for cal in cals:
                    if isinstance(cal, str):
                        if len(cal) == 2:
                            _cals |= {
                                cal,
                            }
                        else:
                            raise Exception(
                                f"Calendars must be 2-letter strings (not {cal})"
                            )
                    else:
                        raise Exception(
                            f"Calendars must be strings (not {type(cal).__name__})"
                        )
            self.cals = _cals
        else:
            self.cals = None

        if self.bd is None and cals and len(cals) > 0:
            self.bd = 0

        # add weekends if adjusting
        if self.bd is not None:
            if self.cals:
                self.cals |= {
                    "WE",
                }
            else:
                self.cals = {
                    "WE",
                }

        # now validate roll
        if roll is not None:
            if isinstance(roll, str):
                if roll in VALID_ROLL_CONVENTIONS:
                    self.roll = roll
                else:
                    NotImplementedError(roll)
            else:
                raise Exception("roll must be a str")
        else:
            if self.bd is not None:
                if self.bd >= 0:
                    self.roll = "F"
                elif self.bd < 0:
                    self.roll = "P"
                else:
                    raise NotImplementedError("n/a")
            else:
                self.roll = None

    @property
    def delta(self):
        """ """
        rd_args = {}
        if self.y:
            rd_args["years"] = self.y
        if self.m:
            rd_args["months"] = self.m
        if self.w:
            rd_args["weeks"] = self.w
        if self.d:
            rd_args["days"] = self.d

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
        if self.roll is not None:
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
        ...

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
        if self.y is not None:
            exact = exact and False
            days += 365.25 * self.y
        if self.m is not None:
            exact = exact and True
            days += 12 * self.m
        if self.w is not None:
            exact = exact and True
            days += 7 * self.w
        if self.d is not None:
            exact = exact and True
            days + self.d
        if self.bd is not None:
            exact = exact and False
            days += 365 / 252 * self.bd
        return exact, days

    @property
    def bd_only(self):
        if self.y is None and self.m is None and self.w is None and self.bd is not None:
            return self.bd
        else:
            return False

    def math(self, b, direction):
        """
        c = a + b
        """
        from dateroll.date.date import Date

        a = self

        # duration + duration
        if isinstance(b, Duration):
            """
            combine both
            """
            y = addNones(a.y, b.y)
            m = addNones(a.m, b.m)
            w = addNones(a.w, b.w)
            d = addNones(a.d, b.d)
            bd = addNones(a.bd, b.bd)

            # union cal sets
            # future, switch these to orNone
            if a.cals is not None:
                if b.cals is not None:
                    cals = a.cals | b.cals
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
                abd = a.bd_only
                bbd = b.bd_only
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
                if diff > 0:
                    _aroll = a.roll if a.roll is not None else ""
                    _broll = a.roll if a.roll is not None else ""
                    if "M" in _aroll or "M" in _broll:
                        roll = "MF"
                    else:
                        roll = "F"
                # if net diff is negative, rolling backwards
                else:
                    if "M" in a.roll or "M" in b.roll:
                        roll = "MP"
                    else:
                        roll = "P"
            else:
                roll = None

            c = Duration(y=y, m=m, w=w, d=d, bd=bd, roll=roll, cals=cals)
            return c

        # duration + rd() --- should not happen
        elif isinstance(b, dateutil.relativedelta.relativedelta):
            return self
            # raise NotImplementedError('need to cast rd')

        elif isinstance(b, Date):
            # adjust b for Non-bd's FIRST
            b_moved = b + self.delta * direction

            # # if you have bd's, then use bd adj and roll:
            if self.bd or self.cals or self.roll:
                shift_adj = self.apply_business_date_adjustment(b_moved)
            else:
                shift_adj = b_moved

            # convert back to dateroll.Date
            return Date.from_datetime(shift_adj)

        else:
            raise NotImplementedError

    @property
    def q(self):
        """equiv quarters"""
        raise NotImplementedError

    @property
    def s(self):
        """equiv semesters"""
        raise NotImplementedError

    ...  # q, w, h, d, bd(with cal), y {implicit act/365, can be setting,} y(with counter)
    # m, ...

    def __radd__(self, x):
        return self.math(x, 1)

    def __rsub__(self, x):
        return self.math(x, -1)

    def __add__(self, x):
        return self.math(x, 1)

    def __sub__(self, x):
        return self.math(x, -1)

    def __iadd__(self, x):
        return self.math(x, 1)

    def __isub__(self, x):
        return self.math(x, -1)

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


PeriodLike = PeriodLike + (Duration,)


if __name__ == "__main__":
    ...
