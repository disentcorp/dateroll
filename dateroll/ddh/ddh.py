import os
import pathlib

# from dateroll.parser.parser import parse_to_dateroll, parse_to_native
import dateroll.parser.parser as parserModule

"""
need daycounters

datroll.* better than native because you can add datestrings to date objects

ddh('t') +'3m' .... it's relaly close to the base but little extra.

"""

# import dateroll.calendars.calendarmath as calendarmathModule
import dateroll.date.date as dateModule
import dateroll.duration.duration as durationModule
import dateroll.schedule.schedule as scheduleModule
import dateroll.calendars.calendarmath as calendarmathModule
import dateroll.calendars.calendars as calendarModule
import dateroll.settings as settingsModule

DEBUG = False

class ddh:
    Date = dateModule.Date
    Duration = durationModule.Duration
    Schedule = scheduleModule.Schedule
    settings = settingsModule.settings
    calmath = calendarmathModule.calmath
    hols = calendarmathModule.calmath.cals

    def __new__(cls, o):
        if isinstance(o, str):
            obj = parserModule.parse_to_dateroll(o)
        elif isinstance(o, dateModule.DateLike):
            return dateModule.Date.from_datetime(o)
        elif isinstance(o, durationModule.DurationLike):
            obj = durationModule.Duration.from_relativedelta(o)
        else:
            raise TypeError(f"ddh() cannot handle {type(o).__name__})")

        return obj

    def purge_all(self):
        """
        dangerous, deletes all calendars and lockfiles
        """
        p = pathlib.Path("~/.dateroll").expanduser()
        import glob

        files = glob.glob(str(p) + "/**/*", recursive=True)
        for file in files:
            if not file.endswith("lockfile"):
                if pathlib.Path(file).is_file():
                    os.remove(file)
        self.hols._purge_all()
        self.calmath._purge_all()


    class YMD:
        global settings
        def __init__(self):
            self.orig = ddh.settings.convention
        def __enter__(self):
            ddh.settings.convention = 'YMD'
        def __exit__(self,*e):
            ddh.settings.convention = self.orig

    class MDY:
        global settings
        def __init__(self):
            self.orig = ddh.settings.convention
        def __enter__(self):
            ddh.settings.convention = 'MDY'
        def __exit__(self,*e):
            ddh.settings.convention = self.orig

    class DMY:
        global settings
        def __init__(self):
            self.orig = ddh.settings.convention
        def __enter__(self):
            ddh.settings.convention = 'DMY'
        def __exit__(self,*e):
            ddh.settings.convention = self.orig


if __name__ == "__main__":  # pragma:no cover
    import time

    a = time.time()
    # [calmath.bck['NYuWE'][calmath.fwd['NYuWE'][i]-1] for i in ddh('1/1/1900,1/1/2100,1d').dates]
    [i - "1bd|NYuWE" for i in ddh("1/1/1900,1/1/2100,1d").dates]
    print(time.time() - a)
