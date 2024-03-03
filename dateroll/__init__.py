from dateroll.date.date import Date
from dateroll.ddh.ddh import calmath, cals, ddh
from dateroll.duration.duration import Duration
from dateroll.schedule.schedule import Schedule

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
