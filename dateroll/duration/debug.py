import datetime
import calendar
import code

calendar.setfirstweekday(calendar.SUNDAY)

from dateroll.utils import color

def before_after(dt1,dt2,cals):
    ...
    # print(dt1,dt2)
    # ym1 = dt1.year,dt1.month
    # ym2 = dt2.year,dt2.month

    if ym1==ym2:
        cal = str(calendar.month(*ym1,w=0))

    d1, d2 = str(dt1.day), str(dt2.day)

    header = '\n'.join(cal.splitlines()[:2])
    body = '\n'.join(cal.splitlines()[2:])

    # days = (dt2.date - dt1.date).days
    
    if dt2>dt1:
        a,b = dt1.date,dt2.date
        arrow = '>'
    else:
        a,b = dt2.date,dt1.date
        arrow = '<'

    # t = a+datetime.timedelta(days=1)

    t = datetime.date(dt1.year,dt1.month,1)
    while t.month==dt1.month and t.year==dt1.year:
        d = str(t.day)
        if len(d)==1:
            d =d.rjust(3)
        i =  t-datetime.timedelta(days=1)
        j =  t+datetime.timedelta(days=1)
        s1 = f'{str(i.day).rjust(2)} {d}'
        s2 = f'{str(j.day).rjust(2)} {d}'
        ii = s1; ii = ii.replace(' ',arrow)
        jj = s2; jj = jj.replace(' ',arrow)
        if t > a and t < b:
            body = body.replace(s1,ii)
            body = body.replace(s2,jj)
        t+=datetime.timedelta(days=1)


    # body = body.replace(str(d1),color(d1,'blue'))
    # body = body.replace(str(d2),color(d2,'blue'))

    # cal = header +'\n' + body
    
    # print(cal)


#     a,b 

#     same month:
#     1 month with colors

#     2 months next ot eachother
#     2 months with colors

#     diff year

#     list of years with colors
#     a month, and b month with colors

# show only the months tht could have a bad interpretation and a good interpeation, form 1 to n 

# weekends greyeed out

# holidays in separate clendar per color

# start and end days in somethign obivous - bold and underline