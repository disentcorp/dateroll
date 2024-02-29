<span style="color:red;">PRE RELEASE</span>

<style>
.bar{
    color:blue;
    /* text-decoration: underline !important; */
    position:absolute;
    top: 595px;
    text-align:right;
}
.outer {
    font-family: helvetica; 
    padding-left: 0%;
    padding-right: 0%;
}
a {
    color: blue !important;
    /* text-decoration: underline !important; */
}
table {
  border-collapse: collapse !important;
}
table td, table th {
  border: 0px !important;
  border-left: 1px dotted rgb(240,240,240) !important;
  border-right: 1px dashed rgb(240,240,240) !important;
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

<!-- <div class="bar">
<span style="font-size:130%;font-weight:bold;color:grey;">ddh</span><br>
Date<br>
Duration<br>
Schedule<br>
Calendars<br>
CalendarMath<br>
Parser<br>
Day counters<br>
</div> -->

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

Excellent for modelling fixed income math on human-scale dates ($\pm200$`y`)

<br />

# reference guide

## ddh <a name="ddh"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

Date duration helper `function` that takes a `str` and returns either a `Date`, `Duration`, or `Schedule`. 

##### Usage

 ```python
 from dateroll import ddh
ddh(some_string)
```

##### Examples

|Flavor|Input|Output|
|-|-|-|
|[Today string        ]()|`ddh('t')`|`Date(2024,2,2)`|
|[Date string         ]()|`ddh('12/31/22')`|`Date(2022,12,31)`|
|[Duration string     ]()|`ddh('+3m')`|`Duration(m=3)`|
|[Date math string     ]()|`ddh('t + 1y')`|`Date(2025,2,2)`|
|[Date schedule string ]()|`ddh('t, t+5y, 1m')`|`[Date(2022,2,2),`...`]`|

<br>

See [Parser]() section for valid strings.


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
|Name|Input|Output|
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

|LHS|Operator|RHS|Result|Input|Output|
|-|-|-|-|-|-|
|`Date`|$+$|`Duration`  |`Date`     |`d + Duration(m=1)`|`Date(2000,2,1)`|
|`Date`|$-$|`Duration`  |`Date`     |`d - Duration(y=1)`|`Date(1999,1,1)`|
|`Date`|$-$|`Date`      |`Duration` |`d - Date(1998,1,1)`|`Duration(d=730)`|


##### `Date` $+$/$-$ `int` (for calendar days)
|LHS|Operator|RHS|Result|Input|Output|
|-|-|-|-|-|-|
|`Date`|$+$|`int`      |`Duration` |`d + 5`|`Date(2000,1,6)`|
|`Date`|$-$|`int`      |`Duration` |`d - 1`|`Date(1999,12,31)`|

##### `Date` $+$/$-$ *Date string* or *Duration string*
|LHS|Operator|RHS|Result|Input|Output|
|-|-|-|-|-|-|
|`Date`|$-$|*Date string*     |`Duration`|`d - "1/1/98"`|`Duration(d=730)`|
|`Date`|$+$|*Duration string* |`Date`    |`d + "1m"`|`Date(2000,2,1)`|
|`Date`|$-$|*Duration string* |`Date`    |`d - "1y"`|`Date(1999,1,1)`|


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


<span style="color:red;">open items for 1st release: (1) split modified from roll direction into 2 settings, (2) add EOM rule, and (3) maybe add BRL longer months/shorter months rule.</span>

¹`roll` can one be following business day (`"F"`), preceding business day (`"P"`) or the equivalent modified conventions: modified following (`"MF"`), or modified previous (`"MP"`). 

²`calendar` can be of the form: `"NY"`, `["NY"]`, `"NYuLN"`, or `["NY","LN"]` (see [`Parser`]() for more details.).

Optional `kwargs` for either `anchor_start=Date(...)` or `anchor_stop=Date(...)` can be user-supplied. These are automatically inherited when `Duration` is the result of some math involving a `Date`.
<br>

#### Properties/Methods
|Name                       |Input                     |Output        |
|-                          |-                      |-          | 
|`.years               `      |`Duration(y=5,m=4,d=3,bd=2)`    |`5`        |
|`.months              `      |`Duration(y=5,m=4,d=3,bd=2)`    |`4`        |
|`.days                `      |`Duration(y=5,m=4,d=3,bd=2)`    |`3`        |
|`.bds                 `      |`Duration(y=5,m=4,d=3,bd=2)`    |`2`        |
|`.anchor_start        `      |`ddh('7/7/2000-7/5/2000')`      |`Dates(2000,7,7)`   |
|`.anchor_stop         `      |`ddh('7/7/2000-7/5/2000')`      |`Dates(2000,7,5)`   |
|`.ndays()         `¹        |`Duration(y=5,m=4,d=3,bd=2)`    |~`1478`    |
|`.nyears(counter)`¹²    |`Duration(y=5,m=4,d=3,bd=2)`    |~`4.05`    |

¹The `n*` methods may require period conversion based upon approximation. see [Period Conversions](#PeriodConversions).

²`counter` is one of `"ACT/360"`, `"30/360"`, ... see [day counters]()

#### Operations

assume ```dur = Duration(years=1)```

##### `Duration` $+$/$-$ `Duration`

|LHS|Operator|RHS|Result|Input|Output|
|-|-|-|-|-|-|
|`Duration`|$+$|`Duration`|`Duration`|`d + Duration(m=1)`|`Duration(y=1,m=1)`|
|`Duration`|$-$|`Duration`|`Duration`|`d - Duration(m=1)`|`Duration(m=11)`|

##### `Duration` $+$/$-$ (*Date string* or *Duration string*)
|LHS|Operator|RHS|Result|Input|Output|
|-|-|-|-|-|-|
|`Duration`|$+$|*Duration string* |`Date`    |`d + "1m"`|`Date(2000,2,1)`|
|`Duration`|$-$|*Duration string* |`Date`    |`d - "1y"`|`Date(1999,1,1)`|

#### Anchoring with `Date`

When a `Duration` is the result of an operation with one or more `Date`, then 2 additional properties (`anchor_start` and/or `anchor_stop`) will be set automatically.

`Date(1999, 1, 1 )` $+$ `Duration(m=1)` $=$ `Duration(anchor_start=Date(1999, 1, 1)`
`Date(2000, 1, 1)` $-$ `Date(1999, 1, 1)` $=$ `Duration(y=1, anchor_start=Date(1999,1,1), anchor_end=date(2000, 1, 1)`

When present, these properties allow for more exact period conversion.


#### Period Conversions <a name="PeriodConversions"></a>

If an approximate conversion is required a warning will be raised.

|From period|Calendar Days|
|-|-|
|`1y`|$= 365.242\phantom{.}500 \ \times$ `1d`
|`1q`|$= \phantom{3}90.310\phantom{.}625 \ \times$ `1d`
|`1m`|$= \phantom{3}30.436\phantom{.}875 \ \times$ `1d`
|`1w`|$=$ `7d`
|`1d`|$=$ `1d`
|`1bd`|$\approx 1.449\phantom{.}375$

¹Numerator is days in a year, denominator is `252bd`. Argument can be made for 250-260, just ask!

## Schedule <a name="Schedule"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

Schedule `class` inherits `list`.

A schedule is a `list` of contiguous dates generated from some start date, stop date, and step increment.

#### Usage
```python
>>> from dateroll import Schedule
>>> sch = Schedule(start=Date(1984, 7 ,2), stop=Date(2024, 7 ,2), step=Duration(y=1)
>>> sch.dates
[Date(1984, 7, 2), Date(1985, 7, 2), ..., Date(2024, 7, 2)]
```

### Contructor args
|Name|Description|Type
|-|-|-|
|`start`|First date in schedule|`Date`
|`stop`|Last date in schedule|`Date`
|`step`|Distance between dates in schedule|`Duration`

<br>

### Leftover days (a.k.a. stub handling)
- if `step` $<0$, then schedule is generated **backwards** from last to first
    -  Leftover days are on the interval **`sch[0:2]`**
- if `step` $>0$, then the scheduled is generated **forwards** from first ot last
    -  Leftover days are on the interval **`sch[-2:]`**

<br />

### Properties/Methods
|Name|Input|Output|
|-|-|-|
|`.start`|`sch.start`|`Date(1984, 7 ,2)`|
|`.stop`|`sch.start`|`Date(2024, 7 ,2)`|
|`.step`|`sch.start`|`Duration(y=1)`|
|`.dates`| `Schedule(start=Date(1984, 7...` | `[Date(1984, 7, 2), Date(...]` (sorted)|
|`list.*`|see [list](https://docs.python.org/3/tutorial/datastructures.html)|
 
<br>

## Calendars <a name="Calendars"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

Calendars is a database for your holidays. 
It's a `dict` whose data is always saved for global access. Keys are calendar names, values are ordinary lists of dates.

### Usage

List calendars
```python
>>> cals.keys()
['WE','ALL','NY']
```

Get one
```python
>>> Duration(bd=0,cals=cals['NY']) # get / use#
```

```python
>>> fed = cals.FED # "dot" notation works too
```

Create one
```python
>>> from dateroll import cals
>>> cals['US'] = [Date(...), Date(...), ...] # add takes list of dates, or Schedule
```
Delete one
```python
>>> del cals['NY'] # delete
```

### Calendar name rules

 - 2-3 letters (A-Z), all uppercase only.
 - Examples: `WE` or `WKD` for weekend. `US` or `FED` or `NY` for US banking days.

### Storage

Saves in users's home folder

- `pathlib.Path.home()`
   - `Linux:` `~/.dateroll/calendars/holiday_lists`
   - `Windows:` `C:/Users/[USERNAME]/.dateroll/calendars/holiday_lists`
- Uses `shelve` (may added extension depending on python version)

<br>

### Properties / Methods
|Name|Descriptions|
|-|-|
|`.load_all_and_we()`|Creates `ALL` and `WE`¹|
|`.load_sample_data()`|Creates `ALL`,`WE`,`LN`,`EU`,`BR`,`NY`,`FED`,`ECB`,`BOE`,`BCB` using `worklendar`|
|`dict.*`|see [dict](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) docs||

<br>

### Available calendars
|Name|Description|Source|
|-|-|-|
|`ALL`|All calendar days|Generated for the interval $[$`ddh(-200y)`,`ddh(+200y)` $]$|
|`WE`|**W**eek**e**nds (Sat/Sun's)|Generated for the interval $[$`ddh(-200y)`,`ddh(+200y)` $]$|
|`NY` `FED`|US banking holidays|`workalendar`¹
|`EU` `ECB`|ECB banking holidays|`workalendar`¹
|`LN` `BOE`|UK holidays|`workalendar`¹
|`BR` `BCB`|Brazil holidays|`workalendar`¹

¹ We used `workalender` and generated dates for the same interval as `ALL` and `WE` (above), data for available calendars is stored in `JSON` to eliminate the library dependency. See [workalendar](https://workalendar.github.io/workalendar/) for more details, they've got a lot of great coverage.

<span style="color:red;font-weight:900;">CAUTION</span> using when someone else's calendars! always verify




## Calendar math <a name="CalendarMath"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

`CalendarMath` is an interim singelton `class` that "compiles" Calendar date lists into $O(1)$ hashes.

If you use `ddh` predominately you'll never need to use this directly.

### Usage

```python
>>> from dateroll import calmath
```

### Properties / Methods
|Name|Usage|Descriptions|
|-|-|-|
|`.add_bd(`|`calmath.add_bd(from_date:Date, n:int, cals=calendar)`¹ $\to$ `Date`|Add n bd's|
|`.sub_bd(`|`calmath.sub_bd(from_date, n, cals=calendar)`¹ $\to$ `Date`|Subtract n bd's`|
|`.is_bd(`|`calmath.is_bd(from_date, cals=calendar)`¹ $\to$ `bool`|Is a bd?`|
|`.prev_bd(`|`calmath.prev_bd(from_date, cals=calendar)`¹ $\to$ `Date`|Advance to next bd|
|`.next_bd(`|`calmath.next_bd(from_date), cals=calendar`¹ $\to$ `Date`|Back up until previous bd|


¹`calendar` can be of the form: `"NY"`, `["NY"]`, `"NYuLN"`, or `["NY","LN"]` (see [`Parser`]() for more details.).

### Calendar unions

A calendar "union" is simple a combination of two calendars (without duplication):

$ \mathbb{X} = \Set{t_1, t_2, t_3,...}$
$ \mathbb{Y} = \Set{t_2, t_4, t_5...}$
$ \mathbb{Z} = \mathbb{X} \bigcup \mathbb{Y} $
$ \mathbb{Z} = \Set{t_1, t_2, t_3, t_4, t_5} $

The first time a calendar union is specified (i.e. list of calendars is sent to `CalendarMath`), then the  $O(1)$ hashes are created on the fly and cached. Local to `CalendarMath` instance (`dateroll.calmath`), not `Calendars` instance (`dateroll.cals`).

### Caching / Invalidation

`CalendarMath` stores an in-memory cache of "compiled" calendars. A compiled calendar is simply a collection of hash tables to do business data movements in $O(1)$ time.

There's several mutation checks, and whenever a `Calendars` value is written to, the the entire `CalendarMath` instance cache is purged for safety.

## Parser <a name="Parser"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)

Parses `str` into a `thing`: can be either `Date`, `Duration`, `Schedule`.

This is the 🧠 brains behind `ddh`. 

It a combo of (1) really big `regex`, and (2) date validation with [`dateutil.parser.parse`](https://dateutil.readthedocs.io/en/stable/parser.html).

### String Parsing Ontology

- `DateRollString` (any of the below)
  - `TodayString` (represents TODAY's `Date`)
     - Three literal values: `"t"`,` "t0"`, or `"today"`
     - Converts to `Date`
  - `DateString` (any `Date`)
     - Supports 3 `conventions`: `'american'`, `'european'`, and `'international'`
        - `american`: `month`$\to$`day`$\to$`year`, slashes/dashes/nothing
           - e.g. `"7/2/84"` or `"07-02-1984"`
        - `european`:  `day`$\to$`day`$\to$`year`, slashes/dashes/nothing
           - e.g. `"2/7/1984"` or `"02-07-84"`
        - `international`:  `year`$\to$`month`$\to$`day`, slashes/dashes/nothing
           - e.g. `"19840702"` or `"19840702"`
     - Converts to `Date`
  - `DurationString` (any `Duration`)
    - `DurationPeriodString`
         - Can be $>1$ pairs of `unit` and `period`
           - Unit must be `int`
           - Valid periods: are `bd` `d` `w` `m` `q` `s` (semester) `h` (halves), and `y`
           - Combos like `5y3m` or `7w2d` or `1y2bd` are allowed
    - `CalendarString`
       -  Any `DurationPeriodString` in a `DurationString` can be followed by the filtration (or pipe) operator `"|"` to denote information from calendar lists of holidays which must be used to perform date aritmetic.
           - `CalendarString` follows rules of calendar (2-3 letters A-Z, all uppercase), and union operator `"u"`
              -  Single calendar, e.g. `"|NY"` or `"|FED"`
              -  Calendar union, e.g. `"|NY u LN"` (2) or `"|FED u BOE u BCB"` (3)
                 -  it mathy like $\mathbb{E} [X_t|\mathscr{F_t}]$ where $\mathscr{F_t}=\Set{\text{NY}\bigcup\text{LN}}$
    - `RollingConventionString`
       - The rolling operator `"/"` can be followed by one of the 4 rolling methods:
          - `"/F"` if all period adjustments to a date land on non-business day roll forward to next business day
          - `"/P"` if all period adjustments to a date land on non-business day roll backwards to previous business day
          - `"/MF"` similar to `"/F"` but if you cross a month boundary, go backwards to 1st business date in that month
          - `"/MP"` similar to `"/P"` but if you cross a month boundary, go forwards to last business date in that month
          - for reference [date rolling](https://en.wikipedia.org/wiki/Date_rolling), it's for when payment adjustments need to stay in a specific accounting period.
  - Example with one of everything `"+ 1y 2h 3s 4q 5m 6w 7d 8bd | NY u LN u JP / MF"`
- `ScheduleString` (any `Schedule`)
     - 3 parts separated by two commas, e.g.  `"X, Y, Z"`
        - `X` is `DateString`, `TodayString`, or `DateMathString`
        - `Y` is is `DateString`, `TodayString`, or `DateMathString`
        - `Z` is `DurationString`
     - yields `Schedule(start=X, stop=Y, step=Z)`
     - e.g. `"t-5y, 1/15/25, 1y"` (from 5 years ago to Jan 15 next year, give me all years)
  - `DateMathString` (any datemath operation)
     - 2 parts separated by math operator plus $+$  or minux $-$, e.g. `"X+Y"` or `"Y-X"`
         - `X` or `Y` can be either `DateString` or `DurationString` and add/sub operation logic must be supported by `Date` and `Duration` objects
         - e.g. `"t+1bd"` or `"t-5y"` or `"7/2/84+39y"`
- Examples
   - Unncessarily complicated
     - `"t-1y2h3s4q5m6w7d8bd|NYuLNuJP/MF,07/02/1984+99y35bd|FED/P,3q7m5d|WE"`
        - *^^ Note* on above, if you `ddh` it, all calendars -unioned (`"|NYuLNuJPuFEDuWE"`), modified convention would hold as it was specified once, and `P` or `F` whould depend on the direction of travel when being appled to a specific date. If approx is needed, it will `warn`.
        -    For example, if you  do `"t+1m-21bd"`, if you have an anchor date, if `1m` > `21bd` (net adjustment is in the future as opposed to past) it assumes you are rolling foward, and would impliy a following (`"/F"`), period conversion is used, see [period conversion rules](#PeriodConversions). If modified was specified it would be inherited as well.
   - Classic
      - Client wants a 5 year loan from today, paid monthly, i need dates to structure it `ddh("t,t+5y,1m")`.


# Appendix

## Day counters <a name="DayCounters"></a>

==NEEDS WORK==

[nice wikipedia](https://en.wikipedia.org/wiki/Day_count_convention)

### 30/360

|Usage|Formula|
|-|-|
|`.nyears("30/360")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
|`.nyears("30/360 BB")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
|`.nyears("30/360")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
|`.nyears("30E/360")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
|`.nyears("30E/360 ISDA")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$

### ACT/<span style="color:red;">???</span>

/36?'s

|Usage|Formula|
|-|-|
|`.nyears("ACT/360")` | $\displaystyle\frac{n_d}{360}$
|`.nyears("30E/364")` | $\displaystyle\frac{n_d}{364}$
|`.nyears("ACT/365)`  | $\displaystyle\frac{n_d}{365}$
|`.nyears("ACT/365F")`| $\displaystyle\frac{n_d}{365}$
|`.nyears("ACT/365L")`| $\displaystyle\frac{n_d}{366}$

/ACT's

|Usage|Formula|
|-|-|
`.nyears("ACT/ACT AFB")` | $\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$
`.nyears("ACT/ACT ICMA")` | $\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$

### BD/252

|Usage|Formula|
|-|-|
|`.nyears("BD/252")`|$\displaystyle\frac{360\times (t_{2}^{y}-t_1^{y})+30\times(t_2^{m}-t_1^{m}) + (t_2^{d}-t_1^{d})}{360}$


### Terms
$t_2 = $`t1 = ddh(some_date_string)`
$t_1 = $`t2 = ddh(another_date_string)` $s.t.\ \  t_2 > t_1$

$t_1^y$ = `t1.years`, $t_2^y$ = `t1.years`
$t_1^m$ = `t1.months`, $t_2^m$ = `t1.months`
$t_1^d$ = `t1.days`, $t_1^d$ = `t1.days`


</div>

## Caveats

- Calendars are political, and each jurisdiction has unique methods to proclaim or repeal.
- This is only designed to be used for "human life" dates, such as -100y ago and +100y from now. In the future we might add support for sub-day time periods (hours, minutes, ...)
- There is no central standards body, these conventions are known as "street conventions", i.e. each financial institutions and 3rd party vendor has their own reference implementations. Reliance on self regulatory agency (ISDA/ICMA) guidance and case law / precedents is the norm.
  
## Acknowledgements

Thank you to the teams behind `dateutil`, `datetime`, `workalendar`, `pandas`, `numpy`, `ICMA`, `ISDA`, `ISO 8601`, and the countless traders and bond/derivatives accountants worldwide.

It is our hope that fixed income and FI math can be a little less scary for everyone, because *every single person in the world* is impacted by it.

\- The [Disent](https://www.disent.com) Team

## References

- https://en.wikipedia.org/wiki/Date_rolling
- https://en.wikipedia.org/wiki/ISO_8601
- https://en.wikipedia.org/wiki/Day_count_convention
- https://www.amazon.com/Calendrical-Calculations-Edward-M-Reingold/dp/0521771676 (thanks Prof!)
- https://www.amazon.com/Fixed-Income-Mathematics-Fifth-Statistical/dp/1264258275

## Documentation Todo's

- Verify all examples
- Cross references features in doc not yet in code base
- Finish daycounters
- add period conversion formulas to recalc the decimals
- Cross doc features against code base
- Separate features from roadmap
- Group proofreading
- Add notebook with examples (maybe a colab?)
- Add REPL in-doc examples