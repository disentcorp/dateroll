import datetime
import pathlib
import pickle
import time
import warnings
import code
import math


from dateroll.calendars.calendars import Calendars
from dateroll.utils import safe_open

PARENT_LOCATION = pathlib.Path.home() / ".dateroll/"
PARENT_LOCATION.mkdir(exist_ok=True)
MODULE_LOCATION = PARENT_LOCATION / "calendars/"
MODULE_LOCATION.mkdir(exist_ok=True)
DATA_LOCATION_FILE = MODULE_LOCATION / "compiled_cals"

WEEKEND_CALENDAR = 'WE'
DEFAULT_IE = "(]"


class CalendarMath:
    """
    CalendarMath is a singleton that holds "compiled" version of your Calendars
    Calendar is a dict-on-disk object that stores vectors of all holidays.
    CalendarMath stores calendar unions (cached), bd-counter dictionaries for your calendars, and more, and has a cached-on-disk backend as well.
    If a mutation of a calendar is detected, cached is purged and CalendarMath triggers a rebuild.

    CalendarMath operationsa are used by Duration and Date:

    add_bd(d,n,cals)    - add n bd's do to d on cals
    sub_bd(d,n,cals)    - sub n bd's to d on cals
    is_bd(d,cals)       - is d a bd on cals
    diff(d1,d2,cals,ie=IE_RULE) - how many bd's between d1 and d2 on cals and using inclusion/exclusion rules (] [) () or []
    next_bd(d1,cals)    - next business day (mod=True triggers modified following)
    prev_bd(d1,cals)    - previous business day (mod=True triggered modified previous)

    calenedar unions are handled automatically and cached, if a list of calendars is provided a new set of compiled calendars is created (doesn't impact Calendar's dict-on-disk representation

    """

    def __init__(self, home=DATA_LOCATION_FILE):
        self.home = home
        self.cals = Calendars()
        self.hash = self.cals.hash
        self.ALL = self.cals["ALL"]
        self.unions = []

        self.fwd = {}
        self.bck = {}

        self.cached_compile_all()

    def load_cache(self):
        if self.home.exists():
            with safe_open(self.home, "rb") as f:
                cached = pickle.load(f)
            return cached
        else:
            return {"hash": None}

    def save_cache(self):
        """
        cache internal state
        """
        cached = {
            "fwd": self.fwd,
            "bck": self.bck,
            "hash": self.hash,
            "unions": self.unions,
        }
        with safe_open(self.home, "wb") as f:
            pickle.dump(cached, f)

    def cached_compile_all(self):
        """
        cached compile/load of calenders, uses temp file in user's home for cache.
        """
        if self.home.exists():
            # check cache on disk
            if not self.has_mutated:
                # load cache
                cached = self.load_cache()
                self.__dict__.update(cached)
                return
            else:
                # cache invalidation
                pass
        # compile
        self.compile_all()

    def compile_all(self):
        print("[dateroll] compiling calendars")
        d = self.cals.copy()
        for k, v in d.items():
            if k == "WE":
                dates = v
                self.fwd[k], self.bck[k] = self.gen_dicts(k, v, self.ALL)

        self.save_cache()
        self.hash = self.cals.hash

    @property
    def has_mutated(self):
        cached = self.load_cache()
        return cached["hash"] != self.hash

    @property
    def recompile_if_mutated(self):
        if self.has_mutated:
            self.compile_all()

    @property
    def data_backend_present(self):
        """
        if any calendars are mutated the datemath backend is automatically removed by the Calendar class for saftey
        originally i checked "recompile_if_mutated" before calendar ops, but adds 89ms to do the unix checksome.
        This is a faster check for the existence of the data.
        """
        if not self.home.exists():
            self.recompile_if_mutated

    @staticmethod
    def gen_dicts(name, dates, all):
        """
        generates 4 dictionaries for a given calendar
        fwd[date]->#bds from inception
        bck[#bds]->date
        prev[date]->prev bus date
        next[date]->next bus date
        """
        # remove duplicates from dates
        dates = set(dates)
        cal = sorted(dates)

        fwd = {}
        bck = {}

        if len(cal) == 0:
            return fwd, bck

        last_cal = cal.pop(0)
        last_idx = 0
        # last_good = None
        for idx, dt in enumerate(sorted(all)):
            # goodbad = None

            if dt == last_cal:
                # gb = "holiday"
                # is holiday
                fwd[dt] = last_idx
                if last_idx not in bck:
                    bck[last_idx] = dt
                # bck[last_idx] = dt
                try:
                    last_cal = cal.pop(0)
                except:
                    break
            else:
                # is good bd
                # gb = "working day"
                last_idx += 1
                fwd[dt] = last_idx
                if last_idx not in bck:
                    bck[last_idx] = dt
                # bck[last_idx] = dt
                # last_good = dt
            # f = lambda x: f"{x.month}/{x.day}" if x is not None else "?"
            # if (dt.year==2024 and dt.month in (2,3)) or idx < 10 and name=='WE':
            #     print(name,f'{idx=},{f(dt)},{f(last_cal)},{last_idx=},{f(last_good)},{gb=}')

        return fwd, bck

    def add_bd(self, d, n, cals, mod=False):
        """
        add's n business days on cal to d
        careful, if n==0, B should auto backtrack, need to verify
        """
        
        if n==0 and math.copysign(1,n)==1:
            # if zero return original date as there is nothing to adjust
            # when n=-0.0 has negative sign, in this case we would like to get the roll/P of date
            return d
        cals = CalendarMath.reverse_calstring(cals)
        cal_name = self.union_key(cals)

        if mod:
            raise NotImplementedError("mod")

        A = self.fwd[cal_name]
        B = self.bck[cal_name]
        if len(A)==0:
            raise ValueError('Please provide holidays')
        from dateroll.date.date import Date

        if isinstance(d, datetime.datetime):
            d = datetime.date(d.year, d.month, d.day)
        elif isinstance(d, Date):
            d = d.date
        elif isinstance(d, datetime.date):
            pass
        else:
            raise TypeError(f"Date must be date (got {type(d).__name__})")
            
        bd_index = A[d]
        new_bd_index = bd_index + n
        new_dt = B[new_bd_index]
        return new_dt

    def sub_bd(self, d, n, cals, mod=False):
        """
        subtract (opposed of add)
        """
        if n<0:
            raise ValueError(f'n needs to be positive number')
        if math.copysign(1,n)<0 and n==0:
            # when it is -0.0 we do not want to mult by -1 to make it 0.0, because we use the - sign
            pass
        else:
            n = -1 * n
        return self.add_bd(d, n, cals, mod=mod)

    def is_bd(self, d, cals):
        """am i business day?"""
        self.recompile_if_mutated

        """ cals can come in as str or list"""
        cals = CalendarMath.reverse_calstring(cals)

        for name in cals:
            cal = self.cals[name]
            if d in cal:
                return False

        return True

    def diff(self, t1, t2, cals, ie=DEFAULT_IE):
        """
        compute business days between two dates
        """
        cals = CalendarMath.reverse_calstring(cals)
        cal_name = self.union_key(cals)
        print(f"[dateroll] IE rules not implemented...warning")

        fwd = self.fwd[cal_name]
        n = fwd[t2] - fwd[t1]
        return n

    def next_bd(self, d, cals, mod=False):
        """
        the next business date from d on calendars cals
        """
        # if mod:
        #     raise NotImplementedError("next_bd")
        # warnings.warn("next bd not implemented yet")
        new_d = self.add_bd(d,1,cals)
        if mod:
            if new_d.month!=d.month:
                # when month is different new d should be within the previous month
                if self.is_bd(d,cals):
                    new_d =d
                else:
                    # if it is holiday, we should prev bd
                    new_d = self.sub_bd(d,-0.0,cals)
        return new_d

    def prev_bd(self, d, cals, mod=False):
        """
        the previous business date from d on calendars cals
        """

        # if mod:
        #     raise NotImplementedError("prev_bd")
        # warnings.warn("prev bd not implemented yet")
        if self.is_bd(d,cals):
            new_d = self.sub_bd(d,1,cals)
        else:
            # when holiday, to get prev_db we should subtract 0 from the date because of fwd,bck property
            new_d = self.sub_bd(d,-0.0,cals)
        if mod:
            if new_d.month!=d.month:
                # when month differs, new_d month should be within the next month
                if self.is_bd(d,cals):
                    new_d = d
                else:
                    new_d = self.add_bd(d,1,cals)
        return new_d


    @staticmethod
    def reverse_calstring(cals):
        """
        cals can be:
            'WE'
            ['WE']
            'WEuNY'
            ['WE','NY']

        always return list of individuals (decompose unions)
        """
        if cals is None:
            cals = [WEEKEND_CALENDAR]  # define at top of file..future user might want WKD instad of WE

        if isinstance(cals, str):
            if "u" in cals:
                cals = tuple(sorted(cals.split("u")))
            else:
                cals = [cals]
        return cals

    def union_key(self, cals):
        """
        takes a cals as either  str of 1 cal or a list of str cals and return a sorted tuple, if empty list assume weekends
        
        """
        # cals always come as a tuple,list,set, no need to raise error here
        
        try:
            cal_union_key = 'u'.join(cals)
        except:
            raise TypeError(f"Calendar name must be string")
        if cal_union_key not in self.unions:
            # union dates wasnt' cached, call _generate_union
            self._generate_union(cal_union_key)
        
        return cal_union_key
        

    def _generate_union(self, cal_union_key):
        """
        creates a union from sorted tuple of cals
        """
        unioned_dates = set()
        cals = CalendarMath.reverse_calstring(cal_union_key)
        for cal in cals:
            # saftey checks
            if cal not in self.cals:
                raise KeyError(f"There is no calendar {cal}")
            
            # the union operation
            unioned_dates |= set(self.cals[cal])

        # self.unions.append(cal_union_key) <## you can delete self.unions, are references used anywhere? user can check fwd.keys()
        # compile into large dicts
        
        print(f"[dateroll] compiling new union [{cal_union_key}]")
        dict_tuple = self.gen_dicts(cal_union_key, unioned_dates, self.ALL)
        self.fwd[cal_union_key], self.bck[cal_union_key] = dict_tuple

        # save cache
        self.save_cache()

    def _purge_all(self):
        self.__init__()

    def __repr__(self):
        """
        Show names of cals and unions
        """
        return f'{self.__class__.__name__}(home="{self.home}")\nCals: {self.cals.keys()}\nUnions: {self.unions}'


calmath = CalendarMath()

if __name__ == "__main__": # pragma: no cover
    calmath = CalendarMath()

    import datetime
    import time

    from dateutil.relativedelta import relativedelta as rd

    t = datetime.date(2024, 2, 25)

    a = time.time()

    print(t)
    # calmath.add_bd(t,1,cals=['WE','NY'])

    t2 = calmath.add_bd(t, 1, cals=["WE"])
    print(t2)

    t2 = calmath.add_bd(t, 100, cals=["WE"])
    print(t2)
    print(calmath.diff(t, t2, cals=["WE"]))
    t2 = t + rd(days=31)
    print(calmath.diff(t, t2, cals=["WE"]))

    b = time.time()
    print((b - a) * 1000, "ms")

    import code

    code.interact(local=locals())
