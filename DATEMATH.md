
# `dateroll`

## Strings vs Native Objects

`dateroll` allows the user to provide strings to rapidly enumerate many types of vanilla and exotic data manipulations.

`ddh(some_string)`

`ddh('thing')`
`ddh('thing,thing,thing')`

where thing is either `DateString`, `DurationString`, or `DateMathString`

== split table below into thing and thing,thing,thing==

Flavor|`str` example|`dateroll` constructor|
|-|-|-|
|Date string|`'7/2/84'`|`Date(1984, 7, 2)`|
|Duration string|`'3m'`|`Duration(m=3)`|
|Date math string|`'2/1/24 + 1y'`|`  Date(2024, 2, 1)`<br>`+ Duration(y=1)`<br>`= Date(2025, 2, 1)`|
|Schedule generator string|`'1/15/20,1/15/24,1m'`|`Schedule = (` <br>  &nbsp;&nbsp;&nbsp;&nbsp;`start=Date(2020,1,15)`,<br>&nbsp;&nbsp;&nbsp;&nbsp;`stop=Date(2024,1,15),` <br>&nbsp;&nbsp;&nbsp;&nbsp;`step=Duration(m=1)`<br>`)`|

## More examples

### Date strings

|`str` example|`Date` constructor|
|-|-|
|`Date('t')` |`Date(y=24,m=2,d=22)`
|`Date('7/2/84')` |`Date(y=84,m=7,d=2)`
|`Date('7/2/84')` |`Date(y=84,m=7,d=2)`

`"t"` is special for today, and valid all other valid DateStrings are what is supported by  the [`dateutil.parser`](https://dateutil.readthedocs.io/en/stable/parser.html) library.


### Duration strings

|`str` example|`Date` constructor|meaning|
|-|-|-|
|`-3m`  |`Duration(m=-3)`|today|
|`'+1bd`|`Duration(d=1,bd=True)`|a date|

### Schedule strings

|`str` example|`Date` constructor|meaning|
|-|-|-|
|`-3m`  |`Duration()`|today|
|`'+1bd`|`Duration()`|a date|

## Supported arithmetic

#### Binary Operations

|LHS type|Operator|RHS type|Result type|`str` example|
|-|-|-|-|-|
|`Date`|$+$|`Duration`|`Date`|`'5/5/5+5y'`|
|`Duration`|$+$|`Date`|`Date`|`'3y+t'`|
|`Duration`|$+$|`Duration`|`Duration`|`'1y+3m'`|
|`Date`|$-$|`Date`|`Duration`|`'7/7/7-6/6/6'`|
|`Date`|$-$|`Duration`|`Date`|`'8/8/8-8m'`|
|`Duration`|$-$|`Duration`|`Duration`|`'1y-11m'`|

#### Business date adjustments

- rolling convention
- calender and calender math

Any base `Duration` `str` can be 

