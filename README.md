<span style="color:red;">THIS IS PRERELEASE SOFTWARE - CREATE ISSES ON GITHUB!!!</span>

<div style="padding-left:12%;padding-right:12%;">

<p align="center">
  <img src="logo.png" style="width:250px"/>
</p>

<center>
  <span style='color:black;font-size:65pt;font-weight:bold'>date</span>
  <span style='color:black;font-size:65pt;font-weight:bold;opacity:60%;'>roll</span>
</center>

<br />

**`dateroll`** makes working with 📅 dates less painful.
<br />


## what's it for
- $+$ and $-$ dates and time periods
- 🎉 dealing with holidays
- computing 💸 payments and 🪙 accruals
- handling 🎫 stubs

<br />

# 🔥rapid start

```bash
$ pip install dateroll
$ python
```

```python
>>> from dateroll import ddh
>>> ddh("t+2bd")
```

# 🚀 use

`ddh` (**d**ate-**d**uration-**h**elper) is your 🪄 magic wand for 📅 dates.


|category|input|output|
|-|-|-|
`Date`|`ddh('t')` (*t is today*)<br>`ddh('5/5/5')`<br>`ddh('2024-02-15')`|`Date(2024,2,19)`<br>`Date(2005,5,5)`<br>`Date(2024,2,15)` 
`Duration`|`ddh('1d')`<br>`ddh('1m')`<br>`ddh('1y')`<br>`ddh('1d\|NY')`<br>`ddh('1d\|NY/MF')`<br>`ddh('1d\|NYuLN')`|`Duration(d=1)`<br>`Duration(m=1)`<br>`Duration(y=1)`<br>`Duration(d=1,cal='NY')`<br>`Duration(d=1,cal='NY', roll='MF')`<br>`Duration(d=1, cal={'NY', 'LN'}, roll='MF)`
`Schedule`|`ddh('t, 6m, 20')`<br>`ddh('t, t+5y ,6m')`|`Schedule(start='2/19/24', step='6m', n=20)`<br>`Schedule(start='2/20/24', stop='2/20/29, step='6m')`

<!-- `Schedule`|`ddh('t, 6m, 20')`<br>`ddh('t, t+5y ,6m')`<br>`ddh('1/15/24,3/30/24,1m)`|`Schedule(start='2/19/24', step='6m', n=20)`<br>`Schedule(start='2/20/24', stop='2/20/29, step='6m')`<br>`Schedule(start='1/15/24', stop='3/30/24, step='1m',stub=']')` -->
<!-- mix/match|`ddh('t') + ddh('3m')*4`|`Schedule(start='2/20/24',per='3m',n=4)` -->
<!-- `Buckets`|`ddh('1m,3m,6m')`<br>`ddh('1y')*5`|`Buckets(l=['1m','3m','6m'])`<br>`Buckets(per='1y',n=5)`
`Schedule`|`ddh('t,t+1y,1m')`<br>`ddh('t')+ddh('1m')*60`|`Schedule(start='t', stop='t+1y, step='1m')`<br>`Schedule(start='t', step='1m', n=60)` -->
<!-- weekly for first 3ms, monthly for next 6, yearly for next 5 -->


### What are the types/objects?
```python
from dateroll import Date, Duration, Schedule
```

in `dateroll`       |Example|python native equivalent|
|-                  |-|-|
|`Date`             |`ddd('7/2/84')`<br>*A date*|`datetime.date`<br>`datetime.datetime`
|`Duration`         |`ddh('1y')`, or `ddh('1m')`<br>*A Duration*|`datetime.timedelta`<br>`dateutil.relativedelta.relativedelta`
|`Schedule`         |`ddh('1/15/2024,1m,60)`<br>*Payment dates*|`dateutil.rrule.rrule`

<!-- |`Buckets`          |`['1m','3m','6m','1y']`<br>*Cash flow pillars*|n/a -->


### let's add

|left side|operation|right side|output
|-|:-:|-|-|
|`Date`|$+$|`Duration`|`Date`
|`Duration`|$+$|`Duration`|`Duration`
<!-- |`Date`|$+$|`Buckets`|`Dates` -->

```python
>>> d = ddh('2/16/22') # a friday before presidents day
>>> d + '1bd|NY'# see calendars section later
Date(2022,2,20)
>>> ddh(')
```

### let's subtract

|left side|operation|right side|output
|-|:-:|-|-|
|`Date`|$-$|`Date`|`Duration`
|`Date`|$-$|`Duration`|`Date`

```python
>>> t1 = ddh('1/5/24')
>>> t2 = ddh('2/6/24')
>>> t2-t1
Duration(start='1/5/24',stop='2/5/24')
```
|method|description|
|-|-|
`Duration.approx`|approximate largest duration|
`Duration.exact`|`Duration` of days only
`Duration.ncd`| `int` of calendar days
`Duration.nbd`| `int` of working days (if cal provided on t1)

```python
>>> (t2-t1).approx

>>> (t2-t1).exact

>>> (t2-t1).ncd # WE cal is explicit

>>> (t2-t1).ncd('NY')

>>> (t2-t1).nbd

```

Much more in the [reference docs]().

Happy rolling! 

- The Disent Team