import datetime
import fcntl
import glob
import hashlib
import os
import pathlib
import pickle
import time
import code
from random import choice

from dateroll.utils import safe_open

ROOT_DIR = pathlib.Path(__file__).parents[2]
PARENT_LOCATION = pathlib.Path.home() / ".dateroll/"
PARENT_LOCATION.mkdir(exist_ok=True)
MODULE_LOCATION = PARENT_LOCATION / "calendars/"
MODULE_LOCATION.mkdir(exist_ok=True)
DATA_LOCATION_FILE = MODULE_LOCATION / "holiday_lists"
SAMPLE_DATA_PATH = ROOT_DIR / "dateroll" / "sampledata" / "*.csv"

SLEEP_TIMES = [25 / 1000, 50 / 1000, 100 / 1000, 300 / 1000]


INCEPTION = datetime.date(1824,2,29)


def load_sample_data():
    files = glob.glob(str(SAMPLE_DATA_PATH))
    data = {}
    for file in files:
        name = pathlib.Path(file).stem
        with safe_open(file) as f:
            ls = f.readlines()
            ld = []
            for i in ls:
                dt = datetime.date(int(i[0:4]), int(i[5:7]), int(i[8:10]))
                if dt > INCEPTION:
                    ld.append(dt)
            data[name] = ld
    return data


class Drawer:
    def __init__(self, cals):
        
        self.path = pathlib.Path(cals.home)
        self.cals = cals

    def __enter__(self):
        if self.cals.hash == self.cals.db_hash:
            return self.cals.db

        if self.path.exists():
            with safe_open(self.path, "rb") as f:
                self.data = pickle.load(f)
                self.cals.db_hash = self.cals.hash
                self.cals.db = self.data
        else:
            print(f"[dateroll] no saved calendars, loading sample data")
            data = load_sample_data()
            self.cals.db = data
            with safe_open(self.path, "wb") as f:
                pickle.dump(self.cals.db, f)

        return self.cals.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self.cals.write:
                with safe_open(self.path, "wb") as f:
                    pickle.dump(self.cals.db, f)
                self.cals.write = False
        else:

            return True


class Calendars(dict):
    """
    dict-like dictionary of calendars
    """

    def __init__(self, home=DATA_LOCATION_FILE):
        self.home = str(home)  # on disk location
        self.db_hash = None  # initial hash
        self.db = {}  # cache
        self.write = False  # sentinel to invalidate cache

        with Drawer(self) as db:
            pass


    def keys(self):
        '''
            return date keys
        '''
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
            with safe_open(filename, "rb") as f:
                result = hashlib.md5(
                    f.read(),
                ).hexdigest()

        return result

    def __setitem__(self, k, v):
        from dateroll.calendars.calendarmath import \
            DATA_LOCATION_FILE as calendar_math_file

        if calendar_math_file.exists():
            os.remove(calendar_math_file)

        # key must be 2-3 letter string in uppercase
        if not isinstance(k, str):
            raise Exception(f"Cal name must be string (got {type(k).__name__})")
        if len(k) < 2 or len(k) > 3:
            raise Exception(f"Cal name be 2 or 3 charts (got {len(k)})")
        if not k.isupper():
            raise Exception(f"Cal name must be all uppercase")
        # value must be a list of dates
        if not isinstance(v, (set, list, tuple)):
            raise Exception(
                f"Cal values must be a set/list/tuple (got {type(v).__name__})"
            )

        processed = []
        for i in v:
            
            if isinstance(i, datetime.datetime):
                dt = datetime.date(i.year, i.month, i.day)
            elif isinstance(i, datetime.date):
                dt = i
            else:
                raise Exception(
                    f"All cal dates must be of dateroll.Date or datetime.date{{time}} (got {type(i).__name__})"
                )
            if dt >= INCEPTION:
                
                processed.append(dt) 

        self.write = True
        if k in self.db.keys():
            raise Exception(
                f"{k} exists already, delete first.if you want to replace."
            )
        with Drawer(self) as db:
            s = list(sorted(list(set(processed))))
            db[k] = s

    def __getitem__(self, k):
        return self.get(k)

    def __getattr__(self, k):
        """
        allows for dot notation
        """
        if k in ("hash", "home"):
            result = super().__getattribute__(k)
        else:
            result = self.get(k)
        return result

    def __contains__(self, k):
        with Drawer(self) as db:
            return str(k) in db

    def __delitem__(self, k):
        self.write = True
        with Drawer(self) as db:
            del db[k]

    def get(self, k):
        with Drawer(self) as db:
            result = db[k]
        return result

    def clear(self):
        self.write = True
        with Drawer(self) as db:
            db.clear()

    def __repr__(self):
        self.info
        return f'{self.__class__.__name__}(home="{self.home}")'

    def copy(self):
        with Drawer(self) as db:
            return db.copy()

    def _purge_all(self):
        self.__init__()

    @property
    def info(self):
        pattern = lambda a, b, c, d: f"{a:6}|{b:>8}|{c:12}|{d:12}"
        with Drawer(self) as db:
            stats = []
            print(pattern("name", "#dates", "min date", "max date"))
            print(pattern("-" * 6, "-" * 8, "-" * 12, "-" * 12))
            for i in db.keys():
                
                l = db.get(i)
                if len(l) > 0:
                    n = len(l)
                    mn = min(l)
                    mx = max(l)
                else:
                    n, mn, mx = 0, None, None
                print(pattern(str(i), str(n), str(mn), str(mx)))


if __name__ == '__main__': # pragma: no cover
    ...
    
