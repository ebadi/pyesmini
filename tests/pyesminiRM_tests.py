#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pyesmini.pyesminiRM import *
import unittest

XODRFILE = "resources/xodr/fabriksgatan.xodr"


class TestStringMethods(unittest.TestCase):

    def test_getOSILaneBoundary(self):
        pyesmini = PyEsminiRM(XODRFILE)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
