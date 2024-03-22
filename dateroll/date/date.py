
import datetime
import dateutil.relativedelta
import dateroll.parser.parsers as parsersModule
from dateroll.settings import settings
from dateroll.calendars.calendarmath import calmath
from dateroll.duration.duration import Duration
from dateroll import pretty

DateLike = (datetime.datetime, datetime.date)


class Date(datetime.date):
    '''
    A Date, inherits from datetime.date, represents a specific day (no sub-units of day)
    '''

    @staticmethod
    def from_string(o):
        """
        """
        if not isinstance(o,str):
            raise TypeError(f'from_string requires string, cannot use {type(o).__name__}')
        
        dt = parsersModule.parseDateString(o)
        return Date.from_datetime(dt)


    @staticmethod
    def from_datetime(o):
        """
        Create a Date instance from a datetime.datetime (drops time information), or datetime.date
        """
        if isinstance(o,Date):
            return o
        elif isinstance(o, DateLike):
            y, m, d = o.year, o.month, o.day
            return Date(y, m, d)
        else:
            raise TypeError(f'from_datetime requires datetime, cannot use {type(o).__name__}')
        
    @staticmethod
    def from_unix(o):
        if not isinstance(o,(int,float)):
            raise TypeError('Must be int/float')        
        dt = datetime.date.fromtimestamp(o)
        return Date.from_datetime(dt)

    @staticmethod
    def from_xls(o):
        '''
        excel integer part is days since 12/30/1899, fraction is sub-day
        '''
        if not isinstance(o,(int,float)):
            if isinstance(o,str):
                try:
                    o = int(o)
                except:
                    raise TypeError('Must be int/float or int-like string')
            else:
                raise TypeError('Must be int/float')
        
        base_date = datetime.datetime(1899, 12, 30)
        days = int(o)
        fraction = o - days
        seconds_in_day = int(fraction * 24 * 3600)
        dt = base_date + datetime.timedelta(days=days, seconds=seconds_in_day)
        return Date.from_datetime(dt)


    @staticmethod
    def from_timestamp(o):
        """
        Create a Date instance from a unix timestamp
        """  
        if isinstance(o,(int,float)):
            dt = datetime.date.fromtimestamp(o)
            return Date.from_datetime(dt)
        else:
            raise TypeError(f'from_datetime requires int/float, cannot use {type(o).__name__}')           

    @staticmethod
    def today():
        return Date.from_datetime(datetime.date.today())

    @property
    def datetime(self):
        return datetime.datetime(self.year, self.month, self.day)

    @property
    def date(self):
        return datetime.date(self.year, self.month, self.day)

    def is_bd(self, cals=None):
        """
        am i a business day?
        """
        return calmath.is_bd(self.date, cals=cals)

    @property
    def dotw(self):
        """
        which day of the week am i
        """
        dt_mapping = {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun",
        }
        day_of_week = dt_mapping[self.weekday()]
        return day_of_week

    @property
    def woty(self):
        """
        week of the year, iso 8601
        """
        return self.isocalendar()[1]

    @property
    def xls(self):
        offset = 693594
        n = self.toordinal()
        rs = n - offset
        return rs

    @property
    def unix(self):
        return self.datetime.timestamp()



    @property
    def iso(self):
        return self.isoformat().split("T")[0]

    def __add__(self, o):
        """
        add, do str conversion first, then handle suborinate cases
        """
        # convert string if first
        if isinstance(o, str):
            from dateroll.ddh.ddh import ddh
            o = ddh(o)

        # apply rules by type
        if isinstance(o, DateLike):
            # date + date
            raise TypeError("unsupported operand type(s) for +: 'Date' and 'Date'")
        
        elif isinstance(o, Duration):
            # date + duration
            # goes to __radd__ of Duration
            return Date.from_datetime(o.__radd__(self))
        elif isinstance(o, int):
            # date + int, int -> duration, -> date + duration -> __radd__ duration
            # goes to __radd__ of Duration
            return Duration(days=o).__radd__(self)
        elif isinstance(o, datetime.timedelta):
            return Date.from_datetime(self.date + o)
        elif isinstance(o, dateutil.relativedelta.relativedelta):
            return Date.from_datetime(self.date + o)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +: 'Date' and {type(o).__name__}"
            )

    def __pos__(self):
        return self

    def __sub__(self, o):
        
        """
        sub
        """
        # convert string if first
        if isinstance(o, str):
            from dateroll.ddh.ddh import ddh

            o = ddh(o)

        # apply rules by type
        
        if isinstance(o, DateLike):
            # date - date
            # convert all datetimes to datetime.date for sub to be timedelta, then create Duration from timedelta
            if isinstance(o,Date):
                dt = o.date
            elif isinstance(o,datetime.datetime):
                # truncates time!
                dt = datetime.date(o.year,o.month,o.day) 
            else:
                if isinstance(o, datetime.date):
                    dt = o

            relative_delta = dateutil.relativedelta.relativedelta(self.date,dt)
            return Duration.from_relativedelta(relative_delta,_anchor_start=dt,_anchor_end=self.date)
        
        elif isinstance(o, Duration) or 'Duration' in o.__class__.__name__:
            # date + duration
            # goes to __radd__ of Duration
            x = o.__rsub__(self)
            return x
        elif isinstance(o, int):
            # date + int, int -> duration, -> date + duration -> __radd__ duration
            # goes to __rsub__ of Duration
            return Duration(days=o).__rsub__(self)
        elif isinstance(o, datetime.timedelta):
            return Date.from_datetime(self.date - o)
        elif isinstance(o, dateutil.relativedelta.relativedelta):
            return Date.from_datetime(self.date - o)
        else:
            raise TypeError(
                f"unsupported operand type(s) for : 'Date' and {type(o).__name__}"
            )
        
    def __rsub__(self,o):
        if isinstance(o,(datetime.date,datetime.datetime)):
            return Date.from_datetime(o) - self

        raise TypeError(f'Cannot subtract Date from {type(o).__name__}, what are you trying to do?')

    def __iadd__(self, o):
        if isinstance(o, str):
            from dateroll.ddh.ddh import ddh

            o = ddh(o)
        self = self + o
        return self

    def __isub__(self, o):
        if isinstance(o, str):
            from dateroll.ddh.ddh import ddh

            o = ddh(o)
        if isinstance(o, DateLike):
            self = self - (self - o)
        else:
            self = self - o
        return self
    
    @property
    def cal(self):
        if hasattr(self,'origin_dur_date'):
            pretty_calendars = pretty.pretty_between_two_dates(self.date,self.origin_dur_date,self.origin_dur_cals,calmath)
            print(pretty_calendars)
        else:
            pretty_calendars = pretty.pretty_between_two_dates(self.date,self.date,None,calmath)
            print(pretty_calendars)

    def __repr__(self):
        return f'Date(year={self.year},month={self.month},day={self.day})'
    
    def to_string(self):
        '''
        should print as string according to convention
        '''
        if settings.convention=='MDY':
            return self.strftime('%m-%d-%Y')
        elif settings.convention=='DMY':
            return self.strftime('%d-%m-%Y')
        else:
            return self.strftime('%Y-%m-%d')
    
    def __str__(self):
        return self.to_string()

DateLike = DateLike + (Date,)


