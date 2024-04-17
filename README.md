<p align="center">
  <img src="logo.png" style="width:250px"/>
</p>

# `dateroll`

![Coverage Status](./coverage-badge.svg?dummy=8484744)

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
Date(2024,3,3)

>>> d = ddh('t')
>>> d - '2bd|NY'
Date(2024,2,29)

```

Use strings for all your date needs with `dateroll.ddh` (ddh= date duration helper).
Our `Date` class is a drop-in replacement for `datetime.date`, and our `Duration` class is a drop-in replacement for `datetime.timedelta` or `datetime.relativedelta.relativedelta`. You can also use schedule strings to define a `Schedule` class, which is not so different than `RRULE`.

Please visit our interactive documentation! [dateroll.disent.com](https://dateroll.disent.com)

Happy rolling! 

- The Disent Team
