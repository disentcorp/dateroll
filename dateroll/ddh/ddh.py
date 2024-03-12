import os
import datetime
import pathlib
import shutil

from dateroll.parser.parser import parse_to_dateroll, parse_to_native

"""
need daycounters

datroll.* better than native because you can add datestrings to date objects

ddh('t') +'3m' .... it's relaly close to the base but little extra.

"""

from dateroll.calendars.calendarmath import calmath
from dateroll.parser.parsers import DEFAULT_CONVENTION
from dateroll.date.date import DateLike, Date
from dateroll.duration.duration import DurationLike, Duration

DEBUG = False

cals = calmath.cals


class ddh:
    convention = DEFAULT_CONVENTION
    calmath = calmath
    cals = cals
    debug = False

    def __new__(cls, o, convention=None,debug=debug):
        if convention is not None:
            cls.convention = convention

        if isinstance(o,str):
            obj = parse_to_dateroll(o, convention=cls.convention,debug=cls.debug)
        elif isinstance(o,DateLike):
            return Date.from_datetime(o)
        elif isinstance(o,DurationLike):
            obj = Duration.from_relativedelta(o)
        else:
            raise TypeError(f'ddh() cannot handle {type(o).__name__})')

        return obj

    @staticmethod
    def purge_all():
        """
        dangerous, deletes all calendars and lockfiles
        """
        p = pathlib.Path("~/.dateroll").expanduser()
        import glob
        files = glob.glob(str(p)+'/**/*',recursive=True)
        for file in files:
            if not file.endswith('lockfile'):
                if pathlib.Path(file).is_file():
                    os.remove(file)
        cals._purge_all()
        calmath._purge_all()
        
