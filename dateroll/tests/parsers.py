import unittest
from unittest import expectedFailure

import string
import datetime
import random
import itertools

from dateroll.parser.parsers import *

TODAY = lambda: datetime.date.today()
TODAY_STRING = {
    "american":TODAY().strftime(r"%m/%d/%Y"),
    "european":TODAY().strftime(r"%d/%m/%Y"),
    "international": TODAY().strftime(r"%Y/%m/%d")
}

RANDOM_LOWERCASE_ALPHABETIC_STRING = lambda length: ''.join(random.choices(string.ascii_lowercase, k=length))
class TestParsers(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls): ...

    # @classmethod
    # def tearDownClass(self): ...

    def testparseTodayStringBase_success(self):
        # Generate pairs of test-conventions and test-today-string-indicators
        conventions = ['american','european','international']
        test_pairs = list(itertools.product(conventions, TODAYSTRINGVALUES))
        # Generate random string of length 8 for testing
        random_string = RANDOM_LOWERCASE_ALPHABETIC_STRING(8).replace('t','') 
        random_insertion_point = random.randint(0,8)
        for test_pair in test_pairs:
            convention = test_pair[0]
            # No today case
            if parseTodayString(random_string, convention) != random_string:
                assert False
            test_today_string_value = test_pair[1]
            test_string = random_string[:random_insertion_point] + test_today_string_value + random_string[random_insertion_point:]
            correct_answer = test_string.replace(test_today_string_value, TODAY_STRING[convention])
            if correct_answer != parseTodayString(test_string, convention):
                assert False
        
        assert True

    def testparseTodayStringWaterfall_success(self):
        today_string_permutations = list(itertools.permutations(TODAYSTRINGVALUES))
        random_string = RANDOM_LOWERCASE_ALPHABETIC_STRING(8).replace('t','') 
        random_insertion_points = random.sample(range(8),3)
        for permutation in today_string_permutations:
            leave_out = random.randint(0,3)
            leave_in = [permutation[i] for i in range(3) if i != leave_out]
            test_string = random_string[:random_insertion_points[0]] + leave_in[0] + random_string[random_insertion_points[0]:random_insertion_points[1]] + leave_in[1] + random_string[random_insertion_points[1]:random_insertion_points[2]]            
            
            correct_answer = test_string
            for t in TODAYSTRINGVALUES:
                if t in test_string:
                    correct_answer = correct_answer.replace(t, TODAY_STRING['american'])
                    break
            if correct_answer != parseTodayString(test_string, 'american'):
                assert False
        
        assert True

    @expectedFailure
    def testparseTodayString_failure(self):
        parseTodayString(RANDOM_LOWERCASE_ALPHABETIC_STRING(10), 'abcd')

    



    # def test_parseDateString(self):
    #     ...




    # def test_process_duration_match(self):
    #     ...


    # def test_parseDurationString(self):
    #     ...


    # def test_parseDateMathString(self):
    #     ...


    # def test_parseScheduleString(self):
    #     ...
if __name__ == "__main__":
    unittest.main()