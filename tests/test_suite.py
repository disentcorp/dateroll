import unittest

from tests.test_calendarmath import TestStringMathMethods
from tests.test_calendars import TestStringMethods
from tests.test_date import TestDate
from tests.test_ddh import TestDDH, TestsPracticalExamples
from tests.test_duration import TestDuration
from tests.test_operations import TestOperations
from tests.test_parser import TestParser
from tests.test_parsers import TestParsers
from tests.test_patterns import TestPatterns
from tests.test_pretty import TestPretty
from tests.test_schedule import TestSchedule
from tests.test_settings import TestSettings
from tests.test_usage import TestUsage, TestUsageMore
from tests.test_usage2 import TestUsage as TestUsage2


def test_suite():
    """
    add test cases into suite
    """
    suite = unittest.TestSuite(
        [
            unittest.TestLoader().loadTestsFromTestCase(TestStringMathMethods),
            unittest.TestLoader().loadTestsFromTestCase(TestStringMethods),
            unittest.TestLoader().loadTestsFromTestCase(TestDate),
            unittest.TestLoader().loadTestsFromTestCase(TestDDH),
            unittest.TestLoader().loadTestsFromTestCase(TestsPracticalExamples),
            unittest.TestLoader().loadTestsFromTestCase(TestDuration),
            unittest.TestLoader().loadTestsFromTestCase(TestOperations),
            unittest.TestLoader().loadTestsFromTestCase(TestParser),
            unittest.TestLoader().loadTestsFromTestCase(TestParsers),
            unittest.TestLoader().loadTestsFromTestCase(TestPatterns),
            unittest.TestLoader().loadTestsFromTestCase(TestPretty),
            unittest.TestLoader().loadTestsFromTestCase(TestSchedule),
            unittest.TestLoader().loadTestsFromTestCase(TestUsage),
            unittest.TestLoader().loadTestsFromTestCase(TestUsageMore),
            unittest.TestLoader().loadTestsFromTestCase(TestSettings),
            unittest.TestLoader().loadTestsFromTestCase(TestUsage2),
        ]
    )
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    suite = test_suite()
    runner.run(suite)
