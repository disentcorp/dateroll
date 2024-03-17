import re
import unittest
import io
from contextlib import redirect_stdout


from dateroll import *

class TestPretty(unittest.TestCase):

    def testPretty(self):
        
        # 1 cal
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('5/5/95+5d').cal
            output = buf.getvalue()
            self.assertGreater(len(output),300) # range is for variable ansi chars
            self.assertLess(len(output),400)
       
        # 2 cal
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('5/5/95+10y').cal
            output = buf.getvalue()
            self.assertGreater(len(output),600)  # range is for variable ansi chars
            self.assertLess(len(output),1000)

        # 2 cal
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('3/4/24-10y').cal
            output = buf.getvalue()
            self.assertGreater(len(output),600)  # range is for variable ansi chars
            self.assertLess(len(output),1000)

        # 1 date 1 cal
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('5/5/95').cal
            self.assertGreater(len(output),300) # range is for variable ansi chars
            self.assertLess(len(output),1025)

        # 1 schedule 2 cal
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('t,t+5y,1m').cal
            self.assertGreater(len(output),600)  # range is for variable ansi chars
            self.assertLess(len(output),1000)

if __name__ == "__main__":
    unittest.main()
