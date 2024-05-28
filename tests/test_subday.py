import datetime
import unittest
import pandas as pd

from tzlocal import get_localzone
from dateutil.relativedelta import relativedelta as rd

import dateroll
from dateroll import utils
import dateroll.date.date as dateModule
import dateroll.duration.duration as durationModule
import dateroll.schedule.schedule as scheduleModule
from dateroll import ddh
from dateroll.settings import settings


# import dateroll.duration.duration as durationModule


class TestSubDay(unittest.TestCase):
    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(self): ...

    def test_subday(self):
        x1 = ddh("1y2m10d2bd12h21min22s+3bd")
        x2 = ddh("1h")
        x3 = ddh("1m")
        x4 = ddh("1h10m")
        x5 = ddh("3bd1h10min2s20us")
        x6 = ddh("20230101T12:23:22").datetime

        expected1 = durationModule.Duration(
            years=1,
            months=2,
            days=10,
            h=12,
            min=21,
            s=22,
            us=0,
            modified=False,
            bd=5.0,
            cals="WE",
        )
        expected2 = durationModule.Duration(
            years=0, months=0, days=0, h=1, min=0, s=0, us=0, modified=False
        )
        expected3 = durationModule.Duration(
            years=0, months=1, days=0, h=0, min=0, s=0, us=0, modified=False
        )
        expected4 = durationModule.Duration(
            years=0, months=10, days=0, h=1, min=0, s=0, us=0, modified=False
        )
        expected5 = durationModule.Duration(
            years=0,
            months=0,
            days=0,
            h=1,
            min=10,
            s=2,
            us=20,
            modified=False,
            bd=3.0,
            cals="WE",
        )
        expected6 = datetime.datetime(2023, 1, 1, 12, 23, 22, 0).astimezone(
            get_localzone()
        )
        with self.assertRaises(dateroll.utils.ParserStringsError):
            ddh("01012023T1h10min")

        self.assertEqual(x1, expected1)
        self.assertEqual(x2, expected2)
        self.assertEqual(x3, expected3)
        self.assertEqual(x4, expected4)
        self.assertEqual(x5, expected5)
        self.assertEqual(x6, expected6)

    def test_dur_calc(self):
        """
        all kind of duration calculations
        """

        x1 = ddh("6bd-3min+4min+1h")
        x2 = ddh("3d+10d-19d+3min-6min+7min-9s+20000s-1h")
        x3 = ddh("1y23m-3s1bd10h")
        x4 = ddh("23h100000min3000000s10us")
        x5 = ddh("-10y4m+2y3bd+300min20us")
        x6 = ddh("10y+31bd-23bd+2bd-10m+10min-8min+2min")
        with self.assertRaises(TypeError):
            ddh("10y+31bd-23bd+2bd-10m+10min-(8min+2min)")
        x7 = ddh("3y15s-10y3bd5s23min|WEuNY/MOD")
        x8 = ddh("-5s10y+1m15s")

        rs1 = durationModule.Duration(bd=6, min=1, h=1)
        rs2 = durationModule.Duration(
            years=0, months=0, days=-6, h=-1, min=4, s=19991, us=0, modified=False
        )
        rs3 = durationModule.Duration(
            years=2,
            months=11,
            days=0,
            h=-10,
            min=0,
            s=-3,
            us=0,
            modified=False,
            bd=-1.0,
            cals="WE",
        )
        rs4 = durationModule.Duration(
            years=0,
            months=0,
            days=0,
            h=23,
            min=100000,
            s=3000000,
            us=10,
            modified=False,
        )
        rs5 = durationModule.Duration(y=-8, m=-4, bd=3, min=300, us=20)
        rs6 = durationModule.Duration(y=9, bd=10, m=2, min=4)
        rs7 = durationModule.Duration(
            years=-7,
            months=0,
            days=0,
            h=0,
            min=-23,
            s=10,
            us=0,
            modified=True,
            bd=-3.0,
            cals="NYuWE",
        )
        rs8 = durationModule.Duration(
            years=-9, months=-11, days=0, h=0, min=0, s=10, us=0, modified=False
        )

        self.assertEqual(x1, rs1)
        self.assertEqual(x2, rs2)
        self.assertEqual(x3, rs3)
        self.assertEqual(x4, rs4)
        self.assertEqual(x5, rs5)
        self.assertEqual(x6, rs6)
        self.assertEqual(x7, rs7)
        self.assertEqual(x8, rs8)

    def test_dur_date_calc(self):
        """
        all kind of date and duration calculation
        """

        x1 = ddh("20230201T00:00:23-10us")
        x2 = ddh("02032011-10bd+20000s-8bd+10y")
        x3 = ddh("2023-01-02T23:12:00-23h-12min")
        x4 = ddh("2023-01-02T23:12:00-23h-13min")
        x5 = ddh("2023-10-11T11:23:22+3d")
        x6 = ddh("03022022-5s3min3y2m")

        rs1 = dateModule.Date(2023, 2, 1, 0, 0, 22, 999990)
        rs2 = dateModule.Date(2021, 1, 10, 5, 33, 20, 0)
        rs3 = dateModule.Date(2023, 1, 2)
        rs4 = dateModule.Date(2023, 1, 1, 23, 59)
        rs5 = dateModule.Date(2023, 10, 14, 11, 23, 22)
        rs6 = dateModule.Date(2019, 1, 1, 23, 56, 55, 0)

        with self.assertRaises(utils.ParserStringsError):
            ddh("2023-01-13T:25:11:22")

        with self.assertRaises(utils.ParserStringsError):
            ddh("03022021+04012022+3h23us22s")

        d = ddh("03082023")
        self.assertTrue(d.tzinfo is not None)
        d = dateModule.Date.to_naive(d.datetime)
        self.assertTrue(d.tzinfo is None)
        with self.assertRaises(TypeError):
            dateModule.Date.to_naive(30)
        d = dateModule.Date.to_naive(datetime.datetime(2023, 3, 8))
        self.assertTrue(d.tzinfo is None)

        self.assertEqual(x1, rs1)
        self.assertEqual(x2, rs2)
        self.assertEqual(x3, rs3)
        self.assertEqual(x4, rs4)
        self.assertEqual(x5, rs5)
        self.assertEqual(x6, rs6)

    def testSchedule(self):
        """
        str->Schedule with subday
        """

        sh1 = ddh("2023-01-02T23:12:00-23h-13min,01022023,1bd").list
        sh2 = ddh("2023-01-02T23:12:00-23h-13min,01022023+20h12min,3bd").list

        rs1 = [
            dateModule.Date(2023, 1, 1, 23, 59, 0, 0),
            dateModule.Date(2023, 1, 2, 0, 0, 0, 0),
        ]
        rs2 = [
            dateModule.Date(2023, 1, 1, 23, 59, 0, 0),
            dateModule.Date(2023, 1, 2, 20, 12, 0, 0),
        ]

        self.assertEqual(sh1, rs1)
        self.assertEqual(sh2, rs2)

    def test_usage_df(self):
        """
        work with the spy dataframe with an intraday data
        load the json data from tests/test_data/test_data_spy.json
        """

        P = "tests/test_data/spy.csv"
        df = pd.read_csv(P,header=[0],index_col=[0])
        
        df["t"] = df["t"].apply(lambda x:ddh.Date.from_timestamp(x / 1000).est.naive.iso)
        cut = ddh("10102022").iso
        df = df[df["t"] >= cut]
        # here t is utc time, convert into EST time
        # df.set_index(df["t"], inplace=True)
        st = ddh('9h30min').time
        ed = ddh('16h').time
        
        #### debug to DELETE
        df.index = pd.to_datetime(df['t'])
        # mkt = df.between_time(st,ed)
        # start one line no code
        ##### 
        # 1 choose date
        # 2 premarket high
        # 3 mkt high
        # old way
        od = datetime.date(2022,10,10).strftime('%Y-%m-%d')
        old = df.loc[od]
        opre = df.between_time(datetime.time(4,0),datetime.time(9,29))['h'].max()
        omkt = df.between_time(datetime.time(9,30),datetime.time(16,0))['h'].max()
        
        ### new way
        nd = ddh('10102022').strftime('%Y-%m-%d')
        new = df.loc[nd]
        npre = df.between_time(ddh('4h').time,ddh('9h29min').time)['h'].max()
        nmkt = df.between_time(ddh('9h30min').time,ddh('16h').time)['h'].max()
        #### some calculation
        
        ### get price at 3 minute interval with eastern time zone
        
        interval = ddh('2022-10-10T09:30:00,2022-10-10T16:00:00,3min').est.naive.iso.list
        new_3min = new[new['t'].isin(interval)]
        # old way
        
        ed = datetime.datetime(2022,10,10,16)
        x = datetime.datetime(2022,10,10,9,30)
        interval_old = [x.isoformat()]
        while x<ed:
            x = x+rd(minutes=3)
            interval_old.append(x.isoformat())
        
        old_3min = old[old['t'].isin(interval_old)]
        
        # after mkt open 10,20,30 min high for the 3 months
        # new way

        
        # self.assertEqual(df.index[0], cut)

        # dates only divisible by 3
        div_3 = lambda x: ddh(x).minute % 3 == 0
        df_div_3 = df[df["t"].apply(div_3)]
        self.assertTrue(len(df_div_3) < len(df))


if __name__ == "__main__":
    unittest.main()
    # utils.create_offset_map()
