import unittest
from dateroll.tests.test_calendarmath import TestStringMathMethods
from dateroll.tests.test_calendars import TestStringMethods
from dateroll.tests.test_date import TestDate
from dateroll.tests.test_ddh import TestDDH
from dateroll.tests.test_duration import TestDuration
from dateroll.tests.test_operations import TestOperations
from dateroll.tests.test_parser import TestParser
from dateroll.tests.test_parsers import TestParsers
from dateroll.tests.test_patterns import TestPatterns
from dateroll.tests.test_schedule import TestSchedule

def test_suite():
    '''
        add test cases into suite
    '''
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStringMathMethods))
    suite.addTest(unittest.makeSuite(TestStringMethods))
    suite.addTest(unittest.makeSuite(TestDate))
    suite.addTest(unittest.makeSuite(TestDDH))
    suite.addTest(unittest.makeSuite(TestDuration))
    suite.addTest(unittest.makeSuite(TestOperations))
    suite.addTest(unittest.makeSuite(TestParser))
    suite.addTest(unittest.makeSuite(TestParsers))
    suite.addTest(unittest.makeSuite(TestPatterns))
    suite.addTest(unittest.makeSuite(TestSchedule))
    return suite

if __name__=='__main__':
    runner = unittest.TextTestRunner()
    suite = test_suite()
    runner.run(suite)