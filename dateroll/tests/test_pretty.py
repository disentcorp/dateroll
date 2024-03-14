import re
import unittest
import io
from contextlib import redirect_stdout


from dateroll import *

class TestPretty(unittest.TestCase):

    def testPretty(self):
        
        # 1 cal
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('5/5/95+5d').src
            output = buf.getvalue()
            self.assertGreater(len(output),300) # range is for variable ansi chars
            self.assertLess(len(output),400)
       
        # 2 cal
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('5/5/95+10y').src
            output = buf.getvalue()
            self.assertGreater(len(output),600)  # range is for variable ansi chars
            self.assertLess(len(output),1000)

        # 2 cal
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('3/4/24-10y').src
            output = buf.getvalue()
            self.assertGreater(len(output),600)  # range is for variable ansi chars
            self.assertLess(len(output),1000)

        # no cal / no shift done
        with io.StringIO() as buf, redirect_stdout(buf):
            s = ddh('5/5/95').src
            output = buf.getvalue()
            self.assertEqual(output,'')

if __name__ == "__main__":
    unittest.main()
