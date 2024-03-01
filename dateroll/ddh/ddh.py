import datetime
import shutil
import pathlib

from dateroll.parser.parser import parse_to_dateroll, parse_to_native

"""
need daycounters

datroll.* better than native because you can add datestrings to date objects

ddh('t') +'3m' .... it's relaly close to the base but little extra.

"""

from dateroll.parser.parsers import DEFAULT_CONVENTION
from dateroll.calendars.calendarmath import calmath

cals = calmath.cals

class ddh:
    convention = DEFAULT_CONVENTION
    calmath = calmath
    cals = cals

    def __new__(self, string, convention=None):
        if convention is not None:
            self.convention = convention
        obj = parse_to_dateroll(string, convention=self.convention)
        return obj

    @staticmethod
    def purge_all():
        '''
        dangerous, deletes all calendars and lockfiles
        '''
        p = pathlib.Path('~/.dateroll').expanduser()
        shutil.rmtree(p)
