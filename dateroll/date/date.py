import datetime
from zoneinfo import ZoneInfo

import dateutil.relativedelta
from tzlocal import get_localzone

import dateroll.ddh.ddh as ddhModule
import dateroll.parser.parser as parserModule
from dateroll import pretty
from dateroll.calendars.calendarmath import calmath
from dateroll.duration.duration import Duration
from dateroll.settings import settings
from dateroll import utils


DateLike = (datetime.datetime, datetime.date)
TZ_DISPLAY = (
    get_localzone()
    if settings.tz_display == "System"
    else ZoneInfo(settings.tz_display)
)
TZ_PARSER = (
    get_localzone() if settings.tz_parser == "System" else ZoneInfo(settings.tz_parser)
)


class Date(datetime.datetime):
    """
    A Date, inherits from datetime.datetime, represents a specific day (no sub-units of day)
    """

    def __new__(cls, *args, **kwargs):
        kwargs.setdefault("tzinfo", TZ_PARSER)
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def from_string(o):
        """ """
        if not isinstance(o, str):
            raise TypeError(
                f"from_string requires string, cannot use {type(o).__name__}"
            )

        dt = parserModule.parse_to_dateroll(o)
        return Date.from_date(dt)

    @staticmethod
    def from_date(o, utc=False):
        """
        Create a Datetime instance from a datetime.date with intraday time hh:mm:ss.us
        """

        if isinstance(o, datetime.datetime):
            return Date(
                o.year, o.month, o.day, o.hour, o.minute, o.second, o.microsecond
            )
        elif isinstance(o, datetime.date):
            return Date(o.year, o.month, o.day, 0, 0)
        else:
            raise TypeError(
                f"from_date requires datetime.datetime, cannot use {type(o).__name__}"
            )

    @staticmethod
    def from_datetime(o):
        if isinstance(o, Date):
            return o
        if isinstance(o, datetime.datetime):

            return Date(
                o.year, o.month, o.day, o.hour, o.minute, o.second, o.microsecond
            )
        elif isinstance(o, datetime.date):
            return utils.date_to_date(o)
        else:
            raise TypeError(
                f"from_date requires datetime.datetime, cannot use {type(o).__name__}"
            )

    @staticmethod
    def from_unix(o):
        """
        convert datetime of UTC
        """
        if not isinstance(o, (int, float)):
            raise TypeError("Must be int/float")
        dt = datetime.datetime.fromtimestamp(o, TZ_PARSER)
        return dt

    @staticmethod
    def from_xls(o):
        """
        excel integer part is days since 12/30/1899, fraction is sub-day
        """
        if not isinstance(o, (int, float)):
            if isinstance(o, str):
                try:
                    o = int(o)
                except Exception:
                    raise TypeError("Must be int/float or int-like string")
            else:
                raise TypeError("Must be int/float")

        base_date = datetime.datetime(1899, 12, 30).astimezone(TZ_PARSER)
        days = int(o)
        fraction = o - days
        seconds_in_day = int(fraction * 24 * 3600)
        dt = base_date + datetime.timedelta(days=days, seconds=seconds_in_day)
        return dt

    @staticmethod
    def from_timestamp(o):
        """
        Create a Date instance from a unix timestamp
        """
        if isinstance(o, (int, float)):
            dt = datetime.datetime.fromtimestamp(o, TZ_PARSER)
            return dt
        else:
            raise TypeError(
                f"from_date requires int/float, cannot use {type(o).__name__}"
            )

    @staticmethod
    def to_naive(o):
        """
        convert time into a naive timezone
        """

        if isinstance(o, DateLike):
            if o.tzinfo is not None:
                dt = o.replace(tzinfo=None)
                return dt
            else:
                return o
        else:
            raise TypeError(
                f"from_date requires int/float, cannot use {type(o).__name__}"
            )

    @staticmethod
    def today():
        return datetime.datetime.now(TZ_PARSER)

    @property
    def time(self):
        return datetime.time(self.hour, self.minute, self.second, self.microsecond)

    @property
    def naive(self):
        """
            convert time into a naive timezone which is a property
        """
        return Date.to_naive(self)

    @property
    def datetime(self):
        if self.tzinfo is not None:
            dt = datetime.datetime(
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                self.second,
                self.microsecond,
            ).astimezone(self.tzinfo)
        else:
            dt = datetime.datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
            )
        
        return dt

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
    def to_xls(self):
        offset = 693594
        n = self.toordinal()
        rs = n - offset
        return rs

    @property
    def to_unix(self):
        return int(self.timestamp())

    @property
    def iso(self):

        if self.tzinfo is not None:
            self = self.replace(tzinfo=None)

        return self.isoformat()

    def __add__(self, o):
        """
        add, do str conversion first, then handle suborinate cases
        """
        # convert string if first
        if isinstance(o, str):
            o = ddhModule.ddh(o)

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
            return Duration(days=o).__radd__(self)
        elif isinstance(o, datetime.timedelta):
            return Date.from_date(self.date + o)
        elif isinstance(o, dateutil.relativedelta.relativedelta):

            result = self.datetime + o
            result = utils.datetime_to_date(result)
            return result
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
            o = ddhModule.ddh(o)
        # apply rules by type

        if isinstance(o, DateLike):
            # date - date
            # convert all datetimes to datetime.datetime for sub to be timedelta, then create Duration from timedelta
            if isinstance(o, Date):
                dt = o.datetime
            elif isinstance(o, datetime.datetime):
                # truncates time!
                dt = o.astimezone(TZ_PARSER)
            else:
                if isinstance(o, datetime.date):
                    dt = datetime.datetime(o.year, o.month, o.day, 0, 0).astimezone(
                        TZ_PARSER
                    )

            relative_delta = dateutil.relativedelta.relativedelta(self.datetime, dt)

            return Duration.from_relativedelta(
                relative_delta, _anchor_start=dt.date(), _anchor_end=self.date
            )

        elif isinstance(o, Duration) or "Duration" in o.__class__.__name__:
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

    def __rsub__(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return Date.from_date(o) - self

        raise TypeError(
            f"Cannot subtract Date from {type(o).__name__}, what are you trying to do?"
        )

    def __iadd__(self, o):
        if isinstance(o, str):

            o = ddhModule.ddh(o)
        self = self + o
        return self

    def __isub__(self, o):
        if isinstance(o, str):

            o = ddhModule.ddh(o)
        if isinstance(o, DateLike):
            self = self - (self - o)
        else:
            self = self - o
        return self

    @property
    def cal(self):

        if hasattr(self, "origin_dur_date"):

            pretty_calendars = pretty.pretty_between_two_dates(
                self.date, self.origin_dur_date.date, self.origin_dur_cals, calmath
            )
            print(pretty_calendars)
        else:
            pretty_calendars = pretty.pretty_between_two_dates(
                self.date, self.date, None, calmath
            )
            print(pretty_calendars)

    def __repr__(self):
        return f"Date({self.year},{self.month},{self.day},{self.hour},{self.minute},{self.second},{self.microsecond},{self.tzinfo})"

    def to_string(self):
        """
        should print as string according to convention
        """
        self.astimezone(TZ_DISPLAY)
        mask = utils.convention_map_datetime[settings.convention]
        result = f"{self.strftime(mask)} {self.tzinfo}"
        return result

    def __str__(self):
        return self.to_string()


DateLike = DateLike + (Date,)
