# dateroll


### dateroll.ddh
[D]ate [D]uration [H]elper  function

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