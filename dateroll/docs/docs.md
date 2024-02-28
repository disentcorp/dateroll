<style>
.outer {
    font-family: helvetica; 
    padding-left: 12%;
    padding-right: 12%;
}
a {
    color: blue !important;
    text-decoration: underline !important;
}
table {
  border-collapse: collapse !important;
}
table td, table th {
  border: 0px !important;
  border-left: 1px dotted rgb(230,230,230) !important;
  border-right: 1px dashed rgb(230,230,230) !important;
  border-top: 1px solid black !important;
  border-bottom: 1px solid black !important;
  padding-top:7px !important;
  padding-bottom:7px !important;
}
table tr:first-child th {
  border-top: 4px solid black !important;
  border-bottom: 4px solid black !important;
}
table tr:last-child td {
  border-bottom: 0 !important;
  border-bottom: 4px solid black !important;
}
table tr td:first-child,
table tr th:first-child {
  border-left: 0 !important;
}
table tr td:last-child,
table tr th:last-child {
  border-right: 0 !important;
}

</style>

<div class="outer">

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

# reference guide

## ddh <a name="ddh"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

Date duration helper `function` that takes a string and returns either a `Date`, `Duration`, or `Schedule`. See [Parser]() section for valid string formats

##### Usage

 ```python
 from dateroll import ddh
ddh(some_string)
```

##### Examples

|`some_string` "flavor"|In|Out|
|-|-|-|
|[Today string        ]()|`ddh('t')`|`Date(2024,2,2)`|
|[Date string         ]()|`ddh('12/31/22')`|`Date(2022,12,31)`|
|[Duration string     ]()|`ddh('+3m')`|`Duration(m=3)`|
|[Date math string     ]()|`ddh('t + 1y')`|`Date(2025,2,2)`|
|[Date schedule string ]()|`ddh('t, t+5y, 1m')`|`[Date(2022,2,2),`...`]`|

<br>

## Date <a name="Date"></a>
[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

Date `class` inherits `datetime.date`.

Adds business day handling, calendar math, and schedule generation when combined with `ddh`, `Duration` and `Schedule`.



#### Usage
```python
>>> from dateroll import Date
>>> Date(1984, 7 ,2)
Date(year, month, day)
```
##### Constructor example
`Date(2024, 7, 2)` 
<br>
*^3 integer args: year, month, and day

##### Properties/Methods
|Name|In|Out|
|-|-|-|
|`.datetime`            | `Date(2024,7,2).datetime` | `datetime.datetime(2024, 7, 2, 0, 0)`|
|`.date`                | `Date(2024,7,2).date` | `datetime.date(2024, 7, 2, 0, 0)`|
|`.iso`                 | `Date(2024,7,2).iso`| `20240702`|
|`.xls`                 | `Date(2024,7,2).xls`| `45475`|
|`.unix`                | `Date(2024,7,2).unix`| `1719892800`|
|`.dotw`                | `Date(2024,7,2).dotw`| `"Tue"`|
|`.wotm`                | `Date(2024,7,2).wotm`| `1`|
|`.woty`                | `Date(2024,7,2).woty`| `27`|                                                    |
|`.is_bd(calendar)`¹    | `Date(2024,7,2).is_bd("NY")`|`False`|
|`datetime.date.*`|see [datetime](https://docs.python.org/3/library/datetime.html#datetime.date)|see [datetime](https://docs.python.org/3/library/datetime.html#datetime.date)

¹`calendar` can be of the form: `"NY"`, `["NY"]`, `"NYuLN"`, or `["NY","LN"]` (see [`Parser`]() for more details.).


##### Operations

assume ```d = Date(2000,1,1)```

##### `Date` $+$/$-$ `Duration` or `Date`

|LHS|Operator|RHS|Result|In|Out|
|-|-|-|-|-|-|
|`Date`|$+$|`Duration`  |`Date`     |`d + Duration(m=1)`|`Date(2000,2,1)`|
|`Date`|$-$|`Duration`  |`Date`     |`d - Duration(y=1)`|`Date(1999,1,1)`|
|`Date`|$-$|`Date`      |`Duration` |`d - Date(1998,1,1)`|`Duration(d=730)`|


##### `Date` $+$/$-$ `int` (for calendar days)
|LHS|Operator|RHS|Result|In|Out|
|-|-|-|-|-|-|
|`Date`|$+$|`int`      |`Duration` |`d + 5`|`Date(2000,1,6)`|
|`Date`|$-$|`int`      |`Duration` |`d - 1`|`Date(1999,12,31)`|

##### `Date` $+$/$-$ *DateString* or *DurationString*
|LHS|Operator|RHS|Result|In|Out|
|-|-|-|-|-|-|
|`Date`|$-$|*DateString*     |`Duration`|`d - "1/1/98"`|`Duration(d=730)`|
|`Date`|$+$|*DurationString* |`Date`    |`d + "1m"`|`Date(2000,2,1)`|
|`Date`|$-$|*DurationString* |`Date`    |`d - "1y"`|`Date(1999,1,1)`|


## Duration <a name="Duration"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)


Duration `class` herits from `dateutil.relativedelta` for defining intervals (periods) of time.

Adds business day handling.


#### Usage
```python
>>> from dateroll import Date
>>> Duration(years=1,months=3)
Duration(years=1,months=3)
```
#### Constructor examples (#'s are `int`egers.)
`n` is a postive or negative `int`

|Description                |Kwargs|Example|
|-                          |-      |-            |
|Years                      |`years` `year` `y`|`Duration(y=n)`|
|Quarters ($\to$ 3m)        |`qtrs` `qtr` `q`|`Duration(q=n)`|
|Weeks ($\to$ 7d)           |`weeks` `week` `w`|`Duration(w=n)`|
|Calendar days              |`days` `cd` `d`|`Duration(d=-n)`|
|Calendar days w/ roll      |`roll=roll`¹|`Duration(d=n,roll="F")`|
|Business days              |`bd`|`Duration(bd=-n)`|
|Business days w/ calendar  |`bd` `cals=calendar`²|`Duration(bd=-1, cals="FED")`|
|Combinations|`y` `m` `bd` `cals`|`Duration(y=1, m=3, bd=-1, cals="FED")`|

¹`roll` can one be following business day (`"F"`), preceding business day (`"P"`) or the equivalent modified conventions: modified following (`"MF"`), or modified previous (`"MP"`). 

²`calendar` can be of the form: `"NY"`, `["NY"]`, `"NYuLN"`, or `["NY","LN"]` (see [`Parser`]() for more details.).

Optional `kwargs` for either `anchor_start=Date(...)` or `anchor_stop=Date(...)` can be user-supplied. These are automatically inherited when `Duration` is the result of some math involving a `Date`.
<br>

#### Properties/Methods
|Name                       |In                     |Out        |
|-                          |-                      |-          | 
|`.years               `      |`Duration(y=5,m=4,d=3,bd=2)`    |`5`        |
|`.months              `      |`Duration(y=5,m=4,d=3,bd=2)`    |`4`        |
|`.days                `      |`Duration(y=5,m=4,d=3,bd=2)`    |`3`        |
|`.bds                 `      |`Duration(y=5,m=4,d=3,bd=2)`    |`2`        |
|`.anchor_start        `      |`ddh('7/7/2000-7/5/2000')`      |`Dates(2000,7,7)`   |
|`.anchor_stop         `      |`ddh('7/7/2000-7/5/2000')`      |`Dates(2000,7,5)`   |
|`.num_days()         `¹        |`Duration(y=5,m=4,d=3,bd=2)`    |~`1478`    |
|`.num_weeks()        `¹        |`Duration(y=5,m=4,d=3,bd=2)`    |~`211`     |
|`.num_quarters()     `¹        |`Duration(y=5,m=4,d=3,bd=2)`    |~`16.67`   |
|`.num_years(`counter`)`¹²    |`Duration(y=5,m=4,d=3,bd=2)`    |~`4.05`    |

¹The `num_*` methods may require period conversion based upon approximation. see [Period Conversions](#PeriodConversions).

²`counter` is one of `"ACT/360"`, `"30/360"`, ... see [day counters]()

#### Operations

assume ```dur = Duration(years=1)```

##### `Duration` $+$/$-$ `Duration`

|LHS|Operator|RHS|Result|In|Out|
|-|-|-|-|-|-|
|`Duration`|$+$|`Duration`|`Duration`|`d + Duration(m=1)`|`Duration(y=1,m=1)`|
|`Duration`|$-$|`Duration`|`Duration`|`d - Duration(m=1)`|`Duration(m=11)`|

##### `Duration` $+$/$-$ (*DateString* or *DurationString*)
|LHS|Operator|RHS|Result|In|Out|
|-|-|-|-|-|-|
|`Duration`|$+$|*DurationString* |`Date`    |`d + "1m"`|`Date(2000,2,1)`|
|`Duration`|$-$|*DurationString* |`Date`    |`d - "1y"`|`Date(1999,1,1)`|

#### Anchoring with `Date`

When a `Durationn` is the result of an operation with `Date`(s), then an anchor start or stop may get set:

Date()-Date()=Duration(anchor_start=Date(),anchor_end=date()
date + duration =

#### Period Conversions <a name="PeriodConversions"></a>

Exact always used first, then approx only if necessary. Will raise warning whenever approx is used.

|From period|Calendar Days|
|-|-|
|`1y`|$12\times$`1m`$=365.242\ 500$
|`1q`|$3\times$`1m`$=90.310\ 625$
|`1m`|$\frac{(2,800\times31)+(1,600\times30)+(303\times28)+(97*29)}{4,800}=30.436\ 875$
|`1w`|`7d`
|`1d`|`1d`
|`1bd`|$\frac{365.2425}{252¹}$

¹Commonly used in finance. If you want want `250` (or something else) let us know, we can make this a setting.

## Schedule <a name="Schedule"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

inherits from list
start
stop 
step


## Calendars <a name="Calendars"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

singleton
inherits from dict
saves to disk
user space
takes lists or schedules of dates

2-3 letter uppercase cal code per list of dates

for sample date we use a pypi library workalenndar which admits their days may be wronng
so please use at your own risk

note* we generator -100 to +100 years of holidays. our resaonsiing is that in finance nothing matters outside this window. if you have use cases outside this window, happy to talk to you.


## Calendar math <a name="CalendarMath"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

singleton caches and stores 'compiled' calendars
allows $O(1)$ bd adjustments + - , next, prev.
.size method 

unions



## Parser <a name="Parser"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

str -> thing

thing in {Date, duration, schedule}

algo

1. comma in string?
   - 0 -> either date, duration, or datemath
     - datemath is dur+d or d+dur ->d2
     - yield d2
   - 2 -> 3 parts
     - part 1 either date or datemath
       - datemath is dur+d or d+dur -> d2, yield schedule.start
     - part 2 either date or datemath
       - datemath is dur+d or d+dur ->d2 , yield schedule.stop
     - part 3 duration, yield schedule.step
     - yield schedule

ops none
properties
orig string, parts,...?

+ add operator
- substractor operator or negative in front of integer
/ indicates start of a roll conventon followed by 1 of 4 possible literals: F P MP MF
| indicates calendars, ends a set a of additive periods, followedd by 1 or more calendar codes
XX or XXX A-Z upper case 2-3 letter calendar codes
u or union operator separates two calendar codes to denote the matehmatical union of the two caalendars

show a performance table of various parsings


Caveats

- calendars are political and chang with regimes and leadership.
- the caelnndar system itself is political and chagnes with regimes adn lleadership
- we use a rule based system as opposed to a more 'accurate' astronomica lobservation based system
- our leap years concepts gets us 'close enough' to astronomical obversions withing a "human meansuable" time frame.
- current rule based system has been in place since oct ?? 1582
- mon/feb were added in ?? by the romans (cold winter months were not counnted as working days)
- approx is necessary some times, some cal math is indeterminate
- conventions are not standardized by any official global body other than 
- 

acknowledges meants

iso 8601
isda
icma
sia
reingold

python dateutil
python timedelta
python datetime
(countlless other open source dat llibraries)

for all their hardwork in making this library possible to hopefully extend their functionalities
it is our hope that fixed income and fi math can be a little less scary because the
conventions hidden behind strings just as the complexity of a computin gthe square root is hidden behind a radical sysmbol.

\- the disent team


add notebook with examples


# Appendix

#### Day counters <a name="DayCounters"></a>

==NEEDS WORK==

[nice wikipedia](https://en.wikipedia.org/wiki/Day_count_convention)

### 30/360

|Usage|Formula|
|-|-|
|`.num_years("30/360")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
|`.num_years("30/360 BB")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
|`.num_years("30/360")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
|`.num_years("30E/360")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
|`.num_years("30E/360 ISDA")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$

### ACT/<span style="color:red;">???</span>

/36?'s

|Usage|Formula|
|-|-|
|`.num_years("ACT/360")` | $\displaystyle\frac{n_d}{360}$
|`.num_years("30E/364")` | $\displaystyle\frac{n_d}{364}$
|`.num_years("ACT/365)`  | $\displaystyle\frac{n_d}{365}$
|`.num_years("ACT/365F")`| $\displaystyle\frac{n_d}{365}$
|`.num_years("ACT/365L")`| $\displaystyle\frac{n_d}{366}$

/ACT's

|Usage|Formula|
|-|-|
`.num_years("ACT/ACT AFB")` | $\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
`.num_years("ACT/ACT ICMA")` | $\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$

### BD/252

|Usage|Formula|
|-|-|
|`.num_years("BD/252")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$


### Terms
$t_2 = $`t1 = ddh(some_date_string)`
$t_1 = $`t2 = ddh(another_date_string)` $s.t.\ \  t_2 > t_1$

$t_1^y$ = `t1.years`, $t_2^y$ = `t1.years`
$t_1^m$ = `t1.months`, $t_2^m$ = `t1.months`
$t_1^d$ = `t1.days`, $t_1^d$ = `t1.days`


</div>