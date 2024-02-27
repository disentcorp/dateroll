import datetime
import pathlib
import pickle

from dateroll.calendars.calendars import Calendars

PARENT_LOCATION = pathlib.Path.home() / ".dateroll/"
PARENT_LOCATION.mkdir(exist_ok=True)
MODULE_LOCATION = PARENT_LOCATION / "calendars/"
MODULE_LOCATION.mkdir(exist_ok=True)
DATA_LOCATION_FILE = MODULE_LOCATION / "compiled_cals.db"


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
        self.prev = {}
        self.next = {}

        self.cached_compile_all()

    def load_cache(self):
        if self.home.exists():
            file = open(self.home, "rb")
            with file:
                cached = pickle.load(file)
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
            "prev": self.prev,
            "next": self.next,
            "hash": self.hash,
            "unions": self.unions,
        }
        self.__dict__.update(cached)
        file = open(self.home, "wb")
        with file:
            pickle.dump(cached, file)

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
                print(
                    "[dateroll] calendar mutation detected, triggering re-compliation"
                )

        # compile
        self.compile_all()

    def compile_all(self):
        print("[dateroll] compiling calendars")
        cals = self.cals
        keys = cals.keys()
        for name in keys:
            dates = self.cals[name]
            self.gen_dicts(name, dates)

        self.save_cache()

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
            self.recompile_if_mutated()

    def gen_dicts(self, name, dates):
        """
        generates 4 dictionaries for a given calendar
        fwd[date]->#bds from inception
        bck[#bds]->date
        prev[date]->prev bus date
        next[date]->next bus date
        """
        cal = sorted(dates)
        all = sorted(self.ALL)

        fwd = {}
        bck = {}
        prev = {}
        next = {}

        if len(cal) == 0:
            return

        last_cal = cal[0]
        last_idx = 0
        last_good = None
        for idx, dt in enumerate(all):
            if dt == last_cal:
                # is holiday
                fwd[dt] = last_idx
                bck[last_idx] = dt
                try:
                    last_cal = cal.pop(0)
                except:
                    break
            else:
                # is good bd
                last_idx += 1
                fwd[dt] = last_idx
                bck[last_idx] = dt
                prev[dt] = last_good
                last_good = dt

        self.fwd[name] = fwd
        self.bck[name] = bck
        self.prev[name] = prev
        self.next[name] = {v: k for k, v in prev.items()}

    def add_bd(self, d, n, cals, mod=False):
        """
        add's n business days on cal to d
        careful, if n==0, B should auto backtrack, need to verify
        """
        cal_name = self.union_swap(cals)

        if mod:
            raise NotImplementedError("mod")

        A = self.fwd[cal_name]
        B = self.bck[cal_name]

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

    def sub_bd(self, d, n, cal, mod=False):
        """
        subtract (opposed of add)
        """
        return self.add_bd(self, d, -1 * n, cal, mod=mod)

    def is_bd(self, d, cals):
        """am i business day?"""
        self.recompile_if_mutated
        cal_name = self.union_swap(cals)
        CAL = self.fwd
        return d in CAL

    def diff(self, t1, t2, cals, ie=DEFAULT_IE):
        """
        compute business days between two dates
        """
        cal_name = self.union_swap(cals)
        print(f"[dateroll] IE rules not implemented...warning")

        fwd = self.fwd[cal_name]
        n = fwd[t2] - fwd[t1]
        return n

    def next_bd(self, d, cals, mod=False):
        """
        the next business date from d on calendars cals
        """
        if mod:
            raise NotImplementedError("mod")

        cal_name = self.union_swap(cals)
        return self.prev[cal_name][d]

    def prev_bd(self, d, cals, mod=False):
        """
        the previous business date from d on calendars cals
        """

        if mod:
            raise NotImplementedError("mod")

        cal_name = self.union_swap(cals)
        return self.next[cal_name][d]

    def union_swap(self, cals):
        """
        check calendar list or str is valid
        and if not copmiled (in self.unions) call self.union to compile the union
        """
        if isinstance(cals, str):
            return cals
        elif isinstance(cals, (tuple, list, set)):
            union_name = "_".join(cals)
            if union_name in self.fwd:
                return union_name
            else:
                self.union(cals)
                return union_name
        else:
            raise TypeError("Calendars must be a valid calendar name or list of names")

    def union(self, cals):
        """
        validate cals passed is in correct format
        union all the cals into a superset, then call gen_dicts and save_cache (no need to tell self.cals/Calendars)
        """
        if isinstance(cals, str):
            return cals
        elif isinstance(cals, (tuple, list, set)):
            union = set()
            if len(cals) == 1:
                if isinstance(cals[0], str):
                    return cals[0]
            for cal in cals:
                if not isinstance(cal, str):
                    raise TypeError(f"Calendar name must be string")
                if cal not in self.cals:
                    raise KeyError(f"There is no calendar {cal}")
                union |= set(self.cals[cal])
            union_name = "_".join(cals)
            self.unions.append(cals)
            dates = list(union)
            print(f"[dateroll] compiling new union [{union_name}]")
            self.gen_dicts(union_name, dates)
            self.save_cache()
        else:
            raise TypeError("Union must be tuple or list of cal names")


cm = CalendarMath()

if __name__ == "__main__":
    cm = CalendarMath()

    import datetime
    import time

    from dateutil.relativedelta import relativedelta as rd

    t = datetime.date(2024, 2, 25)

    a = time.time()

    print(t)
    # cm.add_bd(t,1,cals=['WE','NY'])

    t2 = cm.add_bd(t, 1, cals=["WE"])
    print(t2)

    t2 = cm.add_bd(t, 100, cals=["WE"])
    print(t2)
    print(cm.diff(t, t2, cals=["WE"]))
    t2 = t + rd(days=31)
    print(cm.diff(t, t2, cals=["WE"]))

    b = time.time()
    print((b - a) * 1000, "ms")

    import code

    code.interact(local=locals())
