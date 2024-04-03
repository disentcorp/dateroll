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
# from dateroll.settings import settings

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
    @staticmethod
    def purge_all():
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
        ddh.hols._purge_all()
        ddh.calmath._purge_all()


    class YMD:
        global settings
        def __init__(self):
            pass
        def __enter__(self):
            ddh.settings._convention_override = 'YMD'
        def __exit__(self,*e):
            del ddh.settings._convention_override

    class MDY:
        global settings
        def __init__(self):
            pass
        def __enter__(self):
            ddh.settings._convention_override = 'MDY'
        def __exit__(self,*e):
            del ddh.settings._convention_override

    class DMY:
        global settings
        def __init__(self):
            pass
        def __enter__(self):
            ddh.settings._convention_override = 'DMY'
        def __exit__(self,*e):
            del ddh.settings._convention_override


if __name__ == "__main__":  # pragma:no cover

    ddh('t-1y3m')
    
    ...


    
