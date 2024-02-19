import datetime


from dateroll.date import Date
from dateroll.period import Period
from dateroll.utils import fwd_or_bwd
from dateroll.utils import datePeriodParse, genEndtoEnd
from dateroll.utils import DATE_RANGE_HELPER_DICT, IERULE_MAPPING, LASTDATEOFMONTH


class Schedule:
    def __init__(
        self,
        st,
        ed,
        per="1m",
        stub="short",
        ret="l",
        monthEndRule="anniv",
        ie="[)",
        dc=NotImplementedError,
    ):
        self.stub = stub
        self.ret = ret
        self.monthEndRule = monthEndRule
        self.ie = ie
        self.dc = dc
        asof_st, dur_st = datePeriodParse(st)
        asof_ed, dur_ed = datePeriodParse(ed)
        st1 = Date(asof_st) + Period(dur_st)
        ed1 = Date(asof_ed) + Period(dur_ed)
        self.per_origin = per
        st1, ed1, per, bwd = fwd_or_bwd(st1, ed1, per)
        self.per = Period(per)
        self.bwd = bwd

        if st1 != ed1:  # here applied ieRule; did not understand why self.st>self.ed runs a lot of code?
            ed1, st1 = IERULE_MAPPING[ie](ed1, st1, Period("1bd")) if "bd" in self.per.__str__().lower() else IERULE_MAPPING[ie](ed1, st1, Period("1d"))

        self.st = st1
        self.ed = ed1

    def __call__(self):
        if self.st == self.ed:
            st_ = self.st

            if "bd" in self.per.__str__().lower():
                st_ = st_ + Period("0bd")
            if st_ > self.ed:
                return []
            else:
                return [st_]
        return self.genLWrapper()

    def __repr__(self):
        return f"{self.genLWrapper()}"

    def genL(self):
        """returns range of dates"""
        dts = []
        dt = self.st
        done = False
        max_iter = 40000
        c = 0
        dt = dt + Period("0bd")
        while not done:

            c += 1
            if c > max_iter:
                raise Exception("blowing up")
            dts.append(dt)

            dt += self.per
            if not ("d" in self.per.__str__().lower() or "w" in self.per.__str__().lower()):
                dt_day = min(self.st.day, LASTDATEOFMONTH(dt).day)
                dt = dt.replace(day=dt_day)

            if not self.bwd and dt >= self.ed.datetime:
                done = True
            elif self.bwd and dt <= self.ed:
                done = True

        return dts

    def genLWrapper(self):
        dts = self.genL()
        if "bd" in str(self.per):
            dts[-1] = dts[-1] + Period("0bd")
        lst = dts[-1] + self.per
        if lst == self.ed:

            dts.append(self.ed)
            self.stub = "full"
        else:
            if self.stub == "short":
                dts.append(self.ed)
            else:
                if self.stub != "long":
                    raise Exception("Stub either short or full, please check the stub name")

                if len(dts) % 2 == 0:
                    dts[-1] = self.ed
                else:
                    dts.append(self.ed)
        if not "d" in self.per.__str__().lower() and self.monthEndRule == "end-to-end":
            if self.st != LASTDATEOFMONTH(self.st):
                raise Exception("MonthEndRule only applies when start date is end of month")
            dts = genEndtoEnd(dts)
        if "d" in self.per.__str__().lower() and "1" in self.per.__str__().lower():
            self.stub = "full"
        rs = DATE_RANGE_HELPER_DICT[self.ret.lower()](dts, self.stub)
        # handle result, if lp, it has to be period, if period<0 it has to be negative period in the result
        if not self.ret.lower() in ["ll", "df", "lp"]:
            rs = set(rs)
            rs = list(sorted(rs))
        if self.ret.lower() == "df":
            f = lambda p: f"-{p}" if ("-" in self.per_origin and not "-" in p) else f"{p}"
            rs["dur"] = rs["dur"].apply(f)
        if self.ret.lower() == "lp":
            rs = [Date(f"-{p}d") if ("-" in self.per_origin and p >= 0) else Date(f"{p}d") for p in rs]
        if isinstance(rs,list) and len(rs)>0 and isinstance(rs[0],datetime.datetime):
            # temporary fix, sometimes self.ret has datetime instead of date
            rs = [Date(dt) for dt in rs]

        return rs
    
if __name__ == '__main__':
    ...