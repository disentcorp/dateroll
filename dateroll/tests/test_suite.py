import unittest
from dateroll.tests.calendarmath import TestStringMathMethods
from dateroll.tests.calendars import TestStringMethods
from dateroll.tests.date import TestDate
from dateroll.tests.ddh import TestDDH
from dateroll.tests.duration import TestDuration
from dateroll.tests.operations import TestOperations
from dateroll.tests.parser import TestParser
from dateroll.tests.parsers import TestParsers
from dateroll.tests.patterns import TestPatterns
from dateroll.tests.schedule import TestSchedule

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