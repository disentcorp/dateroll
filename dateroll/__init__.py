from dateroll.ddh.ddh import ddh
from dateroll.date.date import Date
from dateroll.duration.duration import Duration
from dateroll.schedule.schedule import Schedule
from dateroll.calendars.calendarmath import CalendarMath
from dateroll.calendars.calendarmath import Calendars
from dateroll.parser.parser import Parser

import dateroll.calendars.calendarmath as calendarmathModule
import dateroll.calendars.calendars as calendarModule
import dateroll.settings as settingsModule

settings = settingsModule.settings
calmath = calendarmathModule.calmath
cals = calendarmathModule.calmath.cals


# for backwards compatibility testing
# import sys
# import traceback
# try:
#     from dateroll.ddh.ddh import calmath, cals, ddh
#     from dateroll.date.date import Date
#     from dateroll.duration.duration import Duration
#     from dateroll.schedule.schedule import Schedule
#     ddh("t+3m1bd|NYuLN")
#     print("asdfasdf", sys.version.split(" ")[0], "✅" * 30)
# except Exception as e:
#     traceback.print_exc()
#     print("asdfasdf", sys.version.split(" ")[0], "❌" * 30, str(e))
