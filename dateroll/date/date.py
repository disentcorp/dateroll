import calendar
import datetime
from datetime import timezone

import dateutil.relativedelta
from dateutil.parser import parse

from dateroll.calendars.calendarmath import calmath
from dateroll.duration.duration import Duration

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

    def __cmp__(self, b):
        return self.datetime == b

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
        add
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
            return o.__radd__(self)
        elif isinstance(o, int):
            # date + int, int -> duration, -> date + duration -> __radd__ duration
            # goes to __radd__ of Duration
            return Duration(d=o).__radd__(self)
        elif isinstance(o, datetime.timedelta):
            return Date.from_datetime(self.date + o)
        elif isinstance(o, dateutil.relativedelta.relativedelta):
            return Date.from_datetime(self.date + o)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +: 'Date' and {type(o).__name__}"
            )

    @staticmethod
    def minus(a, b):
        if a.year != b.year:
            if a.month == b.month:
                if a.day == b.day:
                    return Duration(y=a.year - b.year)

        elif a.month != b.month and a.day == b.day:
            return Duration(m=(a.month - b.month))

        return Duration(days=(a - b).days)

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
            result = self.minus(self.date, o.date)
            return result
        elif isinstance(o, Duration):
            # date + duration
            # goes to __radd__ of Duration
            return o.__rsub__(self)
        elif isinstance(o, int):
            # date + int, int -> duration, -> date + duration -> __radd__ duration
            # goes to __rsub__ of Duration
            return Duration(d=o).__rsub__(self)
        elif isinstance(o, datetime.timedelta):
            return Date.from_datetime(self.date - o)
        elif isinstance(o, dateutil.relativedelta.relativedelta):
            return Date.from_datetime(self.date - o)
        else:
            raise TypeError(
                f"unsupported operand type(s) for : 'Date' and {type(o).__name__}"
            )

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

    # what about relative deltas?


DateLike = DateLike + (Date,)

if __name__ == "__main__":
    pass
