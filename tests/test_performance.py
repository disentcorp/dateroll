import time
import itertools
import re

from dateroll.ddh.ddh import ddh
from dateroll.settings import settings
from dateroll.parser import parsers

import code
def function_call_string(func, *args, **kwargs):
    arg_str = ', '.join(repr(arg) for arg in args)
    kwarg_str = ', '.join(f"{key}={repr(value)}" for key, value in kwargs.items())
    all_args_str = ', '.join(filter(None, [arg_str, kwarg_str]))
    return f"{func.__name__}({all_args_str})"
def performance_xls():
    """
        to get the dictionary {code:milliseconds} where code is from xls calculation
        code is a string, by eval we can run the code
    """

    import pandas as pd
    perf = {}
    df = pd.read_excel("tests/test_cases.xlsx")
    cols = ["from", "ParserString", "final", "convention"]
    df = df[cols]
    df = df.dropna()
    c = 0
    for idx, row in df.iterrows():
        s = row["ParserString"]
        f = row["from"]
        convention = row["convention"]
        # set correspoinding convention
        settings.convention = convention
        arg = row["final"]
        arg = arg.strftime("%m/%d/%Y") if not isinstance(arg,str) else arg
        _a = time.time()
        
        a = ddh(arg)
        _a2 = time.time()
        b = ddh(s)
        _b = time.time()
        
        ms = round((_a2 - _a) * 1000, 2)
        f = function_call_string(ddh,arg)
        f2 = function_call_string(ddh,s)
        

        
        ms2 = round((_b - _a2) * 1000, 2)
        perf[f] = {'success':True,'run_time':ms}
        perf[f2] = {'success':True,'run_time':ms2}
    return perf

def performance_200():
    """
        to get the dictionary {code:milliseconds} where code is from some combination of month, date and year
    """
    perf = {}

    dates = ["2", "17", "43", "100", "111"]
    months = ["3", "11", "13", "211", "AUG", "au", "augu", "august"]
    years = ["5", "23", "211", "2013", "22414"]
    months_full_name = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    # format mdy
    orig = "MDY"
    settings.convention = orig
    combos = list(itertools.product(months, dates, years))
    combo_count = (
        0  # combo count should be same as len(combos) to cover the all scenarios
    )
    for combo in combos:
        m, d, y = combo
        mdy = f"{m}{d}{y}"

        # m not month name
        if not re.search("[a-zA-Z]", m):
            # combo of mdy can be m=1 d=113 y=2023 works so we need to find new mdy_new
            if len(mdy) == 6 or len(mdy) == 8:
                # should be correct
                mdy_new = f"{m}{d}{y}"
                m2, d2, y2 = mdy_new[:2], mdy[2:4], mdy[4:]
                combo_count += 1
                if int(m2) > 12 or int(m2) < 1:
                    # month is wrong
                    be = time.time()
                    try:
                        ddh(mdy)
                    except:
                        ms = time.time()-be
                        ms = round(ms * 1000,2)
                        f = function_call_string(ddh,mdy)
                        perf[f] = {'success':False,'run_time':ms}

                elif int(d2) > 31 or int(d2) < 1:
                    # date is wrong

                    be = time.time()
                    try:
                        ddh(mdy)
                    except:
                        ms = time.time()-be
                        ms = round(ms * 1000,2)
                        f = function_call_string(ddh,mdy)
                        perf[f] = {'success':False,'run_time':ms}
                elif int(y2) < 1000 and int(y2) >= 100:
                    # eg y=0203

                    be = time.time()
                    try:
                        ddh(mdy)
                    except:
                        ms = time.time()-be
                        ms = round(ms * 1000,2)
                        f = function_call_string(ddh,mdy)
                        perf[f] = {'success':False,'run_time':ms}
                else:
                    # should not raise error
                    be = time.time()
                    ddh(mdy_new)
                    ms = time.time() - be
                    ms = round(ms * 1000,2)
                    f = function_call_string(ddh,mdy_new)
                    perf[f] = {'success':True,'run_time':ms}
            else:
                # should raise error
                if len(mdy) < 6 and len(mdy) > 3:
                    # if less than 3 it wont match so parseError from dateMath

                    be = time.time()
                    try:
                        ddh(mdy)
                    except:
                        ms = time.time()-be
                        ms = round(ms * 1000,2)
                        f = function_call_string(ddh,mdy)
                        perf[f] = {'success':False,'run_time':ms}
                else:

                    be = time.time()
                    try:
                        ddh(mdy)
                    except:
                        ms = time.time()-be
                        ms = round(ms * 1000,2)
                        f = function_call_string(ddh,mdy)
                        perf[f] = {'success':False,'run_time':ms}
                combo_count += 1
        else:
            # m is correct month name
            if len(m) == 3 or m in months_full_name:
                dy_new = f"{d}{y}"
                if len(dy_new) == 4 or len(dy_new) == 6:
                    # correct dy_new
                    d2, y2 = dy_new[:2], dy_new[2:]
                    combo_count += 1
                    if int(d2) > 31 or int(d2) < 1:

                        be = time.time()
                        try:
                            ddh(mdy)
                        except:
                            ms = time.time()-be
                            ms = round(ms * 1000,2)
                            f = function_call_string(ddh,mdy)
                            perf[f] = {'success':False,'run_time':ms}
                    elif int(y2) < 1000 and int(y2) >= 100:
                        # eg y=0203
                        be = time.time()
                        try:
                            ddh(mdy)
                        except:
                            ms = time.time()-be
                            ms = round(ms * 1000,2)
                            f = function_call_string(ddh,mdy)
                            perf[f] = {'success':False,'run_time':ms}
                    else:
                        # it should not raise error
                        be = time.time()
                        ddh(mdy)
                        ms = time.time() - be
                        ms = round(ms * 1000,2)
                        f = function_call_string(ddh,mdy_new)
                        perf[f] = {'success':True,'run_time':ms}
                else:
                    combo_count += 1
                    # will raise error parser
                    if len(dy_new) < 4:
                        # raise value error
                        try:
                            ddh(mdy)
                        except:
                            ms = time.time()-be
                            ms = round(ms * 1000,2)
                            f = function_call_string(ddh,mdy)
                            perf[f] = {'success':False,'run_time':ms}

            else:
                combo_count += 1
                # it will raise value error on month
                try:
                    ddh(mdy)
                except:
                    ms = time.time()-be
                    ms = round(ms * 1000,2)
                    f = function_call_string(ddh,mdy)
                    perf[f] = {'success':False,'run_time':ms}
    print(f"test_parseComboMDY:tested total of {combo_count} cases")

    # reset
    settings.convention = orig 
    return perf

if __name__=='__main__':
    d = performance_xls()
    d2 = performance_200()
    # all dictionary, it is a nested dictionary, if the key 'success' : Fail means it failed to run the arg which is intentional
    d.update(d2)
    