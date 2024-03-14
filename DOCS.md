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
    padding-left: 15%;
    padding-right: 15%;
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
  border-top: 0px solid rgb(50,50,50) !important;
  border-bottom: 0px solid rgb(50,50,50) !important;
  padding-top:7px !important;
  padding-bottom:7px !important;
}
table tr:first-child th {
  border-top: 2px solid black !important;
  border-bottom: 2px solid black !important;
}
table tr:last-child td {
  border-bottom: 0 !important;
  border-bottom: 2px solid black !important;
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

|Flavor|Example|
|-|-|
|[Today string        ]()|<div class="disent-embed" data-defaultinput='ddh("t")'></div><script type='text/javascript' src="http://repl.disent.com/drepl.js" async></script>
|[Date string         ]()|<div class="disent-embed" data-defaultinput='ddh("12/31/22")'></div>|
|[Duration string     ]()|<div class="disent-embed" data-defaultinput='ddh("+3m")'></div>|
|[Date math string     ]()|<div class="disent-embed" data-defaultinput='ddh("t+1y")'></div>|
|[Date schedule string ]()|<div class="disent-embed" data-defaultinput='ddh("t,t+5y,1m")'></div>|

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
<div class="disent-embed" data-defaultinput='Date(2024,7,2)'></div>
<br>
*^3 integer args: year, month, and day

##### Properties/Methods
|Name|Example|
|-|-|
|`.datetime`            | <div class="disent-embed" data-defaultinput='Date(2024,7,2).datetime'></div> |
|`.date`                | <div class="disent-embed" data-defaultinput='Date(2024,7,2).date'></div>|
|`.iso`                 | <div class="disent-embed" data-defaultinput='Date(2024,7,2).iso'></div>|
|`.xls`                 | <div class="disent-embed" data-defaultinput='Date(2024,7,2).xls'></div>|
|`.unix`                | <div class="disent-embed" data-defaultinput='Date(2024,7,2).unix'></div>|
|`.dotw`                | <div class="disent-embed" data-defaultinput='Date(2024,7,2).dotw'></div>|
|`.woty`                | <div class="disent-embed" data-defaultinput='Date(2024,7,2).woty'></div>|                                                  |
|`.is_bd(calendar)`¹    |<div class="disent-embed" data-defaultinput='Date(2024,7,2).is_bd("NY")'></div>|
|`datetime.date.*`|see [datetime](https://docs.python.org/3/library/datetime.html#datetime.date)|

¹`calendar` can be of the form: `"NY"`, `["NY"]`, `"NYuLN"`, or `["NY","LN"]` (see [`Parser`]() for more details.).


##### Operations

##### `Date` $+$/$-$ `Duration` or `Date`

|LHS|Operator|RHS|Result|Example|
|-|-|-|-|-|
|`Date`|$+$|`Duration`  |`Date`     |<div class="disent-embed" data-defaultinput='Date(2000,1,1) + Duration(m=1)'></div>|
|`Date`|$-$|`Duration`  |`Date`     |<div class="disent-embed" data-defaultinput='Date(2000,1,1) + Duration(y=1)'></div>|
|`Date`|$-$|`Date`      |`Duration` |<div class="disent-embed" data-defaultinput='Date(2000,1,1) - Date(1998,1,1)'></div>|


##### `Date` $+$/$-$ `int` (for calendar days)
|LHS|Operator|RHS|Result|Example|
|-|-|-|-|-|
|`Date`|$+$|`int`      |`Duration` |<div class="disent-embed" data-defaultinput='Date(2000,1,1) + 5'></div>|
|`Date`|$-$|`int`      |`Duration` |<div class="disent-embed" data-defaultinput='Date(2000,1,1) - 1'></div>|

##### `Date` $+$/$-$ *Date string* or *Duration string*
|LHS|Operator|RHS|Result|Example|
|-|-|-|-|-|
|`Date`|$-$|*Date string*     |`Duration`|<div class="disent-embed" data-defaultinput='Date(2000,1,1) - "1/1/98"'></div>|
|`Date`|$+$|*Duration string* |`Date`    |<div class="disent-embed" data-defaultinput='Date(2000,1,1) + "1m"'></div>|
|`Date`|$-$|*Duration string* |`Date`    |<div class="disent-embed" data-defaultinput='Date(2000,1,1) - "1y"'></div>|


## Duration <a name="Duration"></a>

[ddh](#ddh) | [Date](#Date) | [Duration](#Duration) | [Schedule](#Schedule) | [Calendars](#Calendars) | [CalendarMath](#CalendarMath) | [Parser](#Parser)


Duration `class` inherits from `dateutil.relativedelta` for defining intervals (periods) of time.

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
|Years                      |`years` `year` `Y` `y`|<div class="disent-embed" data-defaultinput='Duration(y=1)'></div>|
|Quarters ($\to$ 3m)        |`quarters` `quarter` `Q` `q`|<div class="disent-embed" data-defaultinput='Duration(q=1)'></div>|
|Weeks ($\to$ 7d)           |`weeks` `week` `W` `w`|<div class="disent-embed" data-defaultinput='Duration(w=1)'></div>|
|Calendar days              |`days` `day` `D` `d`|<div class="disent-embed" data-defaultinput='Duration(d=-1)'></div>|
|Calendar days w/ modified      |`modified=modified`¹|<div class="disent-embed" data-defaultinput='Duration(d=1,modified=True)'></div>|
|Business days              |`BD` `bd`|<div class="disent-embed" data-defaultinput='Duration(bd=-1)'></div>|
|Business days w/ calendar  |`BD` `bd` `cals=calendar`²|<div class="disent-embed" data-defaultinput='Duration(bd=-1,cals="FED")'></div>|
|Combinations|`y` `m` `bd` `cals`|<div class="disent-embed" data-defaultinput='Duration(y=1,m=3,bd=-1,cals="FED")'></div>|


<span style="color:red;">open items for 1st release: (1) split modified from roll direction into 2 settings, (2) add EOM rule, and (3) maybe add BRL longer months/shorter months rule.</span>

¹`modified` can be True or False. 

²`calendar` can be of the form: `"NY"`, `["NY"]`, `"NYuLN"`, or `["NY","LN"]` (see [`Parser`]() for more details.).

Optional `kwargs` for either `anchor_start=Date(...)` or `anchor_stop=Date(...)` can be user-supplied. These are automatically inherited when `Duration` is the result of some math involving a `Date`.
<br>

#### Properties/Methods
|Name                       |Example                   |
|-                          |-                      | 
|`.years               `      |<div class="disent-embed" data-defaultinput='Duration(y=5,m=4,d=3,bd=2).years'></div>|
|`.months              `      |<div class="disent-embed" data-defaultinput='Duration(y=5,m=4,d=3,bd=2).months'></div>|
|`.days                `      |<div class="disent-embed" data-defaultinput='Duration(y=5,m=4,d=3,bd=2).days'></div>|
|`.bd                 `      |<div class="disent-embed" data-defaultinput='Duration(y=5,m=4,d=3,bd=2).bd'></div>|
|`._anchor_start        `      |<div class="disent-embed" data-defaultinput='ddh("7/7/2000-7/5/2000")._anchor_start'></div>|
|`._anchor_end         `      |<div class="disent-embed" data-defaultinput='ddh("7/7/2000-7/5/2000")._anchor_end'></div>|
|`.ndays()         `¹        |<div class="disent-embed" data-defaultinput='Duration(y=5,m=4,d=3,bd=2)'></div>|
|`.nyears(counter)`²    |<div class="disent-embed" data-defaultinput='Duration(y=5,m=4,d=3,bd=2)'></div>|

¹The `n*` methods may require period conversion based upon approximation. see [Period Conversions](#PeriodConversions).

²`counter` is one of `"ACT/360"`, `"30/360"`, ... see [day counters]()

#### Operations

assume ```dur = Duration(years=1)``` and ```d = Date(2000,1,1)```

##### `Duration` $+$/$-$ `Duration`

|LHS|Operator|RHS|Result|Example|
|-|-|-|-|-|
|`Duration`|$+$|`Duration`|`Duration`|<div class="disent-embed" data-defaultinput='Duration(y=1) + Duration(m=1)'></div>|
|`Duration`|$-$|`Duration`|`Duration`|<div class="disent-embed" data-defaultinput='Duration(y=1) - Duration(m=1)'></div>|

##### `Date` $+$/$-$ *Duration string*
|LHS|Operator|RHS|Result|Example|
|-|-|-|-|-|
|`Date`|$+$|*Duration string* |`Date`    |<div class="disent-embed" data-defaultinput='Date(2000,1,1) + "1m"'></div>|
|`Date`|$-$|*Duration string* |`Date`    |<div class="disent-embed" data-defaultinput='Date(2000,1,1) - "1m"'></div>|

#### Anchoring with `Date`

When a `Duration` is the result of an operation with two `Date`, then 2 additional properties (`_anchor_start` and/or `_anchor_end`) will be set automatically.


`Date(2000, 1, 1)` $-$ `Date(1999, 1, 1)` $=$ `Duration(y=1, _anchor_start=Date(1999,1,1), _anchor_end=date(2000, 1, 1)`

<div class="disent-embed" data-defaultinput='Date(2000,1,1) - Date(1999,1,1)'></div>


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

<div class="disent-embed" data-defaultinput='Schedule(start=Date(1984,7,2),stop=Date(2024,7,2),step=Duration(y=1)).dates'></div><script type='text/javascript' src="http://repl.disent.com/drepl.js" async></script>


### Constructor args

|Name|Description|Type
|-|-|-|
|`start`|First date in schedule|`Date`
|`stop`|Last date in schedule|`Date`
|`step`|Distance between dates in schedule|`Duration`

<br>

### Leftover days (a.k.a. stub handling)
- if `step` $<0$, then schedule is generated **backwards** from last to first
    -  Leftover days are on the interval **`sch[0:2]`**
- if `step` $>0$, then the schedule is generated **forwards** from first to last
    -  Leftover days are on the interval **`sch[-2:]`**

<br />

### Properties/Methods
|Name|Input|Output|
|-|-|-|
|`.start`|`sch.start`|`Date(1984, 7 ,2)`|
|`.stop`|`sch.stop`|`Date(2024, 7 ,2)`|
|`.step`|`sch.step`|`Duration(y=1)`|
|`.dates`| `Schedule(start=Date(1984, 7...` | `[Date(1984, 7, 2), Date(...]` (sorted)|
|`list.*`|see [list](https://docs.python.org/3/tutorial/datastructures.html)|

<div class="disent-embed" data-defaultinput='Schedule(start=Date(1984,7,2),stop=Date(2024,7,2),step=Duration(y=1)).start'></div>

<div class="disent-embed" data-defaultinput='Schedule(start=Date(1984,7,2),stop=Date(2024,7,2),step=Duration(y=1)).stop'></div>

<div class="disent-embed" data-defaultinput='Schedule(start=Date(1984,7,2),stop=Date(2024,7,2),step=Duration(y=1)).step'></div>
 
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
>>> Duration(bd=0,cals=['NY']) # get / use#
```
<div class="disent-embed" data-defaultinput='Duration(bd=0,cals=["NY"])'></div>

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
>>> del cals['US'] # delete
```

### Calendar name rules

 - 2-3 letters (A-Z), all uppercase only.
 - Examples: `WE` for weekend. `FED` or `NY` for US banking days.

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
|`.load_sample_data()`|Creates `ALL`,`WE`,`LN`,`EU`,`BR`,`NY`,`FED`,`ECB`,`BOE`,`BCB` using `workalendar`|
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

### Calendar sets

A calendar "set" is a union of two calendars (without duplication):

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
        - `european`:  `day`$\to$`month`$\to$`year`, slashes/dashes/nothing
           - e.g. `"2/7/1984"` or `"02-07-84"`
        - `international`:  `year`$\to$`month`$\to$`day`, slashes/dashes/nothing
           - e.g. `"19840702"` or `"19840702"`
     - Converts to `Date`
  - `DurationString` (any `Duration`)
    - `DurationPeriodString`
         - Can be $>1$ pairs of `unit` and `period`
           - Unit must be `int`
           - Valid periods: are `bd` `d` `w` `m` `q` and `y`
           - Combos like `5y3m` or `7w2d` or `1y2bd` are allowed
    - `CalendarString`
       -  Any `DurationPeriodString` in a `DurationString` can be followed by the filtration (or pipe) operator `"|"` to denote information from calendar lists of holidays which must be used to perform date arithmetic.
           - `CalendarString` follows rules of calendar (2-3 letters A-Z, all uppercase), and union operator `"u"`
              -  Single calendar, e.g. `"|NY"` or `"|FED"`
              -  Calendar union, e.g. `"|NY u LN"` (2) or `"|FED u BOE u BCB"` (3)
                 -  it mathy like $\mathbb{E} [X_t|\mathscr{F_t}]$ where $\mathscr{F_t}=\Set{\text{NY}\bigcup\text{LN}}$
    - `RollingConventionString`
       - The rolling operator `"/"` can be followed by MOD string:
          - When the direction of direction is positive`"/MOD"` means that if you cross a month boundary, go backwards to 1st business date in that month
          - When the direction of direction is negative`"/MOD"` means that if you cross a month boundary, go forwards to last business date in that month
          - for reference [date rolling](https://en.wikipedia.org/wiki/Date_rolling), it's for when payment adjustments need to stay in a specific accounting period.

         Example:
            <div class="disent-embed" data-defaultinput='ddh("12/30/2023+5bd/MOD")'></div>

  - Example with one of everything `"+ 1y 2h 3s 4q 5m 6w 7d 8bd | NY u LN u JP / MF"`
  
- `ScheduleString` (any `Schedule`)
     - 3 parts separated by two commas, e.g.  `"X, Y, Z"`
        - `X` is `DateString`, `TodayString`, or `DateMathString`
        - `Y` is is `DateString`, `TodayString`, or `DateMathString`
        - `Z` is `DurationString`
     - yields `Schedule(start=X, stop=Y, step=Z)`
     - e.g. `"t-5y, 1/15/25, 1y"` (from 5 years ago to Jan 15 next year, give me all years)
  - `DateMathString` (any datemath operation)
     - 2 parts separated by math operator plus $+$  or minus $-$, e.g. `"X+Y"` or `"Y-X"`
         - `X` or `Y` can be either `DateString` or `DurationString` and add/sub operation logic must be supported by `Date` and `Duration` objects
         - e.g. `"t+1bd"` or `"t-5y"` or `"7/2/84+39y"`
          
         <div class="disent-embed" data-defaultinput='ddh("t+1bd")'></div> 

         <div class="disent-embed" data-defaultinput='ddh("t-5y")'></div> 

         <div class="disent-embed" data-defaultinput='ddh("7/2/84+39y")'></div> 
- Examples
   - Unncessarily complicated
     - `"t-1y4q5m6w7d8bd|NYuLNuBR/MOD,07/02/1984+45y35bd|FED/MOD,3q7m5d|WE"`
        - *^^ Note* on above, if you `ddh` it, all calendars -unioned (`"|NYuLNuJPuFEDuWE"`), modified convention would hold as it was specified once, and `MOD` would depend on the direction of travel when being appled to a specific date. If approx is needed, it will `warn`.
        -    For example, if you  do `"t+1m-21bd"`, if you have an anchor date, if `1m` > `21bd` (net adjustment is in the future as opposed to past) it assumes you are rolling foward, period conversion is used, see [period conversion rules](#PeriodConversions). If modified was specified it would be inherited as well.

        Example:
               <div class="disent-embed" data-defaultinput='Schedule(ddh("t-1y4q5m6w7d8bd|NYuLNuBR/MOD"),ddh("07/02/1984+45y35bd|FED/MOD"),ddh("3q7m5d|WE")).dates'></div> 
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

</div>