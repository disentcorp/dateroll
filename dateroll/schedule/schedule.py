
import code

class Schedule: 
    def __init__(self,start,stop,step):
        self.start = start
        self.stop = stop
        self.step = step
        
        if self.step >=0:
            self.direction = 'forward'
        else:
            self.direction = 'backward'

    @property
    def dates(self):
        '''
            gives the date range
            direction of date generations is given by the sign of step
        '''
        dates = []

        # backward generation
        if self.direction == 'backward':
            cursor = self.start
            while cursor > self.stop:
                dates.append(cursor)
                # we use plus sign because step<0
                cursor += self.step
            dates.append(self.start)
        else:
            # foward generation
            cursor = self.start
            while cursor < self.stop:
                dates.append(cursor)
                cursor += self.step
            dates.append(self.stop)

        return sorted(dates)

# default stub is FRONT short
# old stuff we didn't add back:
#         stub="short",
#         ret="l",
#         monthEndRule="anniv",
#         ie="[)",
#         dc=NotImplementedError,
