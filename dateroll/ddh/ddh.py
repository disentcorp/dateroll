import os
import pathlib
import contextlib
import io

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
    # settings = settings

    def __str__(self):
        s = """

    dateroll types:
      ddh.Date (Date class)
      ddh.Duration (Duration class)
      ddh.Schedule (Schedule class)
    
    dateroll settings:
      ddh.settings (stored in ~/.dateroll/settings.py)
    
    dataroll data containers:
      ddh.hols (Calendars singleton instance)
      ddh.calmath (CalendarMath singleton instance)

    dateroll context managers for temporary convention changes:
      ddh.YMM()
      ddh.MDY()
      ddh.DMY()

      ^ use like with ddh.YMD():
                         ddh(some_string_in_YMD_format)
"""
        return s

    def __repr__(self):
        return self.__str__()

    @classmethod
    def validate_args(cls, date_string):
        if isinstance(date_string, str):
            obj = parserModule.parse_to_dateroll(date_string)
        elif isinstance(date_string, dateModule.DateLike):
            obj = dateModule.Date.from_datetime(date_string)
        elif isinstance(date_string, durationModule.DurationLike):
            obj = durationModule.Duration.from_relativedelta(date_string)
        else:
            raise TypeError(f"ddh() cannot handle {type(date_string).__name__})")
        return obj

    def __new__(cls, date_string):
        '''
        if list-like, ie has iter dunder, return a list of each item processed
        if str call parser
        if python date/datetime or dateutil.relativedelta cast into equiv dateroll type
        '''
        if isinstance(date_string,(str,dateModule.DateLike,durationModule.DurationLike)):
            return cls.validate_args(date_string)
        elif hasattr(date_string,'__iter__'):
            l = []
            for i in date_string:
                l.append(cls.validate_args(i))
            return l
        else:
            raise TypeError(f"ddh() cannot handle {type(date_string).__name__})")

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

    # context managers, these let you change the convention temporaily

    class YMD:
        global settings
        def __init__(self):
            self.orig = ddh.settings.convention
        def __enter__(self):
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                ddh.settings.convention = 'YMD'
        def __exit__(self,*e):
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                ddh.settings.convention = self.orig

    class MDY:
        global settings
        def __init__(self):
            self.orig = ddh.settings.convention
        def __enter__(self):
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                ddh.settings.convention = 'MDY'
        def __exit__(self,*e):
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                ddh.settings.convention = self.orig

    class DMY:
        global settings
        def __init__(self):
            self.orig = ddh.settings.convention
        def __enter__(self):
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                ddh.settings.convention = 'DMY'
        def __exit__(self,*e):
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                ddh.settings.convention = self.orig

if __name__ == "__main__":  # pragma:no cover
    
    import code
    code.interact(local=dict(globals(),**locals()))


    
