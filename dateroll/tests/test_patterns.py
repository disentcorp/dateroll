import re
import unittest

from dateroll.parser import patterns


class TestPatterns(unittest.TestCase):

    def testCompileAll(self):
        for i in patterns.__dict__:
            print(i)
            pat = re.compile(i)
            assert pat is not None


if __name__ == "__main__":
    unittest.main()
