from dateroll.parser import patterns
import re
import unittest

class TestPatterns(unittest.TestCase):

    def testCompileAll(self):
        for i in patterns.__dict__:
            print(i)
            pat = re.compile(i)
            assert pat is not None

if __name__ == "__main__":
    unittest.main()
