
from dateroll.ddh.ddh import ddh  # noqa F401
from dateroll.date.date import Date  # noqa F401
from dateroll.duration.duration import Duration  # noqa F401
from dateroll.schedule.schedule import Schedule  # noqa F401
from dateroll.calendars.calendarmath import CalendarMath  # noqa F401
from dateroll.calendars.calendarmath import Calendars  # noqa F401
from dateroll.parser.parser import Parser  # noqa F401


import dateroll.settings as settingsModule

settings = settingsModule.settings


# # for backwards compatibility testing
# import sys
# import traceback
# try:
#     ddh("t+3m1bd|NYuLN")
#     print("asdfasdf", sys.version.split(" ")[0], "✅" * 30)
# except Exception as e:
#     traceback.print_exc()
#     print("asdfasdf", sys.version.split(" ")[0], "❌" * 30, str(e))
