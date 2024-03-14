import unittest

from tests.test_calendarmath import TestStringMathMethods
from tests.test_calendars import TestStringMethods
from tests.test_date import TestDate
from tests.test_ddh import TestDDH, TestsPracticalExamples
from tests.test_duration import TestDuration
from tests.test_operations import TestOperations
from tests.test_parser import TestParser
from tests.test_parsers import TestParsers
from tests.test_pretty import TestPretty
from tests.test_patterns import TestPatterns
from tests.test_schedule import TestSchedule
from tests.test_settings import TestSettings
from tests.test_usage import TestUsage, TestUsageMore

def test_suite():
    '''
        add test cases into suite
    '''
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStringMathMethods))
    suite.addTest(unittest.makeSuite(TestStringMethods))
    suite.addTest(unittest.makeSuite(TestDate))
    suite.addTest(unittest.makeSuite(TestDDH))
    suite.addTest(unittest.makeSuite(TestsPracticalExamples))
    suite.addTest(unittest.makeSuite(TestDuration))
    suite.addTest(unittest.makeSuite(TestOperations))
    suite.addTest(unittest.makeSuite(TestParser))
    suite.addTest(unittest.makeSuite(TestParsers))
    suite.addTest(unittest.makeSuite(TestPatterns))
    suite.addTest(unittest.makeSuite(TestPretty))
    suite.addTest(unittest.makeSuite(TestSchedule))
    suite.addTest(unittest.makeSuite(TestUsage))
    suite.addTest(unittest.makeSuite(TestUsageMore))
    suite.addTest(unittest.makeSuite(TestSettings))
    return suite

if __name__=='__main__':
    runner = unittest.TextTestRunner()
    suite = test_suite()
    runner.run(suite)