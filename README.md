*NOTE: all examples are illustrated and not yet validated for the purpose of creating the documentation; TO DO Verification of examples using actual library against excel + real calendars.*

![disent](https://i.imgur.com/vGHWsdE.png)

# Date Math (by Disent)
The purpose of the Disent Date Math Library is to extend the native date manipulation capabilities in the python standard libraries to be compatible with the range of date manipulations required in [fixed income mathematics](https://www.amazon.com/Fixed-Income-Mathematics-Analytical-Statistical/dp/007146073X).

If interested we highly recommend reading up on [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) the international standard for representing dates.

## Quick start guide

```python
 from disentpy.dates import ddh 
 # ddh() is the Disent date helper function
```
The helper function, ddh(), allows for many operations without having to use the underlying classes and methods explicitly.

```python
>>> # plain date
>>> ddh("7/2/84")
Date("02-Jul-1984")

```

Adding and subtracting periods from dates

```python
>>> # add period to date
>>> ddh("7/2/84") + "+3m"
Date("02-Oct-1984")
>>> # subtract period from date
>>> ddh("7/2/84 - 1d")
Date("01-Jul-1984")
>>> # add business days (skip weekend days)
>>> ddh("1/8/2015 + 2bd")
Date("12-Jan-2015")
>>> # add days
>>> ddh("1/8/2015 + 2d")
Date("10-Jan-2015")
```

Subtract dates
```python
>>> ddh("5/15/25 - 7/13/22")
Period("2y10m2d")
>>> ddh("5/15/25 - 7/13/22").cd()
1037
>>> ddh("5/15/25 - 7/13/22").bd()
742
>>> ddh("5/15/25 - 7/13/22").bd("NY")
714
>>> ddh("5/15/25 - 7/13/22").bd("NYuBR")
704
>>> ddh("5/15/25 - 7/13/22").bd("NY",ie="[]")
715
>>> dt2 = ddh('1/1/15')
>>> dt1 = ddh('1/7/13')
>>> (dt2 - dt1).bd('NYuEU)
Date('DD-MMM-YYYY')
```

Monthly schedule for 5 years from today, starting backwards:
```python
> ddh("t,t+5y,-1m",ret='df') # returns a Pandas dataframe!
per          bgn          end  dur  stub
60   12-Sep-2027  12-Oct-2027  30d  full
59   12-Aug-2027  12-Sep-2027  31d  full
...  ...          ...          ...   ...
2    12-Nov-2022  12-Dec-2022  30d  full
1    12-Oct-2022  12-Nov-2022  31d  full

[60 rows x 4 columns]
```


## Concepts

There are 3 conceptual objects used in date mathematics. Namely a **`date`**, a **`duration`**, and a **`schedule`**. 

###  Date
You guessed, the basic object in date math is..., well, a date. A date is a **point in time** referenced by a **`year`**, a **`month`**, and a **`day`** and can be represented as a string of characters in various formats. From a date one can extrapolate `day of the week`, `day of the month`, `week number`, and other details.

### Period

A portion, period or **length of time** represented by a **`number`** and a **`unit`**. Example date period: 3 months. Valid date period units are **`day`** or **`calendar day`**, **`business day`**, **`month`**, **`quarter`**, or **`year`**. Periods are not tied in anyway to a specific point in time. Date math operations typically look at the whole (24hour) day as the base unit, and we can ignore sub-units of day for now.

#### Term and Tenor
A derivative of **`Period`** called a term (or tenor) occurs when the duration is anchored to a particular **point in time**, for example `today's date`. This is commonly known as a Term or a Tenor. A typical set of tenors used could be: $\{$`1m`,`3m`,`6m`,`1y`,`100y`$\}$. When the language term/tenor is used, `today's date` is implicitly the anchor point for the beginning of the duration.

##### Equal but unequal

Question: Is `28d` the same as `1m`? What about `90d`= `1q`? or `366d`=`1y`?

Equality of tenors is complicated for a duration, but concrete for a Tenor. The anchoring of the Tenor to a date, allows for the actual days in the period to be counted and equated precisely.

If there is no anchor date, as in duration, then `28d`, `29d`, `30d`, or `31d` *could* be considered `1m`, or a little longer, or a little shorter. E.g. `31d` is `1m1d` if the anchor point for the duration is April 1st, as April always has length of $||30\text{d}||$.

### Schedule

Schedules are **ordered, contiguous, blocks of time** (a.k.a. **`list of durations`**).  A classic example of a schedule would be for modeling the dates of a loan.

#### Example Schedule for a 3-month loan, paid monthly

|per|bgn|end|dur|stub|
|-|-|-|-|-|
|1|`15-Jan-2022`|`15-Feb-2022`|`31d`|`full`|
|2|`15-Feb-2022`|`15-Mar-2022`|`28d`|`full`|
|3|`15-Mar-2022`|`15-Apr-2022`|`31d`|`full`|

- `per` for Period numbers starting with 1
- `bgn` for the start (beginning) date of the period
- `end` for the start date of the period
- `dur` for the duration of the period (in days)
- `stub` for the type of period (either `full`, `short`, or `long`)

Fixed income schedules are driven by a set of rules: Partition a `start date` to `end date` by periods of `duration` in length. Specific considerations are made for complex `month-end rules`, `stub` (a.k.a. stubs). See API details for more information.

### Stubs
When a schedule is created, it is possible that the blocks of time are unequal* in length relative to the primary duration.

Example: Let's do a `+6m` schedule for `2y1q`. You will have an incomplete period because `2y1q` is not evenly divisible by `6m`. This means there is `1q` of leftover days to attribute to the schedule. 

One option is that the days can be tacked on the front (or the back) of the schedule as a "shorter" period, known as a **`stub`**, hence `stub="short"`. Alternatively, the stub days can be included in either the first or the last period to lengthen the period longer than the duration used to generate the schedule originally, known as a **`long coupon`** or here we denote as `stub="long"`. `stub="full"` is for a full period with no adjustment for the sake of completeness.

Examples: `15-Feb-2022`, `1y1q` by `6m`:

#### Short stub, last period
|per|bgn|end|dur|stub|
|-|-|-|-|-|
|1|`15-Jan-2022`|`15-Jul-2022`|`181d`|`full`|
|2|`15-Jul-2022`|`15-Jan-2023`|`184d`|`full`|
|3|`15-Jan-2023`|`15-Mar-2023`|`90d`|`short`|

**This can occur for a number of reasons, perhaps the loan was terminated early, and pro-rata payments must be computed.

==tbd== More examples for short up front, long up front, long at end

### Lists
An auxiliary concept is the **`list`** or lists of either dates, durations, or schedules.
 1. List of **`dates`**
	 - Useful for a variety or purposes (filtering on specific dates, or custom dates that do not follow any particular set of rules. It is a base construct used in creating schedules.
 3. List of **`durations`**
	 - This is synonymous with **`schedule `**.
 4. List of **`schedules`**

## Operations

### Addition

A date and a duration can be added together to form a new date.

`date` + `duration`= `new date`
`7/2/1984` + `38y` = `7/2/2022`

#### Date rolling
Additional rules can be applied when a date rolls past a certain milestone (end of month, end of quarter, or end of year), and or lands on a non-working day (weekend or holiday). Typical methods:

 - Following (roll forward a business day)
 - Modified Following (if rolls into next month, roll back a business day)

### Subtraction

Subtracting two dates is how days are counted in a particular period of a schedule, or a period may be subtracted from a date to form a new date.

#### Subtract a duration from a date
  `date1` - `duration`=`date2`
  `10/10/2022` - `2y` = `10/10/2020`
 
 ##### Date rolling
When subtractining a duration, date rolling rules apply in reverse:
 - Previous business day(roll backwardsalways)
 - Modified Previous (if rolls into previous month, roll forward a business day)

#### Day counting
`date2` - `date1`= `duration`
`10/10/2022` - `07/2/1984` = `38y3m18d` or `13,979d`

Day counting is a complex topic in itself, see [wikipedia](https://en.wikipedia.org/wiki/Day_count_convention#30E/360) article.

Main concepts are:

 1. **Inclusion/exclusion rules**: whether to count the first or last date:
$$[d1,d2), [d1,d2], (d1,d2), \text{or}\ (d1,d2)$$

 2. **Market-specific day counting methods (for accrual calcs)**:
	- 30/360, ACT/360, ACT/365, and others

3. **Non-working days**:
	- Do you skip weekends? 
	- What about holidays? which holidays are required? Is there more than one calendar to be considered? 

		Suppose you need to adjust a date based on a payment that can only occur on a working day in both New York and London. We can represent a list of all weekends as `WE`, we can represent all New York holidays as `NY`, and London holidays as `LN`. Mathematicaly we can represent this as the following:
	
$$ d2 = d1+0bd|\text{WE}\cup \text{NY}\cup\text{LN}$$

# Python API

## Import Library

```python
from disentpy.dates import Date, Period, Schedule
from disentpy.dates import disent_date_helper, ddh, disent_list_dates_helper
```

## Date

```python 
Date(date_string)
Date(year,month,day) # any valid datetime.datetime constructor
Date(datetime.datetime)
```
Date_string is of type `str`, or year/month/day are of type `int`. Any python `datetime.datetime` constructor is valid.
```python
>>> # date string method
>>> Date('1/1/15')
Date('01-Jan-2015')
>>> Date('2015-03-04')
Date('04-Mar-2015')
>>> Date('9/5/29')
Date('05-Sept-1929')
>>> # datetime.datetime like constructor
>>> Date(1984,7,2)
Date('02-Jul-1984')
>>># datetime.datetime's 
>>> dte = datetime.datetime(1992,2,5)
>>> Date(dte)
Date('05-Feb-1992')
```
Suppose you enter days in european format (day preceeds month)?
```python
> Date('25/5/15',dmy=True)  # Alternatively ,ymd=True|False
Date('25-May-2015')
```
Default behavior can be specified as a setting (TBD).

We support numerous permutations like MM/DD/YY, M/D/Y, YYYYMMDD, with slashes or dashes, and more...if there's something we don't do that you want, let us know. 

If 1 or two digit year is provided: 0-71 are 2000 to 2071, and 72 to 99 are 2072 to 2099. This differs from excel which uses 2029 as the divider. A global setting can be provided. Use cause when import two digit years around these cutoffs.


## Period

```python 
Period(duration_string)
```

Period_string is of type `str`. The string can be composed as follows:

Minimum string:
" `[NUMBER OF UNITS]` `[UNIT]`"

e.g. "3d". Number of units is a signed number. Units:

|Unit|Description|
|-|-|
|`d` or `cd`|Calendar day|
|`bd`|Business day|
|`m`|Month|
|`q`|Quarter|
|`y`|Year|


 can be d,cd,bd,m,q or y: day, calendar day (same as day), business day, month, quarter, or year. If no sign on the number sign is assumed to be positive (e.g. "3d" and "+3d" are the same, but different than "-3d").

" `[NUMBER OF UNITS]` `[UNIT]` | `[CALENDAR]`"

If units are `bd` (business days) you can supply a calendar from the available calendars. For list of calendars and calendar management a supplemental document will be provided. (TBD). Canvas Professional users will be able to integrate their own calendars.

Note: if bd is used for the `unit` and no calendar is specified, a system default calendar `WE` will be used which is the weekend calendar that defines all Saturdays and Sundays as non-working days (synonymous with holidays) by which to skip over. Example calendars:

|2-letter code|Description|
|-|-|
|WE|Saturdays and Sundays|
|NY|All WE and New York banking holidays|
|EU|All WE and ECB banking holidays|
|BR|All WE and Brazilian banking holidays|

" `[NUMBER OF UNITS]` `[UNIT]` | `[CALENDAR1]` u `[CALENDAR2]`"

Calendars can be unioned together by separating calendar two letter codes with a `u` character. You can union up to 5 calendars, if there's a need for more, just ask.

Examples: "-2d|NYuLN" for a LIBOR fixing. "+1BD|NYuBR" for an FX settlement.

" `[NUMBER OF UNITS]` `[UNIT]` | `[CALENDAR]` / `[ROLL CONVENTION]` "

Option roll convention for business date adjustment:

|Roll convention|Name|Description|
|-|-|-|
|`/F`|Following|Next business day (default if rolling forward)
|`/MF`|Modified following|Next business day unless rolls into next month, in which case the last business day of the current month is used.
|`/P`|Previous|Previous business day (default if rolling backwards)
|`/MP`|Modified previous|Previous business day unless it rolls into the prior month, in which case the first business day of the current month is used.

### Period Examples

```python
>>> Period('5d')
Period("5d")
>>> Period('5bd')
Period("5bd")
>>> Period('5bd|NY')
Period("5bd|NY")
>>> Period('-2d')
Period("-2d")
>>> Period('-1m')
Period("-1m")
>>> Period('-1q')
Period("-1q")
>>> Period('-5y')
Period("-5y")
>>> Period('-2bd|NY/MP')
Period("-5y")
```

## Schedule

==tbd==

## Helpers

### disent_date_helper` (or ddh)

==tbd==
###  disent_list_dates_helper`
==tbd==

## Operations

==tbd==
### Addition
==tbd==

### Subtraction
==tbd==

# More examples


T+3 payment adjustment rule (can't pay on NY or LN holiday, nor a Sat/Sun:
```python
> ddh('+3bd|NYuLN") 
ddh('+3bd|NYuLN")
> today() + ddh('+3bd|NYuLN")
Date('14-Oct-2022')

```
Monthly schedule for 5 years from today, starting backwards:
```python
> ddh("t,t+5y,-1m,df") # returns a dataframe!
per          bgn          end  dur  stub
1    12-Oct-2022  12-Nov-2022  31d  full
2    12-Nov-2022  12-Dec-2022  30d  full
...  ...          ...          ...   ...
59   12-Aug-2027  12-Sep-2027  31d  full
60   12-Sep-2027  12-Oct-2027  30d  full

[60 rows x 4 columns]
```
Return kwarg `ret` can be either `l` (list of Date), `ll` (List of list of Date, e.g. begining and end of period),`df` (pd.DataFrame**) or `lp` (list of periods (durations).

*pd.Dataframe has 4 columns for start date, end date, duration in days, and type of period (full, short, or long)*

Perhaps you just want to get a list of days to use as a filter somewhere (let's use `ret="l"`):
```python
> today()
Date('11-Oct-2022')
> ddh("t-3y,t-1d,1d",ret='l')
Date(['11-Oct-2019','12-Oct-2019',...,'10-Oct-2022'])  #95 items
```

##  Package Comparison
Comparison of classes in commonly available python standard libraries and 3rd party libraries:

|disentpy.dates|Python Std Lib|Pandas|Numpy|
|-|-|-|-|
|`Date`|datetime.datetime or datetime.date|pd.Timestamp|np.datetime64|
|`Period`|dateutil.relativedelta or datetime.timedelta|offsets, DateOffset|np.timedelta64|
|`Schedule`|dateutil.rrule|date_range or bdate_range or period_range or timedelta_range|n/a|

- `disent_date_helper` (or ddh)
- `disent_list_dates_helper`


#### TBD

*What about year to date or month to date?*

Date().ytd() --> Period
Date().mtd() --> Period