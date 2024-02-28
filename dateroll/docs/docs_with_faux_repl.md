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

|[*DateRollString*]()|Interactive Example (REPL)|
|-|-|
|[*TodayString*        ]()|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> ddh("t")'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="datetime.datetime(2024, 7, 2, 0, 0)"></input></div>|
|[*DateString*         ]()|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> ddh("7/2/84")'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="datetime.datetime(2024, 7, 2, 0, 0)"></input></div>|
|[*DurationString*     ]()|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> ddh("+3m")'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="datetime.datetime(2024, 7, 2, 0, 0)"></input></div>|
|[*DateMathString*     ]()|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> ddh("t+1bd\|NY")'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="datetime.datetime(2024, 7, 2, 0, 0)"></input></div>|
|[*DateScheduleString* ]()|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> ddh("t,t+5y,6m")'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="datetime.datetime(2024, 7, 2, 0, 0)"></input></div>|

<br>



## Date
<!-- [ddh]() | Date| [Dur<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> ddh("t")'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="datetime.datetime(2024, 7, 2, 0, 0)"></input></div>| -->

Date is a `class` which inherits from the native python `datetime.date`. Constructor is the same with  additional properties/methods and operator overloads.

#### Usage
```python
>>> from dateroll import Date
>>> Date(year,month,day)
```
##### Constructor example
<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2)'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="Date(24,7,2)"></input></div>|

##### Properties/Methods
|Name|Example|
|-|-|
|`.datetime`|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).datetime'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="datetime.datetime(2024, 7, 2, 0, 0)"></input></div>|
|`.date`|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).date'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="datetime.date(2024, 7, 2, 0, 0)"></input></div>||
|`.is_bd(calendars)`¹|<div style="display:inline-block"><input style="width:400px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).isBd,cal=["NY","LN"]'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:100px;font-family:consolas;border:1px solid black;" disabled=True value="True"></input></div>|
|`.iso`|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).iso'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="20240702"></input></div>|
|`.xls`|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).xls'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="45475"></input></div>||
|`.unix`|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).unix'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="1719892800.0"></input></div>||
|`.dotw`|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).dotw'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="'Tue'"></input></div>||
|`.wotm`|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).wotm'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="2"></input></div>||
|`.woty`|<div style="display:inline-block"><input style="width:200px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).woty'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:300px;font-family:consolas;border:1px solid black;" disabled=True value="26"></input></div>||
|`datetime.date.*`|see [datetime](https://docs.python.org/3/library/datetime.html#datetime.date)|

¹ For calendars it can be either not provided (checks Sat/Sun only), a list of CalendarString's `['NY','LN']` or a 1 CalendarString `'FEDuECB'`, see [string's]() doc for more.

##### Operations

|LHS|Operator|RHS|Result|Example
|-|-|-|-|-|
|`Date`|$+$|*Datestring*|`Date`|<div style="display:inline-block"><input style="width:125px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).woty'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:125px;font-family:consolas;border:1px solid black;" disabled=True value="26"></input></div>|
|`Date`|$-$|*Datestring*|`Date`|<div style="display:inline-block"><input style="width:125px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).woty'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:125px;font-family:consolas;border:1px solid black;" disabled=True value="26"></input></div>|
|`Date`|$+$|*|`Date`|<div style="display:inline-block"><input style="width:125px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).woty'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:125px;font-family:consolas;border:1px solid black;" disabled=True value="26"></input></div>|
|`Date`|$-$|*Datestring*|`Date`|<div style="display:inline-block"><input style="width:125px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).woty'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:125px;font-family:consolas;border:1px solid black;" disabled=True value="26"></input></div>|
|`Date`|$+$|*Datestring*|`Date`|<div style="display:inline-block"><input style="width:125px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).woty'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:125px;font-family:consolas;border:1px solid black;" disabled=True value="26"></input></div>|
|`Date`|$+$|*Datestring*|`Date`|<div style="display:inline-block"><input style="width:125px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).woty'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:125px;font-family:consolas;border:1px solid black;" disabled=True value="26"></input></div>|
|`Date`|$+$|*Datestring*|`Date`|<div style="display:inline-block"><input style="width:125px;background-color:black; border:none;outline:none;color:white;font-family:consolas;border: 1px solid black;font-size:10pt;" value='>>> Date(24,7,2).woty'></input><input style="background-color:white;font-size:10pt; border:none;outline:none;color:black;width:125px;font-family:consolas;border:1px solid black;" disabled=True value="26"></input></div>|


## Duration

## Schedule

## Calendars

## Calendar math

## Parser