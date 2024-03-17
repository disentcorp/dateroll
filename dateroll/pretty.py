import datetime
import calendar
import code

from dateroll.settings import settings

calendar.setfirstweekday(calendar.SUNDAY)

from dateroll.utils import color

def replacer(i,c,txt1,cals):
    bef = str(i).rjust(3)
    aft = color(bef,c)
    txt2 = txt1.replace(bef,aft)   
    return txt2

def pretty_between_two_dates(dt1,dt2,cals,calmath):
    '''
    experimental feature

    print a calendar or calenders for set of debugging:
        if start and end date fall in same month show calendar for month
        if standard and end date fall in two different months show calendars for starting month and ending month

        color skipped days as cyan
        color start/end days as blue
        color holidays/weekends as grey
    '''
    if dt2>dt1:
        _1,_2 = dt1,dt2
    else:
        _1,_2 = dt2,dt1

    print('from',_1,'to',_2, 'cals',cals)
    
    y1,m1,d1 = _1.year,_1.month,_1.day
    y2,m2,d2 = _2.year,_2.month,_2.day

    c1 = calendar.month(y1,m1)
    c1s = str(c1).splitlines()
    c1s[-1]=c1s[-1].ljust(len(c1s[-2]))
    cal1 = '\n'.join([' '+i[:] for i in c1s][1:])
    
    if m1==m2 and y1==y2:
        # 1 month cal mode       
        for i in range(0,32):
            try:
                _ = datetime.date(year=y1,month=m1,day=i)
                ishol = not calmath.is_bd(_,cals)
            except:
                ishol = False

            if i==d1 or i==d2:
                cal1 = replacer(i, 'blue', cal1, cals)
            elif ishol:
                cal1 = replacer(i, 'gray', cal1, cals)
            elif i>d1 and i<d2:
                cal1 = replacer(i, 'cyan', cal1, cals)


        res = color(f'        {_1.strftime('%b')} {y1}','yellow')
        for idx, (i, j) in enumerate(zip(cal1.splitlines(),cal1.splitlines())):
            if idx>0:
                res += '\n'+ f'  {i} '

    else:
        # 2 month cal mode
        for i in range(0,32):
            try:
                _ = datetime.date(year=y1,month=m1,day=i)
                ishol = not calmath.is_bd(_,cals)
            except:
                ishol = False
            if i==d1:
                cal1 = replacer(i,'blue',cal1,cals)
            elif i >= d1 and not ishol:
                cal1 = replacer(i,'cyan',cal1,cals)
            elif ishol:
                cal1 = replacer(i,'gray',cal1,cals)


        c2 = calendar.month(y2,m2)
        cal2 = '\n'.join([' '+i for i in str(c2).splitlines()][1:])        
        for i in range(0,32):
            try:
                _ = datetime.date(year=y1,month=m1,day=i)
                ishol = not calmath.is_bd(_,cals)
            except:
                ishol = False
            if i==d2:
                cal2 = replacer(i,'blue',cal2,cals)
            elif i<=d2 and not ishol:
                cal2 = replacer(i,'cyan',cal2,cals)
            elif ishol:
                cal2 = replacer(i,'gray',cal2,cals)

        res = color(f'        {_1.strftime('%b')} {y1}                 {_2.strftime('%b')} {y2}                ','yellow')
        for idx, (i, j) in enumerate(zip(cal1.splitlines(),cal2.splitlines())):
            res += '\n' + f'  {i}  {''+j}'
            prev = len(i)

    return res
