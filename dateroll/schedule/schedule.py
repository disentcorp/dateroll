import datetime

import pandas as pd

import dateroll.calendars.calendarmath as calendarmathModule
import dateroll.parser.parsers as parsersModule
from dateroll import pretty
from dateroll.date import date as dateModule
from dateroll.duration import duration as durationModule
from dateroll.ddh import ddh as ddhModule
from dateroll import utils
from dateroll import settings

class Schedule:
    '''
    list-like schedule generator
    '''
    def __init__(self, start, stop, step, origin_string=None):

        self.start = start
        self.stop = stop
        self.step = step
        self.origin_string = origin_string
        if self.step >= 0:
            self.direction = "forward"
        else:
            self.direction = "backward"

        self.cals = step.cals

        self.run()
        self.num_dates = len(self._dates)

    @staticmethod
    def from_string(string):
        if isinstance(string, str):
            return parsersModule.parseScheduleString(string)
        else:
            raise TypeError(f"Must be string not {type(string).__name__}")

    def __len__(self):
        return self.num_dates
    
    @property
    def list(self):
        '''
        returns list of dates
        '''
        return self._dates

    @property
    def dates(self):
        '''
        returns list of dates
        '''
        return self._dates

    def run(self):
        """
        gives the date range
        direction of date generations is given by the sign of step
        """
        dates = []
        # backward generation
        if self.direction == "forward":
            cursor = self.start
            while cursor < self.stop:
                dates.append(cursor)
                # we use plus sign because step<0
                cursor += self.step
            dates.append(self.stop)
        else:
            # backward generation
            cursor = self.stop

            while cursor > self.start:
                dates.append(cursor)
                cursor -= -self.step
            dates.append(self.start)

        self._dates = sorted(dates)

    @property
    def cal(self):
        _ = pretty.pretty_between_two_dates(
            self.start, self.stop, self.cals, calendarmathModule.calmath
        )
        print(_)

    def __getitem__(self,k):
        if isinstance(k,int):
            return self._dates[k]
        elif isinstance(k,str):
            d = ddhModule.ddh(k)
            if d in self._dates:
                return d
            else:
                raise KeyError(d)
        elif isinstance(k,slice):
            return utils.date_slice(k,self._dates)
        else:
            raise TypeError('Indexation only support ints, date strings, or slices.')

    def __str__(self):
        s = f"""Schedule:
    start      : {self.start}
    stop       : {self.start}
    step       : {self.start}
    direction  : {self.direction}
    cals       : {self.cals}
    orig str   : {self.origin_string}
    num dates     : {self.num_dates:,}"""
        return s

    def __repr__(self):
        constructor = ""
        for k, v in self.__dict__.items():
            if k not in ["run", "spit", "dates", "debug"] and v is not None:
                constructor += f"{k}={str(v)}, "

        return f'{self.__class__.__name__}({constructor.rstrip(", ")})'

    def __iter__(self):
        for i in self._dates:
            yield i

    def __contains__(self, x):
        if isinstance(x, dateModule.Date):
            x = x.date
        elif isinstance(x, datetime.datetime):
            # does not do TZ check
            x = datetime.date(x.year, x.month, x.day)
        for i in self._dates:
            if isinstance(i, dateModule.Date):
                i = i.date
            # elif isinstance(i, datetime.datetime):
            #     # does not do TZ check
            #     i = datetime.date(i.year, i.month, i.day)

            if x == i:
                return True
        return False

    @property
    def split(self):
        list_of_dates = self._dates
        start = list_of_dates[:-1]
        stop = list_of_dates[1:]
        df = pd.DataFrame({"start": start, "stop": stop})
        df['step']=df.stop-df.start
        df.index.name = "per"

        return df

    @property
    def split_bond(self):
        """
        makes a bond schedule assuming T+0BD on weekends
        """
        df = self.split
        df["type"] = "interest"
        df.columns = ["starts", "ends", "days", "type"]
        df["pays"] = df["ends"] + "0bd"
        st, ed = min(self._dates), max(self._dates)

        df.loc[-1] = [None, None, None, "principal", st + "0bd"]
        df.loc[len(df) - 1] = [None, None, None, "repayment", ed + "0bd"]
        df.index += 1
        df["days"] = df.apply(
            lambda row: (
                (row["ends"] - row["starts"]).just_exact_days if row["starts"] else None
            ),
            axis=1,
        )
        return df.sort_values(by="pays")

    def to_string(self):
        """
        should print as string
        """
        if self.origin_string:
            return self.origin_string
        else:
            """
            should subtract from t for a today's version of the string
            """
            raise NotImplementedError
