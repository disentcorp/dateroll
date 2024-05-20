import datetime
import unittest

from tzlocal import get_localzone

import dateroll
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

    # def test_subday(self):
        # x1 = ddh('1y2m10d2bd12h21min22s+3bd')
        # x2 = ddh('1h')
        # x3 = ddh('1m')
        # x4 = ddh('1h10m')
        # x5 = ddh('3bd1h10min2s20us')
        # x6 = ddh('20230101T12:23:22').datetime
        
        # expected1 = durationModule.Duration(years=1, months=2, days=10, h=12, min=21, s=22, us=0, modified=False, bd=5.0, cals="WE")
        # expected2 = durationModule.Duration(years=0, months=0, days=0, h=1, min=0, s=0, us=0, modified=False)
        # expected3 = durationModule.Duration(years=0, months=1, days=0, h=0, min=0, s=0, us=0, modified=False)
        # expected4 = durationModule.Duration(years=0, months=10, days=0, h=1, min=0, s=0, us=0, modified=False)
        # expected5 = durationModule.Duration(years=0, months=0, days=0, h=1, min=10, s=2, us=200000, modified=False, bd=3.0, cals="WE")
        # expected6 = datetime.datetime(2023,1,1,12,23,22,0).astimezone(get_localzone())
        # with self.assertRaises(ValueError):
        #     ddh('01012023T1h10min')

        
        # self.assertEqual(x1,expected1)
        # self.assertEqual(x2,expected2)
        # self.assertEqual(x3,expected3)
        # self.assertEqual(x4,expected4)
        # self.assertEqual(x5,expected5)
        # self.assertEqual(x6,expected6)
    
    def test_dur_calc(self):
        """
            all kind of duration calculations
        """

        x1 = ddh("6bd-3min+4min+1h")
        x2 = ddh('3d+10d-19d+3min-6min+7min-9s+20000s-1h')
        x3 = ddh('1y23m-3s1bd10h')
        x4 = ddh('23h100000min3000000s10us')

        rs2 = durationModule.Duration(years=0, months=0, days=-6, h=-1, min=4, s=19991, us=0, modified=False)
        rs3 = durationModule.Duration(years=2, months=11, days=0, h=10, min=0, s=-3, us=0, modified=False, bd=1.0, cals="WE")
        rs4 = durationModule.Duration(years=0, months=0, days=0, h=23, min=100000, s=3000000, us=10, modified=False)
        # print('in test sub')
        # import code;code.interact(local=dict(globals(),**locals()))

if __name__=="__main__":
    unittest.main()