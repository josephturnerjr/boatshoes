import unittest
import sys
import os.path
sys.path.append(os.path.join(os.path.split(__file__)[0], '..'))
from boatshoes.DaemonContext import DaemonContext

class TestDaemonContext(unittest.TestCase):
    def setUp(self):
        pass

    def test_daemonize(self):
        try:
            with DaemonContext(True) as dc:
                # only the child makes it in
                print "yep" # won't be printed
        except SystemExit, e:
            self.assertTrue(e.code == 0)

    def test_return_code(self):
        try:
            with DaemonContext(True) as dc:
                # only the child makes it in
                print "yep" # won't be printed
                dc.return_value = -1
        except SystemExit, e:
            self.assertTrue(e.code == -1)

    def test_noop(self):
        # Shouldn't throw
        with DaemonContext(False) as dc:
            # If you pass in False, DaemonContext is a no-op
            # print "yep" # this one would be printed
            dc.return_value = -1

if __name__ == "__main__":
    unittest.main()
