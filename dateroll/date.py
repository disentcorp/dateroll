import datetime
from datetime import timezone
from tplus1.period import Period
from tplus1.holidays import get_hol_list
from dateutil.parser import parse
import calendar
import numpy

class Date(datetime.date):
    # dt_str some f(y,m,d)
    def __new__(self, *args, **kwargs):
        if isinstance(args[0], str):
            if args[0] in ["0", "t0", "t", "T", "today", "Today", "TODAY"]:
                val = datetime.date.today()
            else:
                val = parse(args[0])
            y, m, d = val.year, val.month, val.day
            return super().__new__(self, y, m, d)  # super().__new__(self,y,m,d,0,0,0)
        elif isinstance(args[0], datetime.date):
            y, m, d = args[0].year, args[0].month, args[0].day
            return super().__new__(self, y, m, d)
        else:
            return super().__new__(self, *args, **kwargs)

    def __str__(self):
        return f'{self.strftime("%d-%b-%Y")}'

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.strftime("%Y-%m-%d")}")'

    def isBd(self, cal="WE"):
        hol_list = get_hol_list([self.year], cal=cal)
        if self.weekday() in [5, 6] or self in hol_list:
            return False
        else:
            return True

    def weekDay(self):
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

    def weekMonth(self):
        d = numpy.array(calendar.monthcalendar(self.year, self.month))
        week_of_month = numpy.where(d == self.day)[0][0] + 1

        return week_of_month

    def weekYear(self):
        return self.isocalendar()[1]

    def toExcel(self):
        offset = 693594
        n = self.toordinal()
        rs = n - offset
        return rs

    def toUnix(self):
        utc_time = datetime.datetime(self.year, self.month, self.day, tzinfo=timezone.utc)

        utc_timestamp = utc_time.timestamp()
        return utc_timestamp

    def toStr(self):
        return self.strftime("%Y%m%d")

    def isoStr(self):
        return self.datetime.isoformat(timespec="minutes")

    def strftime(self, mask):
        return datetime.datetime(self.year, self.month, self.day).strftime(mask)

    @property
    def datetime(self):
        return datetime.datetime(self.year, self.month, self.day)
    
    def __sub__(self, lhs):
        if isinstance(lhs, datetime.date) and isinstance(self, datetime.date):
            dt1 = lhs.toStr()
            dt2 = self.toStr()
            str_ = f"{dt2}-{dt1}"
            return Period(str_)
        else:
            dt = self.strftime("%Y%m%d")
            dr = lhs.__str__()
            str_ = "".join([dt, dr])
            rs = Period(dr).__sub__(self)

            return rs 

    def __add__(self,o):
        if isinstance(o,str):
            try:
                o_adj = Period(o)
            except:
                o_adj = Date(o)
            res = o_adj.__add__(self)
            return res
        return super().__add__(o)
    
    def __radd__(self,o):
        return self.__add__(o)

if __name__ == '__main__':
    ...