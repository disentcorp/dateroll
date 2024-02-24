import datetime
from dateroll.parser import parse_to_dateroll, DEFAULT_CONVENTION

def ddh(string,convention=DEFAULT_CONVENTION):
    return parse_to_dateroll(string,convention=DEFAULT_CONVENTION)