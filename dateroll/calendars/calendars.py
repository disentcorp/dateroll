import pathlib
import shelve
import datetime
import pandas as pd
import hashlib
import os

PARENT_LOCATION = pathlib.Path.home() / '.dateroll/'
PARENT_LOCATION.mkdir(exist_ok=True)
MODULE_LOCATION = PARENT_LOCATION / 'calendars/'
MODULE_LOCATION.mkdir(exist_ok=True)
DATA_LOCATION_FILE = MODULE_LOCATION / 'holiday_lists'

class Calendars:
    def __init__(self,home=DATA_LOCATION_FILE):
        self.home = home
        self.db = lambda :shelve.open(self.home)

        with self.db() as db:
            if 'WE' not in db and 'ALL' not in db:
                self.load_all_and_we()
    
    def keys(self):
        with self.db() as db:
            return list(db.keys())
        
    @property
    def hash(self):
        with open(self.home.with_suffix('.db'),'rb') as f:
            return hashlib.md5(f.read(),).hexdigest()
    
    def __setitem__(self,k,v):
        from dateroll.calendars.calendarmath import DATA_LOCATION_FILE as calendar_math_file 
        if calendar_math_file.exists():
            os.remove(calendar_math_file)

        # key must be 2-3 letter string in uppercase
        if not isinstance(k,str):
            raise Exception(f'Cal name must be string (got {type(k).__name__})')
        if len(k)<2 or len(k) >3:
            raise Exception(f'Cal name be 2 or 3 charts (got {len(k)})')
        if not k.isupper():
            raise Exception(f'Cal name must be all uppercase')
        #value must be a list of dates
        if not isinstance(v,(set,list,tuple)):
            raise Exception(f'Cal values must be a set/list/tuple (got {type(v).__name__})')
        
        from dateroll.date.date import Date
        processed = []
        for i in v:
            if isinstance(i,datetime.datetime):
                dt = datetime.date(i.year,i.month,i.day)
                processed.append(dt)
            elif isinstance(i,datetime.date):
                dt = i
                processed.append(dt)
            elif isinstance(i,Date):
                dt = dt.date
                processed.append(dt)
            else:
                raise Exception(f'All cal dates must be of dateroll.Date or datetime.date{{time}} (got {type(i).__name__})')

        with self.db() as db:
            if k in db.keys():
                raise Exception(f'{k} exists already, delete first.if you want to replace.')
            s = list(sorted(list(set(processed))))
            db[k]=s

    def __getitem__(self,k):
        return self.get(k)
    
    def __getattr__(self,k):
        return self.get(k)
       
    def __contains__(self,k):
        with self.db() as db:
            return str(k) in db

    def __delitem__(self,k):
        with self.db() as db:
            del db[k]

    def get(self,k):
        with self.db() as db:
            return db[k]
        
    def clear(self):
        with self.db() as db:
            db.clear()
    
    def __repr__(self):
        self.info
        return f'{self.__class__.__name__}(home="{self.home}.db")'
    
    def load_all_and_we(self):
        from dateroll.calendars.sampledata import generate_ALL_and_WE
        ALL, WE = generate_ALL_and_WE()
        self['ALL'] = ALL
        self['WE'] = WE

    def load_sample_data(self):
        from dateroll.calendars.sampledata import load_sample_data as lsd
        lsd(self)
        self.info

    @property
    def info(self):
        with self.db() as db:
            stats = []
            for i in db.keys():
                l = db.get(i)
                n = len(l)
                mx = max(l)
                mn = min(l)
                stat = {'name':i,'dates':n,'min':mn,'max':mx}
                stats.append(stat)
            if len(stats)>0:
                print(pd.DataFrame(stats).to_string(index=False))

if __name__ == '__main__':
    cals = Calendars()
    print(cals.hash)
    cals.load_sample_data()

    import code;code.interact(local=locals())

