import unittest
import itertools
import json

from dateroll import ddh

from dateroll.settings import default_settings
import dateroll.duration.yfs as yfs

DAY_COUNT_PATH = lambda: "tests/test_data/ql_data_yfs.json"
DAY_COUNT_PATH_UNIT = lambda: "tests/test_data/ql_data_yfs_unit.json"


def unit_tester(x1, x2, dic):
    """
    accepts date and compate dateroll day convention with
    expected values from json files
    """
    act360_1 = yfs.dc_ACT360(x1, x2, "")

    expected_360 = dic[
        f"{x1.to_string().split(' ')[0]}:{x2.to_string().split(' ')[0]}:ACT/360"
    ]
    # when passing None will call ACT365
    act365_1 = (x2 - x1).yf(None)

    expected_365 = dic[
        f"{x1.to_string().split(' ')[0]}:{x2.to_string().split(' ')[0]}:ACT/365"
    ]

    eur360 = (x2 - x1).yf("30E/360")

    expected_e360 = dic[
        f"{x1.to_string().split(' ')[0]}:{x2.to_string().split(' ')[0]}:30E360"
    ]

    # ie=(]
    ddh.settings.ie = "(]"
    bd_1 = yfs.dc_BD252(x1, x2, cals="BRuWE")
    expected_bd = dic[
        f"{x1.to_string().split(' ')[0]}:{x2.to_string().split(' ')[0]}:bd252:BRuWE:(]"
    ]
    # ie=[]
    ddh.settings.ie = "[]"
    bd1_ie = yfs.dc_BD252(x1, x2, cals="BRuWE")
    expected_bd_ie = dic[
        f"{x1.to_string().split(' ')[0]}:{x2.to_string().split(' ')[0]}:bd252:BRuWE:[]"
    ]

    comp1 = round(act360_1, 4) == round(expected_360, 4)
    comp2 = round(act365_1, 4) == round(expected_365, 4)
    comp3 = round(eur360, 4) == round(expected_e360, 4)
    comp4 = abs(bd_1 - expected_bd) < 0.10
    comp5 = abs(bd1_ie - expected_bd_ie) < 0.10

    rs = all([comp1, comp2, comp3, comp4, comp5])

    return rs, dic


class TestYFS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ddh.settings.convention = "MDY"

    @classmethod
    def tearDownClass(self):
        ddh.settings.convention = "MDY"

    def test_yfs(self):
        """
        test compares
        """
        with open(DAY_COUNT_PATH_UNIT(), "r") as f:
            dic = json.load(f)
        x1 = ddh("01012000")
        x2 = ddh("04032000")

        rs1 = unit_tester(x1, x2, dic)
        self.assertTrue(rs1)

        d1 = ddh("02012024")
        d2 = ddh("03012024")

        rs2 = unit_tester(d1, d2, dic)
        self.assertTrue(rs2)

        # reset
        ddh.settings.ie = default_settings["ie"]
        ddh.settings.convention = default_settings["convention"]

    def test_yfs_auto(self):
        """
        using itertools to test on many dates
        """

        days1 = [1, 2, 5, 6, 16, 28]
        months1 = [2, 3, 7]
        years1 = [2020, 2021]

        days2 = [8, 10, 23, 28, 29, 30, 31]
        months2 = [4, 5, 7]
        years2 = [2023, 2024]

        combo1 = list(itertools.product(*[months1, days1, years1]))
        combo2 = list(itertools.product(*[months2, days2, years2]))
        with open(DAY_COUNT_PATH(), "r") as f:
            dic = json.load(f)
        ddh.settings.convention = "MDY"
        for c1 in combo1:
            date_str = f"{c1[0]}/{c1[1]}/{c1[2]}"
            try:
                d1 = ddh(date_str)
            except Exception:

                continue
            for c2 in combo2:
                date_str2 = f"{c2[0]}/{c2[1]}/{c2[2]}"
                try:
                    d2 = ddh(date_str2)
                except Exception:

                    continue

                rs = unit_tester(d1, d2, dic)
                self.assertTrue(rs)

        # reset
        ddh.settings.convention = default_settings["convention"]


if __name__ == "__main__":
    unittest.main()
