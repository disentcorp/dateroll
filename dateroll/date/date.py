import calendar
import datetime
from datetime import timezone

import dateutil.relativedelta
from dateutil.parser import parse
from dateroll.duration.duration import Duration
from dateroll.calendars.calendarmath import calmath

DateLike = (datetime.datetime, datetime.date)


class Date(datetime.date):
    ...

    @staticmethod
    def from_string(s, **dateparser_kwargs):
        """
        if string provided use dateutil's parser
        """
        dt = parse(s, **dateparser_kwargs)
        return Date.from_datetime(dt)

    @staticmethod
    def from_datetime(dt):
        """
        Create a Date instance from a datetime.datetime (drops time information), or datetime.date
        """
        if isinstance(dt, DateLike):
            y, m, d = dt.year, dt.month, dt.day
            return Date(y, m, d)

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.strftime("%Y-%m-%d")}")'

    def isBd(self, cals=None):
        """
        am i a business day?
        """
        return calmath.is_bd(self.date,cals=cals)

    def weekDay(self):
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

    def weekYear(self):
        """
        week of the year, iso 8601
        """
        return self.isocalendar()[1]

    def toExcel(self):
        offset = 693594
        n = self.toordinal()
        rs = n - offset
        return rs

    def toUnix(self):
        utc_time = datetime.datetime(
            self.year, self.month, self.day, tzinfo=timezone.utc
        )
        utc_timestamp = utc_time.timestamp()
        return utc_timestamp

    @property
    def iso(self):
        return self.isoformat().split("T")[0]

    def isoStr(self):
        return self.datetime.isoformat(timespec="minutes")

    def __cmp__(self, b):
        return self.datetime == b

    @property
    def datetime(self):
        return datetime.datetime(self.year, self.month, self.day)

    @property
    def date(self):
        return datetime.date(self.year, self.month, self.day)

    @property
    def dt(self):
        return datetime.datetime(self.year, self.month, self.day)

    """
    need to test add,sub,iadd,isub,radd,rsub
    """

    def __sub__(self, o):
        if isinstance(o, DateLike):
            td = o - self.dt
            print(o,self.dt,td)
        elif isinstance(o,str):
            from dateroll.ddh.ddh import ddh
            td = ddh(o)-self.dt
            print(o,self.dt,ddh(o),td)
        else:
            td = super().__sub__(o)
        if not isinstance(td,Duration):
            print(td,type(td))
            dur = Duration(d=td.days)
        else:
            dur = td
        return dur

    def __add__(self, o):
        if isinstance(o, DateLike):
            td = o + self.dt
            print(o,self.dt,td)
        elif isinstance(o,str):
            from dateroll.ddh.ddh import ddh         
            td = ddh(o) + self.dt
            print(o,self.dt,ddh(o),td)
        else:
            td = super().__sub__(o)
        if not isinstance(td,Duration):
            print(td,type(td))
            dur = Duration(d=td.days)
        else:
            dur = td
        return dur
    
    def __radd__(self,o):
        return self.__add__(o)


DateLike = DateLike + (Date,)

if __name__ == "__main__":
    pass
