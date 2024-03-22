import fcntl
import pathlib
import re
import calendar
from dateroll.parser import patterns

XPRINT_ON = False

DEBUG_COLORS = {
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[33m",
    "red": "\033[31m",
    "end": "\033[0m",
    "gray": "\x1b[38;5;239m",
}


month_dict = {
        "jan": "01", "feb": "02", "mar": "03",
        "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09",
        "oct": "10", "nov": "11", "dec": "12",
        "january": "01", "february": "02", "march": "03",
        "april": "04","may":"05", "june": "06", "july": "07",
        "august": "08", "september": "09", "october": "10",
        "november": "11", "december": "12"
}

date_string_coordinates = {
    'YMD':{
        6:{
            'y':slice(0,2),
            'm':slice(2,4),
            'd':slice(4,6)
        },
        8:{
            'y':slice(0,4),
            'm':slice(4,6),
            'd':slice(6,8)
        }
    },
    'MDY':{
        6:{
            'y':slice(4,6),
            'm':slice(0,2),
            'd':slice(2,4)
        },
        8:{
            'y':slice(4,8),
            'm':slice(0,2),
            'd':slice(2,4)
        }
    },
    'DMY':{
        6:{
            'y':slice(4,6),
            'm':slice(2,4),
            'd':slice(0,2)
        },
        8:{
            'y':slice(4,8),
            'm':slice(2,4),
            'd':slice(0,2)
        }
    }
}


def color(s, color):
    return DEBUG_COLORS[color] + str(s) + DEBUG_COLORS["end"]

def get_month_days(y,m):
    _, num_days = calendar.monthrange(y, m)
    return num_days

def xprint(*args, **kwargs):  # pragma:no cover
    if XPRINT_ON:
        _color = kwargs.get("color", "yellow")
        if "lbl" in kwargs:
            lbl = kwargs.get("lbl")
            b = kwargs.get("before", "x")
            a = kwargs.get("after", "x")
            b = str(b)
            a = str(a)
            a_star = ""
            for _a, _b in zip(a, b):
                if _a == _b:
                    a_star += color(_a, "green")
                else:
                    a_star += color(_a, "blue")
            b = color(b, "green")
            s = f"{color('before',_color)}: {b}, {color('after',_color)}: {a_star}"
            print(color(f"[debug] {lbl:>12} ", _color), s)
        else:
            args = [color(a, _color) for a in args]
            print(color("[debug]", _color), *args, **kwargs)


def combine_none(a, b):
    if a is None and b is None:
        return None
    a = [] if a is None else a
    b = [] if b is None else b
    return tuple(sorted(set(a) | set(b)))


def add_none(a, b, dir=1):
    if a is None and b is None:
        return None
    else:
        a = 0 if a is None else a
        b = 0 if b is None else b
        return a + b * dir
    
def swap_month_names(s):
    '''
        swap month names into number string eg, Aug-->08
    '''
    month_str = re.match('[a-zA-Z]+',s)
    if month_str:
        # aug or AUG --> Aug
        
        month_str = month_str[0].lower()
        month_str_numb = month_dict.get(month_str,None)
        if month_str_numb is None:
   
            raise ValueError('Month name is wrong')
        s = patterns.MONTHNAMES.sub(month_str_numb,s.capitalize())
    return s 

class safe_open:
    """
    use separate write lockfile to lock/unlock (fcntl removes dealock if pid w/ lock dies)
    lock is removed if pid dies
    """

    def __init__(self, path, mode="r"):
        """
        open lockfile and attempt to lock, will block
        """
        self.path = pathlib.Path(path)
        self.mode = mode
        if mode.startswith('w'):
            self.pathlock = self.path.with_suffix(".lockfile")
            self.lockfile = open(self.pathlock, "w")
            fcntl.lockf(self.lockfile, fcntl.LOCK_EX)

    def __enter__(self):
        """
        open user file and send it to them
        """
        self.file = open(self.path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        release lock, then close both lockfile and user file
        do not delete lockfile (even if no exc)
        """
        if self.mode.startswith('w'):
            fcntl.lockf(self.lockfile, fcntl.LOCK_UN)
            self.lockfile.close()
            self.file.close()


convention_map = {"YMD": r"%Y-%m-%d", "DMY": r"%d-%m-%Y", "MDY": r"%m-%d-%Y"}
