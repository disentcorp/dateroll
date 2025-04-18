import datetime
import math
import os
import pathlib
import pickle

import dateroll.date.date as dateModule
from dateroll.calendars.calendars import Calendars

from dateroll.settings import get_comp_cals_path

WEEKEND_CALENDAR = "WE"
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

    def __init__(self):
        self.home = get_comp_cals_path()
        self.cals = Calendars()
        self.cal_names = list(self.cals.keys())
        self.hash = self.cals.hash
        self.ALL = self.cals["ALL"]

        self.fwd = {}
        self.bck = {}
        self.ibd = {}
        self.cached_compile_all()

    def load_cache(self):
        """
        self.home always exsist because load_cache called if it exists
        """
        if self.home.exists():
            with open(self.home, "rb") as f:
                try:
                    cached = pickle.load(f)
                    return cached
                except Exception as e:
                    import traceback

                    traceback.print_exc()
                    print(f"[dateroll] Cannot load cache for calmath unions, clearing.")
                    os.remove(self.home)
        else:
            self.save_cache()

    def save_cache(self):
        """
        cache internal state
        """
        cached = {
            "fwd": self.fwd,
            "bck": self.bck,
            "ibd": self.ibd,
            "hash": self.hash,
        }
        with open(self.home, "wb") as f:
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
                if cached is not None:
                    self.__dict__.update(cached)
                    return

        # compile
        self.compile_all()

    def compile_all(self):
        d = self.cals.copy()
        for k, v in d.items():
            if k == "WE":
                dates = v
                self.fwd[k], self.bck[k], self.ibd[k] = self.gen_dicts(k, v, self.ALL)

        self.save_cache()
        self.cal_names = list(d.keys())
        self.hash = self.cals.hash

    @property
    def has_mutated(self):
        """
        only time "mutation" occurs is if an underlying calendar has changed
        all __setitem__ to a calendar will automatically trigger removal of the
        calendarmath cache file, thus it's existence confirms cache validity
        """
        cache_is_valid = not self.home.exists()
        return cache_is_valid

    @property
    def cal_list(self):
        if not self.has_mutated:
            return self.cal_names
        else:
            self.compile_all()
            return self.cal_names

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
        ibd = {}
        if len(cal) == 0:
            return fwd, bck, ibd

        last_cal = cal.pop(0)
        last_idx = 0
        for idx, dt in enumerate(sorted(all)):

            if dt == last_cal:
                # it is holiday
                ibd[dt] = False
                fwd[dt] = last_idx
                try:
                    last_cal = cal.pop(0)
                except:
                    break
            else:
                # not holiday
                ibd[dt] = True
                last_idx += 1
                fwd[dt] = last_idx
                if last_idx not in bck:
                    bck[last_idx] = dt

        return fwd, bck, ibd

    def add_bd(self, d, n, cals):
        """
        add's n business days on cal to d
        careful, if n==0, B should auto backtrack, need to verify
        """

        # when not bd, we need to handle n; positive direction n=0-->1 and negative direction n=-1--->0
        # because of the property of fwd, bck dictionaries
        if isinstance(d, datetime.datetime):
            d = datetime.date(d.year, d.month, d.day)
        elif isinstance(d, dateModule.Date):
            d = d.date
        elif isinstance(d, datetime.date):
            pass
        else:
            raise TypeError(f"Date must be date (got {type(d).__name__})")
        if not self.is_bd(d, cals):
            # make sure direction is positive
            if n == 0 and math.copysign(1, n) == 1:
                n = 1
            # when direction is negative
            elif n < 0:
                n += 1

        _cals = CalendarMath.reverse_calstring(cals)
        cal_name = self.union_key(_cals)

        A = self.fwd[cal_name]
        B = self.bck[cal_name]
        if len(A) == 0:
            raise ValueError("Please provide holidays")
        from dateroll.date.date import Date

        bd_index = A[d]
        new_bd_index = bd_index + n
        new_dt = B[new_bd_index]

        return new_dt

    def sub_bd(self, d, n, cals):
        """
        subtract (opposed of add)
        """
        if n < 0:
            raise ValueError(f"n needs to be positive number")

        n = -1 * float(n)
        return self.add_bd(d, n, cals)

    def is_bd(self, d, cals):
        """am i business day?"""
        self.recompile_if_mutated

        """ cals can come in as str or list"""

        _cals = CalendarMath.reverse_calstring(cals)
        cal_name = self.union_key(_cals)

        BD = self.ibd[cal_name]
        if len(BD) == 0:
            return False

        is_bd = self.ibd[cal_name][d]
        return is_bd

    def diff(self, t1, t2, cals, ie=DEFAULT_IE):
        """
        compute business days between two dates
        """

        cals = CalendarMath.reverse_calstring(cals)
        cal_name = self.union_key(cals)

        if t1 == t2:
            return 0

        fwd = self.fwd[cal_name]
        mult = 1 if t1 < t2 else -1
        a, b = (t1, t2) if t1 < t2 else (t2, t1)
        n = fwd[t2] - fwd[t1] + 1 * mult
        if ie[0] == "[" and not a.is_bd(cals=cals):
            # because of the fwd property e.g friday:1,sat:1,sun:1,mon(hol):1,tue:2 we subtract 1 more on the left side
            n = n - 1 * mult
        if ie[0] == "(":
            n = n - 1 * mult

        if ie[1] == ")" and b.is_bd(cals=cals):
            n = n - 1 * mult

        return n

    def next_bd(self, d, cals):
        """
        the next business date from d on calendars cals
        """
        new_d = self.add_bd(d, 1, cals)
        return new_d

    def prev_bd(self, d, cals):
        """
        the previous business date from d on calendars cals
        """
        new_d = self.sub_bd(d, 1, cals)
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
            cals = [
                WEEKEND_CALENDAR
            ]  # define at top of file..future user might want WKD instad of WE

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
        cal_union_key = "u".join(cals)

        if cal_union_key not in self.fwd:
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

        # compile into large dict
        dict_tuple = self.gen_dicts(cal_union_key, unioned_dates, self.ALL)
        self.fwd[cal_union_key], self.bck[cal_union_key], self.ibd[cal_union_key] = (
            dict_tuple
        )
        # save cache
        self.save_cache()

    def _purge_all(self):
        self.__init__()

    def __repr__(self):
        """
        Show names of cals and unions
        """
        return f'{self.__class__.__name__}(home="{self.home}")\nCals: {self.cals.keys()}\nUnions: {list(self.fwd.keys())}'


calmath = CalendarMath()

if __name__ == "__main__":  # pragma:no cover
    from dateroll import ddh
    from dateroll.settings import settings
    import code
    # code.interact(local=dict(globals(),**locals()))
