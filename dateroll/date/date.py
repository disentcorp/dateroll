import calendar
import datetime
from datetime import timezone
import code

import dateutil.relativedelta
from dateutil.parser import parse

from dateroll.calendars.calendarmath import calmath
from dateroll.duration.duration import Duration

DateLike = (datetime.datetime, datetime.date)


class Date(datetime.date):
    ...

    @staticmethod
    def from_string(o, **dateparser_kwargs):
        """
        if string provided use dateutil's parser
        """
        if isinstance(o,Date):
            return o
        elif isinstance(o,str):
            dt = parse(o, **dateparser_kwargs)
            return Date.from_datetime(dt)
        else:
            raise TypeError(f'from_string requires string, cannot use {type(o).__name__}')

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
            raise TypeError(f'from_datetime requires string, cannot use {type(o).__name__}')


    def __repr__(self):
        return f'{self.__class__.__name__}("{self.strftime("%Y-%m-%d")}")'

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

            time_delta = self.date-dt
            return Duration.from_timedelta(time_delta,_anchor_start=dt,_anchor_end=self.date)
        
        elif isinstance(o, Duration) or 'Duration' in o.__class__.__name__:
            # sometimes Duration does not go here instead go as a dateutil, to make sure come here we use .__name__
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


DateLike = DateLike + (Date,)

if __name__ == "__main__": # pragma: no cover
    pass
