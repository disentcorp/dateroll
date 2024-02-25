import datetime
import dateutil
import dateutil.relativedelta

from dateroll.rolling import Rolling
period_order = (*'yhsqmwd','cals','roll')

PeriodLike = (dateutil.relativedelta,datetime.timedelta)

def addNones(*args,zeros=False):
    if zeros:
        sum = 0
    else:
        sum = None
        for arg in args:
            if arg is not None:
                if not sum:
                    sum = arg
                else:
                    sum += arg
    return sum


class Duration:
    '''
    we do not inherit from relativedelta or timedelta, it is something to be considered

    Duration class represents a period of time, a duration of time, an interval of time
    i.e. some distance of time between two specific (yet unknown) dates

    there's implicitly 2 modes:

    calendar day mode - no knowledge of holidays or non-working days
        When counting days, there is no skipping over some days over others because a governing body declares that the offices are closed.
   
    business day mode -  
        a) implicit assumption that 'WE' is always used in bd calcs
            'WE' stands for [W]eek[End] which is our internal two-letter code for the holiday of Saturdays and Sunday's during the "reasonable business period"
        b) user supplied holiday vectors can be unioned for adjusting accordingly

        bd adjustment is O(1) assuming the calenders are in memory or the unions are cached, worst
        bd adjustment is O(n) on bd's between two dates. 

    A duration can have a number of:
        business days
        days (1d = 1.44bd)
        weeks  (1w=7d)
        months (1m approx 28-31d)
        years (1y=12m)

    ^ in order of seniority   


    We define the "reasonable business period" (naiively) as the interval of (t-100y,t+100y)
        this could be extended: from 1582 AD to future if we have historical vectors for holiday calendar changes (i.e. juneteenth 1st occured on X, to map backwards math, and assume last forward for futuree math (e.g. last jubilee was 5cd, and happens every 50years..))
        realistically 5-7 year perfect lookup would be more than substantial for more use cases.
    '''

    # on init, should we turn hemi/sem into 6mo and quarters into 3m?
    collapse_hemi_sem_quart_on_init = True

    def __init__(self,
        y=None,
        Y=None,
        h=None,
        H=None,
        s=None,
        S=None,
        q=None,
        Q=None,
        m=None,
        M=None,
        w=None,
        W=None,
        d=None,
        D=None,
        cals=None,
        bd=None,
        BD=None,
        roll=None,
    ):
        '''
        y = year
        h = half year
        s = semester = half year
        q = quarter
        m = month
        w = week
        d = day
        bd = business days
        cals = list of 2-letter codes for calendars
        roll = roll convention (F,P,MF,MP)

        ^ non means not supplied, 0 means zero supplied

        '''
        self.y = addNones(y,Y)
        if self.collapse_hemi_sem_quart_on_init:
            _m = addNones(addNones(m,M),3*addNones(q,Q,zeros=True),6*addNones(s,S,h,H,zeros=True))
            if _m > 0:
                self.m = 0
            else:
                self.m = None
        else:
            self.m = addNones(m,M)
        self.w = addNones(w,W)
        self.d = addNones(d,D)
        self.bd = addNones(bd,BD)

        if cals is not None:
            _cals = set()
            if isinstance(cals,(list,tuple)):
                for cal in cals:
                    if isinstance(cal,str):
                        if len(cal)==2:
                            ... # tbd
                            _cals | {cal,}
                        else:
                            raise Exception(f'Calendars must be 2-letter strings (not {cal})')
                    else:
                        raise Exception(f'Calendars must be strings (not {type(cal).__name__})')
            self.cals = _cals
        else:
            self.cals = None

        if (self.bd is None and cals and len(cals) > 0):
            self.bd = 0

        # add weekends if adjusting
        if self.bd is not None:
            if self.cals:
                self.cals |= {'WE',}
            else:
                self.cals = {'WE',}

        # now validate roll           
        if roll is not None:
            if isinstance(roll,str):
                if roll in Rolling.__dict__:
                    self.roll = roll
                else:
                    NotImplementedError(roll)
            else:
                raise Exception('roll must be a str')
        else:
            if self.bd is not None:
                if self.bd >= 0:
                    self.roll = 'F'
                elif self.bd <0:
                    self.roll = 'P'
                else:
                    raise NotImplementedError('n/a')
            else:
                self.roll = None




    @property
    def delta(self):
        '''
        '''
        rd_args = {}
        if self.y:
            rd_args['years']=self.y
        if self.m:
            rd_args['months']=self.m
        if self.w:
            rd_args['weeks']=self.w
        if self.d:
            rd_args['days']=self.d
        rd = dateutil.relativedelta.relativedelta(**rd_args)
        return rd
    
    def apply_business_date_adjustment(self,from_date):
        '''
        '''
        print('bd adj on',self.cals)
        # raise NotImplementedError
    
    def apply_roll_convention(self,from_date):
        '''
        '''

        print('rolling to ',self.roll)
        # raise NotImplementedError
    
    def compute_business_days(self):
        '''
        '''
        ...

    def simmplify(self):
        '''
        excluding business days, from smallest unit (d) to largest (y) 
        if units is larger than the next largest unit, and it is perfectly divisible,
        subtract equivalent units from smaller and increment the larger

        e.g.

        25mo = 2y1m (exact)
        5w = 1m1w (approx)
        28d = 1m (approx)

        make a setting to enable approx calculations

        approx:
            28-31 days is 1m
            4w is 1m
        exact:
            12m is 1y

        note - we skip 1w = exactly 7d, because no human knows what 2w3d but they know 17d is roughly 1/2 a month in their head

        note: q, s, and h are automatically converted to more senior buckets

        '''
        ...

    '''
    if 3m with calenda
    
    '''

    def math(self,x,direction):
        '''
        '''
        rd = self.delta
        # add/sub

        y = x + direction*rd

        # bd adjustment
        if self.bd:
            y_adj = self.apply_business_date_adjustment(y)
        else:
            y_adj = y
        
        # date rolling
        if self.roll:
            y_rolled = self.apply_roll_convention(y_adj) 
        else:
            y_rolled = y_adj

        return y_rolled
    

    @property
    def q(self):
        ''' equiv quarters '''

    @property
    def s(self):
        ''' equiv semesters '''

    ... # q, w, h, d, bd(with cal), y {implicit act/365, can be setting,} y(with counter)
    # m, ... 
    
    def __radd__(self, x): return self.math(x, 1)
    def __rsub__(self, x): return self.math(x, -1)
    def __add__ (self, x): return self.math(x, 1)
    def __sub__ (self, x): return self.math(x, -1)
    def __iadd__(self, x): return self.math(x, 1)
    def __isub__(self, x): return self.math(x, -1)

    def __repr__(self):
        '''
        repr sorts units by seniority specificed in global

        future note: implicity call the simplify() method before sorting, and repr on the simpllifed version, not direct on __dict__
        consider moving ny/nm/nd/nbd to dict on class??
        '''
        d = self.__dict__
        items = {k: d[k] for k in period_order if k in d}
        constructor = ''
        for k,v in self.__dict__.items():
            if v!=None or (v==0 and k=='bd'):
                if k =='roll':
                    v = f'"{v}"'
                constructor += f'{k}={v}, '
        return f'{self.__class__.__name__}({constructor.rstrip(", ")})'


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
    

PeriodLike = PeriodLike + (Duration,)


# if __name__ == '__main__':
#     ...