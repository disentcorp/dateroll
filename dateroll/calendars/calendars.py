import datetime
import fcntl
import glob
import hashlib
import os
import pathlib
import pickle
from collections import OrderedDict

from dateroll.calendars import calendarmath as calendarmathModule
from dateroll.date import date as dateModule
from dateroll.utils import date_slice, convention_map
from dateroll import settings
from dateroll.tblfmt import pretty_table

ROOT_DIR = pathlib.Path(__file__).parents[2]
PARENT_LOCATION = pathlib.Path.home() / ".dateroll/"
PARENT_LOCATION.mkdir(exist_ok=True)
MODULE_LOCATION = PARENT_LOCATION / "calendars/"
MODULE_LOCATION.mkdir(exist_ok=True)
DATA_LOCATION_FILE = MODULE_LOCATION / "holiday_lists"
SAMPLE_DATA_PATH = ROOT_DIR / "dateroll" / "sampledata" / "*.csv"

INCEPTION = datetime.date(1824, 2, 29)


SetLike = (list, tuple, set)


def date_check(i):
    if isinstance(i, datetime.datetime):
        dt = datetime.date(i.year, i.month, i.day)
    elif isinstance(i, datetime.date):
        dt = i
    else:
        raise TypeError(
            f"All cal dates must be of dateroll.Date or datetime.date{{time}} (got {type(i).__name__})"
        )
    if dt < INCEPTION:
        raise ValueError(
            "Holiday before 29-Feb-1824 not supported, ask if you need it."
        )

    return dt


def load_sample_data():
    files = glob.glob(str(SAMPLE_DATA_PATH))
    data = {}
    for file in files:
        name = pathlib.Path(file).stem
        with open(file) as f:
            ls = f.readlines()
            l = []
            for i in ls:
                dt = datetime.date(int(i[0:4]), int(i[5:7]), int(i[8:10]))
                if dt >= INCEPTION:
                    l.append(dt)

            ds = DateSet(l,name=name)
            data[name] = ds
    return data


class Drawer:
    def __init__(self, cals):

        self.path = pathlib.Path(cals.home)
        self.cals = cals

    def __enter__(self):

        if self.cals.hash == self.cals.db_hash:
            return self.cals.db

        if self.path.exists():
            try:
                with open(self.path, "rb") as f:
                    self.data = pickle.load(f)
                    self.cals.db_hash = self.cals.hash
                    self.cals.db = self.data

                    return self.cals.db
            except Exception as e:
                import traceback

                traceback.print_exc()
                msg = "Cache is corrupted"
        else:
            msg = "No cache found"

        print(f"[dateroll] Loading sample calendars ({msg})")
        data = load_sample_data()

        self.cals.db = data
        with open(self.path, "wb") as f:
            pickle.dump(self.cals.db, f)
            print("[dateroll] Writing cache (calendars)")
            self.cals.write = False

        return self.cals.db

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_val is not None:
            raise exc_val
        else:
            if self.cals.write:
                with open(self.path, "wb") as f:
                    pickle.dump(self.cals.db, f)
                    print("[dateroll] Writing cache (calendars)")
                self.cals.write = False


class DateSet:
    def __init__(self, content, name=None):
        self.name = name
        if not isinstance(content, SetLike):
            raise TypeError("DateSet content must be set-like (castable)")

        # ordered dict constructure requires dict not set
        d = {date_check(i): True for i in content if i is not None}
        od = OrderedDict(d)
        self._data = od

    def add(self, item):
        dt = date_check(item)
        self._data[dt] = True
        if self.name is not None:
            tothing = f' to {self.name}'
        else:
            tothing = ''
        print(f'[dateroll] {item} added{tothing}.')

    def __contains__(self, item):
        if isinstance(item, dateModule.Date):
            item = item.date
        if isinstance(item, datetime.datetime):
            item = datetime.date(item.year, item.month, item.day)
        return item in self._data

    def extend(self, items):
        if not isinstance(items, SetLike):
            raise TypeError("Must be cast-able into set")
        extension = {date_check(i): None for i in items if i is not None}
        self._data.update(extension)

    def __getitem__(self,k):
        if isinstance(k,slice):
            return date_slice(k,self._data)
        else:
            raise TypeError('Indexation on DateSet only accepts date string slicing')

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"{type(self).__name__}({list(self._data.keys())})"


CALENDARS_ATTRIBUTES = ("write", "home", "db_hash", "db")


class Calendars(dict):
    """
    dict-like dictionary of calendars
    """

    def __init__(self, home=DATA_LOCATION_FILE):
        self.home = str(home)  # on disk location
        self.db_hash = None  # initial hash
        self.db = {}  # cache
        self.write = False  # sentinel to invalidate cache

    def keys(self):
        """
        return date keys
        """
        with Drawer(self) as db:
            return list(db.keys())

    @property
    def hash(self):
        """
        generate hash
        """
        result = -1
        filenames = glob.glob(f"{self.home}")
        if len(filenames) == 1:
            filename = filenames[0]
            with open(filename, "rb") as f:
                result = hashlib.md5(
                    f.read(),
                ).hexdigest()

        return result

    def __setitem__(self, k, v):

        # invalidate calendar union caches, very important
        if calendarmathModule.DATA_LOCATION_FILE.exists():
            os.remove(calendarmathModule.DATA_LOCATION_FILE)

        # key must be 2-3 letter string in uppercase
        if not isinstance(k, str):
            raise Exception(f"Cal name must be string (got {type(k).__name__})")
        if len(k) < 2 or len(k) > 3:
            raise Exception(f"Cal name be 2 or 3 charts (got {len(k)})")
        if not k.isupper():
            raise Exception(f"Cal name must be all uppercase")

        if k in self.db.keys():
            raise Exception(f"{k} exists already, delete first.if you want to replace.")

        self.write = True
        with Drawer(self) as db:
            # value must be a set-like list of dates
            verified = DateSet(v,name=k)
            db[k] = verified
        
        print(f'[dateroll] {k} now has {len(verified)} holidays.')

    def __getitem__(self, k):
        return self.get(k)


    def __getattr__(self, k):
        """
        allows for dot notation
        """
        if k in CALENDARS_ATTRIBUTES:
            return super().__getattribute__(k)
        else:
            try:
                return self.get(k)
            except KeyError:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        if k in CALENDARS_ATTRIBUTES:
            return super().__setattr__(k, v)

        self.__setitem__(k, v)

    def __contains__(self, k):
        with Drawer(self) as db:
            return str(k) in db

    def __delitem__(self, k):
        self.write = True
        with Drawer(self) as db:
            del db[k]

    def __delattr__(self, k):
        """
        if user deletes an attribute it's either
        a - a calendar
        b - an actual attribute, probably by mistake but we should still call super()
        """
        try:
            # case a
            self.__delitem__(k)
        except:
            # case b
            super().__delattr__(k)

    def get(self, k):

        with Drawer(self) as db:
            result = db.get(k)

        if result is not None:
            return result
        else:
            raise KeyError(k)

    def clear(self):
        self.write = True
        with Drawer(self) as db:
            db.clear()
            self.db.clear()

    @property
    def _calsdata(self):
        data = []
        conv = convention_map[settings.settings.convention]
        with Drawer(self) as db:
            for i in sorted(db.keys()):
                l = db.get(i)
                years = {}
                for j in l:
                    if j.year > 1950 and j.year < 2050:
                        if j.year in years:
                            years[j.year]+=1
                        else:
                            years[j.year]=1
            
                num_this_year = years.get(datetime.date.today().year,0)
                if len(l) > 0:
                    n = len(l)
                    mn = min(l).strftime(conv)
                    mx = max(l).strftime(conv)
                else:
                    n, mn, mx = 0, "", ""
                data.append({'name':i,'non-working days':n,'oldest':mn,'newest':mx,'# this year':num_this_year})
        return data
    
    def __str__(self):
        data = self._calsdata
        s = pretty_table(data)
        return s

    def __repr__(self):
        return self.__str__()

    def copy(self):
        with Drawer(self) as db:
            return db.copy()

    def _purge_all(self):
        self.__init__()

    @property
    def info(self):
        print(self.__str__)


if __name__ == "__main__":  # pragma: no cover
    
    
    ...
    

    
