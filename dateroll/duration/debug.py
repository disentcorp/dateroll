import datetime
import calendar
import code

from dateroll.settings import settings

calendar.setfirstweekday(calendar.SUNDAY)

from dateroll.utils import color

def body(i,c,txt1,cals):
    bef = str(i).rjust(3)
    aft = color(bef,c)
    txt2 = txt1.replace(bef,aft)   
    return txt2

def before_after(dt1,dt2,cals,calmath):
    if dt2>dt1:
        _1,_2 = dt1,dt2
    else:
        _1,_2 = dt2,dt1
    
    y1,m1,d1 = _1.year,_1.month,_1.day
    y2,m2,d2 = _2.year,_2.month,_2.day

    c1 = calendar.month(y1,m1)
    cal1 = '\n'.join([' '+i[:] for i in  str(c1).splitlines()][1:])
    
    if m1==m2 and y1==y2:
        # 1 month cal mode       
        for i in range(0,32):
            try:
                _ = datetime.date(year=y1,month=m1,day=i)
                ishol = not calmath.is_bd(_,cals)
            except:
                ishol = False

            if i==d1 or i==d2:
                cal1 = body(i, 'blue', cal1, cals)
            elif ishol:
                cal1 = body(i, 'gray', cal1, cals)
            elif i>d1 and i<d2:
                cal1 = body(i, 'cyan', cal1, cals)


        print(color(f'        {dt1.strftime('%b')} {y1}','yellow'))
        for idx, (i, j) in enumerate(zip(cal1.splitlines(),cal1.splitlines())):
            if idx>0:
                print(f'  {i} ')

    else:
        # 2 month cal mode
        c2 = calendar.month(y2,m2)

        c2s = str(c2).splitlines()
        c2s[-1]=c2s[-1].ljust(len(c2s[4]))
        cal2 = '\n'.join([' '+i for i in c2s][1:])        
        for i in range(0,32):
            try:
                _ = datetime.date(year=y1,month=m1,day=i)
                ishol = not calmath.is_bd(_,cals)
            except:
                ishol = False
            if i==d2:
                cal1 = body(i,'blue',cal1,cals)
            elif i >= d2 and not ishol:
                cal1 = body(i,'cyan',cal1,cals)
            elif ishol:
                cal1 = body(i,'gray',cal1,cals)

        for i in range(0,32):
            try:
                _ = datetime.date(year=y1,month=m1,day=i)
                ishol = not calmath.is_bd(_,cals)
            except:
                ishol = False
            if i==d2:
                cal2 = body(i,'blue',cal2,cals)
            elif i<=d2 and not ishol:
                cal2 = body(i,'cyan',cal2,cals)
            elif ishol:
                cal2 = body(i,'gray',cal2,cals)

        print(color(f'        {dt1.strftime('%b')} {y1}                 {dt2.strftime('%b')} {y2}                ','yellow'))
        prev = 0
        for idx, (i, j) in enumerate(zip(cal1.splitlines(),cal2.splitlines())):
            if idx==5:
                j = '   ' + j
            print(f'  {i}  {''+j}')
            prev = len(i)
