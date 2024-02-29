# DATE_CONVERT_DICT = {
#     "1w": {"d": {"7d": "perfect"}},
#     "1m": {"d": {"30d": "approx"}, "w": {"4w": "approx"}},
#     "1q": {"d": {"90d": "approx"}, "w": {"12w": "approx"}, "m": {"3m": "perfect"}},
#     "1y": {"d": {"365d": "approx"}, "w": {"52w": "approx"}, "m": {"12m": "perfect"}, "q": {"4q": "perfect"}},
#     "7d": {"w": {"1w": "perfect"}},
#     "29d": {"m": {"1m": "approx"}},
#     "30d": {"m": {"1m": "approx"}},
#     "31d": {"m": {"1m": "approx"}},
#     "89d": {"q": {"1q": "approx"}},
#     "90d": {"q": {"1q": "approx"}},
#     "91d": {"q": {"1q": "approx"}},
#     "364d": {"y": {"1y": "approx"}},
#     "365d": {"y": {"1y": "approx"}},
#     "366d": {"y": {"1y": "approx"}},
#     "4w": {"m": {"1m": "approx"}},
#     "12w": {"q": {"1q": "approx"}},
#     "52w": {"y": {"1y": "approx"}},
#     "3m": {"q": {"1q": "perfect"}},
#     "12m": {"y": {"1y": "perfect"}},
#     "4q": {"y": {"1y": "perfect"}},
# }


# def get_numb_yr(per):
#     per = per.replace("+", "")
#     n_ptn = r"(\d+(?:\.\d+)?)"
#     yr_ptn = "[dwmqyDWMQY]"
#     numb = float(re.findall(n_ptn, per)[0])
#     yr = re.findall(yr_ptn, per)[0]
#     return numb, yr


# def period_add(converted_periods):
#     if len(converted_periods) == 1:
#         return converted_periods[0]
#     elif len(converted_periods) > 1:
#         _, per = get_numb_yr(converted_periods[0])  # since all values of list have same period
#         ls = [get_numb_yr(per)[0] for per in converted_periods]
#         numb = sum(ls)
#         return f"{numb}{per}"
#     else:
#         return converted_periods


# def date_convert_dict_helper(per, roughly):
#     converted_per = per
#     perfect_or_approx = "perfect"
#     numb, yr = get_numb_yr(per)
#     per2 = f"1{yr}"
#     if per2 in DATE_CONVERT_DICT.keys():
#         if roughly in DATE_CONVERT_DICT[per2].keys():
#             converted_per, perfect_or_approx = list(DATE_CONVERT_DICT[per2][roughly].items())[0]
#             numb2, yr2 = get_numb_yr(converted_per)
#             numb_last = numb * numb2
#             converted_per = f"{numb_last}{yr2}"
#     return converted_per, perfect_or_approx


# def date_convert_dict(per, roughly):
#     if per in DATE_CONVERT_DICT.keys():
#         if roughly in DATE_CONVERT_DICT[per].keys():
#             converted_per, perfect_or_approx = list(DATE_CONVERT_DICT[per][roughly].items())[0]
#         else:
#             converted_per, perfect_or_approx = date_convert_dict_helper(per, roughly)
#     else:
#         # numb,yr = get_numb_yr(per)

#         converted_per, perfect_or_approx = date_convert_dict_helper(per, roughly)
#     return converted_per, perfect_or_approx


# class Duration:  # look like a subclass of relativedelta
#     # dt_str some f(operatior,num,unit,cal_array,roll_function)
#     def __init__(self, date_period_string):
#         raise Exception
#         self.orig_date_period_string = date_period_string
#         # self.date_period_string,self.st,self.ed = dtYMD_convert(date_period_string)
#         self.date_period_string, self.days_, self.st, self.ed = self.per(date_period_string)
#         self.date_period_function = datePeriodStringToDatePeriod(self.date_period_string)

#     def convert(self, roughly=None):
#         date_period_strings = re.findall(r"\d+[dDwWmMqQsShHyY]", self.date_period_string)
#         converted_periods = []
#         for date_period_string in date_period_strings:
#             converted_per, perfect_or_approx = date_convert_dict(date_period_string, roughly)
#             converted_periods.append(converted_per)
#         converted_per = period_add(converted_periods)
#         if perfect_or_approx == "approx":
#             warnings.warn("roughly approximated, this may not be true as there is no anchor date")
#         return converted_per

#     @staticmethod
#     def from_relativedelta(rd_object):
#         '''
#         create Duration from dateutil.relativedelta.relativedelta
#         '''

#     @staticmethod
#     def from_timedelta(td_object):
#         '''
#         create Duration from datetime.timedelta
#         '''

#     @staticmethod
#     def from_string(td_object):
#         '''
#         create Duration from DurationString
#         '''


#     def cd(self, ie="[)"):
#         # self.stub='short',self.ret='l',self.monthEndRule='anniv',self.ie=NotImplementedError,self.dc=NotImplementedError
#         if self.st == None or self.ed == None:
#             raise Exception("both start date and end date should be given")

#         n = (self.ed - self.st).days
#         return n

#     def toDt(self):
#         if isinstance(self.rs, str):
#             self.rs = datetime.datetime.strptime(self.rs, "%Y%m%d")  # datetime.strptime(rs,'%Y%m%d')

#         # self.rs = self.rs.replace(hour=0, minute=0, second=0, microsecond=0)
#         from dateroll.date import Date
#         return Date(self.rs)

#     def today(self):
#         return self.date_period_function(datetime.date.today(), 1)

#     def __radd__(self, lhs):  # +
#         self.rs = self.date_period_function(lhs, 1)
#         return self.toDt()

#     def __rsub__(self, lhs):  # -
#         self.rs = self.date_period_function(lhs, -1)
#         return self.toDt()

#     def __add__(self, lhs):  # +
#         self.rs = self.date_period_function(lhs, 1)

#         return self.toDt()

#     def __sub__(self, lhs):  # -
#         self.rs = self.date_period_function(lhs, -1)
#         return self.toDt()

#     def __iadd__(self, lhs):  # +=
#         self.rs = self.date_period_function(lhs, 1)

#         return self.toDt()

#     def __isub__(self, lhs):  # -=
#         self.rs = self.date_period_function(lhs, -1)
#         return self.toDt()

#     def __str__(self):
#         return f"{self.orig_date_period_string}"

#     def __repr__(self):
#         return f'Duration("{self.orig_date_period_string}")'

#     def per(self, date_period_string):

#         try:
#             st, ed = re.findall(PTN, date_period_string)
#         except:
#             return date_period_string, "", None, None
#         # this part handles when date parse goes to format like 20220101-03,132022. Tried to other more robust methods, kinda stuck, later change the method
#         if "-" in st:
#             prs1 = st.split("-")

#             if "-" in ed:
#                 ed1 = "-".join([prs1[-1], ed])
#             elif "/" in ed:
#                 ed1 = "/".join([prs1[-1], ed])
#             elif "." in ed:
#                 ed1 = ".".join([prs1[-1], ed])
#             else:
#                 ed1 = "".join([prs1[-1], ed])
#             st = prs1[0]
#             ed = ed1
#         try:
#             st = parse(st)
#             ed = parse(ed)
#         except:
#             return date_period_string, "", None, None
#         m = 0
#         y = 0
#         d = []
#         dt = st
#         if st < ed:
#             dt_prev = dt
#             dt += relativedelta(months=1)

#             while dt <= ed:

#                 d.append((dt - dt_prev).days)
#                 m += 1
#                 if m == 12:
#                     m = 0
#                     y += 1
#                 dt_prev = dt
#                 dt += relativedelta(months=1)
#             if dt > ed:
#                 dt_prev = dt + relativedelta(months=-1)
#                 d.append((ed - dt_prev).days)
#             dur_string = f"-{y}y{m}m{d[-1]}d"
#             days_ = -sum(d)
#         elif st > ed:
#             dt_prev = dt
#             dt += relativedelta(months=-1)
#             while dt >= ed:

#                 d.append(abs((dt - dt_prev).days))
#                 m += 1
#                 if m == 12:
#                     m = 0
#                     y += 1
#                 dt_prev = dt
#                 dt += relativedelta(months=-1)
#             if dt < ed:
#                 d.append(abs((ed - dt_prev).days))
#             dur_string = f"{y}y{m}m{d[-1]}d"
#             days_ = sum(d)
#         else:
#             return "0y0m0d", 0, None, None
#         return dur_string, days_, st, ed

#     @property
#     def days(self):
#         n = Duration(self.date_period_string).convert("d")
#         n = float(n.replace("d", ""))
#         return n
