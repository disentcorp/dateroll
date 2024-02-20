# dateroll

why1? date math will be trivial like floats, even with holidays

why2? market conventions for global fixed income isn't written down in one spot.


### The `types`

in `dateroll`|python native|
|-|-|
|`dateroll.Date`|`datetime.date`<br>`datetime.datetime`
|`dateroll.Duration`|`datetime.timedelta`<br>`dateutil.relativedelta.relativedelta`
|`dateroll.Dates`|`dateutil.rrule.rrule`
|`dateroll.Durations`|

## ddh

`ddh` (date-duration-helper) is your 🪄 magic wand for 📅 dates

### parsing examples 🔥
|activity|input|output|
|-|-|-|
a date|`ddh('t')`*<br>`ddh('2/15/24')`<br>`ddh('2024-02-15')`|`2024,2,19`<br>`Date(2024,2,15)`<br>`Date(2024,2,15)`
a duration|`ddh('+3m')`<br>`ddh('+1bd\|WE')`|`Period(m=3)`<br>`Period(bd=1,cal='WE')`
dates|`ddh('t,t+1y,1m')`|`Dates(['2/19/24','3/19/24',...]])`
durations|`ddh('1m,3m,6m')`<br>`ddh('1y')*5`|`Durations(['1m','3m','6m'])`<br>`Durations([1y','2y','3y',...])`
mixing it up|`ddh('t') + ddh('3m')*4`|`Dates(['2/19/24','5/19/24',...])`

*`t` is `today()`

### let's add

|left side|operation|right side|output
|-|-|-|-|
|`Date`|$+$|`Duration`|`Date`
|`Duration`|$+$|`Duration`|`Duration`
|`Date`|$+$|`Durations`|`Dates`

```python
>>> d = ddh('2/16/22') # a friday before presidents day
>>> d + '1bd|NY'# see calendars section later
Date(2022,2,20)
```

### let's subtract

|left side|operation|right side|output
|-|-|-|-|
|`Date`|$-$|`Date`|`Duration`
|`Date`|$-$|`Duration`|`Date`

```python
>>> t1 = ddh('1/5/24')
>>> t2 = ddh('2/6/24')
>>> t2-t1
Duration(start='1/5/24',stop='2/5/24')
>>> (t2-t1).exact
Duration(d=32)
>>> (t2-t1).approx
Duration(m=1)
>>> (t2-t1).ncd # [n]umber of [c]alender [d]ays
Duration(d=32)
>>> (t2-t1).bd # [b]usiness [d]ays, assumes WE calendar
Duration

```
```python
>>> t = ddh('t')  # 1/29/24
>>> t - '1m'
Date(2024,1,19)
```


### let's multiple







Thing can be: 
- `datetime` $\to$ `Date`
- `date` $\to$ `Date`
- `Date` $\to$ `Date`
- `timedelta` $\to$ `Duration`
- `relativedelta` $\to$ `Duration`
- `Duration` $\to$ `Duration`
- `rrule` $\to$ `Schedule`
- `Schedule` $\to$ `Schedule`
- `Pillars` $\to$ `Pillars`
- `str` $\to$ `Date`
  - `str` parses directly to date
  - `str` $\to$ add(`Date`,`Duration`)
- `str` $\to$ `Duration`
  - 
- `str` $\to$ `Schedule`
- `list(Date)` $\to$  `Schedule`
- `list(Duration)` $\to$  `Pillars`

What kind of `str`?
- `str` $\to$ `Date`



### dateroll.Date
Date class

```python
dateroll.Date(datetime.date(2024,1,1))
dateroll.Date(datetime.datetime(2024,1,1))
dateroll.Date('1/1/24') # users dateutil.parser.parse
```



### dateroll.Duration
Duration class

### dateroll.Schedule
Schedule class

Date takes datetime or date
Period takes Rd,Td

Date.parse_str(s:str)
Period.parse_Str(s:str)

schedule only dates Date,Duration,Period

ddh(lots of things)
all permute back to base types