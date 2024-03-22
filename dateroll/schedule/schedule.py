

import pandas as pd
from dateroll.calendars.calendarmath import calmath
from dateroll import pretty

import dateroll.parser.parsers as parsersModule

class Schedule(list): 
    def __init__(self,start,stop,step,origin_string=None):
        
        self.start = start
        self.stop = stop
        self.step = step
        self.origin_string = origin_string
        if self.step >=0:
            self.direction = 'forward'
        else:
            self.direction = 'backward'

        self.cals = step.cals

        self.run()
        self.num_dates = len(self.dates)

    @staticmethod
    def from_string(string):
        if isinstance(string, str):
            return parsersModule.parseScheduleString(string)
        else:
            raise TypeError(f"Must be string not {type(string).__name__}")
    def __len__(self):
        return self.num_dates

    def run(self):
        '''
            gives the date range
            direction of date generations is given by the sign of step
        '''
        dates = []

        # backward generation
        if self.direction == 'forward':
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


        self.dates = sorted(dates)
        
        
    @property
    def cal(self):
        _ = pretty.pretty_between_two_dates(self.start,self.stop,self.cals,calmath)
        print(_)
    
    def __str__(self):
        s = f"""Schedule:
    start      : {self.start}
    stop       : {self.start}
    step       : {self.start}
    direction  : {self.direction}
    cals       : {self.cals}
    orig str   : {self.origin_string}
    #dates     : {self.num_dates}"""
        return s
    
    
    def __repr__(self):
        constructor = ""
        for k, v in self.__dict__.items():
            if k not in ['run','spit','dates','debug'] and v is not None:
                constructor += f"{k}={str(v)}, "
        
        return f'{self.__class__.__name__}({constructor.rstrip(", ")})'
    
    @property
    def split(self):
        list_of_dates = self.dates
        start = list_of_dates[:-1]
        stop = list_of_dates[1:]
        step = [self.step.to_string()]*(len(list_of_dates)-1)
        df = pd.DataFrame({'start':start,'stop':stop,'step':step})
        df.index.name = 'per'
        
        return df
    
    @property
    def split_bond(self):
        '''
        makes a bond schedule assuming T+0BD on weekends
        '''
        df = self.split
        df['type']='interest'
        df.columns = ['starts','ends','days','type']
        df['pays']=df['ends']+'0bd'
        st,ed = min(self.dates),max(self.dates)
        
        df.loc[-1]=[None,None,None,'principal',st+'0bd']
        df.loc[len(df)-1]=[None,None,None,'repayment',ed+'0bd']
        df.index+=1
        df['days']=df.apply(lambda row: (row["ends"]-row['starts']).just_exact_days if row['starts'] else None,axis=1)
        return df.sort_values(by='pays')

    def to_string(self):
        '''
        should print as string
        '''
        if self.origin_string:
            return self.origin_string
        else:
            '''
            should subtract from t for a today's version of the string
            '''
            raise NotImplementedError
    
    