
class Schedule: 
    # TODO tempo
    
    def __init__(self,start,stop,step):
        self.start = start
        self.stop = stop
        self.step = step

    def range(self):
        '''
            gives the date range, ie=[]
        '''
        dts = [self.start]
        dt = dts[0]
        while dt<self.stop:
            dt+=self.step
            dts.append(dt)
        return dts

# old stuff we didn't add back:
#         stub="short",
#         ret="l",
#         monthEndRule="anniv",
#         ie="[)",
#         dc=NotImplementedError,
