import argparse
from dateroll import ddh

def droll():
    parser = argparse.ArgumentParser(
        prog='droll',
        description="Process DateRollString's from the command line.")
    parser.add_argument('DateRollString')
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    
    args = parser.parse_args()

    x = args.DateRollString
    y = ddh(x)
    print(y)
    if args.verbose:
        hasattr(y,'cal')