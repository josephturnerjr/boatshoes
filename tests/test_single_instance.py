import unittest
import sys
import os.path
sys.path.append(os.path.join(os.path.split(__file__)[0], '..'))

from boatshoes.SingleInstance import SingleInstance, RunningInstanceError
from multiprocessing import Process


def create_si(name):
    try:
        SingleInstance(name)
    except RunningInstanceError:
        sys.exit(66)


class TestSingleInstance(unittest.TestCase):
    def setUp(self):
        self.name = "/tmp/testlock"

    def test_lockfile(self):
        SingleInstance(self.name)
        p = Process(target=create_si, args=(self.name,))
        p.start()
        p.join()
        self.assertTrue(p.exitcode == 66)

if __name__ == "__main__":
    unittest.main()
