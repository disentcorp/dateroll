# `dateroll` docs

[ddh]() | [Date]() | [Duration]() | [Schedule]() | [Calendars]() | [CalendarMath]() | [Parser]()


## ddh

Date duration helper `function` that takes a string and returns either a `Date`, `Duration`, or `Schedule`. See [Parser]() section for valid string formats

##### Usage

 ```python
 from dateroll import ddh
ddh(some_stirng)
```

##### Examples

|[*DateRollString*]()|In|Out|
|-|-|-|
|[*TodayString*        ]()|`ddh('t')`|`Date(2024,2,2)`|
|[*DateString*         ]()|`ddh('12/31/22')`|`Date(2022,12,31)`|
|[*DurationString*     ]()|`ddh('+3m')`|`Duration(m=3)`|
|[*DateMathString*     ]()|`ddh('t + 1y')`|`Date(2025,2,2)`|
|[*DateScheduleString* ]()|`ddh('t, t+5y, 1m')`|`[Date(2022,2,2),`...`]`|

<br>

## Date

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


## Duration

Duration `class` herits from `dateutil.relativedelta` for defining intervals (periods) of time.

Adds business day handling.



#### Usage
```python
>>> from dateroll import Date
>>> Duration(years=1,months=3)
Duration(years=1,months=3)
```
##### Constructor examples (#'s are `int`egers.)
`n` is a postive or negative `int`

|Description                |Kwargs|Example|
|-                          |-      |-            |
|Years                      |`years` `year` `y`|`Duration(y=n)`|
|Quarters ($\to$ 3m)            |`qtrs` `qtr` `q`|`Duration(q=n)`|
|Weeks ($\to$ 7d)               |`weeks` `week` `w`|`Duration(w=n)`|
|Calendar days              |`days` `cd` `d`|`Duration(d=-n)`|
|Calendar days w/ roll      |`roll=roll`¹|`Duration(d=n,roll="F")`|
|Business days              |`bd`|`Duration(bd=-n)`|
|Business days w/ calendar  |`bd` `cals=calendar`²|`Duration(bd=-1, cals="FED")`|
|Combinations|`y` `m` `bd` `cals`|`Duration(y=1, m=3, bd=-1, cals="FED")`|

¹`roll` can one be following business day (`"F"`), preceding business day (`"P"`) or the equivalent modified conventions: modified following (`"MF"`), or modified previous (`"MP"`). 

²`calendar` can be of the form: `"NY"`, `["NY"]`, `"NYuLN"`, or `["NY","LN"]` (see [`Parser`]() for more details.).

<br>

##### Properties/Methods
|Name|In|Out|
|-|-|-|
|.years
|.months
|.days
|.bds
|.anchor_start
|.anchor_stop
|.num_days
|.num_weeks
|.num_quarters
|.num_years(`counter`)

`counter` is one of `"ACT/360"`, `"30/360"`, ...


##### Operations

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

## Schedule

## Calendars

## Calendar math

## Parser