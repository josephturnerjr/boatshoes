import unittest
import sys
import os.path
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
from boatshoes.Privileges import get_int_mode
from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class TestPrivileges(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_int_mode_octal(self):
        self.assertTrue(0644 == get_int_mode("0644"))
        self.assertRaises(OSError, get_int_mode, "06440")
        self.assertTrue(0004 == get_int_mode("0004"))
        self.assertTrue(0 == get_int_mode("0000"))
        self.assertTrue(0 == get_int_mode("0"))
        self.assertTrue(04 == get_int_mode("4"))

    def test_get_int_mode_str(self):
        for i in 'ugoa':
            for j in '+-=':
                for k in powerset('rwxXst'):
                    get_int_mode(i + j + "".join(k))
                for k in 'ugo':
                    get_int_mode(i + j + k)
        self.assertRaises(OSError, get_int_mode, "ua+w")
        self.assertRaises(OSError, get_int_mode, "u+b")
        get_int_mode("+w")
        self.assertRaises(OSError, get_int_mode, "ub")
        self.assertRaises(OSError, get_int_mode, "ur")

if __name__ == "__main__":
    unittest.main()
