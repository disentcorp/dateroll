import datetime

from dateroll.parser import DEFAULT_CONVENTION
from dateroll.parser import parse_to_dateroll
from dateroll.parser import parse_to_native

'''
need daycounters

datroll.* better than native because you can add datestrings to date objects

ddh('t') +'3m' .... it's relaly close to the base but little extra.

'''


def ddh(string,convention=DEFAULT_CONVENTION):
    return parse_to_dateroll(string,convention=DEFAULT_CONVENTION)