import datetime

from dateroll.utils.parser import parse_to_dateroll, parse_to_native

"""
need daycounters

datroll.* better than native because you can add datestrings to date objects

ddh('t') +'3m' .... it's relaly close to the base but little extra.

"""


def ddh(string, convention=None):
    return parse_to_dateroll(string, convention=convention)
