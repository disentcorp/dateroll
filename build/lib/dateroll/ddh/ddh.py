import datetime

from dateroll.parser.parser import parse_to_dateroll, parse_to_native

"""
need daycounters

datroll.* better than native because you can add datestrings to date objects

ddh('t') +'3m' .... it's relaly close to the base but little extra.

"""

from dateroll.calendars.calendarmath import calmath

cals = calmath.cals

class ddh:
    calmath = calmath
    cals = cals

    def __new__(self, string, convention=None):
        obj = parse_to_dateroll(string, convention=convention)
        return obj
